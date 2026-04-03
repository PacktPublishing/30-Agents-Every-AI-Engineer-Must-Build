# Chapter 7: Tool Manipulation and Orchestration Agents

**Book:** *Agents* by Imran Ahmad (Packt, 2026 — B34135)

---

## Overview

This repository is the companion code for **Chapter 7** of *Agents*. It teaches three progressive architectural patterns for building production-ready AI agent systems:

1. **Tool-Using Agents** — A single agent extends its reasoning by invoking external functions through a Think/Plan/Act cycle (Sections 7.1–7.3).
2. **Chain-of-Agents Orchestrators** — Multiple specialized agents collaborate under a cooperation protocol with shared memory and conflict resolution (Sections 7.4–7.6).
3. **Agentic Workflow Systems** — Stateful business processes modeled as state machines with human-in-the-loop checkpoints and guard conditions (Section 7.7).

The repository is built around a **Fail-Gracefully architecture**: if no API key is present, the system automatically enters **Simulation Mode**, returning chapter-derived mock data through a context-aware `MockLLM` class. Every agent action produces color-coded log output. Every tool invocation is wrapped in defensive logic. The notebook always runs to completion.

---

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/<your-org>/chapter-07-tool-orchestration-agents.git
cd chapter-07-tool-orchestration-agents

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Enable Live Mode with an OpenAI key
cp .env.template .env
# Edit .env and paste your real API key

# 5. Launch the notebook
jupyter notebook Chapter_07_Tool_Orchestration.ipynb
```

**No API key?** No problem. The notebook runs end-to-end in Simulation Mode with zero configuration. All LLM-dependent cells use `MockLLM` to return chapter-derived responses.

---

## Repository Structure

```
chapter-07-tool-orchestration-agents/
│
├── README.md                              # This file
├── AGENTS.md                              # Agentic metadata and AI persona prompt
├── TROUBLESHOOTING.md                     # Common issues and platform notes
├── LICENSE                                # MIT License
├── requirements.txt                       # Pinned dependencies
├── .env.template                          # API key placeholder (zero-hardcode)
├── .gitignore                             # .env, __pycache__, outputs/*.png
│
├── Chapter_07_Tool_Orchestration.ipynb    # Master notebook (single entry point)
│
├── helpers/
│   ├── __init__.py                        # Package exports
│   ├── color_logger.py                    # Color-coded visual logging (6 functions)
│   ├── resilience.py                      # @graceful_fallback decorator, safe_invoke()
│   └── mock_llm.py                        # Context-aware MockLLM (6 routes + DEFAULT)
│
├── data/
│   └── sample_ad_campaign.csv             # Synthetic dataset (24 rows, 5 columns)
│
└── outputs/                               # Generated charts (git-ignored)
    └── .gitkeep
```

---

## Component Architecture

```
┌──────────────────────────────────────────────────────────┐
│            Chapter_07_Tool_Orchestration.ipynb            │
│                                                          │
│  Sec 0: Setup & Configuration                            │
│  Sec 1: The Tool-Using Agent              ┐              │
│  Sec 2: Tool Discovery & Selection        │              │
│  Sec 3: Error Handling & Resilience       │  imports     │
│  Sec 4: Chain-of-Agents Orchestrator      │              │
│  Sec 5: Conflict Resolution               │              │
│  Sec 6: Agentic Workflow (E-Commerce)     │              │
│  Sec 7: Agentic Workflow (Insurance)      │              │
│  Sec 8: Summary                           │              │
└───────────────────┬───────────────────────┘              │
                    │                                      │
       ┌────────────┼────────────┐                         │
       ▼            ▼            ▼                         │
┌────────────┐┌───────────┐┌──────────────┐                │
│color_logger││resilience ││  mock_llm    │◄───────────────┘
│            ││           ││              │
│ log_info() ││ @graceful ││ MockLLM      │
│ log_success││ _fallback ││  .generate() │
│ log_error()││           ││  Routes R1-R6│
│ log_warning││ safe_     ││              │
│ log_mock() ││ invoke()  ││              │
│ log_step() ││           ││              │
└──────┬─────┘└─────┬─────┘└──────────────┘
       │            │
       │◄───────────┘  resilience.py imports color_logger
       │
       ▼
