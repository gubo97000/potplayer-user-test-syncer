from pywinauto.application import Application
from pywinauto.controls.hwndwrapper import DialogWrapper
from pywinauto.controls.win32_controls import EditWrapper
from typing import TypedDict

class PresetInstance(TypedDict):
    prefix:str
    showId:bool
    suffix:str
    isReference:bool
class Preset(TypedDict):
    name:str
    instances:list[PresetInstance]

class PresetsFile(TypedDict):
    presets:list[Preset] 

class ResultsInfo(TypedDict):
    item_name:str
    pref_time:int

class Context(TypedDict):
    apps: list[Application]
    pots: list[DialogWrapper]
    time_edits: list[EditWrapper]
    current_playlist: str
    n_istances: int
    apps_status: list[bool]
    results: dict[int, int]
    results_info: dict[int, ResultsInfo]
    item_pos: int
    items: list[str]
    to_test: list[int]
    preset: Preset


