import logging

from textnode import TextNode, TextType
from splitnode import split_nodes_image


def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="bookbot.log",
        filemode="a",
    )

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console.setFormatter(console_formatter)
    logging.getLogger("").addHandler(console)


configure_logging()
logger = logging.getLogger(__name__)


def main():
    t1 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    logger.debug("TextNode: %s", t1)


if __name__ == "__main__":
    logger.debug("##########   NEW RUN   ##########")
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    # main()
