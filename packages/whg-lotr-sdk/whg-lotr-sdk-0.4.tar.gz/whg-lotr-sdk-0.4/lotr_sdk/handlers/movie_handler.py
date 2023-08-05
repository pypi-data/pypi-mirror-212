from dataclasses import dataclass
from typing import List
from lotr_sdk.handlers.base_handler import BaseRequestHandler, BaseResponse


@dataclass
class Movie:
    _id: str
    academyAwardNominations: int
    academyAwardWins: int
    boxOfficeRevenueInMillions: int
    budgetInMillions: int
    name: str
    rottenTomatoesScore: int
    runtimeInMinutes: int
    error: str = None


@dataclass
class Movies(BaseResponse):
    docs: List[Movie]

    @property
    def movies(self):
        return self.docs


class MovieHandler(BaseRequestHandler):
    class_type = Movie
    class_type_all = Movies
    url_base = "movie"

    #  Explicitly list possible kwargs for IDE hinting purposes
    def get_all(self, limit=None, page=None, offset=None, sort=None, filter_string=None):
        return self._get_all(self.url_base, limit=limit, page=page, offset=offset, sort=sort, filter_string=filter_string)

    def get_by_id(self, m_id=None):
        return self._get_one(f"{self.url_base}/{m_id}")
