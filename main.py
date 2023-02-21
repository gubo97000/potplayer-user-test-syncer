import gettext

from pywinauto.application import Application
from pywinauto.findbestmatch import MatchError
import PySimpleGUI as sg
import configparser

from screens.instances import setup_window
from screens.layout import position_windows
from screens.playlists import playlist_set_window

from services.commands import *
from app_types import Context
from utility import build_instaces_names

# Init the configs
config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")
lang = config["GENERAL"]["language"]
# locale_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
# translator = gettext.translation('main', localedir=locale_dir)
translator = gettext.translation("main", localedir="locale", languages=[lang])
translator.install()
_ = translator.gettext

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
    "items": [],
    "to_test": [0, 1],  # list of the instances to test (TEPORARY)
    "preset": {},
}
c = setup_window(c)
unloadedPlaylistBlock = False
if c["preset"]:
    c["to_test"] = [
        i
        for i in range(c["n_istances"])
        if not c["preset"]["instances"][i]["isReference"]
    ]
    unloadedPlaylistBlock = c["preset"]["unloadedPlaylistBlock"]

i_names = build_instaces_names(c)
c["apps_status"] = [True for _ in range(c["n_istances"])]

## INIT THE INSTANCES
for __ in range(c["n_istances"]):
    c["apps"].append(Application().start(cmd_line=config["GENERAL"]["potPlayerPath"]))
for app in c["apps"]:
    app.PotPlayer.wait("ready")
    c["pots"].append(app.PotPlayer)
    app.PotPlayer.send_keystrokes("g")
    c["time_edits"].append(app["Jump to Time/Frame"].Edit)
    app["Jump to Time/Frame"].move_window(y=99999)

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
    """Save the results in a file as csv"""
    with open(f"./results/res_{c['current_playlist'].split('.')[0]}.csv", "w") as f:
        for k, v in c["results"].items():
            name = c["items"][k].split(";")[1].split("\\")[-1].strip()
            f.write(f"{name},{v}\n")


def menu_builder(c: Context):
    """Build the menu for the main window"""
    # PREVIOUS BUTTON
    prev_state = ""
    if c["item_pos"] == 0:
        prev_state = "!"
    menu_def = [
        ["Admin", ["📓 Set Playlist::load_playlist", "---", "📺 Layout::layout"]],
        ["Edit", [f"{prev_state}👈 Previous Item::prev_item"]]
        if c["current_playlist"] != ""
        else ["Edit", []],
    ]

    return menu_def


def main_window(c: Context):
    # playlists = get_playlist()
    print(_("test"))
    menu_elem = sg.Menu(menu_builder(c))
    layout = [
        [menu_elem],
        [
            sg.Column(
                [
                    [
                        sg.Frame(
                            _("📽 Playback Controls"),
                            [
                                [
                                    sg.B("⬅", key="frame_back", font=("Arial", 20)),
                                    sg.B("⏪", key="back", font=("Arial", 20)),
                                    sg.B("⏯", key="play_pause", font=("Arial", 20)),
                                    sg.B("⏩", key="foward", font=("Arial", 20)),
                                    sg.B("➡", key="frame_fow", font=("Arial", 20)),
                                ],
                            ],
                        ),
                    ],
                    [
                        sg.Frame(
                            _("🕰 Sync All Video to"),
                            [
                                [
                                    sg.B(i_names[i], key=f"sync_{i}")
                                    for i in range(c["n_istances"])
                                ],
                            ],
                        ),
                    ],
                    [
                        sg.Frame(
                            _("👓 On/Off Display"),
                            [
                                [
                                    sg.B(i_names[i], key=f"focus_{i}")
                                    for i in range(c["n_istances"])
                                ],
                            ],
                        ),
                    ],
                    [
                        sg.Frame(
                            _("Which display do you prefer?"),
                            [
                                [
                                    sg.Radio(
                                        i_names[i],
                                        "RADIO",
                                        key=f"pref{i}",
                                        enable_events=True,
                                        disabled=True,
                                        font=("Arial", 20),
                                    )
                                    for i in c["to_test"]
                                ],
                            ],
                        ),
                    ],
                    [
                        sg.B(
                            _('Next')+"👉",
                            key="next_item",
                            disabled=True,
                            font=("Arial", 15),
                        ),
                    ],
                ],
                key="column",
                visible=not unloadedPlaylistBlock,
                element_justification="c",
                justification="c",
            )
        ],
        [
            sg.Text(
                _("Load a playlist to start"),
                key="-unloadedPLaylistBlock-",
                visible=unloadedPlaylistBlock,
                font=("Arial", 12),
            )
        ],
    ]
    window = sg.Window(
        "SyncPlay",
        size=(500, 500),
        resizable=True,
        return_keyboard_events=True,
        keep_on_top=True,
    ).Layout(layout)
    while True:
        event, values = window.read()
        print(event, values)
        if event:
            event = event.split("::")[-1]
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
            if c["results"] != {} and c["current_playlist"]!="":  # If there are results, ask for confirmation
                if (
                    sg.popup_yes_no(
                        "Changing the playlist will reset the results.\n Do you want to continue?",
                        keep_on_top=True,
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
                sg.popup(_("User Test Completed!"), keep_on_top=True)
                c["current_playlist"] = ""
            else:  # Next item case
                next_item(c)
                menu_elem.Update(menu_builder(c))
                # updateRadio(c, window)

        if event == "prev_item":
            prev_item(c)
            menu_elem.Update(menu_builder(c))
            # updateRadio(c, window)

        if "pref" in event[:4]:
            for k, v in values.items():
                if isinstance(k, str) and "pref" in k[:4] and v is True:
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

        # PLAYLIST NAME, PROGRESS, ITEM PLAYING
        if c["current_playlist"] != "":
            name = c["items"][c["item_pos"]].split(";")[1].split("\\")[-1]
            window.set_title(
                f"SP - {c['current_playlist']} [{c['item_pos']+1}/{c['playlist_len']}] {c['items'][c['item_pos']].split(';')[0]} - {name}"
            )
            if unloadedPlaylistBlock:
                window["-unloadedPLaylistBlock-"].update(visible=False)
                window["column"].update(visible=True)
        else:
            window.set_title("SyncPlay")
            if unloadedPlaylistBlock:
                window["-unloadedPLaylistBlock-"].update(visible=True)
                window["column"].update(visible=False)

        ## Modify based on varibles change
        for i in range(c["n_istances"]):
            window[f"focus_{i}"].update(f"✅{i}" if c["apps_status"][i] else f"❌{i}")

        # NEXT BUTTON
        if c["item_pos"] + 1 >= c["playlist_len"]:
            window["next_item"].update(_("Finish"))
        else:
            window["next_item"].update(f"{_('Next')}👉")
        # NEXT BUTTON
        if c["results"].get(c["item_pos"], None) is None:
            window["next_item"].update(disabled=True)
        else:
            window["next_item"].update(disabled=False)

        # RADIO BUTTONS
        if c["current_playlist"] != "":
            for i in c["to_test"]:
                window[f"pref{i}"].update(
                    value=False, disabled=False, background_color="#64778d"
                )  # Set all to false and enable
            if c["results"].get(c["item_pos"], None) is not None:
                # If exists a result for the current item, set the radio button to true
                window[f"pref{c['results'].get(c['item_pos'])}"].update(
                    value=True, background_color="black"
                )
        else:
            for i in c["to_test"]:
                window[f"pref{i}"].update(value=False, disabled=True)
        # SYNC BUTTONS
        for i in range(c["n_istances"]):
            window[f"sync_{i}"].update(disabled=not c["apps_status"][i])

    window.close()


main_window(c)
