import PySimpleGUI as sg
from app_types import Context
from utility import build_instaces_names

def position_windows(c:Context):
    """Window to set the position of the windows"""
    # set the window names
    i_names = build_instaces_names(c, prefix="App", suffix="", showId=True)
    # ask for the number of instances ans set
    layout = [
        [sg.Text("Move every Window to the desired display")],
        [
            sg.Text(
                "For correct results couple everytime the app number to the same display"
            )
        ],
        [
            sg.Frame(
                "Outline Apps", [[sg.Button(i_names[i], key=f"o{i}") for i in range(c["n_istances"])]]
            )
        ],
        [
            sg.Frame(
                "Move Apps to 0,0", [[sg.Button(i_names[i], key=f"m{i}") for i in range(c["n_istances"])]]
            )
        ],
        [sg.Button("Fullscreen")],
        [sg.Button("Ok")],
    ]
    window = sg.Window("SyncPlay", size=(300, 300), resizable=True, keep_on_top=True).Layout(layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Ok":
            break
        if event in [f"o{i}" for i in range(c["n_istances"])]:
            c["pots"][int(event[-1])].draw_outline()
            continue
        if event in [f"m{i}" for i in range(c["n_istances"])]:
            c["pots"][int(event[-1])].move_window(0, 0)
            continue
        if event == "Fullscreen":
            for pot in c["pots"]:
                pot.send_keystrokes("~")
            continue
    window.close()
