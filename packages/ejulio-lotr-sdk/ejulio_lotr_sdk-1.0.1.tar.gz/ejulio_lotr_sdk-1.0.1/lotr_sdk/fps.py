from typing import Iterable, Optional, Protocol


class QueryString(Protocol):
    def query_string(self) -> str:
        """Returns the query string representation of filter, sort or page"""
        pass


class _Sort:
    _field: str
    _order: str

    def __init__(self, field: str, order: str):
        self._field = field
        self._order = order

    def query_string(self) -> str:
        return f"sort={self._field}:{self._order}"


class Asc(_Sort):
    def __init__(self, field: str):
        super().__init__(field, "asc")


class Desc(_Sort):
    def __init__(self, field: str):
        super().__init__(field, "desc")


class Page:
    _page: Optional[int]
    _limit: Optional[int]
    _offset: Optional[int]

    def __init__(
        self,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        if page is None and offset is None and limit is None:
            raise ValueError("you must set 'page' or 'limit' and 'offset'")

        self._page = page
        self._limit = offset
        self._offset = limit

    def query_string(self) -> str:
        qs = []
        if self._page is not None:
            qs.append(f"page={self._page}")

        if self._offset is not None:
            qs.append(f"offset={self._offset}")

        if self._limit is not None:
            qs.append(f"limit={self._limit}")

        return "&".join(qs) 


class Filter:
    _field: str
    _operator: str
    _value: str

    def __init__(self, field: str, operator: str, value: str):
        self._field = field
        self._operator = operator
        self._value = value

    def query_string(self) -> str:
        return f"{self._field}{self._operator}{self._value}"


class Match(Filter):
    def __init__(self, field: str, value: str):
        super().__init__(field, "=", value)


class NotMatch(Filter):
    def __init__(self, field: str, value: str):
        super().__init__(field, "!=", value)


class Include(Filter):
    def __init__(self, field: str, *values: Iterable[str]):
        super().__init__(field, "=", ",".join(values))


class Exclude(Filter):
    def __init__(self, field: str, *values: Iterable[str]):
        super().__init__(field, "!=", ",".join(values))


class Exists(Filter):
    def __init__(self, field: str):
        super().__init__(field, "", "")


class DoesNotExist:
    _field: str

    def __init__(self, field: str):
        self._field = field

    def query_string(self) -> str:
        return f"!{self._field}"


class LessThan(Filter):
    def __init__(self, field: str, value: int):
        super().__init__(field, "<", str(value))


class GreaterThan(Filter):
    def __init__(self, field: str, value: int):
        super().__init__(field, ">", str(value))


class GreaterThanOrEqualTo(Filter):
    def __init__(self, field: str, value: int):
        super().__init__(field, ">=", str(value))
