"""用真实候选副本验证完整性失败、源映射和归档边界。"""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import harness_package as hp


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="harness-test-")
        self.root = Path(self.temp.name) / "harness"
        shutil.copytree(hp.PACKAGE, self.root)

    def tearDown(self):
        self.temp.cleanup()

    def manifest(self, change):
        path = self.root / "manifest.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        change(value)
        hp.write_json(path, value)

    def test_candidate_and_supporting_file_tamper(self):
        hp.validate(self.root)
        reference = self.root / "skills/spec-harness-adoption/references/candidate-validation.md"
        reference.write_text("被截断的支持资源", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Hash"):
            hp.integrity.verify(self.root)

    def test_missing_and_extra_files(self):
        path = self.root / "rules/global.md"
        saved = path.read_bytes()
        path.unlink()
        with self.assertRaises(ValueError):
            hp.integrity.verify(self.root)
        path.write_bytes(saved)
        (self.root / "unexpected.txt").write_text("意外文件", encoding="utf-8")
        with self.assertRaises(ValueError):
            hp.integrity.verify(self.root)

    def test_manifest_identity_is_in_package_hash(self):
        before = hp.integrity.verify(self.root)["package_sha256"]
        path = self.root / "manifest.json"
        path.write_bytes(path.read_bytes() + b"\n")
        self.assertNotEqual(before, hp.integrity.verify(self.root)["package_sha256"])

    def test_source_mapping_rejects_noncanonical(self):
        self.manifest(lambda m: m["artifacts"][0]["sources"].append("docs/README.md"))
        with self.assertRaisesRegex(ValueError, "来源"):
            hp.validate(self.root)

    def test_dependency_cycle(self):
        self.manifest(lambda m: m["artifacts"][0]["dependencies"].append(m["artifacts"][0]["id"]))
        with self.assertRaisesRegex(ValueError, "循环"):
            hp.validate(self.root)

    def test_envelope_cannot_mask_missing_procedure_source(self):
        self.manifest(lambda m: next(a for a in m["artifacts"] if a["id"] == "spec-debug")["sources"].clear())
        with self.assertRaisesRegex(ValueError, "主体来源缺失"):
            hp.validate(self.root)

    def test_path_traversal_and_duplicate_json_keys(self):
        for path in ("../outside", "/absolute", "C:/outside", "a\\b", "a/./b"):
            with self.assertRaises(ValueError):
                hp.integrity.safe_path(path)
        path = self.root / "manifest.json"
        path.write_text('{"files": {}, "files": {}}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "重复"):
            hp.integrity.verify(self.root)

    def test_archive_is_reproducible_and_cannot_enter_package(self):
        first = hp.archive(Path(self.temp.name) / "first.zip")
        second = hp.archive(Path(self.temp.name) / "second.zip")
        self.assertEqual(first["archive_sha256"], second["archive_sha256"])
        with self.assertRaises(ValueError):
            hp.archive(hp.PACKAGE / "invalid.zip")


if __name__ == "__main__":
    unittest.main()
