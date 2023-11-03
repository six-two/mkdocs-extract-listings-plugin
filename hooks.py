# builtin
import os
from typing import NamedTuple
from html import escape
# pip
from mkdocs.structure.pages import Page
from mkdocs.config.defaults import MkDocsConfig
from bs4 import BeautifulSoup

OUT_FILE="listings.md"
OUT_PATH=os.path.join
PLACEHOLDER="PLACEHOLDER_VALUE_FOR_THE_LISTINGS_PLUGIN"

def is_code_listing(pre_node) -> bool:
    try:
        for child in pre_node.children:
            if child.name == "code":
                return True
        return False
    except KeyError:
        # No children -> no code listing
        return False


class PageData(NamedTuple):
    page_name: str
    page_url: str
    listings: list[str]

page_data = []

# https://www.mkdocs.org/dev-guide/plugins/#on_page_content
def on_page_content(html: str, page, config: MkDocsConfig, files) -> None:
    soup = BeautifulSoup(html, "html.parser")

    listings = []

    parts = soup.findAll('pre')
    for pre in parts:
        if is_code_listing(pre):
            listings.append(str(pre))

    if listings:
        page_data.append(PageData(
            page_name=page.title,
            page_url=page.abs_url,
            listings=listings,
        ))


def on_pre_build(config: MkDocsConfig):
    # Reset before every build -> prevent duplicate entries
    global page_data
    page_data = []



def on_post_build(config: MkDocsConfig):
    path = os.path.join(config.site_dir, OUT_FILE).removesuffix(".md")
    if config.use_directory_urls:
        path = os.path.join(path, "index.html")
    else:
        path += ".html"

    with open(path, "r") as f:
        html = f.read()

    html = html.replace(PLACEHOLDER, get_listings_html())

    with open(path, "w") as f:
        f.write(html)


def get_listings_html() -> str:
    html = ""

    for p in page_data:
        html += f'<h2><a href="{p.page_url}">{escape(p.page_url)} - {escape(p.page_name)}</a></h2>'
        for listing in p.listings:
            html += listing

    return html