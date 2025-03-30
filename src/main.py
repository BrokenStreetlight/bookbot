import logging
import os
import shutil
import sys

from extractmarkdown import generate_pages_recursive


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


def prep_docs(dest_path: str):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)


def walk_contents(static_path: str, public_path: str) -> None:
    dir_list = os.listdir(static_path)
    for item in dir_list:
        item_path = os.path.join(static_path, item)
        dst_path = os.path.join(public_path, item)
        if os.path.isfile(item_path):
            logger.debug(f"Moving File: {item_path} to {dst_path}")
            shutil.copyfile(item_path, dst_path)
        else:
            logger.debug(f"Walking Folder: {item_path}")
            os.mkdir(dst_path)
            walk_contents(item_path, dst_path)


def main():
    cli_args = sys.argv
    if len(cli_args) == 1:
        basepath = "/"
    else:
        basepath = cli_args[1]
    logger.debug("Prepping Docs folder")
    prep_docs("docs")
    logger.debug("Copying Contents from static folder")
    walk_contents("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
