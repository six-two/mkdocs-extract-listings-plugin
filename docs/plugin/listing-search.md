---
hide:
- toc
---

# Listing search

This page has a search function for all listings.

<div id="listing-extract-search" data-searchmode="words"></div>

<!-- This should work for all builds (hopefully) -->
<script>
(() => {
const scriptElement = document.createElement("script");
const jsLink = "some-path/listing-search.js";

if (location.pathname.endsWith("/") || location.pathname.endsWith("/index.html")) {
    // use_directory_urls: true
    scriptElement.src = "../../" + jsLink;
} else {
    // use_directory_urls: false
    scriptElement.src = "../" + jsLink;
}

document.head.append(scriptElement);
})();
</script>
