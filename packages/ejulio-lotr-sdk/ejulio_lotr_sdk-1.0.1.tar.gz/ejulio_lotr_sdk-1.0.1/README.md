# lotr_sdk

This SDK is a partial wrapper around [The One API](https://the-one-api.dev/).
It is partial because it only works for the `movie` and `quote` endpoints.

To install the sdk

```
pip install ejulio_lotr_sdk
```

Then, you can use it like the following

```
from lotr_sdk.client import Client
from lotr_sdk import fps

client = Client("YOUR API KEY")

for movie in client.get_movies(sorting=fps.Asc("name")):
    print(movie.ID, movie.name)

    if movie.name == "The Two Towers":
        for quote in client.get_movie_quotes(movie.ID):
            print(" ", quote.ID, quote.dialog)

for i in range(1, 3):
    quotes = client.get_quotes(pagination=fps.Page(page=i, limit=10))
    print("Page", i)
    for q in quotes:
        print(q.ID, q.dialog)
```

Under the hood, the SDK is using `requests` to perform the `GET` requests to the API.
Though, the implementation is flexible and allows extensions.

For example, if you want to create a cache for responses.

```
from lotr_sdk.client import Client
from lotr_sdk import fps
from lotr_sdk.http_client import RequestsHttpClient
import requests

class MyClient(RequestsHttpClient):

    _cache = dict()

    def make_request(self, url: str) -> requests.Response:
        cached = self._cache.get(url)
        if cached:
            print("returning from cache")
            return cached

        response = super().make_request(url)
        self._cache[url] = response
        return response


client = Client(MyClient("YOUR API KEY"))

for movie in client.get_movies(filtering=[fps.GreaterThan("academyAwardWins", 8)]):
    print(movie.ID, movie.name)

print("Listing cached movies")

for movie in client.get_movies(filtering=[fps.GreaterThan("academyAwardWins", 8)]):
    print(movie.ID, movie.name)
```

## Documentation

- `lotr_sdk.movie.Movie`
    - `ID`
    - `name`
    - `runtime_in_minutes`
    - `budget_in_millions`
    - `box_office_revenue_in_millions`
    - `academy_award_nominations`
    - `academy_award_wins`
    - `rotten_tomatoes_score`

- `lotr_sdk.quote.Quote`
    - `ID`
    - `dialog`
    - `movie_id`
    - `character_id`

- `lotr_sdk.client.Client(apikey or http_client)`
    - `get_movie(id) -> Movie`
    - `get_quote(id) -> Quote`
    - `get_movies(sorting, pagination, filtering) -> Iterable[Movie]`
    - `get_quotes(sorting, pagination, filtering) -> Iterable[Quote]`
    - `get_movie_quotes(movie_id, sorting, pagination, filtering) -> Iterable[Quote]`

- `lotr_sdk.fps`: For `pagination`, `sorting` and `filtering`
    - `Page(page, offset, limit)`: used to control `pagination` of the endpoints that return lists
    - `Asc(field)`: sorts by the given `field` in `ASC` order
    - `Desc(field)`: sorts by the given `field` in `DESC` order
    - `Match(field, value)`: `field=value`
    - `NotMatch(field, value)`: `field!=value`
    - `Include(field, values)`: `field=value1,value2`
    - `Exclude(field, values)`: `field!=value1,value2`
    - `Exists(field, values)`: `field`
    - `DoesNotExist(field)`: `!field`
    - `LessThan(field, value)`: `field<value`
    - `GreaterThan(field, value)`: `field>value`
    - `GreaterThanOrEqualTo(field, value)`: `field>=value`


- `lotr_sdk.http_client`
    - `UnauthorizedError`: when the response is 401
    - `InternalServerError`: when the response is 500
    - `TooManyRequests`: when the response is 429
    - `RequestsHttpClient`
        - `with_response_handler(status_code, fn(response) -> dict)`: customize how the SDK handles some responses

