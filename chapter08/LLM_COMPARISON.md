# Chapter 8 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of three LLM providers running the Chapter 8 Data Analysis and Reasoning tasks: visualization recommendation, statistical interpretation, verification (NLI), fact-checking, and the General Problem Solver (GPS). DeepSeek V2 16B produced 0 output cells and is excluded from scoring.

---

## Agent Tasks in This Chapter

- **Data Analysis Agent** (Section 8.1) -- Cognitive loop with visualization recommendation, OLS regression, anomaly detection, and LLM-powered statistical interpretation
- **Verification & Validation Agent** (Section 8.2) -- NLI-based fact-checking using BART-MNLI for evidence scoring
- **General Problem Solver** (Section 8.3) -- 5-stage meta-reasoning: decompose, find analogies, hypothesize, test, and meta-learn
- **Case Study 1: News Fact-Checking** (Section 8.4) -- Claim extraction from news articles with verification pipeline
- **Case Study 2: Cross-Disciplinary GPS** (Section 8.5) -- Hypothesis generation across research domains

## Scoring Dimensions

Each provider is rated 0-10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of statistical claims, visualization recommendations, and extracted claims |
| **Completeness** | Coverage of all data dimensions, chart types, and reasoning stages |
| **Structure & Organization** | Quality of analytical reports and reasoning chain structure |
| **Conciseness** | Information density without unnecessary padding |
| **Source Grounding** | Adherence to data analysis best practices from the chapter |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Acknowledgment of data limitations, alternative interpretations |
| **Practical Utility** | How useful the analysis would be for a data practitioner |

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

## Critical Finding: All Providers Used MockLLM for LLM-Dependent Tasks

Despite API key initialization:
- **Claude Sonnet 4:** "Anthropic client initialized. Running in LIVE mode." -- but all llm_call() routes through MockLLM because the `llm_call()` function in `mock_llm.py` only has a live path for OpenAI's `client.chat.completions.create` API format. The Anthropic client is incompatible.
- **Gemini Flash 2.5:** "Gemini client initialized. Running in LIVE mode." -- same issue. The Gemini client does not match the OpenAI chat completions interface.
- **OpenAI GPT-4o:** "No API key detected. Running in SIMULATION MODE." -- explicitly in simulation.

**Evidence:** All three providers produce identical output text:
- Statistical interpretation: "Marketing spend explains approximately 62% of the variation in revenue, indicating a strong positive correlation."
- Claim extraction: 2 claims extracted (unemployment rate 5%, budget surplus $12M)
- GPS decomposition, analogies, and hypotheses: all from MockLLM pre-authored responses
- NLI scores: Precomputed values (entailment: 0.92, neutral: 0.05, contradiction: 0.03)

**Result:** No meaningful LLM-quality differentiation is possible for this chapter.

### What Components ARE Deterministic

| Component | Source | Identical Across Providers? |
|---|---|---|
| Visualization recommendation | Rule-based keyword matching | Yes |
| OLS regression | statsmodels computation | Yes |
| Anomaly detection | Z-score calculation | Yes |
| Statistical interpretation | MockLLM (context_key: stats_interpretation) | Yes |
| NLI verification | Precomputed scores (not actual BART-MNLI) | Yes |
| Claim extraction | MockLLM (context_key: claim_extraction) | Yes |
| GPS stages | MockLLM (context_key: gps_decompose, gps_analogies, gps_hypothesis) | Yes |

---

## Provider Performance

### OpenAI GPT-4o

**Execution mode:** SIMULATION MODE (no API key). All outputs from MockLLM.

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | MockLLM responses are correct (pre-authored); statistical computations accurate |
| Completeness | 7 | Standard MockLLM coverage of all chapter sections |
| Structure & Organization | 7 | MockLLM formatting adequate; deterministic output well-structured |
| Conciseness | 8 | MockLLM responses appropriately sized |
| Source Grounding | 8 | Follows chapter patterns precisely |
| Bloom's Level | **3 -- Apply** | MockLLM applies pre-authored analytical patterns |
| Nuance & Caveats | 5 | MockLLM includes basic caveats (e.g., "possibly due to promotional pricing") |
| Practical Utility | 7 | Functional demonstration of the pipeline architecture |

> *Output is from MockLLM, not the actual GPT-4o model.*

---

### Claude Sonnet 4

**Execution mode:** LIVE MODE initialized but all llm_call() routes through MockLLM. Output identical to OpenAI.

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | Identical MockLLM responses |
| Completeness | 7 | Identical coverage |
| Structure & Organization | 7 | Identical formatting |
| Conciseness | 8 | Identical sizing |
| Source Grounding | 8 | Identical pattern adherence |
| Bloom's Level | **3 -- Apply** | MockLLM output, not Claude |
| Nuance & Caveats | 5 | Identical MockLLM caveats |
| Practical Utility | 7 | Identical demonstration quality |

> *Output is from MockLLM, not the actual Claude Sonnet 4 model. The Anthropic client was initialized but llm_call() uses OpenAI's API format.*

---

### Gemini Flash 2.5

**Execution mode:** LIVE MODE initialized but all llm_call() routes through MockLLM. Output identical to others.

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | Identical MockLLM responses |
| Completeness | 7 | Identical coverage |
| Structure & Organization | 7 | Identical formatting |
| Conciseness | 8 | Identical sizing |
| Source Grounding | 8 | Identical pattern adherence |
| Bloom's Level | **3 -- Apply** | MockLLM output, not Gemini |
| Nuance & Caveats | 5 | Identical MockLLM caveats |
| Practical Utility | 7 | Identical demonstration quality |

