from builder.core import Entry, tool
from urllib.parse import urlsplit
import re

@tool
def banner(entry: Entry):
    """constructs a banner using the entry's name and the urls as tags"""
    if "stars" in entry.metadata:
        stars = f'&nbsp;<span style="float:right">{entry.metadata.get("stars")} ⭐</span>'
    else:
        stars = ""
    entry.contents += f'<h2 class="title">{entry.name}{stars}\n'
    entry.contents += ''
    found_tags = set()
    for url in entry.urls:
        try:
            name = urlsplit(url).netloc.split('.')[-2]
            if name in found_tags: continue
            found_tags.add(name)
            entry.contents += f'<span style="float:right" class="tag is-link is-light"><a href="{url}">🏠 {name}</a></span>\n'
        except Exception: pass
    if entry.owners:
        entry.contents += f'<span style="float:right" class="tag is-warning is-light"><a href="mailto:{entry.owners[0]}">🖂 {entry.owners[0]}</a></span>\n'
    entry.contents += "</h2>\n"

@tool
def keywords(entry: Entry, top:int=8):
    """adds the top keywords as tags"""
    if not entry.keywords: return
    entry.contents += '<div class="tags">'
    for k, v in sorted(entry.keywords.items(), key=lambda x: x[1], reverse=True)[:min(top, len(entry.keywords))]:
        entry.contents += f'<span class="tag is-primary is-light">{k}</span>\n'
    entry.contents += "</div>\n"

def shorter(item: str):
    clean = re.sub(r'<[^>]+>', '', item)
    first_pos = 140
    if len(clean) <= first_pos:
        return clean
    return clean[:first_pos].strip() + '...'

@tool
def sections(entry: Entry):
    """moves all current sections to html contents"""
    contents = '<div>'+"\n".join((desc) for desc in entry.unparsed_sections.get('#Description', ""))+'</div>\n'
    for k ,v in entry.unparsed_sections.items():
        if k.startswith('#'): continue
        contents += f'<h5 class="subtitle is-4 mt-5">{k}</h5>\n'
        for item in v:
            contents += f'<div>{(item)}</div>\n'
    contents = '<div style="max-height:300px; overflow-y:auto">'+contents+'</div>'
    entry.contents += contents
    entry.unparsed_sections = dict()

@tool
def short_sections(entry: Entry):
    """moves a previoew of all current sections to html contents"""
    contents = '<div>'+"\n".join(shorter(desc) for desc in entry.unparsed_sections.get('#Description', ""))+'</div>\n'
    contents += "<table>\n"
    for k ,v in entry.unparsed_sections.items():
        if not k or k.startswith('#'): continue
        contents += f'<tr><td><b>{shorter(k).strip("# ")}</b>&nbsp;&nbsp;</td>\n'
        if v: contents += "<td>"+shorter(v[0])+"</td>"
        contents += "</tr>"
    contents += "</table>\n"
    contents = '<div>'+contents+'</div>'
    entry.contents += contents
    entry.unparsed_sections = dict()

@tool
def container(entry: Entry):
    """adds all generated content in the form of a boxed entry with appropriate id - should be the last step"""
    entry.contents = f'<div class="cell p-2 mt-5 mb-5" id="{entry.normal_name()}"><article class="box">{entry.contents}</article></div>\n'