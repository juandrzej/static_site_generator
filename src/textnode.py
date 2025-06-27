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
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

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
    return_dict = {
        TextType.TEXT: LeafNode(None, text_node.text),
        TextType.BOLD: LeafNode("b", text_node.text),
        TextType.ITALIC: LeafNode("i", text_node.text),
        TextType.CODE: LeafNode("code", text_node.text),
        TextType.LINK: LeafNode("a", text_node.text, {"href": text_node.url}),
        TextType.IMAGE: LeafNode(
            "img",
            "",
            {"src": text_node.url, "alt": text_node.text},
        ),
    }

    def raise_invalid_type():
        raise Exception("Invalid text type")

    return return_dict.get(text_node.text_type, raise_invalid_type)
