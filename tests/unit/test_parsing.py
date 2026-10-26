
from advanced_rag.ingestion.parsing import normalize_text


def test_normalize_line_endings_and_whitespace() -> None:
    assert normalize_text("  Hello  \r\n World \r\n") == (
        "Hello\nWorld"
    )


def test_preserve_paragraphs() -> None:
    assert normalize_text("Section 1\n\n  Section 2  ") == (
        "Section 1\n\nSection 2"
    )


def test_collapse_repeated_blank_lines() -> None:
    assert normalize_text("First\n\n\n\nSecond") == (
        "First\n\nSecond"
    )


def test_empty_text() -> None:
    assert normalize_text("") == ""
    assert normalize_text("  \n  ") == ""
