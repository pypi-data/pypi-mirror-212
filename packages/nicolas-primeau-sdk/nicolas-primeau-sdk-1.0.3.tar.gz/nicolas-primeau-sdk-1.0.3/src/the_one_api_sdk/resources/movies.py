from the_one_api_sdk.components.requests import ResourceListRequest, ResourceRequest
from the_one_api_sdk.resources import adapters, base, quotes
from the_one_api_sdk.config import SdkConfig


class MovieListRequest(ResourceListRequest[base.Movie]):
    @property
    def path(self) -> str:
        return "movie"

    @property
    def adapter(self):
        return adapters.MovieResponseAdapter()


class MovieRequest(ResourceRequest):
    def __init__(self, config: SdkConfig, movie_id: str):
        super().__init__(config)
        self.movie_id = movie_id

    @property
    def path(self) -> str:
        return f"movie/{self.movie_id}"

    @property
    def adapter(self):
        return adapters.MovieResponseAdapter()

    def quotes(self) -> quotes.QuoteListRequest:
        return quotes.QuoteListRequest(self.config, movie_id=self.movie_id)


class MoviesRequest:
    def __init__(self, config: SdkConfig):
        self.config = config

    def __call__(self, movie_id: str) -> MovieRequest:
        return MovieRequest(self.config, movie_id)

    def list(self, **kwargs) -> MovieListRequest:
        return MovieListRequest(self.config, **kwargs)
