# Clash Royale AI Coaching Agent

## Product Requirements Document (PRD)

| Field | Value |
|--------|-------|
| **Version** | 1.0 |
| **Status** | Draft |
| **Date** | 2026-06-26 |
| **Project Type** | Open Source AI Agent |
| **License** | MIT |

---

# 1. Vision

Build an AI-powered Clash Royale coach capable of understanding a player's account, reasoning over their collection and battle history, and recommending personalized decks through autonomous tool usage.

Unlike traditional deck recommendation websites, this project focuses on **Agentic AI**. The LLM should decide which tools to call, gather information, ask follow-up questions when necessary, and generate explainable recommendations.

The project is intended as both an educational AI Agent project and a production-quality open-source application.

---

# 2. Objectives

- Build a real Tool-Calling AI Agent.
- Learn and demonstrate Agentic AI architecture.
- Integrate the official Clash Royale API.
- Generate personalized deck recommendations.
- Produce explainable reasoning.
- Build a clean, modular, and extensible project.

---

# 3. Target Users

### Ladder Players

Players who want to maximize ladder performance using their current card collection.

### Free-to-Play Players

Players who need efficient upgrade recommendations with limited gold and resources.

### Returning Players

Players returning after balance changes who need help adapting to the current meta.

---

# 4. MVP Features

## Player Analysis

- Retrieve player profile
- Retrieve player card collection
- Retrieve recent battle history

## AI Coaching

- Personalized deck recommendations
- Deck ranking
- Upgrade priority recommendations
- Explainable reasoning
- Follow-up questions when needed

---

# 5. Technology Stack

| Layer | Technology |
|--------|------------|
| Language | Python 3.11+ |
| Backend | FastAPI |
| Frontend | Streamlit |
| AI Framework | LangChain |
| LLM | GPT-4o mini |
| LLM Integration | langchain-openai |
| Tool Framework | LangChain Tools (`@tool`) |
| Data Validation | Pydantic |
| HTTP Client | Requests |
| External API | Official Clash Royale API |
| Environment | python-dotenv |

### Future Technologies

- Redis
- Docker
- LangSmith
- Memory
- MCP
- RAG

---

# 6. High-Level Architecture

```text
User
    │
    ▼
Streamlit UI
    │
    ▼
FastAPI
    │
    ▼
LangChain Agent
    │
    ├──────────────┐
    ▼              ▼
Reasoning      Tool Calling
                    │
                    ▼
         Clash Royale Tools
                    │
                    ▼
      Official Clash Royale API
```

---

# 7. Project Structure

```text
clash-royale-ai-agent/

│
├── app/
│
│   ├── agent/
│   │      agent.py
│   │
│   ├── api/
│   │      routes.py
│   │
│   ├── models/
│   │      player.py
│   │      cards.py
│   │      battle.py
│   │
│   ├── services/
│   │      clash_api.py
│   │
│   ├── tools/
│   │      player.py
│   │      cards.py
│   │      battles.py
│   │    
│   │
│   └── main.py
│
├── frontend/
│      app.py
│
├── .env
├── requirements.txt
└── README.md
```

---

# 8. Agent Workflow

Example request:

> I'm player #ABC123. Help me build a deck.

### Workflow

1. Extract player tag.
2. Call `get_player_info()`.
3. Call `get_player_cards()`.
4. Call `get_recent_battles()`.
5. Analyze collected information.
6. Ask follow-up questions if required.
7. Recommend the best decks.
8. Explain the reasoning.
9. Suggest upgrade priorities.

---

# 9. Tool Design Principles

Each API capability should be implemented as an independent LangChain Tool.

Example tools:

- `get_player_info()`
- `get_player_cards()`
- `get_recent_battles()`
- `get_clan_info()`
- `get_card_information()`

Every tool should:

- Perform one task only.
- Return Pydantic models.
- Be reusable.
- Contain no AI logic.
- Contain no business logic beyond its own responsibility.

---

# 10. Design Principles

- Modular Architecture
- Tool-Oriented Design
- Strong Typing
- Pydantic Models
- Separation of Concerns
- Single Responsibility Principle
- Extensible Architecture
- Clean Code

---

# 11. Out of Scope (v1)

- Mobile application
- Authentication
- Clan analytics
- Tournament optimization
- Live battle assistance
- Screen capture
- Multiplayer collaboration

---

# 12. Success Metrics

| Metric | Target |
|---------|--------|
| Response Time | < 5 seconds |
| Personalized Recommendations | Based on player's collection |
| Explainability | Every recommendation includes reasoning |
| Extensibility | New tools can be added easily |
| Open Source Quality | Production-ready GitHub repository |

---

# 13. Sprint Roadmap

## Sprint 1 — Foundation

### Goal

Create the project foundation.

### Tasks

- Initialize repository
- Configure virtual environment
- Configure FastAPI
- Configure Streamlit
- Configure LangChain
- Configure GPT-4o mini
- Configure environment variables
- Build Clash Royale API client
- Test API connectivity

### Deliverable

Player information can be successfully retrieved from the official API.

---

## Sprint 2 — Core Tools

### Goal

Build reusable tools.

### Tasks

- Implement `get_player_info()`
- Implement `get_player_cards()`
- Implement `get_recent_battles()`
- Create Pydantic models
- Write unit tests

### Deliverable

All core tools return structured Pydantic models.

---

## Sprint 3 — AI Agent

### Goal

Create the first autonomous AI Agent.

### Tasks

- Build LangChain Agent
- Register tools
- Prompt engineering
- Tool calling
- Multi-step reasoning

### Deliverable

The agent autonomously retrieves player information and selects appropriate tools.

---

## Sprint 4 — AI Coaching

### Goal

Generate personalized coaching.

### Tasks

- Analyze card collection
- Analyze battle history
- Score decks
- Recommend decks
- Explain reasoning
- Suggest upgrade priorities

### Deliverable

The agent behaves as a personalized Clash Royale coach.

---

## Sprint 5 — Web Application

### Goal

Create the first usable application.

### Tasks

- FastAPI endpoints
- Streamlit interface
- Chat interface
- Conversation history
- Error handling
- Loading states

### Deliverable

Complete end-to-end AI coaching application.

---

## Sprint 6 — Open Source Release

### Goal

Prepare the public release.

### Tasks

- Improve README
- Installation guide
- Screenshots
- Examples
- Documentation
- Code cleanup
- GitHub release

### Deliverable

Production-ready open-source project.

---

# 14. Long-Term Vision

Transform the project into a complete AI coaching platform capable of:

- Advanced reasoning
- Multi-tool planning
- Multiple LLM providers
- Memory
- RAG
- MCP
- Community-contributed tools
- Community-contributed recommendation strategies

while remaining modular, educational, and fully open source.