"""Validate Semantic IR structure, source binding, relations, and release completeness."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any

from .shared import diagnostic, report, sha256_json

CLAUSE_KINDS = {"invariant", "trigger", "gate", "transition", "authority", "artifact", "routing"}
RELATION_TYPES = {"requires", "before", "triggers", "blocks", "specializes", "isolated_from"}
SCOPE_MODES = {"pilot", "release"}


def _string_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value)


def _cycle_nodes(edges: dict[str, set[str]], nodes: set[str]) -> list[str]:
    indegree = {node: 0 for node in nodes}
    for source, targets in edges.items():
        if source not in indegree:
            continue
        for target in targets:
            if target in indegree:
                indegree[target] += 1
    queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    visited = 0
    while queue:
        node = queue.popleft()
        visited += 1
        for target in edges.get(node, set()):
            if target not in indegree:
                continue
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    return sorted(node for node, degree in indegree.items() if degree > 0) if visited != len(nodes) else []


def validate_ir(source_manifest: Any, ir: Any, review_receipt: Any = None) -> dict[str, Any]:
    diagnostics: list[dict[str, Any]] = []
    if not isinstance(source_manifest, dict):
        return report("semantic-validate", False, [diagnostic("INVALID_SOURCE_MANIFEST", "source manifest must be an object")])
    if not isinstance(ir, dict):
        return report("semantic-validate", False, [diagnostic("INVALID_SEMANTIC_IR", "semantic IR must be an object")])

    if ir.get("ir_version") != 1:
        diagnostics.append(diagnostic("INVALID_IR_VERSION", "ir_version must be 1"))
    if ir.get("spec_version") != source_manifest.get("spec_version"):
        diagnostics.append(
            diagnostic(
                "SPEC_VERSION_MISMATCH",
                "Semantic IR spec_version must match source manifest",
                ir_version=ir.get("spec_version"),
                source_version=source_manifest.get("spec_version"),
            )
        )

    source_documents = {
        item.get("path"): item
        for item in source_manifest.get("documents", [])
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    scope = ir.get("scope")
    if not isinstance(scope, dict) or scope.get("mode") not in SCOPE_MODES or not _string_list(scope.get("documents")):
        diagnostics.append(diagnostic("INVALID_SCOPE", "scope requires mode=pilot|release and a non-empty documents array"))
        scope_documents: set[str] = set()
        scope_mode = None
    else:
        scope_documents = set(scope["documents"])
        scope_mode = scope["mode"]
        unknown_scope = sorted(scope_documents - set(source_documents))
        if unknown_scope:
            diagnostics.append(diagnostic("UNKNOWN_SCOPE_DOCUMENT", "scope references documents outside Canonical Corpus", documents=unknown_scope))
        if scope_mode == "release" and scope_documents != set(source_documents):
            diagnostics.append(
                diagnostic(
                    "INCOMPLETE_RELEASE_SCOPE",
                    "release scope must include the entire Canonical Corpus",
                    missing=sorted(set(source_documents) - scope_documents),
                    extra=sorted(scope_documents - set(source_documents)),
                )
            )
        scope_payload = [
            {
                "path": source_documents[path]["path"],
                "kind": source_documents[path]["kind"],
                "git_blob_sha1": source_documents[path].get("git_blob_sha1"),
            }
            for path in sorted(scope_documents)
            if path in source_documents
        ]
        expected_fingerprint = sha256_json(scope_payload)
        if ir.get("source_fingerprint") != expected_fingerprint:
            diagnostics.append(
                diagnostic(
                    "SOURCE_DRIFT",
                    "Semantic IR source_fingerprint does not match the current compiled scope",
                    expected=expected_fingerprint,
                    actual=ir.get("source_fingerprint"),
                )
            )

    clauses = ir.get("clauses")
    if not isinstance(clauses, list) or not clauses:
        diagnostics.append(diagnostic("INVALID_CLAUSES", "clauses must be a non-empty array"))
        clauses = []

    clause_ids: list[str] = []
    relations: list[tuple[str, str, str]] = []
    before_edges: dict[str, set[str]] = defaultdict(set)

    for index, clause in enumerate(clauses):
        if not isinstance(clause, dict):
            diagnostics.append(diagnostic("INVALID_CLAUSE", "clause must be an object", index=index))
            continue
        clause_id = clause.get("id")
        if not isinstance(clause_id, str) or not clause_id.strip():
            diagnostics.append(diagnostic("INVALID_CLAUSE_ID", "clause id must be a non-empty string", index=index))
            continue
        clause_ids.append(clause_id)
        if clause.get("kind") not in CLAUSE_KINDS:
            diagnostics.append(diagnostic("INVALID_CLAUSE_KIND", "unsupported clause kind", clause=clause_id, kind=clause.get("kind")))
        if not any(_string_list(clause.get(field)) and clause.get(field) for field in ("when", "must", "must_not")):
            diagnostics.append(diagnostic("EMPTY_CLAUSE_SEMANTICS", "clause must define at least one non-empty when/must/must_not list", clause=clause_id))

        sources = clause.get("source")
        if not isinstance(sources, list) or not sources:
            diagnostics.append(diagnostic("MISSING_CLAUSE_SOURCE", "clause must have at least one source binding", clause=clause_id))
        else:
            for source in sources:
                if not isinstance(source, dict) or not isinstance(source.get("document"), str) or not isinstance(source.get("anchor"), str):
                    diagnostics.append(diagnostic("INVALID_CLAUSE_SOURCE", "source requires document and anchor", clause=clause_id))
                    continue
                document = source["document"]
                if document not in source_documents:
                    diagnostics.append(diagnostic("UNKNOWN_CLAUSE_SOURCE", "clause source is not Canonical", clause=clause_id, document=document))
                elif scope_documents and document not in scope_documents:
                    diagnostics.append(diagnostic("SOURCE_OUTSIDE_SCOPE", "clause source is outside compiled scope", clause=clause_id, document=document))

        raw_relations = clause.get("relations", [])
        if not isinstance(raw_relations, list):
            diagnostics.append(diagnostic("INVALID_RELATIONS", "relations must be an array", clause=clause_id))
        else:
            for relation in raw_relations:
                if (
                    not isinstance(relation, dict)
                    or relation.get("type") not in RELATION_TYPES
                    or not isinstance(relation.get("target"), str)
                    or not relation["target"].strip()
                ):
                    diagnostics.append(diagnostic("INVALID_RELATION", "relation requires supported type and non-empty target", clause=clause_id))
                    continue
                target = relation["target"]
                relation_type = relation["type"]
                if target == clause_id:
                    diagnostics.append(diagnostic("SELF_RELATION", "clause cannot relate to itself", clause=clause_id, relation=relation_type))
                relations.append((clause_id, relation_type, target))
                if relation_type == "before":
                    before_edges[clause_id].add(target)

    duplicate_ids = sorted({item for item in clause_ids if clause_ids.count(item) > 1})
    if duplicate_ids:
        diagnostics.append(diagnostic("DUPLICATE_CLAUSE_ID", "clause ids must be unique", clauses=duplicate_ids))
    known_ids = set(clause_ids)
    dangling = sorted({target for _, _, target in relations if target not in known_ids})
    if dangling:
        diagnostics.append(diagnostic("DANGLING_RELATION", "relation target does not exist", targets=dangling))
    if not dangling:
        cycle = _cycle_nodes(before_edges, known_ids)
        if cycle:
            diagnostics.append(diagnostic("HARD_ORDER_CYCLE", "before relations contain a cycle", clauses=cycle))

    if scope_mode == "release":
        if not isinstance(review_receipt, dict):
            diagnostics.append(diagnostic("RELEASE_REVIEW_REQUIRED", "release IR requires an external review receipt"))
        else:
            if review_receipt.get("receipt_version") != 1:
                diagnostics.append(diagnostic("INVALID_REVIEW_RECEIPT", "review receipt version must be 1"))
            if review_receipt.get("source_fingerprint") != ir.get("source_fingerprint"):
                diagnostics.append(diagnostic("REVIEW_SCOPE_MISMATCH", "review receipt must bind the same source fingerprint as the IR"))
            reviewer = review_receipt.get("reviewer")
            if not isinstance(reviewer, dict) or reviewer.get("independent") is not True:
                diagnostics.append(diagnostic("INDEPENDENT_REVIEW_REQUIRED", "release review receipt must declare an independent reviewer"))
            document_reviews = review_receipt.get("documents")
            if not isinstance(document_reviews, list):
                diagnostics.append(diagnostic("DOCUMENT_REVIEWS_REQUIRED", "release review requires per-document review records"))
            else:
                reviewed = {
                    item.get("document")
                    for item in document_reviews
                    if isinstance(item, dict) and item.get("verdict") == "pass"
                }
                missing_reviews = sorted(scope_documents - reviewed)
                if missing_reviews:
                    diagnostics.append(diagnostic("DOCUMENT_REVIEW_GAP", "every release document requires a passing review", documents=missing_reviews))
            if review_receipt.get("global_verdict") != "pass":
                diagnostics.append(diagnostic("GLOBAL_REVIEW_REQUIRED", "release review requires global_verdict=pass"))
            mutations = review_receipt.get("mutations")
            if not isinstance(mutations, dict) or mutations.get("status") != "passed":
                diagnostics.append(diagnostic("MUTATION_REVIEW_REQUIRED", "release review requires passing semantic mutation review"))

    return report(
        "semantic-validate",
        not diagnostics,
        diagnostics,
        summary={
            "scope_mode": scope_mode,
            "scope_documents": len(scope_documents),
            "clauses": len(clauses),
            "relations": len(relations),
        },
    )
