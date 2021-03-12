from collections import defaultdict
# TODO: move this stuff to json


def get_language(lang_code: str) -> str:
    langs = defaultdict(lambda: 'en', {'ru': 'ru'})
    return langs[lang_code.split("-")[0]] if lang_code else 'en'


en_text_start = """Hey there, fellow redditor 👋!"""

en_text_help = """
/show - to browse reddit posts. You must specify subreddit, sorting type and quantity of posts to show\
/cancel - to reset your input
\n..or just give me url to reddit post so I can grab it for you"
"""

ru_text_start = """Хей 👋"""

ru_text_help = """Бот для взаимодействия с Реддитом.
/show - возвращает выборку постов. Нужно указать сабреддит, вид сортировки и количество постов.
\tСортировка: [hot, top, new, rising, random]
\tНапример: /show memes top 10
/cancel - что бы сбросить введенные данные
\n..или or just give me url to reddit post so I can grab it for you"
"""

all_strings = {
    "en": {
        "start": en_text_start,
        "help": en_text_help
    },
    "ru": {
        "start": ru_text_start,
        "help": ru_text_help
    }
}
