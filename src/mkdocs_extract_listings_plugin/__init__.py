# builtin
import html
import os
# pip
from mkdocs.config.config_options import Choice, Type, ListOfItems
from mkdocs.config.base import Config
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.nav import Navigation
from mkdocs.structure.files import Files, File, InclusionLevel
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
    default_search_mode = Choice(["substr", "substr-i", "words", "words-i", "glob", "glob-i", "fuzzy"], default="substr-i")
    # Add page options
    search_page_path = Type(str, default="") # append search snippet to the given page if this option is set
    search_page_create_if_missing = Type(bool, default=False) # if the page does not exist, create it and add it to the nav
    search_page_section_name = Type(str, default="Code Snippet Search") # the title of the page or section to create


# local
from .page_processor import PageProcessor
from .all_listings_page import update_all_listings_page
from .search_page import write_javascript_file, get_javascript_file_source_code


class ListingsPlugin(BasePlugin[ListingsConfig]):
    def on_config(self, config: MkDocsConfig) -> None:
        self.page_processor = PageProcessor(self.config)
        # Make sure that it is a relative path to the docs dir
        self.search_page_path = self.config.search_page_path.lstrip("/")

        # Handle and sanitize the section name
        self.search_page_section_name = search_page_section_name = self.config.search_page_section_name

        # Handle leading or trailing whitespace
        search_page_section_name = search_page_section_name.strip()
        if search_page_section_name != self.search_page_section_name:
            logger.warning("search_page_section_name contained leading or trailing spaces, which have been removed")
            self.search_page_section_name = search_page_section_name

        # Handle leading hashtags (section indications)
        search_page_section_name = search_page_section_name.lstrip("#").lstrip()
        if search_page_section_name != self.search_page_section_name:
            logger.warning("search_page_section_name contained leading hashtags which have been removed. It should only contain the name of the section or page, not the full section title markdown")
            self.search_page_section_name = search_page_section_name

        # Handle line breaks
        search_page_section_name = search_page_section_name.replace("\n", "").replace("\r", "")
        if search_page_section_name != self.search_page_section_name:
            logger.warning("search_page_section_name contained line breaks, which have been removed")
            self.search_page_section_name = search_page_section_name


    def on_files(self, files: Files, config: MkDocsConfig) -> Files:
        # It would probably be smart adding the file here, but it would likely make the logic more complicated.
        # Since adding the file in on_nav works too, I will keep it that way for now
        return files

    def on_nav(self, nav: Navigation, config: MkDocsConfig, files: Files) -> Navigation:
        if self.config.search_page_path:
            search_page_exists_in_file_system = os.path.exists(os.path.join(config.docs_dir, self.search_page_path))

            # Look in the existing pages for one with the same path
            search_page = None
            for page in nav.pages:
                if page.file.src_uri == self.search_page_path:
                    search_page = page
                    break
            
            if search_page_exists_in_file_system:
                if search_page:
                    # We found our page, so everything is good
                    pass
                else:
                    logger.warning(f"Search page {self.search_page_path} exists, but is not in the navigation. This may hide it from users.")
            else:
                if self.config.search_page_create_if_missing:
                    # If we need to create the search page, we need to add a virtual page with no markdown file on disk.
                    # Since I remembered, that the print page plugin (https://github.com/timvink/mkdocs-print-site-plugin/blob/master/src/mkdocs_print_site_plugin/plugin.py) does exactly that,
                    # I based my implementation roughly on how it is done there and on some info/comments from MkDocs's source code

                    # Create a blank missing page
                    file = File.generated(config, self.search_page_path, content="", inclusion=InclusionLevel.INCLUDED)
                    page = Page(self.search_page_section_name, file, config)
                    page.edit_url = None # Not sure why, but saw it here: https://github.com/timvink/mkdocs-print-site-plugin/blob/master/src/mkdocs_print_site_plugin/plugin.py

                    # Add it to the end of the navigation
                    nav.items.append(page)
                    nav.pages.append(page)
                    files.append(file)
                else:
                    logger.warning(f"Search page {self.search_page_path} does not exist and the plugin will not create it. Either set 'search_page_create_if_missing' to 'true' or manually create the page")
            
        return nav

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

    def on_page_markdown(self, markdown, page: Page, config: MkDocsConfig, files: Files) -> str:
        if page.file.src_uri == self.search_page_path:
            # This is the search page where we need to add our new file
            js_script_src = get_relative_path_from(page, self.config.javascript_search_file)
            section_content_html = f'\n\n<div id="listing-extract-search"></div>\n<script src="{html.escape(js_script_src)}"></script>\n\n'
            # This is the page we need to update
            if markdown.strip():
                # The page already contains something, so we add a new subsection
                markdown += f'\n\n## {self.search_page_section_name}\n{section_content_html}'
            else:
                markdown = f'# {self.search_page_section_name}\n{section_content_html}'

        return markdown


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


def get_relative_path_from(current_page: Page, absolute_destination_link: str) -> str:
    level = current_page.url.count("/")
    relative_url = ("../" * level) + absolute_destination_link
    return relative_url
    
