import unittest

from textnode import TextNode, TextType
from extract_markdown_images_links import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
)


class ExtractMarkdownImagesLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_2(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("There are no images here!")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_ignores_images(self):
        matches = extract_markdown_links(
            "This is an image: ![alt](https://img.com/cat.png)"
        )
        self.assertListEqual([], matches)

    def test_image_with_empty_alt(self):
        matches = extract_markdown_images(
            "Here is an image with blank alt text ![](https://img.com/no-alt.png)"
        )
        self.assertListEqual([("", "https://img.com/no-alt.png")], matches)

    def test_link_with_special_chars(self):
        matches = extract_markdown_links(
            "Try [searching](https://duckduckgo.com?q=python+regex) for more info."
        )
        self.assertListEqual(
            [("searching", "https://duckduckgo.com?q=python+regex")], matches
        )

    def test_multiple_images_and_links(self):
        text = (
            "![pic1](http://a.com/a.png) and [boot.dev](https://boot.dev)!"
            " ![pic2](http://b.com/b.png), and [Python!](https://python.org)"
        )
        img_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual(
            [("pic1", "http://a.com/a.png"), ("pic2", "http://b.com/b.png")],
            img_matches,
        )
        self.assertListEqual(
            [("boot.dev", "https://boot.dev"), ("Python!", "https://python.org")],
            link_matches,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [boot.dev](https://boot.dev) and another [Python!](https://python.org)!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("boot.dev", TextType.LINK, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("Python!", TextType.LINK, "https://python.org"),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        # Test when there are no images - should return original node
        node = TextNode("This is just plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_empty_text_sections(self):
        # Test that empty text sections are not added
        node = TextNode("![image1](url1)![image2](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image1", TextType.IMAGE, "url1"),
            TextNode("image2", TextType.IMAGE, "url2"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_non_text_nodes(self):
        # Test that non-TEXT nodes are passed through unchanged
        nodes = [
            TextNode("regular text", TextType.TEXT),
            TextNode("link text", TextType.LINK, "https://example.com"),
            TextNode("image alt", TextType.IMAGE, "https://image.com"),
        ]
        new_nodes = split_nodes_image(nodes)
        # Should only process the TEXT node, others pass through
        expected = [
            TextNode("regular text", TextType.TEXT),  # no images, so unchanged
            TextNode("link text", TextType.LINK, "https://example.com"),
            TextNode("image alt", TextType.IMAGE, "https://image.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_multiple_nodes(self):
        # Test processing multiple nodes in the list
        nodes = [
            TextNode("First ![img1](url1) node", TextType.TEXT),
            TextNode("Second ![img2](url2) node", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" node", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_no_links(self):
        # Test when there are no links - should return original node
        node = TextNode("This is just plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_empty_text_sections(self):
        # Test that empty text sections are not added
        node = TextNode("[link1](url1)[link2](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_non_text_nodes(self):
        # Test that non-TEXT nodes are passed through unchanged
        nodes = [
            TextNode("regular text", TextType.TEXT),
            TextNode("link text", TextType.LINK, "https://example.com"),
            TextNode("image alt", TextType.IMAGE, "https://image.com"),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("regular text", TextType.TEXT),  # no links, so unchanged
            TextNode("link text", TextType.LINK, "https://example.com"),
            TextNode("image alt", TextType.IMAGE, "https://image.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_multiple_nodes(self):
        # Test processing multiple nodes in the list
        nodes = [
            TextNode("First [link1](url1) node", TextType.TEXT),
            TextNode("Second [link2](url2) node", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" node", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)


if __name__ == "__main__":
    unittest.main()
