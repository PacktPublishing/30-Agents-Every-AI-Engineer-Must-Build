# Chapter 2: The Agent Engineer's Toolkit

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 2** of *30 Agents Every AI Engineer Must Build*. It covers the full agent engineering stack: frameworks (LangChain, LangGraph, LlamaIndex, AutoGPT, CrewAI, AutoGen), LLM selection guidelines, vector databases, RAG pipelines, tool integration patterns, and cloud-native development platforms.

Every code cell runs **without an API key** in Simulation Mode, powered by a `MockLLM` layer that returns chapter-derived responses. When an OpenAI API key is provided, the notebook seamlessly switches to Live Mode.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter02

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
jupyter notebook chapter_02_agent_toolkit.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **1** | Setup | Environment setup, API key auto-detection, mode banner |
| **2** | §2.1 — Framework Landscape | Comparison of LangChain, LangGraph, LlamaIndex, AutoGPT, CrewAI, AutoGen |
| **3** | §2.2 — LangChain Agent | ReAct pattern with Calculator + WebSearch tools |
| **4** | §2.2 — LangChain Memory | Buffer vs. Summary memory comparison |
| **5** | §2.3 — LangGraph Workflow | Stateful graph: research → analyze → decide → respond |
| **6** | §2.3 — LangGraph State | TypedDict schema + Mermaid diagram |
| **7** | §2.4 — Framework Selection | Selection criteria + integration patterns |
| **8** | §2.5 — Hybrid Routing | Multi-model query router (Mistral/Claude/GPT-4o) |
| **9** | §2.6 — RAG Pipeline | Simulated vector search with similarity scores |
| **10** | §2.7 — LangChain Tools | StockPriceTool abstraction pattern |
| **11** | §2.8 — Function Calling | OpenAI JSON schema + mock execution |
| **12** | §2.9 — Cloud Platforms | AWS / Azure / Google Cloud comparison |
| **13** | Summary | Chapter takeaways and next steps |

## Repository Structure

```
chapter02/
│
├── README.md                            # This file
├── .gitkeep                             # Git placeholder
├── chapter_02_agent_toolkit.ipynb       # Primary deliverable
└── mock_llm_layer.py                    # Mock infrastructure module
```

## Simulation Mode

When no API key is detected, the notebook activates **Simulation Mode**:

- `MockLLM` replaces the OpenAI client transparently
- All responses are pre-authored from Chapter 2 content
- A `[SIMULATION]` prefix confirms activation at startup
- Every cell executes successfully with no external dependencies

Both modes use color-coded logging:
- **Blue** `[INFO]`: Agent initialization, step entry
- **Green** `[SUCCESS]`: Completed steps, valid returns
- **Red** `[HANDLED ERROR]`: Caught exceptions, fallback activation

## Pre-Executed Example Runs

Two pre-executed notebooks are included so you can review the full output without running any code or installing dependencies:

| Notebook | Mode | Description |
|---|---|---|
| [EXAMPLE_RUN_SIMULATION_MODE_chapter_02_agent_toolkit.ipynb](EXAMPLE_RUN_SIMULATION_MODE_chapter_02_agent_toolkit.ipynb) | Simulation | Executed without an API key — MockLLM responses |
| [EXAMPLE_RUN_LLM_MODE_chapter_02_agent_toolkit.ipynb](EXAMPLE_RUN_LLM_MODE_chapter_02_agent_toolkit.ipynb) | Live LLM | Executed with an OpenAI API key — real GPT responses |

Compare both to see how Simulation Mode mirrors Live LLM behavior.

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt`
- **API Key:** Optional (Simulation Mode works without one)

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
