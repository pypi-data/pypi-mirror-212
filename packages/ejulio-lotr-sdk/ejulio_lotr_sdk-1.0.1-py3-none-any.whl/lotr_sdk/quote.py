from dataclasses import dataclass


@dataclass
class Quote:
    ID: str
    dialog: str
    movie_id: str
    character_id: str

    @staticmethod
    def from_api_response(response: dict) -> "Quote":
        return Quote(
            ID=response["_id"],
            movie_id=response["movie"],
            dialog=response["dialog"],
            character_id=response["character"],
        )
