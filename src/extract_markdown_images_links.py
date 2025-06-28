import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    re_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(re_pattern, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    re_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(re_pattern, text)
    return matches
