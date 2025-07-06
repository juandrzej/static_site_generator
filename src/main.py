import os
import shutil
import sys
from generate_page import generate_pages_recursive

PUBLIC_DIR_PATH = "docs"
STATIC_DIR_PATH = "static"
CONTENT_DIR_PATH = "content"
TEMPLATE_HTML_FILE = "template.html"


def clear_public_dir() -> None:
    """Clear the site directory and recreate it."""
    if os.path.exists(PUBLIC_DIR_PATH):
        shutil.rmtree(PUBLIC_DIR_PATH)
    os.mkdir(PUBLIC_DIR_PATH)


def copy_static_to_public(static_path: str | None = None) -> None:
    """Copy all static content to public directory recursively."""
    if static_path is None:
        static_path = STATIC_DIR_PATH
    # relpath would be more generic but maybe this is even "safer" ?
    public_path = static_path.replace(STATIC_DIR_PATH, PUBLIC_DIR_PATH)

    items = os.listdir(static_path)
    for item in items:
        item_static_path = os.path.join(static_path, item)
        item_public_path = os.path.join(public_path, item)

        # If it's a file, just copy it
        if os.path.isfile(item_static_path):
            shutil.copyfile(item_static_path, item_public_path)

        # If it's a dir, create it and public and go thru it recursively
        if os.path.isdir(item_static_path):
            os.mkdir(item_public_path)
            copy_static_to_public(item_static_path)


def main() -> None:
    try:
        base_path: str = sys.argv[1]
    except IndexError:
        base_path = "/"

    clear_public_dir()
    copy_static_to_public()
    generate_pages_recursive(
        CONTENT_DIR_PATH, TEMPLATE_HTML_FILE, PUBLIC_DIR_PATH, base_path
    )


if __name__ == "__main__":
    main()
