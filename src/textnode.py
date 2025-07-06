from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """
    Represents a single contiguous piece of text in the parsed Markdown document.
    TextNode instances are used as leaf nodes within the overall HTML node tree.
    They may optionally include type information if the text should be rendered
    with special formatting, such as bold, italics, or code.
    """

    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            raise Exception("Cannot compare TextNode with different objects")
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    text = text_node.text
    url = text_node.url

    return_dict = {
        TextType.TEXT: LeafNode(None, text),
        TextType.BOLD: LeafNode("b", text),
        TextType.ITALIC: LeafNode("i", text),
        TextType.CODE: LeafNode("code", text),
        TextType.LINK: LeafNode("a", text, {"href": url}),
        TextType.IMAGE: LeafNode("img", "", {"src": url, "alt": text}),
    }

    try:
        return return_dict[text_node.text_type]
    except KeyError:
        raise Exception("Invalid text type")
