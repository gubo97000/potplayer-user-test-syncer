import PySimpleGUI as sg

## FIRST WINDOW
def setup_window():
    # ask for the number of instances
    layout = [
        [sg.Text("Number of instances")],
        [sg.Input()],
        [sg.Button(f"{i}", key=f"but{i}") for i in range(2,5)],
        [sg.Button("Ok")],
    ]
    window = sg.Window("SyncPlay", size=(300, 300), resizable=True).Layout(layout)
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        exit()
    if "but" in event[:3]:
        window.close()
        return int(event[-1])
    
    window.close()
    return int(values[0])
