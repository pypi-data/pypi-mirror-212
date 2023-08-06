import json

import pytest
from test_client import _make_api_response
from test_movie import LOTR_1_FAKE_RESPONSE

from lotr_sdk.http_client import (InternalServerError, RequestsHttpClient,
                             TooManyRequests, UnauthorizedError)


def test_get(requests_mock):
    response = _make_api_response(LOTR_1_FAKE_RESPONSE)
    requests_mock.get("https://the-one-api.dev/v2/movie/123", text=json.dumps(response))
    http = RequestsHttpClient("apikey-123")

    result = http.get("movie/123")

    assert result == response
    assert requests_mock.last_request.headers["Authorization"] == "Bearer apikey-123"


def test_invalid_apikey():
    with pytest.raises(ValueError):
        RequestsHttpClient("")


def test_handle_401(requests_mock):
    requests_mock.get(
        "https://the-one-api.dev/v2/movie/123", status_code=401, text="response 401"
    )
    http = RequestsHttpClient("bad-api-key")

    with pytest.raises(UnauthorizedError) as e:
        http.get("movie/123")

        assert e.apikey == "bad-a..."
        assert e.response_text == "response 401"


def test_handle_500(requests_mock):
    requests_mock.get(
        "https://the-one-api.dev/v2/movie/123", status_code=500, text="response 500"
    )
    http = RequestsHttpClient("api-key")

    with pytest.raises(InternalServerError) as e:
        http.get("movie/123")
        assert e.response_text == "response 500"


def test_handle_429(requests_mock):
    requests_mock.get(
        "https://the-one-api.dev/v2/movie/123",
        status_code=429,
        text="response 429",
        headers={
            "X-RateLimit-Limit": "100",
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": "1685881627",
            "Retry-After": "600",
        },
    )
    http = RequestsHttpClient("api-key")

    with pytest.raises(TooManyRequests) as e:
        http.get("movie/123")

        assert e.response_text == "response 429"
        assert e.ratelimit_limit == 100
        assert e.ratelimit_reset == 1685881627
        assert e.retry_after == 600


def test_unknown_handler(requests_mock):
    requests_mock.get("https://the-one-api.dev/v2/movie/123", status_code=404)
    http = RequestsHttpClient("api-key")

    with pytest.raises(ValueError):
        http.get("movie/123")
