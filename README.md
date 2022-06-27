# Steam Review Checker

![screenshot](screenshot.png)

[![Build status](https://github.com/nightblade9/steam-review-checker/actions/workflows/ci.yml/badge.svg)](https://github.com/nightblade9/steam-review-checker/actions/workflows/ci.yml)

- Do you find it tedious to check Steam reviews daily to see if there's something new?
- Do you often forget to subscribe to your own games' discussion forums on Steam?
- Isn't it painful to check Steam pages for multiple games?

Well, I felt the same way. I created Steam Review Checker with one goal: create a single place I can check daily, and see the latest stuff across all my games.

Currently, Steam Review Checker shows reviews and discussions for your specified games, newest-first. Feel free to suggest more features or open a PR with changes.

# Setup

You'll need Python 3
- Running `python` from the terminal should work.
- If you're using `py.exe` instead, you'll need to update `main.py` to specify that command instead.

First, create a new `config.json` file in the repository root directory, and put your Steam app IDs in it:

```json
{
    "appIds": [ 667510, 1342600 ]
}
```

# Customizations

## Update Frequency

By default, the app refreshes data every 60 minutes. You can change this interval by adding an additional key/value pair to the config file. The following example changes it to refresh every minute:

```json
    "refreshDataIntervalMinutes": 1
```

Build the Python application:

- Run `pip install -r requirements.txt` to install necessary pip packages
- Run `python main.py` to run the web application.

It builds, runs, fetches game data, and starts the web-server. You can open a browser to `localhost:8000` to see the dashboard.

## Paging

By default, the app tries to get *all* pages of data: all pages across all forums, and all API calls necessary to grab all discussions. If you have a game with lots of reiews or discussions, congratulations! Since you check on a regular basis (and only care about seeing new things), you can disable paging to improve performance.

```json
    "enablePaging": false
```

If you would like more granular paging (reviews vs. discussions), open up an issue and let me know.

# Development Environment

For local development setup, you can fetch data, run the web-server and refresh the webpage whenever you make changes
