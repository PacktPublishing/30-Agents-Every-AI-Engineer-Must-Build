# Chapter 14 — Financial and Legal Domain Agents

**Book:** *30 Agents Every AI Engineer Must Build*
**Author:** Imran Ahmad
**Publisher:** Packt Publishing
**Chapter:** 14 — Financial and Legal Domain Agents

---

## Overview

This repository contains the complete, runnable code for Chapter 14 of *30 Agents Every AI Engineer Must Build*. It implements two production-grade agent architectures:

**Financial Advisory Agent** — A supervised multi-agent system (Section 14.1) featuring market data analysis, quantitative risk assessment (VaR, CVaR, volatility scoring), personalized financial planning with configurable investor profiles, and compliance-by-architecture validation gates that structurally enforce regulatory requirements.

**Legal Intelligence Agent** — A RAG-powered legal research system (Section 14.2) featuring hybrid retrieval with a custom vector store, authority-weighted case ranking based on court hierarchy, multi-stage contract analysis, and a citation verification pipeline that detects hallucinated case references — directly inspired by the Schwartz v. Avianca incident discussed in the chapter.

Both agents are built on LangChain and LangGraph, using a supervisor pattern for orchestration and StateGraph for workflow management.

---

## Prerequisites

- **Python 3.10+** (tested on 3.10, 3.11, 3.12)
- **pip** (package manager)
- **Jupyter Notebook** or **JupyterLab** (for running the notebook)
- (Optional) API keys for Live Mode — see the Live Mode section below

---

## Quick Start

Three commands to get running:

```bash
# 1. Clone and enter the repository
git clone https://github.com/your-username/chapter14-financial-legal-agents.git
cd chapter14-financial-legal-agents

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the notebook
jupyter notebook chapter14_financial_legal_agents.ipynb
```

When the notebook starts, press Enter at each API key prompt to run in **Simulation Mode** — no API keys required. Every cell will execute successfully with chapter-faithful mock data.

---

## Project Structure

```
chapter14-financial-legal-agents/
│
├── README.md                                    ← You are here
├── AGENTS.md                                    ← Agentic metadata & AI persona
├── LICENSE                                      ← MIT License
├── requirements.txt                             ← Pinned dependencies
├── .env.template                                ← API key placeholders (zero secrets)
├── .gitignore                                   ← .env, __pycache__, checkpoints
│
├── chapter14_financial_legal_agents.ipynb        ← PRIMARY: Full chapter walkthrough
│
├── mock_llm.py                                  ← Mocking & resilience layer
│   ├── ColorLogger                              ← Color-coded logging (Blue/Green/Red/Yellow)
│   ├── ServiceConfig                            ← Per-service API key detection
│   ├── @graceful_fallback                       ← Defensive execution decorator
│   ├── MockChatOpenAI                           ← LangGraph-compatible mock LLM
│   ├── MockStructuredChain                      ← Deterministic supervisor routing
│   ├── MockEmbeddingModel                       ← Hash-based pseudo-embeddings
│   └── MockVectorStore                          ← In-memory vector store with cosine similarity
│
├── mock_data.py                                 ← Synthetic data derived from chapter
│   ├── MOCK_STOCK_DATA                          ← AAPL, MSFT, GOOGL (yfinance schema)
│   ├── MOCK_FINNHUB_QUOTES                      ← Quote data with risk classification
│   ├── MOCK_FINNHUB_FINANCIALS                  ← Company financials for portfolio analysis
│   ├── generate_mock_price_history()            ← 90-day deterministic price series
│   ├── MOCK_TAVILY_NEWS                         ← 5 news results (Tavily format)
│   ├── MOCK_CLIENT_PROFILES                     ← 2 investor profiles (moderate + conservative)
│   ├── MOCK_LEGAL_CASES                         ← 6 cases (5 verified + 1 fabricated)
│   ├── MOCK_CONTRACT                            ← 8-clause contract for analysis
│   └── MOCK_INTER_AGENT_MESSAGE                 ← Inter-agent JSON protocol (45/20/25/10)
│
└── troubleshooting.md                           ← Dependency conflict resolutions (T1-T10)
```

---

## Simulation Mode (Default — No API Keys Required)

The repository is designed to run completely without any API keys. When keys are absent, the system automatically switches to high-fidelity mock responses derived directly from Chapter 14 content.

**How it works:**

At notebook startup, `ServiceConfig` checks each API key:

