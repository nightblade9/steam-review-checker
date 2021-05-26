#!/bin/python3
import json

class SteamFetcher:
    _CONFIG_JSON_FILENAME = "config.json"

    # Used to get the app title
    _STEAM_APP_URL = "https://store.steampowered.com/app/{}" # append app_id
    # Used to scrape discussions
    _STEAM_COMMUNITY_URL = "https://steamcommunity.com/app/{}"
    
    def _read_config_json(self):
        config_json = ""
        with open(SteamFetcher._CONFIG_JSON_FILENAME) as file_handle:
            config_json = file_handle.read()
        config = json.loads(config_json)
        return config
    