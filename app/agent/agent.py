import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

from app.logger import get_logger
from app.services.clash_api import set_override_api_key
from app.tools.player import get_player_info as _get_player_info
from app.tools.cards import get_player_cards as _get_player_cards
from app.tools.battles import get_recent_battles as _get_recent_battles

logger = get_logger("agent")
load_dotenv()

PROMPT_PRICE_PER_M = 0.15
COMPLETION_PRICE_PER_M = 0.60

class TokenUsageHandler(BaseCallbackHandler):
    def __init__(self):
        self.total_prompt = 0
        self.total_completion = 0
        self.total_tokens = 0
        self.total_cost = 0.0

    def on_llm_end(self, response: LLMResult, **kwargs):
        usage = (response.llm_output or {}).get("token_usage") or {}
        p = usage.get("prompt_tokens", 0)
        c = usage.get("completion_tokens", 0)
        t = usage.get("total_tokens", 0)
        cost = (p * PROMPT_PRICE_PER_M + c * COMPLETION_PRICE_PER_M) / 1_000_000
        self.total_prompt += p
        self.total_completion += c
        self.total_tokens += t
        self.total_cost += cost
        logger.info(
            "LLM  +%s prompt +%s completion = %s tokens (~$%.5f)  (session: %s prompt, %s completion, %s total)",
            f"{p:,}", f"{c:,}", f"{t:,}", cost,
            f"{self.total_prompt:,}", f"{self.total_completion:,}", f"{self.total_tokens:,}",
        )

SYSTEM_PROMPT = """You are a Clash Royale coaching assistant. Your goal is to help players improve their gameplay.

You have access to these tools:
1. get_player_info(tag) - Get a player's profile (name, trophies, level, wins, losses)
2. get_player_cards(tag) - Get a player's card collection with levels
3. get_recent_battles(tag) - Get a player's recent battle history

When a user gives you their player tag (e.g. #ABC123):
- First call get_player_info to identify the player
- Then call get_player_cards to see their collection
- Then call get_recent_battles to see how they've been performing
- Analyze the data and provide helpful coaching advice

If a tool returns an error (e.g. player not found):
- Tell the user the tag could not be found
- Ask them to double-check their player tag (it starts with # and is case-sensitive)
- Do not guess or modify the tag yourself

When recommending:
- Suggest decks that use their highest-level cards
- Consider card synergies and popular meta decks
- Point out under-leveled cards that could be upgraded
- Give specific, actionable advice based on their battle history

Be concise, friendly, and specific. Ask clarifying questions when needed."""

@tool
def get_player_info(tag: str) -> str:
    """Retrieve a player's profile info by their player tag (e.g. #XXXXXXXXX)."""
    try:
        p = _get_player_info(tag)
        return f"Name: {p.name}, Trophies: {p.trophies}, Level: {p.expLevel}, Wins: {p.wins}, Losses: {p.losses}"
    except Exception as e:
        logger.error("get_player_info failed for %s: %s", tag, e)
        return f"Error: Could not find player '{tag}'. Please verify the tag is correct."

@tool
def get_player_cards(tag: str) -> str:
    """Retrieve a player's card collection by their player tag."""
    try:
        cards = _get_player_cards(tag)
        total = len(cards.items)
        lines = "\n".join(f"{c.name} (Level {c.visual_level()}/{c.visual_max_level()})" for c in cards.items)
        return f"Total cards: {total}\n{lines}"
    except Exception as e:
        logger.error("get_player_cards failed for %s: %s", tag, e)
        return f"Error: Could not find cards for '{tag}'. Please verify the tag is correct."

@tool
def get_recent_battles(tag: str) -> str:
    """Retrieve a player's recent battle history by their player tag."""
    try:
        battles = _get_recent_battles(tag)
        lines = []
        for b in battles:
            team = ", ".join(p.name for p in b.team)
            opponent = ", ".join(p.name for p in b.opponent)
            lines.append(f"[{b.type}] {team} vs {opponent}")
        return "\n".join(lines[-10:])
    except Exception as e:
        logger.error("get_recent_battles failed for %s: %s", tag, e)
        return f"Error: Could not find battle history for '{tag}'. Please verify the tag is correct."

tools = [get_player_info, get_player_cards, get_recent_battles]

_agent_instance = None
_agent_openai_key = None

def create_coach_agent(openai_api_key: str | None = None):
    global _agent_instance, _agent_openai_key
    key = openai_api_key or os.getenv("OPENAI_API_KEY")
    if _agent_instance is not None and _agent_openai_key == key:
        logger.debug("Returning cached agent instance")
        return _agent_instance
    _agent_instance = None
    logger.info("Creating LangChain coach agent with gpt-4o-mini")
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        base_url="https://api.avalai.ir/v1",
        temperature=0,
        api_key=key,
    )
    _agent_instance = create_agent(
        llm,
        tools,
        system_prompt=SYSTEM_PROMPT,
    )
    _agent_openai_key = key
    logger.info("LangChain coach agent created successfully")
    return _agent_instance

def invoke_agent(message: str, history: list[dict] | None = None, openai_api_key: str | None = None, cr_api_key: str | None = None) -> str:
    if cr_api_key:
        set_override_api_key(cr_api_key)
    agent = create_coach_agent(openai_api_key=openai_api_key)
    logger.info("Invoking agent with message: %s", message[:80])

    messages = []
    if history:
        for msg in history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "user":
                messages.append(("human", content))
            elif role == "assistant":
                messages.append(("ai", content))

    messages.append(("human", message))
    handler = TokenUsageHandler()
    result = agent.invoke({"messages": messages}, config={"callbacks": [handler]})
    response = result["messages"][-1].content
    logger.info("Agent response: %s...", response[:80])
    logger.info(
        "=== LLM session: %s prompt + %s completion = %s tokens (est. $%.5f) ===",
        f"{handler.total_prompt:,}", f"{handler.total_completion:,}",
        f"{handler.total_tokens:,}", handler.total_cost,
    )
    return response
