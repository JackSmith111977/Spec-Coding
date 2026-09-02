"""Run generic deterministic checks against composed Harness outputs."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from .shared import diagnostic, relative_path, report, runtime_surfaces_for_target, sha256_text
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
    executed_probes = 0
    probe_receipts: list[dict[str, Any]] = []
    probe_classes = {"surface": 0, "semantic": 0, "runtime-visibility": 0}
    limitations: list[dict[str, Any]] = []
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
        if not isinstance(verification, dict):
            diagnostics.append(diagnostic("INVALID_COMPONENT_VERIFICATION", "verification must be an object", component=component_id))
            continue
        executed_components += 1
        for limitation in verification.get("cannot_cover", []):
            limitations.append({"component": component_id, "cannot_cover": limitation})
        for probe in verification.get("probes", []):
            if not isinstance(probe, dict):
                continue
            probe_id = probe.get("id", "unknown")
            probe_type = probe.get("type")
            if probe_type not in probe_classes:
                diagnostics.append(diagnostic("INVALID_COMPONENT_PROBE", "probe type is invalid", component=component_id, probe=probe_id))
                continue
            executed_probes += 1
            probe_classes[probe_type] += 1
            if probe_type == "runtime-visibility":
                invisible = [
                    output.get("target")
                    for output in component.get("outputs", [])
                    if not runtime_surfaces_for_target(baseline.get("runtime"), output.get("target"))
                ]
                passed = not invisible
                probe_receipts.append({"component": component_id, "probe": probe_id, "type": probe_type, "passed": passed, "covers": probe.get("covers", [])})
                if invisible:
                    diagnostics.append(diagnostic("RUNTIME_VISIBILITY_VIOLATION", "runtime-visibility probe found outputs outside declared loader surfaces", component=component_id, probe=probe_id, targets=invisible))
                continue
            expect_success = probe.get("expect") == "pass"
            failure = _run(target_root, component_id, f"probe:{probe_id}", probe.get("command"), expect_success, timeout)
            probe_receipts.append({"component": component_id, "probe": probe_id, "type": probe_type, "passed": failure is None, "covers": probe.get("covers", [])})
            if failure:
                diagnostics.append(failure)
    return report(
        "verify",
        not diagnostics,
        diagnostics,
        summary=summary,
        executed_components=executed_components,
        executed_probes=executed_probes,
        probe_classes=probe_classes,
        probe_receipts=probe_receipts,
        declared_limitations=limitations,
    )
