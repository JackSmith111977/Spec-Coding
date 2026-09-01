"""Create a complete, non-ready Compilation State source ledger for an Agent."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .shared import CompilerInputError, diagnostic, read_json, report
from .state import VALIDATION_DIMENSIONS


def seed(spec_root: Path, baseline: dict[str, Any], baseline_sha256: str, source_inventory_path: Path) -> dict[str, Any]:
    inventory = read_json(source_inventory_path)
    blocks = inventory.get("source_blocks") if isinstance(inventory, dict) else None
    if not isinstance(blocks, list) or not blocks:
        return report("seed", False, [diagnostic("INVALID_SOURCE_INVENTORY", "source inventory needs non-empty source_blocks")])
    try:
        version = (spec_root / "VERSION").read_text(encoding="utf-8").strip()
    except OSError as error:
        raise CompilerInputError(f"cannot read VERSION: {error}") from error
    sources: list[dict[str, Any]] = []
    for index, block in enumerate(blocks, start=1):
        if not isinstance(block, dict) or block.get("kind") not in {"canonical", "adoption"} or not isinstance(block.get("ref"), str) or not isinstance(block.get("content_sha256"), str):
            return report("seed", False, [diagnostic("INVALID_SOURCE_INVENTORY", "source block is incomplete", index=index)])
        source = {"id": f"SRC-{index:03d}", "kind": block["kind"], "ref": block["ref"], "sha256": block["content_sha256"], "status": "RESOLVED"}
        if block.get("semantic_required") is True:
            source["contracts"] = ["CT-001"]
        else:
            source["guidance_only"] = True
        sources.append(source)
    checks = {dimension: {"status": "fail", "evidence": ["seed://agent-derivation-required"]} for dimension in VALIDATION_DIMENSIONS}
    return report(
        "seed",
        True,
        [],
        state={
            "compilation": {"spec_version": version, "target_id": baseline["target"]["id"], "adoption_sha256": baseline_sha256},
            "sources": sources,
            "contracts": [
                {
                    "id": "CT-001",
                    "source": [source["id"] for source, block in zip(sources, blocks) if block.get("semantic_required") is True],
                    "guarantee": "Every semantically required source must be represented by an explicit Agent-derived Harness guarantee before composition.",
                    "strength": "must",
                }
            ],
            "mappings": [{"contract": "CT-001", "decision": "BLOCKED", "reason": "Agent semantic derivation and independent review are required"}],
            "components": [],
            "validation": {**checks, "unresolved": 0, "blocked": 1, "harness_ready": False},
        },
    )
