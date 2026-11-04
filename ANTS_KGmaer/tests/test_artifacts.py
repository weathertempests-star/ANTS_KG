import unittest

from ants_kgmaer.common.artifacts import verify_directory
from ants_kgmaer.common.files import read_json, write_json
from ants_kgmaer.common.files import jsonl
from ants_kgmaer.data.export import export_dataset
from ants_kgmaer.knowledge.repository import KnowledgeRepository
import test_evaluation


class ArtifactTests(unittest.TestCase):
    setUp = test_evaluation.EvaluationTests.setUp

    def test_required_hash_coverage_for_dataset_selection_run(self):
        for directory in (self.dataset, self.selection, self.run):
            self.assertTrue(verify_directory(directory)["verified"])

    def test_modified_preflight_is_detected(self):
        (self.run / "preflight.json").write_text('{}\n')
        with self.assertRaisesRegex(ValueError, "preflight.json"):
            verify_directory(self.run)

    def test_manifest_cannot_silently_omit_generated_file(self):
        path = self.run / "manifest.json"
        manifest = read_json(path)
        del manifest["files"]["usage.json"]
        write_json(path, manifest, replace=True)
        with self.assertRaisesRegex(ValueError, "required artifacts"):
            verify_directory(self.run)

    def test_portable_export_keeps_answers_separate(self):
        output = self.root / "portable"
        manifest = export_dataset(self.dataset, output)
        self.assertEqual(manifest["events"], 6)
        self.assertTrue(verify_directory(output)["verified"])
        rows = list(jsonl(output / "events.jsonl"))
        self.assertEqual(len(rows), 6)
        for row in rows:
            self.assertNotIn("label_binary", row)
            self.assertNotIn("label", row)
        self.assertTrue((output / "annotation_audit.csv").is_file())

    def test_knowledge_markdown_has_one_anchor_per_shared_node(self):
        repository = KnowledgeRepository()
        self.addCleanup(repository.close)
        markdown = repository.engine.markdown()
        self.assertEqual(markdown.count('<a id="node-'), 197)
        self.assertIn("hierarchy edges: 192", markdown)
        self.assertIn("Functional explanation sources", markdown)


if __name__ == "__main__":
    unittest.main()
