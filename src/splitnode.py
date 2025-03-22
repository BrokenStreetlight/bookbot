from textnode import TextNode, TextType
from extractmarkdown import extract_markdown_images, extract_markdown_links


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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        old_text = old_node.text
        for image in images:
            image_alt = image[0]
            image_link = image[1]
            section = old_text.split(f"![{image_alt}]({image_link})", 1)
            print(f"section:{section}")
            print(f"old_text:{old_text}")
            old_text = old_text.replace(section[0])
            print(f"post_old_text:{old_text}")
            print("----")


if __name__ == "__main__":
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
