from pydantic import BaseModel

class Chest(BaseModel):
    index: int
    name: str

class UpcomingChests(BaseModel):
    items: list[Chest]
