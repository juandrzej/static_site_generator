from htmlnode import HTMLNode, LeafNode, ParentNode
from split_blocks import BlockType, markdown_to_blocks, block_to_block_type_functions
from text_to_textnodes import text_to_textnodes
from textnode import text_node_to_html_node


def _code_block_clean(block: str) -> str:
    """Removes leading and trailing whitespaces and code ticks."""
    return block[3:-3].strip()


def _produce_children(block: str) -> list[LeafNode]:
    """Takes md string which is processed into text nodes and finally html nodes"""
    return [text_node_to_html_node(node) for node in text_to_textnodes(block)]


def block_to_node(block: str) -> ParentNode:
    """Takes block string and outputs ParentNode
    with corresponding html tag and children included."""
    block_type: BlockType = block_to_block_type_functions(block)

    # Special case; doesn't change anything inside codeblocks
    if block_type == BlockType.CODE:
        return ParentNode("pre", [LeafNode("code", _code_block_clean(block))])

    # Return ParentNode based on block_type, mainly to give html tags
    if block_type == BlockType.PARAGRAPH:
        # For now removes enters as br tag hasn't been introduced yet
        block = " ".join(block.split("\n"))
        children = _produce_children(block)
        return ParentNode("p", children)

    if block_type == BlockType.QUOTE:
        # I assume that must be better solution for this but it works for now :P
        block = " ".join(block.split("\n")).replace("> ", "")
        children = _produce_children(block)
        return ParentNode("blockquote", children)

    if block_type == BlockType.HEADING:
        heading_count: int = block[:6].count("#")
        # Removes hashes first and their trailing space
        children = _produce_children(block[heading_count + 1 :])
        return ParentNode(f"h{heading_count}", children)

    if block_type == BlockType.ULIST:
        # I assume that must be better solution for this but it works for now :P
        block = "</li><li>".join(block.split("\n"))
        children = _produce_children(block)
        return ParentNode("ul", children)

    if block_type == BlockType.OLIST:
        # I assume that must be better solution for this but it works for now :P
        block = "</li><li>".join(block.split("\n"))
        children = _produce_children(block)
        return ParentNode("ol", children)


"""
Unordered list blocks should be surrounded by a <ul> tag, and each list item should be surrounded by a <li> tag.
Ordered list blocks should be surrounded by a <ol> tag, and each list item should be surrounded by a <li> tag.
"""


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    parents: list[ParentNode] = []
    for block in blocks:
        parents.append(block_to_node(block))

    return ParentNode("div", parents)
