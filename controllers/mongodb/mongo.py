 import motor.motor_asyncio

 class Mongo:

    def __init__(IP: str, PORT: int):
        self._IP = IP
        self._PORT = PORT

        self._db = motor.motor_asyncio.AsyncIOMotorClient(IP, PORT)['telegram_reddit_bot_db']

# set_time_zone
# new_user(model)
# delete_user(user_id)
# get_favorites(user_id)
# push_favorite(user_id, sub_name)
# lock_favorite(user_id, sub_name)
# unlock_favorite(user_id, sub_name)
# get_subscriptions(user_id)
# set_feed_interval(feed_interval)
# set_feed_time(start, end)
# get_subscribers(time) # returns all user_ids witch have curr_time as feed_time