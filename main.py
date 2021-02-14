#!/bin/python3
import json
import os
import time
import urllib.request

class Main:
    _CONFIG_JSON_FILENAME = "config.json"
    _LAST_SEEN_FILE = "last_seen_timestamp.txt"
    _STEAM_BASE_URL = "https://store.steampowered.com/appreviews/{}?json=1"
    

    def main(self):
        all_reviews = []

        config_json = self._read_config_json()
        app_ids = config_json["appIds"]
        last_timestamp = self._get_last_review_time()

        for app_id in app_ids:
            # Call the API for each app and get reviews
            url = Main._STEAM_BASE_URL.format(app_id)
            response = urllib.request.urlopen(url).read()
            json_response = json.loads(response.decode('utf-8'))

            if json_response["success"] != 1:
                print("Error: failed to fetch API for app {}; response was: success={})".format(app_id, json_response["success"]))
            
        self._write_current_time()

    def _read_config_json(self):
        config_json = ""
        with open(Main._CONFIG_JSON_FILENAME) as file_handle:
            config_json = file_handle.read()
        config = json.loads(config_json)
        return config
    
    def _get_last_review_time(self):
        # Check when's the last time we looked at reviews
        last_timestamp = 0
        if os.path.isfile(Main._LAST_SEEN_FILE):
            with open(Main._LAST_SEEN_FILE, 'r') as file_handle:
                last_timestamp = float(file_handle.read())
                print("Read last timestamp {}".format(last_timestamp))

        return last_timestamp

    def _write_current_time(self):
        # Write current time so we get newer reviews next time we run
        with open(Main._LAST_SEEN_FILE, 'w') as file_handle:
            file_handle.write(str(time.time()))
        

Main().main()