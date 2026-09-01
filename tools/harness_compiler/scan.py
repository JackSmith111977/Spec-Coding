"""Enumerate deterministic Canonical and Adoption source blocks for Harness Compiler V2."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from .shared import CompilerInputError, diagnostic, read_json, relative_path, report, sha256_text


HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


def _slug(value: str) -> str:
    normalized = re.sub(r"[^\w]+", "-", value.casefold(), flags=re.UNICODE).strip("-_")
    return normalized or "untitled"


def _block(ref: str, path: str, block_kind: str, content: str, line_start: int | None, line_end: int | None, **extra: Any) -> dict[str, Any]:
    return {
        "ref": ref,
        "path": path,
        "kind": "canonical",
        "block_kind": block_kind,
        "line_start": line_start,
        "line_end": line_end,
        "content_sha256": sha256_text(content),
        **extra,
    }


def scan_markdown(path: Path, repository_path: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    headings: list[dict[str, Any]] = []
    for index, line in enumerate(lines):
        match = HEADING.match(line.rstrip("\r\n"))
        if match:
            headings.append({"index": index, "level": len(match.group(1)), "title": match.group(2).strip()})

    blocks: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    if not headings:
        if text.strip():
            blocks.append(_block(f"{repository_path}#preamble@1", repository_path, "preamble", text, 1, len(lines), semantic_required=True))
        return blocks, diagnostics

    first_h1 = next((heading for heading in headings if heading["level"] == 1), None)
    if first_h1 and first_h1["index"] > 0 and "".join(lines[: first_h1["index"]]).strip():
        content = "".join(lines[: first_h1["index"]])
        blocks.append(_block(f"{repository_path}#leading-preamble@1", repository_path, "preamble", content, 1, first_h1["index"], semantic_required=True))

    occurrences: defaultdict[str, int] = defaultdict(int)
    hierarchy: list[str] = []
    preamble_count = 0
    for ordinal, heading in enumerate(headings):
        start = heading["index"]
        end = headings[ordinal + 1]["index"] if ordinal + 1 < len(headings) else len(lines)
        direct_body = "".join(lines[start + 1 : end])
        content = "".join(lines[start:end])
        level = heading["level"]
        if level == 1:
            hierarchy = [_slug(heading["title"])]
            preamble_count += 1
            # The document title is part of the preamble semantic span.  This
            # preserves title-only documents and keeps the span stable up to
            # the next heading.
            blocks.append(
                _block(
                    f"{repository_path}#preamble@{preamble_count}",
                    repository_path,
                    "preamble",
                    content,
                    start + 1,
                    end,
                    heading_path=hierarchy.copy(),
                    semantic_required=bool(direct_body.strip()),
                )
            )
            continue

        if not hierarchy:
            hierarchy = ["document"]
        hierarchy = hierarchy[: level - 1] + [_slug(heading["title"])]
        hierarchy_key = "/".join(hierarchy)
        occurrences[hierarchy_key] += 1
        blocks.append(
            _block(
                f"{repository_path}#heading:{hierarchy_key}@{occurrences[hierarchy_key]}",
                repository_path,
                "section",
                content,
                start + 1,
                end,
                heading=heading["title"],
                heading_level=level,
                heading_path=hierarchy.copy(),
                semantic_required=bool(direct_body.strip()),
            )
        )
    return blocks, diagnostics


def scan(spec_root: Path, candidates_path: Path) -> dict[str, Any]:
    candidates = read_json(candidates_path)
    if not isinstance(candidates, dict) or not isinstance(candidates.get("candidate_sources"), list):
        raise CompilerInputError("candidate inventory must have candidate_sources")
    diagnostics: list[dict[str, Any]] = []
    source_blocks: list[dict[str, Any]] = []
    seen_paths: set[str] = set()
    for entry in candidates["candidate_sources"]:
        if not isinstance(entry, dict):
            diagnostics.append(diagnostic("INVALID_CANDIDATE_SOURCE", "candidate source must be an object"))
            continue
        if entry.get("kind") == "adoption":
            if not isinstance(entry.get("ref"), str) or not isinstance(entry.get("content_sha256"), str):
                diagnostics.append(diagnostic("INVALID_ADOPTION_SOURCE", "adoption candidate is incomplete"))
                continue
            source_blocks.append(
                {
                    "ref": entry["ref"],
                    "path": None,
                    "kind": "adoption",
                    "fact": entry.get("fact"),
                    "line_start": None,
                    "line_end": None,
                    "content_sha256": entry["content_sha256"],
                    "semantic_required": True,
                }
            )
            continue
        path = entry.get("path")
        if entry.get("kind") != "canonical" or not isinstance(path, str):
            diagnostics.append(diagnostic("INVALID_CANDIDATE_SOURCE", "canonical candidate needs a path"))
            continue
        if path in seen_paths:
            continue
        seen_paths.add(path)
        if not path.endswith(".md"):
            diagnostics.append(diagnostic("UNSUPPORTED_SOURCE_TYPE", "only Markdown canonical sources are supported", path=path))
            continue
        try:
            local_path = relative_path(spec_root, path)
            if not local_path.is_file():
                diagnostics.append(diagnostic("MISSING_CANDIDATE_SOURCE", "canonical candidate does not exist", path=path))
                continue
            blocks, scan_diagnostics = scan_markdown(local_path, path)
            source_blocks.extend(blocks)
            diagnostics.extend(scan_diagnostics)
        except (CompilerInputError, OSError, UnicodeDecodeError) as error:
            diagnostics.append(diagnostic("SOURCE_READ_ERROR", str(error), path=path))

    refs = [block["ref"] for block in source_blocks]
    if len(refs) != len(set(refs)):
        diagnostics.append(diagnostic("DUPLICATE_SOURCE_BLOCK_REF", "scanner generated duplicate source refs"))
    return report("scan", not diagnostics, diagnostics, candidate_inventory=str(candidates_path), source_blocks=source_blocks)
