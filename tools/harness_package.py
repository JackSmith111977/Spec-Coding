"""装配、校验并归档已经由Builder直接编写的Harness；不自动编译语义。"""
import argparse
import importlib.util
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import yaml

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages/harness"
spec = importlib.util.spec_from_file_location("package_verify", PACKAGE / "scripts/verify.py")
integrity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(integrity)
SKILLS = {
    "project-definition": "spec-project-definition",
    "project-understanding": "spec-project-understanding",
    "requirement-clarification": "spec-requirement-clarification",
    "technical-design": "spec-technical-design",
    "implementation-planning": "spec-implementation-planning",
    "development-execution": "spec-development-execution",
    "verification-convergence": "spec-verification-convergence",
    "process-review-improvement": "spec-process-improvement",
    "debug-and-defect-resolution": "spec-debug",
    "project-onboarding": "spec-project-onboarding",
    "harness-adoption-and-adaptation": "spec-harness-adoption",
}
RULES = {"global-execution": "global", "human-agent-collaboration": "collaboration",
         "agent-delegation-and-coordination": "delegation", "code-quality": "code-quality",
         "artifact-organization-and-reading": "artifacts"}
CAPABILITIES = ["read-and-route", "identity-and-scope", "authority-and-state", "trace-and-evidence",
                "deterministic-verification", "independent-review", "scoped-execution",
                "git-lifecycle", "observe-and-recover", "artifact-navigation"]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def source_manifest(revision):
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("source_revision必须是完整提交SHA")
    data = yaml.safe_load(git("show", f"{revision}:docs/manifest.yaml"))
    if data["schema_version"] != 5:
        raise ValueError("未知源清单版本，需重新审定FULL范围和映射")
    return data


