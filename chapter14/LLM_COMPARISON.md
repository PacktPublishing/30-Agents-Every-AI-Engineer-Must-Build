# Chapter 14 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 14 Financial and Legal Intelligence tasks: financial advisory agent with compliance gates and legal intelligence agent with citation verification.

---

## Agent Tasks in This Chapter

- **Financial Advisory Agent** -- Multi-agent supervisor architecture (Market Data Agent, Financial Analysis Agent, News Agent) with LangGraph StateGraph routing, compliance validation gates, and risk assessment framework
- **Legal Intelligence Agent** -- RAG-powered legal research with precedent finding (3-stage pipeline), citation verification against good law status, and contract analysis (5-stage pipeline)

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

## Provider Execution Status

| Provider | Output Cells | LLM Mode | Key Observation |
|---|---|---|---|
| OpenAI GPT-4o | 13 | MockChatOpenAI (fallback) | ChatOpenAI init failed: `No module named 'langchain_core.pydantic_v1'`. Fell back to MockChatOpenAI. |
| Claude Sonnet 4 | 0 | Not executed | Notebook has no saved outputs. Excluded from scoring. |
| Gemini Flash 2.5 | 13 | **Live Gemini** (gemini-2.5-flash) | "Using LIVE Gemini LLM (gemini-2.5-flash)" -- only provider with actual LLM calls. |
| DeepSeek V2 16B | 13 | MockChatOpenAI (simulation) | "Using SIMULATED LLM (MockChatOpenAI)" -- explicit simulation mode. |

### Critical Finding: Only Gemini Ran Live

OpenAI's notebook encountered a `langchain_core.pydantic_v1` import error and silently fell back to MockChatOpenAI. DeepSeek ran in explicit simulation mode. Gemini was the only provider that successfully initialized a live LLM client and used it for agent routing decisions.

---

## Provider-Specific Results

### OpenAI GPT-4o (MockChatOpenAI Fallback)

The OpenAI notebook fell back to `MockChatOpenAI(model=gpt-4o-mini-2024-07-18)` due to a langchain compatibility error. Despite this, the StateGraph routing worked correctly using mock supervisor decisions:

- **Routing:** Market_Data_Agent -> Financial_Analysis_Agent -> News_Agent -> FINISH (correct 4-step sequence)
- **Market data:** "Price: $178.72, Market Cap: $2800000000000, P/E Ratio: 28.5" (simulated, Yahoo Finance returned 429 Too Many Requests)
- **Portfolio analysis:** "P/E Ratio: 28.5, Revenue Growth: 7.8%, 52W High: $199.62, 52W Low: $143.90"
- **Risk assessment:** "Composite risk score 4.85 (MODERATE). Annualized volatility: 0.2340, Max drawdown: -0.0812"
- **Compliance gate:** CONCENTRATION violation detected (us_equities at 45% exceeds 25%), revised allocation validated
- **Legal citation:** 3/4 verified (75% quality); 1 unverified: "No. 22-cv-1234 (S.D.N.Y. 2023)"
- **Contract analysis:** 3 risk items (HIGH: one-sided indemnification, low liability cap; CRITICAL: missing GDPR DPA and SCCs)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct financial metrics (Sharpe, VaR, drawdown); valid legal citations. Mock responses are pre-authored and curated. |
| Completeness | 8 | Full 4-agent routing; compliance gate with violation detection and revision; legal precedent + contract analysis. |
| Structure & Organization | 8 | Clean supervisor routing trace; structured risk scoring; professional legal research memo format. |
| Conciseness | 7 | StateGraph streaming trace adds verbosity; Yahoo Finance 429 errors clutter output. |
| Source Grounding | 9 | Page references throughout (pp. 407, SS14.1--14.2); inter-agent communication protocol shown. |
| Bloom's Level | **4 -- Analyze** | Pipeline decomposes portfolio across multiple risk dimensions; legal pipeline extracts discrete issues. |
| Nuance & Caveats | 7 | Compliance gate enforces concentration limits; citation verification flags unverified sources; risk categories per tolerance. |
| Practical Utility | 7 | Correct architecture demonstration; mock responses limit actual advisory value. |

---

### Gemini Flash 2.5 (Live API)

Gemini was the only provider with a live LLM client. Its StateGraph routing behavior differed from the mock baseline:

