"""为S03安装真实Git故障，并先在独立探针仓库证明钩子可执行。"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import harness_package as hp


def prepare(name):
    staging = (hp.ROOT / ".harness-staging").resolve()
    root = (staging / name).resolve()
    if not root.is_relative_to(staging) or root == staging:
        raise ValueError("只允许明确的隔离测试根")
    metadata = json.loads((root / "coordinator-input.json").read_text(encoding="utf-8"))
    if metadata["case"] != "S03" or metadata["setup_status"] != "PENDING_MANUAL_SETUP":
        raise ValueError("仅处理尚未就绪的S03，不覆盖已执行场景")
    control = root / ".coordinator"
    control.mkdir()
    probe = control / "hook-probe"
    probe.mkdir()
    events = []

    def git(cwd, *args, expected=0):
        result = subprocess.run(["git", *args], cwd=cwd, capture_output=True)
        events.append({"cwd": str(cwd), "argv": ["git", *args], "exit_code": result.returncode,
                       "stdout": result.stdout.decode("utf-8", errors="replace"),
                       "stderr": result.stderr.decode("utf-8", errors="replace")})
        hp.write_json(control / "hook-probe.json", events)
        if result.returncode != expected:
            raise ValueError("钩子探针与预期不同，场景仍未就绪")

    def install(project, remote):
        hooks = project / ".git/hooks"
        hooks.mkdir(exist_ok=True)
        (hooks / "pre-commit").write_text(
            '#!/bin/sh\nif test -f "$(git rev-parse --git-dir)/harness-test-block-commit"; then\n'
            '  echo "测试提交设施暂时不可用，请由测试管理员恢复。" >&2\n  exit 1\nfi\n', encoding="utf-8", newline="\n")
        (project / ".git/harness-test-block-commit").write_text("由协调者在真实失败后解除。\n", encoding="utf-8")
        (remote / "hooks/pre-receive").write_text(
            '#!/bin/sh\nif test -f harness-test-block-receive; then\n'
            '  echo "测试远程接收设施暂时不可用，请由测试管理员恢复。" >&2\n  exit 1\nfi\n', encoding="utf-8", newline="\n")
        (remote / "harness-test-block-receive").write_text("由协调者在真实失败后解除。\n", encoding="utf-8")
        for hook in (hooks / "pre-commit", remote / "hooks/pre-receive"):
            hook.chmod(0o755)

    probe_remote = control / "probe-remote.git"
    git(control, "init", "--bare", str(probe_remote))
    git(probe, "init", "-b", "codex/hook-probe")
    git(probe, "config", "user.name", "Harness 测试")
    git(probe, "config", "user.email", "harness-test@example.invalid")
    git(probe, "commit", "--allow-empty", "-m", "test: 探针初始提交")
    install(probe, probe_remote)
    git(probe, "commit", "--allow-empty", "-m", "test: 预期被拒绝", expected=1)
    (probe / ".git/harness-test-block-commit").unlink()
    git(probe, "commit", "--allow-empty", "-m", "test: 提交设施恢复")
    git(probe, "push", str(probe_remote), "HEAD:refs/heads/probe", expected=1)
    (probe_remote / "harness-test-block-receive").unlink()
    git(probe, "push", str(probe_remote), "HEAD:refs/heads/probe")
    install(root / "project", root / "remote.git")
    metadata.update(setup_status="READY_FOR_EXECUTION", pending_setup=None,
                    fault_probe=".coordinator/hook-probe.json",
                    fault_control=["project/.git/harness-test-block-commit", "remote.git/harness-test-block-receive"])
    hp.write_json(root / "coordinator-input.json", metadata)
    print("S03真实提交/接收故障已安装；独立探针拒绝及恢复均已实际验证。")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    prepare(parser.parse_args().name)
