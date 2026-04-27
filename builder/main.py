from builder.core import show_pipeline
from builder.loader import load
from builder import tools # needed to register all tools


if __name__ == "__main__":
    pipeline = [
        # add extra links
        "builder.tools.github.add_readme",
        "builder.tools.github.add_license",
        "builder.tools.generic.cache",
        # process the card
        "builder.tools.generic.banner",
        "builder.tools.generic.get_md",
        "builder.tools.format.bulma.sections",
        "builder.tools.format.bulma.container",
    ]
    show_pipeline(pipeline)
    entries = load("software.md")
    text = ""
    for entry in entries:
        entry.process(pipeline)
        text += entry.contents

    # set text in template
    with open("builder/tools/format/bulma_template.html") as file:
        template = file.read()
    with open("export.html", "w") as file:
        file.write(template.replace("{{CONTENTS}}", text))