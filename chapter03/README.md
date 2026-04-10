# Chapter 3: The Art of Agent Prompting

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 3** of *30 Agents Every AI Engineer Must Build*. It transforms every concept in the chapter — from the PTCF framework to Tree-of-Thought prompting — into runnable, interactive code. Topics include cognitive programming, two-layer prompt architecture, the Persona-Task-Context-Format blueprint, task decomposition, few-shot learning, chain-of-thought reasoning, and multi-agent communication protocols.

Every code cell runs **without an API key** in Simulation Mode, powered by a `MockLLM` engine that returns chapter-derived responses. When an API key is provided (OpenAI, Anthropic, or Google) or Ollama is running locally, the notebook seamlessly switches to Live Mode. Each provider has its own pre-executed notebook variant.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter03

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
jupyter notebook chapter_03_agent_prompting.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | Imports, API key detection, mode selection |
| **1** | §3.1 — From Instructions to Constitutions | Cognitive programming, persona constraints |
| **2** | §3.2 — Two-Layer Prompt Architecture | System prompt vs. user prompt |
| **3** | §3.3 — The PTCF Blueprint | Persona, Task, Context, Format framework |
| **4** | §3.4 — Designing Thinking Agents | Agent capability spectrum, task decomposition |
| **5** | §3.5 — Teaching by Example | Few-shot learning, ticket classification |
| **6** | §3.6 — Making Reasoning Visible | Chain-of-thought and Tree-of-thought prompting |
| **7** | §3.7 — Architecting Collaboration | Multi-agent communication protocols |
| **8** | Case Studies | SaaS triage, compliance review, code review |
| **9** | Evaluation | A/B comparison, regression testing |

## Repository Structure

```
chapter03/
│
├── README.md                          # This file
├── AGENTS.md                          # Agentic AI metadata
├── LICENSE                            # MIT License
├── requirements.txt                       # Base/shared dependencies
├── requirements-openai.txt                # + OpenAI provider deps
├── requirements-claude.txt                # + Anthropic Claude provider deps
├── requirements-gemini.txt                # + Google Gemini provider deps
├── requirements-ollama.txt                # + Local Ollama provider deps
├── .env.template                      # API key template (zero-hardcode policy)
├── .gitignore                         # Standard Python + .env exclusions
├── troubleshooting.md                 # Dependency conflict resolution guide
│
├── chapter_03_agent_prompting.ipynb   # Primary deliverable
│
├── mock_llm.py                        # MockLLM — simulation engine
└── utils.py                           # Color logger, @graceful_fallback
```

## Simulation Mode

When no API key is detected, the notebook activates **Simulation Mode**:

- `MockLLM` subclasses `BaseChatModel` for full LangChain pipe-operator (`|`) compatibility
- Routes responses via keyword matching to return section-appropriate mock data
- Produces the same structured outputs as a live model
- Every cell executes successfully with no external dependencies

All LLM calls are wrapped in the `@graceful_fallback` decorator — if anything fails, you see a Red `[HANDLED ERROR]` log (never a traceback) and the notebook continues.

## Pre-Executed Notebook Variants

Every notebook is pre-executed with outputs saved. Pick the variant that matches your setup:

| Notebook | Provider | Description |
|---|---|---|
| [ch03_agent_prompting__RUN_NO_KEY_SIMULATION.ipynb](ch03_agent_prompting__RUN_NO_KEY_SIMULATION.ipynb) | Simulation | No API key — MockLLM responses |
| [ch03_agent_prompting__RUN_OPENAI_GPT4o.ipynb](ch03_agent_prompting__RUN_OPENAI_GPT4o.ipynb) | OpenAI GPT-4o | Live LLM via `OPENAI_API_KEY` |
| [ch03_agent_prompting__RUN_CLAUDE_Sonnet4.ipynb](ch03_agent_prompting__RUN_CLAUDE_Sonnet4.ipynb) | Claude Sonnet 4 | Live LLM via `ANTHROPIC_API_KEY` |
| [ch03_agent_prompting__RUN_GEMINI_Flash25.ipynb](ch03_agent_prompting__RUN_GEMINI_Flash25.ipynb) | Gemini Flash 2.5 | Live LLM via `GOOGLE_API_KEY` |
| [ch03_agent_prompting__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb](ch03_agent_prompting__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb) | Local Ollama | DeepSeek V2 16B — no API key |

All variants produce equivalent output. Compare them to see how different providers handle the same agent tasks.

For local LLM setup instructions (Ollama + DeepSeek on Windows, macOS, and Linux), see **[LOCAL_LLM_SETUP.md](LOCAL_LLM_SETUP.md)**.

For a detailed comparison of how each provider performs on this chapter's tasks — including Bloom's taxonomy ratings, strengths/weaknesses, and per-dimension scores — see **[LLM_COMPARISON.md](LLM_COMPARISON.md)**.

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt` (base) and `requirements-<provider>.txt` for your LLM provider
- **API Key:** Optional — any of OpenAI, Anthropic, Google, or local Ollama. Simulation Mode works without any.

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for solutions to common dependency conflicts and environment issues.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
