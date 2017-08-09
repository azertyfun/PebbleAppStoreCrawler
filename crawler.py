#!/usr/bin/env python3

import sys
import os
import os.path
import json

import getIds
import downloader

faces = []
apps = []

if os.path.isfile("watchfaces.json"):
    f = open("watchfaces.json")
    try:
        faces = json.loads(f.read())
        f.close()
    except:
        print("Could not read from watchfaces.json. Make sure the file is valid, otherwise delete it. Aborting...")
        sys.exit()
else:
    faces = getIds.getIds("watchfaces", "watchfaces.json")

if os.path.isfile("watchapps.json"):
    f = open("watchapps.json")
    try:
        apps = json.loads(f.read())
        f.close()
    except:
        print("Could not read from watchapps.json. Make sure the file is valid, otherwise delete it. Aborting...")
        sys.exit()
else:
    apps = getIds.getIds("watchapps", "watchapps.json")

if not downloader.tryMkdir("PebbleAppStore"):
    print("Aborting...")
    sys.exit()

print("Starting threaded download with a maximum of " + str(downloader.N_THREADS) + " threads.")
downloader.threaded_download(list(set(apps + faces)))
