# Chapter 14: Financial and Legal Domain Agents

**Book:** *30 Agents Every AI Engineer Must Build*
**Author:** Imran Ahmad
**Publisher:** Packt Publishing
**Chapter:** 14 — Financial and Legal Domain Agents

---

## Overview

This repository contains the companion code for Chapter 14 of *30 Agents Every AI
Engineer Must Build*. It implements two production-grade agent architectures for
regulated domains:

**Financial Advisory Agent** — A supervised multi-agent system (Figure 14.1) that
coordinates specialist agents through a LangGraph StateGraph. The Supervisor Agent
routes queries to a Market Data Agent (yfinance/Finnhub), a Financial Analysis Agent,
and a News Agent (Tavily). The architecture includes composite risk scoring (VaR,
volatility, maximum drawdown), client tolerance adjustment, and a compliance-by-architecture
validation gate that makes it structurally impossible for non-compliant recommendations
to reach the client.

**Legal Intelligence Agent** — A RAG-powered legal research system (Figures 14.2–14.3)
with hybrid retrieval combining dense vector search and sparse keyword matching. It
implements authority-weighted ranking (0.5 × similarity + 0.3 × authority + 0.2 × recency),
a three-stage precedent-finding pipeline (Issue Extraction → Multi-Dimensional Retrieval →
Synthesis and Verification), contract analysis with parallel compliance validation, and a
citation verification gate that detects hallucinated case law.

Both agents are designed as educational demonstrations. Financial outputs are illustrative
and must not be treated as investment advice. Legal outputs are illustrative and must not
be treated as legal opinions.

---

## Prerequisites

- Python 3.10 or later
- pip (Python package manager)
- Jupyter Notebook or JupyterLab

### Optional API Keys (for Live Mode)

