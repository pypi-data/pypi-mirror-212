import json
import unittest

from test import utils
from the_one_api_sdk.components import base
from the_one_api_sdk.config import SdkConfig
from the_one_api_sdk.resources.base import Movie, Quote
from the_one_api_sdk.sdk import TheOneApiSdk


class TheOneApiSdkTest(unittest.TestCase):
    def test_list_movies(self):
        config = SdkConfig(client=utils.MockClient(
            responses=[
                base.Response(
                    request=None,
                    content=json.dumps({
                        "docs": [
                            {"_id": "a", "name": "test"},
                            {"_id": "b", "name": "test2"}
                        ]
                    }),
                    status_code=200
                ),
                base.Response(request=None, content=json.dumps({"docs": []}), status_code=200)
            ]
        ))
        sdk = TheOneApiSdk(config=config)
        self.assertEquals(len(list(sdk.movies.list())), 2)

    def test_get_movie(self):
        config = SdkConfig(client=utils.MockClient(
            responses=[
                base.Response(
                    request=None, content=json.dumps({"docs": [{"_id": "a", "name": "test"}]}), status_code=200
                ),
                base.Response(request=None, content=json.dumps({"docs": []}), status_code=200)
            ]
        ))
        sdk = TheOneApiSdk(config=config)
        self.assertEquals(sdk.movies("a").fetch(), Movie(movie_id="a", name="test"))

    def test_get_quotes(self):
        config = SdkConfig(client=utils.MockClient(
            responses=[
                base.Response(
                    request=None,
                    content=json.dumps({
                        "docs": [
                            {"_id": "a", "dialog": "test"},
                            {"_id": "b", "dialog": "test2"}
                        ]
                    }),
                    status_code=200
                ),
                base.Response(request=None, content=json.dumps({"docs": []}), status_code=200)
            ]
        ))
        sdk = TheOneApiSdk(config=config)
        self.assertEquals(len(list(sdk.quotes.list())), 2)

    def test_get_quote(self):
        config = SdkConfig(client=utils.MockClient(
            responses=[
                base.Response(
                    request=None,
                    content=json.dumps({
                        "docs": [
                            {"_id": "a", "dialog": "test"},
                        ]
                    }),
                    status_code=200
                ),
                base.Response(request=None, content=json.dumps({"docs": []}), status_code=200)
            ]
        ))
        sdk = TheOneApiSdk(config=config)
        self.assertEquals(sdk.quotes("a").fetch(), Quote(quote_id="a", dialog="test"))

    def test_get_quote_from_movie(self):
        config = SdkConfig(client=utils.MockClient(
            responses=[
                base.Response(
                    request=None,
                    content=json.dumps({
                        "docs": [
                            {"_id": "a", "dialog": "test"},
                            {"_id": "b", "dialog": "test2"}
                        ]
                    }),
                    status_code=200
                ),
                base.Response(request=None, content=json.dumps({"docs": []}), status_code=200)
            ]
        ))
        sdk = TheOneApiSdk(config=config)
        self.assertEquals(len(list(sdk.movies("a").quotes())), 2)
