# Chapter 1: Foundations of Agent Engineering

**Book:** *AI Agents* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 1** of *AI Agents*. It transforms the chapter's theoretical foundations into runnable Python code, covering the cognitive loop, agent brain patterns, interoperability protocols, interaction paradigms, the Agentic AI Progression Framework, and real-world business case studies.

Every code cell runs **without an API key** in Simulation Mode, powered by a `MockLLM` engine that returns chapter-derived responses. When an OpenAI API key is provided, the notebook seamlessly switches to Live Mode.

## Quickstart

```bash
# 1. Clone and enter the repository
git clone https://github.com/<your-org>/ch01-foundations-of-agent-engineering.git
cd ch01-foundations-of-agent-engineering

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
jupyter notebook ch01_foundations_of_agent_engineering.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | Imports, API key detection, mode selection |
| **1** | §1.1 — Introducing Agents | Timeline of AI agent evolution (four eras) |
| **2** | §1.2.1 — The Cognitive Loop | Perceive → Reason → Plan → Act → Learn pipeline |
| **3** | §1.2.3 — Agent Brain Patterns | ReactiveAgent, DeliberativeAgent, HybridAgent |
| **4** | §1.3.1 — Model Context Protocol | MCPRegistry: tool registration, discovery, invocation |
| **5** | §1.3.2 — A2A Protocols | AgentMessage passing in a three-agent pipeline |
| **6** | §1.5 — Interaction Paradigms | Levels 1–5: Direct LLM → Multi-Agent System |
| **7** | §1.6 — Progression Framework | Maturity model Levels 0–4 with self-assessment |
| **8** | §1.7 — Business Impact | Quandri, My AskAI, Enterprise Bot case studies |
| **9** | Resilience Demo | Full-failure demonstration (failure_rate=1.0) |
| **10** | Summary | Key takeaways and Chapter 2 preview |

## Repository Structure

```
ch01-foundations-of-agent-engineering/
│
├── README.md                          # This file
├── AGENTS.md                          # Agentic AI Foundation 2026 metadata
├── requirements.txt                   # Pinned Python dependencies
├── .env.template                      # API key template (zero-hardcode policy)
├── .gitignore                         # Standard Python + .env exclusions
├── TROUBLESHOOTING.md                 # Dependency conflict resolution guide
│
├── ch01_foundations_of_agent_engineering.ipynb   # Primary deliverable
│
└── src/
    ├── __init__.py                    # Package init with version + author
    ├── mock_llm.py                    # MockLLM class + 22-entry response bank
    └── utils.py                       # Color logger, @graceful_fallback, detect_api_key
```

## Simulation Mode

When no API key is detected, the notebook activates **Simulation Mode**:

- `MockLLM` replaces the OpenAI client transparently
- All 22 responses are pre-authored from Chapter 1 content
- A yellow `SIMULATION MODE` banner confirms activation at startup
- Every cell executes successfully with no external dependencies

API key detection follows a three-tier cascade: `.env` file → environment variable → interactive prompt → Simulation Mode.

## Resilience Architecture

All agent operations are wrapped in the `@graceful_fallback` decorator:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

The Resilience Demo cell (Cell Group 9) uses `MockLLM(failure_rate=1.0)` to trigger 100% failures, demonstrating that every operation degrades gracefully.

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt`
- **API Key:** Optional (Simulation Mode works without one)

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to common issues including module import errors, ANSI color rendering, and Python version compatibility.

## License

This code is provided as educational companion material for *AI Agents* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *AI Agents* (Packt Publishing, 2026)
