from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def check_unordered_list_block(block: str) -> bool:
    if block.find("- ") == -1:
        return False

    lines = block.splitlines()
    ul_list_check = True
    for line in lines:
        if line.find("- ", 0, 2) == -1:
            ul_list_check = False
    return ul_list_check


def check_ordered_list_block(block: str) -> bool:
    if block.find("1.", 0, 2) == -1:
        return False

    lines = block.splitlines()
    ol_list_check = True
    i = 1
    for line in lines:
        if line.find(f"{i}.", 0, len(str(i)) + 1) == -1:
            ol_list_check = False
        i += 1
    return ol_list_check


def block_to_block_type(block: str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if not block.find("```", 0, 3) == -1:
        if block.endswith("```"):
            return BlockType.CODE

    if not block.find(">", 0, 1) == -1:
        for line in block.splitlines():
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if check_unordered_list_block(block):
        return BlockType.UNORDERED_LIST

    if check_ordered_list_block(block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    new_blocks: list[str] = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        new_block = block.strip()
        new_block = new_block.lstrip("\n")
        if len(new_block) > 0:
            new_blocks.append(new_block)
    return new_blocks
