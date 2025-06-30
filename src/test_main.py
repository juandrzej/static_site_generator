import unittest

from main import text_to_textnodes
from textnode import TextNode, TextType


class TestMain(unittest.TestCase):
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_only_plain_text(self):
        nodes = text_to_textnodes("This is just plain text.")
        self.assertListEqual(
            [TextNode("This is just plain text.", TextType.TEXT)],
            nodes,
        )

    def test_text_only_bold(self):
        nodes = text_to_textnodes("**Bold text only**")
        self.assertListEqual(
            [
                TextNode("Bold text only", TextType.BOLD),
            ],
            nodes,
        )

    # def test_text_multiple_markdown_types(self):
    #     nodes = text_to_textnodes(
    #         "Hello **world**! This is _fun_ and `code` is **great**."
    #     )
    #     self.assertListEqual(
    #         [
    #             TextNode("Hello ", TextType.TEXT),
    #             TextNode("world", TextType.BOLD),
    #             TextNode("! This is ", TextType.TEXT),
    #             TextNode("fun", TextType.ITALIC),
    #             TextNode(" and ", TextType.TEXT),
    #             TextNode("code", TextType.CODE),
    #             TextNode(" is ", TextType.TEXT),
    #             TextNode("great", TextType.BOLD),
    #             TextNode(".", TextType.TEXT),
    #         ],
    #         nodes,
    #     )

    def test_text_markdown_at_start_end(self):
        nodes = text_to_textnodes("**Start** and _end_.")
        self.assertListEqual(
            [
                TextNode("Start", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("end", TextType.ITALIC),
                TextNode(".", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_with_images_and_links_only(self):
        nodes = text_to_textnodes(
            "![image 1](url1) and [link 1](url2) then ![image 2](url3)"
        )
        self.assertListEqual(
            [
                TextNode("image 1", TextType.IMAGE, "url1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link 1", TextType.LINK, "url2"),
                TextNode(" then ", TextType.TEXT),
                TextNode("image 2", TextType.IMAGE, "url3"),
            ],
            nodes,
        )

    def test_empty_string(self):
        nodes = text_to_textnodes("")
        self.assertListEqual([], nodes)


if __name__ == "__main__":
    unittest.main()
