import os

def get_playlist():
    #from the folder playlist get all the files .dpl and put them in a dict with the name of the file as key and the absolute path as value
    playlist = {}
    playlist_folder = os.path.join(os.getcwd(), "playlist")
    for file in os.listdir(playlist_folder):
        if file.endswith(".dpl"):
            playlist[file] = os.path.join(playlist_folder, file)
    return playlist
