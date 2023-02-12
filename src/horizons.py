import os
import sys
from glob import glob
import time
from argparse import ArgumentParser
import configparser
from exceptions import NoImagesException
from random import * 
import json
configFilePath = f'/home/{os.getlogin()}/.config/horizonsthemer/'
config = configparser.ConfigParser()

if os.path.isdir(configFilePath) is False:
    os.mkdir(configFilePath)
    print("Config folder not found, making one...")

if os.path.isfile(f'{configFilePath}config') is False:
    config['General'] = {
            "DefaultDuration" : "600",
            "Paths" : f'["/home/{os.getlogin()}/wallpapers/"]'}

    try:
        with open(f'{configFilePath}config', 'w') as configfile:
            config.write(configfile)
    except FileExistsError:
        pass

else:
    config.read(f'{configFilePath}config')
    config.sections()
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

def getThemesFromDirectories(directories):
    returnVal = []
    for directory in directories:
        dirImages, dirLength = getImagesContext(directory)
        returnVal.append(directory)
    
    return returnVal
"""
Right now all this does is run the os.system call but at some point in the 
future we might want to have a callback for when this runs, maybe for some 
check in some other part of the application. 
"""
def setTheme(imageLocation): 
    print(imageLocation)
    os.system(f"wal -i {imageLocation}")
    os.system(f"feh --bg-scale {imageLocation}")

parser = ArgumentParser()
parser.add_argument("--remove", "-r", type=int)
parser.add_argument("--nameslist", "-n", nargs="+", default=[])
parser.add_argument("--looping", "-l", action="store_true", 
                    help="Loops the wallpapers")
parser.add_argument("--specific", "-s", type=int, default = 0,
                    help="Specific wallpaper index")
parser.add_argument("--theme", "-t", type=int, default = 0,
                    help="Specific theme index")
parser.add_argument("--duration", "-d", type=int, 
                    default=config['General']['DefaultDuration'], 
                    help="Time in seconds between cycles if in looping mode.")
parser.add_argument("--query", "-q", help="Lists wallpapers",
                    action="store_true")
args = parser.parse_args()

if len(args.nameslist) > 0:
   try:
       with open(f'{configFilePath}config', 'w') as configfile:
           config.set('General', 'Paths', json.dumps(args.nameslist))
           config.write(configfile)
           print("Set the config file paths")
           
   except FileExistsError:
        pass
else:
    print("Using loaded paths")
    themes = getThemesFromDirectories(json.loads(config['General']['Paths']))

wallpapers, length = getImagesContext(themes[args.theme])

if args.query is True:
    [print(f"{ind}: {wallpapers[ind]}") for ind in range(length)]
elif args.looping is False and args.specific is not None:
    setTheme(wallpapers[args.specific])

