import os
import sys
from glob import glob
import time
from argparse import ArgumentParser
import configparser
from exceptions import NoImagesException
from random import * 

themes = []

"""
An "images context" refers to the combination of the images and the length
of that list used for the wallpaper cycle. We do this as a unique tuplet
so that eventually we can run filters / sorts / shuffles in this function,
with an enumerated set of flags as the second argument, i.e.:
    images, length = getImagesContext(themes[2], 
                        context.COLORSORT | context.PNG) 
"""
def getImagesContext(inputFolder):
    _images = glob(f"{inputFolder}*.png") + glob(f"{inputFolder}*.jpg")
    _length = len(_images)
    if _length < 1:
        raise NoImagesException(inputFolder)
    else:
        return (_images, _length)

def setThemesFromDirectories(directories):
    for directory in directories:
        dirImages, dirLength = getImagesContext(directory)
        themes.append(directory)

"""
Right now all this does is run the os.system call but at some point in the 
future we might want to have a callback for when this runs, maybe for some 
check in some other part of the application. 
"""
def setTheme(imageLocation): 
    print(imageLocation)
    os.system(f"wal -i {imageLocation}")

parser = argparse.ArgumentParser()
parser.add_argument("--remove", "-r", type=int)
parser.add_argument("--nameslist", "-n", nargs="+", default=[])
parser.add_argument("--looping", "-l", action="store_true", 
                    help="Loops the wallpapers")
parser.add_argument("--specific", "-s", type=int,
                    help="Specific wallpaper index")
parser.add_argument("--duration", "-d", type=int, 
                    default=config['General']['DefaultDuration'], 
                    help="Time in seconds between cycles if in looping mode.")
parser.add_argument("--directory", "-dir",
                    default=config['General']['DefaultDirectory'], 
                    type=str, help="the directory")
args = parser.parse_args()


