# All test functions and file names must start with test_ to be discoverable by unittest
import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
