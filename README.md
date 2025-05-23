# mkdocs-extract-listings-plugin

A small plugin to extract all your listings and put them in a single page.
It can also generate a search function of code listings with different search methods (fuzzy match, substring, contains words).

## Demo

You can try out the demo at <https://mkdocs-extract-listings-plugin.six-two.dev>.
It is configured to offer both the search and all listings pages an uses the plugin with some common MkDocs themes (mkdocs, readthedocs, and material).
The source for this demo is also in this repo (`mkdocs.yml`, `docs/` and `build.sh`).

## Setup

1. Install the plugin using pip:

    ```bash
    pip install mkdocs-extract-listings-plugin
    ```

2. Add the plugin to your `mkdocs.yml`:

    ```yaml
    plugins:
    - search
    - extract_listings
    ```

    > If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set.

    More information about plugins in the [MkDocs documentation](http://www.mkdocs.org/user-guide/plugins/).

3. Configure a page with all listings, a page with listing search, or both (see below).
4. Optional: To properly detect which language a listing belongs to, you may have to add the following to your `mkdocs.yml` as described in the [Material for MkDocs page on code blocks](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/):
    ```yaml
    markdown_extensions:
    - pymdownx.highlight:
        anchor_linenums: true
        line_spans: __span
        pygments_lang_class: true
    - pymdownx.inlinehilite
    - pymdownx.snippets
    - pymdownx.superfences
    ```


### Listing page

Add a Markdown file for the page that will be filled with all the listings.
In that file add the placeholder where the listings should be inserted.
Then reference that file and specify the placeholder like this in your `mkdocs.yml`:
```yaml
plugins:
- extract_listings:
    listings_file: listings.md
    placeholder: PLACEHOLDER_LISTINGS_PLUGIN
```

### Listing search

#### Via mkdocs.yml

This is the simplest way and is recommended for most users:

1. Set `search_page_path` in your plugin settings to either a page path (it can already exist, but does not need to):
    ```yaml
    plugins:
    - extract_listings:
        search_page_path: plugin/index.md
    ```
2. If the page does not exist and should be added by the plugin, then enable `search_page_create_if_missing`:
    ```yaml
    plugins:
    - extract_listings:
        search_page_path: plugin/index.md
        search_page_create_if_missing: True
    ```

It the page already exists, then a new section with the search box and results will be added.
If it does not exist and should be created, then a page containing only the search box and results will be created.

#### Manual

This is more complicated to set up, but you have more control about the page:

1. Create a page, which should contain the search function.
2. Add a tag where the search elements should be inserted and load the search script:
    ```markdown
    <div id="listing-extract-search"></div>
    <script src="/listing-search.js" async></script>
    ```
3. Specify where you want the plugin to write the script file to.
This should match the path you used in the previous step.
    In `mkdocs.yml`:

    ```yaml
    plugins:
    - extract_listings:
        javascript_search_file: listing-search.js
    ```

I recommend using an absolute path for the `script.src` attribute, since it will keep working after moving the page or after switching between directory URLs and non directory URLs pages.
It just runs into problems when your base directory (where the page is deployed) is not the root directory or when you are using offline mode (from `file://` URLs).

Alternatively you can include the script and the data inline, but this can have tiny performance drawbacks:

- If you include it on multiple pages, all of them will contain a copy of the data -> reduces caching efficiency
- The whole search database needs to be downloaded while your page is loading (can not use `async` or `defer` script attributes).

## Configuration

You can configure the plugin like this:
```yaml
plugins:
- extract_listings:
    listings_file: listings.md
    placeholder: PLACEHOLDER_LISTINGS_PLUGIN
    javascript_search_file: listing-search.js
    default_css: true
    offline: false
    default_search_mode: substr-i
    exclude_language_list:
    - python
    - bash
    search_page_path: ""
    search_page_create_if_missing: false
    search_page_section_name: Code Snippet Search

```

### default_css

`default_css` determines, whether the search JavaScript should also load the default styling for the search dialog and results.
By default it is set to `true`, but you can set it to `false` if the theme you use does not work well with the style.
You should then define your own custom style and include it on the search page.
Also has some effect on the all listings page.

### listings_file

`listings_file` is expected to contain the relative path to the Markdown file, where the listings should be written to.
If the file does not exist, an error will be raised during the build process.
The default value is empty.

### placeholder

The value for `placeholder` will be searched in the file referenced by `listings_file` and be replaced with the list of all listings.

### javascript_search_file

The JavaScript code for the search function will be written to this path.
The default value is empty, meaning that neither the JSON file nor the JavaScript are generated.

### offline

When set to `true` the listing data is included into the JavaScript file.
This way it can be used even when the site if opened from the file system (via a `file://` URL).
The disadvantage is that the loading of the script will take longer and the data is not loaded asynchronously, so the loading of the page via the Internet will be delayed.
Because of that it is set to `false` by default.

### exclude_language_list

Ignore any listings that are in the given languages.
They will not appear on the all listings page or in the listings search.

### default_search_mode

The default search mode to use for all search pages.
This can be overwritten by the `data-searchmode` as shown below for individual search boxes.

### search_page_path

Insert a search box and results on this page.
This allows you to use the plugin without needing to modify the Markdown files in your `docs` directory.

### search_page_create_if_missing

If the page specified by `search_page_path` does not exist, then create it and add it to the navigation.

### search_page_section_name

The name of the section (if page exists) or the page title (if the page was newly created) that will be added to the page specified by `search_page_path`.

### Search mode

You can set the search mode via the `data-searchmode` attribute:
```html
<div id="listing-extract-search" data-searchmode="substr"></div>
```

To see all current valid values inspect the search type dropdown menu using your browser's developer tools.
The data in the `value` attribute is the value you should put in the attribute:

![Firefox's Developer tools](docs/show-search-modes.png)

Alternatively you can put in a random value and will receive an warning message in the developer tools, that also lists the valid values (but without descriptions).


## Changelog

### Version 0.2.1

- Use a default value for `javascript_search_file`.
- Fixed DeprecationWarning: Replaced `bs4.findAll` with `bs4.find_all`.

### Version 0.2.0

- Added `search_page_path`, `search_page_create_if_missing` and `search_page_section_name` settings, which allow adding a search page without touching any Markdown files
- Added inline placeholder search mode: Use `PLACEHOLDER_INLINE_LISTINGS_SEARCH_PLUGIN` in a page to include the script and listings database inline into it.
- Fixed issues with sites using an non-root base directory (`site_url` property in `mkdocs.yml`).
- Added `default_search_mode` setting, which allows to set the default search mode.
- Added `glob` and `glob-i` search modes.

### Version 0.1.3

- Added `exclude_language_list` option which excludes listings in the given languages from the search
- Correctly recognize `mermaid` language when using MkDocs for Material
- Hide the language selector when only one language exists

### Version 0.1.2

- Added a dropdown to filter snippets by language.

### Version 0.1.1

- Fix: Links incorrect if search page is not in the root directory.

### Version 0.1.0

- The plugin should now be able to work when served from `file://` URLs:
    - Search JSON can be inlined to the script via `offline: true` setting.
    - Use relative links on the `listings_file` page.
- Improved the search code:
    - Allow users to specify which matching mode the search uses by default.
    - Added mode `Contains words (case insensitive)`.
- Fixed crash when using `use_directory_urls: false` and not setting `listings_file`.

### Version 0.0.4

- Added styling for the search page and the option `default_css` to disable it.
- Fixed bug: URL for index pages starts with `//`

### Version 0.0.3

- Added snippet search JavaScript and JSON file.
- Changed default for `listings_file` to empty string.

### Version 0.0.2

- Fixed `Unknown path` being shown on with different themes (`readthedocs` and `material`)
