# Steam Review Checker

Little script that pokes Steam for reviews/discussions.

Open up `config.json` and fill in all the values. You can find the steam app ID from browsing the page for your game; the ID is the last numeric value, e.g. for Oneons (`https://store.steampowered.com/app/1342600/Oneons_Prisoners/`) the app ID is 1342600.

Sample:

```json
{
    "appIds": [ 1342600 ]
}
```