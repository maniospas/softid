from builder.core import Entry, tool, shared_config
import re
import os
import markdown

@tool
def cache(entry: Entry):
    """uses a cache of downloadable content that persists across runs"""
    os.makedirs("./.cache", exist_ok=True)
    for url in entry.urls:
        safe_name = re.sub(r'[^\w]', '_', url)[:200]
        cache_path = os.path.join("./.cache", safe_name)
        if os.path.exists(cache_path):
            #print("using cached url", url)
            with open(cache_path, "r", encoding="utf-8") as f:
                entry._cached_contents[url] = f.read()
            if not shared_config.get("retry_cache", False): continue
            if entry._cached_contents[url]: continue
            del entry._cached_contents[url]
        print("downloading url", url)
        text = entry.download(url)
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(text)

def to_markdown(text: str):
    return markdown.markdown(text, extensions=["fenced_code", "codehilite"])

HASH_PLACEHOLDER = "\x00HASH\x00"
def _mask_code_blocks(text: str) -> str:
    """Replace # with placeholder inside fenced code blocks."""
    def replace_hashes(m):
        return m.group(0).replace('#', HASH_PLACEHOLDER)
    return re.sub(r'(?ms)^```.*?^```', replace_hashes, text)

def _unmask_code_blocks(text: str) -> str:
    return text.replace(HASH_PLACEHOLDER, '#')

@tool
def get_md(entry: Entry):
    """gathers all .md file contents as sections (these are not yet added to html results)"""
    for url in entry.urls:
        if not url.endswith(".md"): continue
        text = entry.download(url)
        if not text: continue
        masked = _mask_code_blocks(text)
        parts = re.split(r'(?m)^(#+\s.+)$', masked)
        if len(parts) == 1:
            content = to_markdown(_unmask_code_blocks(masked))
            entry.section("#Description", [content])
            continue
        pre_content = parts[0].strip()
        if pre_content:
            pre_content = to_markdown(_unmask_code_blocks(pre_content))
            entry.section("#Description", [pre_content])
        for i in range(1, len(parts) - 1, 2):
            title = re.sub(r'^#+\s', '', parts[i]).strip()
            #print(title.lower().replace("-",""), entry.name.lower().replace("-",""))
            if title.lower().replace("-","").strip() == entry.name.lower().replace("-","").strip(): title = "#Description"
            else: title = to_markdown(_unmask_code_blocks(title))
            content = parts[i + 1].strip()
            content = to_markdown(_unmask_code_blocks(content))
            if content:
                entry.section(title, [content])

@tool
def iframe(entry: Entry):
    """embeds all urls as iframes"""
    for url in entry.urls:
        entry.contents += f'<iframe style="width:100%;height:500px" src="{url}" title="{url}"></iframe>\n'


@tool
def remove_section_images(entry: Entry):
    """removes images from section html"""
    img_pattern = re.compile(r'<img[^>]*>')
    for section in entry.unparsed_sections.values():
        for i, content in enumerate(section):
            section[i] = img_pattern.sub('', content)