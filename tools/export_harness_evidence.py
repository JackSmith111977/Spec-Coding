"""归档显式选择的隔离试验快照；不把执行者回报自动判为通过。"""
import argparse
import json
import sys
import zipfile
from pathlib import Path

import harness_package as hp


def export(names, output):
    staging = (hp.ROOT / ".harness-staging").resolve()
    output = Path(output).resolve()
    if output.is_relative_to(hp.PACKAGE) or output.is_relative_to(staging):
        raise ValueError("归档必须在冻结包及运行试验目录之外")
    entries = {}
    cases = []
    for name in names:
        hp.integrity.safe_path(name)
        if "/" in name:
            raise ValueError("试验名必须是staging的直接子目录名")
        root = (staging / name).resolve()
        if root == staging or not root.is_relative_to(staging):
            raise ValueError("试验路径越界")
        metadata = json.loads((root / "coordinator-input.json").read_text(encoding="utf-8"))
        # 保留执行者实际消费的包，包括故障对照；不能只留正常发行包来替代坏副本证据。
        snapshot = {}
        for relative, sha256 in hp.integrity.inventory(root).items():
            if any(part in ("__pycache__", ".venv", "node_modules") for part in Path(relative).parts):
                continue
            entries[name + "/" + relative] = root / relative
            snapshot[relative] = sha256
        cases.append({"name": name, "case": metadata["case"], "variant": metadata["variant"],
                      "candidate": metadata["identity"], "files": snapshot,
                      "status": "原始证据快照，不自动判定场景或发行通过"})
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as bundle:
        def add(relative, content):
            entry = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            bundle.writestr(entry, content)
        add("index.json", (json.dumps(cases, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        for relative in sorted(entries):
            data = entries[relative].read_bytes()
            case_name, local = relative.split("/", 1)
            case = next(c for c in cases if c["name"] == case_name)
            if hp.integrity.digest(data) != case["files"][local]:
                raise ValueError("试验仍在变更，停止归档并待执行结束后重试")
            add(relative, data)
    return {"archive": str(output), "archive_sha256": hp.integrity.digest(output.read_bytes()),
            "cases": names, "files": len(entries) + 1}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="+")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    print(json.dumps(export(args.names, args.output), ensure_ascii=False, indent=2))