| Service | Purpose | Free Tier |
|:--------|:--------|:----------|
| OpenAI | LLM reasoning (gpt-4o-mini) | Requires paid API access |
| Finnhub | Real-time financial data | Free at [finnhub.io](https://finnhub.io) |
| Tavily | News search and retrieval | Free at [tavily.com](https://tavily.com) |

API keys are **not required**. Without them, the notebook runs in Simulation Mode
with high-fidelity mock data derived from the chapter.

---

## Quick Start

```bash
# 1. Clone and navigate to the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd 30-Agents-Every-AI-Engineer-Must-Build/chapter14

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the notebook
jupyter notebook chapter14_financial_legal_agents.ipynb
```

The notebook will detect missing API keys and automatically activate Simulation Mode.
No additional configuration is needed.

### Optional: Enable Live Mode

```bash
cp .env.template .env
# Edit .env and add your API keys
```

---

## Project Structure

```
chapter14-financial-legal-agents/
│
├── README.md                                 ← You are here
├── AGENTS.md                                 ← Agentic metadata and AI persona
├── LICENSE                                   ← MIT License
├── requirements.txt                          ← Pinned dependencies (Python 3.10+)
├── .env.template                             ← API key placeholders (zero secrets)
├── .gitignore                                ← .env, __pycache__, .ipynb_checkpoints
│
├── chapter14_financial_legal_agents.ipynb     ← Primary notebook (full chapter walkthrough)
│
├── mock_llm.py                               ← Mocking and resilience layer
│   ├── ColorLogger                           ← Color-coded visual logging
│   ├── ServiceConfig                         ← Per-service API detection + dashboard
│   ├── @graceful_fallback                    ← Resilience decorator with backoff
│   ├── MockChatOpenAI                        ← Keyword-based mock LLM
│   ├── MockStructuredChain                   ← Deterministic supervisor routing
│   ├── MockEmbeddingModel                    ← Hash-based pseudo-embeddings
│   └── MockVectorStore                       ← In-memory vector store with cosine similarity
│
├── mock_data.py                              ← Synthetic data derived from chapter
│   ├── MOCK_STOCK_DATA                       ← yfinance .info schema (AAPL, MSFT, GOOGL)
│   ├── MOCK_FINNHUB_QUOTES                   ← Finnhub quote data with risk tiers
│   ├── MOCK_FINNHUB_FINANCIALS               ← Company financial metrics
│   ├── generate_mock_price_history()         ← Deterministic price series for VaR
│   ├── MOCK_TAVILY_NEWS                      ← 5 financial news results
│   ├── MOCK_CLIENT_PROFILES                  ← Moderate and conservative investors
│   ├── MOCK_LEGAL_CASES                      ← 6 cases (including 1 fabricated)
│   ├── MOCK_CONTRACT                         ← 8-clause MSA with risk areas
│   └── MOCK_INTER_AGENT_MESSAGE              ← Inter-agent JSON protocol (p.407)
│
└── troubleshooting.md                        ← Solutions for 10 common issues
```

---

## Simulation Mode

When API keys are absent, the system automatically switches to Simulation Mode on a
per-service basis. This means a user with an OpenAI key but no Finnhub key gets real
LLM reasoning over mock financial data.

At notebook startup, a color-coded dashboard shows the status of each service:

```
══════════════════════════════════════════════════════════
  CHAPTER 14 — SERVICE STATUS DASHBOARD
  Book: 30 Agents Every AI Engineer Must Build
  Author: Imran Ahmad
══════════════════════════════════════════════════════════
  OpenAI (LLM)                    ○ SIMULATED
  Finnhub (Financial Data)        ○ SIMULATED
  Tavily (News Search)            ○ SIMULATED
══════════════════════════════════════════════════════════
```

All mock data is derived directly from Chapter 14's code examples and narrative. The
`@graceful_fallback` decorator wraps every external call, ensuring the notebook never
crashes — errors are logged in RED and execution continues with fallback values.

---

## Live Mode

To use real API services, copy the template and add your keys:

```bash
cp .env.template .env
```

Edit `.env`:

```
OPENAI_API_KEY=sk-your-key-here
FINNHUB_API_KEY=your-finnhub-key
TAVILY_API_KEY=tvly-your-key-here
```

The dashboard will show `● LIVE` for each configured service. You can mix live and
simulated services — each is detected independently.

---

## Notebook Sections

| Cells | Section | Chapter Reference |
|:------|:--------|:------------------|
| 0 | Setup and Configuration | Technical Requirements (p.392) |
| 1–2 | Supervisor Architecture and Market Data Agent | Section 14.1.1, Figure 14.1, p.393–395 |
| 3–4 | Finnhub Integration and News Agent | Section 14.1.1, p.396–397 |
| 5 | StateGraph Assembly and Streaming | Section 14.1, pp. 397–399 |
| 6 | Risk Assessment (VaR, Volatility, Drawdown) | Section 14.1.2, p.399–404 |
| 7 | Personalized Planning and Compliance Gate | Section 14.1.3, p.403–408 |
| 8 | RetailAdvisor Case Study | Section 14.1.4, p.406–410 |
| 9 | Legal Knowledge Base (Hybrid Retrieval) | Section 14.2.1, p.408–410 |
| 10 | Precedent Finding (3-Stage Pipeline) | Section 14.2.2, Figure 14.2, p.410–414 |
| 11 | Contract Analysis (5-Stage Pipeline) | Section 14.2.3, Figure 14.3, p.414–416 |
| 12 | LegalBrief Case Study (Citation Verification) | Section 14.2.4, p.416–419 |
| 13 | Summary and Extensions | Summary, p.419–420 |

---

## Key Concepts

### Risk Scoring (Section 14.1.2)

The `RiskScorer` computes a composite score on a 0–10 scale:
- **Annualized Volatility** (weight: 0.40) — `returns.std() × √252`, scaled by `/0.05`
- **Maximum Drawdown** (weight: 0.35) — largest peak-to-trough decline, scaled by `/0.05`
- **Value at Risk, 95%** (weight: 0.25) — 5th percentile of returns, scaled by `/0.03`

Risk categories: **HIGH** (≥ 7.0), **MODERATE** (≥ 4.0), **LOW** (< 4.0)

### Authority-Weighted Ranking (Section 14.2.1)

Legal search results are re-ranked by:
- `final_score = 0.5 × similarity + 0.3 × authority_boost + 0.2 × recency_boost`

A Supreme Court decision (authority 10) outranks a district court ruling (authority 3)
when semantic similarity is comparable.

---

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for solutions to 10 common issues including
version conflicts, API rate limits, and platform-specific display problems.

---

## References

- **Book:** *30 Agents Every AI Engineer Must Build* — Imran Ahmad (Packt Publishing, 2026)
- **Chapter:** 14 — Financial and Legal Domain Agents
- **GitHub:** [PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build](https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build)

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

*Author: Imran Ahmad*
