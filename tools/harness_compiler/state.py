"""Compilation State validation for Harness Compiler V2.

The validator proves structural accounting and evidence presence. It deliberately
does not decide whether natural-language guarantees are semantically correct.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .shared import SUPPORT_MODES, diagnostic, relative_path, runtime_surfaces_for_target


SOURCE_STATUSES = {"RESOLVED", "NOT_APPLICABLE", "UNRESOLVED"}
MAPPING_DECISIONS = {"EXISTING", "COMPILE", "BLOCKED"}
VALIDATION_DIMENSIONS = (
    "source_coverage",
    "contract_coverage",
    "semantic_fidelity",
    "runtime_mapping",
    "capability_routing",
    "component_integrity",
    "minimality",
    "runtime_loading",
    "executability",
    "failure_path",
    "reference_drift",
)
SHA256 = re.compile(r"^[0-9a-f]{64}$")
STATE_SCHEMA_PATH = Path(__file__).parent / "schema" / "compilation-state.schema.json"
STATE_SCHEMA = json.loads(STATE_SCHEMA_PATH.read_text(encoding="utf-8"))
STATE_VALIDATOR = Draft202012Validator(STATE_SCHEMA)


def _string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _list_of_strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(_string(item) for item in value)


def _unknown_fields(diagnostics: list[dict[str, Any]], value: Any, allowed: set[str], label: str) -> bool:
    if not isinstance(value, dict):
        diagnostics.append(diagnostic("INVALID_OBJECT", f"{label} must be an object"))
        return False
    unknown = sorted(set(value) - allowed)
    if unknown:
        diagnostics.append(diagnostic("UNKNOWN_FIELD", f"{label} contains unsupported fields", fields=unknown))
        return False
    return True


def _evidence_check(diagnostics: list[dict[str, Any]], value: Any, name: str) -> bool:
    if not isinstance(value, dict):
        diagnostics.append(diagnostic("MISSING_VALIDATION_EVIDENCE", f"validation.{name} must be an object"))
        return False
    if value.get("status") not in {"pass", "fail"}:
        diagnostics.append(diagnostic("INVALID_VALIDATION_STATUS", f"validation.{name}.status must be pass or fail"))
        return False
    if not _list_of_strings(value.get("evidence")):
        diagnostics.append(diagnostic("MISSING_VALIDATION_EVIDENCE", f"validation.{name} needs evidence"))
        return False
    return value["status"] == "pass"


def _valid_readback_contract(
    diagnostics: list[dict[str, Any]],
    contract: dict[str, Any],
    spec_root: Path,
    canonical_documents: set[str],
) -> bool:
    readback = contract.get("readback_contract")
    contract_id = contract.get("id")
    if not isinstance(readback, dict):
        diagnostics.append(diagnostic("MISSING_READBACK_CONTRACT", "COMPILE contract needs a readback_contract", contract=contract_id))
        return False
    if readback.get("mandatory") is not True:
        diagnostics.append(diagnostic("READBACK_NOT_MANDATORY", "COMPILE contract readback_contract.mandatory must be true", contract=contract_id))
        return False
    try:
        canonical_doc = relative_path(spec_root, readback.get("canonical_doc"))
    except Exception:
        diagnostics.append(diagnostic("INVALID_READBACK_DOCUMENT", "readback_contract.canonical_doc must be a safe relative Canonical document path", contract=contract_id))
        return False
    if not canonical_doc.is_file():
        diagnostics.append(diagnostic("MISSING_READBACK_DOCUMENT", "readback_contract.canonical_doc does not exist", contract=contract_id, canonical_doc=readback.get("canonical_doc")))
        return False
    canonical_raw = readback.get("canonical_doc")
    if canonical_raw not in canonical_documents:
        diagnostics.append(diagnostic("READBACK_DOCUMENT_NOT_CANONICAL", "readback_contract.canonical_doc must be one of the resolved Canonical documents", contract=contract_id, canonical_doc=canonical_raw))
        return False
    return True


def validate_state(
    state: Any,
    spec_root: Path,
    target_root: Path,
    baseline: dict[str, Any],
    baseline_sha256: str,
    source_inventory: Any,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    diagnostics: list[dict[str, Any]] = []
    summary = {"sources": 0, "contracts": 0, "mappings": 0, "components": 0, "unresolved": 0, "blocked": 0}
    schema_errors = sorted(STATE_VALIDATOR.iter_errors(state), key=lambda error: list(error.absolute_path))
    if schema_errors:
        for error in schema_errors:
            location = ".".join(str(part) for part in error.absolute_path) or "$"
            diagnostics.append(diagnostic("STATE_SCHEMA_INVALID", error.message, path=location))
        return diagnostics, summary
    if not _unknown_fields(diagnostics, state, {"compilation", "sources", "contracts", "mappings", "components", "validation"}, "state"):
        return diagnostics, summary

    for field in ("compilation", "sources", "contracts", "mappings", "components", "validation"):
        if field not in state:
            diagnostics.append(diagnostic("MISSING_REQUIRED_FIELD", f"state.{field} is required"))
    compilation = state.get("compilation", {})
    if _unknown_fields(diagnostics, compilation, {"spec_version", "target_id", "adoption_sha256"}, "compilation"):
        if not _string(compilation.get("spec_version")):
            diagnostics.append(diagnostic("MISSING_REQUIRED_FIELD", "compilation.spec_version is required"))
        else:
            try:
                current_version = (spec_root / "VERSION").read_text(encoding="utf-8").strip()
                if compilation["spec_version"] != current_version:
                    diagnostics.append(diagnostic("SPEC_VERSION_MISMATCH", "state spec_version does not match the current Spec Coding VERSION"))
            except OSError as error:
                diagnostics.append(diagnostic("SPEC_VERSION_UNREADABLE", f"cannot read VERSION: {error}"))
        if compilation.get("target_id") != baseline.get("target", {}).get("id"):
            diagnostics.append(diagnostic("TARGET_ID_MISMATCH", "state target_id does not match Adoption Baseline"))
        if compilation.get("adoption_sha256") != baseline_sha256:
            diagnostics.append(diagnostic("ADOPTION_BASELINE_MISMATCH", "state does not bind the current Adoption Baseline"))

    sources = state.get("sources", [])
    contracts = state.get("contracts", [])
    mappings = state.get("mappings", [])
    components = state.get("components", [])
    validation = state.get("validation", {})
    for value, label in ((sources, "sources"), (contracts, "contracts"), (mappings, "mappings"), (components, "components")):
        if not isinstance(value, list):
            diagnostics.append(diagnostic("INVALID_COLLECTION", f"state.{label} must be an array"))
    if not isinstance(validation, dict):
        diagnostics.append(diagnostic("INVALID_COLLECTION", "state.validation must be an object"))
        validation = {}
    if not all(isinstance(value, list) for value in (sources, contracts, mappings, components)):
        return diagnostics, summary
    summary.update(sources=len(sources), contracts=len(contracts), mappings=len(mappings), components=len(components))

    inventory_blocks = source_inventory.get("source_blocks") if isinstance(source_inventory, dict) else None
    if not isinstance(inventory_blocks, list):
        diagnostics.append(diagnostic("INVALID_SOURCE_INVENTORY", "source inventory needs source_blocks"))
        inventory_by_ref: dict[str, dict[str, Any]] = {}
    else:
        inventory_by_ref = {
            block.get("ref"): block
            for block in inventory_blocks
            if isinstance(block, dict) and isinstance(block.get("ref"), str)
        }
        if len(inventory_by_ref) != len(inventory_blocks):
            diagnostics.append(diagnostic("INVALID_SOURCE_INVENTORY", "source inventory contains invalid or duplicate refs"))
    canonical_documents = {
        block["ref"].split("#", 1)[0]
        for block in inventory_blocks or []
        if isinstance(block, dict) and block.get("kind") == "canonical" and isinstance(block.get("ref"), str)
    }

    source_by_id: dict[str, dict[str, Any]] = {}
    source_refs: set[str] = set()
    for index, source in enumerate(sources):
        label = f"sources[{index}]"
        if not _unknown_fields(diagnostics, source, {"id", "kind", "ref", "sha256", "status", "contracts", "guidance_only", "reason"}, label):
            continue
        source_id = source.get("id")
        source_ref = source.get("ref")
        status = source.get("status")
        if not _string(source_id) or not _string(source_ref):
            diagnostics.append(diagnostic("INVALID_SOURCE", "source needs id and ref", source=source_id))
            continue
        if source_id in source_by_id:
            diagnostics.append(diagnostic("DUPLICATE_SOURCE_ID", "source ids must be unique", source=source_id))
        source_by_id[source_id] = source
        if source_ref in source_refs:
            diagnostics.append(diagnostic("DUPLICATE_SOURCE_REF", "each source inventory ref must be accounted exactly once", ref=source_ref))
        source_refs.add(source_ref)
        inventory = inventory_by_ref.get(source_ref)
        if inventory is None:
            diagnostics.append(diagnostic("SOURCE_NOT_IN_INVENTORY", "source ref is absent from inventory", ref=source_ref))
        else:
            if source.get("kind") != inventory.get("kind"):
                diagnostics.append(diagnostic("SOURCE_KIND_MISMATCH", "state source kind differs from inventory", ref=source_ref))
            if source.get("sha256") != inventory.get("content_sha256"):
                diagnostics.append(diagnostic("SOURCE_DRIFT", "state source digest differs from inventory", ref=source_ref))
        if source.get("kind") == "canonical":
            path = source_ref.split("#", 1)[0]
            try:
                if not relative_path(spec_root, path).is_file():
                    diagnostics.append(diagnostic("INVALID_SOURCE_REF", "canonical source file does not exist", ref=source_ref))
            except Exception:
                diagnostics.append(diagnostic("INVALID_SOURCE_REF", "canonical source ref is invalid", ref=source_ref))
        elif source.get("kind") != "adoption":
            diagnostics.append(diagnostic("INVALID_SOURCE_KIND", "source kind must be canonical or adoption", ref=source_ref))
        if status not in SOURCE_STATUSES:
            diagnostics.append(diagnostic("INVALID_SOURCE_STATUS", "source status is invalid", source=source_id))
        linked = source.get("contracts", [])
        if linked is not None and not isinstance(linked, list):
            diagnostics.append(diagnostic("INVALID_SOURCE_CONTRACTS", "source contracts must be an array", source=source_id))
            linked = []
        if status == "RESOLVED" and not linked and source.get("guidance_only") is not True:
            diagnostics.append(diagnostic("RESOLVED_WITHOUT_CONTRACT", "resolved source needs a contract or guidance_only", source=source_id))
        if inventory is not None and inventory.get("semantic_required") is True and source.get("guidance_only") is True:
            diagnostics.append(diagnostic("SEMANTIC_SOURCE_GUIDANCE_ONLY", "semantic_required source must link to an explicit contract", ref=source_ref))
        if status == "NOT_APPLICABLE" and not _string(source.get("reason")):
            diagnostics.append(diagnostic("NOT_APPLICABLE_WITHOUT_REASON", "not-applicable source needs a reason", source=source_id))
        if status == "UNRESOLVED":
            summary["unresolved"] += 1
            diagnostics.append(diagnostic("UNRESOLVED_SOURCE", "unresolved source blocks Harness Ready", source=source_id))

    for ref in sorted(set(inventory_by_ref) - source_refs):
        diagnostics.append(diagnostic("SOURCE_NOT_ACCOUNTED", "inventory source is absent from state", ref=ref))

    contract_by_id: dict[str, dict[str, Any]] = {}
    for index, contract in enumerate(contracts):
        label = f"contracts[{index}]"
        if not _unknown_fields(diagnostics, contract, {"id", "source", "guarantee", "strength", "prohibits", "readback_contract", "obligation_type", "failure_mode"}, label):
            continue
        contract_id = contract.get("id")
        if not _string(contract_id) or not _string(contract.get("guarantee")) or contract.get("strength") not in {"must", "must_not", "should", "guidance"}:
            diagnostics.append(diagnostic("INVALID_CONTRACT", "contract needs id, guarantee, and valid strength", contract=contract_id))
            continue
        if contract_id in contract_by_id:
            diagnostics.append(diagnostic("DUPLICATE_CONTRACT_ID", "contract ids must be unique", contract=contract_id))
        contract_by_id[contract_id] = contract
        source_ids = contract.get("source")
        if not _list_of_strings(source_ids):
            diagnostics.append(diagnostic("INVALID_CONTRACT_SOURCE", "contract needs source ids", contract=contract_id))
            continue
        for source_id in source_ids:
            source = source_by_id.get(source_id)
            if source is None:
                diagnostics.append(diagnostic("UNKNOWN_CONTRACT_SOURCE", "contract source does not exist", contract=contract_id, source=source_id))
            elif source.get("status") != "RESOLVED":
                diagnostics.append(diagnostic("CONTRACT_FROM_UNRESOLVED_SOURCE", "contract must originate from RESOLVED source", contract=contract_id, source=source_id))
            elif contract_id not in (source.get("contracts") or []):
                diagnostics.append(diagnostic("SOURCE_CONTRACT_LINK_MISSING", "source must link back to contract", contract=contract_id, source=source_id))

    for source_id, source in source_by_id.items():
        for contract_id in source.get("contracts") or []:
            contract = contract_by_id.get(contract_id)
            if contract is None or source_id not in contract.get("source", []):
                diagnostics.append(diagnostic("CONTRACT_SOURCE_LINK_MISSING", "source-to-contract link is not bidirectional", source=source_id, contract=contract_id))

    mapping_by_contract: dict[str, dict[str, Any]] = {}
    for index, mapping in enumerate(mappings):
        label = f"mappings[{index}]"
        if not _unknown_fields(diagnostics, mapping, {"contract", "decision", "existing", "primitives", "runtime", "reason"}, label):
            continue
        contract_id = mapping.get("contract")
        decision = mapping.get("decision")
        if contract_id not in contract_by_id:
            diagnostics.append(diagnostic("UNKNOWN_MAPPING_CONTRACT", "mapping contract does not exist", contract=contract_id))
        elif contract_id in mapping_by_contract:
            diagnostics.append(diagnostic("DUPLICATE_MAPPING", "every contract needs exactly one mapping", contract=contract_id))
        else:
            mapping_by_contract[contract_id] = mapping
        if decision not in MAPPING_DECISIONS:
            diagnostics.append(diagnostic("INVALID_MAPPING_DECISION", "mapping decision is invalid", contract=contract_id))
            continue
        if decision == "EXISTING":
            existing = mapping.get("existing")
            if not isinstance(existing, dict) or existing.get("coverage") != "sufficient" or not _list_of_strings(existing.get("mechanisms")) or not _list_of_strings(existing.get("evidence")):
                diagnostics.append(diagnostic("EXISTING_WITHOUT_EVIDENCE", "EXISTING needs sufficient coverage, mechanisms, and evidence", contract=contract_id))
        elif decision == "COMPILE":
            runtime = mapping.get("runtime")
            contract = contract_by_id.get(contract_id)
            if contract is not None:
                _valid_readback_contract(diagnostics, contract, spec_root, canonical_documents)
            if not _list_of_strings(mapping.get("primitives")):
                diagnostics.append(diagnostic("COMPILE_WITHOUT_PRIMITIVE", "COMPILE needs primitives", contract=contract_id))
            if not isinstance(runtime, dict) or runtime.get("support") not in SUPPORT_MODES or not _list_of_strings(runtime.get("surfaces")) or not _list_of_strings(runtime.get("evidence")):
                diagnostics.append(diagnostic("COMPILE_WITHOUT_RUNTIME_EVIDENCE", "COMPILE needs runtime support, surfaces, and evidence", contract=contract_id))
            elif runtime["support"] in {"unknown", "unavailable"}:
                diagnostics.append(diagnostic("BLOCKING_RUNTIME_UNKNOWN", "COMPILE cannot rely on unknown or unavailable runtime support", contract=contract_id, support=runtime["support"]))
        else:
            summary["blocked"] += 1
            if not _string(mapping.get("reason")):
                diagnostics.append(diagnostic("BLOCKED_WITHOUT_REASON", "BLOCKED needs a reason", contract=contract_id))

    for contract_id in contract_by_id:
        if contract_id not in mapping_by_contract:
            diagnostics.append(diagnostic("MISSING_MAPPING", "contract lacks mapping", contract=contract_id))
    if summary["blocked"]:
        diagnostics.append(diagnostic("BLOCKED_MAPPING_PRESENT", "blocked mappings prevent the compiler from deriving Harness Ready", blocked=summary["blocked"]))

    component_ids: set[str] = set()
    compiled_coverage: dict[str, list[str]] = {contract_id: [] for contract_id in contract_by_id}
    component_root = baseline.get("publication", {}).get("component_root", "")
    runtime_profile = baseline.get("runtime")
    for index, component in enumerate(components):
        label = f"components[{index}]"
        if not _unknown_fields(diagnostics, component, {"id", "type", "covers", "reason", "outputs", "verification"}, label):
            continue
        component_id = component.get("id")
        if not _string(component_id) or not _string(component.get("type")) or not _string(component.get("reason")):
            diagnostics.append(diagnostic("INVALID_COMPONENT", "component needs id, type, and reason", component=component_id))
        elif component_id in component_ids:
            diagnostics.append(diagnostic("DUPLICATE_COMPONENT_ID", "component ids must be unique", component=component_id))
        else:
            component_ids.add(component_id)
        covers = component.get("covers")
        if not _list_of_strings(covers):
            diagnostics.append(diagnostic("EMPTY_COMPONENT_COVERAGE", "component needs covered contracts", component=component_id))
            covers = []
        for contract_id in covers:
            mapping = mapping_by_contract.get(contract_id)
            if mapping is None:
                diagnostics.append(diagnostic("UNKNOWN_COMPONENT_CONTRACT", "component covers unknown contract", component=component_id, contract=contract_id))
            elif mapping.get("decision") != "COMPILE":
                diagnostics.append(diagnostic("ORPHAN_COMPONENT", "components may only cover COMPILE contracts", component=component_id, contract=contract_id))
            else:
                compiled_coverage[contract_id].append(component_id)
        outputs = component.get("outputs")
        if not isinstance(outputs, list) or not outputs:
            diagnostics.append(diagnostic("EMPTY_COMPONENT_OUTPUT", "component needs outputs", component=component_id))
        else:
            for output in outputs:
                if not _unknown_fields(diagnostics, output, {"target", "action", "staged", "content_sha256"}, f"{label}.outputs"):
                    continue
                if output.get("action") not in {"create", "modify"} or not _string(output.get("target")) or not _string(output.get("staged")) or not isinstance(output.get("content_sha256"), str) or not SHA256.match(output["content_sha256"]):
                    diagnostics.append(diagnostic("INVALID_COMPONENT_OUTPUT", "output needs target, create/modify action, staged path, and digest", component=component_id))
                    continue
                try:
                    target = relative_path(target_root, output["target"])
                    boundary = relative_path(target_root, component_root)
                    target.relative_to(boundary)
                    relative_path(target_root, output["staged"])
                except Exception:
                    diagnostics.append(diagnostic("PUBLICATION_BOUNDARY_VIOLATION", "component output escapes adoption component_root", component=component_id, target=output.get("target")))
                    continue
                if not runtime_surfaces_for_target(runtime_profile, output["target"]):
                    diagnostics.append(diagnostic("RUNTIME_VISIBILITY_VIOLATION", "component output is outside every declared runtime loader surface", component=component_id, target=output["target"]))

        verification = component.get("verification")
        if not isinstance(verification, dict):
            diagnostics.append(diagnostic("INVALID_COMPONENT_VERIFICATION", "component verification must be an object", component=component_id))
            continue
        verification_covers = verification.get("covers")
        if not _list_of_strings(verification_covers):
            diagnostics.append(diagnostic("MISSING_PROBE_COVERAGE", "component verification needs covered contracts", component=component_id))
            verification_covers = []
        elif set(verification_covers) != set(covers):
            diagnostics.append(diagnostic("COMPONENT_VERIFICATION_GAP", "component verification must declare every component contract and no unrelated contract", component=component_id))
        cannot_cover = verification.get("cannot_cover")
        if not isinstance(cannot_cover, list) or not all(_string(item) for item in cannot_cover):
            diagnostics.append(diagnostic("INVALID_PROBE_LIMITATIONS", "component verification cannot_cover must be a string array", component=component_id))
        probes = verification.get("probes")
        if not isinstance(probes, list) or not probes:
            diagnostics.append(diagnostic("MISSING_COMPONENT_PROBES", "component verification needs probes", component=component_id))
            continue
        probe_ids: set[str] = set()
        probed_contracts: set[str] = set()
        has_runtime_visibility_probe = False
        for probe in probes:
            if not isinstance(probe, dict):
                diagnostics.append(diagnostic("INVALID_COMPONENT_PROBE", "probe must be an object", component=component_id))
                continue
            probe_id = probe.get("id")
            probe_type = probe.get("type")
            if not _string(probe_id) or probe_id in probe_ids:
                diagnostics.append(diagnostic("INVALID_COMPONENT_PROBE", "probe ids must be non-empty and unique", component=component_id, probe=probe_id))
            else:
                probe_ids.add(probe_id)
            probe_covers = probe.get("covers")
            if not _list_of_strings(probe_covers) or not set(probe_covers).issubset(set(verification_covers)):
                diagnostics.append(diagnostic("INVALID_PROBE_COVERAGE", "probe coverage must be a non-empty subset of component verification coverage", component=component_id, probe=probe_id))
            else:
                probed_contracts.update(probe_covers)
            if probe_type == "runtime-visibility":
                has_runtime_visibility_probe = True
                if "command" in probe or "expect" in probe:
                    diagnostics.append(diagnostic("INVALID_RUNTIME_VISIBILITY_PROBE", "runtime-visibility probes use declared loader rules and cannot supply a command", component=component_id, probe=probe_id))
            elif probe_type in {"surface", "semantic"}:
                if not _list_of_strings(probe.get("command")) or probe.get("expect") not in {"pass", "fail"}:
                    diagnostics.append(diagnostic("INVALID_COMPONENT_PROBE", "surface and semantic probes need command and pass/fail expectation", component=component_id, probe=probe_id))
            else:
                diagnostics.append(diagnostic("INVALID_COMPONENT_PROBE", "probe type must be surface, semantic, or runtime-visibility", component=component_id, probe=probe_id))
        if not has_runtime_visibility_probe:
            diagnostics.append(diagnostic("MISSING_RUNTIME_VISIBILITY_PROBE", "every compiled component needs a runtime-visibility probe", component=component_id))
        elif probed_contracts != set(verification_covers):
            diagnostics.append(diagnostic("PROBE_COVERAGE_GAP", "component verification contracts must each be covered by at least one probe", component=component_id, missing=sorted(set(verification_covers) - probed_contracts)))

    for contract_id, mapping in mapping_by_contract.items():
        if mapping.get("decision") == "COMPILE" and not compiled_coverage.get(contract_id):
            diagnostics.append(diagnostic("COMPILE_WITHOUT_COMPONENT", "COMPILE contract lacks component coverage", contract=contract_id))

    if not isinstance(validation.get("unresolved"), int) or validation.get("unresolved") != summary["unresolved"]:
        diagnostics.append(diagnostic("VALIDATION_COUNTER_MISMATCH", "validation.unresolved must equal actual unresolved count"))
    if not isinstance(validation.get("blocked"), int) or validation.get("blocked") != summary["blocked"]:
        diagnostics.append(diagnostic("VALIDATION_COUNTER_MISMATCH", "validation.blocked must equal actual blocked count"))

    dimension_passes: dict[str, bool] = {}
    for dimension in VALIDATION_DIMENSIONS:
        dimension_passes[dimension] = _evidence_check(diagnostics, validation.get(dimension), dimension)
        if not dimension_passes[dimension]:
            diagnostics.append(diagnostic("VALIDATION_DIMENSION_FAILED", "validation dimension has not passed", dimension=dimension))
    semantic = validation.get("semantic_fidelity")
    if isinstance(semantic, dict) and semantic.get("status") == "pass":
        reviewer = semantic.get("reviewer")
        if not isinstance(reviewer, dict) or reviewer.get("independent") is not True or reviewer.get("verdict") != "pass" or not isinstance(reviewer.get("findings"), list):
            diagnostics.append(diagnostic("MISSING_INDEPENDENT_REVIEW", "semantic_fidelity pass needs independent reviewer verdict and findings"))
            dimension_passes["semantic_fidelity"] = False
    return diagnostics, summary
