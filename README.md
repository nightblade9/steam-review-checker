# Steam Review Checker

![screenshot of dashboard](https://i.imgur.com/Lh9P8gI.png)

[![Build Status](https://travis-ci.com/nightblade9/steam-review-checker.svg?branch=main)](https://travis-ci.com/nightblade9/steam-review-checker)

- Do you find it tedious to check Steam reviews daily to see if there's something new?
- Do you often forget to subscribe to your own games' discussion forums on Steam?
- Isn't it painful to check Steam pages for multiple games?

Well, I felt the same way. I created Steam Review Checker with one goal: create a single place I can check daily, and see the latest stuff across all my games.

Currently, Steam Review Checker shows reviews and discussions for your specified games, newest-first. Feel free to suggest more features or open a PR with changes.

# Setup

You'll need Python 3 and NodeJS
- Running `python` and `node` from the terminal should work.
- If you're using `py.exe` instead, you'll need to update `main.py` to specify that command instead.

First, create a new `config.json` file in the repository root directory, and put your Steam app IDs in it:

```json
{
    "appIds": [ 667510, 1342600 ]
}
```

Build the web application:

- Open a terminal and browse to the `web` directory
- Run `npm i` to fetch all npm packages
- Run `npm run build` and make sure it builds fine

Build the Python application:

- Run `pip install -r requirements.txt` to install necessary pip packages
- Run `python main.py` to run the web application.

It builds, runs, fetches game data, and starts the web-server. You can open a browser to `localhost:8000` to see the dashboard.

# Development Environment

For local development setup, you can fetch data, and then just run the React app and iterate quickly on the UI:

- Make sure you've run `python main.py` at least once to fetch and write data to disk (see `web/build/data`)
- `cd` into `web` and run `npm start`
