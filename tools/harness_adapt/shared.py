"""Shared primitives for Harness Adapt V3."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class HarnessAdaptInputError(ValueError):
    """Raised when a Harness Adapt input cannot be interpreted safely."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise HarnessAdaptInputError(f"cannot read {path}: {error}") from error
    except json.JSONDecodeError as error:
        raise HarnessAdaptInputError(f"cannot parse JSON {path}: {error}") from error


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def diagnostic(code: str, message: str, **details: Any) -> dict[str, Any]:
    return {"code": code, "message": message, **{key: value for key, value in details.items() if value is not None}}


def report(tool: str, passed: bool, diagnostics: list[dict[str, Any]], **extra: Any) -> dict[str, Any]:
    return {"tool": tool, "passed": passed, "diagnostic_count": len(diagnostics), "diagnostics": diagnostics, **extra}
