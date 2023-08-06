from os import path
from typing import Callable, Dict, Protocol

import requests


class HttpClient(Protocol):
    def get(self, url: str) -> dict:
        """Performs a HTTP GET request and returns the parsed result"""


class UnauthorizedError(Exception):
    apikey: str
    response_text: str

    def __init__(self, apikey: str, response_text: str):
        self.apikey = apikey
        self.response_text = response_text


class InternalServerError(Exception):
    response_text: str

    def __init__(self, response_text: str):
        self.response_text = response_text


class TooManyRequests(Exception):
    response_text: str
    ratelimit_limit: int
    ratelimit_reset: int
    retry_after: int

    def __init__(self, response_text: str, limit: int, reset: int, retry: int):
        self.response_text = response_text
        self.ratelimit_limit = limit
        self.ratelimit_reset = reset
        self.retry_after = retry


response_handler = Callable[[dict], requests.Response]


class RequestsHttpClient:
    _apikey: str
    _base_url: str = "https://the-one-api.dev/v2/"
    _handlers: Dict[int, response_handler]

    def __init__(self, apikey: str):
        if not apikey or not apikey.strip():
            raise ValueError("invalid apikey")

        self._apikey = apikey
        self._handlers = dict()
        self.with_response_handler(200, self._handle_200)
        self.with_response_handler(401, self._handle_401)
        self.with_response_handler(429, self._handle_429)
        self.with_response_handler(500, self._handle_500)

    def get(self, url: str) -> dict:
        return self.handle_response(self.make_request(url))

    def make_request(self, url: str) -> requests.Response:
        return requests.get(
            path.join(self._base_url, url),
            headers={"Authorization": f"Bearer {self._apikey}"},
        )

    def with_response_handler(
        self, status_code: int, handler: response_handler
    ) -> None:
        self._handlers[status_code] = handler

    def handle_response(self, response: requests.Response) -> dict:
        handler = self._handlers.get(response.status_code)
        if not handler:
            raise ValueError(
                f"unknown response handler for status code {response.status_code}: {response.text}"
            )

        return handler(response)

    def _handle_200(self, response: requests.Response) -> dict:
        return response.json()

    def _handle_401(self, response: requests.Response) -> dict:
        raise UnauthorizedError(f"{self._apikey[:5]}...", response.text)

    def _handle_500(self, response: requests.Response) -> dict:
        raise InternalServerError(response.text)

    def _handle_429(self, response: requests.Response) -> dict:
        raise TooManyRequests(
            response.text,
            response.headers.get("X-RateLimit-Limit"),
            response.headers.get("X-RateLimit-Reset"),
            response.headers.get("Retry-After"),
        )
