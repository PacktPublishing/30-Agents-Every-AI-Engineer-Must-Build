# Chapter 14 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of three LLM providers running the Chapter 14 Financial and Legal Intelligence tasks: financial advisory agent with compliance gates and legal intelligence agent with citation verification.

---

## Agent Tasks in This Chapter

- **Financial Advisory Agent** -- Multi-agent supervisor architecture (Market Data Agent, Financial Analysis Agent, News Agent) with compliance validation gates
- **Legal Intelligence Agent** -- RAG-powered legal research with precedent finding, citation verification, and contract analysis

## Scoring Dimensions

Each provider is rated 0--10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of financial calculations and legal interpretations |
| **Completeness** | Coverage of all risk factors, regulatory requirements, and legal dimensions |
| **Structure & Organization** | Quality of financial reports and legal analyses |
| **Conciseness** | Appropriate depth for professional financial/legal communication |
| **Source Grounding** | Adherence to the chapter's financial and legal frameworks |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Handling of market uncertainty, legal qualifications, and disclaimers |
| **Practical Utility** | How useful outputs would be for financial advisors or legal professionals |

### Bloom's Taxonomy Reference

| Level | Verb | What It Looks Like in LLM Output |
|---|---|---|
| 1. Remember | List, define | Repeats facts from context verbatim |
| 2. Understand | Explain, summarize | Paraphrases in own words with coherent structure |
| 3. Apply | Demonstrate, use | Maps retrieved knowledge to the specific question asked |
| 4. Analyze | Compare, differentiate | Breaks down into categories, identifies relationships |
| 5. Evaluate | Assess, judge | States what works, what doesn't, and why |
| 6. Create | Synthesize, design | Produces novel structure, recommendations, or frameworks |

---

## Key Observation: All Providers Run in Simulation Mode with Identical Outputs

Chapter 14 uses **MockChatOpenAI** across all provider notebooks:

- **OpenAI GPT-4o**: "[Simulation Mode] MockChatOpenAI initialized (model=gpt-4o-mini-2024-07-18)" -- 15 output cells
- **Claude Sonnet 4**: 0 output cells (notebook not executed)
- **Gemini Flash 2.5**: "[Simulation Mode] MockChatOpenAI initialized (model=gemini-2.5-flash)" -- 14 output cells
- **DeepSeek V2 16B**: "[Simulation Mode] MockChatOpenAI initialized (model=deepseek-v2:16b)" -- 14 output cells

All external data sources (Finnhub, Tavily) also report SIMULATED status. The LangGraph supervisor routes through Market_Data_Agent, Financial_Analysis_Agent, and News_Agent using deterministic mock responses.

**Evidence of identical outputs across all three active providers:**
- Market data: "Price: $178.72, Market Cap: $2800000000000, P/E Ratio: 28.5"
- Portfolio analysis: "P/E Ratio: 28.5, Revenue Growth: 7.8%, 52W High: $199.62, 52W Low: $143.90"
- Risk assessment: "Composite risk score 4.85 (MODERATE). Annualized volatility: 0.2340, Max drawdown: -0.0812"
- Advisory recommendation: "Allocation: us_equities 0.25, international_equities 0.25, fixed_income 0.25, alternatives 0.2. Risk Score: 6.2. Compliance: VALIDATED"
- Legal precedents: "Smith v. TechCorp International [0.510], Johnson v. DataFlow Systems [0.376], Anderson v. CloudFirst Inc. [0.207]"

**Because all active providers produce identical simulation outputs, meaningful per-provider comparison is not possible.** Claude Sonnet 4 has no saved outputs (0 output cells).

---

## Provider Availability

| Provider | Output Cells | Mode | Status |
|---|---|---|---|
| OpenAI GPT-4o | 15 | Simulation | Identical outputs |
| Claude Sonnet 4 | 0 | Not executed | Excluded from scoring |
| Gemini Flash 2.5 | 14 | Simulation | Identical outputs |
| DeepSeek V2 16B | 14 | Simulation | Identical outputs |

---

## Shared Simulation Output Quality

The simulation outputs demonstrate:

- **Financial Pipeline:** Supervisor correctly routes "Analyze the portfolio for AAPL" through Market_Data_Agent -> Financial_Analysis_Agent -> News_Agent -> FINISH
- **Compliance Gate:** Structural compliance validation passes with no issues; concentration limits (25% max) enforced
- **Risk Assessment:** Multi-factor scoring using annualized volatility (0.234), max drawdown (-0.0812), and VaR
- **Legal Precedent Finding:** 3-stage pipeline (Issue Extraction -> Multi-Dimensional Retrieval -> Synthesis) produces ranked precedents with citation verification against good law status
- **Contract Analysis:** 5-stage pipeline (Ingestion -> Clause Extraction -> Risk Flagging -> Compliance Validation -> Summary)

