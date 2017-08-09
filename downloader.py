import os
import os.path
import json
import codecs
import time
import _thread
import requests

PLATFORMS = ["aplite", "basalt", "chalk", "diorite", "emery"]
N_THREADS = 20

chunks_failed = []

threads = []
thread_lock = _thread.allocate_lock()

def tryMkdir(dir):
    if not os.path.isdir(dir) and not os.path.isfile(dir):
        os.mkdir(dir)
    elif os.path.isfile(dir):
        print("Error: " + dir + " should be a directory, not a file.")
        return False
    return True

def download(list):
    global chunks_failed

    global threads
    global thread_lock

    for app in list:
        with thread_lock:
            print("Downloading app #" + app)

        try:
            if not tryMkdir("PebbleAppStore/" + app):
                pass
            
            pbw_urls = []

            for platform in PLATFORMS:
                if not tryMkdir("PebbleAppStore/" + app + "/" + platform) or not tryMkdir("PebbleAppStore/" + app + "/pbws"):
                    pass
                jsonR = requests.get("https://api2.getpebble.com/v2/apps/id/" + app + "?image_ratio=1&hardware=" + platform)
                jsonDat = json.loads(jsonR.text)
                
                output = codecs.open("PebbleAppStore/" + app + "/" + platform + "/" + app + ".json", "w", "utf-8")
                output.write(jsonR.text)
                output.close()

                if "latest_release" in jsonDat["data"][0]:
                    pbw_url = jsonDat["data"][0]["latest_release"]["pbw_file"]

                    if pbw_url not in pbw_urls:
                        pbw_urls.append(pbw_url)

            i = 0
            for pbw_url in pbw_urls:
                with thread_lock:
                    print("Downloading " + pbw_url)

                r = requests.get(pbw_url, stream=True)
                with open("PebbleAppStore/" + app + "/pbws/" + str(i) + ".pbw", 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                    f.close()

                i = i + 1

        except Exception as e:
            with thread_lock:
                print("Error with " + app + ": " + str(e))

                chunks_failed = chunks_failed + list
    
    threads.remove(_thread.get_ident())

def split_list(list, n):
    for i in range(0, len(list), n):
        yield list[i:i + n]

def threaded_download(l):
    chunks = []
    for chunk in list(split_list(l, 10)):
        chunks.append(chunk)

    chunks_not_downloaded = []
    for i in range(0, len(chunks)):
        chunks_not_downloaded.append(i)

    n_threads = 0
    if len(chunks_not_downloaded) > N_THREADS:
        n_threads = N_THREADS
    else:
        n_threads = len(chunks_not_downloaded)

    for i in range(0, n_threads):
        threads.append(_thread.start_new_thread(download, (chunks[chunks_not_downloaded[0]],)))
        del chunks_not_downloaded[0]

    while len(chunks_not_downloaded) > 0:
        while len(threads) == N_THREADS:
            time.sleep(.1)
        
        threads.append(_thread.start_new_thread(download, (chunks[chunks_not_downloaded[0]],)))
        del chunks_not_downloaded[0]

    while len(threads) > 0:
        time.sleep(.1)

    fout = open("failed_downloads.json", "w")
    fout.write(json.dumps(list(set(chunks_failed))))
    fout.close()