import abc
from typing import Optional, TypeVar, Iterable, List

from the_one_api_sdk.resources import base, adapters

from the_one_api_sdk.components.base import HttpMethods, Request, Response
from the_one_api_sdk.config import SdkConfig


T = TypeVar("T", bound=base.Resource)


class BaseResourceRequest(abc.ABC):
    def __init__(self, config: SdkConfig):
        self.config = config

    @property
    @abc.abstractmethod
    def path(self) -> str:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def method(self) -> HttpMethods:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def adapter(self) -> adapters.ResponseAdapter:
        raise NotImplementedError()

    def get_request(self) -> Request:
        request = Request(url=self.config.url, path=self.path, method=self.method)
        self.config.configure_request(request)
        return request

    def get_response(self) -> Response:
        return self.config.client.get_response(self.get_request())


class ResourceRequest(BaseResourceRequest, abc.ABC):
    @property
    def method(self) -> HttpMethods:
        return HttpMethods.GET

    def fetch(self) -> Optional:
        response = self.get_response()
        docs = response.to_json().get("docs", [])
        return self.adapter.convert_to_resource(docs[0]) if docs else None

    def stream(self):
        response = self.get_response()
        adapter = self.adapter
        return map(adapter.convert_to_resource, response.to_json().get("docs", []))


class ResourceListRequest(BaseResourceRequest, Iterable[T], abc.ABC):
    def __init__(
            self, config: SdkConfig, limit: int = None, page_size: int = None, offset: int = None, page: int = None
    ):
        super().__init__(config)
        self.limit = limit
        self.page_size = page_size
        self.offset = offset
        self.page = page

    @property
    def method(self) -> HttpMethods:
        return HttpMethods.GET

    def __iter__(self):
        yield from self.stream()

    def fetch(self) -> List[T]:
        return list(self.stream())

    def get_request(self) -> Request:
        request = super().get_request()
        if self.page_size:
            request.query_params["limit"] = self.page_size

        if self.offset:
            request.query_params["offset"] = self.offset

        if self.page:
            request.query_params["page"] = self.page

        return request

    def stream(self) -> Iterable[T]:
        adapter = self.adapter
        return map(adapter.convert_to_resource, self._iterate_entries())

    def _iterate_entries(self):
        page = self.page or 1
        request = self.get_request()
        entries = None
        num_returned = 0

        def _has_reached_limit():
            return self.limit is not None and num_returned >= self.limit

        while entries is None or entries:
            request.query_params["page"] = page

            response = self.config.client.get_response(request)
            entries = response.to_json().get("docs", [])

            for item in entries:
                yield item
                num_returned += 1
                if _has_reached_limit():
                    return

            page += 1
