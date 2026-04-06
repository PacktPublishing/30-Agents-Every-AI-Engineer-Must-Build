# Chapter 14: Financial and Legal Domain Agents

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 14** of *30 Agents Every AI Engineer Must Build*. It implements two production-grade agent architectures for regulated domains: the Financial Advisory Agent (supervised multi-agent system with LangGraph StateGraph coordinating Market Data, Financial Analysis, and News specialist agents — featuring composite risk scoring, client tolerance adjustment, and compliance-by-architecture validation) and the Legal Intelligence Agent (RAG-powered legal research with hybrid retrieval, authority-weighted ranking, a three-stage precedent-finding pipeline, contract analysis with parallel compliance validation, and citation verification to detect hallucinated case law).

Every code cell runs **without an API key** in Simulation Mode, powered by `MockChatOpenAI`, `MockStructuredChain`, and `MockVectorStore` that return chapter-derived responses. When API keys are provided, the notebook seamlessly switches to Live Mode on a per-service basis.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter14

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Add your API keys for Live Mode
cp .env.template .env
# Edit .env and add your keys, or skip this step for Simulation Mode

# 5. Launch the notebook
jupyter notebook chapter14_financial_legal_agents.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | Configuration, per-service API detection, status dashboard |
| **1–2** | §14.1.1 — Supervisor & Market Data | Supervisor architecture, Market Data Agent (yfinance/Finnhub) |
| **3–4** | §14.1.1 — Finnhub & News | Finnhub integration, News Agent (Tavily) |
| **5** | §14.1 — StateGraph Assembly | LangGraph StateGraph assembly and streaming |
| **6** | §14.1.2 — Risk Assessment | VaR, Volatility, Maximum Drawdown composite scoring |
| **7** | §14.1.3 — Personalized Planning | Client tolerance adjustment, compliance gate |
| **8** | §14.1.4 — RetailAdvisor Case Study | End-to-end financial advisory demonstration |
| **9** | §14.2.1 — Legal Knowledge Base | Hybrid retrieval with authority-weighted ranking |
| **10** | §14.2.2 — Precedent Finding | Three-stage pipeline: Issue Extraction → Retrieval → Synthesis |
| **11** | §14.2.3 — Contract Analysis | Five-stage pipeline with parallel compliance validation |
| **12** | §14.2.4 — LegalBrief Case Study | Citation verification gate (hallucination detection) |
| **13** | Summary | Extensions and pointers to Chapter 15 |

## Real-World Use Cases

This chapter's agents operate in two of the most regulated industries — where a wrong recommendation triggers lawsuits and a hallucinated citation triggers court sanctions.

**Meridian Wealth Partners** — An RIA firm managing $2.8B can't scale to 6,000 clients because compliance review is the bottleneck (180 recommendations/week, 23% rejection rate). The case study shows how compliance-by-architecture — embedding suitability and concentration gates as structural LangGraph nodes — makes regulatory violations structurally impossible, not just unlikely.

**Cartwright Legal Group** — A 45-attorney firm spends $1.6M–$2.1M/year on legal research, and a junior associate nearly submits a memo with a non-existent citation. The case study shows how authority-weighted hybrid retrieval and the citation verification gate eliminate hallucination risk while cutting research time by 75%.

Read the full case study: **[USECASE.md](USECASE.md)** — includes the RetailAdvisor and LegalBrief walkthroughs, compliance formulas, and revenue impact.

## Repository Structure

```
chapter14/
│
├── README.md                                 # This file
├── AGENTS.md                                 # Agentic AI metadata
├── LICENSE                                   # MIT License
├── requirements.txt                          # Pinned Python dependencies
├── .env.template                             # API key template (zero-hardcode policy)
├── .gitignore                                # Standard Python + .env exclusions
├── troubleshooting.md                        # Dependency conflict resolution guide
│
├── chapter14_financial_legal_agents.ipynb     # Primary deliverable
│
├── mock_llm.py                               # ColorLogger, ServiceConfig, @graceful_fallback,
│                                             #   MockChatOpenAI, MockStructuredChain, MockEmbeddingModel,
│                                             #   MockVectorStore
└── mock_data.py                              # MOCK_STOCK_DATA, MOCK_FINNHUB_*, MOCK_TAVILY_NEWS,
                                              #   MOCK_CLIENT_PROFILES, MOCK_LEGAL_CASES, MOCK_CONTRACT
```

## Simulation Mode

When API keys are absent, the system automatically switches to **Simulation Mode** on a per-service basis. A color-coded dashboard at startup shows each service's status:

- **OpenAI (LLM):** `MockChatOpenAI` with keyword-based mock responses
- **Finnhub (Financial Data):** Deterministic mock stock data, quotes, and financials
- **Tavily (News Search):** Pre-authored financial news results

A user with an OpenAI key but no Finnhub key gets real LLM reasoning over mock financial data. The `@graceful_fallback` decorator wraps every external call, ensuring the notebook never crashes.

## Pre-Executed Example Runs

Two pre-executed notebooks are included so you can review the full output without running any code or installing dependencies:

| Notebook | Mode | Description |
|---|---|---|
| [EXAMPLE_RUN_SIMULATION_MODE_chapter14_financial_legal_agents.ipynb](EXAMPLE_RUN_SIMULATION_MODE_chapter14_financial_legal_agents.ipynb) | Simulation | Executed without an API key — MockLLM responses |
| [EXAMPLE_RUN_LLM_MODE_chapter14_financial_legal_agents.ipynb](EXAMPLE_RUN_LLM_MODE_chapter14_financial_legal_agents.ipynb) | Live LLM | Executed with an OpenAI API key — real GPT responses |

Compare both to see how Simulation Mode mirrors Live LLM behavior.

## Resilience Architecture

All agent operations are wrapped in the `@graceful_fallback` decorator:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt`
- **API Keys:** Optional (Simulation Mode works without any)

Optional API services for Live Mode: OpenAI (gpt-4o-mini), Finnhub (free tier at finnhub.io), Tavily (free tier at tavily.com).

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for solutions to 10 common issues including version conflicts, API rate limits, and platform-specific display problems.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
