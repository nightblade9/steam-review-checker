#!/bin/python3

class SteamFetcher:

    # Used to get the app title
    _STEAM_APP_URL = "https://store.steampowered.com/app/{}" # append app_id
    # Used to scrape discussions
    _STEAM_COMMUNITY_URL = "https://steamcommunity.com/app/{}"
