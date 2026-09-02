"""Prepare a deterministic Environment Discovery seed from Semantic IR."""

from __future__ import annotations

from typing import Any

from .shared import EnvironmentInputError, sha256_json


CORE_QUESTIONS = (
    (
        "ENV-RUNTIME-IDENTITY",
        "runtime",
        "Which runtime and execution surface actually own this Harness compilation?",
        ["runtime metadata", "local executable or configuration evidence"],
    ),
    (
        "ENV-LOADER-SURFACE",
        "runtime",
        "How does the active runtime discover project instructions, procedures, skills, hooks, or extensions?",
        ["local loader/configuration evidence", "version-matched official evidence when local evidence is insufficient"],
    ),
    (
        "ENV-PROVIDER-SURFACES",
        "runtime",
        "Which package, plugin, extension, MCP, or other provider surfaces can be queried on demand for missing capabilities?",
        ["local runtime/package configuration", "runtime-official registry or package evidence when applicable"],
    ),
    (
        "ENV-PROJECT-MECHANISMS",
        "project",
        "Which project-native build, test, lint, typecheck, CI, task, and Git mechanisms can be reused?",
        ["repository files, commands, or CI configuration"],
    ),
    (
        "ENV-EXISTING-HARNESS",
        "harness",
        "Which existing instructions, skills, hooks, extensions, MCP integrations, scripts, or automation already govern the target?",
        ["repository/runtime configuration or directly inspectable harness artifacts"],
    ),
)


def prepare(semantic_ir: dict[str, Any], adoption: dict[str, Any]) -> dict[str, Any]:
    clauses = semantic_ir.get("clauses")
    if not isinstance(clauses, list) or not clauses:
        raise EnvironmentInputError("Semantic IR must contain a non-empty clauses array")

    clause_ids: list[str] = []
    for clause in clauses:
        if not isinstance(clause, dict) or not isinstance(clause.get("id"), str) or not clause["id"].strip():
            raise EnvironmentInputError("every Semantic IR clause must have a non-empty id")
        clause_ids.append(clause["id"])

    if len(clause_ids) != len(set(clause_ids)):
        raise EnvironmentInputError("Semantic IR clause ids must be unique")

    return {
        "schema_version": 1,
        "semantic_fingerprint": sha256_json(semantic_ir),
        "adoption_fingerprint": sha256_json(adoption),
        "clause_work_items": [
            {
                "id": f"DISCOVER-{index:04d}",
                "clause": clause_id,
                "task": "derive_environment_dependencies",
                "status": "PENDING",
            }
            for index, clause_id in enumerate(clause_ids, start=1)
        ],
        "core_questions": [
            {
                "id": question_id,
                "category": category,
                "question": question,
                "evidence_required": evidence,
            }
            for question_id, category, question, evidence in CORE_QUESTIONS
        ],
    }
