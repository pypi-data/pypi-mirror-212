from typing import Callable, Iterable, Optional, Union

from lotr_sdk.fps import QueryString
from lotr_sdk.http_client import HttpClient, RequestsHttpClient
from lotr_sdk.movie import Movie
from lotr_sdk.quote import Quote


class Client:
    _http_client: HttpClient

    def __init__(self, apikey_or_client: Union[str, HttpClient]):
        if isinstance(apikey_or_client, str):
            apikey_or_client = RequestsHttpClient(apikey_or_client)

        self._http_client = apikey_or_client

    def get_movie(self, movie_id: str) -> Movie:
        res = self._get_api_resource(f"movie/{movie_id}", Movie.from_api_response)
        if not res:
            return None
        return res[0]

    def get_movies(
        self,
        sorting: Optional[QueryString] = None,
        pagination: Optional[QueryString] = None,
        filtering: Iterable[QueryString] = [],
    ) -> Iterable[Movie]:
        return self._get_api_resource(
            "movie", Movie.from_api_response, sorting, pagination, filtering
        )

    def get_movie_quotes(
        self,
        movie_id: str,
        sorting: Optional[QueryString] = None,
        pagination: Optional[QueryString] = None,
        filtering: Iterable[QueryString] = [],
    ) -> Iterable[Quote]:
        return self._get_api_resource(
            f"movie/{movie_id}/quote",
            Quote.from_api_response,
            sorting,
            pagination,
            filtering,
        )

    def get_quotes(
        self,
        sorting: Optional[QueryString] = None,
        pagination: Optional[QueryString] = None,
        filtering: Iterable[QueryString] = [],
    ) -> Iterable[Quote]:
        return self._get_api_resource(
            "quote", Quote.from_api_response, sorting, pagination, filtering
        )

    def get_quote(self, quote_id: str) -> Quote:
        res = self._get_api_resource(f"quote/{quote_id}", Quote.from_api_response)
        if not res:
            return None
        return res[0]

    def _get_api_resource(
        self,
        url: str,
        parse: Callable,
        sorting: Optional[QueryString] = None,
        pagination: Optional[QueryString] = None,
        filtering: Iterable[QueryString] = [],
    ) -> Iterable:
        qs = []
        if sorting is not None:
            qs.append(sorting.query_string())

        if pagination is not None:
            qs.append(pagination.query_string())

        for f in filtering:
            qs.append(f.query_string())

        if qs:
            url = f"{url}?{'&'.join(qs)}"

        docs = self._http_client.get(url)["docs"]
        return list(map(parse, docs))
