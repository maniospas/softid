from builder.core import Entry


def load(entry_path: str):
    entries: list[Entry] = list()
    editing_entry: Entry|None = None
    with open(entry_path) as file:
        for line in file:
            line = line.replace("\t", " ")
            line = line.strip()
            if line.startswith("%"): continue
            if not line: continue
            if line.startswith("#"):
                entry = Entry(line[1:].strip())
                entries.append(entry)
                editing_entry = entry
            elif "@" in line:
                assert editing_entry, f"Entry not started yet at {entry_path} line {line}"
                editing_entry.owners.append(line)
            else:
                assert editing_entry, f"Entry not started yet at {entry_path} line {line}"
                editing_entry.urls.append(line)
    return entries