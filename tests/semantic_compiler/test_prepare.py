from __future__ import annotations

import unittest

from tools.semantic_compiler.prepare import prepare_worklist


class SemanticPrepareTests(unittest.TestCase):
    def test_prepare_creates_exactly_one_pending_extraction_and_review_per_document(self) -> None:
        manifest = {
            "spec_version": "1.2.3",
            "corpus_fingerprint": "abc",
            "documents": [
                {"path": "docs/a.md", "kind": "workflow", "sha256": "a" * 64, "git_blob_sha1": "a" * 40},
                {"path": "docs/b.md", "kind": "rule", "sha256": "b" * 64, "git_blob_sha1": "b" * 40},
            ],
        }
        result = prepare_worklist(manifest)
        self.assertTrue(result["passed"], result)
        worklist = result["worklist"]
        self.assertEqual(len(worklist["items"]), 2)
        self.assertEqual([item["document"] for item in worklist["items"]], ["docs/a.md", "docs/b.md"])
        self.assertTrue(all(item["extraction"]["status"] == "pending" for item in worklist["items"]))
        self.assertTrue(all(item["fresh_review"]["status"] == "pending" for item in worklist["items"]))
        self.assertEqual(len(worklist["worklist_fingerprint"]), 64)

    def test_prepare_rejects_duplicate_documents(self) -> None:
        manifest = {
            "spec_version": "1.2.3",
            "corpus_fingerprint": "abc",
            "documents": [
                {"path": "docs/a.md", "kind": "workflow", "sha256": "a" * 64, "git_blob_sha1": "a" * 40},
                {"path": "docs/a.md", "kind": "workflow", "sha256": "a" * 64, "git_blob_sha1": "a" * 40},
            ],
        }
        result = prepare_worklist(manifest)
        self.assertFalse(result["passed"])
        self.assertIn("DUPLICATE_SOURCE_DOCUMENT", {item["code"] for item in result["diagnostics"]})


if __name__ == "__main__":
    unittest.main()
