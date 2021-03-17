# from typing import List

# model = {
#     "user_id": str,
#     "favorites": List[str] # list of sub ids + locked field
#     "subcription_space": int
#     "subscriptions": List[str] # list of sub ids
#     "subcription_space": int
#     "feed_interval": int # half'a'hour/hour/2/4 - enum?
#     "feed_time_start": int # utc time
#     "feed_time_end": int # utc time
#     "time_zone": int
# }

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