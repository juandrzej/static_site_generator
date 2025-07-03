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

    def test_blockquote_simple(self):
        md = """
> This is a simple blockquote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a simple blockquote</blockquote></div>",
        )

    def test_blockquote_multiline(self):
        md = """
> This is a blockquote
> with multiple lines
> all part of the same quote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with multiple lines all part of the same quote</blockquote></div>",
        )

    def test_blockquote_with_inline_markdown(self):
        md = """
> This blockquote has **bold** text
> and _italic_ text too
> plus some `code` in it
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This blockquote has <b>bold</b> text and <i>italic</i> text too plus some <code>code</code> in it</blockquote></div>",
        )

    def test_blockquote_mixed_with_other_blocks(self):
        md = """
This is a paragraph.

> This is a blockquote
> with multiple lines

Another paragraph here.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph.</p><blockquote>This is a blockquote with multiple lines</blockquote><p>Another paragraph here.</p></div>",
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

    def test_unordered_list_simple(self):
        md = """
- First item
- Second item
- Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>",
        )

    def test_unordered_list_with_inline_markdown(self):
        md = """
    - This item has **bold** text
    - This item has _italic_ text
    - This item has `code` text
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This item has <b>bold</b> text</li><li>This item has <i>italic</i> text</li><li>This item has <code>code</code> text</li></ul></div>",
        )

    def test_unordered_list_mixed_with_other_blocks(self):
        md = """
    Here's a paragraph.

    - First list item
    - Second list item

    Another paragraph.
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Here's a paragraph.</p><ul><li>First list item</li><li>Second list item</li></ul><p>Another paragraph.</p></div>",
        )

    def test_unordered_list_single_item(self):
        md = """
    - Just one item
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Just one item</li></ul></div>",
        )

    def test_ordered_list_simple(self):
        md = """
1. First item
2. Second item
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_ordered_list_with_inline_markdown(self):
        md = """
1. This item has **bold** text
2. This item has _italic_ text
3. This item has `code` text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This item has <b>bold</b> text</li><li>This item has <i>italic</i> text</li><li>This item has <code>code</code> text</li></ol></div>",
        )

    def test_ordered_list_mixed_with_other_blocks(self):
        md = """
Here's a paragraph.

1. First list item
2. Second list item

Another paragraph.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Here's a paragraph.</p><ol><li>First list item</li><li>Second list item</li></ol><p>Another paragraph.</p></div>",
        )

    def test_ordered_list_single_item(self):
        md = """
1. Just one item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Just one item</li></ol></div>",
        )

    def test_ordered_list_wrong_numbering_becomes_paragraph(self):
        md = """
    2. This starts with 2 instead of 1
    3. So it should be treated as a paragraph
    4. Not as an ordered list
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>2. This starts with 2 instead of 1 3. So it should be treated as a paragraph 4. Not as an ordered list</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
