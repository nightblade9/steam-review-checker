#!/bin/python3
import json
import os
import time
import urllib.request

class Main:
    STEAM_BASE_URL = "https://store.steampowered.com/appreviews/{}?json=1"
    LAST_SEEN_FILE = "last_seen_timestamp.txt"

    def main(self):
        all_reviews = []
        app_id = "1342600"

        # Call the API for each app and get reviews
        url = Main.STEAM_BASE_URL.format(app_id)
        response = urllib.request.urlopen(url).read()
        json_response = json.loads(response.decode('utf-8'))

        if json_response["success"] != 1:
            print("Error: failed to fetch API for app {}; response was: success={})".format(app_id, json_response["success"]))
        
        # Check when's the last time we looked at reviews
        last_timestamp = 0
        if os.path.isfile(Main.LAST_SEEN_FILE):
            with open(Main.LAST_SEEN_FILE, 'r') as file_handle:
                last_timestamp = float(file_handle.read())
                print("Read last timestamp {}".format(last_timestamp))
        
        # Write current time so we get newer reviews next time we run
        with open(Main.LAST_SEEN_FILE, 'w') as file_handle:
            file_handle.write(str(time.time()))
        
Main().main()