┌──────────────┐
│ data/        │
│ sample_ad_   │
│ campaign.csv │
└──────────────┘
```

---

## Notebook Sections

| Section | Chapter Reference | What It Demonstrates |
|:---|:---|:---|
| **0. Setup and Configuration** | — | Imports, `.env` loading, `getpass` fallback, Simulation Mode detection |
| **1. The Tool-Using Agent** | Section 7.1 | Tool chest functions (`load_csv`, `group_by_and_aggregate`, `plot_bar_chart`, `plot_line_chart`), tool registry, data-viz pipeline |
| **2. Tool Discovery and Selection** | Section 7.2 | `parse_query` intent classifier, selection funnel demonstration |
| **3. Error Handling and Resilience** | Section 7.3 | `data_viz_agent` orchestrator, `@graceful_fallback` in action, deliberate failure scenarios |
| **4. Chain-of-Agents Orchestrator** | Sections 7.4–7.5 | `NewsAgent`, `FinancialAgent`, `SentimentAgent`, manager agent, shared episodic memory |
| **5. Conflict Resolution** | Section 7.6 | `ManagerAgent._synthesize_report()` with `conflict_score` detection |
| **6. Agentic Workflow: E-Commerce** | Section 7.7 | `workflow_manager_agent`, `llm_analyst_agent`, HITL simulation with 3 test orders |
| **7. Agentic Workflow: Insurance Claims** | Section 7.7b | State machine with 5 agents, guard conditions, CLM-4821 walkthrough, 3 test claims |
| **8. Summary and Key Takeaways** | Summary | Recap of all three architectural patterns, pointers to Chapter 8 |

---

## Simulation Mode

The notebook supports two operating modes:

**Simulation Mode** (default — no API key required):
- All LLM calls are routed through `MockLLM`, which returns chapter-derived mock data.
- HITL prompts auto-approve after a 2-second delay.
- Every mock response is tagged with a Cyan `[MOCK]` log badge.
- The notebook runs to completion with zero external dependencies.

**Live Mode** (optional — requires OpenAI API key):
- Create `.env` from `.env.template` and add your key.
- LLM calls go to the OpenAI API via `openai>=1.60`.
- HITL prompts use real `input()` for interactive decisions.

The mode is detected automatically at startup:

```
Simulation Mode startup banner:
[MOCK] ╔══════════════════════════════════════════════════════════╗
[MOCK] ║  SIMULATION MODE ACTIVE                                 ║
[MOCK] ║  All LLM calls return chapter-derived mock responses.   ║
[MOCK] ║  To use a live API, create .env from .env.template      ║
[MOCK] ╚══════════════════════════════════════════════════════════╝
```

---

## Visual Logging

All agent actions produce color-coded output for clear observability:

| Badge | Color | Meaning |
|:---|:---|:---|
| `[INFO]` | Blue | General informational messages |
| `[SUCCESS]` | Green | Tool or agent step completed |
| `[ERROR]` | Red | Exception caught, fallback activated |
| `[WARNING]` | Yellow | Threshold breached or escalation triggered |
| `[MOCK]` | Cyan | Simulation Mode data returned |
| `[Section X \| Step N]` | Blue | Pedagogical step marker with section reference |

---

## Case Studies

The notebook implements three complete case studies from the chapter:

**1. Data Visualization Assistant** (Sections 7.1–7.3) — A single Tool-Using agent that parses natural language queries, selects visualization tools via a selection funnel, and orchestrates a multi-step data pipeline with error recovery. Powered by `data/sample_ad_campaign.csv`.

**2. Market Intelligence Platform** (Sections 7.4–7.6) — A chain-of-agents orchestrator where `NewsAgent`, `FinancialAgent`, and `SentimentAgent` contribute findings to shared episodic memory. A `ManagerAgent` synthesizes a final report with conflict detection.

**3. E-Commerce & Insurance Workflows** (Section 7.7) — Agentic workflow systems modeled as state machines with guard conditions, HITL checkpoints, and audit trails. Includes the CLM-4821 insurance claim walkthrough from the book.

---

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to common dependency conflicts, environment issues, runtime problems, and platform-specific notes.

---

## Author

**Imran Ahmad** — Author of *Agents* (Packt, 2026).

This repository accompanies Chapter 7: Tool Manipulation and Orchestration Agents. For the full text, figures, and theoretical foundations, refer to the book.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
