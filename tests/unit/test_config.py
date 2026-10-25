from advanced_rag.config import Settings


def test_settings_use_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.app_name == "Advanced RAG"
    assert settings.environment == "development"
    assert settings.pinecone_api_key is None


def test_settings_accept_overrides() -> None:
    settings = Settings(
        _env_file=None,
        app_name="Test RAG",
        environment="test",
    )

    assert settings.app_name == "Test RAG"
    assert settings.environment == "test"
