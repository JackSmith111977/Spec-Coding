"""Resolve V2 canonical and Adoption source candidates from a valid baseline."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .shared import (
    CompilerInputError,
    adoption_source_entries,
    diagnostic,
    load_adoption_baseline,
    read_json,
    read_yaml,
    relative_path,
    report,
    require_mapping,
    validate_adoption_baseline,
)


def _string_list(value: Any, label: str, diagnostics: list[dict[str, Any]]) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        diagnostics.append(diagnostic("INVALID_ROUTE_FIELD", f"{label} must be a string array"))
        return []
    return value


def _document_path(canonical_root: str, path: str) -> str:
    root = canonical_root.strip("/")
    normalized = path.strip("/")
    return normalized if not root or normalized.startswith(f"{root}/") else f"{root}/{normalized}"


def _candidate(
    result: list[dict[str, Any]], seen: set[str], path: str, document_kind: str, reason: str
) -> None:
    if path not in seen:
        result.append({"kind": "canonical", "path": path, "document_kind": document_kind, "reason": reason})
        seen.add(path)


def resolve(spec_root: Path, target_root: Path, baseline_path: str, manifest_path: str) -> dict[str, Any]:
    baseline, resolved_baseline_path, baseline_sha256 = load_adoption_baseline(spec_root, baseline_path)
    diagnostics = validate_adoption_baseline(baseline)
    if diagnostics:
        return report("resolve", False, diagnostics)

    try:
        manifest = require_mapping(read_yaml(relative_path(spec_root, manifest_path)), "manifest")
        route = require_mapping(read_json(relative_path(spec_root, baseline["workflow_route"])), "final workflow route")
    except CompilerInputError as error:
        return report("resolve", False, [diagnostic("INPUT_ERROR", str(error))])

    canonical_root = manifest.get("canonical_root")
    if not isinstance(canonical_root, str) or not canonical_root.strip():
        return report("resolve", False, [diagnostic("INVALID_MANIFEST", "manifest.canonical_root is required")])

    version_path = relative_path(spec_root, "VERSION")
    try:
        spec_version = version_path.read_text(encoding="utf-8").strip()
    except OSError as error:
        return report("resolve", False, [diagnostic("INPUT_ERROR", f"cannot read VERSION: {error}")])
    if not spec_version:
        diagnostics.append(diagnostic("EMPTY_VERSION", "VERSION is empty"))

    stage_by_id = {item.get("id"): item for item in manifest.get("stages", []) if isinstance(item, dict) and isinstance(item.get("id"), str)}
    rule_by_id = {
        item.get("id"): item
        for item in manifest.get("rule_documents", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    exception_by_id = {
        item.get("id"): item
        for item in manifest.get("exception_workflows", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }

    stage_ids = _string_list(route.get("stages"), "route.stages", diagnostics)
    rule_ids = _string_list(route.get("rule_ids"), "route.rule_ids", diagnostics)
    exception_ids = _string_list(route.get("exception_ids"), "route.exception_ids", diagnostics)
    if not stage_ids:
        diagnostics.append(diagnostic("EMPTY_WORKFLOW_ROUTE", "route.stages must select at least one stage"))
    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    unresolved: list[dict[str, str]] = []
    selected_stage_names: set[str] = set()

    for stage_id in stage_ids:
        stage = stage_by_id.get(stage_id)
        if not isinstance(stage, dict):
            unresolved.append({"kind": "stage", "id": stage_id})
            continue
        if isinstance(stage.get("name"), str):
            selected_stage_names.add(stage["name"])
        for path in stage.get("documents", []):
            if isinstance(path, str):
                _candidate(candidates, seen, _document_path(canonical_root, path), "workflow", f"route stage {stage_id}")
            else:
                diagnostics.append(diagnostic("INVALID_DOCUMENT_PATH", "stage document path must be a string", stage=stage_id))

    selected_rules: list[dict[str, Any]] = []
    if rule_ids:
        for rule_id in rule_ids:
            rule = rule_by_id.get(rule_id)
            if not isinstance(rule, dict):
                unresolved.append({"kind": "rule", "id": rule_id})
            else:
                selected_rules.append(rule)
    else:
        for rule in rule_by_id.values():
            applies_to = rule.get("applies_to")
            if applies_to == "all" or (isinstance(applies_to, list) and selected_stage_names.intersection(applies_to)):
                selected_rules.append(rule)

    for rule in selected_rules:
        path = rule.get("path")
        if isinstance(path, str):
            _candidate(candidates, seen, _document_path(canonical_root, path), "rule", f"applicable rule {rule.get('id', 'unknown')}")
        else:
            diagnostics.append(diagnostic("INVALID_RULE_PATH", "rule path must be a string", rule=rule.get("id")))

    for exception_id in exception_ids:
        workflow = exception_by_id.get(exception_id)
        if not isinstance(workflow, dict):
            unresolved.append({"kind": "exception", "id": exception_id})
            continue
        for path in workflow.get("documents", []):
            if isinstance(path, str):
                _candidate(candidates, seen, _document_path(canonical_root, path), "exception", f"triggered exception {exception_id}")
            else:
                diagnostics.append(diagnostic("INVALID_DOCUMENT_PATH", "exception document path must be a string", exception=exception_id))

    for entry in candidates:
        try:
            exists = relative_path(spec_root, entry["path"]).is_file()
        except CompilerInputError:
            exists = False
        if not exists:
            diagnostics.append(diagnostic("MISSING_CANDIDATE_SOURCE", "canonical candidate does not exist", path=entry["path"]))

    candidates.extend(adoption_source_entries(baseline))
    return report(
        "resolve",
        not diagnostics and not unresolved,
        diagnostics,
        spec_root=str(spec_root.resolve()),
        target_root=str(target_root.resolve()),
        spec_version=spec_version,
        baseline={
            "path": str(resolved_baseline_path),
            "sha256": baseline_sha256,
            "target_id": baseline["target"]["id"],
            "publication_boundary": baseline["publication"]["boundary"],
        },
        route=baseline["workflow_route"],
        candidate_sources=candidates,
        unresolved_route_items=unresolved,
    )
