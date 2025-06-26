# All test functions and file names must start with test_ to be discoverable by unittest
import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
            node = LeafNode()
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_mixed_children(self):
        node = ParentNode(
            "span",
            [
                LeafNode(None, "plain"),
                LeafNode("b", "bold"),
                LeafNode(None, "text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<span>plain<b>bold</b>text</span>",
        )

    def test_to_html_nested_parent_nodes(self):
        inner = ParentNode("em", [LeafNode(None, "emphasized")])
        outer = ParentNode(
            "div", [LeafNode(None, "start--"), inner, LeafNode(None, "--end")]
        )
        self.assertEqual(outer.to_html(), "<div>start--<em>emphasized</em>--end</div>")

    def test_parent_node_missing_tag_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("i", "abc")]).to_html()

    def test_parent_node_missing_children_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode("ul", None).to_html()

    def test_parent_node_empty_children(self):
        node = ParentNode("section", [])
        # Depending on your implementation, this may return just <section></section>
        self.assertEqual(node.to_html(), "<section></section>")


if __name__ == "__main__":
    unittest.main()
