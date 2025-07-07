from htmlnode import HTMLNode, LeafNode, ParentNode
from split_blocks import BlockType, markdown_to_blocks, block_to_block_type
from markdown_to_textnodes import markdown_to_textnodes
from textnode import text_node_to_html_node


def _produce_children(block: str) -> list[LeafNode]:
    """
    Converts the given markdown block into HTML leaf nodes
    by first parsing text nodes, then converting each to HTML.
    """
    return [text_node_to_html_node(node) for node in markdown_to_textnodes(block)]


def _code_to_node(block: str) -> ParentNode:
    """Removes leading and trailing whitespaces and code ticks.
    Then returns ParentNode which includes all code lines with line breaks."""
    cleaned_block = block[3:-3].strip()
    return ParentNode("pre", [LeafNode("code", cleaned_block)])


def _paragraph_to_node(block: str) -> ParentNode:
    # For now removes enters as br tag hasn't been introduced yet
    block = " ".join(block.splitlines())
    children = _produce_children(block)
    return ParentNode("p", children)


def _heading_to_node(block: str) -> ParentNode:
    heading_count = block[:6].count("#")
    # Removes hashes first and their trailing space
    children = _produce_children(block[heading_count + 1 :])
    return ParentNode(f"h{heading_count}", children)


def _quote_to_node(block: str) -> ParentNode:
    lines = [line[2:] for line in block.splitlines()]
    text = " ".join(lines)
    children = _produce_children(text)
    return ParentNode("blockquote", children)


def _ulist_to_node(block: str) -> ParentNode:
    parents = [
        ParentNode("li", _produce_children(line[2:])) for line in block.splitlines()
    ]
    return ParentNode("ul", parents)


def _olist_to_node(block: str) -> ParentNode:
    parents = []
    for i, line in enumerate(block.splitlines()):
        # Remove the "1. ", "2. ", etc. prefix
        clean_line = line[len(f"{i + 1}. ") :]
        # Create individual list item nodes
        children = _produce_children(clean_line)
        parents.append(ParentNode("li", children))
    return ParentNode("ol", parents)


def block_to_node(block: str) -> ParentNode:
    """
    Converts a markdown block to the appropriate ParentNode (HTML element with children).
    """
    block_type: BlockType = block_to_block_type(block)
    mapping = {
        BlockType.CODE: _code_to_node,
        BlockType.PARAGRAPH: _paragraph_to_node,
        BlockType.HEADING: _heading_to_node,
        BlockType.QUOTE: _quote_to_node,
        BlockType.ULIST: _ulist_to_node,
        BlockType.OLIST: _olist_to_node,
    }

    func = mapping.get(block_type)
    if func is None:
        raise ValueError(f"No conversion function for block type: {block_type}")
    return func(block)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """Break markdown string into blocks which are changed to corresponding HTMLNodes.
    Returns ParentNode which includes all of those nodes."""
    blocks: list[str] = markdown_to_blocks(markdown)
    parents: list[ParentNode] = [block_to_node(block) for block in blocks]
    return ParentNode("div", parents)
