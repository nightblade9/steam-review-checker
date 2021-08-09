#!/bin/python3
import datetime
from re import L
from .steam_fetcher import SteamFetcher
import urllib
import lxml.html

# Scrapes Steam's discussion forums to get you the latest greatest data.
class DiscussionFetcher(SteamFetcher):

    _STEAM_DISCUSSIONS_URL = SteamFetcher._STEAM_COMMUNITY_URL + "/discussions/"
    _DISCUSSION_NODE_ROOT_XPATH = "//div[contains(@class, 'forum_topic ')]"

    # Metadata is a dictionary of app_id => data
    def get_discussions(self, metadata):
        config_json = self._read_config_json()
        app_ids = config_json["appIds"]
        all_discussions = []

        for app_id in app_ids:
            url = DiscussionFetcher._STEAM_DISCUSSIONS_URL.format(app_id)
            game_name = metadata[app_id]["game_name"]
            response = urllib.request.urlopen(url).read()
            raw_html = response.decode('utf-8')
            discussions = _parse_discussions(raw_html, app_id, game_name)
            
            for discussion in discussions:
                all_discussions.append(discussion)
            
            print("Fetched {} discussions for {}".format(len(discussions), game_name))

        # Sort by time descending, order of games isn't important
        all_discussions.sort(key=lambda x: x["date"], reverse=True)
        return all_discussions

def _parse_discussions(raw_html, app_id, game_name):
    discussions = []
    # Repair HTML so we can use XPath
    raw_html = raw_html.replace('class="searchtext"', '')
    
    # Parse the output
    root = lxml.html.fromstring(raw_html)
    discussion_nodes = root.xpath(DiscussionFetcher._DISCUSSION_NODE_ROOT_XPATH)

    for i in range(len(discussion_nodes)):
        node = discussion_nodes[i]

        link_node = [a for a in node if a.tag == 'a'][0]
        discussion_url = link_node.attrib["href"]

        dissected_nodes = node.text_content().strip().split('\t\t\t\t')
        # Dissected nodes is eight items, including some empty ones.
        num_replies = dissected_nodes[0].strip()

        title_and_author = dissected_nodes[7].split('\n')
        title = title_and_author[0].strip()
        author = title_and_author[-1].strip()

        raw_date = dissected_nodes[2].strip()
        discussion_date = _parse_date(raw_date)

        days_ago = (datetime.datetime.now() - discussion_date).days
        # small differences like "8 minutes ago" can become "-1 days" ago (time synch issues), make it 0 days ago
        days_ago = max(days_ago, 0) 

        date_formatted = discussion_date.strftime("%Y-%m-%d %H:%M")

        discussions.append({
            "app_id": app_id,
            "title": title, # discussion title, not game name
            "date": date_formatted,
            "author": author,
            "url": discussion_url,
            "num_replies": num_replies,
            "days_ago": days_ago,
            "game_name": game_name
        })
    
    return discussions

def _parse_date(raw_date):
    # Ah, Steam, ah. Discussion dates can have a variety of interesting, painful formats.
    # 1) The most stable are dates older than a year: we get a full year, month, and day (e.g. April 29, 2019).
    # 2) Reviews this year, have no year attached to them (e.g. May 20).
    # 3) Really recent reviews can be, like, "8 minutes ago", 'Just now', etc.

    if len(raw_date.strip()) == 0 or raw_date.upper() == 'JUST NOW':
        return datetime.datetime.now()
    elif "minutes ago" in raw_date or "hour ago" in raw_date or "hours ago" in raw_date:
        index = raw_date.index(' ') # the first space in "8 minutes ago"
        delta = int(raw_date[0:index])
        delta = datetime.timedelta(minutes=delta) if "minutes" in raw_date else datetime.timedelta(hours=delta)
        return datetime.datetime.now() + delta
    # If there's no year, add one!
    elif not ',' in raw_date:
        # May 23 => May 23, 2021
        raw_date = raw_date.replace(" @ ", ", {} @ ".format(datetime.datetime.now().year))
    
    return datetime.datetime.strptime(raw_date, '%d %b, %Y @ %I:%M%p')
