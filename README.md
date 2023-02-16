# horizonsthemer
A python-based wallpaper and theme manager.

CONTEXT:
This is my first application. I've never written a program other than really poorly made unity projects before. This technically started the day I installed Arch for the first time - I wanted to have my wallpapers looping in the background so I decided to script it myself but I didn't know BASH so I wrote it in Python. Then I eventually moved my personal pc to Arch, and this is the continuation of that. As I add more features, including,
## Subreddit scraping
## Palette saving
## A systray widget
## A tkinter gui
## A sunrise/sunset trigger
I hope to expand my knowledge of python, Linux app development, the git community, and more.

# Installation:
Clone into the repository
Make sure you have the following installed:
Feh
Pywal
Imagicmagick
Python's glob module 
Configparser
Argparse

These will be automated in a future build

# Usage:
By default, Horizons looks for wallpapers in ~/wallpapers/. It will generate a config file at ~/.config/horizonsthemer/ which contains 3 values, Default Theme, Default Duration, and Paths. Default Duration is how long a loop should last if not otherwise specified. Default Theme is which index in the Paths list it should default to. Paths is a json string containing directories.

Each directory in 'paths' is a 'theme' to loop through or query. It's recommended that you name your wallpapers so they show up in the alplabetically sorted query function.

-s sets the index, so for the fifth image of a default theme, use horizons.py -s 4 (as indicies start at 0)
-l sets looping mode, where the script will run repeatedly, incrementing by one each cycle. 
-d sets duration in seconds per loop. 
-t sets the theme
-q overrides -s and -l, if used, it will not set anything, and will instead print the names of every wallpaper in a given theme.
-n takes an arbitrarily long series of strings for directories to set as the new 'paths' variable.

So a first time use may look like (assuming a symlink)
horizons -n /home/username/wallpapers/ /home/username/wallpapers/anime/ 
horizons -q 1
[Prints list of images in anime directory]
horizons -s 2 -l -d 150   -   to loop through the images in the directory every 2 and a half minutes starting at index 2.

MAKE SURE your directories only have pngs, jpgs, and that you give it with the trailing slash /
