import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
test_dict ={
    "href": "www.dummy.com",
    "a": "value"
}
test_answ = " href='www.dummy.com' a='value'"


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_props_to(self):
        node = HTMLNode(props=test_dict)
        self.assertEqual(node.props_to_html(), test_answ)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href='https://www.google.com'>Click me!</a>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", children=[grandchild_node])
        parent_node = ParentNode("div", children=[child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_leaf_node_with_props(self):
        node = LeafNode(tag="a", value="click me", props={"href": "https://example.com"})
        self.assertEqual(node.to_html(), "<a href='https://example.com'>click me</a>")

    def test_parent_node_with_props(self):
        child = LeafNode(tag="p", value="content")
        node = ParentNode(tag="section", children=[child], props={"id": "main"})
        self.assertEqual(node.to_html(), "<section id='main'><p>content</p></section>")

    def test_void_element_br(self):
        node = LeafNode(tag="br", value="")
        # Note: your current LeafNode raises ValueError if value is falsy
        # You may want to allow void elements to have no value
        self.assertEqual(node.to_html(), "<br>")

    def test_void_element_img_with_props(self):
        node = LeafNode(tag="img", value="", props={"src": "cat.png", "alt": "a cat"})
        self.assertEqual(node.to_html(), "<img src='cat.png' alt='a cat'>")

    def test_void_element_input(self):
        node = LeafNode(tag="input", value="", props={"type": "text", "name": "username"})
        self.assertEqual(node.to_html(), "<input type='text' name='username'>")

    def test_void_element_hr(self):
        node = LeafNode(tag="hr", value="")
        self.assertEqual(node.to_html(), "<hr>")

    def test_multiple_children(self):
        children = [
            LeafNode(tag="li", value="one"),
            LeafNode(tag="li", value="two"),
            LeafNode(tag="li", value="three"),
        ]
        node = ParentNode(tag="ul", children=children)
        self.assertEqual(
            node.to_html(),
            "<ul><li>one</li><li>two</li><li>three</li></ul>",
        )

    def test_deep_nesting(self):
        innermost = LeafNode(tag="span", value="deep")
        level3 = ParentNode(tag="div", children=[innermost], props={"class": "level3"})
        level2 = ParentNode(tag="div", children=[level3], props={"class": "level2"})
        level1 = ParentNode(tag="div", children=[level2], props={"class": "level1"})
        self.assertEqual(
            level1.to_html(),
            "<div class='level1'><div class='level2'><div class='level3'><span>deep</span></div></div></div>",
        )

    def test_mixed_children(self):
        children = [
            LeafNode(tag="h1", value="Title"),
            ParentNode(tag="p", children=[LeafNode(tag="em", value="emphasis")]),
            LeafNode(tag="br", value=""),
            LeafNode(tag="p", value="after break"),
        ]
        node = ParentNode(tag="article", children=children)
        self.assertEqual(
            node.to_html(),
            "<article><h1>Title</h1><p><em>emphasis</em></p><br><p>after break</p></article>",
        )

    def test_leaf_node_no_tag(self):
        node = LeafNode(tag=None, value="raw text")
        self.assertEqual(node.to_html(), "raw text")

    def test_parent_node_no_tag_raises(self):
        child = LeafNode(tag="span", value="x")
        node = ParentNode(tag=None, children=[child])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_no_children_raises(self):
        node = ParentNode(tag="div")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_node_no_value_raises(self):
        node = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_table_structure(self):
        cell1 = LeafNode(tag="td", value="A1")
        cell2 = LeafNode(tag="td", value="B1")
        row1 = ParentNode(tag="tr", children=[cell1, cell2])
        cell3 = LeafNode(tag="td", value="A2")
        cell4 = LeafNode(tag="td", value="B2")
        row2 = ParentNode(tag="tr", children=[cell3, cell4])
        table = ParentNode(tag="table", children=[row1, row2])
        self.assertEqual(
            table.to_html(),
            "<table><tr><td>A1</td><td>B1</td></tr><tr><td>A2</td><td>B2</td></tr></table>",
        )

if __name__ == "__main__":
    unittest.main()