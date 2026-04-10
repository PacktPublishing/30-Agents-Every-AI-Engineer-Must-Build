# Chapter 5: Foundational Cognitive Architectures

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 5** of *30 Agents Every AI Engineer Must Build*. It examines the three foundational cognitive architectures that empower intelligent, autonomous agents: the Autonomous Decision-Making Agent (real-time perception → cognition → action loop), the Planning Agent (hierarchical task decomposition and dynamic execution), and the Memory-Augmented Agent (working, episodic, and semantic memory for continuity).

Every code cell runs **without an API key** in Simulation Mode, powered by a `MockLLM` engine and `MockVectorDB` that return chapter-derived responses. When an API key is provided (OpenAI, Anthropic, or Google) or Ollama is running locally, the notebook seamlessly switches to Live Mode. Each provider has its own pre-executed notebook variant.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter05

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
jupyter notebook ch05_foundational_architectures.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | Imports, API key detection, mode selection |
| **1** | §5.1 — Autonomous Decision-Making | The Cognitive Loop: Perceive → Reason → Plan → Act → Learn |
| **2** | §5.1 — Strategy Scoring | Weighted multi-axis decision framework for resolution strategies |
| **3** | §5.1 — Task DAGs | Dependency-aware task graphs for billing, outages, and generic workflows |
| **4** | §5.1 — Safety & Escalation | Five-factor escalation scoring with configurable thresholds |
| **5** | §5.2 — Planning Agent | Hierarchical decomposition of high-level goals into phased subtasks |
| **6** | §5.3 — Memory-Augmented Agent | Working, episodic, and semantic memory implementations |
| **7** | §5.3 — Episodic Retrieval | Vector-similarity search over interaction history |
| **8** | Integration | Combined three-agent architecture in a single scenario |
| **9** | Summary | Key takeaways and Chapter 6 preview |

## Repository Structure

```
chapter05/
│
├── README.md                                  # This file
├── AGENTS.md                                  # Agentic AI metadata
├── TROUBLESHOOTING.md                         # Dependency conflict resolution guide
├── requirements.txt                       # Base/shared dependencies
├── requirements-openai.txt                # + OpenAI provider deps
├── requirements-claude.txt                # + Anthropic Claude provider deps
├── requirements-gemini.txt                # + Google Gemini provider deps
├── requirements-ollama.txt                # + Local Ollama provider deps
├── .env.template                              # API key template (zero-hardcode policy)
├── .gitignore                                 # Standard Python + .env exclusions
│
├── ch05_foundational_architectures.ipynb      # Primary deliverable
│
├── color_logger.py                            # Color-coded logging utilities
├── resilience.py                              # @fail_gracefully decorator
└── mock_llm.py                                # MockLLM + MockVectorDB + MockResponse
```

## Simulation Mode

When no API key is detected, the notebook activates **Simulation Mode**:

- `MockLLM` replaces the LLM client transparently (works identically across all providers)
- `MockVectorDB` provides in-memory Jaccard-based vector search
- All responses are pre-authored from Chapter 5 content
- Every cell executes successfully with no external dependencies

API key detection follows a three-tier cascade: `.env` file → environment variable → interactive prompt → Simulation Mode.

## Pre-Executed Notebook Variants

Every notebook is pre-executed with outputs saved. Pick the variant that matches your setup:

| Notebook | Provider | Description |
|---|---|---|
| [ch05_foundational_architectures__RUN_NO_KEY_SIMULATION.ipynb](ch05_foundational_architectures__RUN_NO_KEY_SIMULATION.ipynb) | Simulation | No API key — MockLLM responses |
| [ch05_foundational_architectures__RUN_OPENAI_GPT4o.ipynb](ch05_foundational_architectures__RUN_OPENAI_GPT4o.ipynb) | OpenAI GPT-4o | Live LLM via `OPENAI_API_KEY` |
| [ch05_foundational_architectures__RUN_CLAUDE_Sonnet4.ipynb](ch05_foundational_architectures__RUN_CLAUDE_Sonnet4.ipynb) | Claude Sonnet 4 | Live LLM via `ANTHROPIC_API_KEY` |
| [ch05_foundational_architectures__RUN_GEMINI_Flash25.ipynb](ch05_foundational_architectures__RUN_GEMINI_Flash25.ipynb) | Gemini Flash 2.5 | Live LLM via `GOOGLE_API_KEY` |
| [ch05_foundational_architectures__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb](ch05_foundational_architectures__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb) | Local Ollama | DeepSeek V2 16B — no API key |

All variants produce equivalent output. Compare them to see how different providers handle the same agent tasks.

For local LLM setup instructions (Ollama + DeepSeek on Windows, macOS, and Linux), see **[LOCAL_LLM_SETUP.md](LOCAL_LLM_SETUP.md)**.

## Resilience Architecture

All agent operations are wrapped in the `@fail_gracefully` decorator from `resilience.py`:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

## Requirements

- **Python:** 3.10+ (required — the code uses `str | None` union syntax)
- **Dependencies:** See `requirements.txt` (base) and `requirements-<provider>.txt` for your LLM provider
- **API Key:** Optional — any of OpenAI, Anthropic, Google, or local Ollama. Simulation Mode works without any.

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to common dependency conflicts, runtime issues, and platform-specific notes.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
