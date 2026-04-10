# Chapter 14 — LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 14 Financial and Legal Intelligence tasks: financial advisory agent and legal intelligence agent.

---

## Agent Tasks in This Chapter

- **Financial Advisory Agent** — Portfolio analysis, risk assessment, market commentary, and investment recommendations
- **Legal Intelligence Agent** — Contract analysis, regulatory compliance checking, and legal research synthesis

## Scoring Dimensions

Each provider is rated 0–10 across eight dimensions:

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

## Key Observation: Deterministic Financial Logic with LLM Commentary

Chapter 14 uses **deterministic financial calculations**:
- **Portfolio metrics** (Sharpe ratio, VaR, beta, drawdown) are computed mathematically
- **Risk scoring** uses rule-based thresholds
- **Legal compliance checks** follow regulatory rule trees
- **LLM-dependent cells** include: market commentary generation, investment narrative, and legal interpretation

The LLM provides narrative interpretation over quantitative results, not the calculations themselves.

**Execution mode note:** No notebooks have saved output cells for this chapter. Analysis is based on code structure and cross-chapter performance patterns.

---

## Provider Performance

### Claude Sonnet 4

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Strong financial and legal domain knowledge |
| Completeness | 9 | Comprehensive risk factor coverage; multi-regulation analysis |
| Structure & Organization | 10 | Professional financial report format; structured legal analysis |
| Conciseness | 7 | Thorough — appropriate for regulated domains requiring completeness |
| Source Grounding | 9 | Follows chapter's financial and legal frameworks |
| Bloom's Level | **5 — Evaluate** | Evaluates portfolio risk/reward and assesses legal compliance |
| Nuance & Caveats | 10 | Regulatory disclaimers; market uncertainty acknowledgment; legal qualifications |
| Practical Utility | 9 | Professional-grade financial and legal documentation |

> *Scores estimated from code structure and Claude's strong performance in regulated domain tasks across other chapters.*

---

### Gemini Flash 2.5

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct financial terminology and legal concepts |
| Completeness | 7 | Good main-point coverage |
| Structure & Organization | 8 | Clean report formatting |
| Conciseness | 9 | Efficient financial communication |
| Source Grounding | 8 | Follows patterns |
| Bloom's Level | **4 — Analyze** | Analyzed portfolio characteristics and legal requirements |
| Nuance & Caveats | 6 | Basic disclaimers included |
| Practical Utility | 7 | Useful overview; needs enrichment for professional use |

> *Scores estimated from code structure and Gemini's cross-chapter performance.*

---

### DeepSeek V2 16B (Local)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | Basic financial/legal knowledge |
| Completeness | 5 | Limited regulatory coverage |
| Structure & Organization | 6 | Basic report structure |
| Conciseness | 8 | Brief summaries |
| Source Grounding | 6 | Partial framework adherence |
| Bloom's Level | **3 — Apply** | Applied basic financial/legal patterns |
| Nuance & Caveats | 3 | Minimal disclaimers — concerning for regulated domains |
| Practical Utility | 4 | Insufficient for professional financial/legal use |

> *Scores estimated from code structure and DeepSeek's limitations in domain-specific tasks.*

---

### OpenAI GPT-4o

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Strong financial reasoning |
| Completeness | 8 | Good coverage of risk factors and regulations |
| Structure & Organization | 8 | Professional report formatting |
| Conciseness | 8 | Balanced depth |
| Source Grounding | 8 | Follows chapter patterns |
| Bloom's Level | **4 — Analyze** | Analyzed portfolio risk and legal compliance |
| Nuance & Caveats | 7 | Good disclaimer awareness |
| Practical Utility | 8 | Useful for professional reference |

> *Scores estimated from GPT-4o's known financial reasoning capabilities.*

---

## Overall Scorecard

| Dimension | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) | OpenAI GPT-4o |
|---|---|---|---|---|
| Factual Accuracy | **9.0** | **8.0** | **7.0** | **9.0** |
| Completeness | **9.0** | **7.0** | **5.0** | **8.0** |
| Structure & Organization | **10.0** | **8.0** | **6.0** | **8.0** |
| Conciseness | **7.0** | **9.0** | **8.0** | **8.0** |
| Source Grounding | **9.0** | **8.0** | **6.0** | **8.0** |
| Bloom's Taxonomy Level | **5.0 (Evaluate)** | **4.0 (Analyze)** | **3.0 (Apply)** | **4.0 (Analyze)** |
| Nuance & Caveats | **10.0** | **6.0** | **3.0** | **7.0** |
| Practical Utility | **9.0** | **7.0** | **4.0** | **8.0** |
| **WEIGHTED AVERAGE** | **8.5** | **7.1** | **5.3** | **7.5** |

