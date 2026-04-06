# Chapter 16: Embodied and Physical World Agents

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 16** of *30 Agents Every AI Engineer Must Build*. It implements two complementary agent architectures: the Embodied Intelligence Agent (real-time single-domain control with millisecond precision, hard safety guarantees, and an asymmetric control loop separating high-latency LLM reasoning from low-latency deterministic control) and the Domain-Transforming Integration Agent (cross-domain coordination via typed knowledge graphs with weighted breadth-first influence propagation). A drone mission case study in Ottawa's winter conditions synthesizes both architectures into a composed system with a Unified Constraint Envelope.

Every code cell runs **without an API key** in Simulation Mode, powered by `MockChatOpenAI` and `MockGraph` that return chapter-derived responses. When an OpenAI API key is provided, the notebook seamlessly switches to Live Mode.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter16

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
jupyter notebook chapter16_embodied_agents.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | Imports, environment detection, Simulation Mode flag |
| **1** | Listing 16.1 — Common Patterns | Shared interface stubs for embodied agents |
| **2** | Listing 16.2 — Embodied Agent | 4-responsibility tool decomposition |
| **3** | Listing 16.3 — Safety-Constrained Loop | Multi-rate perception-action integration with safety constraints |
| **4** | Listing 16.4 — Knowledge Graph | Cross-domain knowledge graph construction |
| **5** | Listing 16.5 — Influence Propagation | Weighted breadth-first traversal for impact estimation |
| **6** | Listing 16.6 — Ottawa Case Study (Drone) | Embodied drone agent + mission execution |
| **7** | Listing 16.7 — Constraint Assembler | Cross-domain constraint assembler + NOTAM integration |
| **8** | Failure Scenarios | Wind RED, Battery RED, NOTAM active, API timeout demos |

## Real-World Use Case: ArcticWing Aerial

How does a drone services company operating in Ottawa winters reduce its 38% flight scrub rate while maintaining Transport Canada safety compliance? The companion case study follows **ArcticWing Aerial** as they deploy the Unified Constraint Envelope (binary AND across 9 constraints in 5 domains) to make deterministic go/no-go decisions, and the cross-domain cascade analyzer to detect when a power outage 3 hops away will block road access to the launch site.

Read the full case study: **[USECASE.md](USECASE.md)** — includes the 5 failure scenarios (wind, battery, NOTAM, timeout, stale data), safety margin calculations, and fleet utilization impact.

## Repository Structure

```
chapter16/
│
├── README.md                              # This file
├── AGENTS.md                              # Agentic AI metadata
├── LICENSE                                # MIT License
├── requirements.txt                       # Pinned Python dependencies
├── .env.template                          # API key template (zero-hardcode policy)
├── .gitignore                             # Standard Python + .env exclusions
├── TROUBLESHOOTING.md                     # Dependency conflict resolution guide
│
├── chapter16_embodied_agents.ipynb        # Primary deliverable
│
├── __init__.py                            # Package init; exports get_llm(), ColorLogger
├── mock_layer.py                          # MockChatOpenAI, MockGraph, synthetic sensor data
└── resilience.py                          # @fail_gracefully decorator + color-coded logging
```

## Simulation Mode

When no API key is detected, the notebook activates **Simulation Mode**:

- `MockChatOpenAI` replaces the OpenAI client transparently
- `MockGraph` provides synthetic sensor and API data
- Safety thresholds are identical to Live Mode
- Failure demos use pre-scripted RED scenarios
- Every cell executes successfully with no external dependencies

API key detection follows a three-tier cascade: `.env` file → environment variable → interactive prompt → Simulation Mode.

## Pre-Executed Example Runs

Two pre-executed notebooks are included so you can review the full output without running any code or installing dependencies:

| Notebook | Mode | Description |
|---|---|---|
| [EXAMPLE_RUN_SIMULATION_MODE_chapter16_embodied_agents.ipynb](EXAMPLE_RUN_SIMULATION_MODE_chapter16_embodied_agents.ipynb) | Simulation | Executed without an API key — MockLLM responses |
| [EXAMPLE_RUN_LLM_MODE_chapter16_embodied_agents.ipynb](EXAMPLE_RUN_LLM_MODE_chapter16_embodied_agents.ipynb) | Live LLM | Executed with an OpenAI API key — real GPT responses |

Compare both to see how Simulation Mode mirrors Live LLM behavior.

## Resilience Architecture

All agent operations are wrapped in the `@fail_gracefully` decorator:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

The chapter's central engineering principle: **conservative constraint fusion** — autonomous systems must satisfy all constraints simultaneously, with safety enforced as a precondition for action rather than an afterthought.

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt`
- **API Key:** Optional (Simulation Mode works without one)

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to 7 common dependency issues.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