- **Routing:** Gemini did not log explicit "[Supervisor] Routing to:" messages. Instead, it routed directly to Financial_Analysis_Agent (skipping Market_Data_Agent), then looped on Financial_Analysis_Agent 4 times before completing. This suggests the live Gemini supervisor made different routing decisions than the mock supervisor.
- **Financial analysis output:** "The portfolio analysis for AAPL shows a P/E Ratio of 28.5, Revenue Growth of 7.8, 52W High of 199.62, and 52W Low of 143" -- natural-language sentence generated by the live LLM (vs. mock's structured format)
- **All downstream outputs (risk, compliance, legal):** Identical to mock providers since these use deterministic pipeline logic, not LLM calls
- **Execution time:** StateGraph took ~8 seconds (20:50:43 to 20:50:51) vs. ~1 second for mock providers

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | Live LLM output is factually correct but the routing anomaly (skipping Market_Data_Agent, 4x loop on Financial_Analysis) suggests incomplete integration. |
| Completeness | 6 | Market_Data_Agent was skipped in the live routing; Financial_Analysis_Agent output repeated 4 times instead of routing through all 3 agents sequentially. |
| Structure & Organization | 7 | Natural-language financial analysis is readable but the routing loop is disorganized compared to the clean 4-step mock sequence. |
| Conciseness | 7 | Downstream outputs identical to mock; the 4x repeated Financial_Analysis message is redundant. |
| Source Grounding | 9 | Same chapter references as other providers; deterministic pipeline components identical. |
| Bloom's Level | **4 -- Analyze** | Same analysis depth on deterministic components; live routing attempted to analyze query intent. |
| Nuance & Caveats | 7 | Same compliance gate and citation verification behavior; live LLM did not add additional caveats. |
| Practical Utility | 7 | Demonstrates real LLM behavior including routing challenges; shows what live deployment looks like. |

---

### DeepSeek V2 16B (Simulation Mode)

DeepSeek ran in explicit simulation mode with MockChatOpenAI:

- **Routing:** Identical to OpenAI mock: Market_Data_Agent -> Financial_Analysis_Agent -> News_Agent -> FINISH
- **All outputs:** Identical to OpenAI mock (both use the same MockChatOpenAI response set)
- **No Yahoo Finance errors** (used simulated market data directly)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Identical to OpenAI mock -- same pre-authored responses. |
| Completeness | 8 | Identical pipeline coverage. |
| Structure & Organization | 8 | Cleaner execution trace (no Yahoo Finance 429 errors). |
| Conciseness | 8 | Cleaner than OpenAI (no yfinance deprecation warnings or 429 errors). |
| Source Grounding | 9 | Identical chapter references. |
| Bloom's Level | **4 -- Analyze** | Identical analysis depth. |
| Nuance & Caveats | 7 | Identical compliance and citation behavior. |
| Practical Utility | 7 | Same architecture demo; zero-cost execution. |

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|---|
| Factual Accuracy | **8.0** | N/A | **7.0** | **8.0** |
| Completeness | **8.0** | N/A | **6.0** | **8.0** |
| Structure & Organization | **8.0** | N/A | **7.0** | **8.0** |
| Conciseness | **7.0** | N/A | **7.0** | **8.0** |
| Source Grounding | **9.0** | N/A | **9.0** | **9.0** |
| Bloom's Taxonomy Level | **4.0 (Analyze)** | N/A | **4.0 (Analyze)** | **4.0 (Analyze)** |
| Nuance & Caveats | **7.0** | N/A | **7.0** | **7.0** |
| Practical Utility | **7.0** | N/A | **7.0** | **7.0** |
| **WEIGHTED AVERAGE** | **7.3** | **N/A** | **6.8** | **7.5** |

> *Claude Sonnet 4 excluded (0 output cells). OpenAI fell back to MockChatOpenAI due to langchain import error. Gemini was the only live provider. DeepSeek ran clean simulation.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     | oooooooooooo O, G, D (all reach Analyze)
Level 3: Apply       |
Level 2: Understand  |
Level 1: Remember    |
```

All three active providers reach Level 4 (Analyze) through multi-agent decomposition: the supervisor analyzes query intent to route to specialists, the risk framework analyzes multiple risk dimensions (volatility, drawdown, VaR), and the legal pipeline decomposes matters into discrete legal questions. None reach Level 5 because no provider evaluates trade-offs between investment strategies or weighs competing legal arguments.

---

## Head-to-Head: Key Differences

| Dimension | OpenAI GPT-4o (Mock) | Gemini Flash 2.5 (Live) | DeepSeek V2 (Mock) |
|---|---|---|---|
| **LLM Mode** | MockChatOpenAI (fallback) | Live Gemini API | MockChatOpenAI (explicit) |
| **StateGraph routing** | Market -> Financial -> News -> FINISH | Financial (x4) -> FINISH | Market -> Financial -> News -> FINISH |
| **Financial output format** | Structured key-value | Natural-language sentence | Structured key-value |
| **Execution time (StateGraph)** | ~1 sec | ~8 sec | ~0.5 sec |
| **Yahoo Finance errors** | 429 Too Many Requests | 429 Too Many Requests | None (fully simulated) |
| **Compliance gate** | Identical | Identical | Identical |
| **Legal pipeline** | Identical | Identical | Identical |

**Gemini's strength:** Only provider demonstrating actual live LLM supervisor routing. The natural-language financial analysis shows how a live deployment would present data to users.

**Gemini's weakness:** The routing anomaly (skipping Market_Data_Agent, 4x loop on Financial_Analysis_Agent) indicates the live Gemini supervisor did not follow the expected 3-agent sequential routing pattern, resulting in incomplete pipeline coverage.

**DeepSeek's strength:** Cleanest execution trace -- no Yahoo Finance errors, no langchain import warnings, zero cost.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  DeepSeek V2 (Local)    7.5  ██████████████████████░░░░░░░░░
  OpenAI GPT-4o          7.3  █████████████████████░░░░░░░░░░
  Gemini Flash 2.5       6.8  ████████████████████░░░░░░░░░░░
  Claude Sonnet 4        N/A  (no saved outputs)
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     |
  L4 Analyze      | O G D
  L3 Apply        | O G D
  L2 Understand   | O G D
  L1 Remember     | O G D
```

Legend: **O** = OpenAI GPT-4o, **G** = Gemini Flash 2.5, **D** = DeepSeek V2

---

## Winner: DeepSeek V2 (Local)

| | |
|---|---|
| **Chapter 14 Winner** | **DeepSeek V2 (Local)** |
| **Score** | **7.5 / 10** |
| **Bloom's Level** | **Level 4 -- Analyze** |

**Why DeepSeek wins:**
- Cleanest execution: no Yahoo Finance 429 errors, no langchain import failures, no deprecation warnings
- Complete and correct 4-agent routing sequence (Market -> Financial -> News -> FINISH)
- Identical pipeline coverage to OpenAI mock but with a cleaner output trace
- Zero cost, zero cloud dependency

**Caveats:**
- DeepSeek's win reflects simulation quality, not actual LLM generation capability
- OpenAI would likely have matched or exceeded DeepSeek if not for the langchain compatibility error
- Gemini was the only provider demonstrating actual live LLM behavior, which is valuable for understanding real deployment characteristics even though it scored lower due to routing issues
- Claude was excluded due to having no saved outputs

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality (live LLM) | Gemini Flash 2.5 | Only provider with actual live LLM routing |
| Clean pipeline demo | DeepSeek V2 (Local) | No external API errors, cleanest trace |
| Cost-efficient production | Gemini Flash 2.5 | Lowest per-token cost among cloud providers |
| Air-gapped / private data | DeepSeek V2 (Local) | Zero cloud dependency |
| Rapid prototyping | DeepSeek V2 (Local) | No API key needed, instant execution |

## Provider Profiles for This Chapter

### OpenAI GPT-4o -- "The Fallback Mock"
**Strengths:** Correct pipeline architecture; complete agent routing; proper compliance gate with concentration violation detection.
**Weaknesses:** Fell back to MockChatOpenAI due to langchain import error; Yahoo Finance 429 errors and deprecation warnings clutter output.

### Claude Sonnet 4 -- Not Evaluated
**Status:** 0 output cells saved. Notebook was not executed.

### Gemini Flash 2.5 -- "The Live Explorer"
**Strengths:** Only provider with actual live LLM calls; natural-language financial analysis demonstrates real deployment output format.
**Weaknesses:** StateGraph routing anomaly -- skipped Market_Data_Agent and looped 4x on Financial_Analysis_Agent instead of clean 3-agent sequence.

### DeepSeek V2 (Local) -- "The Clean Simulator"
**Strengths:** Cleanest execution trace; no external API errors; correct pipeline routing; zero cost.
**Weaknesses:** Pure simulation -- does not reveal actual local LLM behavior.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Financial advisory reports** | Gemini Flash 2.5 (live) | Only provider demonstrating live LLM output |
| **Legal document analysis** | Any (deterministic) | Citation verification and contract analysis are code-identical |
| **Compliance validation** | Any (deterministic) | Compliance gate logic does not depend on LLM |
| **Pipeline development** | DeepSeek V2 (Local) | Zero cost, cleanest output trace |
| **Integration testing** | OpenAI GPT-4o | Exposed a real langchain compatibility issue worth fixing |

> **Regulatory Note:** All LLM-generated financial and legal content requires human expert review before client distribution. The simulation outputs are educational demonstrations only.

---

*Analysis based on Chapter 14 notebook outputs executed April 2026. OpenAI fell back to mock due to langchain error. Gemini was the only live provider but exhibited routing anomalies. DeepSeek produced the cleanest simulation output. Claude had no saved outputs.*
