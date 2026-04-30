from builder.core import Entry, tool
from urllib.parse import urlparse
import requests


@tool
def get_stars(entry: Entry):
    """Fetches star count from GitHub API"""
    prev_urls = list(entry.urls)
    for url in prev_urls:
        if url.endswith(".git"):
            url = url[:-4]
        parsed = urlparse(url)
        if parsed.netloc != "github.com":
            continue
        parts = parsed.path.strip("/").split("/")
        if len(parts) < 2:
            continue
        owner, repo = parts[0], parts[1]
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        headers = {}
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            count_stars = data["stargazers_count"]
            if count_stars:
                entry.metadata["stars"] = str(count_stars)

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