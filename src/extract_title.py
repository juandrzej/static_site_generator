def extract_title(markdown: str) -> str:
    """
    Extracts the title from a Markdown string.

    The title is defined as the first line that starts with "# " (a level-1 heading).
    Returns the title text without leading "# " and whitespace removed.
    Raises an Exception if no level-1 heading is found.
    """
    for line in markdown.split("\n"):
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:]
    raise Exception("Title not found.")
