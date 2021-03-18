import motor.motor_asyncio
from dataclasses import dataclass, asdict
from enum import Enum, unique
from typing import Tuple, Union, List

@dataclass
class UserData:
    user_id: str # telegram chat id for user
    favorites: List[Dict[str, Union[str, bool]]] # list of dicts (subreddit id, locked)
    timezone: int # integer in range [-24:24]
    

class Mongo:

    # TODO: create collection if it dont exist
    # TODO: set index to user_id

    def __init__(self, IP: str, PORT: int):
        self._IP = IP
        self._PORT = PORT

        self._db = motor.motor_asyncio.AsyncIOMotorClient(IP, PORT)['telegram_reddit_bot_db']
        self.user_collection = self._db['user_collection']


    def new_user(self, user_data: UserData):
        try:
            await self.user_collection.insert_one(asdict(user_data))
        except Exception as err:
            logging.error()

    def delete_user(self, user_id: str)
        try:
            await self.user_collection.delete_one({'user_id': user_id})
        except Exception as err:
            logging.error()

    def set_time_zone(self, user_id: str, timezone: int):
        try:
            await self.user_collection.update_one({'user_id': user_id}, 
                                                    {'$set': 
                                                        {'timezone': timezone}
                                                    })
        except Exception as err:
            logging.error()

    def get_favorites(self, user_id: str) -> Union[List[str], None]:
        try:
            await self.user_collection.find_one({'user_id': user_id}, 
                                                {'favorites': 1}).keys()
        except Exception as err:
            logging.error(err)
            return None

        
    def push_favorite(self, user_id: str, sub_name: str, locked: bool = False):
        user_favorites = await self.user_collection.find_one({'user_id': user}, 
                                                             {'favorites': 1}) # Check type of result
        user_favorites

    def lock_favorite(self, user_id: str, sub_name: str):
        try:
            await self.user_collection.update_one({
                                                   'user_id': user_id, 
                                                   'favorites.subreddit': sub_name
                                                  }, 
                                                  {
                                                      '$set': {
                                                        'favorites.$.locked', 
                                                        True
                                                      }
                                                  })
        except Exception as err:
            logging.error(err)

    def unlock_favorite(self, user_id: str, sub_name: str):
                try:
            await self.user_collection.update_one({
                                                   'user_id': user_id, 
                                                   'favorites.subreddit': sub_name
                                                  }, 
                                                  {
                                                      '$set': {
                                                        'favorites.$.locked', 
                                                        False
                                                      }
                                                  })
        except Exception as err:
            logging.error(err)

    # get_subscriptions(user_id)
    # set_feed_interval(feed_interval)
    # set_feed_time(start, end)
    # get_subscribers(time) # returns all user_ids witch have curr_time as feed_time