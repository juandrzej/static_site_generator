import unittest
from markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = """
# This is an h1

## This is an h2

### This is an h3

#### This is an h4

##### This is an h5

###### This is an h6
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is an h1</h1><h2>This is an h2</h2><h3>This is an h3</h3><h4>This is an h4</h4><h5>This is an h5</h5><h6>This is an h6</h6></div>",
        )

    def test_heading_with_inline_markdown(self):
        md = """
# This is a **bold** heading

## This has _italic_ text

### Code in `heading` here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a <b>bold</b> heading</h1><h2>This has <i>italic</i> text</h2><h3>Code in <code>heading</code> here</h3></div>",
        )

    def test_single_heading(self):
        md = "## Just one heading"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Just one heading</h2></div>",
        )


if __name__ == "__main__":
    unittest.main()