```
══════════════════════════════════════════════════════════
  CHAPTER 14 — SERVICE STATUS DASHBOARD
  Book: 30 Agents Every AI Engineer Must Build
  Author: Imran Ahmad
══════════════════════════════════════════════════════════
  OpenAI (LLM)                 ○ SIMULATED
  Finnhub (Financial Data)     ○ SIMULATED
  Tavily (News Search)         ○ SIMULATED
══════════════════════════════════════════════════════════
```

**Per-service detection** means you can mix live and simulated services. For example, if you have an OpenAI key but not a Finnhub key, you get real LLM reasoning over mock financial data.

**Defensive execution** ensures the notebook never crashes: every tool call is wrapped in `@graceful_fallback`, which catches exceptions, logs them in color-coded RED, and returns structured fallback data.

---

## Live Mode (With API Keys)

To run with real API services:

```bash
# 1. Copy the template
cp .env.template .env

# 2. Edit .env and add your keys
OPENAI_API_KEY=sk-...
FINNHUB_API_KEY=...
TAVILY_API_KEY=tvly-...
```

**Required API keys:**

| Service | Purpose | Where to Get |
|---------|---------|--------------|
| OpenAI | LLM reasoning (GPT-4o-mini) | https://platform.openai.com/api-keys |
| Finnhub | Real-time financial data | https://finnhub.io/ (free tier available) |
| Tavily | AI-optimized news search | https://tavily.com/ (free tier available) |

All keys are loaded via `python-dotenv` with a `getpass` fallback for interactive environments. No keys are ever hardcoded in any file.

---

## What You Will Build

### Financial Advisory Agent (Section 14.1)

- **Supervisor Architecture** (Fig 14.1) — Central orchestrator routes queries to specialized agents
- **Market Data Agent** — Fetches real-time stock data via yfinance or Finnhub
- **Risk Assessment** — Computes VaR (Value at Risk), CVaR, volatility scoring, and maximum drawdown
- **Personalized Planning** — Generates investment plans matched to client risk tolerance
- **Compliance Gate** — Structural validation that blocks non-compliant plans (inspired by the Knight Capital incident)
- **RetailAdvisor Case Study** — End-to-end demo with a $50K moderate-growth investor profile

### Legal Intelligence Agent (Section 14.2)

- **Legal Knowledge Base** — Hybrid retrieval combining keyword and semantic search
- **Precedent Finding** (Fig 14.2) — 3-stage pipeline with authority-weighted ranking by court hierarchy
- **Contract Analysis** (Fig 14.3) — 5-stage pipeline analyzing 8 contract clauses for risk and compliance
- **Citation Verification** — Detects hallucinated case references (inspired by Schwartz v. Avianca)
- **LegalBrief Case Study** — Full research workflow with verified vs. unverified citation output

---

## Color-Coded Logging

The notebook uses visual logging throughout for clear execution tracing:

- 🔵 **BLUE** — Informational messages (agent starts, data loading)
- 🟢 **GREEN** — Success messages (tool completion, validation pass)
- 🔴 **RED** — Handled errors (caught by `@graceful_fallback`)
- 🟡 **YELLOW** — Warnings (fallback activated, simulated mode)

---

## Dependencies

All versions are pinned to the exact versions specified in the chapter's Technical Requirements:

| Package | Version | Purpose |
|---------|---------|---------|
| langchain | 0.2.16 | Core LLM framework |
| langchain-openai | 0.1.23 | OpenAI integration |
| langchain-community | 0.2.16 | Community tools |
| langgraph | 0.2.28 | Agent workflow graphs |
| openai | 1.40.0 | OpenAI API client |
| yfinance | 0.2.41 | Yahoo Finance data |
| finnhub-python | 2.4.19 | Finnhub financial data |
| tavily-python | 0.3.3 | Tavily news search |
| numpy | 1.26.4 | Numerical computing |
| pydantic | 2.8.2 | Data validation |
| python-dotenv | 1.0.1 | Environment management |

For dependency conflicts, see [troubleshooting.md](troubleshooting.md).

---

## Troubleshooting

If you encounter issues, check [troubleshooting.md](troubleshooting.md) which covers the 10 most common problems including LangChain version conflicts (T1), Pydantic V1/V2 issues (T2), yfinance empty data (T3), API rate limits (T4), and more.

---

## About the Book

*30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing) is a hands-on guide to building production-grade AI agents. Chapter 14 covers financial and legal domain agents — two of the most demanding application areas for agentic AI, where reliability, compliance, and auditability are critical requirements.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

*Book: 30 Agents Every AI Engineer Must Build — Imran Ahmad (Packt Publishing)*
*Chapter: 14 — Financial and Legal Domain Agents*
