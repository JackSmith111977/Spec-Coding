"""Resolve the complete Spec Coding Canonical Corpus without target/runtime context."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .shared import SemanticCompilerError, diagnostic, git_blob_sha1, read_yaml, relative_path, report, sha256_json, sha256_text


def _canonical_path(canonical_root: str, raw_path: str) -> str:
    root = canonical_root.strip("/")
    path = raw_path.strip("/")
    return path if not root or path.startswith(f"{root}/") else f"{root}/{path}"


def _append(
    documents: list[dict[str, Any]],
    seen: dict[str, str],
    diagnostics: list[dict[str, Any]],
    *,
    path: Any,
    kind: str,
    owner: str,
    canonical_root: str,
) -> None:
    if not isinstance(path, str) or not path.strip():
        diagnostics.append(diagnostic("INVALID_CANONICAL_PATH", "canonical document path must be a non-empty string", owner=owner))
        return
    normalized = _canonical_path(canonical_root, path)
    previous = seen.get(normalized)
    if previous is not None:
        if previous != kind:
            diagnostics.append(
                diagnostic(
                    "CANONICAL_KIND_CONFLICT",
                    "canonical document is registered with conflicting kinds",
                    path=normalized,
                    first_kind=previous,
                    second_kind=kind,
                )
            )
        return
    seen[normalized] = kind
    documents.append({"path": normalized, "kind": kind, "owner": owner})


def resolve_sources(spec_root: Path, manifest_path: str = "docs/manifest.yaml") -> dict[str, Any]:
    spec_root = spec_root.resolve()
    diagnostics: list[dict[str, Any]] = []
    try:
        version = (spec_root / "VERSION").read_text(encoding="utf-8").strip()
        manifest = read_yaml(relative_path(spec_root, manifest_path))
    except (OSError, SemanticCompilerError) as error:
        return report("semantic-resolve", False, [diagnostic("INPUT_ERROR", str(error))])
    if not version:
        diagnostics.append(diagnostic("EMPTY_VERSION", "VERSION is empty"))
    if not isinstance(manifest, dict):
        return report("semantic-resolve", False, [diagnostic("INVALID_MANIFEST", "manifest must be an object")])

    canonical_root = manifest.get("canonical_root")
    if not isinstance(canonical_root, str) or not canonical_root.strip():
        return report("semantic-resolve", False, [diagnostic("INVALID_MANIFEST", "manifest.canonical_root is required")])

    documents: list[dict[str, Any]] = []
    seen: dict[str, str] = {}

    for stage in manifest.get("stages", []):
        if not isinstance(stage, dict):
            diagnostics.append(diagnostic("INVALID_MANIFEST_ENTRY", "stage must be an object"))
            continue
        owner = f"stage:{stage.get('id', 'unknown')}"
        for path in stage.get("documents", []):
            _append(documents, seen, diagnostics, path=path, kind="workflow", owner=owner, canonical_root=canonical_root)

    for rule in manifest.get("rule_documents", []):
        if isinstance(rule, dict):
            _append(
                documents, seen, diagnostics, path=rule.get("path"), kind="rule",
                owner=f"rule:{rule.get('id', 'unknown')}", canonical_root=canonical_root,
            )
        else:
            diagnostics.append(diagnostic("INVALID_MANIFEST_ENTRY", "rule document must be an object"))

    for workflow in manifest.get("exception_workflows", []):
        if not isinstance(workflow, dict):
            diagnostics.append(diagnostic("INVALID_MANIFEST_ENTRY", "exception workflow must be an object"))
            continue
        owner = f"exception:{workflow.get('id', 'unknown')}"
        for path in workflow.get("documents", []):
            _append(documents, seen, diagnostics, path=path, kind="exception", owner=owner, canonical_root=canonical_root)

    for protocol in manifest.get("meta_protocols", []):
        if isinstance(protocol, dict):
            _append(
                documents, seen, diagnostics, path=protocol.get("path"), kind="meta-protocol",
                owner=f"meta-protocol:{protocol.get('id', 'unknown')}", canonical_root=canonical_root,
            )
        else:
            diagnostics.append(diagnostic("INVALID_MANIFEST_ENTRY", "meta protocol must be an object"))

    resolved_documents: list[dict[str, Any]] = []
    for entry in documents:
        try:
            path = relative_path(spec_root, entry["path"])
        except SemanticCompilerError as error:
            diagnostics.append(diagnostic("INVALID_CANONICAL_PATH", str(error), path=entry["path"]))
            continue
        if not path.is_file():
            diagnostics.append(diagnostic("MISSING_CANONICAL_DOCUMENT", "canonical document does not exist", path=entry["path"]))
            continue
        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8")
        except (OSError, UnicodeDecodeError) as error:
            diagnostics.append(diagnostic("CANONICAL_READ_ERROR", str(error), path=entry["path"]))
            continue
        resolved_documents.append({**entry, "sha256": sha256_text(text), "git_blob_sha1": git_blob_sha1(raw)})

    corpus_payload = [{"path": d["path"], "kind": d["kind"], "git_blob_sha1": d["git_blob_sha1"]} for d in resolved_documents]
    source_manifest = {
        "semantic_manifest_version": 1,
        "spec_version": version,
        "canonical_root": canonical_root,
        "document_count": len(resolved_documents),
        "corpus_fingerprint": sha256_json(corpus_payload),
        "documents": resolved_documents,
    }
    return report("semantic-resolve", not diagnostics, diagnostics, source_manifest=source_manifest)
