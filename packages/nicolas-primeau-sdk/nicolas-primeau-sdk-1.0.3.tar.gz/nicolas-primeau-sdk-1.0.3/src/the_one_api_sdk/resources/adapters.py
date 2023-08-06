import abc
from typing import Dict

from the_one_api_sdk.resources import base


class ResponseAdapter(abc.ABC):
    @abc.abstractmethod
    def convert_to_resource(self, response: Dict) -> base.Resource:
        raise NotImplementedError()


class MovieResponseAdapter(ResponseAdapter):
    def convert_to_resource(self, response_data: Dict) -> base.Movie:
        return base.Movie(
            movie_id=response_data["_id"],
            name=response_data["name"],
            runtimeInMinutes=response_data.get("runtimeInMinutes"),
            budgetInMillions=response_data.get("budgetInMillions"),
            boxOfficeRevenueInMillions=response_data.get("boxOfficeRevenueInMillions"),
            academyAwardNominations=response_data.get("academyAwardNominations"),
            academyAwardWins=response_data.get("academyAwardWins"),
            rottenTomatoesScore=response_data.get("rottenTomatoesScore"),
        )


class QuoteResponseAdapter(ResponseAdapter):
    def convert_to_resource(self, response_data: Dict) -> base.Quote:
        return base.Quote(
            quote_id=response_data["_id"],
            dialog=response_data["dialog"],
            character_id=response_data.get("character"),
            movie_id=response_data.get("movie")
        )
