import PySimpleGUI as sg
import yaml

from app_types import Context, Preset

## FIRST WINDOW
def setup_window(c: Context):
    presets:list = get_presets()
    # ask for the number of instances
    layout = [
        [sg.Text("Number of instances")],
        [
            sg.Frame(
                "Fast choice", [[sg.Button(f"{i}", key=f"but{i}") for i in range(2, 5)]]
            )
        ],
        [sg.Frame("Custom", [[sg.Input()], [sg.Button("Ok")]])],
        [
            sg.Frame(
                "Presets",
                [
                    [sg.Combo([x["name"] for x in presets], key="preset", readonly=True)],
                    [sg.Button("Load Preset", key="load_preset")],
                ],
            )
        ]
        if presets
        else [],
    ]
    window = sg.Window("SyncPlay", size=(300, 300), resizable=True).Layout(layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            exit()
        if "but" in event[:3]:
            window.close()
            c["n_istances"] = int(event[-1])
            return c
        if event == "load_preset":
            if values["preset"] == "":
                sg.Popup("No preset selected", keep_on_top=True)
                continue
            else:
                # get the preset with the property name = values["preset"], from the list of dicts presets
                c["preset"] = list(filter(lambda x: x["name"] == values["preset"], presets))[0]
                c["n_istances"] = len(c["preset"]["instances"])
                window.close()
                return c
        window.close()
        c["n_istances"] = int(values[0])
        return c


def get_presets():
    """Get the presets from the presets yaml if the file doesn't exist return an empty list"""
    try:
        with open("./presets.yml", "r", encoding="utf-8") as f:
            presets:list[Preset] = yaml.safe_load(f)["presets"]
    except FileNotFoundError:
        print("No presets file found")
        presets = []
    return presets
