from app.services.clash_api import ClashAPI
from app.models.player import Player
from app.logger import get_logger

logger = get_logger("tool_player")
api = ClashAPI()

def get_player_info(tag: str) -> Player:
    logger.info("Fetching player info for tag=%s", tag)
    try:
        data = api.get_player(tag)
        player = Player(
            tag=data["tag"],
            name=data["name"],
            trophies=data["trophies"],
            expLevel=data["expLevel"],
            wins=data.get("wins", 0),
            losses=data.get("losses", 0),
        )
        logger.info("Found player %s (%d trophies)", player.name, player.trophies)
        return player
    except Exception as e:
        logger.error("Failed to fetch player %s: %s", tag, str(e))
        raise