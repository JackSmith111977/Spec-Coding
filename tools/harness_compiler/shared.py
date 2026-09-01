"""Small, dependency-light primitives shared by Harness Compiler V2 commands."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

import yaml


BOUNDARIES = {"local", "shared", "repository-native"}
SUPPORT_MODES = {"native", "composable", "external", "unavailable", "unknown"}


class CompilerInputError(ValueError):
    """Raised when an input cannot be safely interpreted."""


def diagnostic(code: str, message: str, **details: Any) -> dict[str, Any]:
    return {"code": code, "message": message, **{key: value for key, value in details.items() if value is not None}}


def report(tool: str, passed: bool, diagnostics: list[dict[str, Any]], **extra: Any) -> dict[str, Any]:
    return {"tool": tool, "passed": passed, "diagnostic_count": len(diagnostics), "diagnostics": diagnostics, **extra}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_text(canonical_json(value))


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise CompilerInputError(f"cannot read {path}: {error}") from error
    except json.JSONDecodeError as error:
        raise CompilerInputError(f"cannot parse JSON {path}: {error}") from error


def read_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise CompilerInputError(f"cannot read {path}: {error}") from error
    except yaml.YAMLError as error:
        raise CompilerInputError(f"cannot parse YAML {path}: {error}") from error


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def relative_path(root: Path, raw_path: str) -> Path:
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise CompilerInputError("path must be a non-empty relative string")
    candidate = Path(raw_path)
    if candidate.is_absolute():
        raise CompilerInputError(f"path must be relative: {raw_path}")
    resolved_root = root.resolve()
    resolved = (resolved_root / candidate).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as error:
        raise CompilerInputError(f"path escapes root: {raw_path}") from error
    return resolved


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CompilerInputError(f"{label} must be an object")
    return value


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CompilerInputError(f"{label} must be a non-empty string")
    return value


def _fact(ref: str, fact: str, value: Any) -> dict[str, Any]:
    return {
        "kind": "adoption",
        "ref": ref,
        "fact": fact,
        "value": value,
        "content_sha256": sha256_json(value),
    }


def load_adoption_baseline(spec_root: Path, raw_path: str) -> tuple[dict[str, Any], Path, str]:
    path = relative_path(spec_root, raw_path)
    baseline = require_mapping(read_json(path), "adoption baseline")
    return baseline, path, sha256_json(baseline)


def validate_adoption_baseline(baseline: dict[str, Any]) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    if baseline.get("adoption_version") != 1:
        diagnostics.append(diagnostic("INVALID_ADOPTION_VERSION", "adoption_version must be 1"))

    for field in ("target", "spec_workspace", "publication", "integration"):
        if not isinstance(baseline.get(field), dict):
            diagnostics.append(diagnostic("MISSING_ADOPTION_FACT", f"adoption baseline needs {field}"))

    target = baseline.get("target", {})
    workspace = baseline.get("spec_workspace", {})
    publication = baseline.get("publication", {})
    integration = baseline.get("integration", {})
    if not isinstance(target.get("id"), str) or not target["id"].strip():
        diagnostics.append(diagnostic("MISSING_TARGET_ID", "adoption target.id is required"))
    if not isinstance(workspace.get("id"), str) or not workspace["id"].strip():
        diagnostics.append(diagnostic("MISSING_SPEC_WORKSPACE", "adoption spec_workspace.id is required"))
    if publication.get("boundary") not in BOUNDARIES:
        diagnostics.append(diagnostic("INVALID_PUBLICATION_BOUNDARY", "publication.boundary is invalid"))
    try:
        relative_path(Path("."), publication.get("component_root", ""))
    except CompilerInputError:
        diagnostics.append(diagnostic("INVALID_COMPONENT_ROOT", "publication.component_root must be a relative path"))
    if not isinstance(integration.get("scope"), str) or not integration["scope"].strip():
        diagnostics.append(diagnostic("MISSING_INTEGRATION_SCOPE", "integration.scope is required"))
    if not isinstance(baseline.get("workflow_route"), str) or not baseline["workflow_route"].strip():
        diagnostics.append(diagnostic("MISSING_WORKFLOW_ROUTE", "workflow_route is required"))

    constraints = baseline.get("constraints")
    if not isinstance(constraints, list) or not constraints:
        diagnostics.append(diagnostic("MISSING_ADOPTION_CONSTRAINTS", "constraints must be a non-empty array"))
    else:
        seen: set[str] = set()
        for constraint in constraints:
            if not isinstance(constraint, dict) or not isinstance(constraint.get("id"), str) or not constraint["id"].strip():
                diagnostics.append(diagnostic("INVALID_ADOPTION_CONSTRAINT", "each constraint needs an id"))
                continue
            if constraint["id"] in seen:
                diagnostics.append(diagnostic("DUPLICATE_ADOPTION_CONSTRAINT", "constraint ids must be unique", constraint=constraint["id"]))
            seen.add(constraint["id"])
            if "value" not in constraint:
                diagnostics.append(diagnostic("INVALID_ADOPTION_CONSTRAINT", "each constraint needs a value", constraint=constraint["id"]))
    return diagnostics


def adoption_source_entries(baseline: dict[str, Any]) -> list[dict[str, Any]]:
    entries = [
        _fact("adoption://target-identity", "target-identity", baseline["target"]),
        _fact("adoption://spec-workspace", "spec-workspace", baseline["spec_workspace"]),
        _fact("adoption://publication-boundary", "publication-boundary", baseline["publication"]),
        _fact("adoption://integration-boundary", "integration-boundary", baseline["integration"]),
    ]
    for constraint in baseline.get("constraints", []):
        entries.append(_fact(f"adoption://constraint/{constraint['id']}", constraint["id"], constraint["value"]))
    return entries


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.harness-compiler.tmp")
    try:
        temporary.write_bytes(content)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
