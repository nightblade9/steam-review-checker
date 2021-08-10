# Steam Review Checker

![screenshot of dashboard](https://i.imgur.com/Lh9P8gI.png)

[![Build Status](https://travis-ci.com/nightblade9/steam-review-checker.svg?branch=main)](https://travis-ci.com/nightblade9/steam-review-checker)

- Do you find it tedious to check Steam reviews daily to see if there's something new?
- Do you often forget to subscribe to your own games' discussion forums on Steam?
- Isn't it painful to check Steam pages for multiple games?

Well, I felt the same way. I created Steam Review Checker with one goal: create a single place I can check daily, and see the latest stuff across all my games.

Currently, Steam Review Checker shows reviews and discussions for your specified games, newest-first. Feel free to suggest more features or open a PR with changes.

## Dependencies

You'll need Python 3
- Running `pip` or `pipx` from the terminal should work.
  Although the rest of these docs will only refer to `pip`, they should be interchangeable.

## Quick Start

Install via `pip`:

```bash
pip install "git+https://github.com/nightblade9/steam-review-checker.git"
```

File, CLI, or environmant variable based configuration is supported. See help and configuration details:

```bash
steam-review-checker.exe --help
```

Example config, which you can save at `~/steam-review-checker.json` or `<repo_root>/config.json`:

```json
{
    "app_ids": [ 667510, 1342600 ],
    "refresh_data_interval_minutes": 1
}
```

Run once configured:

```bash
steam-review-checker.exe

# Or by providing `app_ids` to the command:
steam-review-checker.exe [667510,1342600]
```

It runs, fetches game data, and starts the web-server. You can open a browser to `localhost:8000` to see the dashboard.

## Development Environment

After cloning, you can `pip install . --force -e` to install the local package in edit mode.

Then website changes can be picked up simply by refreshing the webpage,
and Python changes by re-executing `steam-review-checker.exe`.
