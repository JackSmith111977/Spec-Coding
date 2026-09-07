"""只校验包完整性，不将Hash当作来源或语义通过证明。"""
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(root):
    root = Path(root).resolve()
    result = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
            raise ValueError(f"包内不允许链接或连接点：{path}")
        if not path.resolve().is_relative_to(root):
            raise ValueError(f"路径越界：{path}")
        if path.is_file():
            result[path.relative_to(root).as_posix()] = digest(path.read_bytes())
    return result


def tree_digest(files):
    return digest("".join(f"{files[p]}  {p}\n" for p in sorted(files)).encode("utf-8"))


def safe_path(value):
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ValueError(f"非法包内路径：{value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in (".", "..", "") for part in value.split("/")):
        raise ValueError(f"非法包内路径：{value!r}")
    return value


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"重复JSON键：{key}")
        result[key] = value
    return result


def verify(root):
    root = Path(root).resolve()
    actual = inventory(root)
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    expected = manifest["files"]
    for path, value in expected.items():
        safe_path(path)
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ValueError(f"非法SHA-256：{path}")
    payload = {p: h for p, h in actual.items() if p != "manifest.json"}
    if payload != expected:
        differences = sorted(p for p in payload.keys() | expected.keys() if payload.get(p) != expected.get(p))
        raise ValueError("文件清单或Hash不符：" + ", ".join(differences))
    if safe_path(manifest["entrypoint"]) not in payload:
        raise ValueError("缺少入口")
    return {"version": manifest["version"], "source_revision": manifest["source_revision"],
            "files": len(actual), "package_sha256": tree_digest(actual), "integrity": "PASS"}


if __name__ == "__main__":
    try:
        print(json.dumps(verify(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]), ensure_ascii=False))
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f"BLOCKED：{error}", file=sys.stderr)
        raise SystemExit(1)
