from pydantic import BaseModel, field_validator
import yaml
from llama_index.core.prompts import PromptTemplate


class LLMConfig(BaseModel):
    model: str
    temperature: float = 0.1


class EmbeddingConfig(BaseModel):
    model: str
    batch_size: int = 8


class IndexingConfig(BaseModel):
    chunk_size: int = 1000
    response_mode: str = "compact"
    similarity_top_k: int = 3
    text_qa_template: PromptTemplate
    refine_template: PromptTemplate

    @field_validator("text_qa_template", "refine_template", mode="before")
    @classmethod
    def validate_prompt_templates(cls, value):
        if isinstance(value, str):
            return PromptTemplate(value)
        return value


class DataConfig(BaseModel):
    source_dir: str


class StorageConfig(BaseModel):
    persist_dir: str


class AoeRagConfig(BaseModel):
    llm: LLMConfig
    embedding: EmbeddingConfig
    indexing: IndexingConfig
    data: DataConfig
    storage: StorageConfig

    @classmethod
    def from_yaml(cls, file_path: str) -> "AoeRagConfig":
        """Load configuration from YAML file."""
        with open(file_path, "r") as f:
            config_data = yaml.safe_load(f)
        return cls(**config_data)
