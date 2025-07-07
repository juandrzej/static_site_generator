# Static Site Generator

A flexible, extensible static site generator written in Python.  
Convert your Markdown documents into clean, customizable HTML websites with ease!

---

## Features

- **Markdown to HTML**: Converts standard markdown (`.md`) files into beautiful HTML pages.
- **Template Engine**: Easily apply consistent layouts across your site using HTML templates.
- **Recursive Directory Handling**: Processes entire directories of content, preserving folder structure.
- **Code Blocks, Lists, Headings, Quotes**: Full support for common Markdown block elements.
- **Asset Copying**: Non-markdown files (images, CSS, etc.) are copied as-is.
- **Navigation Support**: Relative base paths for smooth site navigation.
- **Highly Tested**: Comes with **100 automated tests** to ensure correctness and reliability.

---

## Installation

**Clone the repository:**
```sh
git clone https://github.com/juandrzej/static_site_generator.git
cd static_site_generator
```

## Usage

Generate your whole site recursively:

```python
from generator import generate_pages_recursive

generate_pages_recursive(
    dir_path_content="content/",
    template_path="template.html",
    dest_dir_path="docs/",
    base_path="/"
)
```

- Place your markdown content in the `content/` directory.
- Use `template.html` as the base template (with `{{ Title }}` and `{{ Content }}` placeholders).
- The generated site will appear in the `docs/` directory.

---

## Running Tests

This project is thoroughly tested — there are **100 automated tests** to ensure correctness and reliability.  
To run the test suite: `./test.sh`

## Customization

- **Templates:** Change your site's appearance and structure by editing `template.html` and adding your own CSS.
- **Content:** Any `.md` files you add to the `content/` directory will be automatically converted. Images and other non-markdown files are copied to the output as-is.
