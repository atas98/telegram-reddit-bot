# telegram-reddit-bot
Telegram bot for retrieving reddit posts content

## Commands
* __URL__ -> show content of the post (mb user too)
* __/show__ -> start dialoge to grab specific posts
  1. __subreddit__ -> subreddit to search in, e.g. _memes_ or _r/memes_
  2. __orderby__ -> _hot_ or _new_ or _best_ or _top_
  3. __quantity__ -> number of posts to show
   
  _Example:_ /show memes random 3
* __/subscribe__ -> send new posts every N minutes (max 6 or someth)
    _Example:_ /subscribe r/aww
* __/show_subscribtions__ ->  show list of subscriptions
* __/unsubscribe__ -> 
* __/settings__ ->
  1. Manage favorite subreddits (for subreddit_kb)
  2. Manage subscription feed refreshment time
  3. Manage sub feed time interval

## Roadmap
- [x] - URL to content
  - [x] - Self post (text only) 
  - [x] - Photo 
  - [x] - Album 
  - [x] - Gif 
  - [ ] - Reddit hosted video
  - [x] - Link  
- [x] - /show command
  - [ ] - keyboard for subreddit (keep track of favorite posts) 
  - [x] - keyboard for sort types 
  - [x] - keyboard for quantity
- [ ] - Form messages file w/ locals
- [ ] - Connect MongoDB for subscriptions
- [ ] - /subscribe
- [ ] - Swicth local storage to Redis
- [ ] - Dockerize app 
- [ ] - Deploy to heroku
