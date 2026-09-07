"""检查证据归档保留故障副本，并拒绝归档期间变化的证据。"""
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import export_harness_evidence as exporter


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="harness-evidence-")
        self.root = Path(self.temp.name)
        self.case = self.root / ".harness-staging/故障案例"
        (self.case / "harness/rules").mkdir(parents=True)
        self.evidence = self.case / "harness/rules/global.md"
        self.evidence.write_bytes("缺失语义的故障对照\r\n".encode("utf-8"))
        (self.case / "coordinator-input.json").write_text(json.dumps({
            "case": "负控", "variant": "本地转换", "identity": {"fixture": True}
        }), encoding="utf-8")
        self.output = self.root / "证据.zip"

    def tearDown(self):
        self.temp.cleanup()

    def test_preserves_consumed_faulty_package_and_hash(self):
        with patch.object(exporter.hp, "ROOT", self.root):
            result = exporter.export(["故障案例"], self.output)
        with zipfile.ZipFile(self.output) as bundle:
            raw = bundle.read("故障案例/harness/rules/global.md")
            index = json.loads(bundle.read("index.json"))
        self.assertEqual(raw, self.evidence.read_bytes())
        self.assertEqual(index[0]["files"]["harness/rules/global.md"], exporter.hp.integrity.digest(raw))
        self.assertEqual(result["archive_sha256"], exporter.hp.integrity.digest(self.output.read_bytes()))

    def test_refuses_evidence_changed_after_inventory(self):
        inventory = exporter.hp.integrity.inventory

        def changed(root):
            result = inventory(root)
            self.evidence.write_text("归档时证据仍在变化", encoding="utf-8")
            return result

        with patch.object(exporter.hp, "ROOT", self.root), patch.object(exporter.hp.integrity, "inventory", changed):
            with self.assertRaisesRegex(ValueError, "仍在变更"):
                exporter.export(["故障案例"], self.output)


if __name__ == "__main__":
    unittest.main()
