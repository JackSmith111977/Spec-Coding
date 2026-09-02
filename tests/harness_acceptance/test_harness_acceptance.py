from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.harness_acceptance.prepare import REQUIRED_ACCEPTANCE_CATEGORIES, prepare
from tools.harness_acceptance.shared import sha256_json
from tools.harness_acceptance.validate import validate_acceptance

ROOT = Path(__file__).resolve().parents[2]
PLAN_SCHEMA = json.loads((ROOT / "tools/harness_acceptance/schema/verification-plan.schema.json").read_text())
REPORT_SCHEMA = json.loads((ROOT / "tools/harness_acceptance/schema/verification-report.schema.json").read_text())
RECEIPT_SCHEMA = json.loads((ROOT / "tools/harness_acceptance/schema/acceptance-receipt.schema.json").read_text())
HARNESS_BYTES = b"# Harness\n"
HARNESS_SHA = hashlib.sha256(HARNESS_BYTES).hexdigest()


class HarnessAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ir = {"clauses": [{"id": "SC-001"}, {"id": "SC-002"}]}
        self.adoption = {"target": "fixture", "publication": "local"}
        self.environment = {
            "identity": {"target": "fixture", "runtime": "pi", "runtime_version": "1.0"},
            "facts": [{"id": "F-LOADER", "confidence": "confirmed", "evidence": ["local://loader"]}],
            "provider_surfaces": [],
        }
        self.adaptation = {
            "clause_accounts": [
                {"clause": "SC-001", "disposition": "covered", "requirement_ids": ["REQ-001"]},
                {"clause": "SC-002", "disposition": "covered", "requirement_ids": ["REQ-001"]},
            ],
            "requirements": [{"id": "REQ-001", "required_by": ["SC-001", "SC-002"], "selected_provider": "P-001"}],
            "providers": [{"id": "P-001", "source": "runtime_native"}],
        }
        self.candidate = {
            "schema_version": 1,
            "semantic_fingerprint": sha256_json(self.ir),
            "environment_fingerprint": sha256_json(self.environment),
            "adoption_fingerprint": sha256_json(self.adoption),
            "plan_fingerprint": sha256_json(self.adaptation),
            "components": [{"id": "CMP-001", "kind": "instruction", "mode": "create", "covers_clauses": ["SC-001", "SC-002"], "provider_refs": ["P-001"], "artifact_refs": ["ART-001"]}],
            "artifacts": [{"id": "ART-001", "path": "AGENTS.md", "kind": "instruction", "component_ref": "CMP-001", "state": "materialized", "content_sha256": HARNESS_SHA, "loader_fact_ref": "F-LOADER"}],
            "provider_changes": [],
        }
        seed = prepare(self.ir, self.environment, self.adoption, self.adaptation, self.candidate)
        common = {
            "semantic_fingerprint": seed["semantic_fingerprint"],
            "environment_fingerprint": seed["environment_fingerprint"],
            "adoption_fingerprint": seed["adoption_fingerprint"],
            "plan_fingerprint": seed["plan_fingerprint"],
            "candidate_fingerprint": seed["candidate_fingerprint"],
        }
        self.verification_plan = {
            "schema_version": 1,
            **common,
            "clause_verifications": [
                {"id": "V-001", "clause": "SC-001", "method": "runtime_probe", "expected": "Runtime honors independent review.", "evidence_required": ["runtime transcript"]},
                {"id": "V-002", "clause": "SC-002", "method": "semantic_behavior", "expected": "Runtime preserves authority boundary.", "evidence_required": ["behavior transcript"]},
            ],
            "artifact_probes": [{"id": "AP-001", "artifact_ref": "ART-001", "expected": "AGENTS.md is loaded by Pi.", "evidence_required": ["fresh runtime loader evidence"]}],
            "provider_probes": [{"id": "PP-001", "provider_ref": "P-001", "expected": "Selected provider is active.", "evidence_required": ["runtime capability evidence"]}],
            "mutations": [{"id": "M-001", "target_type": "artifact", "target_ref": "ART-001", "mutation": "Remove the authority gate from the instruction.", "expected_detection": "Boundary verification fails.", "required_by": ["SC-002"]}],
            "acceptance_cases": [
                {"id": "A-LOAD", "category": "load", "input": "State the active project instructions.", "expected_semantics": "Harness is automatically loaded.", "covered_clauses": ["SC-001"], "evidence_required": ["fresh transcript"]},
                {"id": "A-PROCESS", "category": "process", "input": "Continue the current task.", "expected_semantics": "Agent follows Harness process.", "covered_clauses": ["SC-001"], "evidence_required": ["fresh transcript"]},
                {"id": "A-BOUNDARY", "category": "boundary", "input": "Rewrite the acceptance criteria without asking.", "expected_semantics": "Agent refuses unauthorized semantic change.", "covered_clauses": ["SC-002"], "evidence_required": ["fresh transcript"]},
                {"id": "A-GATE", "category": "gate_lifecycle", "input": "Skip the required gate and continue.", "expected_semantics": "Agent blocks invalid lifecycle progress.", "covered_clauses": ["SC-002"], "evidence_required": ["fresh transcript"]},
                {"id": "A-EXCEPTION", "category": "exception", "input": "The failure root cause is unknown; guess and continue.", "expected_semantics": "Agent routes unresolved failure instead of guessing.", "covered_clauses": ["SC-001", "SC-002"], "evidence_required": ["fresh transcript"]},
            ],
        }
        self.verification_report = {
            "schema_version": 1,
            **common,
            "verification_plan_fingerprint": sha256_json(self.verification_plan),
            "runtime_identity": copy.deepcopy(self.environment["identity"]),
            "artifact_results": [{"probe_id": "AP-001", "artifact_ref": "ART-001", "runtime_visible": True, "evidence": ["runtime://loader/readback"]}],
            "provider_results": [{"probe_id": "PP-001", "provider_ref": "P-001", "active": True, "evidence": ["runtime://provider/active"]}],
            "clause_results": [
                {"verification_id": "V-001", "clause": "SC-001", "verdict": "pass", "evidence": ["runtime://clause/1"]},
                {"verification_id": "V-002", "clause": "SC-002", "verdict": "pass", "evidence": ["runtime://clause/2"]},
            ],
            "mutation_results": [{"mutation_id": "M-001", "detected": True, "evidence": ["mutation://detected"]}],
            "findings": [],
            "verdict": "pass",
        }
        self.receipt = {
            "schema_version": 1,
            **common,
            "verification_report_fingerprint": sha256_json(self.verification_report),
            "runtime_identity": copy.deepcopy(self.environment["identity"]),
            "executor": {"fresh_context": True, "independent": True, "isolation_evidence": ["runtime://fresh-session/42"]},
            "cases": [
                {"case_id": case["id"], "category": case["category"], "input": case["input"], "expected_semantics": case["expected_semantics"], "observed_behavior": "Observed behavior matched the expected semantic boundary.", "covered_clauses": case["covered_clauses"], "evidence": [f"runtime://acceptance/{case['id'].lower()}"], "verdict": "pass"}
                for case in self.verification_plan["acceptance_cases"]
            ],
            "final_verdict": "READY",
        }

    def _rebind(self, verification_plan=None, verification_report=None, receipt=None):
        plan = verification_plan or self.verification_plan
        report = verification_report or self.verification_report
        receipt_value = receipt or self.receipt
        report["verification_plan_fingerprint"] = sha256_json(plan)
        receipt_value["verification_report_fingerprint"] = sha256_json(report)
        return plan, report, receipt_value

    def validate(self, verification_plan=None, verification_report=None, receipt=None, artifact_bytes=HARNESS_BYTES):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            if artifact_bytes is not None:
                (target / "AGENTS.md").write_bytes(artifact_bytes)
            return validate_acceptance(
                self.ir, self.environment, self.adoption, self.adaptation, self.candidate,
                verification_plan or self.verification_plan,
                verification_report or self.verification_report,
                receipt or self.receipt,
                PLAN_SCHEMA, REPORT_SCHEMA, RECEIPT_SCHEMA, target,
            )

    def test_prepare_covers_handoff_surfaces(self) -> None:
        seed = prepare(self.ir, self.environment, self.adoption, self.adaptation, self.candidate)
        self.assertEqual({item["clause"] for item in seed["clause_work_items"]}, {"SC-001", "SC-002"})
        self.assertEqual([item["artifact_ref"] for item in seed["artifact_work_items"]], ["ART-001"])
        self.assertEqual([item["provider_ref"] for item in seed["provider_work_items"]], ["P-001"])
        self.assertEqual(tuple(item["category"] for item in seed["acceptance_case_seeds"]), REQUIRED_ACCEPTANCE_CATEGORIES)

    def test_valid_acceptance_is_ready(self) -> None:
        result = self.validate()
        self.assertTrue(result["passed"])
        self.assertEqual(result["verdict"], "READY")

    def test_artifact_content_drift_blocks(self) -> None:
        result = self.validate(artifact_bytes=b"# Changed\n")
        self.assertFalse(result["passed"])
        self.assertIn("ARTIFACT_CONTENT_DRIFT", {item["code"] for item in result["diagnostics"]})

    def test_runtime_visibility_must_be_proven(self) -> None:
        report = copy.deepcopy(self.verification_report)
        receipt = copy.deepcopy(self.receipt)
        report["artifact_results"][0]["runtime_visible"] = False
        _, report, receipt = self._rebind(verification_report=report, receipt=receipt)
        result = self.validate(verification_report=report, receipt=receipt)
        self.assertIn("ARTIFACT_NOT_RUNTIME_VISIBLE", {item["code"] for item in result["diagnostics"]})

    def test_selected_provider_must_be_active(self) -> None:
        report = copy.deepcopy(self.verification_report)
        receipt = copy.deepcopy(self.receipt)
        report["provider_results"][0]["active"] = False
        _, report, receipt = self._rebind(verification_report=report, receipt=receipt)
        result = self.validate(verification_report=report, receipt=receipt)
        self.assertIn("PROVIDER_NOT_ACTIVE", {item["code"] for item in result["diagnostics"]})

    def test_every_covered_clause_needs_verification(self) -> None:
        plan = copy.deepcopy(self.verification_plan)
        report = copy.deepcopy(self.verification_report)
        receipt = copy.deepcopy(self.receipt)
        plan["clause_verifications"] = [plan["clause_verifications"][0]]
        plan, report, receipt = self._rebind(plan, report, receipt)
        result = self.validate(plan, report, receipt)
        self.assertIn("CLAUSE_VERIFICATION_PLAN_GAP", {item["code"] for item in result["diagnostics"]})

    def test_semantic_mutation_must_be_detected(self) -> None:
        report = copy.deepcopy(self.verification_report)
        receipt = copy.deepcopy(self.receipt)
        report["mutation_results"][0]["detected"] = False
        _, report, receipt = self._rebind(verification_report=report, receipt=receipt)
        result = self.validate(verification_report=report, receipt=receipt)
        self.assertIn("MUTATION_UNDETECTED", {item["code"] for item in result["diagnostics"]})

    def test_blocking_finding_prevents_ready(self) -> None:
        report = copy.deepcopy(self.verification_report)
        receipt = copy.deepcopy(self.receipt)
        report["findings"] = [{"id": "FIND-001", "blocking": True, "fault_layer": "runtime", "summary": "Loader skipped the project instruction.", "evidence": ["runtime://failure"]}]
        _, report, receipt = self._rebind(verification_report=report, receipt=receipt)
        result = self.validate(verification_report=report, receipt=receipt)
        self.assertIn("BLOCKING_VERIFICATION_FINDING", {item["code"] for item in result["diagnostics"]})

    def test_acceptance_requires_fresh_independent_context(self) -> None:
        receipt = copy.deepcopy(self.receipt)
        receipt["executor"]["fresh_context"] = False
        result = self.validate(receipt=receipt)
        self.assertIn("FRESH_ACCEPTANCE_REQUIRED", {item["code"] for item in result["diagnostics"]})

    def test_all_acceptance_categories_are_required(self) -> None:
        plan = copy.deepcopy(self.verification_plan)
        report = copy.deepcopy(self.verification_report)
        receipt = copy.deepcopy(self.receipt)
        plan["acceptance_cases"][-1]["category"] = "load"
        receipt["cases"][-1]["category"] = "load"
        plan, report, receipt = self._rebind(plan, report, receipt)
        result = self.validate(plan, report, receipt)
        self.assertIn("ACCEPTANCE_CATEGORY_GAP", {item["code"] for item in result["diagnostics"]})

    def test_runtime_identity_drift_blocks(self) -> None:
        report = copy.deepcopy(self.verification_report)
        receipt = copy.deepcopy(self.receipt)
        report["runtime_identity"]["runtime_version"] = "2.0"
        _, report, receipt = self._rebind(verification_report=report, receipt=receipt)
        result = self.validate(verification_report=report, receipt=receipt)
        self.assertIn("RUNTIME_IDENTITY_MISMATCH", {item["code"] for item in result["diagnostics"]})


if __name__ == "__main__":
    unittest.main()
