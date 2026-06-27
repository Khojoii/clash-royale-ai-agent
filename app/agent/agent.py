import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool

from app.logger import get_logger
from app.tools.player import get_player_info as _get_player_info
from app.tools.cards import get_player_cards as _get_player_cards
from app.tools.battles import get_recent_battles as _get_recent_battles
from app.tools.chests import get_upcoming_chests as _get_upcoming_chests

logger = get_logger("agent")
load_dotenv()

@tool
def get_player_info(tag: str) -> str:
    """Retrieve a player's profile info by their player tag (e.g. #XXXXXXXXX)."""
    p = _get_player_info(tag)
    return f"Name: {p.name}, Trophies: {p.trophies}, Level: {p.expLevel}, Wins: {p.wins}, Losses: {p.losses}"

@tool
def get_player_cards(tag: str) -> str:
    """Retrieve a player's card collection by their player tag."""
    cards = _get_player_cards(tag)
    return "\n".join(f"{c.name} (Level {c.level}/{c.maxLevel})" for c in cards.items)

@tool
def get_recent_battles(tag: str) -> str:
    """Retrieve a player's recent battle history by their player tag."""
    battles = _get_recent_battles(tag)
    lines = []
    for b in battles:
        team = ", ".join(p.name for p in b.team)
        opponent = ", ".join(p.name for p in b.opponent)
        lines.append(f"[{b.type}] {team} vs {opponent}")
    return "\n".join(lines[-10:])

@tool
def get_upcoming_chests(tag: str) -> str:
    """Retrieve a player's upcoming chest cycle by their player tag."""
    chests = _get_upcoming_chests(tag)
    return "\n".join(f"[{c.index}] {c.name}" for c in chests.items)

tools = [get_player_info, get_player_cards, get_recent_battles, get_upcoming_chests]

def create_coach_agent():
    logger.info("Creating LangChain coach agent with gpt-4o-mini")
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        base_url="https://api.avalai.ir/v1",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    agent = create_agent(
        llm,
        tools,
        system_prompt="You are a helpful Clash Royale coaching assistant. "
        "Use the available tools to gather player information and answer the user's questions. "
        "Be concise and informative.",
    )
    logger.info("LangChain coach agent created successfully")
    return agent

agent = None

def simple_agent(user_input: str):
    logger.info("simple_agent called with: %s", user_input[:50])
    if "#" in user_input:
        tag = user_input.split()[-1]
        logger.info("Extracted tag: %s", tag)
        player = _get_player_info(tag)
        logger.info("Returning player info for %s", player.name)
        return f"""
i found the player:
Name: {player.name}
Trophies: {player.trophies}
Level: {player.expLevel}
Wins: {player.wins}
Losses: {player.losses}

How can I help you further?
"""
    logger.warning("No player tag found in input")
    return "Please provide your player tag."
