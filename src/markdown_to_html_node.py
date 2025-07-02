"""
Quote blocks should be surrounded by a <blockquote> tag.
Unordered list blocks should be surrounded by a <ul> tag, and each list item should be surrounded by a <li> tag.
Ordered list blocks should be surrounded by a <ol> tag, and each list item should be surrounded by a <li> tag.
Headings should be surrounded by a <h1> to <h6> tag, depending on the number of # characters.
"""

from types import CodeType
from htmlnode import HTMLNode, LeafNode, ParentNode
from split_blocks import BlockType, markdown_to_blocks, block_to_block_type_functions
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, text_node_to_html_node


def _code_block_clean(block: str) -> str:
    return "\\n".join(block[3:-3].strip().split("\n"))


def block_to_node(block: str) -> ParentNode:
    block_type: BlockType = block_to_block_type_functions(block)

    # Special case; doesn't change anything inside codeblocks
    if block_type == BlockType.CODE:
        return ParentNode("pre", [LeafNode("code", _code_block_clean(block))])

    # First create children as all will use it
    children = [text_node_to_html_node(node) for node in text_to_textnodes(block)]
    if block_type == BlockType.PARAGRAPH:
        return ParentNode("p", children)
    if block_type == BlockType.QUOTE:
        return ParentNode("blockquote", children)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    parents: list[ParentNode] = []
    for block in blocks:
        parents.append(block_to_node(block))

    print(ParentNode("div", parents).to_html())
    return ParentNode("div", parents)
