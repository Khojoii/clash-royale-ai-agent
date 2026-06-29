from fastapi import APIRouter
from app.logger import get_logger
from app.tools.player import get_player_info
from app.tools.cards import get_player_cards
from app.tools.battles import get_recent_battles
from app.agent.agent import invoke_agent
from app.models.chat import ChatRequest, ChatResponse

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

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    logger.info("POST /chat: %s", request.message[:80])
    history = [{"role": m.role, "content": m.content} for m in request.history]
    response = invoke_agent(request.message, history=history)
    return ChatResponse(response=response)

@router.get("/health")
def health():
    return {"status": "ok"}
