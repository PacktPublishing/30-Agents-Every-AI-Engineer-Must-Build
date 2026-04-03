# Chapter 9: Software Development Agents

**Book:** *Agents* by Imran Ahmad (Packt, 2026)
**Chapter:** 9 — Software Development Agents

> *"The art of programming is the art of organizing and mastering complexity."*
> — Edsger Dijkstra

---

## Overview

This repository contains the companion code for **Chapter 9** of the book *Agents* by Imran Ahmad. The chapter explores how AI agents are reshaping software development through three distinct but interconnected capabilities:

- **Code-Generation Agents (§9.2)** — Transform natural language specifications into working, tested implementations using Test-Driven Generation (TDG) and multi-agent orchestration with LangGraph.
- **Compliance-Driven Agents (§9.3)** — Embed security and policy awareness directly into the development workflow, enforcing PCI DSS, HIPAA, and organizational rules through a *scan → evaluate → remediate* loop.
- **Self-Improving Agents (§9.4)** — Learn from operational feedback, evolving strategies through a closed-loop *execute → observe → learn → adapt* control system with human-in-the-loop checkpoints.

The notebook demonstrates all three agent architectures end-to-end, with progressive examples that build from a single shipping calculator function to a full-stack user profile feature and production compliance pipelines.

---

## Prerequisites

- **Python 3.10+** (required for `TypedDict`, `Annotated` support)
- **pip** package manager
- **Jupyter Notebook** or **JupyterLab** (or VS Code with Jupyter extension)

No external API key is required. The repository runs fully in **Simulation Mode** by default.

---

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/Agents.git
cd Agents/ch09-software-development-agents

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the notebook
jupyter notebook ch09_software_dev_agents.ipynb
```

All cells execute in **Simulation Mode** without any configuration. To use a live OpenAI API key, copy `.env.template` to `.env` and add your key.

---

## Simulation Mode

The entire notebook is designed to run without an external API key. When no key is detected, the system automatically activates **Simulation Mode**, which uses `MockLLM` to return chapter-accurate mock responses for every agent interaction.

The API key resolution chain follows a zero-hardcode policy:

1. `.env` file (via python-dotenv)
2. `OPENAI_API_KEY` environment variable
3. Interactive `getpass` prompt
4. **Simulation Mode** fallback (automatic if all above are empty)

In Simulation Mode, every code-generation, compliance scan, and self-improvement cycle produces the same pedagogically meaningful output described in the chapter. Color-coded logging (Blue `[INFO]`, Green `[SUCCESS]`, Red `[HANDLED ERROR]`) is active throughout to make agent behavior visible.

---

## Section-to-Cell Mapping

| Notebook Section | Cells | Chapter Reference | Agent Architecture |
|:---|:---:|:---|:---|
| **Block A** — Setup & Configuration | 1–4 | Preamble | Environment, imports, mode detection |
| **Block B** — Code-Generation Agents | 5–18 | §9.2 | TDG shipping calculator (Stages 1–6), full-stack user profile (T1/T2/T3), LangGraph StateGraph |
| **Block C** — Compliance-Driven Agents | 19–27 | §9.3 | PolicyEngine, static validation, semantic analysis, PCI DSS case study, audit trail |
| **Block D** — Self-Improving Agents | 28–37 | §9.4 | Sensing Layer, Critic Agent, Planner Agent, HITL checkpoint, customer support case study |
| **Block E** — Summary & Metrics | 38–40 | Summary | Cross-section comparison, execution metrics |

---

## Repository Structure

```
ch09-software-development-agents/
├── ch09_software_dev_agents.ipynb   # Primary notebook (narrative spine)
├── src/
│   ├── __init__.py                  # Package marker
│   ├── utils.py                     # Environment, ColorLog, @fail_gracefully
│   ├── state_models.py              # Pydantic: Task, AgentState, ImprovementHypothesis
│   ├── mock_llm.py                  # MockLLM (12 response entries), MockTestRunner
│   ├── agent_nodes.py               # LangGraph node functions, build_workflow()
│   ├── compliance_engine.py         # PolicyEngine, ComplianceScanner, AuditTrail
│   └── self_improving.py            # SensingLayer, CriticAgent, PlannerAgent
├── README.md                        # This file
├── AGENTS.md                        # Agentic metadata (2026 standard)
├── requirements.txt                 # Pinned dependencies
├── troubleshooting.md               # 8 common issues with resolutions
├── .env.template                    # API key template
├── .gitignore                       # Excludes .env, __pycache__, checkpoints
└── LICENSE                          # MIT License
```

---

## Feedback Loop Reference

Each agent class implements a characteristic feedback loop:

| Agent Class | Loop Pattern | Chapter Section |
|:---|:---|:---|
| Code-Generation | generate → test → refine | §9.2 |
| Compliance-Driven | scan → evaluate → remediate | §9.3 |
| Self-Improving | execute → observe → learn → adapt | §9.4 |

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Author

**Imran Ahmad** — Author of *Agents* (Packt, 2026)
