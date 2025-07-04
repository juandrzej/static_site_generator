def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.strip().startswith("# "):
            return line.strip()[2:]
    raise Exception("Title not found.")
