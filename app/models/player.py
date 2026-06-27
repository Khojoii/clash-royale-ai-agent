# app/models/player.py

from pydantic import BaseModel

class Player(BaseModel):
    tag: str
    name: str
    trophies: int
    expLevel: int
    wins: int
    losses: int