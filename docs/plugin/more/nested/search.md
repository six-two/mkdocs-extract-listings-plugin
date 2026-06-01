# More Nested Search Page

Search here:

<div id="listing-extract-search"></div>

<script>
(() => {
const scriptElement = document.createElement("script");
const jsLink = "../../some-path/listing-search.js";

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
