# Chapter 5: Foundational Cognitive Architectures

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 5** of *30 Agents Every AI Engineer Must Build*. It examines the three foundational cognitive architectures that empower intelligent, autonomous agents: the Autonomous Decision-Making Agent (real-time perception → cognition → action loop), the Planning Agent (hierarchical task decomposition and dynamic execution), and the Memory-Augmented Agent (working, episodic, and semantic memory for continuity).

Every code cell runs **without an API key** in Simulation Mode, powered by a `MockLLM` engine and `MockVectorDB` that return chapter-derived responses. When an OpenAI API key is provided, the notebook seamlessly switches to Live Mode.

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

# 4. (Optional) Add your OpenAI API key for Live Mode
cp .env.template .env
# Edit .env and add your key, or skip this step for Simulation Mode

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
├── requirements.txt                           # Pinned Python dependencies
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

- `MockLLM` replaces the OpenAI client transparently
- `MockVectorDB` provides in-memory Jaccard-based vector search
- All responses are pre-authored from Chapter 5 content
- Every cell executes successfully with no external dependencies

API key detection follows a three-tier cascade: `.env` file → environment variable → interactive prompt → Simulation Mode.

## Resilience Architecture

All agent operations are wrapped in the `@fail_gracefully` decorator from `resilience.py`:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

## Requirements

- **Python:** 3.10+ (required — the code uses `str | None` union syntax)
- **Dependencies:** See `requirements.txt`
- **API Key:** Optional (Simulation Mode works without one)

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to common dependency conflicts, runtime issues, and platform-specific notes.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
