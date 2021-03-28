# telegram-reddit-bot

Telegram bot for retrieving reddit posts content. Telegram: [@RedditBot](https://t.me/atasrdtpeeperbot)

## Commands

- **URL** -> show content of the post (mb user too)
- **/show** -> start dialoge to grab specific posts
  1. **subreddit** -> subreddit to search in, e.g. _memes_ or _r/memes_
  2. **orderby** -> _hot_ or _new_ or _best_ or _top_
  3. **quantity** -> number of posts to show
     _Example:_ /show memes random 3
- **/settings** ->
  1. Manage favorite subreddits (for subreddit_kb)
  2. Manage language

## Roadmap

- [x] - URL to content
  - [x] - Self post (text only)
  - [x] - Photo
  - [x] - Album
  - [x] - Gif
  - [ ] - Reddit hosted video
  - [x] - Link
- [x] - /show command
  - [x] - keyboard for subreddit (keep track of favorite posts)
  - [x] - keyboard for sort types
  - [x] - keyboard for quantity
- [ ] - /settings command
  - [ ] - manage lang
  - [ ] - manage favorite subreddits
- [x] - Form messages file w/ locals
- [ ] ~~- Connect MongoDB for subscriptions~~
- [ ] ~~- /subscribe~~
- [x] - Swicth local storage to Redis
- [x] - Dockerize app
- [x] - Deploy to heroku
