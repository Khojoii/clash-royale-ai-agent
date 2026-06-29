import sys
import os
import base64
from io import BytesIO
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.logger import get_logger
from app.agent.agent import invoke_agent

logger = get_logger("frontend")

logo_path = os.path.join(os.path.dirname(__file__), "..", "..", "Logo", "CR-agent_logo.png")
if os.path.exists(logo_path):
    img = Image.open(logo_path)
    w, h = img.size
    # header logo (max 150h)
    if h > 150:
        ratio = 150.0 / h
        img_h = img.resize((int(w * ratio), 150), Image.LANCZOS)
    else:
        img_h = img.copy()
    buf_h = BytesIO()
    img_h.save(buf_h, format="PNG")
    LOGO_HEADER = base64.b64encode(buf_h.getvalue()).decode()

    # favicon (32x32)
    img_f = img.resize((32, 32), Image.LANCZOS)
    buf_f = BytesIO()
    img_f.save(buf_f, format="PNG")
    LOGO_FAVICON = base64.b64encode(buf_f.getvalue()).decode()
else:
    LOGO_HEADER = None
    LOGO_FAVICON = None

st.set_page_config(page_title="Clash Royale AI Coach", layout="centered")

favicon_html = ""
if LOGO_FAVICON:
    favicon_html = f'<link rel="icon" href="data:image/png;base64,{LOGO_FAVICON}" type="image/png">'

