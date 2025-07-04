from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
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
