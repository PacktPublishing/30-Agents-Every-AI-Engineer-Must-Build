# Chapter 1: Foundations of Agent Engineering

**Book:** *AI Agents* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 1** of *AI Agents*. It transforms the chapter's theoretical foundations into runnable Python code, covering the cognitive loop, agent brain patterns, interoperability protocols, interaction paradigms, the Agentic AI Progression Framework, and real-world business case studies.

Every code cell runs **without an API key** in Simulation Mode, powered by a `MockLLM` engine that returns chapter-derived responses. When an API key is provided (OpenAI, Anthropic, or Google) or Ollama is running locally, the notebook seamlessly switches to Live Mode. Each provider has its own pre-executed notebook variant.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter01

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
jupyter notebook ch01_foundations_of_agent_engineering.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | Imports, API key detection, mode selection |
| **1** | §1.1 — Introducing Agents | Timeline of AI agent evolution (four eras) |
| **2** | §1.2.1 — The Cognitive Loop | Perceive → Reason → Plan → Act → Learn pipeline |
| **3** | §1.2.3 — Agent Brain Patterns | ReactiveAgent, DeliberativeAgent, HybridAgent |
| **4** | §1.3.1 — Model Context Protocol | MCPRegistry: tool registration, discovery, invocation |
| **5** | §1.3.2 — A2A Protocols | AgentMessage passing in a three-agent pipeline |
| **6** | §1.5 — Interaction Paradigms | Levels 1–5: Direct LLM → Multi-Agent System |
| **7** | §1.6 — Progression Framework | Maturity model Levels 0–4 with self-assessment |
| **8** | §1.7 — Business Impact | Quandri, My AskAI, Enterprise Bot case studies |
| **9** | Resilience Demo | Full-failure demonstration (failure_rate=1.0) |
| **10** | Summary | Key takeaways and Chapter 2 preview |

## Repository Structure

```
ch01-foundations-of-agent-engineering/
│
├── README.md                          # This file
├── AGENTS.md                          # Agentic AI Foundation 2026 metadata
├── requirements.txt                       # Base/shared dependencies
├── requirements-openai.txt                # + OpenAI provider deps
├── requirements-claude.txt                # + Anthropic Claude provider deps
├── requirements-gemini.txt                # + Google Gemini provider deps
├── requirements-ollama.txt                # + Local Ollama provider deps
├── .env.template                      # API key template (zero-hardcode policy)
├── .gitignore                         # Standard Python + .env exclusions
├── TROUBLESHOOTING.md                 # Dependency conflict resolution guide
│
├── ch01_foundations_of_agent_engineering.ipynb   # Primary deliverable
│
└── src/
    ├── __init__.py                    # Package init with version + author
    ├── mock_llm.py                    # MockLLM class + 22-entry response bank
    └── utils.py                       # Color logger, @graceful_fallback, detect_api_key
```

## Simulation Mode

When no API key is detected, the notebook activates **Simulation Mode**:

- `MockLLM` replaces the LLM client transparently (works identically across all providers)
- All 22 responses are pre-authored from Chapter 1 content
- A yellow `SIMULATION MODE` banner confirms activation at startup
- Every cell executes successfully with no external dependencies

API key detection follows a three-tier cascade: `.env` file → environment variable → interactive prompt → Simulation Mode.

## Pre-Executed Notebook Variants

Every notebook is pre-executed with outputs saved. Pick the variant that matches your setup:

| Notebook | Provider | Description |
|---|---|---|
| [ch01_foundations_of_agent_engineering__RUN_NO_KEY_SIMULATION.ipynb](ch01_foundations_of_agent_engineering__RUN_NO_KEY_SIMULATION.ipynb) | Simulation | No API key — MockLLM responses |
| [ch01_foundations_of_agent_engineering__RUN_OPENAI_GPT4o.ipynb](ch01_foundations_of_agent_engineering__RUN_OPENAI_GPT4o.ipynb) | OpenAI GPT-4o | Live LLM via `OPENAI_API_KEY` |
| [ch01_foundations_of_agent_engineering__RUN_CLAUDE_Sonnet4.ipynb](ch01_foundations_of_agent_engineering__RUN_CLAUDE_Sonnet4.ipynb) | Claude Sonnet 4 | Live LLM via `ANTHROPIC_API_KEY` |
| [ch01_foundations_of_agent_engineering__RUN_GEMINI_Flash25.ipynb](ch01_foundations_of_agent_engineering__RUN_GEMINI_Flash25.ipynb) | Gemini Flash 2.5 | Live LLM via `GOOGLE_API_KEY` |
| [ch01_foundations_of_agent_engineering__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb](ch01_foundations_of_agent_engineering__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb) | Local Ollama | DeepSeek V2 16B — no API key |

All variants produce equivalent output. Compare them to see how different providers handle the same agent tasks.

For local LLM setup instructions (Ollama + DeepSeek on Windows, macOS, and Linux), see **[LOCAL_LLM_SETUP.md](LOCAL_LLM_SETUP.md)**.

For a detailed comparison of how each provider performs on this chapter's tasks — including Bloom's taxonomy ratings, strengths/weaknesses, and per-dimension scores — see **[LLM_COMPARISON.md](LLM_COMPARISON.md)**.

## Resilience Architecture

All agent operations are wrapped in the `@graceful_fallback` decorator:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

The Resilience Demo cell (Cell Group 9) uses `MockLLM(failure_rate=1.0)` to trigger 100% failures, demonstrating that every operation degrades gracefully.

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt` (base) and `requirements-<provider>.txt` for your LLM provider
- **API Key:** Optional — any of OpenAI, Anthropic, Google, or local Ollama. Simulation Mode works without any.

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to common issues including module import errors, ANSI color rendering, and Python version compatibility.

## License

This code is provided as educational companion material for *AI Agents* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *AI Agents* (Packt Publishing, 2026)
