# Window to set the playlist
import os
import PySimpleGUI as sg
from app_types import Context
from services.commands import start_app
from pywinauto.timings import wait_until


def playlist_set_window(c: Context):
    """Window to set the playlist"""
    playlists = get_playlist()
    layout = [
        [sg.Combo(list(playlists.keys()), key="playlist", readonly=True)],
        [sg.Button("Load Playlist", key="load_playlist")],
    ]
    window = sg.Window(
        "SyncPlay", size=(300, 300), resizable=True, return_keyboard_events=True
    ).Layout(layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "load_playlist":
            if values["playlist"] == "":
                sg.Popup("No playlist selected")
                continue
            for pot in c["pots"]:
                pot.send_keystrokes("{VK_F4}")  # Stop
                pot.send_keystrokes("{VK_F3}")  # Open Select Window
            for app in c["apps"]:  # Open the playlist
                app["Open"].wait("ready")
                app["Open"].Edit.set_text(playlists[values["playlist"]])
                app["Open"].Button.click()
            for i in range(c["n_istances"]):  
                wait_until(10, 0.1, lambda: c["pots"][i].element_info.name != "PotPlayer")
            for i in range(c["n_istances"]): # Pause the apps and send to start
                c["pots"][i].send_keystrokes("{SPACE}")
                c["pots"][i].send_keystrokes("{BACKSPACE}")

            # Set playlist variables
            c["apps_status"] = [True] * c["n_istances"]
            c["current_playlist"] = values["playlist"]
            with open(playlists[values["playlist"]], "r", encoding="utf-8") as f:
                c["playlist_len"] = f.read().count("*file")
            c["results"] = {}
            c["item_pos"] = 0
            break
    window.close()
    return c


def get_playlist():
    """From the folder playlist get all the files .dpl and put them in a dict with the name of the file as key and the absolute path as value"""
    playlist = {}
    playlist_folder = os.path.join(os.getcwd(), "playlist")
    for file in os.listdir(playlist_folder):
        if file.endswith(".dpl"):
            playlist[file] = os.path.join(playlist_folder, file)
    return playlist
