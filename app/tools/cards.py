from app.services.clash_api import ClashAPI
from app.models.cards import PlayerCards
from app.logger import get_logger

logger = get_logger("tool_cards")
api = ClashAPI()

def get_player_cards(tag: str) -> PlayerCards:
    logger.info("Fetching cards for tag=%s", tag)
    data = api.get_player_cards(tag)
    cards = data.get("cards", [])
    result = PlayerCards(items=[
        {
            "id": c.get("id"),
            "name": c.get("name"),
            "level": c.get("level"),
            "maxLevel": c.get("maxLevel"),
            "iconUrls": c.get("iconUrls"),
        }
        for c in cards
    ])
    logger.info("Found %d cards for tag=%s", len(result.items), tag)
    return result
