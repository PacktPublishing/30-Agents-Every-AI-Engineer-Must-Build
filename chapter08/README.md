# Chapter 8: Data Analysis and Reasoning Agents

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 8** of *30 Agents Every AI Engineer Must Build*. It implements three agent archetypes that transform raw data into defensible, actionable intelligence: the Data Analysis Agent (cognitive loop for statistical reasoning and anomaly detection), the Verification & Validation Agent (fact-checking, NLI-based evidence scoring, and consistency analysis), and the General Problem Solver (five-stage meta-reasoning cycle: decompose → analogy search → hypothesize → test → meta-learn). Two extended case studies — a newsroom fact-checking assistant and a cross-disciplinary hypothesis engine — demonstrate these patterns, unified by a Tri-Agent Pipeline.

Every code cell runs **without an API key** in Simulation Mode, powered by a `MockLLM` engine that returns chapter-derived responses. When an OpenAI API key is provided, the notebook seamlessly switches to Live Mode.

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

# 4. (Optional) Add your OpenAI API key for Live Mode
cp .env.template .env
# Edit .env and add your key, or skip this step for Simulation Mode

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
├── requirements.txt                             # Pinned Python dependencies
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

## Resilience Architecture

All agent operations are wrapped in the `@fail_gracefully` decorator:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt`
- **API Key:** Optional (Simulation Mode works without one)

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for solutions to common issues including dependency conflicts and runtime errors.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