header_logo_html = ""
if LOGO_HEADER:
    header_logo_html = f'<img src="data:image/png;base64,{LOGO_HEADER}" alt="CR Agent Logo" class="header-logo">'

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    {favicon_html}

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    .stApp {{
        background: linear-gradient(135deg, #0a0e1a 0%, #141b2d 50%, #0d1117 100%);
    }}

    .block-container {{
        padding-top: 1.5rem !important;
    }}

    .main-header {{
        text-align: center;
        padding: 0.5rem 0 0.5rem 0;
        border-bottom: 1px solid rgba(255, 215, 0, 0.15);
        margin-bottom: 1.5rem;
    }}

    .header-logo {{
        height: 80px;
        margin-bottom: 0.25rem;
    }}

    .main-header h1 {{
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: 1px;
        margin: 0;
        background: linear-gradient(135deg, #ffd700 0%, #ffaa00 50%, #ff8800 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    .main-header .subtitle {{
        color: #8892b0;
        font-size: 0.95rem;
        font-weight: 400;
        margin-top: 0.15rem;
        letter-spacing: 0.3px;
    }}

    .status-card {{
        background: linear-gradient(135deg, #1a2035 0%, #1e2740 100%);
        border: 1px solid #2a3350;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
    }}

    .status-card h3 {{
        color: #ccd6f6;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 0 0 0.75rem 0;
        font-weight: 600;
    }}

    .status-item {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.4rem 0;
    }}

    .status-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        flex-shrink: 0;
    }}

    .status-dot.green {{
        background: #3dd68c;
        box-shadow: 0 0 8px rgba(61, 214, 140, 0.5);
    }}

    .status-dot.red {{
        background: #f25b5b;
        box-shadow: 0 0 8px rgba(242, 91, 91, 0.4);
    }}

    .status-label {{
        color: #a8b2d1;
        font-size: 0.85rem;
        font-weight: 500;
    }}

    .status-value {{
        color: #8892b0;
        font-size: 0.75rem;
        margin-left: auto;
    }}

    .sidebar-section {{
        margin-bottom: 1.25rem;
    }}

    .sidebar-section h3 {{
        color: #ccd6f6;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
    }}

    .sidebar-section .section-text {{
        color: #8892b0;
        font-size: 0.8rem;
        line-height: 1.5;
    }}

    .chat-message {{
        padding: 0.75rem 1rem;
        border-radius: 12px;
        margin-bottom: 0.5rem;
        animation: fadeIn 0.3s ease-in;
    }}

    .chat-message.user {{
        background: linear-gradient(135deg, #2a3a6a 0%, #1e3050 100%);
        border: 1px solid rgba(255, 215, 0, 0.1);
    }}

    .chat-message.assistant {{
        background: linear-gradient(135deg, #1a2540 0%, #161e35 100%);
        border: 1px solid rgba(100, 150, 255, 0.08);
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(6px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .loading-container {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 1rem;
        background: linear-gradient(135deg, #1a2540 0%, #161e35 100%);
        border: 1px solid rgba(100, 150, 255, 0.08);
        border-radius: 12px;
        margin-bottom: 0.5rem;
    }}

    .loading-spinner {{
        width: 20px;
        height: 20px;
        border: 2.5px solid rgba(255, 215, 0, 0.15);
        border-top: 2.5px solid #ffd700;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
        flex-shrink: 0;
    }}

    @keyframes spin {{
        to {{ transform: rotate(360deg); }}
    }}

    .loading-dots {{
        display: flex;
        gap: 4px;
    }}

    .loading-dots span {{
        width: 6px;
        height: 6px;
        background: #ffd700;
        border-radius: 50%;
        animation: pulse 1.2s ease-in-out infinite;
    }}

    .loading-dots span:nth-child(2) {{ animation-delay: 0.2s; }}
    .loading-dots span:nth-child(3) {{ animation-delay: 0.4s; }}

    @keyframes pulse {{
        0%, 100% {{ opacity: 0.2; transform: scale(0.8); }}
        50% {{ opacity: 1; transform: scale(1.2); }}
    }}

    .loading-text {{
        color: #8892b0;
        font-size: 0.85rem;
        font-weight: 400;
    }}

    .stChatInputContainer {{
        border: 1px solid #2a3350 !important;
        border-radius: 12px !important;
        background: #1a2035 !important;
    }}

    .stChatInputContainer:focus-within {{
        border-color: #ffd700 !important;
        box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.1) !important;
    }}

    .stChatInputContainer input {{
        color: #ccd6f6 !important;
    }}

    .stChatInputContainer input::placeholder {{
        color: #4a5578 !important;
    }}

    div[data-testid="stChatMessage"] {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-bottom: 0.75rem !important;
    }}

    div[data-testid="stChatMessageContent"] {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        color: #ccd6f6 !important;
    }}

    div[data-testid="stChatMessage"] > div:first-child {{
        display: none;
    }}

    .chat-avatar {{
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        flex-shrink: 0;
    }}

    .chat-avatar.user {{
        background: linear-gradient(135deg, #ffd700, #ff8800);
    }}

    .chat-avatar.assistant {{
        background: linear-gradient(135deg, #4a7dff, #6c5ce7);
    }}

    .chat-row {{
        display: flex;
        gap: 0.75rem;
        align-items: flex-start;
    }}

    .chat-bubble {{
        flex: 1;
        min-width: 0;
    }}

    .stTextInput label, .stTextInput div {{
        color: #8892b0 !important;
    }}

    hr {{
        border-color: rgba(255, 215, 0, 0.08) !important;
        margin: 1rem 0 !important;
    }}

    a {{
        color: #ffd700 !important;
        text-decoration: none !important;
    }}

    a:hover {{
        text-decoration: underline !important;
    }}

    .stAlert {{
        background: #1a2035 !important;
        border: 1px solid #2a3350 !important;
        color: #ccd6f6 !important;
    }}

    .welcome-logo {{
        width: 100px;
        margin-bottom: 1rem;
    }}

    div[data-testid="stChatInput"] {{
        position: fixed;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: min(680px, 100%);
        padding: 0 1rem 1rem 1rem;
        background: linear-gradient(180deg, transparent 0%, #0a0e1a 30%);
        z-index: 100;
    }}

    @media (max-width: 768px) {{
        div[data-testid="stChatInput"] {{
            width: 100%;
        }}
        .main-header h1 {{
            font-size: 1.8rem;
        }}
    }}
</style>
""", unsafe_allow_html=True)

st.markdown(
    f'<div class="main-header">{header_logo_html}'
    '<h1>Clash Royale AI Coach</h1>'
    '<div class="subtitle">Your personal AI-powered battle analyst & deck strategist</div></div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        '<div class="status-card"><h3>🔌 Service Status</h3>'
        f'<div class="status-item"><span class="status-dot {"green" if st.session_state.get("llm_ok") else "red"}"></span>'
        '<span class="status-label">LLM (GPT-4o mini)</span>'
        f'<span class="status-value">{"Connected" if st.session_state.get("llm_ok") else "Not configured"}</span></div>'
        f'<div class="status-item"><span class="status-dot {"green" if st.session_state.get("cr_ok") else "red"}"></span>'
        '<span class="status-label">Clash Royale API</span>'
        f'<span class="status-value">{"Connected" if st.session_state.get("cr_ok") else "Not configured"}</span></div></div>',
        unsafe_allow_html=True,
    )

    with st.expander("🔑 API Keys", expanded=False):
        st.caption("Override `.env` values for this session.")
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.get("openai_key", ""),
            placeholder="sk-... or aa-...",
            key="openai_key_input",
            label_visibility="collapsed",
        )
        cr_key = st.text_input(
            "Clash Royale API Key",
            type="password",
            value=st.session_state.get("cr_key", ""),
            placeholder="eyJ...",
            key="cr_key_input",
            label_visibility="collapsed",
        )
        st.session_state.openai_key = openai_key
        st.session_state.cr_key = cr_key

        if openai_key:
            st.session_state.llm_ok = True
        else:
            st.session_state.llm_ok = bool(os.getenv("OPENAI_API_KEY"))

        if cr_key:
            st.session_state.cr_ok = True
        else:
            st.session_state.cr_ok = bool(os.getenv("CR_API_KEY"))

    st.markdown(
        '<div class="sidebar-section">'
        '<h3>ℹ️ About</h3>'
        '<p class="section-text">This AI coach analyzes your Clash Royale profile, card collection, and battle history to provide personalized deck recommendations and gameplay advice powered by GPT-4o mini.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section">'
        '<h3>💡 Tip</h3>'
        '<p class="section-text">Start by sharing your player tag (e.g. <code>#ABC123</code>) and the coach will analyze your account and suggest improvements.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section">'
        '<p class="section-text" style="font-size:0.7rem; color:#4a5578;">'
        'Clash Royale AI Coach &mdash; Open Source &middot; MIT License'
        '</p></div>',
        unsafe_allow_html=True,
    )

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.llm_ok = bool(os.getenv("OPENAI_API_KEY"))
    st.session_state.cr_ok = bool(os.getenv("CR_API_KEY"))

if not st.session_state.messages:
    welcome_logo = ""
    if LOGO_HEADER:
        welcome_logo = f'<img src="data:image/png;base64,{LOGO_HEADER}" alt="CR Agent Logo" class="welcome-logo">'
    st.markdown(
        f'<div style="text-align:center; padding:3rem 1rem;">'
        f'{welcome_logo}'
        '<div style="color:#8892b0; font-size:1.1rem; font-weight:500; margin-bottom:0.5rem;">'
        'Welcome to Clash Royale AI Coach</div>'
        '<div style="color:#4a5578; font-size:0.9rem; max-width:400px; margin:0 auto;">'
        'Share your player tag and I\'ll analyze your profile, cards, and battles to give you personalized coaching advice.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

for i, msg in enumerate(st.session_state.messages):
    role = msg["role"]
    content = msg["content"]
    avatar_icon = "🫅" if role == "user" else "🤖"
    avatar_class = "user" if role == "user" else "assistant"

    html = (
        f'<div class="chat-row">'
        f'<div class="chat-avatar {avatar_class}">{avatar_icon}</div>'
        f'<div class="chat-message {role} chat-bubble">{content}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

if prompt := st.chat_input("Ask your coach...", key="chat_input"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    avatar_icon = "🫅"
    html = (
        f'<div class="chat-row">'
        f'<div class="chat-avatar user">{avatar_icon}</div>'
        f'<div class="chat-message user chat-bubble">{prompt}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

    loading_placeholder = st.empty()

    loading_html = (
        '<div class="chat-row">'
        '<div class="chat-avatar assistant">🤖</div>'
        '<div class="loading-container">'
        '<div class="loading-spinner"></div>'
        '<div class="loading-dots"><span></span><span></span><span></span></div>'
        '<span class="loading-text">Analyzing your Clash Royale data...</span>'
        '</div>'
        '</div>'
    )
    loading_placeholder.markdown(loading_html, unsafe_allow_html=True)

    try:
        logger.info("User prompt: %s", prompt[:80])
        history = [m for m in st.session_state.messages[:-1] if m["role"] != "system"]
        response = invoke_agent(
            prompt,
            history=history,
            openai_api_key=st.session_state.get("openai_key") or None,
            cr_api_key=st.session_state.get("cr_key") or None,
        )
    except Exception as e:
        logger.error("Agent invocation failed: %s", e)
        response = "Sorry, something went wrong while processing your request. Please check your API keys and try again."
    finally:
        loading_placeholder.empty()

    avatar_icon = "🤖"
    html = (
        f'<div class="chat-row">'
        f'<div class="chat-avatar assistant">{avatar_icon}</div>'
        f'<div class="chat-message assistant chat-bubble">{response}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": response})
