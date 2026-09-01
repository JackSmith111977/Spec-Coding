from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.harness_compiler.scan import scan_markdown


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
SPEC_FIXTURE = FIXTURES / "spec"


class HarnessCompilerV2Tests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "tools.harness_compiler", *args],
            cwd=REPOSITORY_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def prepare_context(self, temporary: Path) -> tuple[Path, Path, Path, Path, Path]:
        spec_root = temporary / "spec"
        target_root = temporary / "target"
        shutil.copytree(SPEC_FIXTURE, spec_root)
        target_root.mkdir()
        candidates = temporary / "candidates.json"
        inventory = temporary / "inventory.json"
        resolved = self.run_cli(
            "resolve", "--spec-root", str(spec_root), "--target-root", str(target_root),
            "--adoption-baseline", "adoption.json", "--output", str(candidates),
        )
        self.assertEqual(resolved.returncode, 0, resolved.stderr or resolved.stdout)
        scanned = self.run_cli("scan", "--spec-root", str(spec_root), "--candidates", str(candidates), "--output", str(inventory))
        self.assertEqual(scanned.returncode, 0, scanned.stderr or scanned.stdout)
        return spec_root, target_root, candidates, inventory, spec_root / "adoption.json"

    @staticmethod
    def digest(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def state_for(self, target_root: Path, inventory_path: Path, baseline_path: Path) -> Path:
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        baseline_sha = self.digest(json.dumps(baseline, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        instruction = "# Harness\n\nUse the compiled instruction before executing work.\n"
        gate = "from __future__ import annotations\n\nimport sys\n\nif __name__ == '__main__':\n    raise SystemExit(0 if sys.argv[1:] == ['--valid'] else 1)\n"
        stage_instruction = target_root / ".harness-staging" / "instruction.md"
        stage_gate = target_root / ".harness-staging" / "gate.py"
        stage_instruction.parent.mkdir(parents=True)
        stage_instruction.write_text(instruction, encoding="utf-8")
        stage_gate.write_text(gate, encoding="utf-8")

        sources = []
        for index, block in enumerate(inventory["source_blocks"], start=1):
            source = {
                "id": f"SRC-{index:03d}", "kind": block["kind"], "ref": block["ref"],
                "sha256": block["content_sha256"], "status": "RESOLVED", "guidance_only": True,
            }
            sources.append(source)
        preamble = next(source for source in sources if source["ref"].endswith("#preamble@1"))
        adoption = next(source for source in sources if source["ref"] == "adoption://constraint/merge-policy")
        preamble.pop("guidance_only")
        adoption.pop("guidance_only")
        preamble["contracts"] = ["CT-001"]
        adoption["contracts"] = ["CT-002"]
        checks = {
            name: {"status": "pass", "evidence": [f"test://{name}"]}
            for name in (
                "source_coverage", "contract_coverage", "semantic_fidelity", "runtime_mapping",
                "capability_routing", "component_integrity", "minimality", "runtime_loading",
                "executability", "failure_path", "reference_drift",
            )
        }
        checks["semantic_fidelity"]["reviewer"] = {"independent": True, "verdict": "pass", "findings": []}
        state = {
            "compilation": {"spec_version": "0.10.0", "target_id": "fixture-target", "adoption_sha256": baseline_sha},
            "sources": sources,
            "contracts": [
                {"id": "CT-001", "source": [preamble["id"]], "guarantee": "instruction is available", "strength": "must"},
                {"id": "CT-002", "source": [adoption["id"]], "guarantee": "verified-only gate rejects invalid input", "strength": "must"},
            ],
            "mappings": [
                {"contract": "CT-001", "decision": "COMPILE", "primitives": ["instruction"], "runtime": {"support": "native", "surfaces": ["harness/AGENTS.md"], "evidence": ["local://instruction-discovery"]}},
                {"contract": "CT-002", "decision": "COMPILE", "primitives": ["script"], "runtime": {"support": "external", "surfaces": ["harness/gate.py"], "evidence": ["local://python3"]}},
            ],
            "components": [
                {"id": "CMP-001", "type": "instruction", "covers": ["CT-001"], "reason": "preserve instruction contract", "outputs": [{"target": "harness/AGENTS.md", "action": "create", "staged": ".harness-staging/instruction.md", "content_sha256": self.digest(instruction)}]},
                {"id": "CMP-002", "type": "script", "covers": ["CT-002"], "reason": "enforce verified-only gate", "outputs": [{"target": "harness/gate.py", "action": "create", "staged": ".harness-staging/gate.py", "content_sha256": self.digest(gate)}], "verification": {"deterministic": True, "load_command": ["python3", "-m", "py_compile", "harness/gate.py"], "command": ["python3", "harness/gate.py", "--valid"], "failure_command": ["python3", "harness/gate.py", "--invalid"]}},
            ],
            "validation": {**checks, "unresolved": 0, "blocked": 0, "harness_ready": True},
        }
        state_path = target_root / "state.json"
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        return state_path

    def test_target_level_e2e_creates_then_verifies_harness(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec_root, target_root, _, inventory, baseline = self.prepare_context(Path(temporary))
            state = self.state_for(target_root, inventory, baseline)
            validated = self.run_cli("validate", "--spec-root", str(spec_root), "--target-root", str(target_root), "--adoption-baseline", "adoption.json", "--state", str(state), "--source-inventory", str(inventory), "--output", str(target_root / "validate.json"))
            self.assertEqual(validated.returncode, 0, validated.stderr or validated.stdout)
            self.assertFalse((target_root / "harness" / "AGENTS.md").exists())
            composed = self.run_cli("compose", "--spec-root", str(spec_root), "--target-root", str(target_root), "--adoption-baseline", "adoption.json", "--state", str(state), "--source-inventory", str(inventory), "--output", str(target_root / "compose.json"))
            self.assertEqual(composed.returncode, 0, composed.stderr or composed.stdout)
            self.assertTrue((target_root / "harness" / "AGENTS.md").is_file())
            verified = self.run_cli("verify", "--spec-root", str(spec_root), "--target-root", str(target_root), "--adoption-baseline", "adoption.json", "--state", str(state), "--source-inventory", str(inventory), "--output", str(target_root / "verify.json"))
            self.assertEqual(verified.returncode, 0, verified.stderr or verified.stdout)
            self.assertEqual(json.loads(verified.stdout)["executed_components"], 1)

    def test_missing_adoption_baseline_blocks_resolve(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec_root = Path(temporary) / "spec"
            target_root = Path(temporary) / "target"
            shutil.copytree(SPEC_FIXTURE, spec_root)
            target_root.mkdir()
            (spec_root / "adoption.json").unlink()
            result = self.run_cli("resolve", "--spec-root", str(spec_root), "--target-root", str(target_root), "--adoption-baseline", "adoption.json", "--output", str(Path(temporary) / "out.json"))
            self.assertNotEqual(result.returncode, 0)

    def test_scan_distinguishes_repeated_heading_occurrences_and_adoption_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _, _, _, inventory, _ = self.prepare_context(Path(temporary))
            refs = [item["ref"] for item in json.loads(inventory.read_text(encoding="utf-8"))["source_blocks"]]
            self.assertIn("docs/workflow.md#heading:sample-workflow/requirement@1", refs)
            self.assertIn("docs/workflow.md#heading:sample-workflow/requirement@2", refs)
            self.assertIn("adoption://publication-boundary", refs)

    def test_unknown_runtime_and_non_independent_review_block_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec_root, target_root, _, inventory, baseline = self.prepare_context(Path(temporary))
            state_path = self.state_for(target_root, inventory, baseline)
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["mappings"][0]["runtime"]["support"] = "unknown"
            state["validation"]["semantic_fidelity"]["reviewer"]["independent"] = False
            state_path.write_text(json.dumps(state), encoding="utf-8")
            result = self.run_cli("validate", "--spec-root", str(spec_root), "--target-root", str(target_root), "--adoption-baseline", "adoption.json", "--state", str(state_path), "--source-inventory", str(inventory), "--output", str(target_root / "invalid.json"))
            self.assertNotEqual(result.returncode, 0)
            codes = {item["code"] for item in json.loads(result.stdout)["diagnostics"]}
            self.assertIn("BLOCKING_RUNTIME_UNKNOWN", codes)
            self.assertIn("MISSING_INDEPENDENT_REVIEW", codes)

    def test_compose_rejects_staged_artifact_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec_root, target_root, _, inventory, baseline = self.prepare_context(Path(temporary))
            state = self.state_for(target_root, inventory, baseline)
            (target_root / ".harness-staging" / "instruction.md").write_text("tampered", encoding="utf-8")
            result = self.run_cli("compose", "--spec-root", str(spec_root), "--target-root", str(target_root), "--adoption-baseline", "adoption.json", "--state", str(state), "--source-inventory", str(inventory), "--output", str(target_root / "compose-invalid.json"))
            self.assertNotEqual(result.returncode, 0)
            codes = {item["code"] for item in json.loads(result.stdout)["diagnostics"]}
            self.assertIn("STAGED_ARTIFACT_DRIFT", codes)
            self.assertFalse((target_root / "harness").exists())

    def test_schema_and_semantic_accounting_failure_paths(self) -> None:
        cases = {
            "schema": (
                lambda state: state["sources"][0].update({"unexpected": True}),
                "STATE_SCHEMA_INVALID",
            ),
            "unaccounted": (
                lambda state: state["sources"].pop(),
                "SOURCE_NOT_ACCOUNTED",
            ),
            "duplicate-ref": (
                lambda state: state["sources"].append(
                    {
                        **state["sources"][0],
                        "id": "SRC-DUPLICATE",
                        "contracts": [],
                        "guidance_only": True,
                    }
                ),
                "DUPLICATE_SOURCE_REF",
            ),
            "unresolved": (
                lambda state: state["sources"][0].update({"status": "UNRESOLVED"}),
                "UNRESOLVED_SOURCE",
            ),
            "missing-mapping": (
                lambda state: state.update({"mappings": []}),
                "MISSING_MAPPING",
            ),
            "compile-without-component": (
                lambda state: state.update({"components": []}),
                "COMPILE_WITHOUT_COMPONENT",
            ),
            "orphan-component": (
                lambda state: state["mappings"].__setitem__(
                    0,
                    {
                        "contract": "CT-001",
                        "decision": "EXISTING",
                        "existing": {
                            "coverage": "sufficient",
                            "mechanisms": ["existing://instruction"],
                            "evidence": ["test://existing-instruction"],
                        },
                    },
                ),
                "ORPHAN_COMPONENT",
            ),
            "blocked": (
                lambda state: (
                    state["mappings"].__setitem__(0, {"contract": "CT-001", "decision": "BLOCKED", "reason": "runtime evidence unavailable"}),
                    state["validation"].update({"blocked": 1}),
                ),
                "READY_INCONSISTENT",
            ),
            "invalid-ref": (
                lambda state: state["sources"][0].update({"ref": "../../outside.md#preamble@1"}),
                "INVALID_SOURCE_REF",
            ),
        }
        for name, (mutate, expected_code) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                spec_root, target_root, _, inventory, baseline = self.prepare_context(Path(temporary))
                state_path = self.state_for(target_root, inventory, baseline)
                state = json.loads(state_path.read_text(encoding="utf-8"))
                mutate(state)
                state_path.write_text(json.dumps(state), encoding="utf-8")
                result = self.run_cli(
                    "validate", "--spec-root", str(spec_root), "--target-root", str(target_root),
                    "--adoption-baseline", "adoption.json", "--state", str(state_path),
                    "--source-inventory", str(inventory), "--output", str(target_root / f"{name}.json"),
                )
                self.assertNotEqual(result.returncode, 0, result.stderr or result.stdout)
                codes = {item["code"] for item in json.loads(result.stdout)["diagnostics"]}
                self.assertIn(expected_code, codes)

    def test_scanner_preserves_headingless_and_title_preamble_spans(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            headingless = root / "headingless.md"
            headingless.write_text("A standalone normative sentence.\n", encoding="utf-8")
            blocks, diagnostics = scan_markdown(headingless, "headingless.md")
            self.assertFalse(diagnostics)
            self.assertEqual(blocks[0]["ref"], "headingless.md#preamble@1")
            self.assertTrue(blocks[0]["semantic_required"])

            titled = root / "titled.md"
            titled.write_text("# Title is semantic\n\nA preamble requirement.\n## Detail\n\nBody.\n", encoding="utf-8")
            blocks, diagnostics = scan_markdown(titled, "titled.md")
            self.assertFalse(diagnostics)
            self.assertEqual(blocks[0]["line_start"], 1)
            self.assertEqual(blocks[0]["line_end"], 3)
            self.assertEqual(blocks[0]["block_kind"], "preamble")

    def test_generic_probe_runner_accepts_a_custom_component_type(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec_root, target_root, _, inventory, baseline = self.prepare_context(Path(temporary))
            state_path = self.state_for(target_root, inventory, baseline)
            state = json.loads(state_path.read_text(encoding="utf-8"))
            custom = state["components"][1]
            custom["type"] = "custom-runtime-adapter"
            custom["verification"] = {
                "deterministic": True,
                "load_command": ["sh", "-c", "test -f harness/gate.py"],
                "command": ["sh", "-c", "test -s harness/gate.py"],
                "failure_command": ["sh", "-c", "test ! -f harness/gate.py"],
            }
            state_path.write_text(json.dumps(state), encoding="utf-8")
            composed = self.run_cli(
                "compose", "--spec-root", str(spec_root), "--target-root", str(target_root),
                "--adoption-baseline", "adoption.json", "--state", str(state_path),
                "--source-inventory", str(inventory), "--output", str(target_root / "compose.json"),
            )
            self.assertEqual(composed.returncode, 0, composed.stderr or composed.stdout)
            verified = self.run_cli(
                "verify", "--spec-root", str(spec_root), "--target-root", str(target_root),
                "--adoption-baseline", "adoption.json", "--state", str(state_path),
                "--source-inventory", str(inventory), "--output", str(target_root / "verify.json"),
            )
            self.assertEqual(verified.returncode, 0, verified.stderr or verified.stdout)

    def test_current_canonical_corpus_resolves_and_scans_from_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            spec_root = temporary_root / "spec"
            target_root = temporary_root / "target"
            shutil.copytree(REPOSITORY_ROOT, spec_root, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
            target_root.mkdir()
            baseline = {
                "adoption_version": 1,
                "target": {"id": "canonical-scan-target"},
                "spec_workspace": {"id": "canonical-scan-workspace"},
                "publication": {"boundary": "local", "component_root": "harness"},
                "integration": {"scope": "project"},
                "workflow_route": "canonical-scan-route.json",
                "constraints": [{"id": "publication", "value": "local-only"}],
            }
            route = {"stages": ["01b"], "rule_ids": [], "exception_ids": []}
            (spec_root / "adoption.json").write_text(json.dumps(baseline), encoding="utf-8")
            (spec_root / "canonical-scan-route.json").write_text(json.dumps(route), encoding="utf-8")
            candidates = temporary_root / "candidates.json"
            inventory = temporary_root / "inventory.json"
            resolved = self.run_cli(
                "resolve", "--spec-root", str(spec_root), "--target-root", str(target_root),
                "--adoption-baseline", "adoption.json", "--output", str(candidates),
            )
            self.assertEqual(resolved.returncode, 0, resolved.stderr or resolved.stdout)
            scanned = self.run_cli("scan", "--spec-root", str(spec_root), "--candidates", str(candidates), "--output", str(inventory))
            self.assertEqual(scanned.returncode, 0, scanned.stderr or scanned.stdout)
            refs = {block["ref"] for block in json.loads(inventory.read_text(encoding="utf-8"))["source_blocks"]}
            self.assertIn("docs/workflows/main/01b-project-understanding/01-project-orientation.md#preamble@1", refs)
            self.assertIn("adoption://publication-boundary", refs)


if __name__ == "__main__":
    unittest.main()
