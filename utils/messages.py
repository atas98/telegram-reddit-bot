from collections import defaultdict


def get_language(lang_code: str) -> str:
    langs = defaultdict(lambda: 'en', {'ru': 'ru'})
    return langs[lang_code.split("-")[0]] if lang_code else 'en'


en_text_start = """Hey there, fellow redditor 👋!"""

en_text_help = """"I can't help your meanenless life 😞, but I can show my commads instead 😀 !\
\n\t/show - to browse reddit posts \
\n\t/login - to use reddit account 🚫 \
\n\t/logout - to stop using all cool personized features 🚫 \
\n\t/subscribe - to tell me that you need this memes regulary 🚫 \
\n..or just give me url to reddit post so I can grab it for you"
"""

ru_text_start = """Хей 👋"""

ru_text_help = """Здесь таак пусто..."""

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