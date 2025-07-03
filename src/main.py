import os
import shutil
from textnode import TextType, TextNode

PUBLIC_DIR_PATH = "public/"


def clear_public_dir() -> None:
    if os.path.exists(PUBLIC_DIR_PATH):
        shutil.rmtree(PUBLIC_DIR_PATH)
    os.mkdir(PUBLIC_DIR_PATH)


def copy_static_to_public() -> None:
    pass


def main() -> None:
    clear_public_dir()


if __name__ == "__main__":
    main()
