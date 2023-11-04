# mkdocs-extract-listings-plugin

A small plugin to extract all your listings and put them in a single page.
Might for example be useful if the search plugin makes it hard finding a code snippet you want to find (or you disabled the search).
Just open the page with all listings and use the `Find in page` function.

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

3. Add a Markdown file for the page that will be filled with all the listings.
    In that file add the placeholder where the listings should be inserted.
    The default configuration expects a file named `listings.md` in your `docs` folder, which contains the placeholder `PLACEHOLDER_LISTINGS_PLUGIN`.
    This can be changed, see details in the following section.

## Configuration

You can configure the plugin like this:
```yaml
- extract_listings:
    listings_file: listings.md
    placeholder: PLACEHOLDER_LISTINGS_PLUGIN
```

### listings_file

`listings_file` is expected to contain the relative path to the Markdown file, where the listings should be written to.
If the file does not exist, an error will be raised during the build process.
The default value the string `listings.md`.

### placeholder

The value for `placeholder` will be searched in the file referenced by `listings_file` and be replaced with the list of all listings.


## Changelog

### Version 0.0.2

- Fixed `Unknown path` being shown on with different themes (`readthedocs` and `material`)
