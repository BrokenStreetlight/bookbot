class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        """Convert the Node to HTML string.
        returns:
        str"""
        raise NotImplementedError("Needs to be implemented")

    def props_to_html(self):
        text = ""
        if self.props is None:
            return text
        for key, value in self.props.items():
            text += f' {key}="{value}"'
        return text

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All LeafNode's must have a value.")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list["HTMLNode"], props: dict[str, str] | None = None
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All ParentNode's must have a tag.")

        if self.children is None:
            raise ValueError("All ParentNode's must have children.")

        html = f"<{self.tag}>"
        for child_node in self.children:
            html += child_node.to_html()
        return f"{html}</{self.tag}>"
