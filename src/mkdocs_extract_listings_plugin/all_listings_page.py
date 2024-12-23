import os
from html import escape

# pip
from mkdocs.config.defaults import MkDocsConfig
# local
from .page_processor import PageData
from . import ListingsConfig


def update_all_listings_page(page_data_list: list[PageData], plugin_config: ListingsConfig, config: MkDocsConfig) -> None:
    # We write the data in post-build -> listings should not be re-indexed and all pages were processed
    if plugin_config.listings_file:
        path = os.path.join(config.site_dir, plugin_config.listings_file)
        path = markdown_path_to_html_path(config, path)

        with open(path, "r") as f:
            html = f.read()

        listings_html_content = get_listings_html(page_data_list, plugin_config, config, plugin_config.listings_file)
        html = html.replace(plugin_config.placeholder, listings_html_content)

        with open(path, "w") as f:
            f.write(html)


def get_listings_html(page_data_list: list[PageData], plugin_config: ListingsConfig, config: MkDocsConfig, relative_path_to_markdown_file: str) -> str:
    html = ""
    if plugin_config.default_css:
        html += '<style>a.url { color: gray; font-size: small; display: block; }</style>'

    path_to_base_url = "../" * relative_path_to_markdown_file.count("/")
    if config.use_directory_urls:
        path_to_base_url += "../"
    for p in page_data_list:
        relative_path = p.page_url

        html += f'<h2><a class="heading" href="{escape(path_to_base_url + relative_path)}">{escape(p.page_name)}</a></h2>'
        html += f'<a class="url" href="{escape(path_to_base_url + relative_path)}">{escape(relative_path)}</a>'
        for listing in p.listings:
            html += listing.html

    return html


def markdown_path_to_html_path(config: MkDocsConfig, markdown_path: str) -> str:
    if markdown_path.endswith(".md"):
        path_without_extension = markdown_path[:-3]
        if config.use_directory_urls:
            file_name = os.path.basename(markdown_path)
            if file_name == "index.md":
                return f"{path_without_extension}.html"
            else:
                return os.path.join(path_without_extension, "index.html")
        else:
            return f"{path_without_extension}.html"
    else:
        return markdown_path

