from pywinauto.timings import wait_until
from app_types import Context

def get_active_windows(c:Context):
    """Returns the list of active windows"""
    return [i for i, x in enumerate(c["apps_status"]) if x]


def sync_apps(c:Context, index=0):
    # Copy the time from the first window
    time = c["apps"][index]["Jump to Time/Frame"].SysLink.texts()[0][3:-4]
    # Paste the time in the other windows
    for i in range(0, c["n_istances"]):
        c["time_edits"][i].set_text(time)
        c["time_edits"][i].send_keystrokes("{ENTER}")
    c["pots"][index].send_keystrokes("^")  # Focus on the last window
    return index

def focus_apps(c:Context, index=0):
    """Stops all windows except the one selected"""
    for i in range(0, c["n_istances"]):
        if i != index:
            c["pots"][i].send_keystrokes("{VK_F4}")
    return index

def stop_app(c:Context, index=0):
    """Stops the selected window"""
    c["pots"][index].send_keystrokes("{VK_F4}")
    c["apps_status"][index] = False
    return c

def start_app(c:Context, index=0):
    """Starts the selected window after a stop, it will start paused"""
    c["pots"][index].send_keystrokes("{SPACE}")
    wait_until(1.5, 0.1, lambda: c["pots"][index].element_info.name != "PotPlayer")
    c["pots"][index].send_keystrokes("{SPACE}")
    c["apps_status"][index] = True
    return c

def play_apps(c:Context):
    """Play all windows"""
    for i in get_active_windows(c):
        c["pots"][i].send_keystrokes("{SPACE}")
    return c

def frame_forward_apps(c:Context):
    """Frame forward all windows"""
    for i in get_active_windows(c):
        c["pots"][i].send_keystrokes("f")
    return c

def frame_back_apps(c:Context):
    """Frame back all windows"""
    for i in get_active_windows(c):
        c["pots"][i].send_keystrokes("d")
    return c

def foward_apps(c:Context):
    """Foward all windows"""
    for i in get_active_windows(c):
        c["pots"][i].send_keystrokes("{RIGHT}")
    return c

def back_apps(c:Context):    
    """Back all windows"""
    for i in get_active_windows(c):
        c["pots"][i].send_keystrokes("{LEFT}")
    return c

def next_item(c:Context):
    """Next item in the playlist"""
    c["apps_status"] = [True] * c["n_istances"]
    for app in c["pots"]:
        app.send_keystrokes("{PGDN}")
    c["item_pos"] += 1
    return c

def prev_item(c:Context):
    """Previous item in the playlist"""
    c["apps_status"] = [True] * c["n_istances"]
    for app in c["pots"]:
        app.send_keystrokes("{PGUP}")
    c["item_pos"] -= 1
    return c
