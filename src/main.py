import logging

from textnode import TextNode, TextType


def setup_file_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a file handler that logs even debug messages
    fh = logging.FileHandler("bookbot.log")
    fh.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(fh)
    return logger


def main():
    t1 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    logger.debug("TextNode: %s", t1)


if __name__ == "__main__":
    logger = setup_file_logger()
    main()
