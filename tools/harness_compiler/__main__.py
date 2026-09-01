"""Command-line entry point for the non-normative Harness Compiler V2 tools."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .compose import compose
from .resolve import resolve
from .scan import scan
from .shared import CompilerInputError, diagnostic, load_adoption_baseline, read_json, report, write_json
from .state import validate_state
from .verify import verify


def _roots(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--spec-root", type=Path, required=True, help="Spec Coding workspace root")
    parser.add_argument("--target-root", type=Path, required=True, help="Harness target root")
    parser.add_argument("--adoption-baseline", required=True, help="JSON path relative to spec-root")


def _load_context(args: argparse.Namespace) -> tuple[Path, Path, dict[str, Any], str]:
    spec_root = args.spec_root.resolve()
    target_root = args.target_root.resolve()
    baseline, _, baseline_sha256 = load_adoption_baseline(spec_root, args.adoption_baseline)
    return spec_root, target_root, baseline, baseline_sha256


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    resolve_parser = subcommands.add_parser("resolve", help="resolve Canonical and Adoption source candidates")
    _roots(resolve_parser)
    resolve_parser.add_argument("--manifest", default="docs/manifest.yaml")
    resolve_parser.add_argument("--output", type=Path, required=True)
    scan_parser = subcommands.add_parser("scan", help="scan deterministic source blocks")
    scan_parser.add_argument("--spec-root", type=Path, required=True)
    scan_parser.add_argument("--candidates", type=Path, required=True)
    scan_parser.add_argument("--output", type=Path, required=True)
    for name in ("compose", "validate", "verify"):
        command_parser = subcommands.add_parser(name)
        _roots(command_parser)
        command_parser.add_argument("--state", type=Path, required=True)
        # Compose is a writer. It must validate the same sealed state/inventory
        # contract as validate and verify before it is allowed to materialize it.
        command_parser.add_argument("--source-inventory", type=Path, required=True)
        command_parser.add_argument("--output", type=Path, required=True)
        if name == "verify":
            command_parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()
    try:
        if args.command == "resolve":
            result = resolve(args.spec_root.resolve(), args.target_root.resolve(), args.adoption_baseline, args.manifest)
        elif args.command == "scan":
            result = scan(args.spec_root.resolve(), args.candidates)
        else:
            spec_root, target_root, baseline, baseline_sha256 = _load_context(args)
            state = read_json(args.state)
            inventory = read_json(args.source_inventory)
            if args.command == "compose":
                diagnostics, summary = validate_state(state, spec_root, target_root, baseline, baseline_sha256, inventory)
                result = (
                    report("compose", False, diagnostics, summary=summary)
                    if diagnostics
                    else compose(target_root, baseline, state)
                )
            else:
                if args.command == "validate":
                    diagnostics, summary = validate_state(state, spec_root, target_root, baseline, baseline_sha256, inventory)
                    result = report("validate", not diagnostics, diagnostics, summary=summary)
                else:
                    result = verify(spec_root, target_root, baseline, baseline_sha256, state, inventory, args.timeout)
    except CompilerInputError as error:
        result = report(args.command, False, [diagnostic("INPUT_ERROR", str(error))])
    write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
