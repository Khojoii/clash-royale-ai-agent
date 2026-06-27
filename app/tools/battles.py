from app.services.clash_api import ClashAPI
from app.models.battle import Battle
from app.logger import get_logger

logger = get_logger("tool_battles")
api = ClashAPI()

def get_recent_battles(tag: str) -> list[Battle]:
    logger.info("Fetching recent battles for tag=%s", tag)
    data = api.get_recent_battles(tag)
    battles = []
    for b in data:
        battle = Battle(
            type=b.get("type", ""),
            arena=b.get("arena", {}),
            team=[_parse_player(p) for p in b.get("team", [])],
            opponent=[_parse_player(p) for p in b.get("opponent", [])],
        )
        battles.append(battle)
    logger.info("Found %d recent battles for tag=%s", len(battles), tag)
    return battles

def _parse_player(p: dict):
    return {
        "tag": p.get("tag", ""),
        "name": p.get("name", ""),
        "crowns": p.get("crowns", 0),
        "trophies": p.get("startingTrophies", 0),
    }
