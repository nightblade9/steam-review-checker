#!/bin/python3
from fetchers.steam_fetcher import SteamFetcher
import urllib.request

class GameFetcher(SteamFetcher):

    def get_game_metadata(self):
        config_json = self._read_config_json()
        app_ids = config_json["appIds"]
        all_data = {}

        for app_id in app_ids:
            game_name = self._get_steam_game_title(app_id)

            all_data[app_id] = { 
                "game_name": game_name
            }

        print('.', end='', flush=True) # progress
        return all_data

    def _get_steam_game_title(self, app_id):
        url = SteamFetcher._STEAM_APP_URL.format(app_id)
        response = urllib.request.urlopen(url).read()
        raw_html = response.decode('utf-8')

        return _parse_title(raw_html)
    
def _parse_title(raw_html:str):
    # Starting some time around 2023, all game pages have this nifty little tag:
    # <div id="appHubAppName" class="apphub_AppName">Gem Worlds</div>
    # Parsing <title>...</title> doesn't make sense any more. Can delete it as a fallback, I suppose.

    #start_position = raw_html.index("<title>") + len("<title>")
    #stop_position = raw_html.index("on Steam", start_position) - 1
    #title = raw_html[start_position:stop_position]
    #return title

    search_string = "<div id=\"appHubAppName\""
    start_position = raw_html.index(search_string)
    # go to the end of the tag
    start_position = raw_html.index(">", start_position) + 1
    stop_position = raw_html.index("</div>", start_position)
    title = raw_html[start_position:stop_position]
    return title
