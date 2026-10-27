import pytest
from pydantic import ValidationError

from advanced_rag.evaluation.schemas import EvaluationExample


def test_accepts_answerable_example() -> None:
    example = EvaluationExample(
        query_id="q1",
        query="What does section 80C cover?",
        category="exact_reference",
        answerable=True,
        relevant_chunk_ids=["chunk-1"],
    )

    assert example.query_id == "q1"
    assert example.relevant_chunk_ids == ["chunk-1"]


def test_accepts_unanswerable_example() -> None:
    example = EvaluationExample(
        query_id="q2",
        query="What is the tax rule on an imaginary deduction?",
        category="unanswerable",
        answerable=False,
    )

    assert example.answerable is False
    assert example.relevant_chunk_ids == []


def test_rejects_blank_query() -> None:
    with pytest.raises(ValidationError):
        EvaluationExample(
            query_id="q1",
            query="   ",
            category="exact_reference",
            answerable=True,
            relevant_chunk_ids=["chunk-1"],
        )


def test_rejects_answerable_example_without_chunk_ids() -> None:
    with pytest.raises(ValidationError):
        EvaluationExample(
            query_id="q1",
            query="A question",
            category="exact_reference",
            answerable=True,
        )


def test_rejects_unanswerable_example_with_chunk_ids() -> None:
    with pytest.raises(ValidationError):
        EvaluationExample(
            query_id="q1",
            query="A question",
            category="unanswerable",
            answerable=False,
            relevant_chunk_ids=["chunk-1"],
        )


def test_rejects_duplicate_chunk_ids() -> None:
    with pytest.raises(ValidationError):
        EvaluationExample(
            query_id="q1",
            query="A question",
            category="exact_reference",
            answerable=True,
            relevant_chunk_ids=["chunk-1", "chunk-1"],
        )
