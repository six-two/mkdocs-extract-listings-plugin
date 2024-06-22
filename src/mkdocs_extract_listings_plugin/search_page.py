import json
import os
from urllib.parse import urlparse
# pip
from mkdocs.config.defaults import MkDocsConfig
# local
from . import SCRIPT_DIR
from .page_processor import PageData


def write_javascript_file(page_data_list: list[PageData], plugin_config, config: MkDocsConfig) -> None:
    dst_path = os.path.join(config.site_dir, plugin_config.javascript_search_file)
    dst_path_parent = os.path.dirname(dst_path)
    if not os.path.exists(dst_path_parent):
        os.makedirs(dst_path_parent)

    src_path = os.path.join(SCRIPT_DIR, "listing-search.js")
    with open(src_path, "r") as f:
        js = f.read()

    if plugin_config.default_css:
        with open(os.path.join(SCRIPT_DIR, "default.css")) as f:
            css = f.read()
        js = js.replace("STYLE=``;", f"STYLE=`{css}`;")

    # We traverse from the JSON file up to the root directory
    path_to_root = "../" * plugin_config.javascript_search_file.count("/")
    if plugin_config.offline:
        json_data = get_json_data(page_data_list, path_to_root)
        js = js.replace("OFFLINE_JSON_DATA=null;", f"OFFLINE_JSON_DATA={json.dumps(json_data)};")
    else:
        write_json_file(page_data_list, plugin_config, config, path_to_root)

    if config.site_url:
        path = urlparse(config.site_url).path
        # Remove trailing trashes
        while path.endswith("/"):
            path = path[:-1]

        if path:
            # Path contains something else than just slashes
            js = js.replace('BASE_URL=""', f'BASE_URL="{path}"')

    with open(dst_path, "w") as f:
        f.write(js)


def write_json_file(page_data_list: list[PageData], plugin_config, config: MkDocsConfig, url_prefix: str) -> None:
    # We use a relative path to the script file (script file + ".json" extension)
    dst_path = os.path.join(config.site_dir, plugin_config.javascript_search_file) + ".json"
    json_data = get_json_data(page_data_list, url_prefix)
    with open(dst_path, "w") as f:
        json.dump(json_data, f, indent=2)


def get_json_data(page_data_list: list[PageData], url_prefix: str) -> list[dict]:
    json_data = []
    for page in page_data_list:
        for listing in page.listings:
            json_data.append({
                "page_name": page.page_name,
                "page_url": url_prefix + page.page_url,
                "text": listing.text,
                "html": listing.html,
                "language": listing.language,
            })

    return json_data
