import logging
from collections.abc import Callable, Generator

from textnode import TextNode, TextType
from extractmarkdown import extract_markdown_images, extract_markdown_links

logger = logging.getLogger(__name__)


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        split_texts = old_node.text.split(delimiter)
        if len(split_texts) % 2 == 0:
            raise ValueError(
                f"Missing matching delimiter: {delimiter} in {old_node.text}"
            )
        flip = True
        for text in split_texts:
            if flip:
                new_nodes.append(TextNode(text, TextType.TEXT))
                flip = False
            else:
                new_nodes.append(TextNode(text, text_type))
                flip = True
    return new_nodes


def split_old_node_text(old_text: str, node: TextNode) -> tuple[str, str]:
    if node.text_type == TextType.IMAGE:
        delimiter = f"![{node.text}]({node.url})"
    elif node.text_type == TextType.LINK:
        delimiter = f"[{node.text}]({node.url})"
    else:
        raise ValueError(
            "TextType is invalid for split_node_url: %s", node.text_type.value
        )

    split_text = old_text.split(delimiter, 1)
    before_text = split_text[0]
    after_text = split_text[1]
    return before_text, after_text


def split_nodes_url(
    old_node: TextNode,
    text_type: TextType,
    func: Callable[[str], list[tuple[str, str]]],
) -> Generator[TextNode, None, None]:
    markdown_returns = func(old_node.text)
    if not markdown_returns:
        logger.debug("Old Node did not contain %s markdown", text_type.value)
        yield old_node
        return
    original_text = old_node.text
    for md_return in markdown_returns:
        node = TextNode(md_return[0], text_type, md_return[1])
        before, original_text = split_old_node_text(original_text, node)
        if len(before) > 0:
            yield TextNode(before, TextType.TEXT)
        yield node


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if not old_node.text_type == TextType.TEXT:
            new_nodes.append(old_node)
            continue
        new_nodes.extend(
            split_nodes_url(old_node, TextType.IMAGE, extract_markdown_images)
        )
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if not old_node.text_type == TextType.TEXT:
            new_nodes.append(old_node)
            continue
        new_nodes.extend(
            split_nodes_url(old_node, TextType.LINK, extract_markdown_links)
        )
    return new_nodes
