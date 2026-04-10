# Chapter 13: Healthcare and Scientific Agents

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 13** of *30 Agents Every AI Engineer Must Build*. It explores two agent architectures for high-stakes, information-intensive domains: the Healthcare Intelligence Agent (four-layer architecture with data ingestion, clinical knowledge integration, Bayesian diagnostic reasoning, and audience-adapted explanation generation — including safety escalation, provenance tracking, and immutable audit trails) and the Scientific Discovery Agent (multi-phase pipeline for fault-tolerant literature synthesis, information-theoretic knowledge gap detection, abductive hypothesis generation, and closed-loop experimental feedback).

Every code cell runs **without an API key** in Simulation Mode, powered by context-aware mock responses derived directly from Chapter 13 content. When an API key is provided (OpenAI, Anthropic, or Google) or Ollama is running locally, the notebook seamlessly switches to Live Mode. Each provider has its own pre-executed notebook variant.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter13

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Configure your LLM provider for Live Mode
cp .env.template .env
# Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY — or use Ollama locally

# 5. Launch the notebook
jupyter notebook chapter13_healthcare_scientific_agents.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | Setup and configuration, technical requirements |
| **1** | Infrastructure | Simulation infrastructure (cross-cutting mock layer) |
| **2** | §13.1–13.4 — Healthcare Intelligence Agent | Data ingestion, clinical knowledge, Bayesian reasoning, explanation generation |
| **3** | §13.5–13.8 — Scientific Discovery Agent | Literature synthesis, knowledge gap detection, hypothesis generation, experimental feedback |
| **4** | §13.9 — Cross-Domain Analysis | Integration patterns and shared architectural lessons |

## Real-World Use Cases

This chapter's two agent architectures target domains where decisions directly impact human welfare and scientific progress.

**Pinnacle Health Network** — A regional health system's ED misses 14 sepsis cases per year because subtle presentations slip past triage. The case study shows how Bayesian belief updating with a 0.15 escalation threshold catches sepsis 74% faster than the existing qSOFA screening — while reducing alert fatigue from a 94% dismissal rate to 18%.

**NovaMateria Labs** — A materials science company needs to design an aerospace polymer meeting three competing targets (Tg > 350°C, tensile ≥ 100 MPa, elongation ≥ 15%) under a 14-month DARPA deadline. The case study shows how knowledge gap detection finds a cross-disciplinary blind spot, and closed-loop experimental feedback compresses the research timeline by 60%.

Read the full case study: **[USECASE.md](USECASE.md)** — includes Bayesian update walkthrough, privacy architecture, and experimental convergence data.

## Repository Structure

```
chapter13/
│
├── README.md                                          # This file
├── AGENTS.md                                          # Agentic AI metadata
├── LICENSE                                            # MIT License
├── requirements.txt                                   # Pinned Python dependencies
├── .env.template                                      # API key template (zero-hardcode policy)
├── .gitignore                                         # Standard Python + .env exclusions
├── troubleshooting.md                                 # Dependency conflict resolution guide
│
└── chapter13_healthcare_scientific_agents.ipynb        # Primary deliverable (self-contained)
```

## Simulation Mode

When no API key is detected, the notebook activates **Simulation Mode**:

- All LLM calls, database queries, and external API requests have deterministic fallbacks
- Mock responses are derived directly from Chapter 13 content
- Every cell executes successfully with no external dependencies
- Outputs match the examples discussed in the book

API key detection follows a three-tier cascade: `.env` file → environment variable → interactive prompt → Simulation Mode.

## Pre-Executed Notebook Variants

Every notebook is pre-executed with outputs saved. Pick the variant that matches your setup:

| Notebook | Provider | Description |
|---|---|---|
| [ch13_healthcare_scientific_agents__RUN_NO_KEY_SIMULATION.ipynb](ch13_healthcare_scientific_agents__RUN_NO_KEY_SIMULATION.ipynb) | Simulation | No API key — MockLLM responses |
| [ch13_healthcare_scientific_agents__RUN_OPENAI_GPT4o.ipynb](ch13_healthcare_scientific_agents__RUN_OPENAI_GPT4o.ipynb) | OpenAI GPT-4o | Live LLM via `OPENAI_API_KEY` |
| [ch13_healthcare_scientific_agents__RUN_CLAUDE_Sonnet4.ipynb](ch13_healthcare_scientific_agents__RUN_CLAUDE_Sonnet4.ipynb) | Claude Sonnet 4 | Live LLM via `ANTHROPIC_API_KEY` |
| [ch13_healthcare_scientific_agents__RUN_GEMINI_Flash25.ipynb](ch13_healthcare_scientific_agents__RUN_GEMINI_Flash25.ipynb) | Gemini Flash 2.5 | Live LLM via `GOOGLE_API_KEY` |
| [ch13_healthcare_scientific_agents__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb](ch13_healthcare_scientific_agents__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb) | Local Ollama | DeepSeek V2 16B — no API key |

All variants produce equivalent output. Compare them to see how different providers handle the same agent tasks.

For local LLM setup instructions (Ollama + DeepSeek on Windows, macOS, and Linux), see **[LOCAL_LLM_SETUP.md](LOCAL_LLM_SETUP.md)**.

## Resilience Architecture

All agent operations are wrapped in resilience decorators:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt` (includes `numpy`, `langchain-core`, `fhir.resources`, `aiohttp`, `scipy`)
- **API Key:** Optional — any of OpenAI, Anthropic, Google, or local Ollama. Simulation Mode works without any.

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for solutions to known dependency conflicts and fixes.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
