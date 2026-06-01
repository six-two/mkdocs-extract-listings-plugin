import os
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
    def __init__(self, plugin_config: ListingsConfig, base_url: str):
        self.page_data_list: list[PageData] = []
        self.plugin_config = plugin_config
        self.base_url = base_url

    def process_page(self, html: str, page: Page):
        if listings := parse_listings_from_html(html):
            listings = [x for x in listings if x.language not in self.plugin_config.exclude_language_list]
            page_url = os.path.join(self.base_url, page.url)
            self.page_data_list.append(PageData(
                page_name=str(page.title) if page.title else "Untitled page",
                page_url=page_url,
                listings=listings,
            ))

    def clear(self):
        self.page_data_list = []
