# Chapter 15: Education and Knowledge Agents

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 15** of *30 Agents Every AI Engineer Must Build*. It implements two agent architectures that apply the cognitive loop to teaching and collective reasoning: the Education Intelligence Agent (POMDP-based adaptive tutor with probabilistic mastery estimates, zone-of-proximal-development curriculum planning, Bayesian Knowledge Tracing, SM-2 spaced repetition, and two-stage misconception detection) and the Collective Intelligence Agent (multi-agent collaboration with role-specialized agents performing propose/critique/synthesize through weighted consensus with adversarial critic rotation and cross-pollination).

Every code cell runs **without an API key** in Simulation Mode, powered by a `MockLLM` engine with a 9-key section-mapped response registry. When an OpenAI API key is provided, the notebook seamlessly switches to Live Mode.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter15

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
jupyter notebook chapter15_education_and_knowledge_agents.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | Imports, API key detection, Simulation Mode switch |
| **1** | Dataclasses | 12 supporting type definitions |
| **2** | §15.1 — Knowledge Graph | DAG curriculum with 10 Python learning objectives |
| **3** | §15.2 — Student Model | Per-student probabilistic mastery state |
| **4** | §15.3 — Curriculum Planner | ZPD-aligned Gaussian expected-gain objective selection |
| **5** | §15.4 — Placement Test | IRT 2PL adaptive diagnostics with Fisher information |
| **6** | §15.5 — BKT Update | Bayesian Knowledge Tracing (posterior + transition) |
| **7** | §15.6 — Spaced Repetition | SM-2 algorithm with overdue priority scoring |
| **8** | §15.7 — Feedback Generator | Two-stage misconception detection + pedagogical nudge |
| **9** | §15.8 — Case Study "Alex" | End-to-end: Placement → BKT → Feedback → Review |
| **10** | §15.9 — Collaborative Agent | Propose/critique dual pathway with confidence metadata |
| **11** | §15.10 — Consensus Engine | Weighted multi-round consensus with adversarial rotation |
| **12** | §15.11 — Rubric Case Study | Three-agent rubric design + emergent intelligence |
| **13** | Summary | Key takeaways and further reading |

## Repository Structure

```
chapter15/
│
├── README.md                                              # This file
├── AGENTS.md                                              # Agentic AI metadata
├── LICENSE                                                # MIT License
├── requirements.txt                                       # Pinned Python dependencies
├── .env.template                                          # API key template (zero-hardcode policy)
├── .gitignore                                             # Standard Python + .env exclusions
├── TROUBLESHOOTING.md                                     # Dependency conflict resolution guide
│
├── chapter15_education_and_knowledge_agents.ipynb          # Primary deliverable
│
├── __init__.py                                            # Package exports
├── mock_llm.py                                            # MockLLM + 9-key section-mapped response registry
└── resilience.py                                          # ColorLogger + @graceful_fallback decorator
```

## Simulation Mode

When no API key is detected, the notebook activates **Simulation Mode**:

- `MockLLM` replaces the OpenAI client transparently
- Pre-authored, section-mapped mock responses are educationally accurate
- All mathematical models (BKT, IRT, SM-2) run full computation using pure math
- Consensus protocol runs all rounds with mock proposals
- Every cell executes successfully with no external dependencies

API key detection follows a three-tier cascade: `.env` file → environment variable → interactive prompt → Simulation Mode.

## Resilience Architecture

All agent operations are wrapped in the `@graceful_fallback` decorator:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

## Requirements

- **Python:** 3.10+ (tested up to 3.12)
- **Dependencies:** See `requirements.txt` (includes `openai`, `numpy`, `networkx`, `python-dotenv`)
- **API Key:** Optional (Simulation Mode works without one)

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for dependency conflicts, platform-specific issues, and common runtime problems.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
