# AGENTS.md — Clash Royale AI Coach

## Commands

```powershell
# FastAPI (port 8000)
python -m uvicorn app.main:app --reload

# Streamlit UI (port 8501)
streamlit run app/frontend/app.py --server.port 8501

# Quick agent test (interactive REPL)
python -m app.test_agent

# Verify API connectivity
python -c "from app.tools.player import get_player_info; p = get_player_info('#XXXXXXXXX'); print(p.name)"
```

## Architecture

```
app/main.py              → FastAPI entrypoint (root redirects to /docs)
app/backend/routes.py    → API routes under /api prefix
app/frontend/app.py      → Streamlit UI
app/agent/agent.py       → LangChain agent (create_agent, LangGraph-based)
app/services/clash_api.py→ Clash Royale API client
app/tools/               → Tool functions wrapping API calls
app/models/              → Pydantic models
app/logger.py            → Rotating file logger → LOG/app.log
```

## Quirks & Gotchas

- **Streamlit import conflict**: `app/frontend/app.py` conflicts with the `app/` package. The file adds `sys.path.insert(0, ...)` at the top to work around it. Do not rename the file without fixing this.
- **LangChain version**: Uses `langchain.agents.create_agent` (LangGraph-based, returns `CompiledStateGraph`). The old `create_tool_calling_agent` and `AgentExecutor` do not exist in this version.
- **`get_player_cards`**: Calls the same `/players/{tag}` endpoint as `get_player` — the card data is extracted from the `cards` key in the response.
- **`ClashAPI`** is instantiated per module (5× on import) — not a singleton. Harmless but noisy in logs.
- **LLM config**: `agent.py` has a custom `base_url` for `ChatOpenAI` (https://api.avalai.ir/v1). Change if using official OpenAI.
- **`.env`** requires `CR_API_KEY` and `OPENAI_API_KEY`.
- **Python 3.14+**: Pydantic V1 compat warning on every import — cosmetic, can be ignored.
- **Dead code**: `app/tools/clan.py` + `app/models/clan.py` are wired but not imported anywhere.
- **No test framework or lint config** configured yet.

## Project State

Sprint 1 (Foundation) complete per `project_PRD.md`. Roadmap: 6 sprints total. Current deliverable: player data retrievable from official Clash Royale API.
