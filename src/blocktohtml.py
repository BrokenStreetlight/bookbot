from collections.abc import Generator

from htmlnode import HTMLNode, ParentNode, LeafNode
from blocks import BlockType, markdown_to_blocks, block_to_block_type
from textnode import text_to_textnodes, text_node_to_html_node


def block_type_tag(block_type: BlockType, text: str) -> str:
    if block_type == BlockType.PARAGRAPH:
        return "p"
    if block_type == BlockType.CODE:
        return "code"
    if block_type == BlockType.QUOTE:
        return "blockquote"
    if block_type == BlockType.UNORDERED_LIST:
        return "ul"
    if block_type == BlockType.ORDERED_LIST:
        return "ol"
    if block_type == BlockType.HEADING:
        if not text.find("# ", 0, 2) == -1:
            return "h1"
        if not text.find("## ", 0, 3) == -1:
            return "h2"
        if not text.find("### ", 0, 4) == -1:
            return "h3"
        if not text.find("#### ", 0, 5) == -1:
            return "h4"
        if not text.find("##### ", 0, 6) == -1:
            return "h5"
        if not text.find("###### ", 0, 7) == -1:
            return "h6"
    raise ValueError(f"Got unexpected BlockType: {block_type}")


def text_to_children(text: str) -> Generator[LeafNode, None, None]:
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        child_node = text_node_to_html_node(node)
        yield child_node


def convert_returns(text: str) -> str:
    lines = text.splitlines()
    lines = [x.strip() for x in lines if len(x) > 0]
    return "\n".join(lines)


def code_block(text: str) -> ParentNode:
    text = text.replace("```", "")
    clean_text = convert_returns(text)
    text_node = LeafNode(None, clean_text)
    inner_node = ParentNode("code", [text_node])
    outer_node = ParentNode("pre", [inner_node])
    return outer_node


def ul_block(text: str) -> ParentNode:
    nodes: list[LeafNode] = []
    lines = text.splitlines()

    for line in lines:
        if line.find("- ", 0, 2) == -1:
            raise ValueError("Got unexpected line start in unordered list")
        nodes.append(LeafNode("li", line))
    return ParentNode("ul", nodes)


def ol_block(text: str) -> ParentNode:
    nodes: list[LeafNode] = []
    lines = text.splitlines()

    i = 1
    for line in lines:
        if line.find(f"{i}.", 0, len(str(i)) + 1) == -1:
            raise ValueError("Got unexpected line start in ordered list")
        i += 1
        nodes.append(LeafNode("li", line))
    return ParentNode("ol", nodes)


def strip_returns(text: str) -> str:
    lines = text.splitlines()
    lines = [x.strip() for x in lines]
    return " ".join(lines)


def quote_block(text: str) -> ParentNode:
    lines = text.split("\n")
    new_lines: list[str] = []
    nodes: list[LeafNode] = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Got unexpected line start in quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    nodes.extend(text_to_children(content))
    return ParentNode("blockquote", nodes)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    nodes: list[ParentNode] = []

    for block in markdown_to_blocks(markdown):
        children: list[LeafNode | ParentNode] = []
        block_type = block_to_block_type(block)
        block_tag = block_type_tag(block_type, block)
        if block_type == BlockType.CODE:
            nodes.append(code_block(block))
            continue
        if block_type == BlockType.UNORDERED_LIST:
            nodes.append(ul_block(block))
            continue
        if block_type == BlockType.ORDERED_LIST:
            nodes.append(ol_block(block))
            continue
        if block_type == BlockType.QUOTE:
            nodes.append(quote_block(block))
            continue
        clean_text = strip_returns(block)
        children.extend(text_to_children(clean_text))
        nodes.append(ParentNode(block_tag, children))

    return ParentNode("div", nodes)


if __name__ == "__main__":
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    node = markdown_to_html_node(md)
    html = node.to_html()
    print(html)
