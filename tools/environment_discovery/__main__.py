"""CLI for Environment Discovery V3 support tools."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .prepare import prepare
from .shared import EnvironmentInputError, diagnostic, read_json, report, write_json
from .validate import validate_environment


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    prepare_parser = commands.add_parser("prepare", help="prepare per-Clause discovery work without guessing environment semantics")
    prepare_parser.add_argument("--semantic-ir", type=Path, required=True)
    prepare_parser.add_argument("--adoption", type=Path, required=True)
    prepare_parser.add_argument("--output", type=Path, required=True)

    validate_parser = commands.add_parser("validate", help="validate discovery coverage and Environment Model evidence")
    validate_parser.add_argument("--semantic-ir", type=Path, required=True)
    validate_parser.add_argument("--adoption", type=Path, required=True)
    validate_parser.add_argument("--discovery", type=Path, required=True)
    validate_parser.add_argument("--environment", type=Path, required=True)
    validate_parser.add_argument("--output", type=Path, required=True)

    args = parser.parse_args()
    try:
        semantic_ir = read_json(args.semantic_ir)
        adoption = read_json(args.adoption)
        if args.command == "prepare":
            result = prepare(semantic_ir, adoption)
            write_json(args.output, result)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0

        discovery = read_json(args.discovery)
        environment = read_json(args.environment)
        schema_root = Path(__file__).resolve().parent / "schema"
        result = validate_environment(
            semantic_ir,
            adoption,
            discovery,
            environment,
            read_json(schema_root / "discovery-plan.schema.json"),
            read_json(schema_root / "environment-model.schema.json"),
        )
    except EnvironmentInputError as error:
        result = report(args.command, False, [diagnostic("INPUT_ERROR", str(error))])

    write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
