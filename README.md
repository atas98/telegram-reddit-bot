# telegram-reddit-bot

Telegram bot for retrieving reddit posts content. Telegram: [@RedditBot](https://t.me/atasrdtpeeperbot)

## Commands
<<<<<<< HEAD
* __URL__ -> show content of the post (mb user too)
* __/show__ -> start dialoge to grab specific posts
  1. __subreddit__ -> subreddit to search in, e.g. _memes_ or _r/memes_
  2. __orderby__ -> _hot_, _new_, _top_, _rising_ or _random_
  3. __quantity__ -> number of posts to show
  _Example:_ /show memes random 3

## TODO
* __/subscribe__ -> send new posts every N minutes (max 6 or someth)
    _Example:_ /subscribe r/aww
* __/show_subscribtions__ ->  show list of subscriptions
* __/unsubscribe__ -> 
* __/settings__ ->
  1. Manage favorite subreddits (for subreddit_kb)
  2. Manage subscription feed refreshment time
  3. Manage sub feed time interval
  4. Turn comments on/off
=======

- **URL** -> show content of the post (mb user too)
- **/show** -> start dialoge to grab specific posts
  1. **subreddit** -> subreddit to search in, e.g. _memes_ or _r/memes_
  2. **orderby** -> _hot_ or _new_ or _best_ or _top_
  3. **quantity** -> number of posts to show
     _Example:_ /show memes random 3
- **/settings** ->
  1. Manage favorite subreddits (for subreddit_kb)
  2. Manage language
>>>>>>> 6636cff09ffcf701c63d311d1fd59de4c4bbb6a3

## Roadmap

- [x] - URL to content
  - [x] - Self post (text only)
  - [x] - Photo
  - [x] - Album
  - [x] - Gif
  - [ ] - Reddit hosted video
  - [x] - Link
- [x] - /show command
<<<<<<< HEAD
  - [ ] - keyboard for subreddit (keep track of favorite subs) 
  - [x] - keyboard for sort types 
  - [x] - keyboard for quantity
  - [ ] - __Show more__ button
- [ ] ~~- Switch to webhooks~~
- [ ] ~~- Authorization for upvotes and comments~~
- [ ] - Form messages file w/ locals
- [ ] ~~- Connect MongoDB for subscriptions~~
- [ ] - Subscribe logic
- [x] - Swicth local storage to Redis
- [x] - Dockerize app 
=======
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
>>>>>>> 6636cff09ffcf701c63d311d1fd59de4c4bbb6a3
- [x] - Deploy to heroku
