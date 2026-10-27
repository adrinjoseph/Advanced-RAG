import json
from pathlib import Path

from pydantic import ValidationError

from advanced_rag.evaluation.schemas import EvaluationExample


class EvaluationDatasetError(ValueError):
    """Raised when an evaluation dataset is invalid."""


def load_dataset(path: str | Path) -> list[EvaluationExample]:
    """Load and validate a JSONL evaluation dataset."""

    dataset_path = Path(path)
    examples: list[EvaluationExample] = []
    seen_ids: dict[str, int] = {}

    with dataset_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise EvaluationDatasetError(
                    f"Invalid JSON at line {line_number}: {exc.msg}"
                ) from exc

            if not isinstance(record, dict):
                raise EvaluationDatasetError(
                    f"Expected a JSON object at line {line_number}"
                )

            try:
                example = EvaluationExample.model_validate(record)
            except ValidationError as exc:
                raise EvaluationDatasetError(
                    f"Invalid evaluation example at line {line_number}: {exc}"
                ) from exc

            if example.query_id in seen_ids:
                first_line = seen_ids[example.query_id]
                raise EvaluationDatasetError(
                    f"Duplicate query_id {example.query_id!r} at line "
                    f"{line_number}; first seen at line {first_line}"
                )

            seen_ids[example.query_id] = line_number
            examples.append(example)

    if not examples:
        raise EvaluationDatasetError(
            f"Evaluation dataset is empty: {dataset_path}"
        )

    return examples
