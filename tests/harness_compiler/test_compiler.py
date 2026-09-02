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

from tools.harness_compiler.compose import compose
from tools.harness_compiler.scan import scan_markdown
from tests.harness_compiler.verify_spec_coding_harness import verify_fixture


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
        semantic_sources = [source for source, block in zip(sources, inventory["source_blocks"]) if block.get("semantic_required") is True]
        for source in semantic_sources:
            source.pop("guidance_only")
            source["contracts"] = ["CT-001"]
        adoption = next(source for source in sources if source["ref"] == "adoption://constraint/merge-policy")
        adoption["contracts"].append("CT-002")
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
            "compilation": {"spec_version": "0.11.0", "target_id": "fixture-target", "adoption_sha256": baseline_sha},
            "sources": sources,
            "contracts": [
                {"id": "CT-001", "source": [source["id"] for source in semantic_sources], "guarantee": "instruction is available", "strength": "must", "readback_contract": {"when": "before source-derived work", "canonical_doc": "docs/workflow.md", "mandatory": True}},
                {"id": "CT-002", "source": [adoption["id"]], "guarantee": "verified-only gate rejects invalid input", "strength": "must", "readback_contract": {"when": "before execution", "canonical_doc": "docs/workflow.md", "mandatory": True}, "failure_mode": "invalid input must fail"},
            ],
            "mappings": [
                {"contract": "CT-001", "decision": "COMPILE", "primitives": ["instruction"], "runtime": {"support": "native", "surfaces": ["harness/AGENTS.md"], "evidence": ["local://instruction-discovery"]}},
                {"contract": "CT-002", "decision": "COMPILE", "primitives": ["script"], "runtime": {"support": "external", "surfaces": ["harness/gate.py"], "evidence": ["local://python3"]}},
            ],
            "components": [
                {"id": "CMP-001", "type": "instruction", "covers": ["CT-001"], "reason": "preserve instruction contract", "outputs": [{"target": "AGENTS.md", "action": "create", "staged": ".harness-staging/instruction.md", "content_sha256": self.digest(instruction)}], "verification": {"covers": ["CT-001"], "cannot_cover": ["semantic fidelity requires independent review"], "probes": [{"id": "runtime-visible", "type": "runtime-visibility", "covers": ["CT-001"]}]}},
                {"id": "CMP-002", "type": "script", "covers": ["CT-002"], "reason": "enforce verified-only gate", "outputs": [{"target": ".fixture/extensions/gate.py", "action": "create", "staged": ".harness-staging/gate.py", "content_sha256": self.digest(gate)}], "verification": {"covers": ["CT-002"], "cannot_cover": ["runtime behavior requires a fresh-agent acceptance run"], "probes": [{"id": "runtime-visible", "type": "runtime-visibility", "covers": ["CT-002"]}, {"id": "syntax", "type": "surface", "covers": ["CT-002"], "command": ["python3", "-m", "py_compile", ".fixture/extensions/gate.py"], "expect": "pass"}, {"id": "accept-invalid", "type": "surface", "covers": ["CT-002"], "command": ["python3", ".fixture/extensions/gate.py", "--invalid"], "expect": "fail"}]}},
            ],
            "validation": {**checks, "unresolved": 0, "blocked": 0},
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
            self.assertFalse((target_root / "AGENTS.md").exists())
            composed = self.run_cli("compose", "--spec-root", str(spec_root), "--target-root", str(target_root), "--adoption-baseline", "adoption.json", "--state", str(state), "--source-inventory", str(inventory), "--output", str(target_root / "compose.json"))
            self.assertEqual(composed.returncode, 0, composed.stderr or composed.stdout)
            self.assertTrue((target_root / "AGENTS.md").is_file())
            verified = self.run_cli("verify", "--spec-root", str(spec_root), "--target-root", str(target_root), "--adoption-baseline", "adoption.json", "--state", str(state), "--source-inventory", str(inventory), "--output", str(target_root / "verify.json"))
            self.assertEqual(verified.returncode, 0, verified.stderr or verified.stdout)
            verification = json.loads(verified.stdout)
            self.assertEqual(verification["executed_components"], 2)
            self.assertEqual(verification["probe_classes"], {"surface": 2, "semantic": 0, "runtime-visibility": 2})
            self.assertEqual(len(verification["declared_limitations"]), 2)

    def test_runtime_visibility_readback_and_probe_declarations_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec_root, target_root, _, inventory, baseline = self.prepare_context(Path(temporary))
            state_path = self.state_for(target_root, inventory, baseline)
            state = json.loads(state_path.read_text(encoding="utf-8"))

            invisible = copy.deepcopy(state)
            invisible["components"][0]["outputs"][0]["target"] = "harness/AGENTS.md"
            state_path.write_text(json.dumps(invisible), encoding="utf-8")
            result = self.run_cli("validate", "--spec-root", str(spec_root), "--target-root", str(target_root), "--adoption-baseline", "adoption.json", "--state", str(state_path), "--source-inventory", str(inventory), "--output", str(target_root / "invisible.json"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("RUNTIME_VISIBILITY_VIOLATION", {item["code"] for item in json.loads(result.stdout)["diagnostics"]})
            compose_report = compose(target_root, json.loads(baseline.read_text(encoding="utf-8")), invisible)
            self.assertFalse(compose_report["passed"])
            self.assertIn("RUNTIME_VISIBILITY_VIOLATION", {item["code"] for item in compose_report["diagnostics"]})

            missing_readback = copy.deepcopy(state)
            missing_readback["contracts"][0].pop("readback_contract")
            state_path.write_text(json.dumps(missing_readback), encoding="utf-8")
            result = self.run_cli("validate", "--spec-root", str(spec_root), "--target-root", str(target_root), "--adoption-baseline", "adoption.json", "--state", str(state_path), "--source-inventory", str(inventory), "--output", str(target_root / "readback.json"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("MISSING_READBACK_CONTRACT", {item["code"] for item in json.loads(result.stdout)["diagnostics"]})

            noncanonical_readback = copy.deepcopy(state)
            noncanonical_readback["contracts"][0]["readback_contract"]["canonical_doc"] = "VERSION"
            state_path.write_text(json.dumps(noncanonical_readback), encoding="utf-8")
            result = self.run_cli("validate", "--spec-root", str(spec_root), "--target-root", str(target_root), "--adoption-baseline", "adoption.json", "--state", str(state_path), "--source-inventory", str(inventory), "--output", str(target_root / "noncanonical-readback.json"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("READBACK_DOCUMENT_NOT_CANONICAL", {item["code"] for item in json.loads(result.stdout)["diagnostics"]})

            partial_probe_coverage = copy.deepcopy(state)
            partial_probe_coverage["components"][0]["covers"] = ["CT-001", "CT-002"]
            partial_probe_coverage["components"][0]["verification"]["covers"] = ["CT-001", "CT-002"]
            state_path.write_text(json.dumps(partial_probe_coverage), encoding="utf-8")
            result = self.run_cli("validate", "--spec-root", str(spec_root), "--target-root", str(target_root), "--adoption-baseline", "adoption.json", "--state", str(state_path), "--source-inventory", str(inventory), "--output", str(target_root / "partial-probe-coverage.json"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PROBE_COVERAGE_GAP", {item["code"] for item in json.loads(result.stdout)["diagnostics"]})

            missing_runtime_probe = copy.deepcopy(state)
            missing_runtime_probe["components"][0]["verification"]["probes"] = [
                {"id": "surface-only", "type": "surface", "covers": ["CT-001"], "command": ["python3", "-c", "pass"], "expect": "pass"}
            ]
            state_path.write_text(json.dumps(missing_runtime_probe), encoding="utf-8")
            result = self.run_cli("validate", "--spec-root", str(spec_root), "--target-root", str(target_root), "--adoption-baseline", "adoption.json", "--state", str(state_path), "--source-inventory", str(inventory), "--output", str(target_root / "missing-runtime-probe.json"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("MISSING_RUNTIME_VISIBILITY_PROBE", {item["code"] for item in json.loads(result.stdout)["diagnostics"]})

    def test_missing_adoption_baseline_blocks_resolve(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec_root = Path(temporary) / "spec"
            target_root = Path(temporary) / "target"
            shutil.copytree(SPEC_FIXTURE, spec_root)
            target_root.mkdir()
            (spec_root / "adoption.json").unlink()
            result = self.run_cli("resolve", "--spec-root", str(spec_root), "--target-root", str(target_root), "--adoption-baseline", "adoption.json", "--output", str(Path(temporary) / "out.json"))
            self.assertNotEqual(result.returncode, 0)

    def test_runtime_loader_profile_is_required_and_invalid_shapes_return_diagnostics(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec_root = Path(temporary) / "spec"
            target_root = Path(temporary) / "target"
            shutil.copytree(SPEC_FIXTURE, spec_root)
            target_root.mkdir()
            baseline_path = spec_root / "adoption.json"
            baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
            baseline["runtime"] = []
            baseline_path.write_text(json.dumps(baseline), encoding="utf-8")
            result = self.run_cli(
                "resolve", "--spec-root", str(spec_root), "--target-root", str(target_root),
                "--adoption-baseline", "adoption.json", "--output", str(Path(temporary) / "out.json"),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("MISSING_ADOPTION_FACT", {item["code"] for item in json.loads(result.stdout)["diagnostics"]})

    def test_seed_accounts_for_every_scanned_source_but_is_not_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec_root, target_root, _, inventory, _ = self.prepare_context(Path(temporary))
            state = target_root / "seed.json"
            seeded = self.run_cli(
                "seed", "--spec-root", str(spec_root), "--target-root", str(target_root),
                "--adoption-baseline", "adoption.json", "--source-inventory", str(inventory), "--output", str(state),
            )
            self.assertEqual(seeded.returncode, 0, seeded.stderr or seeded.stdout)
            source_count = len(json.loads(inventory.read_text(encoding="utf-8"))["source_blocks"])
            seeded_state = json.loads(state.read_text(encoding="utf-8"))
            self.assertEqual(len(seeded_state["sources"]), source_count)
            self.assertNotIn("harness_ready", seeded_state["validation"])
            result = self.run_cli(
                "validate", "--spec-root", str(spec_root), "--target-root", str(target_root),
                "--adoption-baseline", "adoption.json", "--state", str(state), "--source-inventory", str(inventory),
                "--output", str(target_root / "seed-validate.json"),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("VALIDATION_DIMENSION_FAILED", {item["code"] for item in json.loads(result.stdout)["diagnostics"]})

    def test_derive_seals_unique_semantic_source_contracts_and_output_digests(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            spec_root, target_root, _, inventory, _ = self.prepare_context(Path(temporary))
            seed_path = target_root / "seed.json"
            seeded = self.run_cli(
                "seed", "--spec-root", str(spec_root), "--target-root", str(target_root),
                "--adoption-baseline", "adoption.json", "--source-inventory", str(inventory), "--output", str(seed_path),
            )
            self.assertEqual(seeded.returncode, 0, seeded.stderr or seeded.stdout)
            seed = json.loads(seed_path.read_text(encoding="utf-8"))
            stage = target_root / ".harness-staging" / "instruction.md"
            stage.parent.mkdir()
            stage.write_text("# Compiled Harness\n", encoding="utf-8")
            semantic_ids = [source["id"] for source in seed["sources"] if source.get("guidance_only") is not True]
            checks = {
                name: {"status": "pass", "evidence": [f"test://{name}"]}
                for name in (
                    "source_coverage", "contract_coverage", "semantic_fidelity", "runtime_mapping",
                    "capability_routing", "component_integrity", "minimality", "runtime_loading",
                    "executability", "failure_path", "reference_drift",
                )
            }
            checks["semantic_fidelity"]["reviewer"] = {"independent": True, "verdict": "pass", "findings": []}
            derivation = {
                "contracts": [{"id": "CT-001", "source_selectors": semantic_ids, "guarantee": "compiled instruction is source-linked", "strength": "must", "readback_contract": {"when": "before source-derived work", "canonical_doc": "docs/workflow.md", "mandatory": True}}],
                "mappings": [{"contract": "CT-001", "decision": "COMPILE", "primitives": ["instruction"], "runtime": {"support": "native", "surfaces": ["AGENTS.md"], "evidence": ["test://entry"]}}],
                "components": [{"id": "CMP-001", "type": "instruction", "covers": ["CT-001"], "reason": "source-linked instruction", "outputs": [{"target": "AGENTS.md", "action": "create", "staged": ".harness-staging/instruction.md"}], "verification": {"covers": ["CT-001"], "cannot_cover": ["semantic fidelity requires independent review"], "probes": [{"id": "runtime-visible", "type": "runtime-visibility", "covers": ["CT-001"]}]}}],
                "validation": {**checks, "unresolved": 0, "blocked": 0},
            }
            derivation_path = target_root / "derivation.json"
            derivation_path.write_text(json.dumps(derivation), encoding="utf-8")
            state_path = target_root / "derived.json"
            result = self.run_cli(
                "derive", "--spec-root", str(spec_root), "--target-root", str(target_root),
                "--adoption-baseline", "adoption.json", "--seed-state", str(seed_path),
                "--derivation", str(derivation_path), "--output", str(state_path),
            )
            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual({source["contracts"][0] for source in state["sources"] if source.get("guidance_only") is not True}, {"CT-001"})
            self.assertEqual(state["components"][0]["outputs"][0]["content_sha256"], self.digest("# Compiled Harness\n"))

            missing_readback = copy.deepcopy(derivation)
            missing_readback["contracts"][0].pop("readback_contract")
            missing_readback_path = target_root / "missing-readback-derivation.json"
            missing_readback_path.write_text(json.dumps(missing_readback), encoding="utf-8")
            blocked = self.run_cli(
                "derive", "--spec-root", str(spec_root), "--target-root", str(target_root),
                "--adoption-baseline", "adoption.json", "--seed-state", str(seed_path),
                "--derivation", str(missing_readback_path), "--output", str(target_root / "missing-readback-state.json"),
            )
            self.assertNotEqual(blocked.returncode, 0)
            self.assertIn("MISSING_READBACK_CONTRACT", {item["code"] for item in json.loads(blocked.stdout)["diagnostics"]})

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
            "self-ready": (
                lambda state: state["validation"].update({"harness_ready": True}),
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
                "BLOCKED_MAPPING_PRESENT",
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
                "covers": ["CT-002"],
                "cannot_cover": ["semantic fidelity requires independent review"],
                "probes": [
                    {"id": "runtime-visible", "type": "runtime-visibility", "covers": ["CT-002"]},
                    {"id": "exists", "type": "surface", "covers": ["CT-002"], "command": ["sh", "-c", "test -f .fixture/extensions/gate.py"], "expect": "pass"},
                    {"id": "non-empty", "type": "surface", "covers": ["CT-002"], "command": ["sh", "-c", "test -s .fixture/extensions/gate.py"], "expect": "pass"},
                    {"id": "negative-control", "type": "surface", "covers": ["CT-002"], "command": ["sh", "-c", "test ! -f .fixture/extensions/gate.py"], "expect": "fail"},
                ],
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
                "publication": {"boundary": "local", "component_root": "."},
                "integration": {"scope": "project"},
                "runtime": {
                    "id": "fixture-runtime",
                    "evidence": ["test://runtime-loader-rules"],
                    "loader_rules": {"context_files": ["AGENTS.md"], "skill_dirs": [], "extension_dirs": []},
                },
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

    def test_self_hosted_harness_fixture_is_current_and_rejects_invalid_conditions(self) -> None:
        self.assertEqual(verify_fixture(), [])
        probe = subprocess.run(
            [sys.executable, "tests/harness_compiler/verify_spec_coding_harness.py", "--probe"],
            cwd=REPOSITORY_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(probe.returncode, 0)
        self.assertIn("intentional invalid Harness fixture conditions rejected", probe.stderr)


if __name__ == "__main__":
    unittest.main()
