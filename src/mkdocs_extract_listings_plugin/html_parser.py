from typing import NamedTuple
# pip
from bs4 import BeautifulSoup

# local
from . import logger

class ListingData(NamedTuple):
    text: str
    html: str
    language: str # empty string if not set


def parse_listings_from_html(html: str) -> list[ListingData]:
    listings = []
    soup = BeautifulSoup(html, "html.parser")

    for pre in soup.findAll('pre'):
        if is_code_listing(pre):
            listings.append(ListingData(
                text=pre.get_text(),
                html=str(pre),
                language=get_code_listing_language(pre),
            ))
    return listings


def is_code_listing(pre_node) -> bool:
    try:
        for child in pre_node.children:
            if child.name == "code":
                return True
        return False
    except KeyError:
        # No children -> no code listing
        return False


def get_code_listing_language(pre) -> str:
    language = "" # empty = no language, the default
    parent_with_highlight = pre.find_parent("div", class_="highlight")
    if parent_with_highlight:
        for class_ in parent_with_highlight.attrs.get("class", []):
            if class_.startswith("language-"):
                if language:
                    logger.warn("[Warn] Multiple languages in class list:", parent_with_highlight.attrs.get("class", []))
                    # Exit early, so that we do not show the message multiple times
                    return language
                else:
                    language = class_.replace("language-", "", 1)
    else:
        # Check if it is a mermaid diagram
        for class_ in pre.attrs.get("class", []):
            if class_ == "mermaid":
                language = "mermaid"
    
    return language

