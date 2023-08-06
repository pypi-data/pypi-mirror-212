import os

from the_one_api_sdk.components.base import Request
from the_one_api_sdk.components.client import Client, get_default


class SdkConfig:
    THE_ONE_API_TOKEN_KEY = "THE_ONE_API_TOKEN"

    def __init__(self, auth_token: str = None, client: Client = None):
        self.auth_token = auth_token or SdkConfig._infer_auth_token()
        self.client = client or get_default()

    @staticmethod
    def _infer_auth_token() -> str:
        return os.getenv(SdkConfig.THE_ONE_API_TOKEN_KEY)

    @property
    def url(self) -> str:
        return f"https://the-one-api.dev/{self.version}"

    @property
    def version(self) -> str:
        return "v2"

    def configure_request(self, request: Request) -> Request:
        if self.auth_token:
            request.headers["Authorization"] = f"Bearer {self.auth_token}"

        return request
