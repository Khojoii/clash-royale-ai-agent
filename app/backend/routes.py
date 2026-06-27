from fastapi import APIRouter
from app.logger import get_logger
from app.tools.player import get_player_info
from app.tools.cards import get_player_cards
from app.tools.battles import get_recent_battles
from app.tools.chests import get_upcoming_chests

logger = get_logger("routes")
router = APIRouter()

@router.get("/player/{tag}")
def player_info(tag: str):
    logger.info("GET /player/%s", tag)
    return get_player_info(tag)

@router.get("/player/{tag}/cards")
def player_cards(tag: str):
    logger.info("GET /player/%s/cards", tag)
    return get_player_cards(tag)

@router.get("/player/{tag}/battles")
def player_battles(tag: str):
    logger.info("GET /player/%s/battles", tag)
    return get_recent_battles(tag)

@router.get("/player/{tag}/chests")
def player_chests(tag: str):
    logger.info("GET /player/%s/chests", tag)
    return get_upcoming_chests(tag)

@router.get("/health")
def health():
    return {"status": "ok"}