def canonical(data):
    groups = [("stages", "canonical_document_count"), ("exception_workflows", "canonical_exception_document_count")]
    paths = []
    for group, count in groups:
        values = ["docs/" + p for item in data[group] for p in item["documents"]]
        if len(values) != data[count]:
            raise ValueError(f"规范数量不符：{group}")
        paths.extend(values)
    for group, count in [("rule_documents", "canonical_rule_document_count"), ("meta_protocols", "canonical_meta_protocol_document_count")]:
        values = ["docs/" + item["path"] for item in data[group]]
        if len(values) != data[count]:
            raise ValueError(f"规范数量不符：{group}")
        paths.extend(values)
    if len(set(paths)) != len(paths):
        raise ValueError("规范登记重复")
    return sorted(paths)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def assemble(revision, package=None):
    package = Path(package) if package is not None else PACKAGE
    data = source_manifest(revision)
    sources = canonical(data)
    version = git("show", f"{revision}:VERSION").decode().strip()
    if version != data["spec_coding_version"] or (ROOT / "VERSION").read_text().strip() != version:
        raise ValueError("源提交、清单与工作树版本不同")
    for path in sources + ["docs/manifest.yaml"]:
        current = (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
        if current != git("show", f"{revision}:{path}").replace(b"\r\n", b"\n"):
            raise ValueError(f"工作树规范已偏离固定源，须重新构建：{path}")
    files = {p: h for p, h in integrity.inventory(package).items() if p != "manifest.json"}
    artifacts = []

    def artifact(ident, kind, path, source_paths, applies, dependencies, requires):
        subset = {p: h for p, h in files.items() if p == path or p.startswith(path + "/")}
        if not subset:
            raise ValueError(f"缺资产：{path}")
        artifacts.append({"id": ident, "type": kind, "path": path, "sources": sorted(source_paths),
                          "applies_when": applies, "dependencies": dependencies, "requires": requires,
                          "requirements": "bootstrap/requirements.md", "sha256": integrity.tree_digest(subset)})

    common = ["rule-global", "rule-collaboration", "rule-artifacts"]
    for item in data["rule_documents"]:
        key = RULES[item["id"]]
        deps = [] if key == "artifacts" else (["rule-artifacts"] if key == "global" else
                (["rule-global", "rule-artifacts"] if key == "collaboration" else common))
        artifact("rule-" + key, "rule", f"rules/{key}.md", ["docs/" + item["path"]], item["description"], deps,
                 ["authority-and-state", "trace-and-evidence", "artifact-navigation"] + (["independent-review", "scoped-execution"] if key == "delegation" else []))
    for item in data["stages"] + data["exception_workflows"]:
        key = SKILLS[item["name"]]
        extra = ["rule-code-quality"] if item["name"] in ("development-execution", "verification-convergence") else []
        artifact(key, "agent-skill", "skills/" + key, ["docs/" + p for p in item["documents"]], item["description"],
                 common + extra, ["read-and-route", "authority-and-state", "trace-and-evidence", "artifact-navigation"] +
                 (["deterministic-verification", "git-lifecycle"] if item["name"] == "development-execution" else []))
    for item in data["meta_protocols"]:
        key = SKILLS[item["id"]]
        artifact(key, "agent-skill", "skills/" + key, ["docs/" + item["path"]], item["description"], common,
                 CAPABILITIES if item["id"] == "harness-adoption-and-adaptation" else ["authority-and-state", "trace-and-evidence", "artifact-navigation"])
    meta = ["docs/" + x["path"] for x in data["meta_protocols"]]
    envelope = [("entry", "bootstrap", "bootstrap/BOOTSTRAP.md", meta, common),
                ("routes", "bootstrap", "bootstrap/routes.md", sources, common),
                ("requirements", "requirements", "bootstrap/requirements.md", sources, []),
                ("readme", "documentation", "README.md", meta, []),
                ("plugin", "agent-plugin", "plugin.json", [], []),
                ("integrity", "tool", "scripts/verify.py", [meta[1]], [])]
    for ident, kind, path, src, deps in envelope:
        artifact(ident, kind, path, src, "包消费入口、组合或完整性核验", deps, ["read-and-route", "identity-and-scope"])
    result = {"version": version, "source_revision": revision, "build_mode": "FULL", "entrypoint": "bootstrap/BOOTSTRAP.md",
              "integrity_definition": "README.md", "capability_definitions": "bootstrap/requirements.md",
              "conditional_dependencies": {"delegation-isolation-review-routing": "rule-delegation", "code-changes": "rule-code-quality"},
              "artifacts": artifacts, "files": files}
    write_json(package / "manifest.json", result)
    return validate(package)


def validate(package=PACKAGE):
    package = Path(package).resolve()
    report = integrity.verify(package)
    manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"), object_pairs_hook=integrity.unique_object)
    data = source_manifest(manifest["source_revision"])
    sources = set(canonical(data))
    version = git("show", f"{manifest['source_revision']}:VERSION").decode().strip()
    if version != manifest["version"] or version != data["spec_coding_version"]:
        raise ValueError("源与包版本不一致")
    files = manifest["files"]
    artifacts = manifest["artifacts"]
    ids = [a["id"] for a in artifacts]
    if len(ids) != len(set(ids)):
        raise ValueError("资产ID重复")
    covered_files, covered_sources = set(), set()
    for item in artifacts:
        path = integrity.safe_path(item["path"])
        subset = {p: h for p, h in files.items() if p == path or p.startswith(path + "/")}
        if not subset or covered_files.intersection(subset):
            raise ValueError(f"资产空或重复拥有文件：{path}")
        covered_files.update(subset)
        if integrity.tree_digest(subset) != item["sha256"]:
            raise ValueError(f"资产Hash不符：{path}")
        if not set(item["sources"]) <= sources:
            raise ValueError(f"来源不属于固定规范清单：{path}")
        if len(item["sources"]) != len(set(item["sources"])):
            raise ValueError(f"重复来源：{path}")
        covered_sources.update(item["sources"])
        if not set(item["dependencies"]) <= set(ids) or not set(item["requires"]) <= set(CAPABILITIES):
            raise ValueError(f"未知依赖或能力：{path}")
        if not item["applies_when"] or item["requirements"] not in files:
            raise ValueError(f"适用条件或要求缺失：{path}")
    if covered_files != set(files) or covered_sources != sources:
        raise ValueError("全量资产文件或规范来源未覆盖")
    visiting, done = set(), set()
    by_id = {a["id"]: a for a in artifacts}
    for item in data["stages"] + data["exception_workflows"]:
        primary = by_id.get(SKILLS[item["name"]])
        expected_sources = {"docs/" + p for p in item["documents"]}
        if primary is None or not expected_sources <= set(primary["sources"]):
            raise ValueError(f"流程主体来源缺失：{item['name']}")
    for item in data["rule_documents"] + data["meta_protocols"]:
        ident = "rule-" + RULES[item["id"]] if item["id"] in RULES else SKILLS[item["id"]]
        if ident not in by_id or "docs/" + item["path"] not in by_id[ident]["sources"]:
            raise ValueError(f"规则或元协议主体来源缺失：{ident}")
    for dependency in manifest["conditional_dependencies"].values():
        if dependency not in by_id:
            raise ValueError(f"未知条件依赖：{dependency}")

    def visit(ident):
        if ident in visiting:
            raise ValueError("共享依赖循环")
        if ident in done:
            return
        visiting.add(ident)
        for dependency in by_id[ident]["dependencies"]:
            visit(dependency)
        visiting.remove(ident)
        done.add(ident)
    for ident in ids:
        visit(ident)
    if any(item["id"] == "artifact-organization-and-reading" for item in data["rule_documents"]):
        for item in artifacts:
            if item["type"] == "agent-skill" or item["id"] == "entry":
                if "rule-artifacts" not in item["dependencies"]:
                    raise ValueError(f"消费者缺少产物规则依赖：{item['id']}")
    plugin = json.loads((package / "plugin.json").read_text(encoding="utf-8"))
    if plugin != {"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", "name": "spec-coding", "version": version,
                  "description": "Spec Coding 预编译流程、共享规则与目标侧按需接入程序", "repository": "https://github.com/JackSmith111977/Spec-Coding"}:
        raise ValueError("本次Plugin元数据与声明不符")
    skill_count = 0
    for path in package.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        if path.name == "SKILL.md":
            skill_count += 1
            match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
            if not match:
                raise ValueError(f"缺Skill frontmatter：{path}")
            front = yaml.safe_load(match[1])
            name, description = front.get("name", ""), front.get("description", "")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64 or name != path.parent.name:
                raise ValueError(f"Skill名称非法：{path}")
            if not isinstance(description, str) or not 1 <= len(description) <= 1024:
                raise ValueError(f"Skill描述非法：{path}")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
            if re.match(r"[a-z]+://", target):
                continue
            target = target.split("#", 1)[0]
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(package) or not resolved.is_file():
                raise ValueError(f"引用缺失或逃出包：{path} → {target}")
    if skill_count != 11:
        raise ValueError("首次构建应完整承载11个流程Skill")
    report.update(structure="PASS", canonical_sources=len(sources), artifacts=len(artifacts), skills=skill_count,
                  limitation="仅确定性结构与身份检查，不证明来源映射语义或行为正确")
    return report


def archive(output, package=None):
    package = Path(package).resolve() if package is not None else PACKAGE
    report = validate(package)
    output = Path(output).resolve()
    if output.is_relative_to(package):
        raise ValueError("归档与证据不得放进冻结包")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as bundle:
        for relative in sorted(integrity.inventory(package)):
            entry = zipfile.ZipInfo("harness/" + relative, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            bundle.writestr(entry, (package / relative).read_bytes())
    report.update(archive=output.name, archive_sha256=integrity.digest(output.read_bytes()))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["assemble", "verify", "archive"])
    parser.add_argument("--source-revision")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--package", type=Path, default=PACKAGE, help="待装配、验证或归档的完整包目录")
    args = parser.parse_args()
    if args.action == "assemble":
        if not args.source_revision:
            parser.error("assemble必须显式绑定--source-revision")
        report = assemble(args.source_revision, args.package)
    elif args.action == "archive":
        if not args.output:
            parser.error("archive必须指定--output")
        report = archive(args.output, args.package)
    else:
        report = validate(args.package)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f"BLOCKED：{error}", file=sys.stderr)
        raise SystemExit(1)
