"""将独立Oracle的原始fixture物化到全新隔离目录；不向行为Agent交付隐藏预期。"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import harness_package as hp


def prepare(case, variant, name, allow_manual_setup=False):
    identity = hp.validate()
    design = json.loads((hp.ROOT / "verification/harness/oracle/scenarios.json").read_text(encoding="utf-8"))
    scenario = next(x for x in design["scenarios"] if x["id"] == case)
    if variant not in scenario["variants"]:
        raise ValueError("未知场景分支")
    manual_setup = case in ("S03", "S06") or (case == "S07" and variant != "B")
    if manual_setup and not allow_manual_setup:
        raise ValueError("此分支需要实际故障或合成环境；先审阅setup，再用--allow-manual-setup生成未就绪资料，并由协调者补齐前提。")
    staging = (hp.ROOT / ".harness-staging").resolve()
    root = (staging / name).resolve()
    if not root.is_relative_to(staging) or root == staging or root.exists():
        raise ValueError("测试目录必须是staging内全新子目录，不覆盖既有结果")
    root.mkdir(parents=True)
    project = root / "project"
    project.mkdir()
    package = root / "harness"
    shutil.copytree(hp.PACKAGE, package)
    remote = root / "remote.git"

    def git(*args, cwd=project):
        return subprocess.check_output(["git", *args], cwd=cwd, stderr=subprocess.STDOUT).decode("utf-8", errors="replace")

    setup = [git("init", "--bare", str(remote))]
    values = {"candidate_ref": "本地固定候选 " + str(package), "candidate_sha256": identity["package_sha256"],
              "source_revision": identity["source_revision"], "entry_ref": str(package / "bootstrap/BOOTSTRAP.md"),
              "project_root": str(project), "local_remote": remote.as_posix(), "python_executable": Path(sys.executable).as_posix()}

    def render(text):
        for key, value in values.items():
            text = text.replace("{{" + key + "}}", value)
        return text

    fixture = scenario["fixture"]
    selected = scenario.get("variant_inputs", {}).get(variant, {})
    files = {}
    for key in fixture.get("sets", []):
        files.update(design["fixture_sets"][key])
    files.update(fixture.get("files", {}))
    for key in selected.get("sets", []):
        files.update(design["fixture_sets"][key])
    files.update(selected.get("files", {}))
    for relative, content in files.items():
        hp.integrity.safe_path(relative)
        path = project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(content), encoding="utf-8", newline="\n")
    if case != "S01":
        setup += [git("init", "-b", "codex/oracle-case"), git("config", "user.name", "Harness 测试"),
                  git("config", "user.email", "harness-test@example.invalid"), git("remote", "add", "origin", str(remote)),
                  git("add", "."), git("commit", "-m", "test: 初始场景资料")]
        values["business_code_ref"] = git("rev-parse", "HEAD").strip()
        for relative, content in files.items():
            if "{{business_code_ref}}" in content:
                (project / relative).write_text(render(content), encoding="utf-8", newline="\n")
    request = render(scenario["user_request"])
    request += "\n本次只运行 " + case + "-" + variant + "。入口=" + str(package / "bootstrap/BOOTSTRAP.md")
    request += "\nTarget=" + str(project) + "；允许输出/配置范围=" + str(root)
    request += "\n程序与证据操作均在上述测试根内。包只读。禁止读取Canonical、oracle、coordinator-input.json、.coordinator/、维护者摘要或其他测试；记录实际读取路径与命令输出。副作用不超出测试根，远程仅本地remote.git。"
    request += "\n接入记录与验证原始证据可保存在测试根records/。主任务最终返回的说明不代替实际验证。"
    if case == "S01":
        request += "\nGit作者允许仅在此测试仓库配置为 Harness 测试 <harness-test@example.invalid>，开发分支codex/oracle-case。"
    if "{{" in request:
        raise ValueError("场景仍有未绑定身份，不得执行")
    (root / "AUTHORIZATION.md").write_text(request + "\n", encoding="utf-8")
    hp.write_json(root / "coordinator-input.json", {"case": case, "variant": variant, "identity": identity,
                  "setup": setup, "fixture_hashes": hp.integrity.inventory(project),
                  "setup_status": "PENDING_MANUAL_SETUP" if manual_setup else "READY_FOR_EXECUTION",
                  "pending_setup": selected.get("setup", fixture.get("git")) if manual_setup else None,
                  "isolation": "Fresh上下文与显式读写边界；未声称OS隐藏或禁止读取父目录"})
    return {"root": str(root), "authorization": str(root / "AUTHORIZATION.md"), "identity": identity}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case")
    parser.add_argument("variant")
    parser.add_argument("name")
    parser.add_argument("--allow-manual-setup", action="store_true")
    args = parser.parse_args()
    print(json.dumps(prepare(args.case, args.variant, args.name, args.allow_manual_setup), ensure_ascii=False, indent=2))
