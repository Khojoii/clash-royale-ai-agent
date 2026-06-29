import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.logger import get_logger
from app.agent.agent import invoke_agent

logger = get_logger("frontend")

st.set_page_config(page_title="Clash Royale AI Coach", layout="centered")
st.title("Clash Royale AI Coach")

with st.sidebar:
    st.header("Settings")
    with st.expander("API Keys", expanded=False):
        st.caption("Keys provided here override `.env` values.")
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.get("openai_key", ""),
            placeholder="sk-... or aa-...",
            key="openai_key_input",
        )
        cr_key = st.text_input(
            "Clash Royale API Key",
            type="password",
            value=st.session_state.get("cr_key", ""),
            placeholder="eyJ...",
            key="cr_key_input",
        )
        st.session_state.openai_key = openai_key
        st.session_state.cr_key = cr_key

st.markdown("Chat with your AI coach. Share your player tag (e.g. `#XXXXXXXXX`) to get started.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your Clash Royale coach. Share your player tag and I'll help you improve your game."}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask your coach..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            logger.info("User prompt: %s", prompt[:80])
            history = [m for m in st.session_state.messages[:-1] if m["role"] != "system"]
            response = invoke_agent(
                prompt,
                history=history,
                openai_api_key=st.session_state.get("openai_key") or None,
                cr_api_key=st.session_state.get("cr_key") or None,
            )
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