> *Output is from MockLLM, not the actual Gemini Flash 2.5 model.*

---

### DeepSeek V2 16B (Local)

**Execution mode:** 0 output cells in the notebook. Cannot be scored.

> *DeepSeek notebook has no saved outputs. Excluded from scoring.*

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 |
|---|---|---|---|
| Factual Accuracy | **7.0*** | **7.0*** | **7.0*** |
| Completeness | **7.0*** | **7.0*** | **7.0*** |
| Structure & Organization | **7.0*** | **7.0*** | **7.0*** |
| Conciseness | **8.0*** | **8.0*** | **8.0*** |
| Source Grounding | **8.0*** | **8.0*** | **8.0*** |
| Bloom's Taxonomy Level | **3.0 (Apply)*** | **3.0 (Apply)*** | **3.0 (Apply)*** |
| Nuance & Caveats | **5.0*** | **5.0*** | **5.0*** |
| Practical Utility | **7.0*** | **7.0*** | **7.0*** |
| **WEIGHTED AVERAGE** | **6.6*** | **6.6*** | **6.6*** |

> *\* All scores reflect MockLLM output. Every provider produced identical outputs because llm_call() routes through MockLLM regardless of client initialization. No actual model capabilities were exercised.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     |
Level 3: Apply       | ============ All Providers (MockLLM)
Level 2: Understand  |
Level 1: Remember    |
```

All providers operate at Level 3 (Apply) through MockLLM's pre-authored responses, which apply analytical patterns (statistical interpretation, claim extraction, GPS decomposition) without genuine reasoning.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  OpenAI GPT-4o          6.6*  ===================...........
  Claude Sonnet 4        6.6*  ===================...........
  Gemini Flash 2.5       6.6*  ===================...........
```

> *All identical -- MockLLM output.*

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     |
  L4 Analyze      |
  L3 Apply        | O C G (all MockLLM)
  L2 Understand   | O C G
  L1 Remember     | O C G
```

Legend: **O** = OpenAI GPT-4o, **C** = Claude Sonnet 4, **G** = Gemini Flash 2.5

---

## Winner: Tie (All Providers)

| | |
|---|---|
| **Chapter 8 Winner** | **Tie -- No Differentiation** |
| **Score** | **6.6 / 10** |
| **Bloom's Level** | **Level 3 -- Apply** |

**Why there is no winner:**
- All three providers produced identical outputs through MockLLM
- The `llm_call()` function in `mock_llm.py` only supports OpenAI's API format for live calls; Anthropic and Gemini clients are incompatible
- Statistical computations (OLS, correlation, z-scores) are deterministic
- NLI scores are precomputed, not from the actual BART-MNLI model
- Visualization recommendations use rule-based keyword matching

**What would happen with live LLM calls:**
Chapter 8 is the most LLM-differentiated chapter in design -- statistical interpretation, claim extraction, and GPS reasoning all require genuine analytical capability. With a properly integrated live API path:
- **GPT-4o** would likely excel at quantitative reasoning and concise statistical summaries
- **Claude Sonnet 4** would likely produce the most structured analytical reports with comprehensive caveats
- **Gemini Flash 2.5** would likely offer the fastest execution with solid accuracy

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Current notebook execution | Any (identical) | All produce the same MockLLM output |
| After fixing llm_call() integration | GPT-4o or Claude | Strong quantitative reasoning |
| Cost-efficient production | Gemini Flash 2.5 | Lowest per-token cost |
| Air-gapped / local | DeepSeek V2 (when available) | Zero cloud dependency |


## Provider Profiles for This Chapter

### OpenAI GPT-4o -- "Not Differentiated (MockLLM)"
**Note:** Explicitly in Simulation Mode. Same output as all other providers.

### Claude Sonnet 4 -- "Not Differentiated (MockLLM)"
**Note:** LIVE mode initialized but llm_call() incompatible with Anthropic client. Same MockLLM output as all providers.

### Gemini Flash 2.5 -- "Not Differentiated (MockLLM)"
**Note:** LIVE mode initialized but llm_call() incompatible with Gemini client. Same MockLLM output as all providers.

### DeepSeek V2 16B -- "Not Tested"
**Note:** 0 output cells. Cannot be scored.

---

## Technical Root Cause

The `llm_call()` function in `chapter08/mock_llm.py` (line 272-282) uses:
```python
resp = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
)
result = resp.choices[0].message.content
```

This is the OpenAI API format. When the client is an Anthropic or Gemini object, the call fails silently and falls through to the MockLLM path (line 289). To enable genuine LLM differentiation, the live path would need provider-specific dispatch logic.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Current pipeline demo** | Any (identical) | All produce the same output |
| **Statistical interpretation** | Fix llm_call() integration | Current output is MockLLM for all providers |
| **Fact-checking pipeline** | Fix llm_call() integration | Claim extraction is from MockLLM |
| **GPS hypothesis generation** | Fix llm_call() integration | All GPS stages are MockLLM |
| **Production data analysis** | Re-run after fixing integration | No meaningful model comparison possible |

---

*Analysis based on Chapter 8 notebook outputs executed April 2026. All three cloud providers used MockLLM for LLM-dependent tasks due to an API format incompatibility in the llm_call() function. DeepSeek produced no outputs. Statistical computations and NLI scores are deterministic/precomputed and identical across providers.*
