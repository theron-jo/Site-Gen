from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "raw text"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        for attr in vars(self):
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.type}, {self.url})"

def text_node_to_html_node(node):
    if node.type not in TextType:
        raise TypeError
    if node.type == TextType.TEXT:
        return LeafNode(value=node.text)
    elif node.type == TextType.BOLD:
        return LeafNode("b", node.text)
    elif node.type == TextType.ITALIC:
        return LeafNode("i", node.text)
    elif node.type == TextType.CODE:
        return LeafNode("code", node.text)
    elif node.type == TextType.LINK:
        return LeafNode("a", props={"href" : node.url})
    elif node.type == TextType.IMAGE:
        return LeafNode("img", props={"src":node.url, "alt": node.text})
        