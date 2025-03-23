import unittest

from blocks import BlockType, markdown_to_blocks, block_to_block_type


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_blocktype_heading(self):
        md = "# This is a heading"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING)

    def test_blocktype_paragraph(self):
        md = "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_blocktype_ordered_list(self):
        md = """1. This is the first list item in a list block
2. This is a list item
3. This is another list item"""
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

    def test_blocktype_unordered_list(self):
        md = """- This is the first list item in a list block
- This is a list item
- This is another list item"""
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

    def test_blocktype_code(self):
        md = "```# This is a heading```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)
