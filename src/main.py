import logging

from textnode import text_to_textnodes


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


def main(text: str):
    nodes = text_to_textnodes(text)
    for node in nodes:
        logger.debug("Node: %s", node)


if __name__ == "__main__":
    logger.debug("##########   NEW RUN   ##########")
    markdown = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    main(markdown)
