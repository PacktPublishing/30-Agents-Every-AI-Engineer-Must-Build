# Chapter 7: Tool Manipulation and Orchestration Agents

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 7** of *30 Agents Every AI Engineer Must Build*. It teaches three progressive architectural patterns for building production-ready AI agent systems: Tool-Using Agents (single agent extending reasoning via external functions through a Think/Plan/Act cycle), Chain-of-Agents Orchestrators (multiple specialized agents collaborating under a cooperation protocol with shared memory and conflict resolution), and Agentic Workflow Systems (stateful business processes modeled as state machines with human-in-the-loop checkpoints and guard conditions).

Every code cell runs **without an API key** in Simulation Mode, powered by a context-aware `MockLLM` class that returns chapter-derived responses. When an API key is provided (OpenAI, Anthropic, or Google) or Ollama is running locally, the notebook seamlessly switches to Live Mode. Each provider has its own pre-executed notebook variant.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter07

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# 3. Install dependencies
pip install -r requirements.txt

# Then add your provider's dependencies:
pip install -r requirements-openai.txt    # For OpenAI GPT-4o
pip install -r requirements-claude.txt    # For Anthropic Claude Sonnet 4
pip install -r requirements-gemini.txt    # For Google Gemini Flash 2.5
pip install -r requirements-ollama.txt    # For local Ollama (DeepSeek V2)

# 4. (Optional) Configure your LLM provider for Live Mode
cp .env.template .env
# Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY — or use Ollama locally

# 5. Launch the notebook
jupyter notebook Chapter_07_Tool_Orchestration.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | Imports, `.env` loading, `getpass` fallback, Simulation Mode detection |
| **1** | §7.1 — Tool-Using Agent | Tool chest functions, tool registry, data-viz pipeline |
| **2** | §7.2 — Tool Discovery | `parse_query` intent classifier, selection funnel demonstration |
| **3** | §7.3 — Error Handling | `data_viz_agent` orchestrator, `@graceful_fallback` in action |
| **4** | §7.4–7.5 — Chain-of-Agents | NewsAgent, FinancialAgent, SentimentAgent, manager agent, shared memory |
| **5** | §7.6 — Conflict Resolution | `ManagerAgent._synthesize_report()` with `conflict_score` detection |
| **6** | §7.7 — Agentic Workflow (E-Commerce) | `workflow_manager_agent`, HITL simulation with 3 test orders |
| **7** | §7.7b — Agentic Workflow (Insurance) | State machine with 5 agents, guard conditions, CLM-4821 walkthrough |
| **8** | Summary | Recap of all three architectural patterns, pointers to Chapter 8 |

## Real-World Use Case: ShieldPoint Insurance

What does it look like when a regional insurer automates 18,000 claims per month using all three orchestration patterns? The companion case study follows **ShieldPoint Insurance** through tool-using agents for analytics, chain-of-agents for market intelligence with conflict detection, and a 5-agent state-machine claims workflow with HITL gates and full audit trails.

Read the full case study: **[USECASE.md](USECASE.md)** — includes the three test claims (auto-approve, HITL escalation, validation rejection), revenue impact, and integration roadmap.

## Repository Structure

```
chapter07/
│
├── README.md                              # This file
├── LOCAL_LLM_SETUP.md                     # Ollama setup guide (Win/Mac/Linux)
├── AGENTS.md                              # Agentic AI metadata
├── TROUBLESHOOTING.md                     # Dependency conflict resolution guide
├── LICENSE                                # MIT License
├── requirements.txt                       # Base/shared dependencies
├── requirements-openai.txt                # + OpenAI provider deps
├── requirements-claude.txt                # + Anthropic Claude provider deps
├── requirements-gemini.txt                # + Google Gemini provider deps
├── requirements-ollama.txt                # + Local Ollama provider deps
├── .env.template                          # API key template (zero-hardcode policy)
├── .gitignore                             # Standard Python + .env exclusions
│
├── Chapter_07_Tool_Orchestration.ipynb    # Primary deliverable
│
├── helpers/
│   ├── __init__.py                        # Package exports
│   ├── color_logger.py                    # Color-coded visual logging
│   ├── resilience.py                      # @graceful_fallback decorator, safe_invoke()
│   └── mock_llm.py                        # Context-aware MockLLM (6 routes + DEFAULT)
│
├── data/
│   └── sample_ad_campaign.csv             # Synthetic dataset (24 rows, 5 columns)
│
└── outputs/                               # Generated charts (git-ignored)
    └── .gitkeep
```

## Simulation Mode

When no API key is detected, the notebook activates **Simulation Mode**:

- All LLM calls are routed through `MockLLM`, returning chapter-derived mock data
- HITL prompts auto-approve after a 2-second delay
- Every mock response is tagged with a Cyan `[MOCK]` log badge
- The notebook runs to completion with zero external dependencies

API key detection follows a three-tier cascade: `.env` file → environment variable → interactive prompt → Simulation Mode.

## Pre-Executed Notebook Variants

Every notebook is pre-executed with outputs saved. Pick the variant that matches your setup:

| Notebook | Provider | Description |
|---|---|---|
| [ch07_tool_orchestration__RUN_NO_KEY_SIMULATION.ipynb](ch07_tool_orchestration__RUN_NO_KEY_SIMULATION.ipynb) | Simulation | No API key — MockLLM responses |
| [ch07_tool_orchestration__RUN_OPENAI_GPT4o.ipynb](ch07_tool_orchestration__RUN_OPENAI_GPT4o.ipynb) | OpenAI GPT-4o | Live LLM via `OPENAI_API_KEY` |
| [ch07_tool_orchestration__RUN_CLAUDE_Sonnet4.ipynb](ch07_tool_orchestration__RUN_CLAUDE_Sonnet4.ipynb) | Claude Sonnet 4 | Live LLM via `ANTHROPIC_API_KEY` |
| [ch07_tool_orchestration__RUN_GEMINI_Flash25.ipynb](ch07_tool_orchestration__RUN_GEMINI_Flash25.ipynb) | Gemini Flash 2.5 | Live LLM via `GOOGLE_API_KEY` |
| [ch07_tool_orchestration__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb](ch07_tool_orchestration__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb) | Local Ollama | DeepSeek V2 16B — no API key |

All variants produce equivalent output. Compare them to see how different providers handle the same agent tasks.

For local LLM setup instructions (Ollama + DeepSeek on Windows, macOS, and Linux), see **[LOCAL_LLM_SETUP.md](LOCAL_LLM_SETUP.md)**.

For a detailed comparison of how each provider performs on this chapter's tasks — including Bloom's taxonomy ratings, strengths/weaknesses, and per-dimension scores — see **[LLM_COMPARISON.md](LLM_COMPARISON.md)**.

## Resilience Architecture

All agent operations are wrapped in the `@graceful_fallback` decorator:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt` (base) and `requirements-<provider>.txt` for your LLM provider
- **API Key:** Optional — any of OpenAI, Anthropic, Google, or local Ollama. Simulation Mode works without any.

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to common dependency conflicts, environment issues, runtime problems, and platform-specific notes.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
