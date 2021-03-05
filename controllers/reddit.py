import requests
from enum import Enum
from asyncpraw.models import Submission

class Post_Types(Enum):
    TEXT = 0
    PIC = 1
    GIF = 2
    VID = 3
    LINK = 4 
    
supported_types = {
    Post_Types.PIC: {"image/jpeg", "image/png", "image/tiff"},
    Post_Types.GIF: {"image/gif"},
    Post_Types.VID: {"video/mpeg", "video/mp4", "video/webm"}
}

def get_post_type(post :Submission) -> Post_Types:
    if post.is_self:
        return Post_Types.TEXT
    header_type = requests.head(post.url).headers['Content-Type']
    for key, type_headers in supported_types:
        if header_type in type_headers:
            return key
    return Post_Types.LINK
    