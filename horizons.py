#!/usr/bin/python
import os
import sys
import glob
import time
import argparse
import configparser
import WEBPConverter
from random import * 

WEBPConverter.BatchConvert(
        "/home/maeve/wallpapers/wallpapersToConvert/",
        "/home/maeve/wallpapers/wallpapersToConvert/convertTest/")

"""
Pre-emptively resolves the directory for the config file. os.getlogin() yields 
the username of the account. 
/home/{username}/ is where .config/ is.
"""
configFilePath = f'/home/{os.getlogin()}/.config/pornowall/'

config = configparser.ConfigParser()
# Do we already have a config folder?
if os.path.isdir(configFilePath) is False:
    os.mkdir(configFilePath)
    print("Config folder not found, making one...")

else:
    # We DO have a config folder. This line can be ommitted in prod. 
    print("Config folder found")

"""
This is to make sure we don't overwrite the file on accident. 
Might not be necessary exactly. Will refactor if possible.
"""
if os.path.isfile(f'{configFilePath}config') is False:
    config['General'] = {
        'DefaultDirectory':f"/home/{os.getlogin()}/wallpapers/",
        'DefaultDuration':'600'
    }

    try:
        with open(f'{configFilePath}config', 'w') as configfile:
            config.write(configfile)
    except FileExistsError:
       pass 

else:
    config.read(f'{configFilePath}config') # Loads config file, parses it. 
    config.sections
    print(f"{config['General']['DefaultDirectory']}")

"""
After this previous block of code runs, either a new config file has been 
created and its default values are used, or a pre-existing one was found and 
that was loaded. Either way, these values won't fail as both scenarios are 
covered
"""
# Command line argument parser. Should refactor this. 
parser = argparse.ArgumentParser()
parser.add_argument("--remove", "-r", type=int)
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

# Gets size of directory.
images = glob.glob(f"{args.directory}*") 
length = len(images) 

if args.remove is not None:
    os.system(f"rm {images[args.remove]}")

# Main method here, this is what actually does the change.
def changeStyle(index):
    os.system(f"wal -i {images[index]} > /dev/null")
    #os.system(f"feh --bg-scale {images[index]}")

# If -l is specified, this is the looping code. 
def startLoop(startingValue = 0):
    val = startingValue
    while True:
        changeStyle(val)
        print(f"external scope length: {length}")
        if val + 1 == length:
            val = 0
        else:
            val = val + 1
        time.sleep(args.duration)

if args.looping is True and args.specific is not None:
    startLoop(args.specific)
elif args.looping is True and args.specific is None:
    startLoop(0)
elif args.looping is False and args.specific is not None:
    changeStyle(args.specific)
elif args.remove is None: 
    print("Error!") # ELABORATE THIS LATER
