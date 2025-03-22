import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        html = HTMLNode(
            "a", "a", None, {"href": "https://www.google.com", "target": "_blank"}
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(html.props_to_html(), expected)

    def test_error(self):
        html = HTMLNode(
            "a", "a", None, {"href": "https://www.google.com", "target": "_blank"}
        )
        with self.assertRaises(NotImplementedError):
            html.to_html()

    def test_none(self):
        html = HTMLNode()
        self.assertIsNone(html.tag)
        self.assertIsNone(html.value)
        self.assertIsNone(html.children)
        self.assertIsNone(html.props)


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        html = LeafNode("p", "This is a paragraph of text.").to_html()
        expected = "<p>This is a paragraph of text.</p>"
        self.assertEqual(html, expected)

    def test_eq2(self):
        html = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(html, expected)

    def test_eq3(self):
        html = LeafNode("p", "Hello, world!").to_html()
        expected = "<p>Hello, world!</p>"
        self.assertEqual(html, expected)

    def test_error(self):
        html = LeafNode("p", None)  # type: ignore checking for ValueError
        with self.assertRaises(ValueError):
            html.to_html()


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        c1 = LeafNode("span", "child")
        p = ParentNode("div", [c1])
        self.assertEqual(p.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        g1 = LeafNode("b", "grandchild")
        c1 = ParentNode("span", [g1])
        p1 = ParentNode("div", [c1])
        self.assertEqual(p1.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_many_children(self):
        p1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            p1.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_tag_error(self):
        p1 = ParentNode(None, [LeafNode(None, "Normal text")])  # type: ignore Testing ValueError
        with self.assertRaises(ValueError):
            p1.to_html()
