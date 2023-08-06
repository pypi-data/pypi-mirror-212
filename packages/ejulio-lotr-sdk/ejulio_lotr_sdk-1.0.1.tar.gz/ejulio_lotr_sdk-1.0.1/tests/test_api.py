import os

import pytest

from lotr_sdk import fps
from lotr_sdk.client import Client
from lotr_sdk.http_client import (InternalServerError, TooManyRequests,
                             UnauthorizedError)


def test_api():
    """This is an end to end test to ensure the SDK
    hits the API and handles the responses properly"""
    apikey = os.environ.get("TEST_APIKEY")
    if apikey is None:
        pytest.skip("TEST_APIKEY not set, skipping...")

    with pytest.raises(UnauthorizedError) as e:
        client = Client("wrong-apikey")
        client.get_movies()
        print("unauthorized", e)

    client = Client(apikey)

    with pytest.raises(InternalServerError) as e:
        m = client.get_movie("invalid-movie")
        print("invalid movie", e)

    movies = client.get_movies()
    assert len(movies) > 0
    print("## MOVIES ##\n", movies)

    for movie in filter(lambda x: x.name == "The Two Towers", movies):
        print(movie)

        m = client.get_movie(movie.ID)
        print(m)

        quotes = client.get_movie_quotes(m.ID)
        print(f"## {len(quotes)} QUOTES ##\n", quotes)

    quotes = client.get_quotes()
    assert len(quotes) > 0
    print("## QUOTES ##\n", quotes[:2])

    for quote in quotes[:3]:
        print(quote)

        q = client.get_quote(quote.ID)
        print(q)

    with pytest.raises(TooManyRequests) as e:
        for i in range(200):
            quotes = client.get_quotes(
                sorting=fps.Desc("dialog"),
                pagination=fps.Page(offset=i, limit=1),
            )
            print(quotes)
