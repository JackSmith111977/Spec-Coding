"""CLI for the Spec Coding Semantic Compiler frontend."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .prepare import prepare_worklist
from .resolve import resolve_sources
from .shared import SemanticCompilerError, diagnostic, read_json, report, write_json
from .validate import validate_ir


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)

    resolve_parser = subcommands.add_parser("resolve", help="resolve the full Canonical Corpus")
    resolve_parser.add_argument("--spec-root", type=Path, required=True)
    resolve_parser.add_argument("--manifest", default="docs/manifest.yaml")
    resolve_parser.add_argument("--output", type=Path, required=True)

    prepare_parser = subcommands.add_parser("prepare", help="create one extraction/review work item per Canonical document")
    prepare_parser.add_argument("--source-manifest", type=Path, required=True)
    prepare_parser.add_argument("--output", type=Path, required=True)

    validate_parser = subcommands.add_parser("validate", help="validate an Agent-authored Semantic IR")
    validate_parser.add_argument("--source-manifest", type=Path, required=True)
    validate_parser.add_argument("--ir", type=Path, required=True)
    validate_parser.add_argument("--review-receipt", type=Path)
    validate_parser.add_argument("--output", type=Path, required=True)

    args = parser.parse_args()
    try:
        if args.command == "resolve":
            result = resolve_sources(args.spec_root, args.manifest)
            output = result.get("source_manifest", result)
        elif args.command == "prepare":
            result = prepare_worklist(read_json(args.source_manifest))
            output = result.get("worklist", result)
        else:
            source_manifest = read_json(args.source_manifest)
            ir = read_json(args.ir)
            review_receipt = read_json(args.review_receipt) if args.review_receipt else None
            result = validate_ir(source_manifest, ir, review_receipt)
            output = result
    except SemanticCompilerError as error:
        result = report(f"semantic-{args.command}", False, [diagnostic("INPUT_ERROR", str(error))])
        output = result

    write_json(args.output, output)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
