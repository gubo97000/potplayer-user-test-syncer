from pywinauto.application import Application
from pywinauto.findbestmatch import MatchError
import PySimpleGUI as sg
import configparser

from screens.instances import setup_window
from screens.layout import position_windows
from screens.playlists import playlist_set_window

from services.commands import *
from app_types import Context

# Init the configs
config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

# Init the context
c: Context = {
    "apps": [],
    "pots": [],
    "time_edits": [],
    "current_playlist": "",
    "playlist_len": 0,
    "n_istances": 0,
    "apps_status": [],
    "results": {},
    "item_pos": 0,
    "to_test": [0,1], # list of the instances to test (TEPORARY)
}
c = setup_window(c)
c["apps_status"] = [True for _ in range(c["n_istances"])]

## INIT THE INSTANCES
for _ in range(c["n_istances"]):
    c["apps"].append(
        Application().start(
            cmd_line=config["GENERAL"]["potPlayerPath"]
        )
    )
for app in c["apps"]:
    app.PotPlayer.wait("ready")
    c["pots"].append(app.PotPlayer)
    app.PotPlayer.send_keystrokes("g")
    c["time_edits"].append(app["Jump to Time/Frame"].Edit)

## LAYOUT HELPER WINDOW
position_windows(c)


# def updateRadio(c: Context, window: sg.Window):
#     """Update the radio buttons in the main window"""
#     for i in c["to_test"]:
#         window[f"pref{i}"].update(value=False)
#     if c["results"].get(c["item_pos"], None) is None:
#         return
#     window[f"pref{c['results'].get(c['item_pos'])}"].update(value=True)


def save_results(c: Context):
    """Save the results in a file"""
    with open(f"./results/res_{c['current_playlist']}.txt", "w") as f:
        f.write(str(c["results"]))


def main_window(c: Context):
    # playlists = get_playlist()
    layout = [
        [
            sg.B("📺", key="layout"),
            sg.Button("📓", key="load_playlist"),
            sg.T("", key="playlist_name"),
            sg.T("", key="playlist_progress"),
        ],
        [
            sg.Frame(
                "📽 Playback Controls",
                [
                    [
                        sg.B("🔙", key="frame_back"),
                        sg.B("⏪", key="back"),
                        sg.B("⏯", key="play_pause"),
                        sg.B("⏩", key="foward"),
                        sg.B("🔜", key="frame_fow"),
                    ],
                ],
            ),
        ],
        [
            sg.Frame(
                "🕰 Sync All Video to",
                [
                    [
                        sg.B(f"Display {i}", key=f"sync_{i}")
                        for i in range(c["n_istances"])
                    ],
                ],
            )
        ],
        [
            sg.Frame(
                "👓 On/Off Display",
                [
                    [
                        sg.B(f"Display {i}", key=f"focus_{i}")
                        for i in range(c["n_istances"])
                    ],
                ],
            )
        ],
        [
            sg.Frame(
                "Which display do you prefer?",
                [
                    [
                        sg.R(
                            f"Display {i}",
                            "RADIO",
                            key=f"pref{i}",
                            enable_events=True,
                            disabled=True,
                        )
                        for i in c["to_test"]
                    ],
                ],
            ),

            [
                sg.Button("Prev", key="prev_item", disabled=True),
                sg.B("Next", key="next_item", disabled=True),
            ],
        ],
    ]
    window = sg.Window(
        "SyncPlay", size=(300, 300), resizable=True, return_keyboard_events=True
    ).Layout(layout)
    while True:
        event, values = window.read()
        print(event, values)
        print(c)
        if event == sg.WIN_CLOSED:
            for pot in c["pots"]:
                try:
                    pot.close()
                except MatchError:
                    print("Couldn't close one app. Maybe already closed?")
            break
        if event == "layout":
            position_windows(c)

        if event == "load_playlist":
            if c["results"] != {}:  # If there are results, ask for confirmation
                if (
                    sg.popup_yes_no(
                        "Changing the playlist will reset the results.\n Do you want to continue?"
                    )
                    == "Yes"
                ):
                    c = playlist_set_window(c)
            else:
                c = playlist_set_window(c)

        if event == "play_pause":
            play_apps(c)

        if event == "frame_fow":
            frame_forward_apps(c)

        if event == "frame_back":
            frame_back_apps(c)

        if event == "foward":
            foward_apps(c)

        if event == "back":
            back_apps(c)

        if event == "next_item":
            if c["item_pos"] + 1 >= c["playlist_len"]:  # Finish case
                for i in range(c["n_istances"]):
                    c = stop_app(c, i)
                save_results(c)
                sg.popup("User Test Completed!")
            else:  # Next item case
                next_item(c)
                # updateRadio(c, window)

        if event == "prev_item":
            prev_item(c)
            # updateRadio(c, window)

        if "pref" in event[:4]:
            for k, v in values.items():
                if "pref" in k[:4] and v is True:
                    print(k[-1])
                    c["results"][c["item_pos"]] = int(k[-1])
                    break

        if "sync" in event[:5]:
            sync_apps(c, int(event[-1]))

        if "focus" in event[:6]:
            if c["apps_status"][int(event[-1])]:
                c = stop_app(c, int(event[-1]))
            else:
                c = start_app(c, int(event[-1]))

        # if event:
        #     for app in apps:
        #         app.PotPlayer.send_keystrokes(event)
        #     continue

        ## Modify based on varibles change
        for i in range(c["n_istances"]):
            window[f"focus_{i}"].update(f"✅{i}" if c["apps_status"][i] else f"❌{i}")
        # PREVIOUS BUTTON
        if c["item_pos"] != 0:
            window["prev_item"].update(disabled=False)
        else:
            window["prev_item"].update(disabled=True)
        # NEXT BUTTON
        if c["item_pos"] + 1 >= c["playlist_len"]:
            window["next_item"].update("Finish")
        else:
            window["next_item"].update("Next")
        # NEXT BUTTON
        if c["results"].get(c["item_pos"], None) is None:
            window["next_item"].update(disabled=True)
        else:
            window["next_item"].update(disabled=False)
        # PLAYLIST NAME
        if c["current_playlist"] != "":
            window["playlist_name"].update(f"Playlist: {c['current_playlist']}")
        else:
            window["playlist_name"].update("")
        # PLAYLIST PROGRESS
        if c["current_playlist"] != "":
            window["playlist_progress"].update(f"{c['item_pos']+1}/{c['playlist_len']}")
        else:
            window["playlist_name"].update("")

        # RADIO BUTTONS
        if c["current_playlist"] != "":
            for i in c["to_test"]:
                window[f"pref{i}"].update(value=False, disabled=False) #Set all to false and enable
            if c["results"].get(c["item_pos"], None) is not None:
                #If exists a result for the current item, set the radio button to true
                window[f"pref{c['results'].get(c['item_pos'])}"].update(value=True) 
        else:
            for i in c["to_test"]:
                window[f"pref{i}"].update(value=False, disabled=True)
        # SYNC BUTTONS
        for i in range(c["n_istances"]):
            window[f"sync_{i}"].update(disabled=not c["apps_status"][i])
    window.close()


main_window(c)
