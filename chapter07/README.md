# Chapter 7: Tool Manipulation and Orchestration Agents

**Book:** *30 Agents Every AI Engineer Must Build*
**Author:** Imran Ahmad
**Publisher:** Packt Publishing, 2026
**Chapter Pages:** pp. 173–201

---

## Overview

This repository is the companion code for **Chapter 7** of *30 Agents Every AI Engineer Must Build*. It teaches three progressive architectural patterns for building production-ready AI agent systems:

1. **Tool-Using Agents** (Sections 7.1–7.3, pp. 174–186) — A single agent extends its reasoning by invoking external functions through a Think/Plan/Act cycle.
2. **Chain-of-Agents Orchestrators** (Sections 7.4–7.6, pp. 186–194) — Multiple specialized agents collaborate under a cooperation protocol with shared memory and conflict resolution.
3. **Agentic Workflow Systems** (Section 7.7, pp. 195–201) — Stateful business processes modeled as state machines with human-in-the-loop checkpoints and guard conditions.

The repository is built around a **Fail-Gracefully architecture**: if no API key is present, the system automatically enters **Simulation Mode**, returning chapter-derived mock data through a context-aware `MockLLM` class. Every agent action produces color-coded log output. Every tool invocation is wrapped in defensive logic. The notebook always runs to completion.

---

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd chapter07

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
chapter07-tool-orchestration-agents/
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

## Notebook Sections

| Section | Chapter Reference | Book Pages | What It Demonstrates |
|:---|:---|:---|:---|
| **0. Setup and Configuration** | — | pp. 173–174 | Imports, `.env` loading, `getpass` fallback, Simulation Mode detection |
| **1. The Tool-Using Agent** | Section 7.1 | pp. 174–179 | Tool chest functions (`load_csv`, `group_by_and_aggregate`, `plot_bar_chart`, `plot_line_chart`), tool registry, data-viz pipeline |
| **2. Tool Discovery and Selection** | Section 7.2 | pp. 179–183 | `parse_query` intent classifier, selection funnel demonstration |
| **3. Error Handling and Resilience** | Section 7.3 | pp. 183–186 | `data_viz_agent` orchestrator, `@graceful_fallback` in action, deliberate failure scenarios |
| **4. Chain-of-Agents Orchestrator** | Sections 7.4–7.5 | pp. 186–191 | `NewsAgent`, `FinancialAgent`, `SentimentAgent`, manager agent, shared episodic memory |
| **5. Conflict Resolution** | Section 7.6 | pp. 191–194 | `ManagerAgent._synthesize_report()` with `conflict_score` detection |
| **6. Agentic Workflow: E-Commerce** | Section 7.7 | pp. 195–197 | `workflow_manager_agent`, `llm_analyst_agent`, HITL simulation with 3 test orders |
| **7. Agentic Workflow: Insurance Claims** | Section 7.7b | pp. 198–200 | State machine with 5 agents, guard conditions, CLM-4821 walkthrough, 3 test claims |
| **8. Summary and Key Takeaways** | Summary | pp. 200–201 | Recap of all three architectural patterns, pointers to Chapter 8 |

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

---

## Case Studies

The notebook implements three complete case studies from the chapter:

**1. Data Visualization Assistant** (Sections 7.1–7.3, pp. 174–186) — A single Tool-Using agent that parses natural language queries, selects visualization tools via a selection funnel, and orchestrates a multi-step data pipeline with error recovery. Powered by `data/sample_ad_campaign.csv`.

**2. Market Intelligence Platform** (Sections 7.4–7.6, pp. 186–194) — A chain-of-agents orchestrator where `NewsAgent`, `FinancialAgent`, and `SentimentAgent` contribute findings to shared episodic memory. A `ManagerAgent` synthesizes a final report with conflict detection.

**3. E-Commerce & Insurance Workflows** (Section 7.7, pp. 195–201) — Agentic workflow systems modeled as state machines with guard conditions, HITL checkpoints, and audit trails. Includes the CLM-4821 insurance claim walkthrough from the book.

---

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to common dependency conflicts, environment issues, runtime problems, and platform-specific notes.

---

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026).

This repository accompanies Chapter 7: Tool Manipulation and Orchestration Agents. For the full text, figures, and theoretical foundations, refer to the book.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
