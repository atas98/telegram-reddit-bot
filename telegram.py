from aiogram import Bot, Dispatcher, executor, types

def init(): 
    bot = Bot(token=tg_token)
    disp = Dispatcher(bot=bot)
    
    tg_token = json.load(open('./config.json', 'r'))['telegramToken']
    bot = Bot(token=tg_token)
    disp = Dispatcher(bot=bot)
    
    disp.register_message_handler(start_handler, commands={"start"})
    disp.register_message_handler(help_handler, commands={"help"})
    # disp.register_message_handler(show_handler, commands={"show"})
    # disp.register_message_handler(login_handler, commands={"login"})
    # disp.register_message_handler(logout_handler, commands={"logout"})
    # disp.register_message_handler(subscribe, commands={"subscribe"})
    disp.register_message_handler(text_handler)