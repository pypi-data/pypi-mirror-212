from dataclasses import dataclass
from typing import List
from lotr_sdk.handlers.base_handler import BaseRequestHandler, BaseResponse


@dataclass
class Quote:
    _id: str
    character: str
    dialog: str
    id: str
    movie: str
    error: str = None


@dataclass
class Quotes(BaseResponse):
    docs: List[Quote]

    @property
    def quotes(self):
        return self.docs


class QuoteHandler(BaseRequestHandler):
    class_type = Quote
    class_type_all = Quotes
    url_base = "quote"

    #  Explicitly list possible kwargs for IDE hinting purposes
    def get_all(self, limit=None, page=None, offset=None, sort=None, filter_string=None):
        return self._get_all(self.url_base, limit=limit, page=page, offset=offset, sort=sort, filter_string=filter_string)

    def get_by_id(self, q_id=None):
        return self._get_one(f"{self.url_base}/{q_id}")

    # while this uses the movie endpoint conceptually it belongs here
    def get_by_movie_id(self, m_id, limit=None, page=None, offset=None, sort=None, filter_string=None):
        return self._get_all(f"movie/{m_id}/quote", limit=limit, page=page, offset=offset, sort=sort, filter_string=filter_string)
