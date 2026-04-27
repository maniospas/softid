from builder.core import Entry, tool

@tool
def sections(entry: Entry):
    """moves all current sections to html contents"""
    for k ,v in entry.unparsed_sections.items():
        entry.contents += f'<h3 class="subtitle">{k}</h3>\n'
        for item in v:
            entry.contents += item +"\n"
    entry.unparsed_sections = dict()

@tool
def container(entry: Entry):
    """adds all generated content in the form of a boxed entry with appropriate id - should be the last step"""
    entry.contents = f'<div class="cell" id="{entry.name}"><article class="box">{entry.contents}</article></div>\n'