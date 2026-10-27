from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class EvaluationExample(BaseModel):
    """One labelled example in the RAG evaluation dataset."""

    model_config = ConfigDict(extra="forbid")

    query_id: str
    query: str
    category: str
    answerable: bool
    relevant_chunk_ids: list[str] = Field(default_factory=list)
    reference_answer: str | None = None
    notes: str | None = None

    @field_validator("query_id", "query", "category")
    @classmethod
    def validate_non_empty_string(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Must not be empty or whitespace only")
        return value

    @field_validator("relevant_chunk_ids")
    @classmethod
    def validate_chunk_ids(cls, value: list[str]) -> list[str]:
        cleaned_ids = []

        for chunk_id in value:
            chunk_id = chunk_id.strip()
            if not chunk_id:
                raise ValueError("Chunk IDs must not be empty")
            cleaned_ids.append(chunk_id)

        if len(cleaned_ids) != len(set(cleaned_ids)):
            raise ValueError("Relevant chunk IDs must be unique")

        return cleaned_ids

    @model_validator(mode="after")
    def validate_answerability(self) -> "EvaluationExample":
        if self.answerable and not self.relevant_chunk_ids:
            raise ValueError(
                "Answerable examples must have at least one relevant chunk ID"
            )

        if not self.answerable and self.relevant_chunk_ids:
            raise ValueError(
                "Unanswerable examples must not have relevant chunk IDs"
            )

        return self