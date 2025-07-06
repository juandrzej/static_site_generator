import unittest

from split_blocks import BlockType, markdown_to_blocks, block_to_block_type


class TestSplitBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """


# Heading with lots of newlines


This is a paragraph



Another paragraph


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading with lots of newlines",
                "This is a paragraph",
                "Another paragraph",
            ],
        )

    def test_markdown_to_blocks_whitespace_handling(self):
        md = """   # Heading with leading spaces   

  This paragraph has leading and trailing spaces  

    - List item with spaces    
    - Another list item    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading with leading spaces",
                "This paragraph has leading and trailing spaces",
                "- List item with spaces\n- Another list item",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "Just a single paragraph with no breaks"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single paragraph with no breaks"])

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_newlines(self):
        md = "\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_mixed_whitespace(self):
        md = "\t\n# Heading\n\n\t\nParagraph with tabs\n\n\t\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading", "Paragraph with tabs"])

    def test_markdown_to_blocks_multiline_within_block(self):
        md = """First paragraph line
Second paragraph line
Third paragraph line

Another block here"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph line\nSecond paragraph line\nThird paragraph line",
                "Another block here",
            ],
        )

    def test_markdown_to_blocks_code_blocks(self):
        md = """Here's some code:

```python
def hello():
    print("world")
```

And here's more text"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Here's some code:",
                '```python\ndef hello():\nprint("world")\n```',
                "And here's more text",
            ],
        )


class TestBlockToLockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(BlockType.HEADING, block_to_block_type("# tsjfbsjkbfj"))

    def test_heading2(self):
        self.assertEqual(BlockType.HEADING, block_to_block_type("### tsjfbsjkbfj"))

    def test_heading3(self):
        self.assertEqual(BlockType.HEADING, block_to_block_type("###### tsjfbsjkbfj"))

    def test_heading_too_many_hashes(self):
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type("####### Not a valid heading"),
        )

    def test_heading_missing_space(self):
        self.assertEqual(
            BlockType.PARAGRAPH, block_to_block_type("###Not a valid heading")
        )

    def test_code_block(self):
        self.assertEqual(BlockType.CODE, block_to_block_type("```\ncode here\n```"))

    def test_code_block_single_line(self):
        self.assertEqual(BlockType.CODE, block_to_block_type("```print('hi')```"))

    def test_code_block_incomplete(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("```not closed"))

    def test_quote_block(self):
        self.assertEqual(BlockType.QUOTE, block_to_block_type("> to be\n> or not"))

    def test_quote_block_missing_symbol(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("> good\nbad"))

    def test_unordered_list(self):
        self.assertEqual(BlockType.ULIST, block_to_block_type("- alpha\n- beta"))

    def test_unordered_list_missing_dash(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("- first\nsecond"))

    def test_ordered_list(self):
        self.assertEqual(
            BlockType.OLIST, block_to_block_type("1. one\n2. two\n3. three")
        )

    def test_ordered_list_skips_a_number(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("1. first\n3. third"))

    def test_ordered_list_duplicate_number(self):
        self.assertEqual(
            BlockType.PARAGRAPH, block_to_block_type("1. first\n1. second")
        )

    def test_ordered_list_non_number(self):
        self.assertEqual(
            BlockType.PARAGRAPH, block_to_block_type("one. first\n2. second")
        )

    def test_paragraph(self):
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("just some text"))


if __name__ == "__main__":
    unittest.main()
