# builtin
import os
from typing import NamedTuple
from html import escape
import json
from urllib.parse import urlparse
# pip
from mkdocs.config.config_options import Type
from mkdocs.config.base import Config
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.pages import Page
from mkdocs.config.defaults import MkDocsConfig
from bs4 import BeautifulSoup

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class ListingsConfig(Config):
    listings_file = Type(str, default="")
    placeholder = Type(str, default="PLACEHOLDER_LISTINGS_PLUGIN")
    javascript_search_file = Type(str, default="")


def is_code_listing(pre_node) -> bool:
    try:
        for child in pre_node.children:
            if child.name == "code":
                return True
        return False
    except KeyError:
        # No children -> no code listing
        return False


class ListingData(NamedTuple):
    text: str
    html: str


class PageData(NamedTuple):
    page_name: str
    page_url: str
    listings: list[ListingData]


class ListingsPlugin(BasePlugin[ListingsConfig]):
    def __init__(self) -> None:
        super().__init__()
        self.page_data: list[PageData] = []
        self.logger = get_plugin_logger(__name__)

    def on_pre_build(self, config: MkDocsConfig) -> None:
        # Reset before every build -> prevent duplicate entries when running mkdocs serve
        self.page_data = []

        if self.config.listings_file:
            listings_file = os.path.join(config.docs_dir, self.config.listings_file)
            if not os.path.isfile(listings_file):
                raise PluginError(f"'listings_file' does not reference a valid Markdown file: '{listings_file}' does not exist")
            elif not self.config.listings_file.endswith(".md"):
                self.logger.warning(f"Value for 'listings_file' should probably end in '.md', but is '{self.config.listings_file}'")
        else:
            if not self.config.javascript_search_file:
                self.logger.warning("Neither 'javascript_search_file' nor 'listings_file' are set -> This plugin will do nothing. Please check the setup instructions at https://github.com/six-two/mkdocs-extract-listings-plugin/blob/main/README.md")

    # https://www.mkdocs.org/dev-guide/plugins/#on_page_content
    def on_page_content(self, html: str, page: Page, config: MkDocsConfig, files) -> None:
        listings = []
        soup = BeautifulSoup(html, "html.parser")

        for pre in soup.findAll('pre'):
            if is_code_listing(pre):
                listings.append(ListingData(
                    text=pre.get_text(),
                    html=str(pre),
                ))

        if listings:
            page_url = page.abs_url or page.canonical_url or f"{config.site_url or ''}/{page.url}"
            self.page_data.append(PageData(
                page_name=page.title or "Untitled page",
                page_url=page_url,
                listings=listings,
            ))

    def on_post_build(self, config: MkDocsConfig) -> None:
        self.update_all_listings_page(config)

        if self.config.javascript_search_file:
            self.write_javascript_file(config)
            self.write_json_file(config)

    def update_all_listings_page(self, config: MkDocsConfig) -> None:
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

    def write_json_file(self, config: MkDocsConfig) -> None:   
        json_data = []
        for page in self.page_data:
            for listing in page.listings:
                json_data.append({
                    "page_name": page.page_name,
                    "page_url": page.page_url,
                    "text": listing.text,
                    "html": listing.html,
                })
        
        with open(os.path.join(config.site_dir, "extract-listings.json"), "w") as f:
            json.dump(json_data, f, indent=2)


    def write_javascript_file(self, config: MkDocsConfig) -> None:
        dst_path = os.path.join(config.site_dir, self.config.javascript_search_file)
        dst_path_parent = os.path.dirname(dst_path)
        if not os.path.exists(dst_path_parent):
            os.makedirs(dst_path_parent)
        
        src_path = os.path.join(SCRIPT_DIR, "listing-search.js")
        with open(src_path, "r") as f:
            js = f.read()

        if config.site_url:
            path = urlparse(config.site_url).path
            # Remove trailing trashes
            while path.endswith("/"):
                path = path[:-1]

            # Fix duplicate slashes (no idea why it happens)
            path = path.replace("//", "/")

            if path:
                # PAth contains something else than just slashes
                js = js.replace('BASE_URL=""', f'BASE_URL="{path}"')
                # self.logger.info(f"Set baseurl to {path}")

        with open(dst_path, "w") as f:
            f.write(js)

    def get_listings_html(self) -> str:
        html = ""

        for p in self.page_data:
            html += f'<h2><a href="{p.page_url}">{escape(p.page_url)} - {escape(p.page_name)}</a></h2>'
            for listing in p.listings:
                html += listing.html

        return html
