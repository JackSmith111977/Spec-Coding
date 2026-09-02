"""Prepare deterministic Verify & Accept work items from a Stage 3 Harness Candidate."""

from __future__ import annotations

from typing import Any

from .shared import HarnessAcceptanceInputError, sha256_json


REQUIRED_ACCEPTANCE_CATEGORIES = ("load", "process", "boundary", "gate_lifecycle", "exception")


def prepare(
    semantic_ir: dict[str, Any],
    environment: dict[str, Any],
    adoption: dict[str, Any],
    adaptation_plan: dict[str, Any],
    candidate: dict[str, Any],
) -> dict[str, Any]:
    covered_clauses = [
        item.get("clause")
        for item in adaptation_plan.get("clause_accounts", [])
        if isinstance(item, dict) and item.get("disposition") == "covered" and isinstance(item.get("clause"), str)
    ]
    if not covered_clauses:
        raise HarnessAcceptanceInputError("Adaptation Plan must contain at least one covered Clause")

    selected_providers = []
    for requirement in adaptation_plan.get("requirements", []):
        if isinstance(requirement, dict) and isinstance(requirement.get("selected_provider"), str):
            selected_providers.append(requirement["selected_provider"])

    artifact_ids = [
        item.get("id")
        for item in candidate.get("artifacts", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]

    return {
        "schema_version": 1,
        "semantic_fingerprint": sha256_json(semantic_ir),
        "environment_fingerprint": sha256_json(environment),
        "adoption_fingerprint": sha256_json(adoption),
        "plan_fingerprint": sha256_json(adaptation_plan),
        "candidate_fingerprint": sha256_json(candidate),
        "clause_work_items": [
            {
                "id": f"VERIFY-CLAUSE-{index:04d}",
                "clause": clause,
                "task": "derive_verification_method",
                "instruction": "Choose the minimum reliable deterministic/runtime/semantic verification that proves this covered Clause in the real Runtime.",
            }
            for index, clause in enumerate(covered_clauses, start=1)
        ],
        "artifact_work_items": [
            {"id": f"VERIFY-ARTIFACT-{index:04d}", "artifact_ref": artifact, "task": "prove_runtime_visibility"}
            for index, artifact in enumerate(artifact_ids, start=1)
        ],
        "provider_work_items": [
            {"id": f"VERIFY-PROVIDER-{index:04d}", "provider_ref": provider, "task": "prove_provider_active"}
            for index, provider in enumerate(dict.fromkeys(selected_providers), start=1)
        ],
        "acceptance_case_seeds": [
            {"category": category, "task": "design_fresh_agent_acceptance_case"}
            for category in REQUIRED_ACCEPTANCE_CATEGORIES
        ],
    }
