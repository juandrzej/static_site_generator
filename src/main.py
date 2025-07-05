import os
import shutil
import sys
from generate_page import generate_pages_recursive

PUBLIC_DIR_PATH = "public"
STATIC_DIR_PATH = "static"
CONTENT_DIR_PATH = "content"
TEMPLATE_HTML_FILE = "template.html"


def clear_public_dir() -> None:
    if os.path.exists(PUBLIC_DIR_PATH):
        shutil.rmtree(PUBLIC_DIR_PATH)
    os.mkdir(PUBLIC_DIR_PATH)


def copy_static_to_public(current_path: str | None = None) -> None:
    if current_path is None:
        current_path = STATIC_DIR_PATH
    files = os.listdir(current_path)
    # relpath would be more generic but maybe this is even "safer" ?
    current_pub_path = current_path.replace(STATIC_DIR_PATH, PUBLIC_DIR_PATH)

    for file in files:
        file_path = os.path.join(current_path, file)
        if os.path.isfile(file_path):
            shutil.copyfile(file_path, os.path.join(current_pub_path, file))
        if os.path.isdir(file_path):
            os.mkdir(os.path.join(current_pub_path, file))
            copy_static_to_public(file_path)


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
