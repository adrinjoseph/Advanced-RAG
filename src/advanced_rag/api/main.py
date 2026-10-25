from fastapi import FastAPI

app = FastAPI(
    title="Advanced RAG",
    description="Enterprise Knowledge Intelligence Platform",
    version="0.1.0",
)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Return the basic health status of the API."""
    return {"status": "ok"}
