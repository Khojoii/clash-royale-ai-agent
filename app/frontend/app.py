import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.logger import get_logger
from app.tools.player import get_player_info
from app.tools.cards import get_player_cards
from app.tools.battles import get_recent_battles
from app.tools.chests import get_upcoming_chests

logger = get_logger("frontend")

st.set_page_config(page_title="Clash Royale AI Coach", layout="centered")
st.title("Clash Royale AI Coach")
st.markdown("Enter your player tag to get started.")

tag = st.text_input("Player Tag", placeholder="#C2C0L2QLR")

if st.button("Analyze") and tag:
    logger.info("User requested analysis for tag=%s", tag)
    with st.spinner("Fetching player data..."):
        try:
            player = get_player_info(tag)
            cards = get_player_cards(tag)
            battles = get_recent_battles(tag)
            chests = get_upcoming_chests(tag)
        except Exception as e:
            st.error(f"Failed to fetch data: {e}")
            logger.error("Analysis failed for tag=%s: %s", tag, str(e))
            st.stop()

    logger.info("Displaying data for player %s", player.name)
    st.subheader(f"Player: {player.name}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Trophies", player.trophies)
    col2.metric("Level", player.expLevel)
    col3.metric("Wins", player.wins)
    col4.metric("Losses", player.losses)

    with st.expander("Cards"):
        for c in cards.items:
            st.write(f"{c.name} — Level {c.level}/{c.maxLevel}")

    with st.expander("Recent Battles"):
        for b in battles[-5:]:
            st.write(f"{b.type} — Team: {b.team[0].name} vs {b.opponent[0].name}")

    with st.expander("Upcoming Chests"):
        for c in chests.items:
            st.write(f"[{c.index}] {c.name}")
