"""Turn an Agent-authored semantic derivation into a sealed Compilation State."""

from __future__ import annotations

import copy
import re
from pathlib import Path
from typing import Any

from .shared import diagnostic, read_json, relative_path, report, sha256_bytes


SOURCE_RANGE = re.compile(r"^(SRC-\d{3,})\.\.(SRC-\d{3,})$")
CONTRACT_FIELDS = {"id", "source_selectors", "guarantee", "strength", "prohibits"}
DERIVATION_FIELDS = {"contracts", "mappings", "components", "validation"}


def _expand_selectors(selectors: Any, source_order: list[str]) -> tuple[list[str], str | None]:
    if not isinstance(selectors, list) or not selectors or not all(isinstance(item, str) and item for item in selectors):
        return [], "source_selectors must be a non-empty array of source ids or inclusive source-id ranges"
    index = {source_id: position for position, source_id in enumerate(source_order)}
    selected: list[str] = []
    for selector in selectors:
        match = SOURCE_RANGE.match(selector)
        if match:
            start, end = match.groups()
            if start not in index or end not in index or index[start] > index[end]:
                return [], f"invalid source range: {selector}"
            selected.extend(source_order[index[start] : index[end] + 1])
        elif selector in index:
            selected.append(selector)
        else:
            return [], f"unknown source selector: {selector}"
    if len(set(selected)) != len(selected):
        return [], "a semantic source may appear in only one derived contract"
    return selected, None


def _sealed_components(target_root: Path, components: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not isinstance(components, list) or not components:
        return [], [diagnostic("INVALID_DERIVATION", "derivation.components must be a non-empty array")]
    diagnostics: list[dict[str, Any]] = []
    sealed: list[dict[str, Any]] = []
    for component in components:
        if not isinstance(component, dict):
            diagnostics.append(diagnostic("INVALID_DERIVATION", "component must be an object"))
            continue
        output_component = copy.deepcopy(component)
        outputs = output_component.get("outputs")
        if not isinstance(outputs, list) or not outputs:
            diagnostics.append(diagnostic("INVALID_DERIVATION", "component needs outputs", component=component.get("id")))
            continue
        for output in outputs:
            if not isinstance(output, dict) or not isinstance(output.get("staged"), str):
                diagnostics.append(diagnostic("INVALID_DERIVATION", "component output needs a staged path", component=component.get("id")))
                continue
            try:
                staged = relative_path(target_root, output["staged"])
            except Exception as error:
                diagnostics.append(diagnostic("INVALID_DERIVATION", str(error), component=component.get("id")))
                continue
            if not staged.is_file():
                diagnostics.append(diagnostic("MISSING_STAGED_ARTIFACT", "derivation cannot seal a missing staged artifact", component=component.get("id"), staged=output["staged"]))
                continue
            output["content_sha256"] = sha256_bytes(staged.read_bytes())
        sealed.append(output_component)
    return sealed, diagnostics


def derive(seed_state_path: Path, derivation_path: Path, target_root: Path) -> dict[str, Any]:
    seed = read_json(seed_state_path)
    derivation = read_json(derivation_path)
    if not isinstance(seed, dict) or not isinstance(derivation, dict):
        return report("derive", False, [diagnostic("INVALID_DERIVATION", "seed state and derivation must be JSON objects")])
    unknown = sorted(set(derivation) - DERIVATION_FIELDS)
    if unknown:
        return report("derive", False, [diagnostic("INVALID_DERIVATION", "derivation has unsupported fields", fields=unknown)])
    sources = seed.get("sources")
    raw_contracts = derivation.get("contracts")
    if not isinstance(sources, list) or not isinstance(raw_contracts, list) or not raw_contracts:
        return report("derive", False, [diagnostic("INVALID_DERIVATION", "seed sources and derivation contracts are required")])
    source_order: list[str] = []
    semantic_ids: set[str] = set()
    for source in sources:
        if not isinstance(source, dict) or not isinstance(source.get("id"), str):
            return report("derive", False, [diagnostic("INVALID_DERIVATION", "seed state has an invalid source")])
        source_id = source["id"]
        source_order.append(source_id)
        if source.get("guidance_only") is not True:
            semantic_ids.add(source_id)
    assigned: dict[str, str] = {}
    contracts: list[dict[str, Any]] = []
    for raw in raw_contracts:
        if not isinstance(raw, dict) or set(raw) - CONTRACT_FIELDS:
            return report("derive", False, [diagnostic("INVALID_DERIVATION", "each contract may only contain semantic derivation fields")])
        contract_id = raw.get("id")
        if not isinstance(contract_id, str) or not contract_id:
            return report("derive", False, [diagnostic("INVALID_DERIVATION", "derived contract needs id")])
        selected, error = _expand_selectors(raw.get("source_selectors"), source_order)
        if error:
            return report("derive", False, [diagnostic("INVALID_DERIVATION", error, contract=contract_id)])
        for source_id in selected:
            if source_id not in semantic_ids:
                return report("derive", False, [diagnostic("INVALID_DERIVATION", "guidance-only source cannot be assigned a semantic contract", source=source_id)])
            if source_id in assigned:
                return report("derive", False, [diagnostic("INVALID_DERIVATION", "semantic source is assigned more than once", source=source_id, contracts=[assigned[source_id], contract_id])])
            assigned[source_id] = contract_id
        contract = {key: copy.deepcopy(value) for key, value in raw.items() if key != "source_selectors"}
        contract["source"] = selected
        contracts.append(contract)
    missing = sorted(semantic_ids - set(assigned))
    if missing:
        return report("derive", False, [diagnostic("UNMAPPED_SEMANTIC_SOURCE", "every semantic source needs exactly one derived contract", sources=missing)])
    sealed_components, component_diagnostics = _sealed_components(target_root, derivation.get("components"))
    if component_diagnostics:
        return report("derive", False, component_diagnostics)
    derived_sources: list[dict[str, Any]] = []
    for source in sources:
        derived = copy.deepcopy(source)
        source_id = derived["id"]
        if source_id in assigned:
            derived.pop("guidance_only", None)
            derived["contracts"] = [assigned[source_id]]
        derived_sources.append(derived)
    state = {
        "compilation": copy.deepcopy(seed.get("compilation")),
        "sources": derived_sources,
        "contracts": contracts,
        "mappings": copy.deepcopy(derivation.get("mappings")),
        "components": sealed_components,
        "validation": copy.deepcopy(derivation.get("validation")),
    }
    return report("derive", True, [], state=state, derived_contracts=len(contracts), semantic_sources=len(semantic_ids))
