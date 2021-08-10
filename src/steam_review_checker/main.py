import asyncio
import datetime
from pathlib import Path
import sys
import time

from aiohttp import web
from jsonargparse import ArgumentParser
from jsonargparse.typing import (List, PositiveFloat, PositiveInt)

from .fetchers.discussion_fetcher import DiscussionFetcher
from .fetchers.game_fetcher import GameFetcher
from .fetchers.review_fetcher import ReviewFetcher

PORT = 8000
WEB_DIR = Path(__file__).parent / "web"
DEFAULT_CONFIG_FILES = [
    Path("~") / "steam-review-checker.json",
    Path(__file__).parent.parent.parent / "config.json"
]

class App:
    def __init__(self, app_ids, refresh_data_interval_minutes):
        self.app_ids = app_ids
        self.refresh_data_interval_minutes = refresh_data_interval_minutes

        self.data = {
            "metadata": {},
            "reviews": [],
            "discussions": []
        }

    async def run(self):
        loop = asyncio.get_event_loop()

        await self._fetch_all_data()
        loop.create_task(self._poll_data())
        
        web_server = web.Application(loop=loop)
        web_server.add_routes([
            web.get("/data/{type}.json", self._handle_data_request),
            web.get("/", self._redirect_to_index),
            web.static("/", WEB_DIR)
        ])
        server = await loop.create_server(web_server.make_handler(), "127.0.0.1", PORT)

        print("Web server running on http://localhost:{}. Data is refreshed every {} minutes.".format(PORT, self.refresh_data_interval_minutes))
        await server.serve_forever()

    async def _poll_data(self):
        while True:
            await asyncio.sleep(self.refresh_data_interval_minutes * 60)
            await self._fetch_all_data()
    
    async def _fetch_all_data(self):
        start_time = time.time()

        metadata = await GameFetcher().get_game_metadata(self.app_ids)
        self.data["metadata"] = metadata

        self.data["reviews"], self.data["discussions"] = await asyncio.gather(*[
            ReviewFetcher().get_reviews(self.app_ids, metadata),
            DiscussionFetcher().get_discussions(self.app_ids, metadata)
        ])

        stop_time = time.time()
        elapsed_time = stop_time - start_time
        print("{0} | Fetched data in {1:g}s".format(datetime.datetime.now(), elapsed_time))

    async def _handle_data_request(self, request):
        data_type = request.match_info["type"]

        if data_type in self.data:
            return web.json_response(self.data[data_type])
        raise web.HTTPNotFound()
    
    async def _redirect_to_index(self, request):
        return web.HTTPFound("/index.html")

def run_from_cli():
    arg_parser = ArgumentParser(
        prog="steam-review-checker",
        description="Shows reviews and discussions for your specified games, newest-first.",
        default_config_files=list(map(str, DEFAULT_CONFIG_FILES)),
        default_env=True,
        env_prefix="STEAM_REVIEW_CHECKER"
    )
    arg_parser.add_argument(
        "app_ids",
        type=List[PositiveInt],
        help="List of Steam app IDs to fetch and display data for. e.g.: \"[1672920,1373250,1057990]\". "
            # It doesn't show env hints for positional arguments..
            "ENV: STEAM_REVIEW_CHECKER_APP_IDS"
    )
    arg_parser.add_argument(
        "--refresh_data_interval_minutes",
        type=PositiveFloat,
        default=60,
        help="The interval in which data is pulled/refreshed from Steam."
    )

    cli_args = sys.argv[1:]
    args = arg_parser.parse_args(cli_args)

    app = App(args.app_ids, args.refresh_data_interval_minutes)
    asyncio.run(app.run())

if __name__ == "__main__":
    run_from_cli()
