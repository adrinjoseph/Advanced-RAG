
import pytest

from advanced_rag.ingestion.chunking import chunk_text


def test_empty_text_returns_no_chunks() -> None:
    assert chunk_text("") == []
    assert chunk_text("   \n\t") == []


def test_short_text_returns_one_chunk() -> None:
    assert chunk_text("Hello RAG", chunk_size=20, overlap=5) == [
        "Hello RAG"
    ]


def test_exact_size_text_returns_one_chunk() -> None:
    assert chunk_text("ABCDEFGH", chunk_size=8, overlap=3) == [
        "ABCDEFGH"
    ]


def test_long_text_uses_expected_overlap() -> None:
    assert chunk_text("ABCDEFGHIJKLMNO", chunk_size=8, overlap=3) == [
        "ABCDEFGH",
        "FGHIJKLM",
        "KLMNO",
    ]


def test_zero_overlap() -> None:
    assert chunk_text("ABCDEFGH", chunk_size=4, overlap=0) == [
        "ABCD",
        "EFGH",
    ]


def test_invalid_configuration_raises_value_error() -> None:
    with pytest.raises(ValueError):
        chunk_text("hello", chunk_size=0)

    with pytest.raises(ValueError):
        chunk_text("hello", chunk_size=5, overlap=-1)

    with pytest.raises(ValueError):
        chunk_text("hello", chunk_size=5, overlap=5)
