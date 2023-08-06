import os
import unittest

from the_one_api_sdk.components import base
from the_one_api_sdk.config import SdkConfig


class SdkConfigTest(unittest.TestCase):
    def test_configures_request_for_auth(self):
        config = SdkConfig(auth_token="test")
        request = base.Request(url=config.url, method=base.HttpMethods.GET, path="doesntmatter")
        config.configure_request(request)
        self.assertEquals(request.headers.get("Authorization"), "Bearer test")

    def test_infers_auth_from_env(self):
        os.environ[SdkConfig.THE_ONE_API_TOKEN_KEY] = "test"
        config = SdkConfig()
        self.assertEquals(config.auth_token, "test")

    def test_infer_auth_precedence(self):
        os.environ[SdkConfig.THE_ONE_API_TOKEN_KEY] = "test"
        config = SdkConfig(auth_token="test1")
        self.assertEquals(config.auth_token, "test1")
