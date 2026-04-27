# SoftId

A repo for building software indexing pipelines.

⚡ Quickstart

Clone and install dependencies in a new Python
virtual environment. Example in Linux with *pip*:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then create files that catalogue various software.
These should be in formats like below, with any
number of owners or associated websites. For this
repository, such catalogues are found in *lists/*.
You can have multiple software per list file, and
use `%` at the start of a line to denote it as comments.

```md
# name
owner@email
page.site
```

Then, parse all considered lists with code like
below, which is also contained in *main.py*. The 
processing consists of loading all software
entries from the lists and then applying
several steps pipeline steps (defined in *tools/*
and registered via decorators like `@tool`) that 
end up creating an html representation to be 
placed within template html files. See code
for details.

```python
# main.py
from builder.core import show_pipeline, process, shared_config
from builder.loader import load
from builder import tools # needed to register all tools


if __name__ == "__main__":
    #shared_config["retry_cache"] = True
    list_paths = ["lists/biodata_group.txt", "lists/mever_group.txt"]
    pipeline = [
        "builder.tools.format.bulma.banner",
        "builder.tools.github.add_readme",
        "builder.tools.github.add_license",
        "builder.tools.generic.cache",
        "builder.tools.generic.get_md",
        "builder.tools.format.bulma.sections",
        "builder.tools.format.bulma.container",
    ]
    show_pipeline(pipeline)
    entries = list()
    for list_path in list_paths:
        entries.extend(load(list_path))
    text = process(entries, pipeline)

    with open("builder/tools/format/bulma_template.html") as file:
        template = file.read()
    with open("export.html", "w") as file:
        file.write(template.replace("{{CONTENTS}}", text))
```

Run `python -m main.py` and you will obtain a file
*export.html*. The script starts by printing
pipeline information, like below.

```text
┌──────────────────────────────────────────────────────────────┐
│ builder.tools.format.bulma.banner: constructs a banner using │
│ the entry's name and the urls as tags                        │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ builder.tools.github.add_readme: adds main/README.md to the  │
│ urls of the entry                                            │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ builder.tools.github.add_license: adds main/LICENSE to the   │
│ urls of the entry                                            │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ builder.tools.generic.cache: uses a cache of downloadable    │
│ content that persists across runs                            │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ builder.tools.generic.get_md: gathers all .md file contents  │
│ as sections (these are not yet added to html results)        │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ builder.tools.format.bulma.sections: moves all current       │
│ sections to html contents                                    │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ builder.tools.format.bulma.container: adds all generated     │
│ content in the form of a boxed entry with appropriate id -   │
│ should be the last step                                      │
└──────────────────────────────────────────────────────────────┘
```


📜 License

Apache 2.0
