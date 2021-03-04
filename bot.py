import json
import asyncio
import logging
import telegram
from handlers import *


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(filename='dump.log', level=logging.DEBUG)
    
    telegramToken, reddit = json.load(open('./config.json', 'r'))
    
    executor = telegram.init(telegramToken)
    
    executor.start_polling(disp, skip_updates=True)
    







# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(message.chat.id, 'Hey there fellow redditor')
    
# @bot.message_handler(commands=['help'])
# def start_message(message):
#     bot.send_message(message.chat.id, 'To use bot type valid subreddit name or paste link to post (e.g. r/all)')

# @bot.message_handler(content_types=['text'])
# def get_text_messages(message): 
#     command, *props = message.text.split()
#     command = command.lower()
    
#     for post in commands[command](*props): 
#         bot.send_message(message.from_user.id, post)

# if __name__ == '__main__':
#     print("Polling...")
#     bot.polling(none_stop=True, interval=0)