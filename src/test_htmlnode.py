# All test functions and file names must start with test_ to be discoverable by unittest
import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_printed_nodes(self):
        node = HTMLNode("p", "test paragraph")
        node2 = HTMLNode(
            "a",
            "",
            [node],
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(str(node), "HTMLNode(p, test paragraph, None, None)")
        node2_printed = "HTMLNode(a, , [HTMLNode(p, test paragraph, None, None)], {'href': 'https://www.google.com', 'target': '_blank'})"
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
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode()


if __name__ == "__main__":
    unittest.main()
