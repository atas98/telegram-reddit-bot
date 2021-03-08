import logging
import requests

from asyncpraw import Reddit
from asyncpraw.models import Submission, Subreddit
from dataclasses import dataclass
from enum import Enum, unique
from typing import Generator, Optional, Union


@unique
class Post_Types(Enum):
    TEXT = 0
    PIC = 1
    GIF = 2
    VID = 3
    LINK = 4


supported_types = {
    Post_Types.PIC: {"image/jpeg", "image/png", "image/tiff"},
    Post_Types.GIF: {"image/gif"},
    Post_Types.VID: {"video/mpeg", "video/mp4", "video/webm"}
}


def get_post_type(post: Submission) -> Post_Types:
    """Returns format of the posts content

    Args:
        post (asyncpraw.models.Submission)

    Returns:
        Post_Types: content format
    """
    if post.is_self:
        return Post_Types.TEXT
    try:
        header_type = requests.head(post.url).headers['Content-Type']
        for key, type_headers in supported_types.items():
            if header_type in type_headers:
                return key
    except Exception as err:
        logging.warning(err)
    return Post_Types.LINK


# TODO: Move all dataclasses/enums to separate module
@dataclass
class Post_Data:
    title: str
    text: str
    url: str
    type: Post_Types
    score: int
    comments: int


async def get_post_by_url(reddit_obj: Reddit, url: str) -> Post_Data:
    """Returns data of reddit post by url

    Args:
        reddit_obj (asyncpraw.Reddit): instance of Reddit object
        url (str): valid link to requsted post

    Returns:
        Post_Data
    """
    post = await reddit_obj.submission(url=url)
    return Post_Data(title=post.title,
                     text=post.selftext,
                     url=post.url,
                     score=post.score,
                     comments=post.num_comments,
                     type=get_post_type(post))


@unique
class Sort_Types(Enum):
    HOT = 'hot'
    TOP = 'top'
    NEW = 'new'
    BEST = 'best'
    RISING = 'rising'
    RANDOM = 'random_rising'


async def get_posts_from_subreddit(
        reddit_obj: Reddit, subreddit: Union[str,
                                             Subreddit], sort_by: Sort_Types,
        quantity: int) -> Optional[Generator[Post_Data, None, None]]:
    if isinstance(subreddit, str):
        try:
            subreddit = await reddit_obj.subreddit(subreddit)
        except Exception as err:
            logging.error(err)
    elif not isinstance(subreddit, Submission):
        raise ValueError

    try:
        async for post in getattr(subreddit, sort_by)(limit=quantity):
            yield Post_Data(title=post.title,
                            text=post.selftext,
                            url=post.url,
                            type=get_post_type(post),
                            score=post.score,
                            comments=post.num_comments)
    except TypeError as err:
        logging.error(err)
        return


# TODO: auth with refreshToken
# def authenticateReddit(client_id, client_secret, user_agent):
#   pass
