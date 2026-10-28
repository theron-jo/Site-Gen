

class HTMLNode():
    VOID_ELEMENTS = frozenset({
    'area','base','br','col','embed','hr','img','input',
    'link','meta','param','source','track','wbr'
})
    def __init__(self, tag: str = None, value:str = None, children:list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        html_all = ""
        for att, prop in self.props.items():
            html = f" {att}='{prop}'"
            html_all += html
        return html_all

    def __repr__(self):
        return f"HTMLNode ({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other) -> bool:
        for attr in vars(self):
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if not self.value and self.tag not in self.VOID_ELEMENTS:
            raise ValueError
        if not self.tag:
            return self.value
        if self.tag in self.VOID_ELEMENTS and self.props:
            prop_html = self.props_to_html()
            return f"<{self.tag}{prop_html}>"
        elif self.tag in self.VOID_ELEMENTS and not self.props:
            return f"<{self.tag}>"
        elif self.tag not in self.VOID_ELEMENTS and self.props:
            prop_html = self.props_to_html()
            return f"<{self.tag}{prop_html}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LEAFNode ({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag=None, value=None, children:list[HTMLNode]=None, props=None):
        super().__init__(tag, value, children, props)
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if not self.tag:
            raise ValueError ("Node not adorned with HTML tag")
        if not self.children:
            raise ValueError ("Parent Node has no assigned child Nodes")
        all_html = ""
        if self.props:
            prop_html = self.props_to_html()
            for child in self.children:
                html = child.to_html()
                all_html += html
            return f"<{self.tag}{prop_html}>{all_html}</{self.tag}>"
        else:
            for child in self.children:
                html = child.to_html()
                all_html += html
            return f"<{self.tag}>{all_html}</{self.tag}>"
        
