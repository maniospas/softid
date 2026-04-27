from builder.core import Entry, tool
from urllib.parse import urlparse


@tool
def add_readme(entry: Entry):
    """adds main/README.md to the urls of the entry"""
    prev_urls = list(entry.urls)
    for url in prev_urls:
        if url.endswith(".git"): url = url[:-4]
        parsed = urlparse(url)
        if parsed.netloc != "github.com": continue
        parts = parsed.path.strip("/").split("/")
        entry.urls.append(f"https://raw.githubusercontent.com/{parts[0]}/{parts[1]}/HEAD/README.md")

@tool
def add_license(entry: Entry):
    """adds main/LICENSE to the urls of the entry"""
    prev_urls = list(entry.urls)
    for url in prev_urls:
        if url.endswith(".git"): url = url[:-4]
        parsed = urlparse(url)
        if parsed.netloc != "github.com": continue
        parts = parsed.path.strip("/").split("/")
        entry.urls.append(f"https://raw.githubusercontent.com/{parts[0]}/{parts[1]}/HEAD/LICENSE")