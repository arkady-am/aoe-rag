import os
from typing import Optional, Dict, Any

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter

from aoe_rag_config import AoeRagConfig


class AoeRag:
    """AOE RAG application for document querying using LlamaIndex."""

    DEFAULT_CONFIG_PATH = "config.yaml"

    def __init__(
        self,
        config: Optional[AoeRagConfig] = None,
        config_path: str = DEFAULT_CONFIG_PATH,
    ):
        """Initialize the RAG application with configuration.

        Args:
            config: Configuration object. If provided, config_path is ignored.
            config_path: Path to YAML config file. Used only if config is None.
        """
        # Load or use provided configuration
        self.config = (
            config if config is not None else AoeRagConfig.from_yaml(config_path)
        )
        self._setup_settings()
        self._index = None

    def _setup_settings(self) -> None:
        """Configure LlamaIndex settings based on configuration."""
        Settings.llm = OpenAI(
            model=self.config.llm.model,
            temperature=self.config.llm.temperature,
        )

        Settings.embed_model = OpenAIEmbedding(
            model=self.config.embedding.model,
            embed_batch_size=self.config.embedding.batch_size,
        )

        Settings.text_splitter = SentenceSplitter(
            chunk_size=self.config.indexing.chunk_size
        )

    def initialize_index(self, force_rebuild: bool = False) -> None:
        """Initialize or load the vector index."""
        persist_dir = self.config.storage.persist_dir

        if force_rebuild or not os.path.exists(persist_dir):
            self._create_index()
        else:
            self._load_index()

    def _create_index(self) -> None:
        """Create a new vector index from documents."""
        source_dir = self.config.data.source_dir
        persist_dir = self.config.storage.persist_dir
        chunk_size = self.config.indexing.chunk_size

        print(f"💥 Creating new index from {source_dir}")
        documents = SimpleDirectoryReader(source_dir).load_data()
        self._index = VectorStoreIndex.from_documents(documents, chunk_size=chunk_size)
        self._index.storage_context.persist(persist_dir=persist_dir)

    def _load_index(self) -> None:
        """Load an existing vector index from storage."""
        persist_dir = self.config.storage.persist_dir
        print(f"📦 Loading existing index from {persist_dir}")
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        self._index = load_index_from_storage(storage_context)

    def query(self, query_text: str) -> str:
        """Query the index and return the response."""
        query_engine = self._index.as_query_engine(
            response_mode=self.config.indexing.response_mode,
            similarity_top_k=self.config.indexing.similarity_top_k,
        )
        response = query_engine.query(query_text)
        return str(response)
