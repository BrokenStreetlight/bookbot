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
