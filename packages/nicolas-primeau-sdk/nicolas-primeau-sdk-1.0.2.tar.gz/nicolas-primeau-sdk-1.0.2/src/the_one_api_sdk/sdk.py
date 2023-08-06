from the_one_api_sdk.resources import quotes, movies
from the_one_api_sdk.config import SdkConfig


class TheOneApiSdk:
    def __init__(self, config: SdkConfig = None):
        self._config = config or SdkConfig()

    @property
    def movies(self) -> movies.MoviesRequest:
        return movies.MoviesRequest(self._config)

    @property
    def quotes(self) -> quotes.QuotesRequest:
        return quotes.QuotesRequest(self._config)
