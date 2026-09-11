"""在临时真实Git仓库中验证Patch命令链，不模拟源提交或Git Diff。"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import harness_package as hp


class PatchCliTests(unittest.TestCase):
    def test_real_source_to_complete_archive(self):
        with tempfile.TemporaryDirectory(prefix="patch-cli-") as directory:
            root = Path(directory)
            repo = root / "repo"
            baseline = root / "baseline"
            prepared = root / "prepared"
            frozen = root / "frozen"
            old = hp.validate(hp.PACKAGE)
            bundle = root / "source.bundle"
            packed = subprocess.run(["git", "-C", str(hp.ROOT), "bundle", "create", str(bundle),
                                     "HEAD"], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(packed.returncode, 0, packed.stderr)
            cloned = subprocess.run(["git", "clone", "--quiet", "--no-checkout",
                                     str(bundle), str(repo)], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(cloned.returncode, 0, cloned.stderr)
            subprocess.run(["git", "-C", str(repo), "checkout", "--quiet", "--detach",
                            old["source_revision"]], check=True, capture_output=True)
            shutil.copytree(hp.PACKAGE, baseline)
            shutil.copytree(hp.PACKAGE, prepared)
            # 测试当前维护工具，基线正文与历史保持独立。
            shutil.copytree(hp.ROOT / "tools", repo / "tools", dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__"))
            numbers = list(map(int, old["version"].split(".")))
            numbers[2] += 1
            version = ".".join(map(str, numbers))
            (repo / "VERSION").write_text(version + "\n", encoding="utf-8")
            manifest = repo / "docs/manifest.yaml"
            manifest.write_text(manifest.read_text(encoding="utf-8").replace(
                f'spec_coding_version: "{old["version"]}"', f'spec_coding_version: "{version}"'), encoding="utf-8")
            changed = "docs/rules/agent-delegation-and-coordination.md"
            marker = "\n<!-- 隔离测试：无行为变化的文档注释 -->\n"
            with (repo / changed).open("a", encoding="utf-8") as stream:
                stream.write(marker)
            subprocess.run(["git", "-C", str(repo), "add", "--", "VERSION", "docs/manifest.yaml", changed],
                           check=True, capture_output=True)
            subprocess.run(["git", "-C", str(repo), "-c", "user.name=Patch Test", "-c",
                            "user.email=patch-test@example.invalid", "-c", "commit.gpgSign=false",
                            "-c", f"core.hooksPath={root / 'no-hooks'}", "commit", "--quiet", "-m", "隔离Patch测试源"],
                           check=True, capture_output=True)
            revision = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()

            def cli(tool, *args):
                result = subprocess.run([sys.executable, "-B", "-X", "utf8", str(repo / "tools" / tool), *map(str, args)],
                                        cwd=repo, capture_output=True, text=True, encoding="utf-8", timeout=90)
                self.assertEqual(result.returncode, 0, result.stderr)
                return json.loads(result.stdout)

            common = ("--baseline", baseline, "--baseline-sha256", old["package_sha256"], "--source-revision", revision)
            scope = cli("harness_patch.py", "plan", *common)
            self.assertIn(changed, scope["changed_sources"])
            self.assertIn("rule-delegation", scope["direct_artifacts"])
            self.assertTrue(scope["package_integration_required"])
            plugin = json.loads((prepared / "plugin.json").read_text(encoding="utf-8"))
            plugin["version"] = version
            hp.write_json(prepared / "plugin.json", plugin)
            with (prepared / "rules/delegation.md").open("a", encoding="utf-8") as stream:
                stream.write(marker)
            cli("harness_package.py", "assemble", "--package", prepared, "--source-revision", revision)
            built = cli("harness_patch.py", "build", *common, "--candidate", prepared, "--output", frozen)
            self.assertEqual(built["candidate"]["source_revision"], revision)
            self.assertEqual(built["candidate"]["files"], old["files"])
            first = cli("harness_package.py", "archive", "--package", frozen, "--output", root / "one.zip")
            second = cli("harness_package.py", "archive", "--package", frozen, "--output", root / "two.zip")
            self.assertEqual(first["archive_sha256"], second["archive_sha256"])
            self.assertEqual(hp.validate(baseline)["package_sha256"], old["package_sha256"])


if __name__ == "__main__":
    unittest.main()
