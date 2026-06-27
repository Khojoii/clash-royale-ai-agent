from app.services.clash_api import ClashAPI
from app.models.clan import Clan
from app.logger import get_logger

logger = get_logger("tool_clan")
api = ClashAPI()

def get_clan_info(tag: str) -> Clan:
    logger.info("Fetching clan info for tag=%s", tag)
    data = api.get_clan(tag)
    result = Clan(
        tag=data.get("tag", ""),
        name=data.get("name", ""),
        clanScore=data.get("clanScore", 0),
        clanWarTrophies=data.get("clanWarTrophies", 0),
        members=data.get("members", 0),
        type=data.get("type", ""),
    )
    logger.info("Found clan %s (%d members)", result.name, result.members)
    return result
