"""Run generic deterministic checks against composed Harness outputs."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from .shared import diagnostic, relative_path, report, sha256_text
from .state import validate_state


def _run(target_root: Path, component: str, label: str, command: Any, expect_success: bool, timeout: int) -> dict[str, Any] | None:
    if not isinstance(command, list) or not command or not all(isinstance(part, str) and part for part in command):
        return diagnostic("INVALID_COMMAND", f"{label} must be a non-empty string array", component=component)
    try:
        result = subprocess.run(command, cwd=target_root, shell=False, text=True, capture_output=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as error:
        return diagnostic("COMMAND_EXECUTION_ERROR", f"{label} could not run: {error}", component=component)
    passed = result.returncode == 0 if expect_success else result.returncode != 0
    if passed:
        return None
    return diagnostic(
        "COMMAND_UNEXPECTED_RESULT",
        f"{label} returned an unexpected exit code",
        component=component,
        command=command,
        returncode=result.returncode,
        stdout=result.stdout[-1000:],
        stderr=result.stderr[-1000:],
    )


def verify(
    spec_root: Path,
    target_root: Path,
    baseline: dict[str, Any],
    baseline_sha256: str,
    state: dict[str, Any],
    source_inventory: dict[str, Any],
    timeout: int,
) -> dict[str, Any]:
    diagnostics, summary = validate_state(state, spec_root, target_root, baseline, baseline_sha256, source_inventory)
    if diagnostics:
        return report("verify", False, diagnostics, summary=summary, executed_components=0)
    executed_components = 0
    for component in state.get("components", []):
        component_id = component.get("id", "unknown")
        for output in component.get("outputs", []):
            target_raw = output.get("target")
            try:
                target = relative_path(target_root, target_raw)
            except Exception as error:
                diagnostics.append(diagnostic("INVALID_COMPONENT_TARGET", str(error), component=component_id, target=target_raw))
                continue
            if not target.is_file():
                diagnostics.append(diagnostic("MISSING_COMPONENT_TARGET", "composed target does not exist", component=component_id, target=target_raw))
                continue
            actual_sha = sha256_text(target.read_text(encoding="utf-8"))
            if actual_sha != output.get("content_sha256"):
                diagnostics.append(diagnostic("COMPOSED_ARTIFACT_DRIFT", "target content differs from composition receipt", component=component_id, target=target_raw))
        verification = component.get("verification")
        if not verification:
            continue
        if not isinstance(verification, dict):
            diagnostics.append(diagnostic("INVALID_COMPONENT_VERIFICATION", "verification must be an object", component=component_id))
            continue
        executed_components += 1
        if verification.get("deterministic") is True and "failure_command" not in verification:
            diagnostics.append(diagnostic("MISSING_FAILURE_PATH", "deterministic mechanism needs failure_command", component=component_id))
        for label in ("load_command", "command"):
            if label in verification:
                failure = _run(target_root, component_id, label, verification[label], True, timeout)
                if failure:
                    diagnostics.append(failure)
        if "failure_command" in verification:
            failure = _run(target_root, component_id, "failure_command", verification["failure_command"], False, timeout)
            if failure:
                diagnostics.append(failure)
    return report("verify", not diagnostics, diagnostics, summary=summary, executed_components=executed_components)
