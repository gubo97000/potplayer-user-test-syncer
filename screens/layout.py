import PySimpleGUI as sg
from app_types import Context

def position_windows(c:Context):
    """Window to set the position of the windows"""
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
                "Apps", [[sg.Button(f"App {i}", key=f"{i}") for i in range(c["n_istances"])]]
            )
        ],
        [sg.Button("Fullscreen")],
        [sg.Button("Ok")],
    ]
    window = sg.Window("SyncPlay", size=(300, 300), resizable=True).Layout(layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Ok":
            break
        if event in [f"{i}" for i in range(c["n_istances"])]:
            c["pots"][int(event[-1])].draw_outline()
            continue
        if event == "Fullscreen":
            for pot in c["pots"]:
                pot.send_keystrokes("~")
            continue
    window.close()
