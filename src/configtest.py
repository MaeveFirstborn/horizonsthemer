import os
import sys
import configparser
import json

config = configparser.ConfigParser()
x = ["/home/maeve/wallpapers/", "/home/maeve/wallpapers/lofi/"]
y = json.dumps(x)

config['Themes'] = { 'Paths' : y }
print(y)

print(f"Loaded from Config: {json.loads(config['Themes']['Paths'])}")
z = json.loads(config['Themes']['Paths'])
print(z[1])
