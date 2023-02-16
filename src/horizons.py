import os
import sys
import time
import configparser
import threading
import json
from glob import glob
from argparse import ArgumentParser
from exceptions import NoImagesException

"""
Sets the themes (list of directories to pull wallpapers from) as an empty
list to be appended to later.
"""
themes = []

username = os.getlogin().lower()
configFilePath = f'/home/{username}/.config/horizonsthemer/'
config = configparser.ConfigParser()

"""
Generates a config file if there isn't one and reads from it if there is 
"""
if os.path.isdir(configFilePath) is False:
    os.mkdir(configFilePath)
    print("Config folder not found, making one...")

if os.path.isfile(f'{configFilePath}config') is False:
    print(f'{configFilePath}config')
    config['General'] = {
            "DefaultDuration" : "600",
            "Paths" : f'["/home/{username}/wallpapers/"]',
            "DefaultTheme" : "0"}

    try:
        with open(f'{configFilePath}config', 'w') as configfile:
            config.write(configfile)
    except FileExistsError:
        pass

else:
    config.read(f'{configFilePath}config')
    config.sections()


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

"""
Returns list of directories. Basically, this is a handler that will throw 
an exception if any of the directories is empty or does not contain images,
using the error handling in getImagesContext()
"""
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
    os.system(f"wal -i {imageLocation} > /dev/null")
    os.system(f"feh --bg-scale {imageLocation}")

def setThemeLooping(incomingWallpapers, wpIndex, themeLength, sleepDuration):
    count = wpIndex
    while True:
        setTheme(incomingWallpapers[count])
        if count + 1 is themeLength:
            count = 0
        else:
            count += 1
        time.sleep(sleepDuration)

"""
TODO: Refactor this! 
"""
parser = ArgumentParser()

# If this is specified, delete the image that is specified (NOT IMPLEMENTED)
parser.add_argument("--remove", "-r", type=int)
# If this has arguments passed to it, set the themes in the config file.  
parser.add_argument("--nameslist", "-n", nargs="+", default=[])
# If this is true, loop through the theme selected.
parser.add_argument("--looping", "-l", action="store_true", 
                    help="Loops the wallpapers")
# If this is given a value, set that specific wallpaper. If in looping mode, 
# This will set the starting wallpaper.
parser.add_argument("--specific", "-s", type=int, default = 0,
                    help="Specific wallpaper index")
# Set the specific theme to load wallpapers from. 
parser.add_argument("--theme", "-t", type=int, 
                    default = config['General']['DefaultTheme'],
                    help="Specific theme index")
# Override the default 600 seconds as set in the config file for the loop.
parser.add_argument("--duration", "-d", type=int, 
                    default=config['General']['DefaultDuration'], 
                    help="Time in seconds between cycles if in looping mode.")
# This should override all other paramters if set, other than theme: list by 
# name all wallpapers in a given theme. If this is set, do NOTHING other than
# list those filenames.
parser.add_argument("--query", "-q", help="Lists wallpapers",
                    action="store_true")
args = parser.parse_args()

index = args.specific
themesIndex = args.theme
duration = args.duration
loopmode = args.looping
query = args.query
newDirectories = args.nameslist

"""
Determines if we passed in new folders for the themes. This uses JSON to store
an arbitrarily sized array of strings as one key value for the ConfigParser 
dict. TODO: Better FileExistsError handling
Maybe an interactive prompt? 
"""
if len(newDirectories) > 0:
   try:
       with open(f'{configFilePath}config', 'w') as configfile:
           config.set('General', 'Paths', json.dumps(args.nameslist))
           config.write(configfile)
   except FileExistsError:
        print("Can't write new lines to config")
else:
    print("Using loaded paths")
    
themes = getThemesFromDirectories(json.loads(config['General']['Paths']))

# Gets the master context for the rest of the script. 
wallpapers, length = getImagesContext(themes[themesIndex])

wallpapers.sort()

# Are we in query mode? 
settingMode = (query is False and len(newDirectories) == 0)

# TODO: Implement rest of Pornographics codebase here
if query is True:
    [print(f"{ind}: {wallpapers[ind]}") for ind in range(length)]
elif settingMode:
    if args.looping is False:
        setTheme(wallpapers[index])
    elif args.looping is True:
        try:
           loopThread = threading.Thread(target=setThemeLooping,
                                         args=(wallpapers, index, length, duration))
           loopThread.start()
        except:
           print("Could not start looping thread.")
