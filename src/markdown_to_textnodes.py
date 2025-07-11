from extract_markdown_images_links import split_nodes_image, split_nodes_link
from textnode import TextType, TextNode
from split_nodes_delimiter import split_nodes_delimiter


def markdown_to_textnodes(markdown: str) -> list[TextNode]:
    """
    Converts a markdown text string into a list of TextNode objects,
    handling bold (**), italic (_), code (`), images, and links in order.
    """
    initial_node = TextNode(markdown, TextType.TEXT)
    after_bold = split_nodes_delimiter([initial_node], "**", TextType.BOLD)
    after_italic = split_nodes_delimiter(after_bold, "_", TextType.ITALIC)
    after_code = split_nodes_delimiter(after_italic, "`", TextType.CODE)
    after_img = split_nodes_image(after_code)
    after_link = split_nodes_link(after_img)
    return after_link
