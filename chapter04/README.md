# Chapter 4: Agent Deployment and Responsible Development

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 4** of *30 Agents Every AI Engineer Must Build*. The chapter addresses the critical shift from prototype to production for AI agent systems, covering six interconnected domains: infrastructure scaling by agent typology, cost-aware model routing, high-throughput resilience patterns, microservice-based cognitive architectures, zero-trust security, and ethical fairness auditing.

Every code cell runs **without an API key** in Simulation Mode, powered by a `MockLLM` engine that returns chapter-derived responses. When an OpenAI API key is provided, the notebook seamlessly switches to Live Mode.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter04

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
jupyter notebook chapter_04_agent_deployment.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | Environment detection, Simulation Mode banner |
| **1** | §4.1 — Agent Typology | Infrastructure profiles for reactive, deliberative, hybrid, and multi-agent systems |
| **2** | §4.2 — Cost-Aware Routing | Tiered routing, caching, budget enforcement |
| **3** | §4.3 — Circuit Breaker | Tenacity-based breaker with state transitions and fallback |
| **4** | §4.4 — Microservice Pipeline | Five-service chain from Planner to Response Synthesizer |
| **5** | §4.5 — Threat Detection | Adversarial input classification across nine attack vectors |
| **6** | §4.6 — Fairness Audit | Demographic parity and equalized opportunity with pre/post-mitigation comparison |
| **7** | Reference | Toolchain Reference Explorer — formatted display of all tools cited in the chapter |
| **8** | Summary | Cost Dashboard and section completion status |

## Repository Structure

```
chapter04/
│
├── README.md                              # This file
├── AGENTS.md                              # Agentic metadata and AI persona prompt
├── LICENSE                                # MIT License
├── requirements.txt                       # Pinned Python dependencies
├── .env.template                          # API key template (zero-hardcode policy)
├── .gitignore                             # Standard Python + .env exclusions
├── TROUBLESHOOTING.md                     # Dependency conflict resolution guide
│
├── chapter_04_agent_deployment.ipynb      # Primary deliverable
│
├── __init__.py                            # Package metadata
├── agent_utils.py                         # AgentLogger, @fail_gracefully, CostTracker,
│                                          #   CircuitBreaker, InputValidator
└── mock_llm.py                            # MockLLM, RESPONSE_BANK, SyntheticDataFactory
```

## Simulation Mode

When no API key is detected, the notebook activates **Simulation Mode**:

- `MockLLM` replaces the OpenAI client transparently
- All 20 section-keyed mock responses are traceable to specific chapter references
- `SyntheticDataFactory` generates deterministic datasets (seed=42) for fairness auditing, cost routing, and threat detection
- Every cell executes successfully with no external dependencies

API key detection follows a three-tier cascade: `.env` file → environment variable → interactive prompt → Simulation Mode.

## Resilience Architecture

All agent operations are wrapped in the `@fail_gracefully` decorator:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

Key infrastructure components include `CostTracker` (per-call accounting with budget ceiling), `CircuitBreaker` (closed → open → half_open state machine), and `InputValidator` (prompt sanitization against attack patterns).

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt`
- **API Key:** Optional (Simulation Mode works without one)

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to common issues including module import errors, ANSI color rendering, and Python version compatibility.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
