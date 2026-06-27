from pydantic import BaseModel

class BattlePlayer(BaseModel):
    tag: str
    name: str
    crowns: int
    trophies: int

class Battle(BaseModel):
    type: str
    arena: dict
    team: list[BattlePlayer]
    opponent: list[BattlePlayer]
