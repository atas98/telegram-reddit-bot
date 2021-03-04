from typing import Any, Generator, List
import asyncpraw
from asyncpraw.models import Submission
import logging
import json
import requests
from enum import Enum

class Post_Types(Enum):
    TEXT = 0
    PIC = 1
    GIF = 2
    VID = 3
    LINK = 4 


reddit = asyncpraw.Reddit(**redditCredits)

async def get_post_type(post :Submission) -> Post_Types:
    if post.is_self:
        return Post_Types.TEXT
    header_type = requests.head(post.url).headers['Content-Type']
        

async def get_post(link :str):
    try:
        post = await reddit.submission(url=link)
        
        # Url parsing
        if post.is_self:
            post_type = post_types.TEXT
        else:
            post_type = post_types.LINK

        # TODO: return {title, url_to_post, type[TEXT, PIC, GIF, VID, LINK, MULTILINK], content}
        return {
            "title": post.title,
            "url": post.permalink,
            "type": post_type,
            "nsfw": post.over_18,
            "content": post.selftext or post.url
        }
    except asyncpraw.exceptions.InvalidURL:
        logging.warning("Invalid URL!")
        

# def top_handler(subreddit='all', num=1, *args :Any) -> Generator:
#     """Handler for /top command to tg bot

#     Args:
#         subreddit (str, optional): Subreddit to serch into. Defaults to 'r/all'.
#         num (int, optional): number of posts to process. Defaults to 1.

#     Returns:
#         [Generator[str]]: titles of requested posts
#     """
#     num = int(num) or 1
#     subreddit = _subreddit_is_valid(subreddit)
#     if not subreddit:
#         raise ValueError("Invalid subreddit name")
        
#     posts = []
#     try:
#         for submission in reddit.subreddit(subreddit).top(limit=num):
#             posts.append(submission)
#     except praw.prawcore.exceptions.BadRequest as err:
#         print(err)
#     return _post_generator(posts)