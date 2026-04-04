# Chapter 6 — Information Retrieval and Knowledge Agents

**Book:** *Agents* by Imran Ahmad (Packt, 2026)
**Author:** Imran Ahmad
**Chapter:** 6 — Information Retrieval and Knowledge Agents
**Pages:** 145–171

---

## Overview

This repository contains the companion code for **Chapter 6** (pp. 145–171), which explores three major categories of knowledge agents that extend the static capabilities of large language models into dynamic, evidence-grounded systems:

1. **Knowledge Retrieval Agent (§6.1, pp. 146–153)** — Implements a full RAG pipeline using LangChain, OpenAI embeddings, and FAISS. Demonstrates query understanding, retrieval, preprocessing, and grounded answer generation with provenance tracking.

2. **Document Intelligence Agent (§6.2, pp. 153–160)** — Builds a five-stage document processing pipeline covering ingestion, OCR with confidence scoring, layout parsing, schema-driven extraction, and validation. Processes a synthetic invoice to extract structured fields.

3. **Scientific Research Agent (§6.3, pp. 161–168)** — Performs automated literature synthesis across a research corpus using semantic embeddings, thematic clustering (KMeans), and extractive summarization. Produces a structured synthesis report with evidence tables.

All agents are implemented in a single Jupyter notebook with shared utilities for logging, resilience, and simulation.

## Quick Start

```bash
# 1. Clone the repository
git clone <repo-url>
cd chapter-06-knowledge-agents

# 2. (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Configure API key for Live Mode
cp .env.template .env
# Edit .env and add your OPENAI_API_KEY

# 5. Launch the notebook
jupyter notebook chapter_06_knowledge_agents.ipynb
```

No API key is required. The notebook runs fully in **Simulation Mode** by default, producing chapter-derived mock outputs that are pedagogically equivalent to live API responses.

## Repository Structure

```
chapter-06-knowledge-agents/
│
├── README.md                              ← You are here
├── AGENTS.md                              ← Agentic metadata + persona prompt
├── LICENSE                                ← MIT License
├── requirements.txt                       ← Pinned dependencies (Python >= 3.10)
├── .env.template                          ← API key placeholder
├── .gitignore                             ← .env, __pycache__, checkpoints
│
├── chapter_06_knowledge_agents.ipynb      ← Primary notebook — all 3 agents
├── agent_utils.py                         ← ColorLogger, MockLLM, decorators
│
├── docs/                                  ← Synthetic corpus for RAG demo
│   ├── knowledge_base_rag.txt             ← RAG concepts and limitations
│   └── compliance_policy.txt              ← Sample policy doc for retrieval
│
├── samples/                               ← Inputs for Document Intelligence
│   └── sample_invoice.png                 ← Programmatically generated invoice
│
└── troubleshooting.md                     ← Dependency conflict resolution
```

## Execution Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Simulation Mode** (default) | No API key provided | All outputs use chapter-derived mocks via `agent_utils.py` |
| **Live Mode** | Valid `OPENAI_API_KEY` in `.env` | Full API calls to OpenAI, live arXiv queries, real OCR |

Both modes produce pedagogically equivalent output. Simulation Mode is the default and expected path for most readers. Every external call is wrapped in a `@fail_gracefully` decorator that catches exceptions and falls back to mock output automatically.

## Chapter Sections Covered

| Notebook Section | Chapter Reference | Book Pages | Agent Type | Key Concepts |
|---|---|:---:|---|---|
| 0. Setup & Configuration | — | — | — | API key management, Simulation Mode gate |
| 1. Knowledge Retrieval Agent | §6.1 | 146–153 | Retrieval | RAG pipeline, FAISS, RetrievalQA, provenance |
| 2. Chunking Strategies Deep Dive | §6.1 | 151 | Retrieval | Fixed, recursive, semantic chunking comparison |
| 3. Document Intelligence Agent | §6.2 | 153–160 | Doc Intel | OCR, confidence thresholding, schema extraction |
| 4. Scientific Research Agent | §6.3 | 161–168 | Research | arXiv search, embeddings, KMeans clustering, synthesis |
| 5. Knowledge Agent Spectrum | §Summary | 168–170 | All | Comparison table, capability levels |

## Key Figures

| Figure | Description | Book Page |
|:---|:---|:---:|
| Figure 6.1 | Modular architecture of a Knowledge Retrieval agent | 148 |
| Figure 6.2 | Document intelligence pipeline (five-stage) | 159 |
| Table 6.1 | Comparison of knowledge agent types | 169 |

## Key Technical Patterns

- **ColorLogger** — ANSI color-coded logging (Blue=INFO, Green=SUCCESS, Red=ERROR) replaces all raw `print()` calls
- **@fail_gracefully** — Resilience decorator on every external call; logs errors with chapter section references and returns fallback values
- **MockLLM / MockEmbeddings** — Keyword-routed, chapter-derived response registry enabling full Simulation Mode without API keys
- **Zero-Hardcode Policy** — API keys resolved via `.env` → environment → interactive prompt → Simulation Mode

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for solutions to common issues including FAISS installation, Tesseract setup, sentence-transformers model downloads, and LangChain import errors.

## AI Assistant Integration

See [AGENTS.md](AGENTS.md) for the agentic persona prompt, capability declaration, and file map that any AI coding assistant should adopt when working with this repository.

## Author

**Imran Ahmad** — Author of *Agents* (Packt, 2026)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
