import unittest
from textnode import TextNode, TextType
from convert import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks

class TestConvert(unittest.TestCase):
    def test_sing_delim(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes1 = split_nodes_delimiter([node1], "`", TextType.CODE)
        self.assertEqual(new_nodes1, [
    TextNode("This is text with a ", TextType.TEXT, None),
    TextNode("code block", TextType.CODE, None),
    TextNode(" word", TextType.TEXT, None),
])
        node2 = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], "**", TextType.BOLD)
        self.assertEqual(new_nodes2, [
    TextNode("This is text with a ", TextType.TEXT, None),
    TextNode("bold", TextType.BOLD, None),
    TextNode(" word", TextType.TEXT, None),
])

    def test_multiple_delimiters_same_node(self):
        node = TextNode("This has **bold** and **more bold** here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This has ", TextType.TEXT, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" and ", TextType.TEXT, None),
            TextNode("more bold", TextType.BOLD, None),
            TextNode(" here", TextType.TEXT, None),
        ])

    def test_no_delimiter_present(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("Just plain text", TextType.TEXT, None),
        ])

    def test_delimiter_at_start_and_end(self):
        node = TextNode("**bold** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("bold", TextType.BOLD, None),
            TextNode(" in the middle", TextType.TEXT, None),
        ])

    def test_non_text_node_passthrough(self):
        bold_node = TextNode("already bold", TextType.BOLD)
        text_node = TextNode("some **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([bold_node, text_node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("already bold", TextType.BOLD, None),
            TextNode("some ", TextType.TEXT, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" text", TextType.TEXT, None),
        ])

    def test_odd_delimiter_count_raises(self):
        node = TextNode("unmatched ** delimiter", TextType.TEXT)
        with self.assertRaises(TypeError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_odd_single_char_delimiter_raises(self):
        node = TextNode("has one ` backtick only", TextType.TEXT)
        with self.assertRaises(TypeError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_nodes_mixed(self):
        node1 = TextNode("first **bold**", TextType.TEXT)
        node2 = TextNode("no delimiters here", TextType.TEXT)
        node3 = TextNode("second `code` block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("first ", TextType.TEXT, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode("no delimiters here", TextType.TEXT, None),
            TextNode("second `code` block", TextType.TEXT, None),
        ])

    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [])

    def test_three_delimiters_raises(self):
        node = TextNode("**a** **b", TextType.TEXT)
        with self.assertRaises(TypeError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "Here is a cat: ![a cat](https://example.com/cat.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("a cat", "https://example.com/cat.png")],
        )

    def test_multiple_images(self):
        text = "![first](https://a.com/1.png) and ![second](http://b.com/2.jpg)"
        self.assertEqual(
            extract_markdown_images(text),
            [("first", "https://a.com/1.png"), ("second", "http://b.com/2.jpg")],
        )

    def test_no_images(self):
        text = "Just a plain paragraph with no images."
        self.assertEqual(extract_markdown_images(text), [])

    def test_empty_alt_text(self):
        text = "![ ](https://example.com/x.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [(" ", "https://example.com/x.png")],
        )

    def test_image_with_spaces_in_alt(self):
        text = "![my favorite photo](https://example.com/photo.jpg)"
        self.assertEqual(
            extract_markdown_images(text),
            [("my favorite photo", "https://example.com/photo.jpg")],
        )

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "Visit [our site](https://example.com) for more."
        self.assertEqual(
            extract_markdown_links(text),
            [("our site", "https://example.com")],
        )

    def test_multiple_links(self):
        text = "[one](https://a.com) and [two](http://b.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("one", "https://a.com"), ("two", "http://b.com")],
        )

    def test_no_links(self):
        text = "No links here at all."
        self.assertEqual(extract_markdown_links(text), [])

    def test_link_with_parens_in_url(self):
        text = "[wiki](https://en.wikipedia.org/wiki/Foo_(bar))"
        self.assertEqual(
            extract_markdown_links(text),
            [("wiki", "https://en.wikipedia.org/wiki/Foo_(bar)")],
        )

class TestImagesVsLinks(unittest.TestCase):
    def test_images_not_matched_as_links(self):
        """Images contain [text](url) inside them — links function may or may not pick them up."""
        text = "![alt text](https://example.com/img.png)"
        result = extract_markdown_links(text)
        # The links pattern WILL match the [alt text](url) inside the image syntax
        # This documents the current behavior (it's a known overlap)
        self.assertEqual(result, [("alt text", "https://example.com/img.png")])

    def test_images_not_matched_as_links(self):
        text = "![alt text](https://example.com/img.png)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
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
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://wikipedia.org"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )

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