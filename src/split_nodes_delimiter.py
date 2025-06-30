from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    result_nodes_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result_nodes_list.append(node)
            continue
        if node.text.count(delimiter) == 0:
            result_nodes_list.append(node)
            continue
        if node.text.count(delimiter) == 2:
            start, mid, end = node.text.split(delimiter)
            if start:
                result_nodes_list.append(TextNode(start, TextType.TEXT))
            result_nodes_list.append(TextNode(mid, text_type))
            if end:
                result_nodes_list.append(TextNode(end, TextType.TEXT))
            continue
        raise Exception("That's invalid Markdown syntax.")
    return result_nodes_list
