from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.semantic_compiler.resolve import resolve_sources
from tools.semantic_compiler.shared import sha256_json
from tools.semantic_compiler.validate import validate_ir


class SemanticCompilerTests(unittest.TestCase):
    def make_spec(self, root: Path) -> None:
        (root / "docs/workflows/main/demo").mkdir(parents=True)
        (root / "docs/rules").mkdir(parents=True)
        (root / "docs/meta-protocols").mkdir(parents=True)
        (root / "VERSION").write_text("9.9.9\n", encoding="utf-8")
        (root / "docs/workflows/main/demo/01-step.md").write_text("# Step\n\n## Gate\n\nLocal verification MUST pass before commit.\n", encoding="utf-8")
        (root / "docs/rules/global.md").write_text("# Global\n\n## Authority\n\nRequirement meaning is a human decision.\n", encoding="utf-8")
        (root / "docs/meta-protocols/onboarding.md").write_text("# Onboarding\n\nDiscover facts before asking the human.\n", encoding="utf-8")
        (root / "docs/manifest.yaml").write_text("""
canonical_root: docs
stages:
  - id: "05"
    name: demo
    documents:
      - workflows/main/demo/01-step.md
rule_documents:
  - id: global
    path: rules/global.md
    applies_to: all
exception_workflows: []
meta_protocols:
  - id: onboarding
    path: meta-protocols/onboarding.md
""".lstrip(), encoding="utf-8")

    def valid_ir(self, manifest: dict) -> dict:
        docs = [item["path"] for item in manifest["documents"]]
        return {
            "ir_version": 1,
            "spec_version": manifest["spec_version"],
            "source_fingerprint": sha256_json([
                {"path": item["path"], "kind": item["kind"], "git_blob_sha1": item["git_blob_sha1"]}
                for item in sorted(manifest["documents"], key=lambda item: item["path"])
            ]),
            "scope": {"mode": "pilot", "documents": docs},
            "clauses": [
                {"id": "SC-001", "kind": "gate", "source": [{"document": "docs/workflows/main/demo/01-step.md", "anchor": "## Gate"}], "must": ["Local verification passes before commit."], "relations": [{"type": "before", "target": "SC-002"}]},
                {"id": "SC-002", "kind": "authority", "source": [{"document": "docs/rules/global.md", "anchor": "## Authority"}], "must": ["Human owns requirement meaning."]}
            ]
        }

    def test_resolve_is_target_independent_and_hashes_whole_documents(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_spec(root)
            result = resolve_sources(root)
            self.assertTrue(result["passed"], result)
            manifest = result["source_manifest"]
            self.assertEqual(manifest["spec_version"], "9.9.9")
            self.assertEqual(manifest["document_count"], 3)
            self.assertEqual({item["kind"] for item in manifest["documents"]}, {"workflow", "rule", "meta-protocol"})
            self.assertTrue(all(len(item["sha256"]) == 64 for item in manifest["documents"]))

    def test_one_source_can_support_multiple_atomic_clauses(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_spec(root)
            manifest = resolve_sources(root)["source_manifest"]
            ir = self.valid_ir(manifest)
            ir["clauses"].append({"id": "SC-003", "kind": "invariant", "source": [{"document": "docs/workflows/main/demo/01-step.md", "anchor": "## Gate"}], "must_not": ["Treat commit as verification."]})
            self.assertTrue(validate_ir(manifest, ir)["passed"])

    def test_dangling_relation_and_hard_order_cycle_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_spec(root)
            manifest = resolve_sources(root)["source_manifest"]
            dangling = self.valid_ir(manifest)
            dangling["clauses"][0]["relations"][0]["target"] = "SC-999"
            result = validate_ir(manifest, dangling)
            self.assertIn("DANGLING_RELATION", {item["code"] for item in result["diagnostics"]})
            cyclic = self.valid_ir(manifest)
            cyclic["clauses"][1]["relations"] = [{"type": "before", "target": "SC-001"}]
            result = validate_ir(manifest, cyclic)
            self.assertIn("HARD_ORDER_CYCLE", {item["code"] for item in result["diagnostics"]})

    def test_source_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_spec(root)
            manifest = resolve_sources(root)["source_manifest"]
            ir = self.valid_ir(manifest)
            ir["source_fingerprint"] = "0" * 64
            result = validate_ir(manifest, ir)
            self.assertIn("SOURCE_DRIFT", {item["code"] for item in result["diagnostics"]})

    def test_release_requires_full_scope_and_external_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_spec(root)
            manifest = resolve_sources(root)["source_manifest"]
            ir = self.valid_ir(manifest)
            ir["scope"] = {"mode": "release", "documents": ["docs/workflows/main/demo/01-step.md", "docs/rules/global.md"]}
            result = validate_ir(manifest, ir)
            codes = {item["code"] for item in result["diagnostics"]}
            self.assertIn("INCOMPLETE_RELEASE_SCOPE", codes)
            self.assertIn("RELEASE_REVIEW_REQUIRED", codes)

    def test_release_passes_with_full_scope_and_external_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_spec(root)
            manifest = resolve_sources(root)["source_manifest"]
            ir = self.valid_ir(manifest)
            documents = [item["path"] for item in manifest["documents"]]
            ir["scope"] = {"mode": "release", "documents": documents}
            receipt = {
                "receipt_version": 1,
                "source_fingerprint": ir["source_fingerprint"],
                "reviewer": {"id": "fresh-reviewer", "independent": True},
                "documents": [{"document": document, "verdict": "pass", "findings": []} for document in documents],
                "global_verdict": "pass",
                "mutations": {"status": "passed", "cases": ["must-to-should", "delete-gate"]}
            }
            self.assertTrue(validate_ir(manifest, ir, receipt)["passed"])

    def test_repository_pilot_ir_stays_bound_to_current_sources(self) -> None:
        repository_root = Path(__file__).resolve().parents[2]
        resolved = resolve_sources(repository_root)
        self.assertTrue(resolved["passed"], resolved)
        pilot = json.loads((repository_root / "semantic/pilot/clauses.json").read_text(encoding="utf-8"))
        result = validate_ir(resolved["source_manifest"], pilot)
        self.assertTrue(result["passed"], result)
        self.assertEqual(result["summary"]["clauses"], 17)
        self.assertEqual(result["summary"]["scope_documents"], 7)


if __name__ == "__main__":
    unittest.main()
