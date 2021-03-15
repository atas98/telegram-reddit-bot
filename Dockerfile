FROM python:3

WORKDIR /telegram-reddit-bot

COPY requirements.txt /telegram-reddit-bot/
RUN pip install -r /telegram-reddit-bot/requirements.txt
COPY . /telegram-reddit-bot/

CMD python3 /telegram-reddit-bot/bot.py