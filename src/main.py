import logging
import os
import shutil

from extractmarkdown import generate_page


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


def prep_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")


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


def copy_contents():
    walk_contents("static", "public")


def main():
    logger.debug("Prepping Public folder")
    prep_public()
    logger.debug("Copying Contents from static folder")
    copy_contents()
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
