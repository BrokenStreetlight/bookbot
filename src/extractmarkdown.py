import re
import logging

logger = logging.getLogger(__name__)


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    finds: list[tuple[str, str]] = []
    match_groups: list[tuple[str, str]] = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    if not match_groups:
        logger.debug("Did not find any image markdown in text")
        return finds
    for matches in match_groups:
        alt_text = matches[0]
        url_text = matches[1]
        finds.append((alt_text, url_text))
    return finds


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    finds: list[tuple[str, str]] = []
    match_groups: list[tuple[str, str]] = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    if not match_groups:
        logger.debug("Did not find any link markdown in text")
        return finds
    for matches in match_groups:
        a_text = matches[0]
        url_text = matches[1]
        finds.append((a_text, url_text))
    return finds


def markdown_to_blocks(markdown: str) -> list[str]:
    new_blocks: list[str] = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        new_block = block.strip()
        new_block = new_block.lstrip("\n")
        if len(new_block) > 0:
            new_blocks.append(new_block)
    return new_blocks


if __name__ == "__main__":
    markdown = """# This is a heading




This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
    """
    print(markdown_to_blocks(markdown))
