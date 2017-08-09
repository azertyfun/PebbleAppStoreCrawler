Pebble App Store Crawler
========================

This is a remake of /u/magmapus's [App Store Archive](https://www.reddit.com/r/pebble/comments/5g0gmx/in_light_of_recent_news_i_archived_the_app_store/).

It is more lightweight, only downloading JSONs and PBWs, and it downloads jsons from every platform (aplite, basalt, etc.).

It is intented to be used for Rebble's App Store, although you can use it to download your own archive of the Pebble App Store.

Usage
-----

Run `./crawler.py` to crawl the whole appstore, then download it. Alternatively, you can put a JSON array containing the UUIDs you want to download in watchapps.json and watchfaces.json (if the files don't exist, the crawler will create and populate them).

You can then run `./download_missing_apps.py` to download the apps that are in watchapps.json and watchfaces.json but not PebbleAppStore/.

Download
--------

You can download a copy of the appstore as it was on 2017-08-09 [here](https://drive.google.com/file/d/0B1rumprSXUAhTjB1aU9GUFVPUW8/view).