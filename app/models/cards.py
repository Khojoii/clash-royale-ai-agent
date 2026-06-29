from pydantic import BaseModel

class Card(BaseModel):
    id: int
    name: str
    level: int
    maxLevel: int
    iconUrls: dict | None = None

    def visual_level(self) -> int:
        return self.level + (16 - self.maxLevel)

    def visual_max_level(self) -> int:
        return 16

class PlayerCards(BaseModel):
    items: list[Card]
