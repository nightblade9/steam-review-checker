# Steam Review Checker

![](https://i.imgur.com/qElKnFu.png)

- Do you find it tedious to check Steam reviews daily to see if there's something new?
- Do you often forget to subscribe to your own games' discussion forums on Steam?
- Isn't it painful to check Steam pages for multiple games?

Well, I felt the same way. I created Steam Review Checker with one goal: create a single place I can check daily, and see the latest stuff across all my games.

Currently, Steam Review Checker shows reviews and discussions for your specified games, newest-first. Feel free to suggest more features or open a PR with changes.

# Setup

You'll need Python 3 and NodeJS.

- Open up `config.json` and put your Steam app IDs in it.
- Run `npm i` from the `web` directory to fetch all npm packages
- Run `npm build` and make sure it builds fine

Run `python main.py` to run the web application. It builds, runs, and starts the web-server.

Sample `config.json`:
```json
{
    "appIds": [ 667510, 1342600 ]
}
```

# Development Environment

For local development:

- Make sure you've run `python main.py` at least once
- Run `npm start` from `web`

