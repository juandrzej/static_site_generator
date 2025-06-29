import re

from textnode import TextNode, TextType


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    re_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(re_pattern, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    re_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(re_pattern, text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return_list = []
    for node in old_nodes:
        # if the current node is not plain text, add it as is and move to next one
        if node.text_type != TextType.TEXT:
            return_list.append(node)
            continue
        current_text = node.text
        matches = extract_markdown_images(current_text)
        for match in matches:
            image_alt, image_link = match[0], match[1]
            sections = current_text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0]:
                return_list.append(TextNode(sections[0], TextType.TEXT))
            return_list.append(TextNode(image_alt, TextType.IMAGE, image_link))
            current_text = sections[1]
        if current_text:
            return_list.append(TextNode(current_text, TextType.TEXT))
    return return_list


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return_list = []
    for node in old_nodes:
        # if the current node is not plain text, add it as is and move to next one
        if node.text_type != TextType.TEXT:
            return_list.append(node)
            continue
        current_text = node.text
        matches = extract_markdown_links(current_text)
        for match in matches:
            link_text, link_url = match[0], match[1]
            sections = current_text.split(f"[{link_text}]({link_url})", 1)
            if sections[0]:
                return_list.append(TextNode(sections[0], TextType.TEXT))
            return_list.append(TextNode(link_text, TextType.LINK, link_url))
            current_text = sections[1]
        if current_text:
            return_list.append(TextNode(current_text, TextType.TEXT))
    return return_list
