import praw
import requests
import telegram
from time import sleep

credits = {
    "client_id": "kbxF1_ebddEviw",
    "client_secret": "j2hLcEoKxaYmXZ1EP2Cz9be8YngTag",
    "user_agent": "script by u/atas66"
}
telegramToken = "1646875907:AAGDwEv3EuY67P2ILlsiDkpGO9K4xw2_ssw"

link = "https://www.reddit.com/r/WinStupidPrizes/comments/m1agnx/push_a_woman_win_a_prize_this_is_by_far_the_most/"

r = praw.Reddit(**credits)

post = r.submission(url=link)
headers = requests.head(post.url).headers

print(post.url)
print(post.media)
print(headers['Content-Type'])
print(headers['Content-Length'])

# bot = telegram.Bot(token=telegramToken)

# while True:
#     updates = bot.getUpdates()
#     if updates:
#         for update in updates:
#             chat_id = update.message.chat_id
#             bot.send_message(chat_id, "im here")
#             # bot.send_photo(chat_id, post.url)
#             print(chat_id)
#     sleep(10)