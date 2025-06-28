import unittest

from extract_markdown_images_links import (
    extract_markdown_images,
    extract_markdown_links,
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


if __name__ == "__main__":
    unittest.main()
