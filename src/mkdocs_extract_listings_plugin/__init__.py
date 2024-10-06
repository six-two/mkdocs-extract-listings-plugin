# builtin
import os
# pip
from mkdocs.config.config_options import Type, ListOfItems
from mkdocs.config.base import Config
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.pages import Page
from mkdocs.config.defaults import MkDocsConfig

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
logger = get_plugin_logger(__name__)


class ListingsConfig(Config):
    listings_file = Type(str, default="")
    placeholder = Type(str, default="PLACEHOLDER_LISTINGS_PLUGIN")
    default_css = Type(bool, default=True)
    offline = Type(bool, default=False)
    javascript_search_file = Type(str, default="")
    exclude_language_list = ListOfItems(Type(str), default=[])


# local
from .page_processor import PageProcessor
from .all_listings_page import update_all_listings_page
from .search_page import write_javascript_file, get_javascript_file_source_code


class ListingsPlugin(BasePlugin[ListingsConfig]):
    def on_config(self, config: MkDocsConfig) -> None:
        self.page_processor = PageProcessor(self.config)

    def on_pre_build(self, config: MkDocsConfig) -> None:
        # Reset before every build -> prevent duplicate entries when running mkdocs serve
        self.page_processor.clear()

        if self.config.listings_file:
            if os.path.isabs(self.config.listings_file):
                raise PluginError(f"'listings_file' can not be an absolute path: ${self.config.listings_file}")

            listings_file = os.path.join(config.docs_dir, self.config.listings_file)
            if not os.path.isfile(listings_file):
                raise PluginError(f"'listings_file' does not reference a valid Markdown file: '{listings_file}' does not exist")
            elif not self.config.listings_file.endswith(".md"):
                logger.warning(f"Value for 'listings_file' should probably end in '.md', but is '{self.config.listings_file}'")
        else:
            if not self.config.javascript_search_file:
                logger.warning("Neither 'javascript_search_file' nor 'listings_file' are set -> This plugin will do nothing, unless you use inline placeholder replacement. Please check the setup instructions at https://github.com/six-two/mkdocs-extract-listings-plugin/blob/main/README.md")

    # https://www.mkdocs.org/dev-guide/plugins/#on_page_content
    def on_page_content(self, html: str, page: Page, config: MkDocsConfig, files) -> None:
        self.page_processor.process_page(html, page)

    # https://www.mkdocs.org/dev-guide/plugins/#on_post_page
    def on_post_page(self, output: str, page: Page, config: MkDocsConfig) -> str:
        if "PLACEHOLDER_INLINE_LISTINGS_SEARCH_PLUGIN" in output:
            # Can not be cached, since script paths are dependent on current page path
            # https://www.mkdocs.org/dev-guide/themes/#page
            # https://www.mkdocs.org/dev-guide/api/#mkdocs.structure.files.File.src_uri
            inline_script_html = '<div id="listing-extract-search"></div>\n<script>\n' + get_javascript_file_source_code(self.page_processor.page_data_list, self.config, True, page.file.src_uri, config) + '\n</script>'
            output = output.replace("PLACEHOLDER_INLINE_LISTINGS_SEARCH_PLUGIN", inline_script_html)
        return output

    def on_post_build(self, config: MkDocsConfig) -> None:
        update_all_listings_page(self.page_processor.page_data_list, self.config, config)

        if self.config.javascript_search_file:
            write_javascript_file(self.page_processor.page_data_list, self.config, config)
