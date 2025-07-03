import os
import shutil

PUBLIC_DIR_PATH = "public/"
STATIC_DIR_PATH = "static/"


def clear_public_dir() -> None:
    if os.path.exists(PUBLIC_DIR_PATH):
        shutil.rmtree(PUBLIC_DIR_PATH)
    os.mkdir(PUBLIC_DIR_PATH)


def copy_static_to_public(current_path: str | None = None) -> None:
    if current_path is None:
        current_path = STATIC_DIR_PATH
    files = os.listdir(current_path)
    # relpath would be more generic but maybe this is even "safer" ?
    current_pub_path = current_path.replace("static", "public")
    # print(current_pub_path)
    # print(files)

    for file in files:
        file_path = os.path.join(current_path, file)
        if os.path.isfile(file_path):
            # print("file" + file_path)
            shutil.copyfile(file_path, os.path.join(current_pub_path, file))
        if os.path.isdir(file_path):
            # print("dir" + file_path)
            os.mkdir(os.path.join(current_pub_path, file))
            copy_static_to_public(file_path)


def main() -> None:
    clear_public_dir()
    copy_static_to_public()


if __name__ == "__main__":
    main()
