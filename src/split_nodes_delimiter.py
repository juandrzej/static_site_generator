from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    result_nodes_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result_nodes_list.append(node)
            continue
        if node.text.count(delimiter) != 2:
            raise Exception("That's invalid Markdown syntax.")
        start, mid, end = node.text.split(delimiter)
        result_nodes_list.extend(
            [
                TextNode(start, TextType.TEXT),
                TextNode(mid, text_type),
                TextNode(end, TextType.TEXT),
            ]
        )
    return result_nodes_list
