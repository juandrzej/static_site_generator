import unittest

from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodes(unittest.TestCase):
    def test_invalid_markdown(self):
        with self.assertRaises(Exception):
            node = TextNode("Testing **invalid md syntax.", TextType.TEXT)
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_non_text_node_passed_through(self):
        bold_node = TextNode("This is **bold** text", TextType.BOLD)
        italic_node = TextNode("This is _italic_ text", TextType.ITALIC)
        text_node_to_split = TextNode("`code` and regular text", TextType.TEXT)

        old_nodes = [bold_node, text_node_to_split, italic_node]
        delimiter = "`"
        text_type = TextType.CODE

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        expected_nodes = [
            bold_node,  # Unchanged
            TextNode("code", TextType.CODE),
            TextNode(" and regular text", TextType.TEXT),
            italic_node,  # Unchanged
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_bold(self):
        node = TextNode("This is text with **bold text** in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(" in it", TextType.TEXT),
            ],
        )

    def test_italic(self):
        node = TextNode("This is text with _italic text_ in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("italic text", TextType.ITALIC),
                TextNode(" in it", TextType.TEXT),
            ],
        )

    def test_multiple_delimiters_same_type(self):
        node = TextNode("`code1` and `code2`", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)


if __name__ == "__main__":
    unittest.main()
