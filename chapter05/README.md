# Chapter 5: Foundational Cognitive Architectures

**Book:** *30 Agents Every AI Engineer Must Build*
**Author:** Imran Ahmad
**Publisher:** Packt Publishing, 2026
**Repository:** [PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build](https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build)

---

## Overview

This chapter examines the three foundational cognitive architectures that
empower intelligent, autonomous agents to operate in complex, dynamic
environments. These architectures serve as the structural backbone of
modern AI systems, simulating essential aspects of human cognition —
decision-making, planning, and memory — to enable agents to tackle
real-world problems with increasing sophistication.

**The three agent types implemented here:**

| Agent Type | Focus | Chapter Section |
|---|---|---|
| **Autonomous Decision-Making Agent** | Real-time perception → cognition → action loop | Section 5.1, pp. 118–132 |
| **Planning Agent** | Hierarchical task decomposition and dynamic execution | Section 5.2, pp. 131–137 |
| **Memory-Augmented Agent** | Working, episodic, and semantic memory for continuity | Section 5.3, pp. 135–144 |

---

## Repository Structure

```
Chapter-05/
│
├── README.md                                  # This file
├── AGENTS.md                                  # Agentic metadata and persona
├── TROUBLESHOOTING.md                         # Common issues and fixes
├── requirements.txt                           # Python dependencies
├── .env.template                              # API key template (copy to .env)
├── .gitignore                                 # Git ignore rules
│
├── ch05_foundational_architectures.ipynb      # PRIMARY DELIVERABLE
│
├── color_logger.py                            # Color-coded logging utilities
├── resilience.py                              # @fail_gracefully decorator
├── mock_llm.py                                # MockLLM + MockVectorDB
│
└── figures/                                   # Diagrams referenced in text
    ├── fig5_1_decision_loop.png
    ├── fig5_2_planning_architecture.png
    ├── fig5_3_memory_architecture.png
    └── fig5_4_integrated_architecture.png
```

### Dependency Graph

```
ch05_foundational_architectures.ipynb
  │
  ├── imports → color_logger.py       (log_info, log_success, log_error, log_warn, log_section)
  ├── imports → resilience.py         (@fail_gracefully decorator → uses color_logger)
  └── imports → mock_llm.py           (MockLLM, MockVectorDB, MockResponse)
```

---

## Quick Start

### Prerequisites

- Python 3.10+ (required — the code uses `str | None` union syntax)
- git
- A terminal (macOS, Windows PowerShell, or Linux)

### Setup

```bash
# 1) Clone the repo and enter this chapter's folder
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd "30-Agents-Every-AI-Engineer-Must-Build/Chapter 05"

# 2) Create and activate a virtual environment
python -m venv .venv

# macOS/Linux:
source .venv/bin/activate

# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# 3) Install dependencies
pip install -r requirements.txt

# 4) Launch the notebook
jupyter notebook ch05_foundational_architectures.ipynb
```

### (Optional) Enable Live LLM Mode

```bash
# Copy the template and add your API keys
cp .env.template .env
# Edit .env with your keys
```

---

## Simulation Mode vs. Live Mode

This repository is designed to run **entirely without API keys** in
Simulation Mode. The mock layer (`mock_llm.py`) provides drop-in
replacements for an LLM client and a vector database, enabling every
notebook cell to execute end-to-end.

| Feature | Simulation Mode | Live Mode |
|---|---|---|
| **API key required** | No | Yes (OpenAI or Anthropic) |
| **LLM responses** | Pre-built MockResponse objects | Real LLM completions |
| **Vector database** | In-memory MockVectorDB with Jaccard search | Chroma, Pinecone, or Weaviate |
| **Use case** | Learning, demos, CI/CD testing | Production prototyping |
| **Activation** | Default (no `.env` or empty key) | Set `OPENAI_API_KEY` in `.env` |

The notebook auto-detects which mode to use at startup. A color-coded
log message confirms the active mode before any agent code runs.

---

## What You Will Learn

Working through this notebook, you will implement and understand:

1. **The Cognitive Loop** — How perception, cognition, action, and
   learning form a continuous cycle for autonomous agents (Figure 5.1).

2. **Strategy Scoring** — A weighted multi-axis decision framework
   that selects between full autonomous resolution, immediate
   escalation, and guided resolution (pp. 121–122).

3. **Task DAGs** — Dependency-aware task graphs for billing issues,
   service outages, and generic workflows (pp. 123–124).

4. **Safety Checks & Escalation** — Five-factor escalation scoring
   with configurable thresholds (pp. 128–131).

5. **Hierarchical Decomposition** — Breaking high-level goals into
   phased, actionable subtasks with monitoring (Figure 5.2).

6. **Episodic Memory Retrieval** — Vector-similarity search over
   interaction history for personalized, context-aware responses
   (Figure 5.3).

7. **Integrated Architecture** — Combining all three agent types in
   a single scenario (Figure 5.4, Table 5.2).

---

## Engineering Patterns

Every agent tool call in this repository follows two core patterns
from the book's Engineering Best Practices (pp. 142–144):

- **Observability:** All execution is traced through `color_logger.py`
  with timestamped, color-coded output (blue for info, green for
  success, red for errors, yellow for warnings).

- **Robustness:** Every tool call is wrapped in the `@fail_gracefully`
  decorator from `resilience.py`, which provides exponential-backoff
  retries and fallback values. The system never crashes.

---

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to common
dependency conflicts, runtime issues, and platform-specific notes.

---

## Further Reading

- **Chapter 1** — The cognitive loop foundation that this chapter builds upon
- **Chapter 3** — The Art of Agent Prompting (prompt engineering for cognition)
- **Chapter 4** — Agent Deployment and Responsible Development
- **Chapter 6** — Information Retrieval and Knowledge Agents
- **Chapter 7** — Multi-agent systems and tool-using agents

---

## License

Refer to the book's license terms. See the
[main repository](https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build)
for details.
