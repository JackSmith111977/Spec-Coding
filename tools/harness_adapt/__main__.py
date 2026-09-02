"""CLI for Harness Adapt V3 deterministic support tools."""

from __future__ import annotations

import argparse
from pathlib import Path

from .prepare import prepare
from .shared import read_json, write_json
from .validate import validate_adaptation


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m tools.harness_adapt")
    sub = parser.add_subparsers(dest="command", required=True)
    prepare_cmd = sub.add_parser("prepare")
    prepare_cmd.add_argument("--semantic-ir", type=Path, required=True)
    prepare_cmd.add_argument("--environment", type=Path, required=True)
    prepare_cmd.add_argument("--adoption", type=Path, required=True)
    prepare_cmd.add_argument("--output", type=Path, required=True)
    validate_cmd = sub.add_parser("validate")
    validate_cmd.add_argument("--semantic-ir", type=Path, required=True)
    validate_cmd.add_argument("--environment", type=Path, required=True)
    validate_cmd.add_argument("--adoption", type=Path, required=True)
    validate_cmd.add_argument("--plan", type=Path, required=True)
    validate_cmd.add_argument("--candidate", type=Path, required=True)
    validate_cmd.add_argument("--target-root", type=Path, required=True)
    validate_cmd.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.command == "prepare":
        result = prepare(read_json(args.semantic_ir), read_json(args.environment), read_json(args.adoption))
        write_json(args.output, result)
        return 0
    schema_root = Path(__file__).with_name("schema")
    result = validate_adaptation(read_json(args.semantic_ir), read_json(args.environment), read_json(args.adoption), read_json(args.plan), read_json(args.candidate), read_json(schema_root / "adaptation-plan.schema.json"), read_json(schema_root / "harness-candidate.schema.json"), args.target_root)
    write_json(args.output, result)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
