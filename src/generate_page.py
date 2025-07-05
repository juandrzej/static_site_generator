import os
from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    """Generates html page from md file. Please provide src file in .md nad dest file in .html"""
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown: str = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template: str = f.read()

    title: str = extract_title(markdown)
    content: str = markdown_to_html_node(markdown).to_html()
    static_site = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", content
    )

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(static_site)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    """Crawls recursively thru content dir copying whole structure to dest dir.
    .md files will be generated into .html pages. Other files and dirs will be moved as they are."""
    current_dir = os.listdir(dir_path_content)

    for item in current_dir:
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(src_path):
            dest_path = dest_path.replace(".md", ".html")
            generate_page(src_path, template_path, dest_path)
        else:
            os.makedirs(dest_path)
            generate_pages_recursive(src_path, template_path, dest_path)
