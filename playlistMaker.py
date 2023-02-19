import PySimpleGUI as sg
#%%
import os
import random
import win32api

# path = "C:\\Users\\gubo9\\Desktop\\download\\The Amazing World of Gumball S01-S06 1080p WEB-DL AAC2.0 H.264-MiXED [RiCK]\\The.Amazing.World.of.Gumball.S03.1080p.WEB-DL.AAC2.0.H.264-iT00NZ"
# path = "C:\\GProjects\\potplayer\\testvideo"
# seed = 42
# path = win32api.GetShortPathName(path)
# files = os.listdir(path)
# files = [os.path.join(path, file) for file in files]
# files = [win32api.GetShortPathName(file) for file in files]
# files.sort()

# n = 5
# random.seed(seed)
# for i in range(n):
#     with open(f"./{i}.dpl", "w") as f:
#         f.write("DAUMPLAYLIST\n")
#         # permutate the list
#         random.shuffle(files)
#         for j, file in enumerate(files):
#             f.write(f"{j+1}*file*{file}\n")

def create_playlist(path, n, seed):
    path = win32api.GetShortPathName(path)
    files = os.listdir(path)
    files = [os.path.join(path, file) for file in files]
    files = [win32api.GetShortPathName(file) for file in files]
    files.sort()

    random.seed(seed)
    #create folder playlist if not exists
    if not os.path.exists("playlist"):
        os.mkdir("playlist")
    for i in range(n):
        with open(f"./playlist/{i}.dpl", "w") as f:
            f.write("DAUMPLAYLIST\n")
            # permutate the list
            random.shuffle(files)
            for j, file in enumerate(files):
                f.write(f"{j+1}*file*{file}\n")

def main_window():
    """Window to set the playlist"""
    folder = ""
    layout = [
        [sg.FolderBrowse("Open Directory", enable_events=True, key="-FOLDER-", initial_folder="./")],
        [sg.Listbox(values=[], size=(100,5), key="-FILE LIST-")],
        [sg.Text("Number of playlists")],
        [sg.Input(key="-N-")],
        [sg.Text("Seed")],
        [sg.Input(key="-SEED-")],
        [sg.Button("Create Playlist", key="create_playlist")],
    ]
    window = sg.Window(
        "Playlist Maker", size=(300, 300), resizable=True, return_keyboard_events=True
    ).Layout(layout)
    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
        if event == '-FOLDER-':
            folder = values['-FOLDER-']
        if event == "create_playlist":
            if folder == "":
                sg.popup("Select a folder", keep_on_top=True)
                continue
            if values["-N-"] == "":
                sg.popup("Insert the number of playlists", keep_on_top=True)
                continue
            create_playlist(folder, int(values["-N-"]), values.get("-SEED-", None))
        if folder != "":
            files = os.listdir(folder)
            files = [os.path.join(folder, file) for file in files]
            files = [win32api.GetShortPathName(file) for file in files]
            files.sort()
            window["-FILE LIST-"].update(files)
    window.close()
main_window()

# %%
