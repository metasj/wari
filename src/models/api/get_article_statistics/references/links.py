from typing import List

from pydantic import BaseModel

from src.models.wikimedia.wikipedia.url import WikipediaUrl


class Links(BaseModel):
    """The purpose of this class is to model the statistics
    the user wants from the get_article_statistics endpoint

    We use BaseModel to avoid the cache attribute"""

    all: int = 0
    s200: int = 0
    s404: int = 0
    s5xx: int = 0
    other: int = 0
    details: List[WikipediaUrl] = []