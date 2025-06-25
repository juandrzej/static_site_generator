# All test functions and file names must start with test_ to be discoverable by unittest
import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_printed_nodes(self):
        node = HTMLNode("test paragraph", "p")
        node2 = HTMLNode(
            "",
            "a",
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
            [node],
        )
        self.assertEqual(str(node), "HTMLNode(test paragraph, p, None, None)")
        node2_printed = "HTMLNode(, a, {'href': 'https://www.google.com', 'target': '_blank'}, [HTMLNode(test paragraph, p, None, None)])"
        self.assertEqual(str(node2), node2_printed)

    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        self.assertTrue(
            node.props_to_html() == ' href="https://www.google.com" target="_blank"'
        )

    def test_empty_nodes(self):
        node = HTMLNode()
        self.assertEqual(str(node), "HTMLNode(None, None, None, None)")

    def test_leaf_to_html_p(self):
        node = LeafNode("Hello, world!", "p")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("Click me!", "a", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )


if __name__ == "__main__":
    unittest.main()
