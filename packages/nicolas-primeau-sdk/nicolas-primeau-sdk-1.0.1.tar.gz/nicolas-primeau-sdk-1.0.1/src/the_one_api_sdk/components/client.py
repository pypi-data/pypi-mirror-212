import abc

import requests

from the_one_api_sdk import exceptions
from the_one_api_sdk.components import base


class UnsupportedHttpMethodException(exceptions.TheOneApiSDKException):
    pass


class Client(abc.ABC):
    @abc.abstractmethod
    def get_response(self, request: base.Request) -> base.Response:
        raise NotImplementedError()


class RequestsClient(Client):
    def get_response(self, request: base.Request) -> base.Response:
        requests_response = requests.request(
            method=request.method,
            url=request.full_url,
            headers=request.headers,
            params=request.query_params,
            data=request.body
        )
        response = base.Response(
            request=request,
            headers=dict(requests_response.headers),
            content=requests_response.text,
            status_code=requests_response.status_code
        )
        if not (200 <= response.status_code < 300):
            raise exceptions.RestExceptionHandler.get_exception(response)
        return response


def get_default() -> Client:
    return RequestsClient()
