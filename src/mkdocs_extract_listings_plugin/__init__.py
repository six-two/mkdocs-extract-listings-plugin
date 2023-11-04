# builtin
import os
from typing import NamedTuple
from html import escape
# pip
from mkdocs.config.config_options import Type
from mkdocs.config.base import Config
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.pages import Page
from mkdocs.config.defaults import MkDocsConfig
from bs4 import BeautifulSoup

class ListingsConfig(Config):
    listings_file = Type(str, default="listings.md")
    placeholder = Type(str, default="PLACEHOLDER_LISTINGS_PLUGIN")


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


class ListingsPlugin(BasePlugin[ListingsConfig]):
    def __init__(self) -> None:
        super().__init__()
        self.page_data: list[PageData] = []
        self.logger = get_plugin_logger(__name__)

    def on_pre_build(self, config: MkDocsConfig):
        # Reset before every build -> prevent duplicate entries when running mkdocs serve
        self.page_data = []

        listings_file = os.path.join(config.docs_dir, self.config.listings_file)
        if not os.path.isfile(listings_file):
            raise PluginError(f"'listings_file' does not reference a valid Markdown file: '{listings_file}' does not exist")
        elif not self.config.listings_file.endswith(".md"):
            self.logger.warning(f"Value for 'listings_file' should probably end in '.md', but is '{self.config.listings_file}'")

    # https://www.mkdocs.org/dev-guide/plugins/#on_page_content
    def on_page_content(self, html: str, page: Page, config: MkDocsConfig, files) -> None:
        listings = []
        soup = BeautifulSoup(html, "html.parser")

        for pre in soup.findAll('pre'):
            if is_code_listing(pre):
                listings.append(str(pre))

        if listings:
            page_url = page.abs_url or page.canonical_url or f"{config.site_url or ''}/{page.url}"
            self.page_data.append(PageData(
                page_name=page.title or "Untitled page",
                page_url=page_url,
                listings=listings,
            ))

    def on_post_build(self, config: MkDocsConfig):
        # We write the data in post-build -> listings should not be re-indexed and all pages were processed
        path = os.path.join(config.site_dir, self.config.listings_file).removesuffix(".md")
        if config.use_directory_urls:
            path = os.path.join(path, "index.html")
        else:
            path += ".html"

        with open(path, "r") as f:
            html = f.read()

        html = html.replace(self.config.placeholder, self.get_listings_html())

        with open(path, "w") as f:
            f.write(html)


    def get_listings_html(self) -> str:
        html = ""

        for p in self.page_data:
            html += f'<h2><a href="{p.page_url}">{escape(p.page_url)} - {escape(p.page_name)}</a></h2>'
            for listing in p.listings:
                html += listing

        return html