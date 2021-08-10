#!/bin/python3
import aiohttp
import asyncio
from .steam_fetcher import SteamFetcher

class GameFetcher(SteamFetcher):

    async def get_game_metadata(self, app_ids):
        all_data = {}

        async def populate_data_for_app(app_id):
            game_name = await self._get_steam_game_title(app_id)

            all_data[app_id] = { 
                "game_name": game_name
            }

            print("Fetched metadata for {}".format(game_name))
        
        await asyncio.gather(*[
            populate_data_for_app(app_id)
            for app_id
            in app_ids
        ])

        return all_data

    async def _get_steam_game_title(self, app_id):
        url = SteamFetcher._STEAM_APP_URL.format(app_id)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                raw_html = await resp.text()

        return _parse_title(raw_html)
    
def _parse_title(raw_html):
        start_position = raw_html.index("<title>") + len("<title>")
        stop_position = raw_html.index("on Steam", start_position) - 1
        title = raw_html[start_position:stop_position]
        return title
