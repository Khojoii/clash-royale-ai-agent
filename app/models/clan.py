from pydantic import BaseModel

class Clan(BaseModel):
    tag: str
    name: str
    clanScore: int
    clanWarTrophies: int
    members: int
    type: str
