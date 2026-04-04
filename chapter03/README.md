# Chapter 3: The Art of Agent Prompting

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 3** of *30 Agents Every AI Engineer Must Build*. It transforms every concept in the chapter — from the PTCF framework to Tree-of-Thought prompting — into runnable, interactive code. Topics include cognitive programming, two-layer prompt architecture, the Persona-Task-Context-Format blueprint, task decomposition, few-shot learning, chain-of-thought reasoning, and multi-agent communication protocols.

Every code cell runs **without an API key** in Simulation Mode, powered by a `MockLLM` engine that returns chapter-derived responses. When an OpenAI API key is provided, the notebook seamlessly switches to Live Mode.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter03

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
jupyter notebook chapter_03_agent_prompting.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | Imports, API key detection, mode selection |
| **1** | §3.1 — From Instructions to Constitutions | Cognitive programming, persona constraints |
| **2** | §3.2 — Two-Layer Prompt Architecture | System prompt vs. user prompt |
| **3** | §3.3 — The PTCF Blueprint | Persona, Task, Context, Format framework |
| **4** | §3.4 — Designing Thinking Agents | Agent capability spectrum, task decomposition |
| **5** | §3.5 — Teaching by Example | Few-shot learning, ticket classification |
| **6** | §3.6 — Making Reasoning Visible | Chain-of-thought and Tree-of-thought prompting |
| **7** | §3.7 — Architecting Collaboration | Multi-agent communication protocols |
| **8** | Case Studies | SaaS triage, compliance review, code review |
| **9** | Evaluation | A/B comparison, regression testing |

## Repository Structure

```
chapter03/
│
├── README.md                          # This file
├── AGENTS.md                          # Agentic AI metadata
├── LICENSE                            # MIT License
├── requirements.txt                   # Pinned Python dependencies
├── .env.template                      # API key template (zero-hardcode policy)
├── .gitignore                         # Standard Python + .env exclusions
├── troubleshooting.md                 # Dependency conflict resolution guide
│
├── chapter_03_agent_prompting.ipynb   # Primary deliverable
│
├── mock_llm.py                        # MockLLM — simulation engine
└── utils.py                           # Color logger, @graceful_fallback
```

## Simulation Mode

When no API key is detected, the notebook activates **Simulation Mode**:

- `MockLLM` subclasses `BaseChatModel` for full LangChain pipe-operator (`|`) compatibility
- Routes responses via keyword matching to return section-appropriate mock data
- Produces the same structured outputs as a live model
- Every cell executes successfully with no external dependencies

All LLM calls are wrapped in the `@graceful_fallback` decorator — if anything fails, you see a Red `[HANDLED ERROR]` log (never a traceback) and the notebook continues.

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt`
- **API Key:** Optional (Simulation Mode works without one)

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for solutions to common dependency conflicts and environment issues.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
