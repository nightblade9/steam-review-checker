#!/bin/python3
import json
import urllib.request

class SteamFetcher:
    _CONFIG_JSON_FILENAME = "config.json"

    # Used to get the app title
    _STEAM_APP_URL = "https://store.steampowered.com/app/{}" # append app_id

    # Sort by newest-first, up to the max (100 per page). See: https://partner.steamgames.com/doc/store/getreviews
    _STEAM_REVIEWS_URL = "https://store.steampowered.com/appreviews/{}?json=1&filter=recent&num_per_page=100"
    
    def _read_config_json(self):
        config_json = ""
        with open(SteamFetcher._CONFIG_JSON_FILENAME) as file_handle:
            config_json = file_handle.read()
        config = json.loads(config_json)
        return config
    
    def _get_steam_game_title(self, app_id):
        url = SteamFetcher._STEAM_APP_URL.format(app_id)
        response = urllib.request.urlopen(url).read()
        text = response.decode('utf-8')
        start_position = text.index("<title>") + len("<title>")
        stop_position = text.index("on Steam", start_position) - 1
        title = text[start_position:stop_position]
        return title
