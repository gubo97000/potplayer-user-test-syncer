#%%
import os
import random
import win32api

# path = "C:\\Users\\gubo9\\Desktop\\download\\The Amazing World of Gumball S01-S06 1080p WEB-DL AAC2.0 H.264-MiXED [RiCK]\\The.Amazing.World.of.Gumball.S03.1080p.WEB-DL.AAC2.0.H.264-iT00NZ"
path = "C:\\GProjects\\potplayer\\testvideo"
path = win32api.GetShortPathName(path)
files = os.listdir(path)
files = [os.path.join(path, file) for file in files]
files = [win32api.GetShortPathName(file) for file in files]

n = 5
for i in range(n):
    with open(f"./{i}.dpl", "w") as f:
        f.write("DAUMPLAYLIST\n")
        # permutate the list
        random.shuffle(files)
        for j, file in enumerate(files):
            f.write(f"{j+1}*file*{file}\n")

# %%
