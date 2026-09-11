"""规划修复版本的增量范围，将已准备的完整候选冻结为Patch构建；不判断语义或发布。"""
import argparse
import copy
import json
import re
import shutil
import sys
from pathlib import Path

import harness_package as hp


def read_manifest(package):
    return json.loads((Path(package) / "manifest.json").read_text(encoding="utf-8"),
                      object_pairs_hook=hp.integrity.unique_object)


def version_parts(value):
    if not re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", value):
        raise ValueError("Patch仅接受正式三段版本号")
    return tuple(map(int, value.split(".")))


def plan(baseline, baseline_sha256, revision, defects=()):
    report = hp.validate(baseline)
    if report["package_sha256"] != baseline_sha256:
        raise ValueError("基线包Hash与外部固定值不符")
    old = read_manifest(baseline)
    before = hp.source_manifest(old["source_revision"])
    after = hp.source_manifest(revision)
    version = hp.git("show", f"{revision}:VERSION").decode().strip()
    a, b = version_parts(old["version"]), version_parts(version)
    if b != (a[0], a[1], a[2] + 1) or after["spec_coding_version"] != version:
        raise ValueError("目标必须为基线的下一Patch版本，且与源清单一致")
    old_shape, new_shape = copy.deepcopy(before), copy.deepcopy(after)
    for value in (old_shape, new_shape):
        value.pop("spec_coding_version", None)
        value.pop("status", None)
    if old_shape != new_shape:
        raise ValueError("清单结构或适用关系变化：退出Patch快捷路径，按完整范围治理处理")
    changed = sorted(set(hp.git("diff", "--name-only", "--no-renames", "-z",
                                old["source_revision"], revision, "--", *hp.canonical(after))
                         .decode("utf-8").rstrip("\0").split("\0")) - {""})
    by_id = {x["id"]: x for x in old["artifacts"]}
    if not set(defects) <= by_id.keys():
        raise ValueError("缺陷声明包含未知资产")
    affected = set(defects) | {x["id"] for x in by_id.values() if set(x["sources"]) & set(changed)}
    if not affected:
        raise ValueError("没有规范变化或显式缺陷，不构建空Patch")
    direct = sorted(affected)
    # 条件依赖未标注具体消费者时保守覆盖全部Skill及入口，不按猜测收窄。
    conditional = set(old["conditional_dependencies"].values())
    while True:
        expanded = affected | {x["id"] for x in by_id.values() if set(x["dependencies"]) & affected}
        if conditional & affected:
            expanded |= {x["id"] for x in by_id.values() if x["type"] == "agent-skill" or x["id"] == "entry"}
        if expanded == affected:
            break
        affected = expanded
    envelope = sorted(x["id"] for x in by_id.values() if x["type"] not in ("agent-skill", "rule"))
    rebuild = affected | set(envelope)
    return {"mode": "INCREMENTAL", "release_kind": "PATCH", "version": version,
            "baseline": {"version": old["version"], "source_revision": old["source_revision"],
                         "package_sha256": baseline_sha256},
            "source_revision": revision, "changed_sources": changed, "declared_defects": sorted(set(defects)),
            "direct_artifacts": direct, "affected_artifacts": sorted(affected),
            "refresh_envelope": envelope, "rebuild_artifacts": sorted(rebuild),
            "reusable_artifacts": sorted(by_id.keys() - rebuild),
            "package_integration_required": any(by_id[i]["type"] not in ("agent-skill", "documentation", "agent-plugin")
                                                for i in affected),
            "limitation": "仅确定性范围；基线是否正式可信、Patch语义资格、来源回查及验证证据由维护者审定"}


def build(baseline, baseline_sha256, revision, candidate, output, defects=()):
    scope = plan(baseline, baseline_sha256, revision, defects)
    candidate, baseline, output = map(lambda p: Path(p).resolve(), (candidate, baseline, output))
    if output.exists() or any(output.is_relative_to(p) or p.is_relative_to(output) for p in (candidate, baseline)):
        raise ValueError("输出必须为全新且不包含或嵌套于输入的目录")
    hp.validate(candidate)
    old, new = read_manifest(baseline), read_manifest(candidate)
    if new["source_revision"] != revision or new["version"] != scope["version"]:
        raise ValueError("候选身份与本轮范围不符")
    for field in ("entrypoint", "integrity_definition", "capability_definitions"):
        if new[field] != old[field]:
            raise ValueError(f"包级消费契约变化，退出Patch快捷路径：{field}")
    old_assets = {a["id"]: a for a in old["artifacts"]}
    new_assets = {a["id"]: a for a in new["artifacts"]}
    if old_assets.keys() != new_assets.keys() or new["conditional_dependencies"] != old["conditional_dependencies"]:
        raise ValueError("资产集合或条件路由变化：不能使用Patch快捷路径")
    for ident in old_assets:
        # 不接受借声明缺陷改变组合契约；这种变化交给常规构建审定。
        left, right = dict(old_assets[ident]), dict(new_assets[ident])
        left.pop("sha256"); right.pop("sha256")
        if left != right:
            raise ValueError(f"资产映射或契约变化：{ident}")
    for ident in scope["reusable_artifacts"]:
        if old_assets[ident]["sha256"] != new_assets[ident]["sha256"]:
            raise ValueError(f"范围外资产变化，须补缺陷声明或重新审定范围：{ident}")
    for ident in scope["refresh_envelope"]:
        if (old_assets[ident]["sha256"] != new_assets[ident]["sha256"]
                and old_assets[ident]["type"] not in ("documentation", "agent-plugin")
                and ident not in scope["affected_artifacts"]):
            raise ValueError(f"运行入口或核验工具变化必须进入受影响范围：{ident}")
    # 只复制已核验的普通包文件，不执行候选内程序；使用维护者校验实现。
    hp.integrity.inventory(candidate)
    shutil.copytree(candidate, output)
    new["build_mode"] = "INCREMENTAL"
    new["patch_baseline"] = scope["baseline"]
    new["affected_artifacts"] = scope["affected_artifacts"]
    hp.write_json(output / "manifest.json", new)
    result = hp.validate(output)
    return {"scope": scope, "candidate": result, "verdict": "待独立语义及行为验证；非发行PASS"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("plan", "build"))
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--baseline-sha256", required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--defect", action="append", default=[], help="Canonical未变的缺陷资产ID，可重复")
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.action == "build":
        if not args.candidate or not args.output:
            parser.error("build必须指定--candidate及--output")
        result = build(args.baseline, args.baseline_sha256, args.source_revision,
                       args.candidate, args.output, args.defect)
    else:
        result = plan(args.baseline, args.baseline_sha256, args.source_revision, args.defect)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, hp.subprocess.CalledProcessError) as error:
        print(f"BLOCKED：{error}", file=sys.stderr)
        raise SystemExit(1)
