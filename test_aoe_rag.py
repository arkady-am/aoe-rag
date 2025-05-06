import pytest
import os
import shutil

from aoe_rag import AoeRag
from aoe_rag_config import AoeRagConfig

TEST_CONFIG_YAML = "test_config.yaml"
TEST_DATA = "test_data"
TEST_TXT = os.path.join(TEST_DATA, "test_doc.txt")
TEST_TXT_CONTENT = "AOE is a technology company."
TEST_STORAGE = "test_storage"


@pytest.fixture
def rag():
    """Setup the RAG system for testing."""
    # Use test configuration
    rag = AoeRag(config_path=TEST_CONFIG_YAML)

    # Ensure test data directory exists
    if not os.path.exists(TEST_DATA):
        os.makedirs(TEST_DATA)
        with open(TEST_TXT, "w") as f:
            f.write(TEST_TXT_CONTENT)

    yield rag

    # Cleanup after tests
    if os.path.exists(TEST_DATA):
        shutil.rmtree(TEST_DATA)
    if os.path.exists(TEST_STORAGE):
        shutil.rmtree(TEST_STORAGE)


def test_initialization(rag):
    """Test that the RAG system initializes properly."""
    rag.initialize_index(force_rebuild=True)
    assert rag._index is not None


def test_query(rag):
    """Test basic querying capability."""
    rag.initialize_index(force_rebuild=True)
    response = rag.query("Was ist AOE?")
    assert response is not None
    assert "technologie" in str(response).lower()


def test_load_existing_index(rag):
    """Test loading an existing index."""
    # First create an index
    rag.initialize_index(force_rebuild=True)
    # Then try to load it
    rag._index = None
    rag.initialize_index(force_rebuild=False)
    assert rag._index is not None


def test_config_loading():
    """Test loading configuration from file."""
    config = AoeRagConfig.from_yaml("test_config.yaml")
    rag = AoeRag(config)
    assert rag.config is not None
    assert rag.config == config


def test_force_rebuild(rag):
    """Test force rebuilding the index."""
    # Initial build
    rag.initialize_index(force_rebuild=True)

    # Add new test data to see if rebuild picks it up
    with open("test_data/new_doc.txt", "w") as f:
        f.write("AOE specializes in digital transformation.")

    # Force rebuild with new data
    rag.initialize_index(force_rebuild=True)

    # Query for the new content
    response = rag.query("What does AOE specialize in?")
    assert "transformation" in str(response).lower()


def test_response_format(rag):
    """Test that the response is properly formatted."""
    rag.initialize_index(force_rebuild=True)
    response = rag.query("What is AOE?")
    assert isinstance(response, str)
    assert len(response) > 0


def test_query_with_no_index(rag):
    """Test that querying without an initialized index raises an exception."""
    # Ensure index is None
    rag._index = None

    # Query should raise an exception
    with pytest.raises(ValueError, match="Index not initialized"):
        rag.query("What is AOE?")


def test_multiple_queries(rag):
    """Test multiple queries in sequence."""
    rag.initialize_index(force_rebuild=True)

    query1 = "What is AOE?"
    response1 = rag.query(query1)
    assert response1 is not None

    query2 = "What services does AOE offer?"
    response2 = rag.query(query2)
    assert response2 is not None

    # Responses should be different for different queries
    assert response1 != response2


if __name__ == "__main__":
    pytest.main()
