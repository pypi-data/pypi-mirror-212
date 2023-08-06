from typing import Iterable, Union

from test_movie import LOTR_1_FAKE_RESPONSE, LOTR_2_FAKE_RESPONSE
from test_quote import QUOTE_1_FAKE_RESPONSE, QUOTE_2_FAKE_RESPONSE

from lotr_sdk import fps
from lotr_sdk.client import Client
from lotr_sdk.movie import Movie
from lotr_sdk.quote import Quote


def _make_api_response(docs: Union[dict, Iterable[dict]]) -> dict:
    if isinstance(docs, dict):
        docs = [docs]

    return {"docs": docs, "total": 1, "limit": 1000, "offset": 0, "page": 1, "pages": 1}


class FakeHttpClient:
    _api_responses: dict

    def __init__(self):
        self._api_responses = {
            "movie/123": _make_api_response(LOTR_1_FAKE_RESPONSE),
            "movie": _make_api_response([LOTR_1_FAKE_RESPONSE, LOTR_2_FAKE_RESPONSE]),
            "movie?sort=runtimeInMinutes:desc&page=3&name=/the/i": _make_api_response(
                [LOTR_2_FAKE_RESPONSE, LOTR_1_FAKE_RESPONSE]
            ),
            "movie/missing": _make_api_response([]),
            "quote/123": _make_api_response(QUOTE_1_FAKE_RESPONSE),
            "quote/missing": _make_api_response([]),
            "quote": _make_api_response([QUOTE_1_FAKE_RESPONSE, QUOTE_2_FAKE_RESPONSE]),
            "quote?sort=dialog:desc&page=5&movie!=123": _make_api_response(
                [QUOTE_2_FAKE_RESPONSE, QUOTE_1_FAKE_RESPONSE]
            ),
            "movie/456/quote": _make_api_response([QUOTE_1_FAKE_RESPONSE]),
            "movie/123/quote": _make_api_response([]),
            "movie/123/quote?sort=dialog:asc&page=2&character=123": _make_api_response(
                []
            ),
        }

    def get(self, url) -> dict:
        return self._api_responses[url]


def test_get_movie():
    c = Client(FakeHttpClient())
    movie = c.get_movie("123")

    assert movie == Movie.from_api_response(LOTR_1_FAKE_RESPONSE)


def test_get_missing_movie():
    c = Client(FakeHttpClient())
    movie = c.get_movie("missing")

    assert movie is None


def test_get_movies():
    c = Client(FakeHttpClient())
    movies = c.get_movies()

    assert len(movies) == 2
    assert movies[0] == Movie.from_api_response(LOTR_1_FAKE_RESPONSE)
    assert movies[1] == Movie.from_api_response(LOTR_2_FAKE_RESPONSE)


def test_get_movies_query_string():
    c = Client(FakeHttpClient())
    movies = c.get_movies(
        sorting=fps.Desc("runtimeInMinutes"),
        pagination=fps.Page(page=3),
        filtering=[fps.Match("name", r"/the/i")],
    )

    assert len(movies) == 2
    assert movies[0] == Movie.from_api_response(LOTR_2_FAKE_RESPONSE)
    assert movies[1] == Movie.from_api_response(LOTR_1_FAKE_RESPONSE)


def test_get_quote():
    c = Client(FakeHttpClient())
    quote = c.get_quote("123")

    assert quote == Quote.from_api_response(QUOTE_1_FAKE_RESPONSE)


def test_get_missing_quote():
    c = Client(FakeHttpClient())
    quote = c.get_quote("missing")

    assert quote is None


def test_get_quotes():
    c = Client(FakeHttpClient())
    quotes = c.get_quotes()

    assert len(quotes) == 2
    assert quotes[0] == Quote.from_api_response(QUOTE_1_FAKE_RESPONSE)
    assert quotes[1] == Quote.from_api_response(QUOTE_2_FAKE_RESPONSE)


def test_get_quotes_query_string():
    c = Client(FakeHttpClient())
    quotes = c.get_quotes(
        sorting=fps.Desc("dialog"),
        pagination=fps.Page(page=5),
        filtering=[fps.NotMatch("movie", "123")],
    )

    assert len(quotes) == 2
    assert quotes[0] == Quote.from_api_response(QUOTE_2_FAKE_RESPONSE)
    assert quotes[1] == Quote.from_api_response(QUOTE_1_FAKE_RESPONSE)


def test_get_movie_quotes():
    c = Client(FakeHttpClient())
    quotes = c.get_movie_quotes("456")

    assert len(quotes) == 1
    assert quotes[0] == Quote.from_api_response(QUOTE_1_FAKE_RESPONSE)


def test_get_missing_movie_quotes():
    c = Client(FakeHttpClient())
    quotes = c.get_movie_quotes("123")

    assert len(quotes) == 0


def test_get_movie_quotes_query_string():
    c = Client(FakeHttpClient())
    quotes = c.get_movie_quotes(
        "123",
        sorting=fps.Asc("dialog"),
        pagination=fps.Page(page=2),
        filtering=[fps.Match("character", "123")],
    )
    assert len(quotes) == 0
