from typing import NamedTuple
from mkdocs.structure.pages import Page
# local
from . import logger, ListingsConfig
from .html_parser import ListingData, parse_listings_from_html

class PageData(NamedTuple):
    page_name: str
    page_url: str
    listings: list[ListingData]


class PageProcessor:
    def __init__(self, plugin_config: ListingsConfig):
        self.page_data_list: list[PageData] = []
        self.plugin_config = plugin_config

    def process_page(self, html: str, page: Page):
        if listings := parse_listings_from_html(html):
            listings = [x for x in listings if x.language not in self.plugin_config.exclude_language_list]
            self.page_data_list.append(PageData(
                page_name=page.title or "Untitled page",
                page_url=get_page_url(page),
                listings=listings,
            ))

    def clear(self):
        self.page_data_list = []


def get_page_url(page: Page) -> str:
    page_url = page.abs_url or page.canonical_url or page.url
    # This SHOULD fix the duplicate slash display bug (like '//readthedocs/')
    for _ in range(3):
        page_url = page_url.replace("//", "/")

    # Remove leading slash
    if page_url.startswith("/"):
        page_url = page_url[1:] or "index.html"

    if page_url.startswith("http://") or page_url.startswith("https://"):
        logger.warning(f"page_url is expected to be just a path, but it is a full URL: '{page_url}'")
        # No clue if it can happen. If it can, I should parse the path from the URL (and maybe remove the base URL).
    
    return page_url
