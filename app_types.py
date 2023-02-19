from pywinauto.application import Application
from pywinauto.controls.hwndwrapper import DialogWrapper
from pywinauto.controls.win32_controls import EditWrapper
from typing import TypedDict

class Context(TypedDict):
    apps: list[Application]
    pots: list[DialogWrapper]
    time_edits: list[EditWrapper]
    current_playlist: str
    n_istances: int
    apps_status: list[bool]
    results: dict[int, int]
    item_pos: int
    items: list[str]
    to_test: list[int]