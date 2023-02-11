import os
import sys
from glob import glob
import time
import argparse
import configparser
from exceptions.py import NoImagesException
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
    os.system(f"wal -i {imageLocation}")

setThemesFromDirectories(["/home/maeve/wallpapers/", 
                          "/home/maeve/wallpapers/lofi/"])

images, length = getImagesContext(themes[0])
setTheme(images[21]) 
