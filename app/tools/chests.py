from app.services.clash_api import ClashAPI
from app.models.chests import UpcomingChests
from app.logger import get_logger

logger = get_logger("tool_chests")
api = ClashAPI()

def get_upcoming_chests(tag: str) -> UpcomingChests:
    logger.info("Fetching upcoming chests for tag=%s", tag)
    data = api.get_upcoming_chests(tag)
    items = data.get("items", [])
    result = UpcomingChests(items=[
        {"index": c.get("index"), "name": c.get("name")}
        for c in items
    ])
    logger.info("Found %d upcoming chests for tag=%s", len(result.items), tag)
    return result
