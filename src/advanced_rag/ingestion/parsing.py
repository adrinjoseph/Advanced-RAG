
def normalize_text(text: str) -> str:
    """Normalize whitespace while preserving paragraph boundaries."""
    if not text or not text.strip():
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    lines = [line.strip() for line in text.split("\n")]
    normalized = "\n".join(lines)

    # Collapse repeated blank lines to a single paragraph break.
    while "\n\n\n" in normalized:
        normalized = normalized.replace("\n\n\n", "\n\n")

    return normalized.strip()
