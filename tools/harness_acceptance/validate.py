"""Validate real-runtime Harness verification and fresh-agent acceptance evidence."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .prepare import REQUIRED_ACCEPTANCE_CATEGORIES
from .shared import diagnostic, report, sha256_file, sha256_json


FAULT_LAYERS = {"semantic", "environment", "adaptation", "candidate", "runtime"}


def _schema_errors(schema: dict[str, Any], value: dict[str, Any], label: str) -> list[dict[str, Any]]:
    errors = []
    for error in sorted(Draft202012Validator(schema).iter_errors(value), key=lambda item: list(item.path)):
        errors.append(diagnostic("SCHEMA_ERROR", f"{label}: {error.message}", path=list(error.path)))
    return errors


def _runtime_matches(expected: dict[str, Any], actual: dict[str, Any]) -> bool:
    if actual.get("target") != expected.get("target") or actual.get("runtime") != expected.get("runtime"):
        return False
    expected_version = expected.get("runtime_version")
    return expected_version is None or actual.get("runtime_version") == expected_version


def validate_acceptance(
    semantic_ir: dict[str, Any],
    environment: dict[str, Any],
    adoption: dict[str, Any],
    adaptation_plan: dict[str, Any],
    candidate: dict[str, Any],
    verification_plan: dict[str, Any],
    verification_report: dict[str, Any],
    acceptance_receipt: dict[str, Any],
    verification_plan_schema: dict[str, Any],
    verification_report_schema: dict[str, Any],
    acceptance_receipt_schema: dict[str, Any],
    target_root: Path | None = None,
) -> dict[str, Any]:
    diagnostics = _schema_errors(verification_plan_schema, verification_plan, "verification_plan")
    diagnostics.extend(_schema_errors(verification_report_schema, verification_report, "verification_report"))
    diagnostics.extend(_schema_errors(acceptance_receipt_schema, acceptance_receipt, "acceptance_receipt"))

    fingerprints = {
        "semantic_fingerprint": sha256_json(semantic_ir),
        "environment_fingerprint": sha256_json(environment),
        "adoption_fingerprint": sha256_json(adoption),
        "plan_fingerprint": sha256_json(adaptation_plan),
        "candidate_fingerprint": sha256_json(candidate),
    }
    for label, value in (("verification_plan", verification_plan), ("verification_report", verification_report), ("acceptance_receipt", acceptance_receipt)):
        for key, expected in fingerprints.items():
            if value.get(key) != expected:
                diagnostics.append(diagnostic("FINGERPRINT_MISMATCH", f"{label} is not bound to current {key}", artifact=label, fingerprint=key))

    if verification_report.get("verification_plan_fingerprint") != sha256_json(verification_plan):
        diagnostics.append(diagnostic("VERIFICATION_PLAN_FINGERPRINT_MISMATCH", "verification report is not bound to the current Verification Plan"))
    if acceptance_receipt.get("verification_report_fingerprint") != sha256_json(verification_report):
        diagnostics.append(diagnostic("VERIFICATION_REPORT_FINGERPRINT_MISMATCH", "acceptance receipt is not bound to the current Verification Report"))

    expected_runtime = environment.get("identity", {}) if isinstance(environment.get("identity"), dict) else {}
    for label, value in (("verification_report", verification_report), ("acceptance_receipt", acceptance_receipt)):
        actual_runtime = value.get("runtime_identity", {}) if isinstance(value.get("runtime_identity"), dict) else {}
        if not _runtime_matches(expected_runtime, actual_runtime):
            diagnostics.append(diagnostic("RUNTIME_IDENTITY_MISMATCH", f"{label} runtime identity does not match the Environment Model", artifact=label))

    all_clauses = {item.get("id") for item in semantic_ir.get("clauses", []) if isinstance(item, dict) and isinstance(item.get("id"), str)}
    accounts = adaptation_plan.get("clause_accounts", []) if isinstance(adaptation_plan.get("clause_accounts"), list) else []
    covered_clauses = {item.get("clause") for item in accounts if isinstance(item, dict) and item.get("disposition") == "covered"}
    blocked_clauses = {item.get("clause") for item in accounts if isinstance(item, dict) and item.get("disposition") == "blocked"}
    if blocked_clauses:
        diagnostics.append(diagnostic("BLOCKED_ADAPTATION_RECEIVED", "Stage 4 cannot accept a Candidate with blocked adaptation Clauses", clauses=sorted(blocked_clauses)))

    artifact_by_id = {item.get("id"): item for item in candidate.get("artifacts", []) if isinstance(item, dict) and isinstance(item.get("id"), str)}
    provider_by_id = {item.get("id"): item for item in adaptation_plan.get("providers", []) if isinstance(item, dict) and isinstance(item.get("id"), str)}
    component_ids = {item.get("id") for item in candidate.get("components", []) if isinstance(item, dict) and isinstance(item.get("id"), str)}
    selected_providers = {
        item.get("selected_provider")
        for item in adaptation_plan.get("requirements", [])
        if isinstance(item, dict) and isinstance(item.get("selected_provider"), str)
    }

    target = target_root.resolve() if target_root is not None else None
    if target is not None:
        for artifact_id, artifact in artifact_by_id.items():
            path = artifact.get("path")
            if not isinstance(path, str):
                continue
            candidate_path = (target / path).resolve()
            try:
                candidate_path.relative_to(target)
            except ValueError:
                diagnostics.append(diagnostic("ARTIFACT_OUTSIDE_TARGET", "candidate artifact path escapes target root", artifact=artifact_id, path=path))
                continue
            if not candidate_path.is_file():
                diagnostics.append(diagnostic("MISSING_CANDIDATE_ARTIFACT", "candidate artifact no longer exists at acceptance time", artifact=artifact_id, path=path))
            elif artifact.get("content_sha256") != sha256_file(candidate_path):
                diagnostics.append(diagnostic("ARTIFACT_CONTENT_DRIFT", "candidate artifact changed after Stage 3 handoff", artifact=artifact_id, path=path))

    clause_verifications = verification_plan.get("clause_verifications", []) if isinstance(verification_plan.get("clause_verifications"), list) else []
    verification_by_id = {item.get("id"): item for item in clause_verifications if isinstance(item, dict) and isinstance(item.get("id"), str)}
    if len(verification_by_id) != len(clause_verifications):
        diagnostics.append(diagnostic("DUPLICATE_VERIFICATION_ID", "Clause verification ids must be unique"))
    planned_clause_coverage = {item.get("clause") for item in clause_verifications if isinstance(item, dict)}
    if not covered_clauses.issubset(planned_clause_coverage):
        diagnostics.append(diagnostic("CLAUSE_VERIFICATION_PLAN_GAP", "every covered Clause requires at least one verification method", clauses=sorted(covered_clauses - planned_clause_coverage)))
    unknown_verified = planned_clause_coverage - covered_clauses
    if unknown_verified:
        diagnostics.append(diagnostic("VERIFIES_NONCOVERED_CLAUSE", "Verification Plan may only verify covered Clauses", clauses=sorted(unknown_verified)))

    clause_results = verification_report.get("clause_results", []) if isinstance(verification_report.get("clause_results"), list) else []
    clause_result_by_id = {item.get("verification_id"): item for item in clause_results if isinstance(item, dict) and isinstance(item.get("verification_id"), str)}
    if len(clause_result_by_id) != len(clause_results):
        diagnostics.append(diagnostic("DUPLICATE_CLAUSE_RESULT", "verification result ids must be unique"))
    for verification_id, planned in verification_by_id.items():
        result = clause_result_by_id.get(verification_id)
        if result is None:
            diagnostics.append(diagnostic("MISSING_CLAUSE_VERIFICATION_RESULT", "planned Clause verification has no result", verification=verification_id, clause=planned.get("clause")))
        elif result.get("clause") != planned.get("clause"):
            diagnostics.append(diagnostic("CLAUSE_RESULT_TRACE_MISMATCH", "Clause result does not match planned verification", verification=verification_id))
        elif result.get("verdict") != "pass":
            diagnostics.append(diagnostic("CLAUSE_VERIFICATION_FAILED", "covered Clause verification did not pass", verification=verification_id, clause=planned.get("clause")))
        elif not result.get("evidence"):
            diagnostics.append(diagnostic("CLAUSE_VERIFICATION_WITHOUT_EVIDENCE", "passing Clause verification requires evidence", verification=verification_id))

    artifact_probes = verification_plan.get("artifact_probes", []) if isinstance(verification_plan.get("artifact_probes"), list) else []
    artifact_probe_by_id = {item.get("id"): item for item in artifact_probes if isinstance(item, dict) and isinstance(item.get("id"), str)}
    probed_artifacts = [item.get("artifact_ref") for item in artifact_probes if isinstance(item, dict)]
    if set(probed_artifacts) != set(artifact_by_id) or len(probed_artifacts) != len(set(probed_artifacts)):
        diagnostics.append(diagnostic("ARTIFACT_PROBE_COVERAGE_GAP", "every Candidate Artifact requires exactly one Runtime visibility probe"))
    artifact_results = verification_report.get("artifact_results", []) if isinstance(verification_report.get("artifact_results"), list) else []
    artifact_result_by_probe = {item.get("probe_id"): item for item in artifact_results if isinstance(item, dict) and isinstance(item.get("probe_id"), str)}
    for probe_id, planned in artifact_probe_by_id.items():
        result = artifact_result_by_probe.get(probe_id)
        if result is None:
            diagnostics.append(diagnostic("MISSING_ARTIFACT_PROBE_RESULT", "Artifact Runtime probe has no result", probe=probe_id))
        elif result.get("artifact_ref") != planned.get("artifact_ref"):
            diagnostics.append(diagnostic("ARTIFACT_PROBE_TRACE_MISMATCH", "Artifact Runtime probe result does not match plan", probe=probe_id))
        elif result.get("runtime_visible") is not True:
            diagnostics.append(diagnostic("ARTIFACT_NOT_RUNTIME_VISIBLE", "Candidate Artifact exists but is not proven visible to the real Runtime", artifact=planned.get("artifact_ref")))

    provider_probes = verification_plan.get("provider_probes", []) if isinstance(verification_plan.get("provider_probes"), list) else []
    provider_probe_by_id = {item.get("id"): item for item in provider_probes if isinstance(item, dict) and isinstance(item.get("id"), str)}
    probed_providers = [item.get("provider_ref") for item in provider_probes if isinstance(item, dict)]
    if set(probed_providers) != selected_providers or len(probed_providers) != len(set(probed_providers)):
        diagnostics.append(diagnostic("PROVIDER_PROBE_COVERAGE_GAP", "every selected Provider requires exactly one active-state probe"))
    provider_results = verification_report.get("provider_results", []) if isinstance(verification_report.get("provider_results"), list) else []
    provider_result_by_probe = {item.get("probe_id"): item for item in provider_results if isinstance(item, dict) and isinstance(item.get("probe_id"), str)}
    for probe_id, planned in provider_probe_by_id.items():
        provider_ref = planned.get("provider_ref")
        if provider_ref not in provider_by_id:
            diagnostics.append(diagnostic("UNKNOWN_PROVIDER_PROBE", "Provider probe references unknown Provider", probe=probe_id, provider=provider_ref))
        result = provider_result_by_probe.get(probe_id)
        if result is None:
            diagnostics.append(diagnostic("MISSING_PROVIDER_PROBE_RESULT", "Provider active-state probe has no result", probe=probe_id))
        elif result.get("provider_ref") != provider_ref:
            diagnostics.append(diagnostic("PROVIDER_PROBE_TRACE_MISMATCH", "Provider probe result does not match plan", probe=probe_id))
        elif result.get("active") is not True:
            diagnostics.append(diagnostic("PROVIDER_NOT_ACTIVE", "selected Provider is not proven active in the real Runtime", provider=provider_ref))

    mutations = verification_plan.get("mutations", []) if isinstance(verification_plan.get("mutations"), list) else []
    mutation_by_id = {item.get("id"): item for item in mutations if isinstance(item, dict) and isinstance(item.get("id"), str)}
    if len(mutation_by_id) != len(mutations):
        diagnostics.append(diagnostic("DUPLICATE_MUTATION_ID", "Mutation ids must be unique"))
    for mutation_id, mutation in mutation_by_id.items():
        for clause in mutation.get("required_by", []):
            if clause not in covered_clauses:
                diagnostics.append(diagnostic("MUTATION_TRACE_MISMATCH", "Mutation required_by must reference covered Clauses", mutation=mutation_id, clause=clause))
        target_type = mutation.get("target_type")
        target_ref = mutation.get("target_ref")
        known = (
            target_ref in all_clauses if target_type == "clause" else
            target_ref in provider_by_id if target_type == "provider" else
            target_ref in component_ids if target_type == "component" else
            target_ref in artifact_by_id if target_type == "artifact" else False
        )
        if not known:
            diagnostics.append(diagnostic("UNKNOWN_MUTATION_TARGET", "Mutation target does not exist", mutation=mutation_id, target=target_ref))
    mutation_results = verification_report.get("mutation_results", []) if isinstance(verification_report.get("mutation_results"), list) else []
    mutation_result_by_id = {item.get("mutation_id"): item for item in mutation_results if isinstance(item, dict) and isinstance(item.get("mutation_id"), str)}
    for mutation_id in mutation_by_id:
        result = mutation_result_by_id.get(mutation_id)
        if result is None:
            diagnostics.append(diagnostic("MISSING_MUTATION_RESULT", "planned semantic mutation has no result", mutation=mutation_id))
        elif result.get("detected") is not True:
            diagnostics.append(diagnostic("MUTATION_UNDETECTED", "verification failed to detect semantic weakening", mutation=mutation_id))

    findings = verification_report.get("findings", []) if isinstance(verification_report.get("findings"), list) else []
    for finding in findings:
        if not isinstance(finding, dict):
            continue
        if finding.get("fault_layer") not in FAULT_LAYERS:
            continue
        if finding.get("blocking") is True:
            diagnostics.append(diagnostic("BLOCKING_VERIFICATION_FINDING", "blocking Harness verification finding remains open", finding=finding.get("id"), fault_layer=finding.get("fault_layer")))
    if verification_report.get("verdict") != "pass":
        diagnostics.append(diagnostic("VERIFICATION_REPORT_FAILED", "Verification Report must pass before Fresh-Agent Acceptance"))

    planned_cases = verification_plan.get("acceptance_cases", []) if isinstance(verification_plan.get("acceptance_cases"), list) else []
    planned_case_by_id = {item.get("id"): item for item in planned_cases if isinstance(item, dict) and isinstance(item.get("id"), str)}
    if len(planned_case_by_id) != len(planned_cases):
        diagnostics.append(diagnostic("DUPLICATE_ACCEPTANCE_CASE_ID", "Acceptance Case ids must be unique"))
    category_counts = Counter(item.get("category") for item in planned_cases if isinstance(item, dict))
    missing_categories = [category for category in REQUIRED_ACCEPTANCE_CATEGORIES if category_counts[category] == 0]
    if missing_categories:
        diagnostics.append(diagnostic("ACCEPTANCE_CATEGORY_GAP", "Fresh-Agent Acceptance must include all required representative categories", categories=missing_categories))
    for case in planned_cases:
        if not isinstance(case, dict):
            continue
        invalid_clauses = set(case.get("covered_clauses", [])) - covered_clauses
        if invalid_clauses:
            diagnostics.append(diagnostic("ACCEPTANCE_CASE_TRACE_MISMATCH", "Acceptance Case may only reference covered Clauses", case=case.get("id"), clauses=sorted(invalid_clauses)))

    executor = acceptance_receipt.get("executor", {}) if isinstance(acceptance_receipt.get("executor"), dict) else {}
    if executor.get("fresh_context") is not True or executor.get("independent") is not True or not executor.get("isolation_evidence"):
        diagnostics.append(diagnostic("FRESH_ACCEPTANCE_REQUIRED", "Acceptance Receipt requires an independent Fresh Context with isolation evidence"))

    receipt_cases = acceptance_receipt.get("cases", []) if isinstance(acceptance_receipt.get("cases"), list) else []
    receipt_case_by_id = {item.get("case_id"): item for item in receipt_cases if isinstance(item, dict) and isinstance(item.get("case_id"), str)}
    if len(receipt_case_by_id) != len(receipt_cases):
        diagnostics.append(diagnostic("DUPLICATE_ACCEPTANCE_RESULT", "Acceptance result case ids must be unique"))
    for case_id, planned in planned_case_by_id.items():
        result = receipt_case_by_id.get(case_id)
        if result is None:
            diagnostics.append(diagnostic("MISSING_ACCEPTANCE_CASE_RESULT", "planned Fresh-Agent Acceptance Case has no result", case=case_id))
            continue
        if result.get("category") != planned.get("category") or result.get("input") != planned.get("input") or result.get("expected_semantics") != planned.get("expected_semantics"):
            diagnostics.append(diagnostic("ACCEPTANCE_CASE_PLAN_MISMATCH", "Acceptance result does not match the planned case", case=case_id))
        if set(result.get("covered_clauses", [])) != set(planned.get("covered_clauses", [])):
            diagnostics.append(diagnostic("ACCEPTANCE_CASE_CLAUSE_MISMATCH", "Acceptance result Clause trace does not match plan", case=case_id))
        if result.get("verdict") != "pass":
            diagnostics.append(diagnostic("ACCEPTANCE_CASE_FAILED", "Fresh-Agent Acceptance Case did not pass", case=case_id, category=planned.get("category")))
        if not result.get("evidence"):
            diagnostics.append(diagnostic("ACCEPTANCE_CASE_WITHOUT_EVIDENCE", "passing Acceptance Case requires evidence", case=case_id))

    if acceptance_receipt.get("final_verdict") != "READY":
        diagnostics.append(diagnostic("HARNESS_NOT_READY", "Acceptance Receipt final_verdict must be READY"))

    passed = not diagnostics
    return report(
        "harness-acceptance-validate",
        passed,
        diagnostics,
        verdict="READY" if passed else "BLOCKED",
        summary={
            "covered_clauses": len(covered_clauses),
            "clause_verifications": len(clause_verifications),
            "artifact_probes": len(artifact_probes),
            "provider_probes": len(provider_probes),
            "mutations": len(mutations),
            "acceptance_cases": len(planned_cases),
        },
    )
