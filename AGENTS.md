# AGENTS.md — Clash Royale AI Coach

## Commands

```powershell
# FastAPI (port 8000)
python -m uvicorn app.main:app --reload

# Streamlit UI (port 8501) — must run from venv
.\.venv\Scripts\python.exe -m streamlit run app/frontend/app.py --server.port 8501

# Quick agent test (interactive REPL)
python -m app.test_agent

# Verify API connectivity
python -c "from app.tools.player import get_player_info; p = get_player_info('#XXXXXXXXX'); print(p.name)"

# One-shot agent query
python -c "from app.agent.agent import invoke_agent; print(invoke_agent('analyze player #XXXXXXXXX'))"
```

## Architecture

```
app/main.py              → FastAPI entrypoint (root redirects to /docs)
app/backend/routes.py    → API routes under /api prefix (+ POST /api/chat)
app/frontend/app.py      → Streamlit chat UI (uses agent directly)
app/agent/agent.py       → LangChain agent (create_agent, LangGraph-based)
app/services/clash_api.py→ Clash Royale API client
app/tools/               → Tool functions wrapping API calls
app/models/              → Pydantic models (includes chat.py, cards.py)
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
- **Tests**: `python -m pytest tests/ -v` — uses `unittest.mock` to mock the ClashAPI client.
- **`Card.visual_level()`**: `level + (16 - maxLevel)` converts API internal levels to in-game visual levels (all cap at 16). E.g., API `level=10, maxLevel=14` (rare) → visual `12/16`.
- **Agent singleton**: `create_coach_agent()` caches the CompiledStateGraph in `_agent_instance` after first creation.
- **FastAPI agent route**: `POST /api/chat` accepts `{"message": "..."}` and returns `{"response": "..."}`, same logic as direct Python invocation.

## Git Workflow

After completing any implementation:

- Summarize the changes.
- Ask whether this work should be committed now or combined with future changes.
- Never commit automatically.
- Never create branches.
- Never push to any remote repository.
- Never rewrite Git history.

## Logging

Use the project's `logger.py` in every new module and feature.

Log:
- API requests
- Tool execution
- Service calls
- Agent decisions
- External API requests
- Warnings
- Exceptions
- Important state changes

Do not use `print()` for debugging.

Never log:
- API keys
- Secrets
- Tokens
- Sensitive environment variables

## Dependencies

You may install new Python packages if they improve the implementation.

When installing a package:
- Explain why it is needed.
- Prefer actively maintained libraries.
- Avoid unnecessary dependencies.
## Python Version

Target Python version: 3.11

Write code compatible with Python 3.11.
Avoid features introduced in newer Python versions.

## Planning

Before writing code:

1. Briefly explain the implementation plan.
2. Identify the files that will be modified.
3. If requirements are ambiguous, ask for clarification before coding.
4. Modify the minimum number of files necessary.

## Project State

Sprint 1–3 complete per `project_PRD.md`. Roadmap: 6 sprints total. Current deliverable: autonomous AI agent retrieves player data, analyzes card collection & battle history, and generates personalized coaching.
