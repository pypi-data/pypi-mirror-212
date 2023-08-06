from lotr_sdk.movie import Movie

LOTR_1_FAKE_RESPONSE = {
    "_id": "123",
    "name": "LOTR",
    "runtimeInMinutes": 1,
    "budgetInMillions": 2,
    "boxOfficeRevenueInMillions": 3,
    "academyAwardNominations": 4,
    "academyAwardWins": 5,
    "rottenTomatoesScore": 6,
}

LOTR_2_FAKE_RESPONSE = {
    "_id": "456",
    "name": "LOTR 2",
    "runtimeInMinutes": 6,
    "budgetInMillions": 5,
    "boxOfficeRevenueInMillions": 4,
    "academyAwardNominations": 3,
    "academyAwardWins": 2,
    "rottenTomatoesScore": 1,
}


def test_from_api_response():
    m = Movie.from_api_response(LOTR_1_FAKE_RESPONSE)

    assert m.ID == "123"
    assert m.name == "LOTR"
    assert m.runtime_in_minutes == 1
    assert m.budget_in_millions == 2
    assert m.box_office_revenue_in_millions == 3
    assert m.academy_award_nominations == 4
    assert m.academy_award_wins == 5
    assert m.rotten_tomatoes_score == 6
