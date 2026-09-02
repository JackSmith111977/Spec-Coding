from __future__ import annotations

import argparse
import json
from pathlib import Path

from .prepare import prepare
from .shared import HarnessAcceptanceInputError, read_json, write_json
from .validate import validate_acceptance


def _schema(name: str) -> dict:
    path = Path(__file__).parent / "schema" / name
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Harness Verify & Accept V3 deterministic support")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare")
    for name in ("semantic-ir", "environment", "adoption", "plan", "candidate", "output"):
        prepare_parser.add_argument(f"--{name}", required=True)

    validate_parser = subparsers.add_parser("validate")
    for name in ("semantic-ir", "environment", "adoption", "plan", "candidate", "verification-plan", "verification-report", "acceptance-receipt", "target-root", "output"):
        validate_parser.add_argument(f"--{name}", required=True)

    args = parser.parse_args()
    try:
        if args.command == "prepare":
            result = prepare(read_json(Path(args.semantic_ir)), read_json(Path(args.environment)), read_json(Path(args.adoption)), read_json(Path(args.plan)), read_json(Path(args.candidate)))
        else:
            result = validate_acceptance(
                read_json(Path(args.semantic_ir)),
                read_json(Path(args.environment)),
                read_json(Path(args.adoption)),
                read_json(Path(args.plan)),
                read_json(Path(args.candidate)),
                read_json(Path(args.verification_plan)),
                read_json(Path(args.verification_report)),
                read_json(Path(args.acceptance_receipt)),
                _schema("verification-plan.schema.json"),
                _schema("verification-report.schema.json"),
                _schema("acceptance-receipt.schema.json"),
                Path(args.target_root),
            )
        write_json(Path(args.output), result)
        return 0 if result.get("passed", True) else 1
    except (HarnessAcceptanceInputError, OSError, json.JSONDecodeError) as error:
        write_json(Path(args.output), {"tool": "harness-acceptance", "passed": False, "diagnostics": [{"code": "INPUT_ERROR", "message": str(error)}]})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
