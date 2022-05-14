#!/bin/python3
import datetime
from datetime import timezone
from fetchers.steam_fetcher import SteamFetcher
import lxml.html
import urllib

# Scrapes Steam's discussion forums to get you the latest greatest data.
class DiscussionFetcher(SteamFetcher):

    # In December 2021, Steam changed the discussion date; it went from "13 Aug" to "Aug 13" - but that's not all.
    # What's worse: some clients see one format, while some see the other - at the same time, on the same page!
    # It's clear we need to be more robust here and allow mapping to multiple formats.
    _DATETIME_FORMAT_STRINGS = [
        '%d %b, %Y @ %I:%M%p', # circa Dec. 2021
        '%b %d, %Y @ %I:%M%p' # circa 2020
    ]

    # Steam has multiple "forums" - while we can parse this, for now, we just look at the main two:
    # The default one ("General Discussions"), and "Events & Announcements."
    _STEAM_DISCUSSIONS_URLS = {
        "General": SteamFetcher._STEAM_COMMUNITY_URL + "/discussions/",
        "Announcements": SteamFetcher._STEAM_COMMUNITY_URL + "/eventcomments",
    }
    
    _SUBFORUMS_ROOT_PAGE = SteamFetcher._STEAM_COMMUNITY_URL + "/discussions/"
    _SUBFORUMS_NODE_ROOT_XPATH = "//div[contains(@class, 'forum_list')]"
    _SUBFORUM_TITLE_NODE_XPATH = "//div[contains(@class, 'rightbox_list_option selected')]//a"
    _SUBFORUMS_URLS_XPATH = _SUBFORUMS_NODE_ROOT_XPATH + "//a"

    _DISCUSSION_NODE_ROOT_XPATH = "//div[contains(@class, 'forum_topic ')]"
    # Relative to the above (grandparent) node ...
    _DISCUSSION_ANSWER_XPATH = "///img[contains(@class, 'forum_topic_answer')]"

    # Magic numbers. Normal number of nodes is 8.
    _NUM_NODES_IF_DISCUSSION_AWARD = 9
    _NUM_NODES_FOR_PINNED_OR_ANSWERED_DISCUSSIONS = 10
    _NUM_NODES_FOR_PINNED_AND_AWARD = 11

    # Metadata is a dictionary of app_id => data
    def get_discussions(self, metadata):
        config_json = self._read_config_json()
        app_ids = config_json["appIds"]

        all_discussions = []

        for app_id in app_ids:
            all_subforum_urls = _get_subforum_urls(app_id)
            for subforum_url in all_subforum_urls:
                game_name = metadata[app_id]["game_name"]
                response = urllib.request.urlopen(subforum_url).read()
                raw_html = response.decode('utf-8')
                subforum_name = _get_subforum_title(raw_html)

                discussions = _parse_discussions(raw_html, app_id, game_name, subforum_name)
                
                for discussion in discussions:
                    all_discussions.append(discussion)
                
            print("Fetched {} discussions for {} across {} subforums".format(len(all_discussions), game_name, len(all_subforum_urls)))

        # Sort by time descending, order of games isn't important
        all_discussions.sort(key=lambda x: x["date"], reverse=True)
        return all_discussions

def _get_subforum_title(raw_html:str):
    root = lxml.html.fromstring(raw_html)
    nodes = root.xpath(DiscussionFetcher._SUBFORUM_TITLE_NODE_XPATH)
    name = nodes[0].text
    return name.strip()

def _get_subforum_urls(app_id:str):
    url = DiscussionFetcher._SUBFORUMS_ROOT_PAGE.format(app_id)
    response = urllib.request.urlopen(url).read()
    raw_html = response.decode('utf-8')
    
    root = lxml.html.fromstring(raw_html)
    subforum_nodes = root.xpath(DiscussionFetcher._SUBFORUMS_URLS_XPATH)

    urls = []
    for node in subforum_nodes:
        urls.append(node.attrib["href"])

    return urls

def _parse_discussions(raw_html, app_id, game_name, subforum_type):
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
        num_dissected_nodes = len(dissected_nodes)
        # Dissected nodes is eight items, including some empty ones.
        num_replies = int(dissected_nodes[0].strip())

        # Normal discussions have eight groups; pinned ones have 10. Some announcements have 9.
        # Seems like the last node is always the title.
        title_index = num_dissected_nodes - 1
        title_and_author = dissected_nodes[title_index].split('\n')
        title = title_and_author[0].strip()

        # Pinned are ten groups. Same for answered questions. /shrug
        if num_dissected_nodes == DiscussionFetcher._NUM_NODES_FOR_PINNED_OR_ANSWERED_DISCUSSIONS:
            answer_nodes = node.xpath(DiscussionFetcher._DISCUSSION_ANSWER_XPATH)
            if len(answer_nodes) > 0:
                title = "✅ {}".format(title)
            else:
                title = "📌 {}".format(title)
        
        if len(title.strip()) == 0:
            raise RuntimeError("Discussion title is empty for {}".format(discussion_url))

        author = title_and_author[-1].strip()
        
        # Discussions with a shiny award, have an extra node (Viking Trickshot)
        # Discussions that are pinned AND have a shiny award, have extra nodes (Biomutant)
        # In both cases, look for the date a node past its usual spot.
        date_index = 2
        if num_dissected_nodes == DiscussionFetcher._NUM_NODES_IF_DISCUSSION_AWARD or num_dissected_nodes == DiscussionFetcher._NUM_NODES_FOR_PINNED_AND_AWARD:
            date_index = 3
        raw_date = dissected_nodes[date_index].strip()

        if len(raw_date.strip()) == 0:
            raise RuntimeError("Discussion date failed to parse (empty string): i={} count={}".format(date_index, num_dissected_nodes))

        discussion_date = _parse_date(raw_date)
        # UTC to auto-detected local
        discussion_date = discussion_date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        now = datetime.datetime.now().replace(tzinfo=timezone.utc).astimezone(tz=None)
        days_ago = (now - discussion_date).days
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
            "game_name": game_name,
            "subforum": subforum_type
        })
    
    return discussions

def _parse_date(raw_date):
    # Ah, Steam, ah. Discussion dates can have a variety of interesting, painful formats.
    # 1) The most stable are dates older than a year: we get a full year, month, and day (e.g. April 29, 2019).
    # 2) Reviews this year, have no year attached to them (e.g. May 20).
    # 3) Really recent reviews can be, like, "8 minutes ago", 'Just now', etc.
    #
    # Note that Steam gives you this relative to your current timezone, NOT UTC.
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
    
    ### Try to parse all seen/known formats, throwing if none of them match
    last_error = None
    for date_format in DiscussionFetcher._DATETIME_FORMAT_STRINGS:
        try:
            return datetime.datetime.strptime(raw_date, date_format)
        except ValueError as v:
            last_error = v
    # If we reached here, the date-time isn't *any* known valid format
    raise last_error