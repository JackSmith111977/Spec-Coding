"""Prepare a non-skippable per-Clause capability-analysis worklist."""

from __future__ import annotations

from typing import Any

from .shared import sha256_json


def prepare(semantic_ir: dict[str, Any], environment: dict[str, Any], adoption: dict[str, Any]) -> dict[str, Any]:
    clauses = [item.get("id") for item in semantic_ir.get("clauses", []) if isinstance(item, dict) and isinstance(item.get("id"), str) and item.get("id")]
    return {"schema_version": 1, "semantic_fingerprint": sha256_json(semantic_ir), "environment_fingerprint": sha256_json(environment), "adoption_fingerprint": sha256_json(adoption), "clause_work_items": [{"clause": clause, "task": "derive_capability_requirements", "instruction": "Derive the minimum stable capability/primitive requirements needed to preserve this Clause. Do not select a Runtime-specific provider yet."} for clause in clauses], "provider_surfaces": [{"id": item.get("id"), "kind": item.get("kind"), "status": item.get("status"), "trust_scope": item.get("trust_scope")} for item in environment.get("provider_surfaces", []) if isinstance(item, dict)]}
