from advanced_rag.config import Settings


def test_settings_use_safe_defaults() -> None:
    settings = Settings(database_url="postgresql+psycopg://user:pass@localhost/test")

    assert settings.app_name == "Advanced RAG"
    assert settings.environment == "development"
    assert settings.pinecone_index_name == "advanced-rag"
    assert settings.pinecone_api_key is None
    assert settings.openai_api_key is None
