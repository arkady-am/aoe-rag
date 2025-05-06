import unittest
import os
import shutil
from aoe_rag import AoeRag
from aoe_rag_config import AoeRagConfig


class TestAoeRag(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        # Use test configuration
        test_config = AoeRagConfig(
            {
                "llm": {"model": "gpt-3.5-turbo", "temperature": 0.0},
                "storage": {"persist_dir": "test_storage"},
                "data": {"source_dir": "test_data"},
            }
        )
        self.rag = AoeRag(test_config)

        # Ensure test data directory exists
        if not os.path.exists("test_data"):
            os.makedirs("test_data")
            with open("test_data/test_doc.txt", "w") as f:
                f.write("AOE is a technology company.")

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists("test_storage"):
            shutil.rmtree("test_storage")

    def test_initialization(self):
        """Test that the RAG system initializes properly."""
        self.rag.initialize_index(force_rebuild=True)
        self.assertIsNotNone(self.rag._index)

    def test_query(self):
        """Test basic querying capability."""
        response = self.rag.query("Was ist AOE?")
        self.assertIsNotNone(response)
        self.assertIn("technology", str(response).lower())


if __name__ == "__main__":
    unittest.main()
