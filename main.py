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