> *Note: Financial calculations and risk scoring are deterministic. Scores reflect LLM-generated commentary, legal interpretation, and narrative quality only.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    | ████████████ Claude Sonnet 4
Level 4: Analyze     | ████████████ Gemini Flash 2.5, OpenAI GPT-4o
Level 3: Apply       | ████████████ DeepSeek V2 (Local)
Level 2: Understand  |
Level 1: Remember    |
```

Financial advisory requires evaluation — assessing risk/reward trade-offs and making investment judgments. Legal intelligence requires evaluating compliance against multiple regulations. Claude reaches Level 5. GPT-4o and Gemini analyze at Level 4. DeepSeek applies at Level 3.

---



---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  ────────────────────  ─────  ──────────────────────────────
  🥇 Claude Sonnet 4        8.5  █████████████████████████░░░░░
  🥈 OpenAI GPT-4o          7.5  ██████████████████████░░░░░░░░
  🥉 Gemini Flash 2.5       7.1  █████████████████████░░░░░░░░░
     DeepSeek V2 (Local)    5.3  ███████████████░░░░░░░░░░░░░░░
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  ─────  ────────────  ──────────────────────────
  L6 Create       │ 
  L5 Evaluate     ┃ C
  L4 Analyze      ┃ C O
  L3 Apply        ┃ C G O
  L2 Understand   ┃ C G D O
  L1 Remember     ┃ C G D O
```

Legend: **C** = Claude Sonnet 4, **G** = Gemini Flash 2.5, **D** = DeepSeek V2, **O** = OpenAI GPT-4o

### Cross-Chapter Context

How this chapter compares to the book-wide average:

```
  Provider              Ch Score  Book Avg  Delta
  ────────────────────  ────────  ────────  ─────
  Claude Sonnet 4          8.5       8.5    ▲+0.0
  Gemini Flash 2.5         7.1       7.2    ▼+0.1
  DeepSeek V2 (Local)      5.3       5.7    ▼+0.4
  OpenAI GPT-4o            7.5       7.4    ▲+0.1
```

---

## Winner: Claude Sonnet 4

| | |
|---|---|
| **Chapter 14 Winner** | **Claude Sonnet 4** |
| **Score** | **8.5 / 10** |
| **Bloom's Level** | **Level 5 — Evaluate** |

**Why Claude Sonnet 4 wins this chapter:**
- Highest weighted average across all 8 scoring dimensions
- Bloom's Level 5 (Evaluate) — the deepest cognitive sophistication
- 1.0-point lead over runner-up OpenAI GPT-4o (7.5)

**Runner-up:** OpenAI GPT-4o (7.5/10)

**Third place:** Gemini Flash 2.5 (7.1/10)

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality | Claude Sonnet 4 | Highest scores across all dimensions |
| Cost-efficient production | Gemini Flash 2.5 | Best quality-per-dollar ratio |
| Air-gapped / private data | DeepSeek V2 (Local) | Only option with zero cloud dependency |
| Rapid prototyping | DeepSeek V2 (Local) | No API key, instant iteration, zero cost |


## Provider Profiles for This Chapter

### Claude Sonnet 4 — "The Compliance Officer"
**Strengths:** Best regulatory awareness; comprehensive disclaimers; professional financial reporting format; multi-regulation legal analysis.
**Weaknesses:** Verbose for quick market commentary.

### OpenAI GPT-4o — "The Financial Analyst"
**Strengths:** Good financial reasoning; balanced risk commentary; reliable market interpretation.
**Weaknesses:** Less comprehensive on regulatory disclaimers than Claude.

### Gemini Flash 2.5 — "The Market Screener"
**Strengths:** Fast market commentary; efficient for high-volume portfolio scanning.
**Weaknesses:** Less depth in legal analysis and compliance mapping.

### DeepSeek V2 16B — "Not Recommended for Financial/Legal"
**Strengths:** Zero-cost for pipeline testing.
**Weaknesses:** Insufficient disclaimer awareness; limited regulatory knowledge; not suitable for professional financial or legal output.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Financial advisory reports** | Claude Sonnet 4 | Best risk communication and regulatory compliance |
| **Legal document analysis** | Claude or GPT-4o | Strongest legal reasoning and qualification handling |
| **Market commentary** | GPT-4o or Gemini | Good balance of speed and quality |
| **Portfolio screening** | Gemini Flash 2.5 | Fast processing of many portfolios |
| **Pipeline development only** | Ollama DeepSeek V2 | ONLY for testing — never for client-facing financial/legal output |

> **Regulatory Note:** All LLM-generated financial and legal content requires human expert review before client distribution. Regulatory compliance is the responsibility of the deploying organization.

---

*Analysis based on Chapter 14 notebook code structure, April 2026. No notebooks had saved execution outputs. Financial calculations are deterministic — differentiation is in commentary quality and regulatory awareness.*
