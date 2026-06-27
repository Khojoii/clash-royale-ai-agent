# 🏆 Clash Royale AI Coach

> An AI-powered autonomous coaching agent for Clash Royale — analyzes your account, recommends decks, and explains its reasoning using LLM-driven tool calling.

## ✨ Features

- 🔍 **Player Analysis** — Fetch profile, card collection, battle history, and chest cycle
- 🤖 **AI-Powered Coaching** — LangChain agent with GPT-4o mini decides which tools to call
- 💬 **Explainable Recommendations** — Every suggestion includes reasoning
- 🌐 **Dual Interface** — FastAPI backend + Streamlit frontend
- 🧩 **Extensible Tool System** — Drop-in tool modules following single-responsibility principle

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| AI Framework | LangChain (LangGraph-based) |
| LLM | GPT-4o mini (via langchain-openai) |
| Data Validation | Pydantic |
| External API | [Clash Royale API](https://developer.clashroyale.com) |

## 🏗 Architecture

```
User
  │
  ▼
┌─────────────┐     ┌──────────┐
│ Streamlit   │────▶│ FastAPI  │
│ UI (:8501)  │     │ (:8000)  │
└─────────────┘     └────┬─────┘
                         │
                    ┌────▼─────┐
                    │ LangChain│
                    │  Agent   │
                    └────┬─────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
         get_player  get_cards  get_battles
              │          │          │
              └──────────┼──────────┘
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
git clone <repo>
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
PLAYER_TAG=#XXXXXXXXX
```

### Run

**Terminal 1 — FastAPI backend:**
```powershell
python -m uvicorn app.main:app --reload
# → http://127.0.0.1:8000/docs
```

**Terminal 2 — Streamlit frontend:**
```powershell
streamlit run app/frontend/app.py --server.port 8501
# → http://127.0.0.1:8501
```

**Quick test (REPL):**
```powershell
python -m app.test_agent
```

## 📁 Project Structure

```
app/
├── agent/          # LangChain agent with tool registration
│   └── agent.py
├── backend/        # FastAPI route handlers
│   └── routes.py
├── frontend/       # Streamlit UI
│   └── app.py
├── models/         # Pydantic data models
│   ├── player.py
│   ├── cards.py
│   ├── battle.py
│   ├── chests.py
│   └── clan.py
├── services/       # Clash Royale API client
│   └── clash_api.py
├── tools/          # LangChain tool implementations
│   ├── player.py
│   ├── cards.py
│   ├── battles.py
│   ├── chests.py
│   └── clan.py
├── logger.py       # Rotating file logger → LOG/app.log
├── main.py         # FastAPI entrypoint
└── test_agent.py   # Interactive agent test REPL
```

## 🗺 Roadmap

| Sprint | Status | Goal |
|--------|--------|------|
| 1 — Foundation | ✅ Done | FastAPI + Streamlit + LangChain + API client |
| 2 — Core Tools | ⬜ Pending | Structured tools + Pydantic models + tests |
| 3 — AI Agent | ⬜ Pending | Autonomous tool-calling agent |
| 4 — Coaching | ⬜ Pending | Deck recommendations + upgrade guidance |
| 5 — Web App | ⬜ Pending | Full chat interface + conversation history |
| 6 — Open Source | ⬜ Pending | Docs, cleanup, GitHub release |

## 📄 License

MIT
