from htmlnode import HTMLNode, LeafNode, ParentNode
from split_blocks import BlockType, markdown_to_blocks, block_to_block_type_functions
from text_to_textnodes import text_to_textnodes
from textnode import text_node_to_html_node


def _produce_children(block: str) -> list[LeafNode]:
    """Takes md string which is processed into text nodes and finally html nodes"""
    return [text_node_to_html_node(node) for node in text_to_textnodes(block)]


def _code_to_node(block: str) -> ParentNode:
    """Removes leading and trailing whitespaces and code ticks.
    Then returns ParentNode which includes all code lines with line breaks."""
    cleaned_block = block[3:-3].strip()
    return ParentNode("pre", [LeafNode("code", cleaned_block)])


def _paragraph_to_node(block: str) -> ParentNode:
    # For now removes enters as br tag hasn't been introduced yet
    block = " ".join(block.split("\n"))
    children = _produce_children(block)
    return ParentNode("p", children)


def _heading_to_node(block: str) -> ParentNode:
    heading_count = block[:6].count("#")
    # Removes hashes first and their trailing space
    children = _produce_children(block[heading_count + 1 :])
    return ParentNode(f"h{heading_count}", children)


def _quote_to_node(block: str) -> ParentNode:
    quote_lines = []
    for line in block.split("\n"):
        quote_lines.append(line[2:])  # Remove "> "
    quote_text = " ".join(quote_lines)
    children = _produce_children(quote_text)
    return ParentNode("blockquote", children)


def _ulist_to_node(block: str) -> ParentNode:
    parents = []
    for line in block.split("\n"):
        # Remove the "- " prefix
        clean_line = line[2:]
        # Create individual list item nodes
        children = _produce_children(clean_line)
        parents.append(ParentNode("li", children))
    return ParentNode("ul", parents)


def _olist_to_node(block: str) -> ParentNode:
    parents = []
    for i, line in enumerate(block.split("\n")):
        # Remove the "1. ", "2. ", etc. prefix
        clean_line = line[len(f"{i + 1}. ") :]
        # Create individual list item nodes
        children = _produce_children(clean_line)
        parents.append(ParentNode("li", children))
    return ParentNode("ol", parents)


def block_to_node(block: str) -> ParentNode:
    """Takes block string and outputs ParentNode
    with corresponding html tag and children included."""
    block_type: BlockType = block_to_block_type_functions(block)

    return_dict = {
        BlockType.CODE: _code_to_node,
        BlockType.PARAGRAPH: _paragraph_to_node,
        BlockType.HEADING: _heading_to_node,
        BlockType.QUOTE: _quote_to_node,
        BlockType.ULIST: _ulist_to_node,
        BlockType.OLIST: _olist_to_node,
    }
    return return_dict.get(block_type)(block)
    # # Return ParentNode based on block_type, mainly to give html tags
    # if block_type == BlockType.CODE:
    #     return _code_to_node(block)
    # if block_type == BlockType.PARAGRAPH:
    #     return _paragraph_to_node(block)
    # if block_type == BlockType.HEADING:
    #     return _heading_to_node(block)
    # if block_type == BlockType.QUOTE:
    #     return _quote_to_node(block)
    # if block_type == BlockType.ULIST:
    #     return _ulist_to_node(block)
    # if block_type == BlockType.OLIST:
    #     return _olist_to_node(block)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """Break markdown string into blocks which are changed to corresponding HTMLNodes.
    Returns ParentNode which includes all of those nodes."""
    blocks: list[str] = markdown_to_blocks(markdown)
    parents: list[ParentNode] = [block_to_node(block) for block in blocks]
    return ParentNode("div", parents)
