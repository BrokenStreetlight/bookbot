from textnode import TextNode, TextType


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
