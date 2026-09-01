"""Deterministic repository gate for the composed Spec Coding Harness."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "VERSION",
    "docs/manifest.yaml",
    "harness/adoption-baseline.json",
    "harness/final-workflow-route.json",
    "harness/source-inventory.json",
    "AGENTS.md",
    "harness/review-receipt.json",
)
REQUIRED_INSTRUCTION = (
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
        return None, f"cannot read {path.relative_to(ROOT)}: {error}"
    if not isinstance(value, dict):
        return None, f"{path.relative_to(ROOT)} must be a JSON object"
    return value, None


def _branch() -> str | None:
    result = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, text=True, capture_output=True, check=False)
    return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else None


def _manifest_version_matches() -> bool:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    manifest = (ROOT / "docs/manifest.yaml").read_text(encoding="utf-8")
    match = re.search(r'^spec_coding_version:\s*["\']?([^"\'\s]+)["\']?\s*$', manifest, flags=re.MULTILINE)
    return match is not None and match.group(1) == version


def _release_guard_errors(trusted_base: bool, protected_fields_clean: bool, tagged: bool) -> list[str]:
    errors: list[str] = []
    if not trusted_base:
        errors.append("could not establish main merge-base as the trusted release baseline")
    if not protected_fields_clean:
        errors.append("VERSION or docs/manifest.yaml changed relative to the trusted release baseline")
    if tagged:
        errors.append("current Harness commit is already tagged and cannot be treated as pre-release work")
    return errors


def _git_release_guard() -> list[str]:
    main_ref = subprocess.run(["git", "rev-parse", "--verify", "main"], cwd=ROOT, text=True, capture_output=True, check=False)
    merge_base = subprocess.run(["git", "merge-base", "main", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=False)
    trusted_base = main_ref.returncode == 0 and merge_base.returncode == 0 and bool(merge_base.stdout.strip())
    protected_fields_clean = False
    if trusted_base:
        protected = subprocess.run(
            ["git", "diff", "--quiet", merge_base.stdout.strip(), "--", "VERSION", "docs/manifest.yaml"],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        protected_fields_clean = protected.returncode == 0
    tags = subprocess.run(["git", "tag", "--points-at", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=False)
    return _release_guard_errors(trusted_base, protected_fields_clean, tags.returncode == 0 and bool(tags.stdout.strip()))


def _source_blocks(value: dict[str, Any]) -> list[dict[str, Any]] | None:
    blocks = value.get("source_blocks")
    if not isinstance(blocks, list) or not blocks:
        return None
    if not all(isinstance(item, dict) and isinstance(item.get("ref"), str) and isinstance(item.get("content_sha256"), str) for item in blocks):
        return None
    return blocks


def _source_inventory_matches_current(ledger: dict[str, Any]) -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="harness-gate-") as temporary:
        temporary_root = Path(temporary)
        candidates = temporary_root / "candidates.json"
        inventory = temporary_root / "inventory.json"
        resolve = subprocess.run(
            [sys.executable, "-m", "tools.harness_compiler", "resolve", "--spec-root", ".", "--target-root", ".", "--adoption-baseline", "harness/adoption-baseline.json", "--output", str(candidates)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        if resolve.returncode != 0:
            return False, "could not resolve the current source route"
        scan = subprocess.run(
            [sys.executable, "-m", "tools.harness_compiler", "scan", "--spec-root", ".", "--candidates", str(candidates), "--output", str(inventory)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        if scan.returncode != 0:
            return False, "could not scan the current source route"
        current, error = _load_json(inventory)
        if error or current is None:
            return False, "could not read freshly scanned source inventory"
    return _source_blocks(ledger) == _source_blocks(current), "source inventory digest ledger differs from current Canonical sources"


def _check_values(baseline: dict[str, Any], route: dict[str, Any], instruction: str, receipt: dict[str, Any], ledger: dict[str, Any], branch: str | None) -> list[str]:
    errors: list[str] = []
    if baseline.get("target", {}).get("id") != "spec-coding" or baseline.get("publication", {}).get("component_root") != ".":
        errors.append("Adoption Baseline does not bind this repository-root Harness")
    if route.get("stages") != ["04", "05", "06"]:
        errors.append("Final Workflow Route is not the intended implementation-to-verification path")
    absent = [phrase for phrase in REQUIRED_INSTRUCTION if phrase not in instruction]
    if absent:
        errors.append(f"Harness instruction lacks required guarantees: {absent}")
    if receipt.get("independent") is not True or receipt.get("verdict") != "pass" or receipt.get("findings"):
        errors.append("independent semantic review receipt does not pass")
    if _source_blocks(ledger) is None:
        errors.append("source inventory ledger is malformed")
    if branch in {None, "main"}:
        errors.append("Harness integration must run from a named feature branch, never main")
    return errors


def _negative_probe() -> int:
    baseline = {"target": {"id": "wrong"}, "publication": {"component_root": "."}}
    route = {"stages": ["04", "05"]}
    receipt = {"independent": False, "verdict": "fail", "findings": ["missing"]}
    ledger = {"source_blocks": []}
    caught = _check_values(baseline, route, "", receipt, ledger, "main")
    caught.extend(_release_guard_errors(False, False, True))
    if len(caught) < 9:
        print("negative probe did not reject every invalid Harness condition", file=sys.stderr)
        return 0
    print("intentional invalid Harness conditions rejected", file=sys.stderr)
    return 1


def main() -> int:
    if sys.argv[1:] == ["--probe"]:
        return _negative_probe()
    if sys.argv[1:]:
        print("usage: verify-harness.py [--probe]", file=sys.stderr)
        return 2
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        print(f"missing required Harness files: {', '.join(missing)}", file=sys.stderr)
        return 1
    baseline, baseline_error = _load_json(ROOT / "harness/adoption-baseline.json")
    route, route_error = _load_json(ROOT / "harness/final-workflow-route.json")
    receipt, receipt_error = _load_json(ROOT / "harness/review-receipt.json")
    ledger, ledger_error = _load_json(ROOT / "harness/source-inventory.json")
    errors = [error for error in (baseline_error, route_error, receipt_error, ledger_error) if error]
    if errors:
        print("; ".join(errors), file=sys.stderr)
        return 1
    assert baseline is not None and route is not None and receipt is not None and ledger is not None
    errors.extend(_check_values(baseline, route, (ROOT / "AGENTS.md").read_text(encoding="utf-8"), receipt, ledger, _branch()))
    if not _manifest_version_matches():
        errors.append("VERSION and docs/manifest.yaml spec_coding_version differ")
    errors.extend(_git_release_guard())
    source_matches, source_message = _source_inventory_matches_current(ledger)
    if not source_matches:
        errors.append(source_message)
    tests = subprocess.run([sys.executable, "-m", "unittest", "discover", "-v"], cwd=ROOT, text=True, capture_output=True, check=False)
    if tests.returncode != 0:
        errors.append("repository unit test suite failed")
    if errors:
        print("; ".join(errors), file=sys.stderr)
        if tests.returncode != 0:
            print(tests.stdout[-2000:], file=sys.stderr)
            print(tests.stderr[-2000:], file=sys.stderr)
        return 1
    print("Harness deterministic repository gate passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
