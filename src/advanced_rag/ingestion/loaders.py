
from pathlib import Path


def load_text_file(path: str | Path) -> str:
    """Read a UTF-8 text file and return its raw contents."""
    file_path = Path(path)

    if not file_path.is_file():
        raise FileNotFoundError(f"Text file not found: {file_path}")

    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            f"File is not valid UTF-8 text: {file_path}"
        ) from exc
