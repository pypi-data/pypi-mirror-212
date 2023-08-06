from lotr_sdk.quote import Quote

QUOTE_1_FAKE_RESPONSE = {
    "_id": "123",
    "dialog": "this is a test",
    "movie": "456",
    "character": "789",
    "id": "123",
}

QUOTE_2_FAKE_RESPONSE = {
    "_id": "456",
    "dialog": "another fake quote",
    "movie": "987",
    "character": "654",
    "id": "321",
}


def test_from_pai_response():
    q = Quote.from_api_response(QUOTE_1_FAKE_RESPONSE)

    assert q.ID == "123"
    assert q.dialog == "this is a test"
    assert q.movie_id == "456"
    assert q.character_id == "789"
