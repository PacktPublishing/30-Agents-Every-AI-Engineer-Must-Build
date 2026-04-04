# Chapter 13: Healthcare and Scientific Agents

**Book:** *30 Agents Every AI Engineer Must Build*
**Author:** Imran Ahmad
**Publisher:** Packt Publishing, 2026
**Chapter:** 13 — Healthcare and Scientific Agents
**Chapter Pages:** pp. 361–389

---

## Overview

This repository contains the companion code for Chapter 13, which explores two agent architectures designed for high-stakes, information-intensive domains:

- **Healthcare Intelligence Agent** — A four-layer architecture separating data ingestion, clinical knowledge integration, Bayesian diagnostic reasoning, and audience-adapted explanation generation. Includes safety escalation, provenance tracking, and immutable audit trails.

- **Scientific Discovery Agent** — A multi-phase pipeline for fault-tolerant literature synthesis, information-theoretic knowledge gap detection, abductive hypothesis generation, and closed-loop experimental feedback.

Both agents demonstrate that in domains where errors carry serious consequences, safety and compliance must be designed in as first-class architectural layers — not bolted on after the fact.

## Repository Structure

```
chapter13-healthcare-scientific-agents/
│
├── chapter13_healthcare_scientific_agents.ipynb   # Single self-contained notebook
├── AGENTS.md              # Agentic metadata and AI collaborator persona
├── README.md              # This file
├── requirements.txt       # Pinned dependencies with compatibility notes
├── .env.template          # API key placeholders (all optional)
└── troubleshooting.md     # Preemptive dependency conflict resolutions
```

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd 30-Agents-Every-AI-Engineer-Must-Build/chapter13

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Configure API keys
cp .env.template .env
# Edit .env with your keys — or skip this step entirely

# 5. Run the notebook
jupyter notebook chapter13_healthcare_scientific_agents.ipynb
```

## Simulation Mode

**No API keys are required.** The notebook runs fully in Simulation Mode, using context-aware mock responses derived directly from Chapter 13 content. Every LLM call, database query, and external API request has a deterministic fallback that produces the same outputs discussed in the book.

To enable live mode, add your OpenAI API key to `.env` or enter it when prompted.

## Technical Requirements

- Python 3.10 or later
- Key packages: `numpy`, `langchain-core`, `langchain-community`, `fhir.resources`, `aiohttp`, `scipy`, `python-dotenv`
- See `requirements.txt` for pinned version ranges
- See `troubleshooting.md` for known dependency conflicts and fixes

## Notebook Sections

| Section | Topic | Book Reference |
|:--------|:------|:---------------|
| 0 | Setup and Configuration | Technical Requirements (p. 362) |
| 1 | Simulation Infrastructure | Cross-cutting |
| 2 | Healthcare Intelligence Agent | §13.1–13.4 (pp. 362–375) |
| 3 | Scientific Discovery Agent | §13.5–13.8 (pp. 375–387) |
| 4 | Cross-Domain Analysis | §13.9 (pp. 387–389) |

## License

This project is provided as educational material accompanying the book. See the [Packt Publishing repository](https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build) for license details.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
