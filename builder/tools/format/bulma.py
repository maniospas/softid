from builder.core import Entry, tool
from urllib.parse import urlsplit

@tool
def banner(entry: Entry):
    """constructs a banner using the entry's name and the urls as tags"""
    entry.contents += '<div>'
    entry.contents += f'<h1 class="title">{entry.name}</h1>\n'
    entry.contents += '<div class="tags">'
    found_tags = set()
    for url in entry.urls:
        try:
            name = urlsplit(url).netloc.split('.')[-2]
            if name in found_tags: continue
            found_tags.add(name)
            entry.contents += f'<span class="tag is-info is-light mb-5"><a href="{url}">{name}</a></span>\n'
        except Exception: pass
    entry.contents += "</div>\n"
    entry.contents += "</div>\n"

@tool
def sections(entry: Entry):
    """moves all current sections to html contents"""
    entry.contents += "\n".join(entry.unparsed_sections.get('#Description', ""))
    for k ,v in entry.unparsed_sections.items():
        if k.startswith('#'): continue
        entry.contents += f'<h4 class="subtitle is-4 mt-5">{k}</h4>\n'
        for item in v:
            entry.contents += item +"\n"
    entry.unparsed_sections = dict()

@tool
def container(entry: Entry):
    """adds all generated content in the form of a boxed entry with appropriate id - should be the last step"""
    entry.contents = f'<div class="cell p-2 mt-5 mb-5" id="{entry.name}"><article class="box">{entry.contents}</article></div>\n'