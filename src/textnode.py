from enum import Enum


class TextType(Enum):
    PLAIN_TEXT_TYPE = "plain"
    BOLD_TEXT_TYPE = "bold"
    ITALIC_TEXT_TYPE = "italic"
    CODE_TEXT_TYPE = "code"
    LINK_TEXT_TYPE = "link"
    IMAGE_TEXT_TYPE = "image"


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
