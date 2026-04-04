# Chapter 3: The Art of Agent Prompting

**Book:** *Agents* by Imran Ahmad (Packt Publishing, 2026)  
**Author:** Imran Ahmad  
**Chapter Pages:** 61–92

This repository is the standalone companion for Chapter 3 of *Agents*. It transforms every concept in the chapter — from the PTCF framework to Tree-of-Thought prompting — into runnable, interactive code.

---

## Quick Start (3 steps)

```bash
# 1. Clone and enter the directory
git clone <repo-url>
cd chapter-03-art-of-agent-prompting

# 2. Install dependencies
pip install -r requirements.txt

# 3. Open the notebook
jupyter notebook chapter_03_agent_prompting.ipynb
```

**No API key?** No problem. The notebook runs automatically in **Simulation Mode** using the built-in `MockLLM` engine — every demo produces meaningful, chapter-faithful output at zero cost.

**Have an API key?** Copy `.env.template` to `.env`, paste your OpenAI key, and restart the kernel for live GPT-4o output.

---

## Repository Structure

```
chapter-03-art-of-agent-prompting/
│
├── README.md                          # This file
├── AGENTS.md                          # Agentic metadata + AI persona prompt
├── LICENSE                            # MIT License
├── requirements.txt                   # Pinned dependencies
├── .env.template                      # API key template
├── .gitignore                         # Standard ignores
│
├── chapter_03_agent_prompting.ipynb   # PRIMARY: The reader's single entry point
│
├── mock_llm.py                        # MockLLM — simulation engine
├── utils.py                           # ColorLogger + @graceful_fallback
│
└── troubleshooting.md                 # Dependency conflict resolutions
```

---

## Chapter Section Mapping

**Chapter 3 spans pages 61–92 of the book.**

| Notebook Section | Chapter Reference | Pages | Key Concept |
|-----------------|-------------------|-------|-------------|
| §3.1 | From Instructions to Constitutions | pp. 61–63 | Cognitive programming, persona constraints |
| §3.2 | Two-Layer Prompt Architecture | pp. 64–67 | System prompt vs. user prompt |
| §3.3 | The PTCF Blueprint | pp. 67–72 | Persona, Task, Context, Format framework |
| §3.4 | Designing Thinking Agents | pp. 72–77 | Agent capability spectrum, task decomposition |
| §3.5 | Teaching by Example | pp. 77–80 | Few-shot learning, ticket classification |
| §3.6 | Making Reasoning Visible | pp. 81–85 | Chain-of-thought and Tree-of-thought prompting |
| §3.7 | Architecting Collaboration | pp. 86–88 | Multi-agent communication protocols |
| Case Studies | Production Contexts | pp. 88–90 | SaaS triage, compliance review, code review |
| Evaluation | Iterating Prompts | pp. 90–91 | A/B comparison, regression testing |

---

## Simulation Mode

All demos use a `MockLLM` engine that returns chapter-faithful responses when no API key is detected. The simulation engine:

- Subclasses `BaseChatModel` for full LangChain pipe-operator (`|`) compatibility
- Routes responses via keyword matching to return section-appropriate mock data
- Produces the same structured outputs you would see from a live model

Every LLM call is wrapped in the `@graceful_fallback` decorator — if anything fails, you see a Red `[HANDLED ERROR]` log (never a traceback) and the notebook continues.

### Visual Feedback System

- 🔵 **Blue [INFO]** — Operation starting
- 🟢 **Green [SUCCESS]** — Operation completed successfully
- 🔴 **Red [HANDLED ERROR]** — Error caught and handled gracefully

---

## Prerequisites

- Python 3.11+
- pip (package manager)
- Jupyter Notebook or JupyterLab

See `troubleshooting.md` for common dependency conflict resolutions.

---

## License

MIT License — see `LICENSE` file.

---

*Author: Imran Ahmad*  
*Book: Agents (Packt Publishing, 2026)*