### Unified Score (All Active Providers)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct financial metrics (Sharpe, VaR, drawdown); valid legal citations with proper case names |
| Completeness | 8 | Both financial and legal agents demonstrated end-to-end; compliance gate and citation verification included |
| Structure & Organization | 8 | Professional supervisor routing; structured legal precedent ranking with scores |
| Conciseness | 7 | Appropriate detail for regulated domains; StateGraph streaming adds execution trace verbosity |
| Source Grounding | 9 | Explicit page references (SS14.1-14.2); Figure 14.1, 14.2, 14.3 referenced throughout |
| Bloom's Level | **4 -- Analyze** | Pipeline analyzes portfolio across multiple dimensions and decomposes legal matters into discrete issues |
| Nuance & Caveats | 7 | Compliance validation gate enforces regulatory constraints; disclaimer present; risk levels categorized |
| Practical Utility | 7 | Good pipeline architecture demo; would need live LLM for actual advisory/legal output |

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|
| Factual Accuracy | **8.0** | **8.0** | **8.0** |
| Completeness | **8.0** | **8.0** | **8.0** |
| Structure & Organization | **8.0** | **8.0** | **8.0** |
| Conciseness | **7.0** | **7.0** | **7.0** |
| Source Grounding | **9.0** | **9.0** | **9.0** |
| Bloom's Taxonomy Level | **4.0 (Analyze)** | **4.0 (Analyze)** | **4.0 (Analyze)** |
| Nuance & Caveats | **7.0** | **7.0** | **7.0** |
| Practical Utility | **7.0** | **7.0** | **7.0** |
| **WEIGHTED AVERAGE** | **7.3** | **7.3** | **7.3** |

> *Claude Sonnet 4 excluded (0 output cells). All active providers produce identical simulation outputs.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     | oooooooooooo O, G, D (all identical simulation)
Level 3: Apply       |
Level 2: Understand  |
Level 1: Remember    |
```

The simulation pipeline reaches Level 4 (Analyze) through multi-agent decomposition: the supervisor analyzes query intent to route to specialists, the risk framework analyzes multiple risk dimensions, and the legal pipeline analyzes matters into discrete legal questions. It does not reach Level 5 because it does not evaluate trade-offs between investment strategies or weigh competing legal arguments.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  OpenAI GPT-4o          7.3  █████████████████████░░░░░░░░░░
  Gemini Flash 2.5       7.3  █████████████████████░░░░░░░░░░
  DeepSeek V2 (Local)    7.3  █████████████████████░░░░░░░░░░
  Claude Sonnet 4        N/A  (no saved outputs)
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     |
  L4 Analyze      | O G D (all identical)
  L3 Apply        | O G D
  L2 Understand   | O G D
  L1 Remember     | O G D
```

Legend: **O** = OpenAI GPT-4o, **G** = Gemini Flash 2.5, **D** = DeepSeek V2

---

## Winner: Tie (OpenAI / Gemini / DeepSeek)

| | |
|---|---|
| **Chapter 14 Winner** | **Tie -- All Active Providers** |
| **Score** | **7.3 / 10** |
| **Bloom's Level** | **Level 4 -- Analyze** |

**Why this is a tie:**
- All three active provider notebooks use MockChatOpenAI with identical simulation responses
- The LangGraph supervisor, compliance gate, risk scoring, and legal precedent pipeline produce byte-identical outputs
- No live LLM calls are made; all routing decisions use deterministic mock responses
- Claude Sonnet 4 has 0 output cells and is excluded

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality | Any (identical) | Simulation outputs are the same |
| Cost-efficient production | Gemini Flash 2.5 | Lowest per-token cost for equivalent output |
| Air-gapped / private data | DeepSeek V2 (Local) | Only option with zero cloud dependency |
| Rapid prototyping | DeepSeek V2 (Local) | No API key, instant iteration, zero cost |

## Provider Profiles for This Chapter

### OpenAI GPT-4o, Gemini Flash 2.5, DeepSeek V2 -- "The Compliance Pipeline"
**Strengths:** Well-structured multi-agent financial architecture with compliance-by-design; effective legal RAG with citation verification; proper disclaimer handling.
**Weaknesses:** No live LLM differentiation; identical simulation outputs; advisory narrative is formulaic.

### Claude Sonnet 4 -- Not Evaluated
**Status:** 0 output cells saved. Notebook was not executed.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Financial advisory reports** | Any -- then add live LLM | Pipeline architecture is identical; live LLM quality would differentiate |
| **Legal document analysis** | Any -- then add live LLM | Citation verification gate is deterministic |
| **Compliance validation** | Any (deterministic) | Compliance gate logic does not depend on LLM |
| **Portfolio screening** | Gemini Flash 2.5 | Lowest cost for equivalent pipeline output |
| **Pipeline development** | Ollama DeepSeek V2 | Zero cost, identical functionality |

> **Regulatory Note:** All LLM-generated financial and legal content requires human expert review before client distribution. The simulation outputs are educational demonstrations only.

---

*Analysis based on Chapter 14 notebook outputs executed April 2026. Three providers (OpenAI, Gemini, DeepSeek) produce identical simulation-mode outputs. Claude has no saved outputs. Financial calculations, risk scoring, and legal precedent retrieval are entirely deterministic.*
