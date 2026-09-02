"""Validate Environment Discovery coverage and evidence for V3 handoff."""

from __future__ import annotations

from typing import Any

from jsonschema import Draft202012Validator

from .shared import diagnostic, report, sha256_json


SUPPORT_MODES = {"native", "composable", "external", "unavailable", "unknown"}
QUESTION_STATES = {"confirmed", "not_applicable", "unknown", "blocked"}


def _schema_errors(schema: dict[str, Any], value: dict[str, Any], label: str) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for error in sorted(Draft202012Validator(schema).iter_errors(value), key=lambda item: list(item.path)):
        errors.append(diagnostic("SCHEMA_ERROR", f"{label}: {error.message}", path=list(error.path)))
    return errors


def validate_environment(
    semantic_ir: dict[str, Any],
    adoption: dict[str, Any],
    discovery: dict[str, Any],
    environment: dict[str, Any],
    discovery_schema: dict[str, Any],
    environment_schema: dict[str, Any],
) -> dict[str, Any]:
    diagnostics = _schema_errors(discovery_schema, discovery, "discovery")
    diagnostics.extend(_schema_errors(environment_schema, environment, "environment"))

    semantic_fingerprint = sha256_json(semantic_ir)
    adoption_fingerprint = sha256_json(adoption)
    for label, value in (("discovery", discovery), ("environment", environment)):
        if value.get("semantic_fingerprint") != semantic_fingerprint:
            diagnostics.append(diagnostic("SEMANTIC_FINGERPRINT_MISMATCH", f"{label} is not bound to the current Semantic IR"))
        if value.get("adoption_fingerprint") != adoption_fingerprint:
            diagnostics.append(diagnostic("ADOPTION_FINGERPRINT_MISMATCH", f"{label} is not bound to the current Adoption Context"))

    clause_ids = {item.get("id") for item in semantic_ir.get("clauses", []) if isinstance(item, dict)}
    accounts = discovery.get("clause_accounts", []) if isinstance(discovery.get("clause_accounts"), list) else []
    account_ids = [item.get("clause") for item in accounts if isinstance(item, dict)]
    if set(account_ids) != clause_ids or len(account_ids) != len(clause_ids):
        diagnostics.append(diagnostic("CLAUSE_DISCOVERY_COVERAGE_GAP", "every Semantic Clause must have exactly one discovery disposition"))

    questions = discovery.get("questions", []) if isinstance(discovery.get("questions"), list) else []
    question_by_id = {item.get("id"): item for item in questions if isinstance(item, dict) and isinstance(item.get("id"), str)}
    if len(question_by_id) != len(questions):
        diagnostics.append(diagnostic("DUPLICATE_DISCOVERY_QUESTION", "discovery question ids must be unique"))

    facts = environment.get("facts", []) if isinstance(environment.get("facts"), list) else []
    fact_by_id = {item.get("id"): item for item in facts if isinstance(item, dict) and isinstance(item.get("id"), str)}
    if len(fact_by_id) != len(facts):
        diagnostics.append(diagnostic("DUPLICATE_ENVIRONMENT_FACT", "environment fact ids must be unique"))

    for account in accounts:
        if not isinstance(account, dict):
            continue
        clause = account.get("clause")
        disposition = account.get("disposition")
        if disposition == "discover":
            question_ids = account.get("question_ids")
            if not isinstance(question_ids, list) or not question_ids:
                diagnostics.append(diagnostic("MISSING_DISCOVERY_QUESTION", "discover disposition requires question_ids", clause=clause))
                continue
            for question_id in question_ids:
                question = question_by_id.get(question_id)
                if question is None:
                    diagnostics.append(diagnostic("UNKNOWN_DISCOVERY_QUESTION", "clause references an unknown discovery question", clause=clause, question=question_id))
                elif clause not in question.get("required_by", []):
                    diagnostics.append(diagnostic("QUESTION_TRACE_MISMATCH", "question.required_by must include the clause that references it", clause=clause, question=question_id))
        elif disposition == "no_environment_dependency":
            if not isinstance(account.get("reason"), str) or not account["reason"].strip():
                diagnostics.append(diagnostic("MISSING_NO_DEPENDENCY_REASON", "no_environment_dependency requires a reason", clause=clause))

    for question in questions:
        if not isinstance(question, dict):
            continue
        status = question.get("status")
        if status not in QUESTION_STATES:
            continue
        if status == "confirmed":
            refs = question.get("fact_refs")
            if not isinstance(refs, list) or not refs:
                diagnostics.append(diagnostic("CONFIRMED_WITHOUT_FACT", "confirmed discovery question requires fact_refs", question=question.get("id")))
            else:
                for ref in refs:
                    fact = fact_by_id.get(ref)
                    if fact is None:
                        diagnostics.append(diagnostic("UNKNOWN_FACT_REFERENCE", "question references an unknown environment fact", question=question.get("id"), fact=ref))
                    elif fact.get("confidence") != "confirmed":
                        diagnostics.append(diagnostic("UNCONFIRMED_EVIDENCE", "confirmed discovery question must resolve through confirmed facts", question=question.get("id"), fact=ref))
        if status in {"unknown", "blocked"} and question.get("blocking") is True:
            diagnostics.append(diagnostic("BLOCKING_DISCOVERY_UNKNOWN", "a required environment question remains unresolved", question=question.get("id"), status=status))

    for fact in facts:
        if not isinstance(fact, dict):
            continue
        if fact.get("confidence") == "confirmed" and not fact.get("evidence"):
            diagnostics.append(diagnostic("FACT_WITHOUT_EVIDENCE", "confirmed fact requires evidence", fact=fact.get("id")))

    for capability in environment.get("capabilities", []):
        if not isinstance(capability, dict):
            continue
        support = capability.get("support")
        if support not in SUPPORT_MODES:
            continue
        refs = capability.get("fact_refs", [])
        if support != "unknown":
            if not refs:
                diagnostics.append(diagnostic("CAPABILITY_WITHOUT_FACT", "resolved capability requires supporting facts", capability=capability.get("id")))
            elif not any(fact_by_id.get(ref, {}).get("confidence") == "confirmed" for ref in refs):
                diagnostics.append(diagnostic("CAPABILITY_WITHOUT_CONFIRMED_EVIDENCE", "resolved capability needs at least one confirmed fact", capability=capability.get("id")))
        for ref in refs:
            if ref not in fact_by_id:
                diagnostics.append(diagnostic("UNKNOWN_FACT_REFERENCE", "capability references an unknown environment fact", capability=capability.get("id"), fact=ref))

    for unknown in environment.get("unknowns", []):
        if isinstance(unknown, dict) and unknown.get("blocking") is True:
            diagnostics.append(diagnostic("BLOCKING_ENVIRONMENT_UNKNOWN", "Environment Model contains a blocking unknown", unknown=unknown.get("id")))

    return report(
        "environment-validate",
        not diagnostics,
        diagnostics,
        summary={
            "clauses": len(clause_ids),
            "questions": len(questions),
            "facts": len(facts),
            "capabilities": len(environment.get("capabilities", [])),
        },
    )
