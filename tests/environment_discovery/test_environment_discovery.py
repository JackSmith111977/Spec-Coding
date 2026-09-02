from __future__ import annotations

import copy
import unittest

from tools.environment_discovery.prepare import CORE_QUESTIONS, prepare
from tools.environment_discovery.validate import validate_environment


DISCOVERY_SCHEMA = {"type": "object", "required": ["schema_version", "semantic_fingerprint", "adoption_fingerprint", "clause_accounts", "questions"]}
ENVIRONMENT_SCHEMA = {"type": "object", "required": ["schema_version", "semantic_fingerprint", "adoption_fingerprint", "identity", "facts", "capabilities", "provider_surfaces", "project_mechanisms", "existing_harness", "constraints", "unknowns"]}


class EnvironmentDiscoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ir = {"clauses": [{"id": "SC-001"}, {"id": "SC-002"}]}
        self.adoption = {"target": "fixture", "publication": "local"}
        seed = prepare(self.ir, self.adoption)
        facts = []
        questions = []
        core_fact_by_question = {}
        for index, (question_id, category, question, evidence_required) in enumerate(CORE_QUESTIONS, start=1):
            fact_id = f"F-CORE-{index:02d}"
            core_fact_by_question[question_id] = fact_id
            facts.append({"id": fact_id, "category": category, "statement": f"Confirmed answer for {question_id}.", "confidence": "confirmed", "evidence": [f"local://{question_id.lower()}"]})
            questions.append({"id": question_id, "category": category, "question": question, "required_by": [], "evidence_required": evidence_required, "status": "confirmed", "blocking": True, "fact_refs": [fact_id]})
        questions.append({"id": "Q-001", "category": "runtime", "question": "Can the runtime isolate an independent review context?", "required_by": ["SC-001"], "evidence_required": ["local runtime evidence"], "status": "confirmed", "blocking": True, "fact_refs": ["F-001"]})
        facts.append({"id": "F-001", "category": "runtime", "statement": "Runtime exposes isolated child execution.", "confidence": "confirmed", "evidence": ["local://runtime/help"]})
        self.discovery = {"schema_version": 1, "semantic_fingerprint": seed["semantic_fingerprint"], "adoption_fingerprint": seed["adoption_fingerprint"], "clause_accounts": [{"clause": "SC-001", "disposition": "discover", "question_ids": ["Q-001"]}, {"clause": "SC-002", "disposition": "no_environment_dependency", "reason": "pure semantic invariant"}], "questions": questions}
        self.environment = {"schema_version": 1, "semantic_fingerprint": seed["semantic_fingerprint"], "adoption_fingerprint": seed["adoption_fingerprint"], "identity": {"target": "fixture", "runtime": "fixture-runtime"}, "facts": facts, "capabilities": [{"id": "CAP-001", "name": "independent_execution", "support": "native", "mechanism": "isolated child execution", "fact_refs": ["F-001"]}], "provider_surfaces": [{"id": "PS-001", "kind": "runtime_package", "status": "reachable", "query_mechanism": "runtime package search", "install_mechanism": "runtime package install", "trust_scope": "runtime_official", "fact_refs": [core_fact_by_question["ENV-PROVIDER-SURFACES"]]}], "project_mechanisms": [], "existing_harness": [], "constraints": [], "unknowns": []}

    def validate(self, discovery=None, environment=None):
        return validate_environment(self.ir, self.adoption, discovery or self.discovery, environment or self.environment, DISCOVERY_SCHEMA, ENVIRONMENT_SCHEMA)

    def test_prepare_accounts_for_every_clause(self) -> None:
        seed = prepare(self.ir, self.adoption)
        self.assertEqual([item["clause"] for item in seed["clause_work_items"]], ["SC-001", "SC-002"])
        self.assertEqual(len(seed["core_questions"]), 5)

    def test_valid_environment_handoff_passes(self) -> None:
        self.assertTrue(self.validate()["passed"])

    def test_missing_core_question_fails(self) -> None:
        discovery = copy.deepcopy(self.discovery)
        discovery["questions"] = [item for item in discovery["questions"] if item["id"] != "ENV-PROVIDER-SURFACES"]
        result = self.validate(discovery=discovery)
        self.assertFalse(result["passed"])
        self.assertIn("CORE_DISCOVERY_GAP", {item["code"] for item in result["diagnostics"]})

    def test_missing_clause_account_fails(self) -> None:
        discovery = copy.deepcopy(self.discovery)
        discovery["clause_accounts"].pop()
        result = self.validate(discovery=discovery)
        self.assertFalse(result["passed"])
        self.assertIn("CLAUSE_DISCOVERY_COVERAGE_GAP", {item["code"] for item in result["diagnostics"]})

    def test_claimed_capability_needs_confirmed_fact(self) -> None:
        environment = copy.deepcopy(self.environment)
        environment["facts"][-1]["confidence"] = "inferred"
        result = self.validate(environment=environment)
        self.assertFalse(result["passed"])
        self.assertIn("CAPABILITY_WITHOUT_CONFIRMED_EVIDENCE", {item["code"] for item in result["diagnostics"]})

    def test_provider_surface_needs_confirmed_fact(self) -> None:
        environment = copy.deepcopy(self.environment)
        surface_fact = environment["provider_surfaces"][0]["fact_refs"][0]
        for fact in environment["facts"]:
            if fact["id"] == surface_fact:
                fact["confidence"] = "inferred"
        result = self.validate(environment=environment)
        self.assertFalse(result["passed"])
        self.assertIn("PROVIDER_SURFACE_WITHOUT_CONFIRMED_EVIDENCE", {item["code"] for item in result["diagnostics"]})

    def test_blocking_unknown_fails(self) -> None:
        environment = copy.deepcopy(self.environment)
        environment["unknowns"] = [{"id": "U-001", "question": "loader unknown", "affects_clauses": ["SC-001"], "blocking": True}]
        result = self.validate(environment=environment)
        self.assertFalse(result["passed"])
        self.assertIn("BLOCKING_ENVIRONMENT_UNKNOWN", {item["code"] for item in result["diagnostics"]})


if __name__ == "__main__":
    unittest.main()
