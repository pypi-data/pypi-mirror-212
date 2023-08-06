from dataclasses import dataclass


@dataclass
class Movie:
    ID: str
    name: str
    runtime_in_minutes: float
    budget_in_millions: float
    box_office_revenue_in_millions: float
    academy_award_nominations: int
    academy_award_wins: int
    rotten_tomatoes_score: int

    @staticmethod
    def from_api_response(response: dict) -> "Movie":
        return Movie(
            ID=response["_id"],
            name=response["name"],
            runtime_in_minutes=response["runtimeInMinutes"],
            budget_in_millions=response["budgetInMillions"],
            box_office_revenue_in_millions=response["boxOfficeRevenueInMillions"],
            academy_award_nominations=response["academyAwardNominations"],
            academy_award_wins=response["academyAwardWins"],
            rotten_tomatoes_score=response["rottenTomatoesScore"],
        )
