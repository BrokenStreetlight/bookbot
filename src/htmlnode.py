class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Needs to be implemented")

    def props_to_html(self):
        text = ""
        if self.props is None:
            raise ValueError("Expected props to no be None")
        for key, value in self.props.items():
            text += f' {key}="{value}"'
        return text

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
