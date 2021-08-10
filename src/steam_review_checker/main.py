from aiohttp import web
import asyncio
import datetime
from .fetchers.steam_fetcher import SteamFetcher
from .fetchers.discussion_fetcher import DiscussionFetcher
from .fetchers.game_fetcher import GameFetcher
from .fetchers.review_fetcher import ReviewFetcher
import os
import time

REFRESH_INTERVAL_CONFIG_KEY = "refreshDataIntervalMinutes"
REFRESH_INTERVAL_DEFAULT_MINUTES = 60

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(__file__), "web")
WEB_DATA_DIR = os.path.join(WEB_DIR, "data")

class App:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.data = {
            "metadata": {},
            "reviews": [],
            "discussions": []
        }

    async def run(self):
        config = SteamFetcher()._read_config_json()
        refresh_minutes = REFRESH_INTERVAL_DEFAULT_MINUTES

        if REFRESH_INTERVAL_CONFIG_KEY in config:
            refresh_minutes = int(config[REFRESH_INTERVAL_CONFIG_KEY])

        await self._fetch_all_data()
        self.loop.create_task(self._poll_data(refresh_minutes))
        
        web_server = web.Application(loop=self.loop)
        web_server.add_routes([
            web.get("/data/{type}.json", self._handle_data_request),
            web.get("/", self._redirect_to_index),
            web.static("/", WEB_DIR)
        ])
        server = await self.loop.create_server(web_server.make_handler(), "127.0.0.1", 8000)
        await server.serve_forever()
    
    async def _poll_data(self, refresh_minutes):
        while True:
            await asyncio.sleep(refresh_minutes * 60)
            await self._fetch_all_data()
    
    async def _fetch_all_data(self):
        start_time = time.time()

        metadata = await GameFetcher().get_game_metadata()
        self.data["metadata"] = metadata

        self.data["reviews"], self.data["discussions"] = await asyncio.gather(*[
            ReviewFetcher().get_reviews(metadata),
            DiscussionFetcher().get_discussions(metadata)
        ])

        stop_time = time.time()
        elapsed_time = stop_time - start_time
        print("{0} | Fetched data in {1:g}s".format(datetime.datetime.now(), elapsed_time))

    async def _handle_data_request(self, request):
        data_type = request.match_info["type"]

        if data_type in app.data:
            return web.json_response(app.data[data_type])
        raise web.HTTPNotFound()
    
    async def _redirect_to_index(self, request):
        return web.HTTPFound("/index.html")

app = App()

def run_app():
    asyncio.run(app.run())

if __name__ == "__main__":
    run_app()
