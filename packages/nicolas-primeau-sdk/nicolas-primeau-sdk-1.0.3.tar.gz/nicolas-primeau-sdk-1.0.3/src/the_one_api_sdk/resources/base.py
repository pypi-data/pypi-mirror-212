import dataclasses
from typing import Optional


class Resource:
    pass


@dataclasses.dataclass
class Movie(Resource):
    movie_id: str
    name: str
    runtimeInMinutes: Optional[int] = None
    budgetInMillions: Optional[int] = None
    boxOfficeRevenueInMillions: Optional[int] = None
    academyAwardNominations: Optional[int] = None
    academyAwardWins: Optional[int] = None
    rottenTomatoesScore: Optional[int] = None


@dataclasses.dataclass
class Quote(Resource):
    quote_id: str
    dialog: str
    character_id: Optional[str] = None
    movie_id:  Optional[str] = None
