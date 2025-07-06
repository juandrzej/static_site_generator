from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """
    Splits TextNode objects by a delimiter, converting every odd segment (inside delimiter)
    into a node of the given text_type if the node is of type TEXT.

    Any nodes not of type TEXT are left unchanged.
    Raises Exception if there's an odd number of delimiters (invalid markdown).
    """
    result_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            result_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            # Even number of parts == odd number of delimiters: invalid markdown
            raise Exception(
                f"Invalid Markdown syntax: unmatched {delimiter!r} delimiter."
            )

        for i, part in enumerate(parts):
            if part == "":
                continue  # Skip empty parts
            node_type = text_type if i % 2 == 1 else TextType.TEXT
            result_nodes.append(TextNode(part, node_type))
    return result_nodes
