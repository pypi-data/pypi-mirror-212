from the_one_api_sdk.components import base


class TheOneApiSDKException(Exception):
    pass


class TheOneApiSDKRestException(TheOneApiSDKException):
    def __init__(self, *args, response: base.Response):
        super().__init__(*args)
        self.response = response


class UnauthorizedError(TheOneApiSDKRestException):
    def __init__(self, response: base.Response):
        super().__init__("Request not authorized", response=response)


class RestExceptionHandler:
    @classmethod
    def get_exception(cls, response: base.Response):
        match response.status_code:
            case 401:
                return UnauthorizedError(response)
            case _:
                return TheOneApiSDKRestException(f"API returned code {response.status_code}", response=response)
