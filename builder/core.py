import re
import requests
from tqdm import tqdm
from typing import Callable, Any

_tools: dict[str, Callable] = dict()
shared_config: dict[str, Any] = dict()

class Entry:
    def __init__(self, name: str):
        # obtained from import
        self.name = name
        self.urls = list()
        self.owners = list()
        # dynamic sections that are modified by tools
        self.contents: str = ""
        self.unparsed_sections: dict[str,list[str]] = dict()
        self.keywords: dict[str,float] = dict()
        self._cached_contents: dict[str, str] = dict()

    def normal_name(self):
        return self.name.replace(" ", "_").replace("-", "_")

    def download(self, url: str):
        result = self._cached_contents.get(url)
        if result is not None: return result
        get = requests.get(url)
        if get.status_code == 200: result = get.text
        else: result = ""
        self._cached_contents[url] = result
        return result

    def section(self, title, contents: list[str]):
        section = self.unparsed_sections.get(title)
        if section is None:
            section = list()
            self.unparsed_sections[title] = section
        section.extend(contents)

def process(entries: list[Entry], tools: list[str]):
    for tool in tools:
        runner = _tools.get(tool)
        assert runner, f"Not found tool '{tool}' among:\n"+"\n".join(_tools.keys())
        runner(entries)
    kwdata = "<script>const kwdata = {"
    for entry in entries:
        kwdata += "\n"+entry.normal_name()+": {"
        for k, v in entry.keywords.items():
            kwdata += f"\""+k+"\":"+str(v)+","
        kwdata += "},"
    kwdata += "\n};</script>"
    return "\n".join(entry.contents for entry in entries)+kwdata

def tool(func):
    name = func.__module__+"."+func.__name__
    def wrapper(entries: Entry, **kwargs):
        assert isinstance(entries, list), "@tool definitions apply to all entries"
        for entry in tqdm(entries, name.ljust(40)):
            ret = func(entry, **kwargs)
            if ret:
                assert isinstance(ret, list), name+" returned a non-None and non-List value"
                entry.section(name, ret)
    wrapper.__doc__ = func.__doc__
    _tools[name] = wrapper
    return wrapper

def raw_tool(func):
    name = func.__module__+"."+func.__name__
    _tools[name] = func
    return func

def show_pipeline(tools: list[str], max_width: int = 60):
    # THIS FUNCTION IS LLM-GENERATED (CAN THUS BE MAINTAINED WITH AN LLM)
    elements = []
    for tool in tools:
        runner = _tools.get(tool)
        assert runner, f"Not found tool '{tool}' among:\n" + "\n".join(_tools.keys())
        elements.append(f'\33[0;36m{tool}\33[0m: {runner.__doc__}')
    def strip_ansi(text: str) -> str:
        return re.sub(r'\x1b\[[0-9;]*m', '', text)
    def visible_len(text: str) -> int:
        return len(strip_ansi(text))
    def wrap_text(text: str, width: int) -> list[str]:
        words = text.split()
        lines = []
        current = ""
        for word in words:
            if current and visible_len(current) + 1 + visible_len(word) > width:
                lines.append(current)
                current = word
            else: current = (current + " " + word).strip()
        if current: lines.append(current)
        return lines
    def pad_line(text: str, width: int) -> str:
        return text + " " * (width - visible_len(text))
    border = "┌" + "─" * (max_width + 2) + "┐"
    bottom = "└" + "─" * (max_width + 2) + "┘"
    arrow  = " " * ((max_width // 2) + 1) + "│"
    tip    = " " * ((max_width // 2) + 1) + "▼"
    for i, element in enumerate(elements):
        print(border)
        for line in wrap_text(element, max_width):
            print("│ " + pad_line(line, max_width) + " │")
        print(bottom)
        if i < len(elements) - 1:
            print(arrow)
            print(tip)