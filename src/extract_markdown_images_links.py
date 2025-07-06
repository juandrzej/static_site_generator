import re
from textnode import TextNode, TextType


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """
    Extracts all markdown image patterns from text.
    Returns a list of (alt_text, image_url) tuples.
    """
    re_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(re_pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """
    Extracts all markdown link patterns from text (excluding images).
    Returns a list of (link_text, link_url) tuples.
    """
    re_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(re_pattern, text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits text nodes into image and text segments based on markdown image syntax.
    Non-text nodes are returned unchanged.
    """
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        text = node.text
        matches = extract_markdown_images(text)
        for alt, url in matches:
            before, after = text.split(f"![{alt}]({url})", 1)
            # Alternative - for more safety but I think redundant here
            # before, sep, after = text.partition(f"![{alt}]({url})")
            if before:
                result.append(TextNode(before, TextType.TEXT))
            result.append(TextNode(alt, TextType.IMAGE, url))
            text = after  # Continue processing any further images in 'after'

        if text:
            result.append(TextNode(text, TextType.TEXT))
    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits text nodes into link and text segments based on markdown link syntax.
    Non-text nodes are returned unchanged.
    """
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        text = node.text
        matches = extract_markdown_links(text)
        for txt, url in matches:
            before, after = text.split(f"[{txt}]({url})", 1)
            # Alternative - for more safety but I think redundant here
            # before, sep, after = text.partition(f"[{txt}]({url})")
            if before:
                result.append(TextNode(before, TextType.TEXT))
            result.append(TextNode(txt, TextType.LINK, url))
            text = after  # Continue processing any further links in 'after'

        if text:
            result.append(TextNode(text, TextType.TEXT))
    return result
