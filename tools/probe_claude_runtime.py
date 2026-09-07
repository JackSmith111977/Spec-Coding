"""有界运行无文件/工具权限的本机Claude探测，保留真实结果。"""
import json
import subprocess
import sys
import time
from pathlib import Path

root = Path(__file__).resolve().parents[1]
output = root / ".harness-build/runtime-probes"
output.mkdir(parents=True, exist_ok=True)
command = [str(Path.home() / ".local/bin/claude.exe"), "--safe-mode", "--no-session-persistence",
           "--permission-mode", "dontAsk", "--tools", "", "--output-format", "json", "-p",
           "仅回复运行就绪，不读取文件，不调用工具。"]
start = time.monotonic()
try:
    result = subprocess.run(command, cwd=root / ".harness-staging/runtime-probe", capture_output=True, timeout=45)
    record = {"exit_code": result.returncode, "stdout": result.stdout.decode("utf-8", errors="replace"),
              "stderr": result.stderr.decode("utf-8", errors="replace"), "timed_out": False}
except subprocess.TimeoutExpired as error:
    record = {"exit_code": None, "stdout": (error.stdout or b"").decode("utf-8", errors="replace"),
              "stderr": (error.stderr or b"").decode("utf-8", errors="replace"), "timed_out": True}
record.update(command=command, elapsed_seconds=round(time.monotonic() - start, 2),
              limitation="仅可用性探测，不是Harness接入或行为验证")
(output / "claude.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps(record, ensure_ascii=False, indent=2))
