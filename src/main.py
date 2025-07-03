from extract_markdown_images_links import split_nodes_image, split_nodes_link
from textnode import TextType, TextNode


def main() -> None:
    dummy = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(dummy)


if __name__ == "__main__":
    main()
