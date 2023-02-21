import PySimpleGUI as sg

from app_types import Context

## FIRST WINDOW
def setup_window(c: Context):
    # ask for the number of instances
    layout = [
        [sg.Text("Number of instances")],
        [
            sg.Frame(
                "Fast choice",
                [[sg.Button(f"{i}", key=f"but{i}") for i in range(2, 5)]]
            )
        ],
        [sg.Frame("Custom", [[sg.Input()], [sg.Button("Ok")]])],
    ]
    window = sg.Window("SyncPlay", size=(300, 300), resizable=True).Layout(layout)
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        exit()
    if "but" in event[:3]:
        window.close()
        c["n_istances"] = int(event[-1])
        return c

    window.close()
    c["n_istances"] = int(values[0])
    return c
