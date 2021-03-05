import json
from pathlib import Path
from dataclasses import dataclass
from .dataclass_from_dict import dataclass_from_dict

@dataclass
class RedditCredits:
    client_id :str
    user_agent :str
    client_secret :str

@dataclass
class Settings:
    telegramToken :str
    reddit :RedditCredits

def load_config(path :Path) -> Settings:
    return dataclass_from_dict(json.load(open(path, 'r')))