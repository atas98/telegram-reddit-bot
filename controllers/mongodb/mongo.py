import logging
from motor.motor_asyncio import AsyncIOMotorClient
from dataclasses import dataclass, asdict
from enum import Enum, unique
from typing import Union, List, Dict


@dataclass
class UserData:
    user_id: str  # telegram chat id for user
    favorites: List[Dict[str,
                         Union[str,
                               bool]]]  # list of dicts (subreddit id, locked)
    timezone: int  # integer in range [-24:24]


class Mongo:

    # TODO: create collection if it dont exist
    # TODO: set index to user_id

    def __init__(self, IP: str, PORT: int):
        self._IP = IP
        self._PORT = PORT

        self._db = AsyncIOMotorClient(IP, PORT)['telegram_reddit_bot_db']
        self.user_collection = self._db['user_collection']

    async def new_user(self, user_data: UserData):
        try:
            await self.user_collection.insert_one(asdict(user_data))
        except Exception as err:
            logging.error(err)

    async def delete_user(self, user_id: str):
        try:
            await self.user_collection.delete_one({'user_id': user_id})
        except Exception as err:
            logging.error(err)

    async def set_time_zone(self, user_id: str, timezone: int):
        try:
            await self.user_collection.update_one(
                {'user_id': user_id}, {'$set': {
                    'timezone': timezone
                }})
        except Exception as err:
            logging.error(err)

    async def get_favorites(self, user_id: str) -> Union[List[str], None]:
        try:
            return await self.user_collection.find_one({
                'user_id': user_id
            }, {
                'favorites': 1
            }).keys()
        except Exception as err:
            logging.error(err)
            return None

    async def push_favorite(self,
                            user_id: str,
                            sub_id: str,
                            locked: bool = False):
        user_favorites = await self.user_collection.find_one(
            {'user_id': user_id},
            {'favorites': 1})['favorites'
                             ]  # TODO: Check type of result (list or dict)
        user_favorites = user_favorites.pop(0).append(sub_id, locked)
        await self.user_collection.update_one(
            {'user_id': user_id}, {'$set': {
                'favorites': user_favorites
            }})

    async def lock_favorite(self, user_id: str, sub_name: str):
        try:
            await self.user_collection.update_one(
                {
                    'user_id': user_id,
                    'favorites.subreddit': sub_name
                }, {'$set': {'favorites.$.locked', True}})
        except Exception as err:
            logging.error(err)

    async def unlock_favorite(self, user_id: str, sub_name: str):
        try:
            await self.user_collection.update_one(
                {
                    'user_id': user_id,
                    'favorites.subreddit': sub_name
                }, {'$set': {'favorites.$.locked', False}})
        except Exception as err:
            logging.error(err)

    # get_subscriptions(user_id)
    # set_feed_interval(feed_interval)
    # set_feed_time(start, end)
    # get_subscribers(time) # returns all user_ids witch have curr_time as feed_time