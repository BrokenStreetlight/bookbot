from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            raise NotImplementedError(
                f"This can only compare objects of Type: TextNode"
            )
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    node_type = text_node.text_type
    node_text = text_node.text

    if node_type == TextType.TEXT:
        return LeafNode(None, node_text)

    if node_type == TextType.BOLD:
        return LeafNode("b", node_text)

    if node_type == TextType.ITALIC:
        return LeafNode("i", node_text)

    if node_type == TextType.CODE:
        return LeafNode("code", node_text)

    if node_type == TextType.LINK:
        if text_node.url is None:
            raise ValueError("URL is required for LINK TextType")
        return LeafNode("a", node_text, {"href": text_node.url})

    if node_type == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("URL is required for IMAGE TextType")
        return LeafNode("img", "", {"src": text_node.url, "alt": node_text})
    raise NotImplementedError("TextNode cannot determine TextType")
