from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.harness_adapt.prepare import prepare
from tools.harness_adapt.shared import sha256_json
from tools.harness_adapt.validate import validate_adaptation

ROOT = Path(__file__).resolve().parents[2]
PLAN_SCHEMA = json.loads((ROOT / "tools/harness_adapt/schema/adaptation-plan.schema.json").read_text())
CANDIDATE_SCHEMA = json.loads((ROOT / "tools/harness_adapt/schema/harness-candidate.schema.json").read_text())


class HarnessAdaptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ir = {"clauses": [{"id": "SC-001"}, {"id": "SC-002"}]}
        self.adoption = {"target": "fixture", "publication": "local"}
        self.environment = {
            "schema_version": 1,
            "semantic_fingerprint": "0" * 64,
            "adoption_fingerprint": "1" * 64,
            "identity": {"target": "fixture", "runtime": "pi"},
            "facts": [
                {"id": "F-001", "category": "runtime", "statement": "Pi exposes a reachable official package registry.", "confidence": "confirmed", "evidence": ["local://pi/packages"]},
                {"id": "F-002", "category": "runtime", "statement": "The project loader reads AGENTS.md.", "confidence": "confirmed", "evidence": ["local://loader"]},
            ],
            "capabilities": [],
            "provider_surfaces": [{"id": "PS-001", "kind": "runtime_package", "status": "reachable", "query_mechanism": "pi packages search", "install_mechanism": "pi packages install", "trust_scope": "runtime_official", "fact_refs": ["F-001"]}],
            "project_mechanisms": [],
            "existing_harness": [],
            "constraints": [],
            "unknowns": [],
        }
        seed = prepare(self.ir, self.environment, self.adoption)
        self.plan = {
            "schema_version": 1,
            "semantic_fingerprint": seed["semantic_fingerprint"],
            "environment_fingerprint": seed["environment_fingerprint"],
            "adoption_fingerprint": seed["adoption_fingerprint"],
            "clause_accounts": [
                {"clause": "SC-001", "disposition": "covered", "requirement_ids": ["REQ-001"]},
                {"clause": "SC-002", "disposition": "not_applicable", "reason": "No target adaptation is required."},
            ],
            "requirements": [{
                "id": "REQ-001",
                "name": "independent_review",
                "semantic_guarantee": "Provide an independent review execution path.",
                "required_by": ["SC-001"],
                "primitives": ["Agent / Subagent"],
                "provider_ids": ["P-001"],
                "selected_provider": "P-001",
                "selection_reason": "Official Pi package provides the required isolation with less custom maintenance.",
            }],
            "providers": [{
                "id": "P-001",
                "source": "registry",
                "availability": "installable",
                "mechanism": "official-review-package",
                "trust": "runtime_official",
                "satisfies": ["REQ-001"],
                "evidence": ["official://pi/packages/review"],
                "surface_ref": "PS-001",
                "requires_change": True,
                "authority_status": "allowed",
            }],
        }
        self.candidate = {
            "schema_version": 1,
            "semantic_fingerprint": seed["semantic_fingerprint"],
            "environment_fingerprint": seed["environment_fingerprint"],
            "adoption_fingerprint": seed["adoption_fingerprint"],
            "plan_fingerprint": sha256_json(self.plan),
            "components": [{"id": "CMP-001", "kind": "review-routing", "mode": "create", "covers_clauses": ["SC-001"], "provider_refs": ["P-001"], "artifact_refs": ["ART-001"]}],
            "artifacts": [{"id": "ART-001", "path": "AGENTS.md", "kind": "instruction", "component_ref": "CMP-001", "state": "materialized", "loader_fact_ref": "F-002"}],
            "provider_changes": [{"provider_ref": "P-001", "action": "install", "status": "applied", "refresh_evidence": ["local://pi/packages/installed/review"]}],
        }

    def validate(self, plan=None, candidate=None, create_artifact=True):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            if create_artifact:
                (target / "AGENTS.md").write_text("# Harness\n")
            return validate_adaptation(self.ir, self.environment, self.adoption, plan or self.plan, candidate or self.candidate, PLAN_SCHEMA, CANDIDATE_SCHEMA, target)

    def test_prepare_accounts_for_every_clause(self) -> None:
        seed = prepare(self.ir, self.environment, self.adoption)
        self.assertEqual([item["clause"] for item in seed["clause_work_items"]], ["SC-001", "SC-002"])
        self.assertEqual(seed["provider_surfaces"][0]["id"], "PS-001")

    def test_registry_provider_candidate_passes(self) -> None:
        self.assertTrue(self.validate()["passed"])

    def test_registry_provider_needs_reachable_surface(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["providers"][0]["surface_ref"] = "PS-MISSING"
        result = self.validate(plan=plan)
        self.assertFalse(result["passed"])
        self.assertIn("REGISTRY_SURFACE_REQUIRED", {item["code"] for item in result["diagnostics"]})

    def test_selected_provider_requires_semantic_sufficiency(self) -> None:
        plan = copy.deepcopy(self.plan)
        plan["providers"][0]["satisfies"] = ["REQ-OTHER"]
        result = self.validate(plan=plan)
        self.assertFalse(result["passed"])
        self.assertIn("PROVIDER_SEMANTIC_GAP", {item["code"] for item in result["diagnostics"]})

    def test_provider_change_requires_refresh_evidence(self) -> None:
        candidate = copy.deepcopy(self.candidate)
        candidate["provider_changes"][0]["refresh_evidence"] = []
        result = self.validate(candidate=candidate)
        self.assertFalse(result["passed"])
        self.assertIn("PROVIDER_REFRESH_REQUIRED", {item["code"] for item in result["diagnostics"]})

    def test_every_covered_clause_needs_component(self) -> None:
        candidate = copy.deepcopy(self.candidate)
        candidate["components"] = []
        candidate["artifacts"] = []
        result = self.validate(candidate=candidate)
        self.assertFalse(result["passed"])
        self.assertIn("CANDIDATE_COVERAGE_GAP", {item["code"] for item in result["diagnostics"]})

    def test_materialized_artifact_must_exist(self) -> None:
        result = self.validate(create_artifact=False)
        self.assertFalse(result["passed"])
        self.assertIn("MISSING_MATERIALIZED_ARTIFACT", {item["code"] for item in result["diagnostics"]})


if __name__ == "__main__":
    unittest.main()
