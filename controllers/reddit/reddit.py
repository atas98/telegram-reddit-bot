import logging
import requests
import typing

from asyncpraw import Reddit
from asyncpraw.models import Submission, Subreddit
from asyncpraw.exceptions import InvalidURL
from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Generator, Optional, Union


@unique
class Post_Types(Enum):
    TEXT = 0
    PIC = 1
    GIF = 2
    VID = 3
    ALB = 4
    LINK = 5
    UNKNOWN = 6


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
    elif hasattr(post, 'is_video') and post.is_video:
        return Post_Types.VID
    elif hasattr(post,
                 'is_gallery') and hasattr(post, 'media_metadata') and hasattr(
                     post, 'gallery_data') and post.is_gallery:
        return Post_Types.ALB
    elif post.url:
        try:
            header_type = requests.head(post.url).headers['Content-Type']
            for key, supported_headers in supported_types.items():
                if header_type in supported_headers:
                    return key
        except Exception as err:
            logging.warning(err)
        return Post_Types.LINK
    else:
        return Post_Types.UNKNOWN


# TODO: Move all dataclasses/enums to separate file
# TODO: add id field
@dataclass
class Post_Data:
    title: str
    text: str
    url: str
    type: Post_Types
    score: int
    comments: int
    media_metadata: typing.List[Any]
    gallery_data: typing.Dict[str, Any]


async def get_post_by_url(reddit_obj: Reddit, url: str) -> Post_Data:
    """Returns data of reddit post by url

    Args:
        reddit_obj (asyncpraw.Reddit): instance of Reddit object
        url (str): valid link to requsted post

    Returns:
        Post_Data
    """
    try:
        post = await reddit_obj.submission(url=url)
    except InvalidURL as err:
        raise ValueError(err)
    return Post_Data(title=post.title,
                     text=post.selftext,
                     url=post.url,
                     score=post.score,
                     comments=post.num_comments,
                     type=get_post_type(post),
                     media_metadata=getattr(post, "media_metadata", None),
                     gallery_data=getattr(post, "gallery_data", None))


@unique
class Sort_Types(Enum):
    HOT = 'hot'
    TOP = 'top'
    NEW = 'new'
    RISING = 'rising'
    RANDOM = 'random_rising'

    @staticmethod
    def get(input_sortby: str):
        try:
            return Sort_Types.__members__[input_sortby]
        except AttributeError:
            return None


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
        if sort_by != Sort_Types.RANDOM:
            async for post in getattr(subreddit,
                                      sort_by.value)(limit=quantity):
                yield Post_Data(title=post.title,
                                text=post.selftext,
                                url=post.url,
                                type=get_post_type(post),
                                score=post.score,
                                comments=post.num_comments,
                                media_metadata=getattr(post, "media_metadata",
                                                       None),
                                gallery_data=getattr(post, "gallery_data",
                                                     None))
        else:
            for _ in range(quantity):
                post = await subreddit.random()
                yield Post_Data(title=post.title,
                                text=post.selftext,
                                url=post.url,
                                type=get_post_type(post),
                                score=post.score,
                                comments=post.num_comments,
                                media_metadata=getattr(post, "media_metadata",
                                                       None),
                                gallery_data=getattr(post, "gallery_data",
                                                     None))
    except TypeError as err:
        logging.error(err)
        return


def photos_from_album(post: Post_Data) -> Generator[str, None, None]:
    ids = [item['media_id'] for item in post.gallery_data['items']]
    for id in ids:
        url = post.media_metadata[id]['p'][0]['u']
        url = url.split("?")[0].replace("preview", "i")
        yield url


# TODO: auth with refreshToken
# def authenticateReddit(client_id, client_secret, user_agent):
#   pass
