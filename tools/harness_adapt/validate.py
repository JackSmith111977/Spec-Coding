"""Validate Harness Adapt coverage, provider selection, and candidate traceability."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .shared import diagnostic, report, sha256_file, sha256_json


CLAUSE_DISPOSITIONS = {"covered", "not_applicable", "blocked"}
PROVIDER_SOURCES = {"runtime_native", "project_existing", "installed_extension", "registry", "external", "custom"}
PROVIDER_AVAILABILITY = {"active", "installable", "reachable", "buildable", "unavailable"}
TRUST_SCOPES = {"runtime_official", "project_trusted", "third_party", "unknown"}
AUTHORITY_STATES = {"allowed", "approval_required", "forbidden"}
COMPONENT_MODES = {"reuse", "configure", "create"}


def _schema_errors(schema: dict[str, Any], value: dict[str, Any], label: str) -> list[dict[str, Any]]:
    errors = []
    for error in sorted(Draft202012Validator(schema).iter_errors(value), key=lambda item: list(item.path)):
        errors.append(diagnostic("SCHEMA_ERROR", f"{label}: {error.message}", path=list(error.path)))
    return errors


def validate_adaptation(
    semantic_ir: dict[str, Any],
    environment: dict[str, Any],
    adoption: dict[str, Any],
    plan: dict[str, Any],
    candidate: dict[str, Any],
    plan_schema: dict[str, Any],
    candidate_schema: dict[str, Any],
    target_root: Path | None = None,
) -> dict[str, Any]:
    diagnostics = _schema_errors(plan_schema, plan, "plan")
    diagnostics.extend(_schema_errors(candidate_schema, candidate, "candidate"))

    semantic_fingerprint = sha256_json(semantic_ir)
    environment_fingerprint = sha256_json(environment)
    adoption_fingerprint = sha256_json(adoption)
    for label, value in (("plan", plan), ("candidate", candidate)):
        if value.get("semantic_fingerprint") != semantic_fingerprint:
            diagnostics.append(diagnostic("SEMANTIC_FINGERPRINT_MISMATCH", f"{label} is not bound to the current Semantic IR"))
        if value.get("environment_fingerprint") != environment_fingerprint:
            diagnostics.append(diagnostic("ENVIRONMENT_FINGERPRINT_MISMATCH", f"{label} is not bound to the current Environment Model"))
        if value.get("adoption_fingerprint") != adoption_fingerprint:
            diagnostics.append(diagnostic("ADOPTION_FINGERPRINT_MISMATCH", f"{label} is not bound to the current Adoption Context"))
    if candidate.get("plan_fingerprint") != sha256_json(plan):
        diagnostics.append(diagnostic("PLAN_FINGERPRINT_MISMATCH", "candidate is not bound to the current Adaptation Plan"))

    clause_ids = {item.get("id") for item in semantic_ir.get("clauses", []) if isinstance(item, dict) and isinstance(item.get("id"), str)}
    facts = {item.get("id"): item for item in environment.get("facts", []) if isinstance(item, dict) and isinstance(item.get("id"), str)}
    surfaces = {item.get("id"): item for item in environment.get("provider_surfaces", []) if isinstance(item, dict) and isinstance(item.get("id"), str)}

    accounts = plan.get("clause_accounts", []) if isinstance(plan.get("clause_accounts"), list) else []
    account_ids = [item.get("clause") for item in accounts if isinstance(item, dict)]
    if set(account_ids) != clause_ids or len(account_ids) != len(clause_ids):
        diagnostics.append(diagnostic("CLAUSE_ADAPTATION_COVERAGE_GAP", "every Semantic Clause must have exactly one adaptation disposition"))

    requirements = plan.get("requirements", []) if isinstance(plan.get("requirements"), list) else []
    requirement_by_id = {item.get("id"): item for item in requirements if isinstance(item, dict) and isinstance(item.get("id"), str)}
    if len(requirement_by_id) != len(requirements):
        diagnostics.append(diagnostic("DUPLICATE_REQUIREMENT_ID", "capability requirement ids must be unique"))

    providers = plan.get("providers", []) if isinstance(plan.get("providers"), list) else []
    provider_by_id = {item.get("id"): item for item in providers if isinstance(item, dict) and isinstance(item.get("id"), str)}
    if len(provider_by_id) != len(providers):
        diagnostics.append(diagnostic("DUPLICATE_PROVIDER_ID", "provider ids must be unique"))

    for account in accounts:
        if not isinstance(account, dict):
            continue
        clause = account.get("clause")
        disposition = account.get("disposition")
        if disposition not in CLAUSE_DISPOSITIONS:
            continue
        if disposition == "covered":
            refs = account.get("requirement_ids")
            if not isinstance(refs, list) or not refs:
                diagnostics.append(diagnostic("COVERED_WITHOUT_REQUIREMENT", "covered Clause requires requirement_ids", clause=clause))
            else:
                for ref in refs:
                    requirement = requirement_by_id.get(ref)
                    if requirement is None:
                        diagnostics.append(diagnostic("UNKNOWN_REQUIREMENT", "Clause references unknown capability requirement", clause=clause, requirement=ref))
                    elif clause not in requirement.get("required_by", []):
                        diagnostics.append(diagnostic("REQUIREMENT_TRACE_MISMATCH", "requirement.required_by must include the Clause", clause=clause, requirement=ref))
        elif disposition == "blocked":
            diagnostics.append(diagnostic("BLOCKED_CLAUSE", "blocked Clause prevents Stage 3 handoff", clause=clause, reason=account.get("reason")))
        elif not isinstance(account.get("reason"), str) or not account["reason"].strip():
            diagnostics.append(diagnostic("MISSING_DISPOSITION_REASON", "not_applicable Clause requires a reason", clause=clause))

    selected_provider_ids = set()
    for requirement in requirements:
        if not isinstance(requirement, dict):
            continue
        requirement_id = requirement.get("id")
        for clause in requirement.get("required_by", []):
            if clause not in clause_ids:
                diagnostics.append(diagnostic("UNKNOWN_REQUIRED_BY_CLAUSE", "requirement references unknown Clause", requirement=requirement_id, clause=clause))
        candidate_refs = requirement.get("provider_ids", [])
        selected = requirement.get("selected_provider")
        if selected not in candidate_refs:
            diagnostics.append(diagnostic("SELECTED_PROVIDER_NOT_CANDIDATE", "selected provider must be listed in provider_ids", requirement=requirement_id, provider=selected))
        provider = provider_by_id.get(selected)
        if provider is None:
            diagnostics.append(diagnostic("UNKNOWN_SELECTED_PROVIDER", "selected provider does not exist", requirement=requirement_id, provider=selected))
            continue
        selected_provider_ids.add(selected)
        if requirement_id not in provider.get("satisfies", []):
            diagnostics.append(diagnostic("PROVIDER_SEMANTIC_GAP", "selected provider must explicitly satisfy the requirement", requirement=requirement_id, provider=selected))
        if provider.get("availability") == "unavailable":
            diagnostics.append(diagnostic("UNAVAILABLE_PROVIDER_SELECTED", "cannot select an unavailable provider", requirement=requirement_id, provider=selected))
        authority = provider.get("authority_status")
        if authority == "forbidden":
            diagnostics.append(diagnostic("FORBIDDEN_PROVIDER_SELECTED", "selected provider violates current authority constraints", requirement=requirement_id, provider=selected))
        if authority == "approval_required" and not provider.get("approval_evidence"):
            diagnostics.append(diagnostic("PROVIDER_APPROVAL_REQUIRED", "selected provider needs approval evidence", requirement=requirement_id, provider=selected))
        if not isinstance(requirement.get("selection_reason"), str) or not requirement["selection_reason"].strip():
            diagnostics.append(diagnostic("MISSING_PROVIDER_SELECTION_REASON", "selected provider requires a selection reason", requirement=requirement_id))

    for provider in providers:
        if not isinstance(provider, dict):
            continue
        provider_id = provider.get("id")
        source = provider.get("source")
        if source not in PROVIDER_SOURCES:
            continue
        if provider.get("availability") not in PROVIDER_AVAILABILITY or provider.get("trust") not in TRUST_SCOPES:
            continue
        if not provider.get("evidence"):
            diagnostics.append(diagnostic("PROVIDER_WITHOUT_EVIDENCE", "provider candidate requires current evidence", provider=provider_id))
        for ref in provider.get("fact_refs", []):
            if ref not in facts:
                diagnostics.append(diagnostic("UNKNOWN_FACT_REFERENCE", "provider references unknown Environment fact", provider=provider_id, fact=ref))
        if source == "registry":
            surface_ref = provider.get("surface_ref")
            surface = surfaces.get(surface_ref)
            if surface is None:
                diagnostics.append(diagnostic("REGISTRY_SURFACE_REQUIRED", "registry provider must reference a discovered provider surface", provider=provider_id, surface=surface_ref))
            elif surface.get("status") != "reachable":
                diagnostics.append(diagnostic("REGISTRY_SURFACE_UNREACHABLE", "registry provider surface is not currently reachable", provider=provider_id, surface=surface_ref))

    components = candidate.get("components", []) if isinstance(candidate.get("components"), list) else []
    covered_clauses = {item.get("clause") for item in accounts if isinstance(item, dict) and item.get("disposition") == "covered"}
    candidate_covered = set()
    signatures = set()
    used_providers = set()

    artifacts = candidate.get("artifacts", []) if isinstance(candidate.get("artifacts"), list) else []
    artifact_ids = set()
    artifact_paths = set()
    artifact_by_id = {}
    target = target_root.resolve() if target_root is not None else None
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        artifact_id = artifact.get("id")
        path = artifact.get("path")
        if artifact_id in artifact_ids:
            diagnostics.append(diagnostic("DUPLICATE_ARTIFACT_ID", "artifact ids must be unique", artifact=artifact_id))
        artifact_ids.add(artifact_id)
        if path in artifact_paths:
            diagnostics.append(diagnostic("DUPLICATE_ARTIFACT_PATH", "artifact paths must be unique", path=path))
        artifact_paths.add(path)
        artifact_by_id[artifact_id] = artifact

        loader_fact_ref = artifact.get("loader_fact_ref")
        if loader_fact_ref and loader_fact_ref not in facts:
            diagnostics.append(diagnostic("UNKNOWN_LOADER_FACT", "artifact loader_fact_ref must reference Environment evidence", artifact=artifact_id, fact=loader_fact_ref))

        if target is not None and isinstance(path, str):
            candidate_path = (target / path).resolve()
            try:
                candidate_path.relative_to(target)
            except ValueError:
                diagnostics.append(diagnostic("ARTIFACT_OUTSIDE_TARGET", "artifact path escapes target root", artifact=artifact_id, path=path))
            else:
                if not candidate_path.is_file():
                    diagnostics.append(diagnostic("MISSING_CANDIDATE_ARTIFACT", "candidate artifact does not exist", artifact=artifact_id, path=path))
                elif artifact.get("content_sha256") != sha256_file(candidate_path):
                    diagnostics.append(diagnostic("ARTIFACT_CONTENT_DRIFT", "candidate artifact content does not match content_sha256", artifact=artifact_id, path=path))

    component_ids = [item.get("id") for item in components if isinstance(item, dict)]
    if len(component_ids) != len(set(component_ids)):
        diagnostics.append(diagnostic("DUPLICATE_COMPONENT_ID", "component ids must be unique"))
    for component in components:
        if not isinstance(component, dict):
            continue
        component_id = component.get("id")
        mode = component.get("mode")
        clauses = component.get("covers_clauses", [])
        providers_for_component = component.get("provider_refs", [])
        artifacts_for_component = component.get("artifact_refs", [])
        if mode not in COMPONENT_MODES:
            continue
        if not clauses:
            diagnostics.append(diagnostic("EMPTY_COMPONENT_COVERAGE", "component must cover at least one Clause", component=component_id))
        for clause in clauses:
            if clause not in covered_clauses:
                diagnostics.append(diagnostic("COMPONENT_COVERS_NONCOVERED_CLAUSE", "component may only cover covered Clauses", component=component_id, clause=clause))
            else:
                candidate_covered.add(clause)
        for provider_ref in providers_for_component:
            if provider_ref not in provider_by_id:
                diagnostics.append(diagnostic("UNKNOWN_COMPONENT_PROVIDER", "component references unknown provider", component=component_id, provider=provider_ref))
            else:
                used_providers.add(provider_ref)
        for artifact_ref in artifacts_for_component:
            artifact = artifact_by_id.get(artifact_ref)
            if artifact is None:
                diagnostics.append(diagnostic("UNKNOWN_COMPONENT_ARTIFACT", "component references unknown artifact", component=component_id, artifact=artifact_ref))
            elif artifact.get("component_ref") != component_id:
                diagnostics.append(diagnostic("ARTIFACT_COMPONENT_MISMATCH", "artifact.component_ref must match the owning component", component=component_id, artifact=artifact_ref))
        if mode == "create" and not artifacts_for_component:
            diagnostics.append(diagnostic("CREATE_WITHOUT_ARTIFACT", "create component must materialize at least one artifact", component=component_id))
        signature = (component.get("kind"), mode, tuple(sorted(clauses)), tuple(sorted(providers_for_component)))
        if signature in signatures:
            diagnostics.append(diagnostic("DUPLICATE_COMPONENT", "duplicate component coverage/provider signature violates structural minimality", component=component_id))
        signatures.add(signature)

    missing_candidate_coverage = sorted(covered_clauses - candidate_covered)
    if missing_candidate_coverage:
        diagnostics.append(diagnostic("CANDIDATE_COVERAGE_GAP", "every covered Clause must be implemented by at least one candidate component", clauses=missing_candidate_coverage))
    unused_selected = sorted(selected_provider_ids - used_providers)
    if unused_selected:
        diagnostics.append(diagnostic("SELECTED_PROVIDER_UNUSED", "every selected provider must be used by a candidate component", providers=unused_selected))

    changes = candidate.get("provider_changes", []) if isinstance(candidate.get("provider_changes"), list) else []
    change_by_provider = {item.get("provider_ref"): item for item in changes if isinstance(item, dict) and isinstance(item.get("provider_ref"), str)}
    for provider_id in selected_provider_ids:
        provider = provider_by_id.get(provider_id, {})
        if provider.get("requires_change") is True:
            change = change_by_provider.get(provider_id)
            if change is None:
                diagnostics.append(diagnostic("PROVIDER_CHANGE_REQUIRED", "selected provider requires install/config/connect/build action", provider=provider_id))
            elif change.get("status") != "applied":
                diagnostics.append(diagnostic("PROVIDER_CHANGE_NOT_APPLIED", "provider change must be applied before Stage 3 handoff", provider=provider_id))
            elif not change.get("refresh_evidence"):
                diagnostics.append(diagnostic("PROVIDER_REFRESH_REQUIRED", "applied provider change requires targeted refresh evidence", provider=provider_id))

    return report(
        "harness-adapt-validate",
        not diagnostics,
        diagnostics,
        summary={
            "clauses": len(clause_ids),
            "requirements": len(requirements),
            "providers": len(providers),
            "components": len(components),
            "artifacts": len(artifacts),
        },
    )
