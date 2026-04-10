# Chapter 8: Data Analysis and Reasoning Agents

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 8** of *30 Agents Every AI Engineer Must Build*. It implements three agent archetypes that transform raw data into defensible, actionable intelligence: the Data Analysis Agent (cognitive loop for statistical reasoning and anomaly detection), the Verification & Validation Agent (fact-checking, NLI-based evidence scoring, and consistency analysis), and the General Problem Solver (five-stage meta-reasoning cycle: decompose → analogy search → hypothesize → test → meta-learn). Two extended case studies — a newsroom fact-checking assistant and a cross-disciplinary hypothesis engine — demonstrate these patterns, unified by a Tri-Agent Pipeline.

Every code cell runs **without an API key** in Simulation Mode, powered by a `MockLLM` engine that returns chapter-derived responses. When an API key is provided (OpenAI, Anthropic, or Google) or Ollama is running locally, the notebook seamlessly switches to Live Mode. Each provider has its own pre-executed notebook variant.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter08

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
jupyter notebook ch08_data_analysis_reasoning_agents.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | Environment setup, API key resolution, Simulation Mode |
| **1** | §8.1 — Data Analysis Agent | Visualization recommender, OLS regression, anomaly detection |
| **2** | §8.2 — Verification & Validation Agent | Theory narrative, BART-MNLI NLI demo |
| **3** | §8.3 — General Problem Solver | Theory, pseudocode class, five-stage meta-reasoning |
| **4** | §8.4 — Case Study 1 | Newsroom fact-checking assistant |
| **5** | §8.5 — Case Study 2 | Cross-disciplinary GPS hypothesis engine |
| **6** | §8.6 — Tri-Agent Pipeline | Integration demo: trust-then-escalate architecture |

## Repository Structure

```
chapter08/
│
├── README.md                                    # This file
├── AGENTS.md                                    # Agentic AI metadata
├── LICENSE                                      # MIT License
├── requirements.txt                       # Base/shared dependencies
├── requirements-openai.txt                # + OpenAI provider deps
├── requirements-claude.txt                # + Anthropic Claude provider deps
├── requirements-gemini.txt                # + Google Gemini provider deps
├── requirements-ollama.txt                # + Local Ollama provider deps
├── .env.template                                # API key template (zero-hardcode policy)
├── .gitignore                                   # Standard Python + .env exclusions
├── troubleshooting.md                           # Dependency conflict resolution guide
│
├── ch08_data_analysis_reasoning_agents.ipynb    # Primary deliverable
│
├── __init__.py                                  # Public exports
├── config.py                                    # Three-tier API key resolution
├── color_logger.py                              # ANSI color-coded logging
├── mock_llm.py                                  # MockLLM, 7-entry mock registry, llm_call()
└── sample_sales_data.csv                        # Synthetic sales dataset (100 rows, seed=42)
```

## Simulation Mode

When no API key is detected, the notebook activates **Simulation Mode**:

- All LLM calls route to `MockLLM` with deterministic, chapter-accurate responses
- Color-coded logging (Blue/Green/Red) traces the agent's reasoning
- Every cell completes without errors or tracebacks
- Outputs are logically identical to live-mode results

API key detection follows a three-tier cascade: `.env` file → environment variable → interactive prompt → Simulation Mode.

## Pre-Executed Notebook Variants

Every notebook is pre-executed with outputs saved. Pick the variant that matches your setup:

| Notebook | Provider | Description |
|---|---|---|
| [ch08_data_analysis_reasoning_agents__RUN_NO_KEY_SIMULATION.ipynb](ch08_data_analysis_reasoning_agents__RUN_NO_KEY_SIMULATION.ipynb) | Simulation | No API key — MockLLM responses |
| [ch08_data_analysis_reasoning_agents__RUN_OPENAI_GPT4o.ipynb](ch08_data_analysis_reasoning_agents__RUN_OPENAI_GPT4o.ipynb) | OpenAI GPT-4o | Live LLM via `OPENAI_API_KEY` |
| [ch08_data_analysis_reasoning_agents__RUN_CLAUDE_Sonnet4.ipynb](ch08_data_analysis_reasoning_agents__RUN_CLAUDE_Sonnet4.ipynb) | Claude Sonnet 4 | Live LLM via `ANTHROPIC_API_KEY` |
| [ch08_data_analysis_reasoning_agents__RUN_GEMINI_Flash25.ipynb](ch08_data_analysis_reasoning_agents__RUN_GEMINI_Flash25.ipynb) | Gemini Flash 2.5 | Live LLM via `GOOGLE_API_KEY` |
| [ch08_data_analysis_reasoning_agents__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb](ch08_data_analysis_reasoning_agents__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb) | Local Ollama | DeepSeek V2 16B — no API key |

All variants produce equivalent output. Compare them to see how different providers handle the same agent tasks.

For local LLM setup instructions (Ollama + DeepSeek on Windows, macOS, and Linux), see **[LOCAL_LLM_SETUP.md](LOCAL_LLM_SETUP.md)**.

## Resilience Architecture

All agent operations are wrapped in the `@fail_gracefully` decorator:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt` (base) and `requirements-<provider>.txt` for your LLM provider
- **API Key:** Optional — any of OpenAI, Anthropic, Google, or local Ollama. Simulation Mode works without any.

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for solutions to common issues including dependency conflicts and runtime errors.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
