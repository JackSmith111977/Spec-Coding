"""Dependency-light helpers for the Semantic Compiler frontend."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


class SemanticCompilerError(ValueError):
    """Raised when Semantic Compiler input cannot be safely interpreted."""


def diagnostic(code: str, message: str, **details: Any) -> dict[str, Any]:
    return {"code": code, "message": message, **{k: v for k, v in details.items() if v is not None}}


def report(tool: str, passed: bool, diagnostics: list[dict[str, Any]], **extra: Any) -> dict[str, Any]:
    return {"tool": tool, "passed": passed, "diagnostic_count": len(diagnostics), "diagnostics": diagnostics, **extra}


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_text(canonical_json(value))


def git_blob_sha1(value: bytes) -> str:
    header = f"blob {len(value)}\0".encode("utf-8")
    return hashlib.sha1(header + value).hexdigest()


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise SemanticCompilerError(f"cannot read {path}: {error}") from error
    except json.JSONDecodeError as error:
        raise SemanticCompilerError(f"cannot parse JSON {path}: {error}") from error


def read_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise SemanticCompilerError(f"cannot read {path}: {error}") from error
    except yaml.YAMLError as error:
        raise SemanticCompilerError(f"cannot parse YAML {path}: {error}") from error


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def relative_path(root: Path, raw_path: str) -> Path:
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise SemanticCompilerError("path must be a non-empty relative string")
    candidate = Path(raw_path)
    if candidate.is_absolute():
        raise SemanticCompilerError(f"path must be relative: {raw_path}")
    resolved_root = root.resolve()
    resolved = (resolved_root / candidate).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as error:
        raise SemanticCompilerError(f"path escapes root: {raw_path}") from error
    return resolved
