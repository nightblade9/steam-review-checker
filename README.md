# Steam Review Checker

![screenshot of dashboard](https://i.imgur.com/Lh9P8gI.png)

[![Build Status](https://travis-ci.com/nightblade9/steam-review-checker.svg?branch=main)](https://travis-ci.com/nightblade9/steam-review-checker)

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

By default, the app refreshes data every 60 minutes. You can change this interval by adding an additional key/value pair to the config file. The following example changes it to refresh every minute:

```json
    "refreshDataIntervalMinutes": 1
```

Build the Python application:

- Run `pip install -r requirements.txt` to install necessary pip packages
- Run `python main.py` to run the web application.

It builds, runs, fetches game data, and starts the web-server. You can open a browser to `localhost:8000` to see the dashboard.

# Development Environment

For local development setup, you can fetch data, run the web-server and refresh the webpage whenever you make changes
