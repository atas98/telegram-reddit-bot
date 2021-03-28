from collections import defaultdict


def get_language(lang_code: str) -> str:
    langs = defaultdict(lambda: 'en', {'ru': 'ru'})
    return langs[lang_code.split("-")[0]] if lang_code else 'en'


en_text_start = """Hey there, fellow redditor 👋!"""

en_text_help = """
/show - to browse reddit posts. You must specify subreddit, sorting type and quantity of posts to show\
\tSubreddit: [memes, r/ThisIsNotASubreddit, r/gifs, worldnews, spaceporn]
\tSortby: [hot, top, new, rising, random]
\tQuantity: [1, 3, 5] (max 10)
\tE.g.: /show memes top 10
/cancel - to reset your input
\n..or just give me url (or urls) to reddit post so I can grab it for you"
\n\tGitHub: https://github.com/atas98/telegram-reddit-bot
"""

en_input_inv_subreddit = "Subreddit:"
en_input_inv_sortby = "Sortby:"
en_input_inv_quanitity = "Quantity:"

en_error_wrong_args = "Oopsie, wrong arguments here 🤨"
en_error_file_2_big = "Step Dad, what are u doing!? Its too big!! 🤯 "
en_error_wrong_post_type = "Hey, thats illegal! (post type) 👮 "
en_error_wrong_input = "What are u trying to tell me? I dont understand 😠 ! You can try again or fuck yourself"
en_error_video = "Sorry, but im not support reddit hosted videos yet 😔"

ru_text_start = """Хей 👋"""

ru_text_help = """Бот для взаимодействия с Реддитом.
/show - возвращает выборку постов. Нужно указать сабреддит, вид сортировки и количество постов.
\tСабреддит: [memes, r/ThisIsNotASubreddit, r/gifs, worldnews, spaceporn]
\tСортировка: [hot, top, new, rising, random]
\tКоличество: [1, 3, 5] (максимум 10)
\tНапример: /show memes top 10
/cancel - что бы сбросить введенные данные
..или просто поделись ссылкой (или ссылками) на пост"
\n\tGitHub: https://github.com/atas98/telegram-reddit-bot
"""

ru_input_inv_subreddit = "Сабреддит:"
ru_input_inv_sortby = "Сортировка:"
ru_input_inv_quantity = "Количество:"

ru_error_wrong_args = "Ууупс, неправильные параметры 🤨"
ru_error_file_2_big = "Файл слишком большой!! 🤯 "
ru_error_wrong_post_type = "Я незнаю что это за пост! 👮 "
ru_error_wrong_input = "Ничего не понял, можешь повторить?"
ru_error_video = "Сори, но я еще пока не поддерживаю видео с реддита 😔"

all_strings = {
    "en": {
        "start": en_text_start,
        "help": en_text_help,
        "input_inv_subreddit": en_input_inv_subreddit,
        "input_inv_sortby": en_input_inv_sortby,
        "input_inv_quantity": en_input_inv_quanitity,
        "error_wrong_args": en_error_wrong_args,
        "error_file_2_big": en_error_file_2_big,
        "error_wrong_post_type": en_error_wrong_post_type,
        "error_wrong_input": en_error_wrong_input,
        "error_video": en_error_video
    },
    "ru": {
        "start": ru_text_start,
        "help": ru_text_help,
        "input_inv_subreddit": ru_input_inv_subreddit,
        "input_inv_sortby": ru_input_inv_sortby,
        "input_inv_quantity": ru_input_inv_quanitity,
        "error_wrong_args": ru_error_wrong_args,
        "error_file_2_big": ru_error_file_2_big,
        "error_wrong_post_type": ru_error_wrong_post_type,
        "error_wrong_input": ru_error_wrong_input,
        "error_video": ru_error_video
    }
}
