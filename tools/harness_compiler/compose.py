"""Materialize Agent-authored staged Harness outputs without deciding their semantics."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .shared import atomic_write, diagnostic, relative_path, report, sha256_bytes


def compose(target_root: Path, baseline: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    diagnostics: list[dict[str, Any]] = []
    receipts: list[dict[str, Any]] = []
    planned_writes: list[dict[str, Any]] = []
    planned_targets: set[Path] = set()
    component_root = baseline.get("publication", {}).get("component_root", "")
    try:
        allowed_root = relative_path(target_root, component_root)
    except Exception as error:
        return report("compose", False, [diagnostic("INVALID_COMPONENT_ROOT", str(error))])

    for component in state.get("components", []):
        if not isinstance(component, dict):
            continue
        component_id = component.get("id", "unknown")
        for output in component.get("outputs", []):
            if not isinstance(output, dict):
                continue
            target_raw = output.get("target")
            staged_raw = output.get("staged")
            action = output.get("action")
            expected_sha = output.get("content_sha256")
            try:
                target = relative_path(target_root, target_raw)
                target.relative_to(allowed_root)
                staged = relative_path(target_root, staged_raw)
            except Exception as error:
                diagnostics.append(diagnostic("PUBLICATION_BOUNDARY_VIOLATION", str(error), component=component_id, target=target_raw))
                continue
            if not staged.is_file():
                diagnostics.append(diagnostic("MISSING_STAGED_ARTIFACT", "Agent-staged artifact is missing", component=component_id, staged=staged_raw))
                continue
            content = staged.read_bytes()
            actual_sha = sha256_bytes(content)
            if actual_sha != expected_sha:
                diagnostics.append(diagnostic("STAGED_ARTIFACT_DRIFT", "staged artifact digest does not match Compilation State", component=component_id, staged=staged_raw))
                continue
            if action == "create" and target.exists():
                diagnostics.append(diagnostic("CREATE_TARGET_EXISTS", "create output already exists", component=component_id, target=target_raw))
                continue
            if action == "modify" and not target.is_file():
                diagnostics.append(diagnostic("MODIFY_TARGET_MISSING", "modify output does not exist", component=component_id, target=target_raw))
                continue
            if action not in {"create", "modify"}:
                diagnostics.append(diagnostic("INVALID_COMPONENT_ACTION", "output action must be create or modify", component=component_id))
                continue
            if target in planned_targets:
                diagnostics.append(diagnostic("DUPLICATE_COMPONENT_OUTPUT_TARGET", "multiple outputs target the same file", component=component_id, target=target_raw))
                continue
            planned_targets.add(target)
            planned_writes.append(
                {
                    "component": component_id,
                    "action": action,
                    "target": target,
                    "target_raw": target_raw,
                    "content": content,
                    "content_sha256": actual_sha,
                }
            )

    # A failed composition must not leave a partially materialized Harness.
    # Validate every staged output before the Single Writer Boundary mutates
    # the target workspace.
    if diagnostics:
        return report("compose", False, diagnostics, receipts=receipts, written_outputs=0)

    for planned in planned_writes:
        try:
            atomic_write(planned["target"], planned["content"])
        except OSError as error:
            diagnostics.append(
                diagnostic(
                    "COMPOSE_WRITE_ERROR",
                    f"could not materialize staged artifact: {error}",
                    component=planned["component"],
                    target=planned["target_raw"],
                )
            )
            break
        receipts.append(
            {
                "component": planned["component"],
                "action": planned["action"],
                "target": planned["target_raw"],
                "content_sha256": planned["content_sha256"],
            }
        )
    return report("compose", not diagnostics, diagnostics, receipts=receipts, written_outputs=len(receipts))
