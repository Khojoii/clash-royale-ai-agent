# 🏆 Clash Royale AI Coach

> An AI-powered autonomous coaching agent for Clash Royale — analyzes your account, recommends decks, and explains its reasoning using LLM-driven tool calling.

## ✨ Features

- 🔍 **Player Analysis** — Fetch profile, card collection, and battle history from the official Clash Royale API
- 🤖 **AI-Powered Coaching** — LangChain agent (LangGraph-based) with GPT-4o mini decides which tools to call and generates personalized advice
- 💬 **Explainable Recommendations** — Every suggestion includes reasoning based on your actual card levels and battle history
- 🌐 **Dual Interface** — FastAPI backend (`POST /api/chat`) + Streamlit chat UI
- 🔑 **API Key Override** — Set OpenAI and Clash Royale keys directly in the Streamlit sidebar (overrides `.env`)
- 💰 **Token Cost Tracking** — Per-session LLM token usage and estimated cost logged automatically
- 🧩 **Extensible Tool System** — Drop-in tool modules following single-responsibility principle
- ✅ **Tested** — 14 unit tests covering all models and tools

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| AI Framework | LangChain (LangGraph-based `create_agent`) |
| LLM | GPT-4o mini (via `langchain-openai`) |
| Data Validation | Pydantic |
| External API | [Clash Royale API](https://developer.clashroyale.com) |
| Testing | pytest + unittest.mock |

## 🏗 Architecture

```
User
  │
  ├── Streamlit UI (:8501) ──► LangChain Agent (direct import)
  │
  └── FastAPI (:8000) ──► POST /api/chat ──► LangChain Agent
                              │
                         ┌────┴─────┐
                         │  Agent   │
                         │  (GPT-4o)│
                         └────┬─────┘
                              │
               ┌──────────────┼──────────────┐
               ▼              ▼              ▼
          get_player     get_cards      get_battles
          (profile)    (collection)     (history)
               │              │              │
               └──────────────┼──────────────┘
                              ▼
                    ┌──────────────────┐
                    │  Clash Royale    │
                    │  API Client      │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │  Official API    │
                    │  (api.clashroyale│
                    │   .com/v1)       │
                    └──────────────────┘
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- [Clash Royale API key](https://developer.clashroyale.com) (free)
- OpenAI API key (or compatible endpoint)

### Installation

```powershell
git clone https://github.com/Khojoii/clash-royale-ai-agent
cd clash-royale-ai-agent
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Configuration

Create `.env` in the project root:

```env
CR_API_KEY=your_clash_royale_api_key
OPENAI_API_KEY=your_openai_api_key
```

Alternatively, set both keys at runtime via the Streamlit sidebar (Settings > API Keys).

### Run

**Terminal 1 — FastAPI backend:**
```powershell
python -m uvicorn app.main:app --reload
# → http://127.0.0.1:8000/docs
```

**Terminal 2 — Streamlit frontend (must run from venv):**
```powershell
.\.venv\Scripts\python.exe -m streamlit run app/frontend/app.py --server.port 8501
# → http://127.0.0.1:8501
```

**Quick test (REPL):**
```powershell
python -m app.test_agent
```

**One-shot agent query:**
```powershell
python -c "from app.agent.agent import invoke_agent; print(invoke_agent('analyze player #XXXXXXXXX'))"
```

### Testing

```powershell
python -m pytest tests/ -v
# 14 tests covering all Pydantic models and tool functions
```

## 📁 Project Structure

```
app/
├── agent/          # LangChain agent with tool registration
│   └── agent.py    # — create_coach_agent(), invoke_agent(), TokenUsageHandler
├── backend/        # FastAPI route handlers
│   └── routes.py   # — POST /api/chat, health check
├── frontend/       # Streamlit chat UI (sys.path workaround for import)
│   └── app.py      # — chat interface + sidebar API key inputs
├── models/         # Pydantic data models
│   ├── player.py
│   ├── cards.py    # — Card.visual_level() converts API → in-game levels
│   ├── battle.py
│   ├── chat.py     # — chat request/response models
│   └── clan.py     # — unused (wired but not imported)
├── services/       # Clash Royale API client
│   └── clash_api.py# — per-call key resolution, override support
├── tools/          # LangChain tool implementations
│   ├── player.py   # — get_player_info
│   ├── cards.py    # — get_player_cards
│   ├── battles.py  # — get_recent_battles
│   └── clan.py     # — unused
├── logger.py       # Rotating file logger → LOG/app.log
├── main.py         # FastAPI entrypoint (root → /docs)
└── test_agent.py   # Interactive agent test REPL
```

## 🗺 Roadmap

| Sprint | Status | Goal |
|--------|--------|------|
| 1 — Foundation | ✅ Done | FastAPI + Streamlit + LangChain + API client |
| 2 — Core Tools | ✅ Done | Pydantic models, tool functions, 14 unit tests |
| 3 — AI Agent | ✅ Done | Autonomous agent with singleton caching, error handling, multi-turn chat |
| 4 — AI Coaching | ⬜ Pending | Deck recommendations, upgrade guidance, scoring |
| 5 — Web Application | ⬜ Pending | Conversation persistence, loading states, error UI |
| 6 — Open Source | ⬜ Pending | Docs, screenshots, examples, GitHub release |

## 💡 Key Design Decisions

- **Card levels**: API returns internal levels; `visual_level = level + (16 - maxLevel)` converts to in-game visual levels (all cap at `/16`).
- **Singleton agent**: `create_coach_agent()` caches the `CompiledStateGraph` across invocations, re-creating only if the API key changes.
- **Error handling**: Tool functions catch exceptions and return friendly error strings so the LLM can guide the user gracefully.
- **Token tracking**: Custom `TokenUsageHandler` (via `langchain_core` callbacks) logs per-turn and per-session token counts with estimated cost.
- **No `print()`**: All logging goes through the project's rotating file logger (`app/logger.py` → `LOG/app.log`).

## 📄 License

MIT
