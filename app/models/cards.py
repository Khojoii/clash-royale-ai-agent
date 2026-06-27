from pydantic import BaseModel

class Card(BaseModel):
    id: int
    name: str
    level: int
    maxLevel: int
    iconUrls: dict | None = None

class PlayerCards(BaseModel):
    items: list[Card]
