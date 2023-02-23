# Sync PotPlayer 
Interface to sync different instances of PotPlayer together, the sync is not perfect but is acceptable for the use case, when paused the sync is perfect.

## Usage
### Options change
The following options need to be changed in PotPlayer:
- General:  
  - Logo: 
    - change it to a black png 
    - Logo position: `stretch` 
- Playback:
    - Default window size: `Do not use`
    - Repeat video playback: `Enable: Repeat playing item`
    - - [x] Remember video playback position
    <!-- - Playlist
        - - [x] Start instantly to play selected album -->

### Notes
- By using the render Direct3D 11 the video will not start again if, when paused, the video is moved to the end
- 
### Rules for a smooth usage
- Do not control the playback within potplayer, except for the scrubbing
- You can turn off an app anytime, but you can turn it on only if the others are playing
- Send controls with calm, do not spam the buttons

# TODO
- [x] Fix playlist set after fist
- [x] Black screen find best way
- [x] ON/OFF
- [x] Open PLaylist fix
- [x] Try to fix the playlists loading????
- [x] Hide jump to frame
- [x] Reference display
- [ ] Perfect sync, maybe with multiprocess? (more a wish that anything else)