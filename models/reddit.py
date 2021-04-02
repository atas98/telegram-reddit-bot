from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Dict, List


@unique
class Post_Types(Enum):
    TEXT = 0
    PIC = 1
    GIF = 2
    VID = 3
    ALB = 4
    LINK = 5
    UNKNOWN = 6


@unique
class Sort_Types(str, Enum):
    HOT = 'hot'
    TOP = 'top'
    NEW = 'new'
    RISING = 'rising'
    RANDOM = 'random-rising'

    @staticmethod
    def get(input_sortby: str):
        try:
            return Sort_Types.__members__[input_sortby]
        except AttributeError:
            return None


@dataclass
class Post_Data:
    id: str
    title: str
    text: str
    url: str
    post_link: str
    type: Post_Types
    nsfw: bool
    score: int
    comments: int
    media: Dict[str, Any]
    media_metadata: List[Any]
    gallery_data: Dict[str, Any]