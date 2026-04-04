# Chapter 6: Information Retrieval and Knowledge Agents

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 6** of *30 Agents Every AI Engineer Must Build*. It explores three major categories of knowledge agents that extend LLMs into dynamic, evidence-grounded systems: the Knowledge Retrieval Agent (RAG pipeline with FAISS and provenance tracking), the Document Intelligence Agent (five-stage OCR and schema-driven extraction pipeline), and the Scientific Research Agent (literature synthesis with semantic clustering and extractive summarization).

Every code cell runs **without an API key** in Simulation Mode, powered by a `MockLLM` and `MockEmbeddings` layer that returns chapter-derived responses. When an OpenAI API key is provided, the notebook seamlessly switches to Live Mode.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter06

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
jupyter notebook chapter_06_knowledge_agents.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | API key management, Simulation Mode gate |
| **1** | §6.1 — Knowledge Retrieval Agent | RAG pipeline, FAISS, RetrievalQA, provenance tracking |
| **2** | §6.1 — Chunking Strategies | Fixed, recursive, and semantic chunking comparison |
| **3** | §6.2 — Document Intelligence Agent | OCR, confidence thresholding, schema-driven extraction |
| **4** | §6.3 — Scientific Research Agent | arXiv search, embeddings, KMeans clustering, synthesis |
| **5** | Summary — Knowledge Agent Spectrum | Comparison table, capability levels |

## Repository Structure

```
chapter06/
│
├── README.md                              # This file
├── AGENTS.md                              # Agentic AI metadata
├── LICENSE                                # MIT License
├── requirements.txt                       # Pinned Python dependencies
├── .env.template                          # API key template (zero-hardcode policy)
├── .gitignore                             # Standard Python + .env exclusions
├── troubleshooting.md                     # Dependency conflict resolution guide
│
├── chapter_06_knowledge_agents.ipynb      # Primary deliverable
├── agent_utils.py                         # ColorLogger, MockLLM, decorators
│
├── docs/                                  # Synthetic corpus for RAG demo
│   ├── knowledge_base_rag.txt
│   └── compliance_policy.txt
│
└── samples/                               # Inputs for Document Intelligence
    └── sample_invoice.png
```

## Simulation Mode

When no API key is detected, the notebook activates **Simulation Mode**:

- `MockLLM` and `MockEmbeddings` replace the OpenAI client transparently
- Keyword-routed responses return section-appropriate mock data
- Every external call is wrapped in `@fail_gracefully` with automatic mock fallback
- Every cell executes successfully with no external dependencies

API key detection follows a three-tier cascade: `.env` file → environment variable → interactive prompt → Simulation Mode.

## Resilience Architecture

All agent operations are wrapped in the `@fail_gracefully` decorator:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt`
- **API Key:** Optional (Simulation Mode works without one)

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for solutions to common issues including FAISS installation, Tesseract setup, sentence-transformers model downloads, and LangChain import errors.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
