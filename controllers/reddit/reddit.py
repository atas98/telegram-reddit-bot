import logging
from typing import Generator, Optional, Union

import asyncstdlib
import requests
from asyncpraw import Reddit as Redd
from asyncpraw.exceptions import InvalidURL
from asyncpraw.models import Submission, Subreddit
from asyncprawcore import NotFound
from models.reddit import Post_Data, Post_Types, Sort_Types


class Reddit(object):

    supported_types = {
        Post_Types.PIC: {"image/jpeg", "image/png", "image/tiff"},
        Post_Types.GIF: {"image/gif"},
        Post_Types.VID: {"video/mpeg", "video/mp4", "video/webm"}
    }

    def __init__(self, client_id: str, client_secret: str,
                 user_agent: str) -> None:
        self.reddit = Redd(client_id=client_id,
                           client_secret=client_secret,
                           user_agent=user_agent)

    def get_post_type(self, post: Submission) -> Post_Types:
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
        elif hasattr(post, 'is_gallery') and hasattr(
                post, 'media_metadata') and hasattr(
                    post, 'gallery_data') and post.is_gallery:
            return Post_Types.ALB
        elif post.url:
            try:
                header_type = requests.head(post.url).headers['Content-Type']
                for key, supported_headers in self.supported_types.items():
                    if header_type in supported_headers:
                        return key
            except Exception as err:
                logging.warning(err)
            return Post_Types.LINK
        else:
            return Post_Types.UNKNOWN

    async def get_post_by_url(self, url: str) -> Post_Data:
        """Returns data of reddit post by url

        Args:
            reddit_obj (asyncpraw.Reddit): instance of Reddit object
            url (str): valid link to requsted post

        Returns:
            Post_Data
        """
        try:
            post = await self.reddit.submission(url=url)
        except InvalidURL as err:
            raise ValueError(err)
        return Post_Data(id=post.id,
                         title=post.title,
                         text=post.selftext,
                         url=post.url,
                         post_link=self.get_post_link(post),
                         score=post.score,
                         comments=post.num_comments,
                         type=self.get_post_type(post),
                         nsfw=post.over_18,
                         media=getattr(post, "media", None),
                         media_metadata=getattr(post, "media_metadata", None),
                         gallery_data=getattr(post, "gallery_data", None))

    async def get_posts_from_subreddit(
            self,
            subreddit: Union[str, Subreddit],
            sort_by: Sort_Types,
            quantity: int,
            skip: int = 0) -> Optional[Generator[Post_Data, None, None]]:
        if isinstance(subreddit, str):
            try:
                subreddit = await self.reddit.subreddit(subreddit)
            except Exception as err:
                logging.error(err)
        elif not isinstance(subreddit, Submission):
            raise ValueError

        try:
            if sort_by != Sort_Types.RANDOM:
                if not skip:
                    async for post in getattr(subreddit,
                                              sort_by)(limit=quantity):
                        yield Post_Data(
                            id=post.id,
                            title=post.title,
                            text=post.selftext,
                            url=post.url,
                            post_link=self.get_post_link(post),
                            type=self.get_post_type(post),
                            score=post.score,
                            nsfw=post.over_18,
                            comments=post.num_comments,
                            media=getattr(post, "media", None),
                            media_metadata=getattr(post, "media_metadata",
                                                   None),
                            gallery_data=getattr(post, "gallery_data", None))
                elif skip > 0:
                    async for i, post in asyncstdlib.enumerate(
                            getattr(subreddit, sort_by)(limit=quantity)):
                        if i < skip:
                            continue
                        yield Post_Data(
                            id=post.id,
                            title=post.title,
                            text=post.selftext,
                            url=post.url,
                            post_link=self.get_post_link(post),
                            type=self.get_post_type(post),
                            score=post.score,
                            nsfw=post.over_18,
                            comments=post.num_comments,
                            media=getattr(post, "media", None),
                            media_metadata=getattr(post, "media_metadata",
                                                   None),
                            gallery_data=getattr(post, "gallery_data", None))
            else:
                for _ in range(quantity):
                    post = await subreddit.random()
                    yield Post_Data(
                        id=post.id,
                        title=post.title,
                        text=post.selftext,
                        url=post.url,
                        post_link=self.get_post_link(post),
                        type=self.get_post_type(post),
                        nsfw=post.over_18,
                        score=post.score,
                        comments=post.num_comments,
                        media=getattr(post, "media", None),
                        media_metadata=getattr(post, "media_metadata", None),
                        gallery_data=getattr(post, "gallery_data", None))
        except TypeError as err:
            logging.error(err)
            return

    @staticmethod
    def photos_from_album(post: Post_Data) -> Generator[str, None, None]:
        ids = [item['media_id'] for item in post.gallery_data['items']]
        for id in ids:
            url = post.media_metadata[id]['p'][0]['u']
            url = url.split("?")[0].replace("preview", "i")
            yield url

    @staticmethod
    def get_post_link(post: Submission) -> str:
        return "https://www.reddit.com" + post.permalink

    def sub_exists(self, sub):
        exists = True
        try:
            self.reddit.subreddits.search_by_name(sub, exact=True)
        except NotFound:
            exists = False
        return exists
