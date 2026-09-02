"""Deterministic checks for the composed Spec Coding Harness test fixture."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "spec-coding-harness"
FIXTURE_RELATIVE_ROOT = FIXTURE_ROOT.relative_to(REPOSITORY_ROOT).as_posix()
REQUIRED_FILES = (
    "AGENTS.md",
    "adoption-baseline.json",
    "final-workflow-route.json",
    "source-inventory.json",
    "review-receipt.json",
)
REQUIRED_INSTRUCTION = (
    "compiled test fixture",
    "Before any source-derived action",
    "do not infer publication, authority, or target scope",
    "Ready is persistent; Runnable is a runtime derivation",
    "Task Commit is neither Task Done, Requirement integration, Merge, Release, nor deployment",
    "Requirement Integration, then its AC Gate, then Requirement Push",
    "Verification is read-only",
    "Run deterministic checks first",
    "sole writer",
    "Do not merge to `main`, tag, release, or change version fields",
)


def _load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return None, f"cannot read {path.relative_to(REPOSITORY_ROOT)}: {error}"
    if not isinstance(value, dict):
        return None, f"{path.relative_to(REPOSITORY_ROOT)} must be a JSON object"
    return value, None


def _manifest_version_matches() -> bool:
    version = (REPOSITORY_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    manifest = (REPOSITORY_ROOT / "docs/manifest.yaml").read_text(encoding="utf-8")
    match = re.search(r'^spec_coding_version:\s*["\']?([^"\'\s]+)["\']?\s*$', manifest, flags=re.MULTILINE)
    return match is not None and match.group(1) == version


def _source_blocks(value: dict[str, Any]) -> list[dict[str, Any]] | None:
    blocks = value.get("source_blocks")
    if not isinstance(blocks, list) or not blocks:
        return None
    if not all(isinstance(item, dict) and isinstance(item.get("ref"), str) and isinstance(item.get("content_sha256"), str) for item in blocks):
        return None
    return blocks


def _source_inventory_matches_current(ledger: dict[str, Any]) -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="harness-fixture-") as temporary:
        temporary_root = Path(temporary)
        candidates = temporary_root / "candidates.json"
        inventory = temporary_root / "inventory.json"
        baseline_path = f"{FIXTURE_RELATIVE_ROOT}/adoption-baseline.json"
        resolve = subprocess.run(
            [
                sys.executable, "-m", "tools.harness_compiler", "resolve",
                "--spec-root", str(REPOSITORY_ROOT), "--target-root", str(FIXTURE_ROOT),
                "--adoption-baseline", baseline_path, "--output", str(candidates),
            ],
            cwd=REPOSITORY_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if resolve.returncode != 0:
            return False, "could not resolve the current fixture source route"
        scan = subprocess.run(
            [
                sys.executable, "-m", "tools.harness_compiler", "scan",
                "--spec-root", str(REPOSITORY_ROOT), "--candidates", str(candidates), "--output", str(inventory),
            ],
            cwd=REPOSITORY_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if scan.returncode != 0:
            return False, "could not scan the current fixture source route"
        current, error = _load_json(inventory)
        if error or current is None:
            return False, "could not read freshly scanned fixture source inventory"
    return _source_blocks(ledger) == _source_blocks(current), "fixture source inventory digest ledger differs from current Canonical sources"


def _check_values(baseline: dict[str, Any], route: dict[str, Any], instruction: str, receipt: dict[str, Any], ledger: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if baseline.get("target", {}).get("id") != "spec-coding" or baseline.get("publication", {}).get("component_root") != ".":
        errors.append("Adoption Baseline does not bind the self-hosted test fixture")
    if baseline.get("workflow_route") != f"{FIXTURE_RELATIVE_ROOT}/final-workflow-route.json":
        errors.append("Adoption Baseline does not bind the fixture workflow route")
    if route.get("stages") != ["04", "05", "06"]:
        errors.append("Final Workflow Route is not the intended implementation-to-verification path")
    absent = [phrase for phrase in REQUIRED_INSTRUCTION if phrase not in instruction]
    if absent:
        errors.append(f"Harness fixture instruction lacks required guarantees: {absent}")
    if receipt.get("independent") is not True or receipt.get("verdict") != "pass" or receipt.get("findings"):
        errors.append("independent semantic review receipt does not pass")
    if _source_blocks(ledger) is None:
        errors.append("fixture source inventory ledger is malformed")
    return errors


def verify_fixture() -> list[str]:
    missing = [path for path in REQUIRED_FILES if not (FIXTURE_ROOT / path).is_file()]
    if missing:
        return [f"missing required Harness fixture files: {', '.join(missing)}"]
    baseline, baseline_error = _load_json(FIXTURE_ROOT / "adoption-baseline.json")
    route, route_error = _load_json(FIXTURE_ROOT / "final-workflow-route.json")
    receipt, receipt_error = _load_json(FIXTURE_ROOT / "review-receipt.json")
    ledger, ledger_error = _load_json(FIXTURE_ROOT / "source-inventory.json")
    errors = [error for error in (baseline_error, route_error, receipt_error, ledger_error) if error]
    if errors:
        return errors
    assert baseline is not None and route is not None and receipt is not None and ledger is not None
    instruction = (FIXTURE_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    errors.extend(_check_values(baseline, route, instruction, receipt, ledger))
    if not _manifest_version_matches():
        errors.append("VERSION and docs/manifest.yaml spec_coding_version differ")
    source_matches, source_message = _source_inventory_matches_current(ledger)
    if not source_matches:
        errors.append(source_message)
    return errors


def _negative_probe() -> int:
    baseline = {"target": {"id": "wrong"}, "publication": {"component_root": "."}, "workflow_route": "wrong.json"}
    route = {"stages": ["04", "05"]}
    receipt = {"independent": False, "verdict": "fail", "findings": ["missing"]}
    ledger = {"source_blocks": []}
    caught = _check_values(baseline, route, "", receipt, ledger)
    if len(caught) < 5:
        print("negative probe did not reject every invalid Harness fixture condition", file=sys.stderr)
        return 0
    print("intentional invalid Harness fixture conditions rejected", file=sys.stderr)
    return 1


def main() -> int:
    if sys.argv[1:] == ["--probe"]:
        return _negative_probe()
    if sys.argv[1:]:
        print("usage: verify_spec_coding_harness.py [--probe]", file=sys.stderr)
        return 2
    errors = verify_fixture()
    if errors:
        print("; ".join(errors), file=sys.stderr)
        return 1
    print("Spec Coding Harness test fixture passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
