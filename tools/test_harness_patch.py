"""用真实完整包副本与隔离源读取验证Patch范围、身份及输出。"""
import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import harness_package as hp
import harness_patch as pp


class PatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="harness-patch-")
        self.root = Path(self.temp.name)
        self.baseline = self.root / "base"
        self.candidate = self.root / "candidate"
        shutil.copytree(hp.PACKAGE, self.baseline)
        shutil.copytree(hp.PACKAGE, self.candidate)
        self.old = pp.read_manifest(self.baseline)
        self.pin = hp.validate(self.baseline)["package_sha256"]
        self.rev = "f" * 40
        self.version = ".".join(map(str, (*pp.version_parts(self.old["version"])[:2],
                                        pp.version_parts(self.old["version"])[2] + 1)))
        self.data = copy.deepcopy(hp.source_manifest(self.old["source_revision"]))
        self.data["spec_coding_version"] = self.version
        self.changed = set()
        original_git = hp.git

        def fake_git(*args):
            if args[0] == "diff" and self.rev in args:
                return "\0".join(sorted(self.changed)).encode()
            if len(args) == 2 and args[0] == "show" and args[1].startswith(self.rev + ":"):
                name = args[1].split(":", 1)[1]
                if name == "VERSION":
                    return self.version.encode()
                if name == "docs/manifest.yaml":
                    return hp.yaml.safe_dump(self.data).encode()
                value = original_git("show", self.old["source_revision"] + ":" + name)
                return value + ("\n修复\n".encode() if name in self.changed else b"")
            return original_git(*args)
        self.mock = patch.object(hp, "git", side_effect=fake_git)
        self.mock.start()
        plugin = json.loads((self.candidate / "plugin.json").read_text(encoding="utf-8"))
        plugin["version"] = self.version
        hp.write_json(self.candidate / "plugin.json", plugin)
        self.refresh()

    def tearDown(self):
        self.mock.stop()
        self.temp.cleanup()

    def refresh(self):
        data = pp.read_manifest(self.candidate)
        data.update(version=self.version, source_revision=self.rev)
        files = hp.integrity.inventory(self.candidate)
        files.pop("manifest.json")
        data["files"] = files
        for a in data["artifacts"]:
            a["sha256"] = hp.integrity.tree_digest({p: h for p, h in files.items()
                                                    if p == a["path"] or p.startswith(a["path"] + "/")})
        hp.write_json(self.candidate / "manifest.json", data)

    def test_pin_version_and_empty_scope_rejected(self):
        with self.assertRaisesRegex(ValueError, "Hash"):
            pp.plan(self.baseline, "0" * 64, self.rev, ["rule-delegation"])
        with self.assertRaisesRegex(ValueError, "空Patch"):
            pp.plan(self.baseline, self.pin, self.rev)
        self.version = "9.0.0"
        with self.assertRaisesRegex(ValueError, "下一Patch"):
            pp.plan(self.baseline, self.pin, self.rev, ["rule-delegation"])

    def test_conditional_rule_propagates_to_all_skills(self):
        self.changed.add("docs/rules/agent-delegation-and-coordination.md")
        result = pp.plan(self.baseline, self.pin, self.rev)
        skills = {a["id"] for a in self.old["artifacts"] if a["type"] == "agent-skill"}
        self.assertTrue(skills <= set(result["affected_artifacts"]))
        self.assertTrue(result["package_integration_required"])

    def test_manifest_applicability_change_rejected(self):
        self.data["rule_documents"][0]["applies_to"] = "changed"
        with self.assertRaisesRegex(ValueError, "清单结构"):
            pp.plan(self.baseline, self.pin, self.rev, ["entry"])

    def test_out_of_scope_change_rejected_before_output(self):
        p = self.candidate / "rules/code-quality.md"
        p.write_bytes(p.read_bytes() + "\n变更\n".encode())
        self.refresh()
        out = self.root / "output"
        with self.assertRaisesRegex(ValueError, "范围外"):
            pp.build(self.baseline, self.pin, self.rev, self.candidate, out, ["readme"])
        self.assertFalse(out.exists())

    def test_complete_patch_and_reproducible_archive(self):
        out = self.root / "output"
        result = pp.build(self.baseline, self.pin, self.rev, self.candidate, out, ["readme"])
        self.assertEqual(pp.read_manifest(out)["build_mode"], "INCREMENTAL")
        self.assertEqual(result["candidate"]["files"], len(hp.integrity.inventory(self.baseline)))
        self.assertEqual(hp.archive(self.root / "one.zip", out)["archive_sha256"],
                         hp.archive(self.root / "two.zip", out)["archive_sha256"])
        self.assertEqual(hp.validate(self.baseline)["package_sha256"], self.pin)
        with self.assertRaisesRegex(ValueError, "全新"):
            pp.build(self.baseline, self.pin, self.rev, self.candidate, out, ["readme"])

    def test_envelope_refresh_cannot_hide_runtime_change(self):
        p = self.candidate / "bootstrap/requirements.md"
        p.write_bytes(p.read_bytes() + "\n改变运行要求\n".encode())
        self.refresh()
        with self.assertRaisesRegex(ValueError, "运行入口"):
            pp.build(self.baseline, self.pin, self.rev, self.candidate, self.root / "out", ["readme"])

    def test_manifest_entry_change_rejected_before_output(self):
        data = pp.read_manifest(self.candidate)
        data["entrypoint"] = "README.md"
        hp.write_json(self.candidate / "manifest.json", data)
        out = self.root / "out"
        with self.assertRaisesRegex(ValueError, "消费契约"):
            pp.build(self.baseline, self.pin, self.rev, self.candidate, out, ["readme"])
        self.assertFalse(out.exists())

    def test_nested_output_and_wrong_candidate_identity(self):
        with self.assertRaisesRegex(ValueError, "全新"):
            pp.build(self.baseline, self.pin, self.rev, self.candidate, self.baseline / "out", ["readme"])
        with self.assertRaisesRegex(ValueError, "候选身份"):
            pp.build(self.baseline, self.pin, self.rev, self.baseline, self.root / "out", ["readme"])

    def test_assemble_explicit_package_preserves_baseline(self):
        source = self.root / "source"
        source.mkdir()
        revision = self.old["source_revision"]
        data = hp.source_manifest(revision)
        for name in hp.canonical(data) + ["docs/manifest.yaml", "VERSION"]:
            target = source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(hp.git("show", f"{revision}:{name}"))
        prepared = self.root / "prepared"
        shutil.copytree(self.baseline, prepared)
        repository = hp.ROOT
        def fixed_git(*args):
            return hp.subprocess.check_output(["git", *args], cwd=repository)
        with patch.object(hp, "ROOT", source), patch.object(hp, "git", side_effect=fixed_git):
            report = hp.assemble(revision, prepared)
        self.assertEqual(report["source_revision"], revision)
        self.assertEqual(hp.validate(self.baseline)["package_sha256"], self.pin)


if __name__ == "__main__":
    unittest.main()
