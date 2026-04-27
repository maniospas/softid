from builder.core import Entry, tool
from urllib.parse import urlsplit
import re
import os

@tool
def banner(entry: Entry):
    """constructs a banner using the entry's name and the urls as tags"""
    entry.contents += "<div>"
    entry.contents += f'<h1 class="title">{entry.name}</h1>\n'
    found_tags = set()
    for url in entry.urls:
        try:
            name = urlsplit(url).netloc.split('.')[-2]
            if name in found_tags: continue
            found_tags.add(name)
            entry.contents += f'<span class="tag is-info is-light"><a href="{url}">{name}</a></span>\n'
        except Exception: pass
    entry.contents += "</div>\n"

@tool
def cache(entry: Entry):
    os.makedirs("./.cache", exist_ok=True)
    for url in entry.urls:
        safe_name = re.sub(r'[^\w]', '_', url)[:200]
        cache_path = os.path.join("./.cache", safe_name)
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                entry._cached_contents[url] = f.read()
            continue
        text = entry.download(url)
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(text)

@tool
def get_md(entry: Entry):
    """gathers all .md file contents as sections (these are not yet added to html results)"""
    for url in entry.urls:
        if not url.endswith(".md"): continue
        text = entry.download(url)
        if not text: continue
        parts = re.split(r'(?m)^(#+\s.+)$', text)
        if len(parts) == 1:
            entry.section("description", [text])
            continue
        pre_content = parts[0].strip()
        if pre_content: entry.section("description", [pre_content])
        for i in range(1, len(parts) - 1, 2):
            title = re.sub(r'^#+\s', '', parts[i]).strip()
            content = parts[i + 1].strip()
            if content:
                entry.section(title, [content])

@tool
def iframe(entry: Entry):
    """embeds all urls as iframes"""
    for url in entry.urls:
        entry.contents += f'<iframe style="width:100%;height:500px" src="{url}" title="{url}"></iframe>\n'
