import os
import re
import logging

from blocktohtml import markdown_to_html_node

logger = logging.getLogger(__name__)


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    finds: list[tuple[str, str]] = []
    match_groups: list[tuple[str, str]] = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    if not match_groups:
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
        return finds
    for matches in match_groups:
        a_text = matches[0]
        url_text = matches[1]
        finds.append((a_text, url_text))
    return finds


def extract_title(markdown: str) -> str:
    lines = markdown.splitlines()
    for line in lines:
        if not line.strip().find("# ", 0, 2) == -1:
            text = line.strip("# ")
            return text.strip()
    raise ValueError("Did not find H1 header")


def generate_page(
    from_path: str, template_path: str, dest_path: str, base_path: str
) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    logger.debug(
        f"Generating page from {from_path} to {dest_path} using {template_path}"
    )

    with open(from_path, mode="r") as f:
        markdown = f.read()

    with open(template_path, mode="r") as f:
        template = f.read()

    node = markdown_to_html_node(markdown)
    html = node.to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'src="{base_path}')

    if os.path.exists(dest_path):
        os.remove(dest_path)

    with open(dest_path, mode="w") as f:
        f.write(template)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, base_path: str
) -> None:
    dir_list = os.listdir(dir_path_content)
    for item in dir_list:
        item_path = os.path.join(dir_path_content, item)
        dst_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_path):
            logger.debug(f"Creating HTML from {item}")
            dst_path = dst_path.replace(".md", ".html")
            generate_page(item_path, template_path, dst_path, base_path)
        else:
            logger.debug(f"Walking Folder: {item_path}")
            os.mkdir(dst_path)
            generate_pages_recursive(item_path, template_path, dst_path, base_path)
