# Chapter 4: Agent Deployment and Responsible Development

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 4** of *30 Agents Every AI Engineer Must Build*. The chapter addresses the critical shift from prototype to production for AI agent systems, covering six interconnected domains: infrastructure scaling by agent typology, cost-aware model routing, high-throughput resilience patterns, microservice-based cognitive architectures, zero-trust security, and ethical fairness auditing.

Every code cell runs **without an API key** in Simulation Mode, powered by a `MockLLM` engine that returns chapter-derived responses. When an API key is provided (OpenAI, Anthropic, or Google) or Ollama is running locally, the notebook seamlessly switches to Live Mode. Each provider has its own pre-executed notebook variant.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter04

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
jupyter notebook chapter_04_agent_deployment.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | Environment detection, Simulation Mode banner |
| **1** | §4.1 — Agent Typology | Infrastructure profiles for reactive, deliberative, hybrid, and multi-agent systems |
| **2** | §4.2 — Cost-Aware Routing | Tiered routing, caching, budget enforcement |
| **3** | §4.3 — Circuit Breaker | Tenacity-based breaker with state transitions and fallback |
| **4** | §4.4 — Microservice Pipeline | Five-service chain from Planner to Response Synthesizer |
| **5** | §4.5 — Threat Detection | Adversarial input classification across nine attack vectors |
| **6** | §4.6 — Fairness Audit | Demographic parity and equalized opportunity with pre/post-mitigation comparison |
| **7** | Reference | Toolchain Reference Explorer — formatted display of all tools cited in the chapter |
| **8** | Summary | Cost Dashboard and section completion status |

## Real-World Use Case: NovaClaim Insurance

How would a mid-market insurer deploy these patterns to process 40,000 claims per month? The companion case study follows **NovaClaim Insurance** as they tackle cost explosion, API outages, prompt injection risks, and regulatory fairness audits — mapping each section of this chapter to a specific operational problem.

Read the full case study: **[USECASE.md](USECASE.md)** — includes stakeholder profiles, failed alternatives, revenue impact analysis, and next-step recommendations.

## Repository Structure

```
chapter04/
│
├── README.md                              # This file
├── LOCAL_LLM_SETUP.md                     # Ollama setup guide (Win/Mac/Linux)
├── AGENTS.md                              # Agentic metadata and AI persona prompt
├── LICENSE                                # MIT License
├── requirements.txt                       # Base/shared dependencies
├── requirements-openai.txt                # + OpenAI provider deps
├── requirements-claude.txt                # + Anthropic Claude provider deps
├── requirements-gemini.txt                # + Google Gemini provider deps
├── requirements-ollama.txt                # + Local Ollama provider deps
├── .env.template                          # API key template (zero-hardcode policy)
├── .gitignore                             # Standard Python + .env exclusions
├── TROUBLESHOOTING.md                     # Dependency conflict resolution guide
│
├── chapter_04_agent_deployment.ipynb      # Primary deliverable
│
├── __init__.py                            # Package metadata
├── agent_utils.py                         # AgentLogger, @fail_gracefully, CostTracker,
│                                          #   CircuitBreaker, InputValidator
└── mock_llm.py                            # MockLLM, RESPONSE_BANK, SyntheticDataFactory
```

## Simulation Mode

When no API key is detected, the notebook activates **Simulation Mode**:

- `MockLLM` replaces the LLM client transparently (works identically across all providers)
- All 20 section-keyed mock responses are traceable to specific chapter references
- `SyntheticDataFactory` generates deterministic datasets (seed=42) for fairness auditing, cost routing, and threat detection
- Every cell executes successfully with no external dependencies

API key detection follows a three-tier cascade: `.env` file → environment variable → interactive prompt → Simulation Mode.

## Pre-Executed Notebook Variants

Every notebook is pre-executed with outputs saved. Pick the variant that matches your setup:

| Notebook | Provider | Description |
|---|---|---|
| [ch04_agent_deployment__RUN_NO_KEY_SIMULATION.ipynb](ch04_agent_deployment__RUN_NO_KEY_SIMULATION.ipynb) | Simulation | No API key — MockLLM responses |
| [ch04_agent_deployment__RUN_OPENAI_GPT4o.ipynb](ch04_agent_deployment__RUN_OPENAI_GPT4o.ipynb) | OpenAI GPT-4o | Live LLM via `OPENAI_API_KEY` |
| [ch04_agent_deployment__RUN_CLAUDE_Sonnet4.ipynb](ch04_agent_deployment__RUN_CLAUDE_Sonnet4.ipynb) | Claude Sonnet 4 | Live LLM via `ANTHROPIC_API_KEY` |
| [ch04_agent_deployment__RUN_GEMINI_Flash25.ipynb](ch04_agent_deployment__RUN_GEMINI_Flash25.ipynb) | Gemini Flash 2.5 | Live LLM via `GOOGLE_API_KEY` |
| [ch04_agent_deployment__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb](ch04_agent_deployment__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb) | Local Ollama | DeepSeek V2 16B — no API key |

All variants produce equivalent output. Compare them to see how different providers handle the same agent tasks.

For local LLM setup instructions (Ollama + DeepSeek on Windows, macOS, and Linux), see **[LOCAL_LLM_SETUP.md](LOCAL_LLM_SETUP.md)**.

For a detailed comparison of how each provider performs on this chapter's tasks — including Bloom's taxonomy ratings, strengths/weaknesses, and per-dimension scores — see **[LLM_COMPARISON.md](LLM_COMPARISON.md)**.

## Resilience Architecture

All agent operations are wrapped in the `@fail_gracefully` decorator:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

Key infrastructure components include `CostTracker` (per-call accounting with budget ceiling), `CircuitBreaker` (closed → open → half_open state machine), and `InputValidator` (prompt sanitization against attack patterns).

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt` (base) and `requirements-<provider>.txt` for your LLM provider
- **API Key:** Optional — any of OpenAI, Anthropic, Google, or local Ollama. Simulation Mode works without any.

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to common issues including module import errors, ANSI color rendering, and Python version compatibility.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
