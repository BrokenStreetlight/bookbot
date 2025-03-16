import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        html = HTMLNode(
            "a", "a", "a", {"href": "https://www.google.com", "target": "_blank"}
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(html.props_to_html(), expected)

    def test_error(self):
        html = HTMLNode(
            "a", "a", "a", {"href": "https://www.google.com", "target": "_blank"}
        )
        with self.assertRaises(NotImplementedError):
            html.to_html()

    def test_none(self):
        html = HTMLNode()
        self.assertIsNone(html.tag)
        self.assertIsNone(html.value)
        self.assertIsNone(html.children)
        self.assertIsNone(html.props)
