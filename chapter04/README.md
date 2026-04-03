# Chapter 4: Agent Deployment and Responsible Development

**Book:** *Agents* by Imran Ahmad (Packt, 2026)
**Chapter:** 4 — Agent Deployment and Responsible Development
**Author:** Imran Ahmad

---

## Overview

This repository is the companion code for Chapter 4 of *Agents*. The chapter addresses the critical shift from prototype to production for AI agent systems, covering six interconnected domains: infrastructure scaling by agent typology, cost-aware model routing, high-throughput resilience patterns, microservice-based cognitive architectures, zero-trust security, and ethical fairness auditing. The notebook translates every major concept — including figures, tables, and the book's circuit-breaker code — into runnable, interactive demonstrations backed by a full Simulation Mode that requires no API key.

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/imran-ahmad/chapter-04-agent-deployment.git
cd chapter-04-agent-deployment

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the notebook
jupyter notebook chapter_04_agent_deployment.ipynb
```

The notebook detects whether an OpenAI API key is available and automatically activates **Simulation Mode** if none is found. No additional configuration is needed.

---

## Simulation Mode

Every external dependency (OpenAI API, HTTP tool endpoints) is backed by a deterministic mock layer in `src/mock_llm.py`. When no API key is present, the notebook runs with full functionality using chapter-derived mock responses — every mock value is traceable to a specific page, table, or figure in the book.

To enable live mode, copy `.env.template` to `.env` and add your key:

```bash
cp .env.template .env
# Edit .env and replace your-api-key-here with your actual key
```

---

## Notebook Section Guide

| Cell | Section | Topic | Chapter Reference |
|:-----|:--------|:------|:------------------|
| 0 | Setup | Environment detection, Simulation Mode banner | Preamble |
| 1 | 4.1 | Agent Typology Simulator — infrastructure profiles for reactive, deliberative, hybrid, and multi-agent systems | Figure 4.1, pp. 3–6 |
| 2 | 4.2 | Cost-Aware Model Router — tiered routing, caching, budget enforcement | Figure 4.2, pp. 7–10 |
| 3 | 4.3 | Circuit Breaker and Resilience — tenacity-based breaker with state transitions and fallback | Table 4.1, pp. 11–15 |
| 4 | 4.4 | Microservice Pipeline Simulation — five-service chain from Planner to Response Synthesizer | Table 4.2, p. 13 |
| 5 | 4.5 | Threat Detection and Zero Trust — adversarial input classification across nine attack vectors | Tables 4.3a/b, pp. 18–21 |
| 6 | 4.6 | Fairness and Bias Audit — demographic parity and equalized opportunity with pre/post-mitigation comparison | Figure 4.3, p. 24 |
| 7 | Ref | Toolchain Reference Explorer — formatted display of all tools cited in the chapter | Table 4.5, pp. 27–29 |
| 8 | Summary | Cost Dashboard and section completion status | All sections |

---

## Repository Structure

```
chapter-04-agent-deployment/
│
├── README.md                              # This file
├── AGENTS.md                              # Agentic metadata and AI persona prompt
├── LICENSE                                # MIT License
├── requirements.txt                       # Pinned dependencies
├── .env.template                          # API key placeholder
├── .gitignore                             # .env, __pycache__, checkpoints
│
├── chapter_04_agent_deployment.ipynb      # Primary notebook
│
├── src/
│   ├── __init__.py                        # Package metadata
│   ├── mock_llm.py                        # MockLLM, RESPONSE_BANK, SyntheticDataFactory
│   └── agent_utils.py                     # AgentLogger, @fail_gracefully, CostTracker,
│                                          #   CircuitBreaker, InputValidator, format_table()
│
└── docs/
    └── TROUBLESHOOTING.md                 # Dependency conflict resolution guide
```

---

## Key Components

**`src/agent_utils.py`** — Shared infrastructure utilities:
- `AgentLogger` — Color-coded ANSI logging (Blue for info, Green for success, Red for handled errors)
- `@fail_gracefully` — Resilience decorator that catches exceptions and returns fallback values
- `CostTracker` — Per-call cost accounting with configurable budget ceiling and degradation
- `CircuitBreaker` — State-machine breaker (closed → open → half_open) extending the book's code from pp. 14–15
- `InputValidator` — Prompt sanitisation against attack patterns from Tables 4.3a/b

**`src/mock_llm.py`** — Simulation engine:
- `RESPONSE_BANK` — 20 section-keyed mock responses, each traceable to a specific chapter reference
- `MockLLM` — Per-section methods covering all six chapter domains
- `SyntheticDataFactory` — Deterministic dataset generators (seed=42) for fairness auditing, cost routing, threat detection, and circuit-breaker scenarios

---

## Further Reading

- [AGENTS.md](AGENTS.md) — AI persona prompt and interaction boundaries for this chapter
- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) — Solutions for common dependency and environment issues

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

Copyright (c) 2026 Imran Ahmad
