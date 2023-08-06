import pytest

from lotr_sdk import fps


def test_sort_asc():
    asc = fps.Asc("name")
    assert asc.query_string() == "sort=name:asc"


def test_sort_desc():
    desc = fps.Desc("dialog")
    assert desc.query_string() == "sort=dialog:desc"


def test_page():
    page = fps.Page(page=2)
    assert page.query_string() == "page=2"


def test_page_offset_limit():
    page = fps.Page(offset=10, limit=10)
    assert page.query_string() == "offset=10&limit=10"

def test_page_offset_limit():
    page = fps.Page(page=2, offset=10, limit=10)
    assert page.query_string() == "page=2&offset=10&limit=10"

def test_invalid_page_no_args():
    with pytest.raises(ValueError):
        fps.Page()


def test_match():
    m = fps.Match("name", "Gandalf")
    assert m.query_string() == "name=Gandalf"


def test_not_match():
    m = fps.NotMatch("name", "Gandalf")
    assert m.query_string() == "name!=Gandalf"


def test_include():
    m = fps.Include("name", "Gandalf", "Frodo")
    assert m.query_string() == "name=Gandalf,Frodo"


def test_exclude():
    m = fps.Exclude("name", "Gandalf", "Frodo")
    assert m.query_string() == "name!=Gandalf,Frodo"


def test_exists():
    m = fps.Exists("name")
    assert m.query_string() == "name"


def test_does_not_exist():
    m = fps.DoesNotExist("name")
    assert m.query_string() == "!name"


def test_less_than():
    m = fps.LessThan("budgetInMillions", 100)
    assert m.query_string() == "budgetInMillions<100"


def test_greater_than():
    m = fps.GreaterThan("budgetInMillions", 100)
    assert m.query_string() == "budgetInMillions>100"


def test_greater_than_or_equal_to():
    m = fps.GreaterThanOrEqualTo("budgetInMillions", 100)
    assert m.query_string() == "budgetInMillions>=100"
