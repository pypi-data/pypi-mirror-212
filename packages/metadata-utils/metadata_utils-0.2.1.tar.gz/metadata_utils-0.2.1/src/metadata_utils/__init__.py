# stdlib
import unicodedata
from xml.sax.saxutils import escape
from xml.sax.saxutils import unescape

__VERSION__ = "0.2.1"


# ==============================================================================


# https://wiki.python.org/moin/EscapingHtml
# escape() and unescape() takes care of "&" , "<" and ">"
# we need to handle quotes, so we don't break things
html_attribute_escape_table: dict = {'"': "&quot;", "'": "&apos;"}
html_attribute_unescape_table: dict = {
    v: k for (k, v) in html_attribute_escape_table.items()
}


def html_attribute_escape(text: str) -> str:
    return escape(text, html_attribute_escape_table)


def html_attribute_unescape(text: str) -> str:
    return unescape(text, html_attribute_unescape_table)


def force_clean_ascii_NFKD(text: str) -> bytes:
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore")


def force_clean_ascii_NFKC(text: str) -> bytes:
    return unicodedata.normalize("NFKC", text).encode("ascii", "ignore")
