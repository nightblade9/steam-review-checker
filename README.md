# Steam Review Checker

Little web application that grabs data from public APIs and displays them nicely in a dashboard for you.

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

