"""Build a deterministic per-document Semantic Compilation worklist."""

from __future__ import annotations

from typing import Any

from .shared import diagnostic, report, sha256_json


def prepare_worklist(source_manifest: Any) -> dict[str, Any]:
    if not isinstance(source_manifest, dict):
        return report("semantic-prepare", False, [diagnostic("INVALID_SOURCE_MANIFEST", "source manifest must be an object")])
    documents = source_manifest.get("documents")
    if not isinstance(documents, list) or not documents:
        return report("semantic-prepare", False, [diagnostic("INVALID_SOURCE_MANIFEST", "source manifest requires documents")])

    diagnostics: list[dict[str, Any]] = []
    work_items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, document in enumerate(documents, start=1):
        if not isinstance(document, dict) or not isinstance(document.get("path"), str):
            diagnostics.append(diagnostic("INVALID_SOURCE_DOCUMENT", "source document is incomplete", index=index))
            continue
        path = document["path"]
        if path in seen:
            diagnostics.append(diagnostic("DUPLICATE_SOURCE_DOCUMENT", "source document appears more than once", path=path))
            continue
        seen.add(path)
        work_items.append(
            {
                "id": f"SEM-{index:03d}",
                "document": path,
                "kind": document.get("kind"),
                "source_sha256": document.get("sha256"),
                "git_blob_sha1": document.get("git_blob_sha1"),
                "extraction": {"status": "pending"},
                "fresh_review": {"status": "pending"},
            }
        )

    worklist = {
        "worklist_version": 1,
        "spec_version": source_manifest.get("spec_version"),
        "corpus_fingerprint": source_manifest.get("corpus_fingerprint"),
        "worklist_fingerprint": sha256_json(
            [{"document": item["document"], "source_sha256": item["source_sha256"]} for item in work_items]
        ),
        "items": work_items,
    }
    return report("semantic-prepare", not diagnostics, diagnostics, worklist=worklist)
