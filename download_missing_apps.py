#!/usr/bin/env python3

import sys
import os
import os.path
import json

import downloader

faces = []
apps = []

f = open("watchfaces.json")
try:
	faces = json.loads(f.read())
	f.close()
except:
	print("Could not read from watchfaces.json. Make sure the file is valid, otherwise delete it and re-run the crawler. Aborting...")
	sys.exit()

f = open("watchapps.json")
try:
	apps = json.loads(f.read())
	f.close()
except:
	print("Could not read from watchapps.json. Make sure the file is valid, otherwise delete it and re-run the crawler. Aborting...")
	sys.exit()

allapps = list(set(apps + faces))

print(str(len(faces)) + " faces, " + str(len(apps)) + " apps. Total: " + str(len(allapps)))

if not os.path.isdir("PebbleAppStore"):
	print("Error: No PebbleAppStore/ directory. Please run ./crawler.py first.")
	sys.exit(1)

dir = os.listdir("PebbleAppStore")

missing = []

for app in allapps:
	if app not in dir:
		missing.append(app)

downloader.threaded_download(missing)
