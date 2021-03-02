from typing import Any, Generator, List
import praw
import json
import re


redditCredits = json.load(open('./config.json', 'r'))['reddit']
reddit = praw.Reddit(**redditCredits)

def _subreddit_is_valid(subreddit :str) -> str:
    """Check subreddit if subreddit name is valid and it exists

    Args:
        subreddit (str): inputed subreddit title to validate
    Returns:
        [str]: Empty string if subreddit title is invalid else returns title without '/r'
    """
    pattern = r"^(r\/)*[A-Za-z0-9]+"
    if not re.match(pattern, subreddit):
        return ''
    elif 'r/' in subreddit:
        return subreddit[2:]
    else:
        return subreddit


def _post_generator(posts :List[praw.models.Submission]) -> Generator[str, None, None]:
    """[summary]

    Args:
        posts (List[praw.models.Submission]): List of reddit posts

    Yields:
        Generator[str]: Pprinting post data
    """    
    for post in posts:
        # TODO: Handle different types of posts (polls, gifs, videos)
        # TODO: Format output
        
        if post.is_self:
            yield f"{post.title}\n{post.selftext}"
        else:
            # TODO: There can be couple url's
            yield f"{post.title}\n{post.url}" 


def top_handler(subreddit='all', num=1, *args :Any) -> Generator:
    """Handler for /top command to tg bot

    Args:
        subreddit (str, optional): Subreddit to serch into. Defaults to 'r/all'.
        num (int, optional): number of posts to process. Defaults to 1.

    Returns:
        [Generator[str]]: titles of requested posts
    """
    num = int(num) or 1
    subreddit = _subreddit_is_valid(subreddit)
    if not subreddit:
        raise ValueError("Invalid subreddit name")
        
    posts = []
    try:
        for submission in reddit.subreddit(subreddit).top(limit=num):
            posts.append(submission)
    except praw.prawcore.exceptions.BadRequest as err:
        print(err)
    return _post_generator(posts)


commands = {
    'top': top_handler,
    # 'best': best_handler,
    # 'new': new_handler,
    # 'hot': hot_handler,
    # 'random': random_handler,
    # 'show': show_handler
}