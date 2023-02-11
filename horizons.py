#!/usr/bin/python
import os
import sys
from glob import glob
import time
import argparse
import configparser
from random import * 

def getImagesContext(inputFolder):
    _images = glob(f"{inputFolder}*.png") + glob(f"{inputFolder}*.jpg")
    _length = len(_images)
    return (_images, _length)

directory = "/home/maeve/wallpapers/"
images, length = getImagesContext(directory)

os.system(f"wal -i {images[0]}")


