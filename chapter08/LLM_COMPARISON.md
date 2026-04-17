# Chapter 8 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 8 Data Analysis and Reasoning tasks: visualization recommendation, statistical interpretation, verification (NLI), fact-checking, and the General Problem Solver (GPS).

---

## Agent Tasks in This Chapter

- **Data Analysis Agent** (Section 8.1) -- Cognitive loop with visualization recommendation, OLS regression, anomaly detection, and LLM-powered statistical interpretation
- **Verification & Validation Agent** (Section 8.2) -- NLI-based fact-checking using BART-MNLI for evidence scoring
- **General Problem Solver** (Section 8.3-8.5) -- 5-stage meta-reasoning: decompose, find analogies, hypothesize, test, and meta-learn
- **Case Study: News Fact-Checking** (Section 8.4) -- Claim extraction from news articles with verification pipeline

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

## Critical Finding: Only OpenAI Achieved Live LLM Calls

Despite all providers initializing in LIVE MODE:

| Provider | Init Message | Live LLM Calls? | Reason |
|---|---|---|---|
| **OpenAI GPT-4o** | "OpenAI client initialized. Running in LIVE mode." | YES | `llm_call()` uses `client.chat.completions.create()` -- compatible |
| **Claude Sonnet 4** | "Anthropic client initialized. Running in LIVE mode." | NO | `'Anthropic' object has no attribute 'chat'` -- API incompatible with llm_call() |
| **Gemini Flash 2.5** | "Gemini client initialized. Running in LIVE mode." | NO | `'GenerativeModel' object has no attribute 'chat'` -- API incompatible with llm_call() |
| **DeepSeek V2 16B** | N/A | NO | 0 output cells in notebook |

**Root cause:** The `llm_call()` function in `mock_llm.py` uses `client.chat.completions.create()` -- the OpenAI API format. When the client is an Anthropic or Gemini object, the call fails and falls back to MockLLM. Claude and Gemini's error messages explicitly confirm: `Live API call failed: 'Anthropic' object has no attribute 'chat' -- falling back to MockLLM.`

**Result:** OpenAI GPT-4o is the only provider with genuine LLM-generated outputs for statistical interpretation, claim extraction, and GPS reasoning. Claude and Gemini both fell back to MockLLM for every LLM-dependent task.

---

## What Components Are Deterministic

| Component | Source | Identical Across Providers? |
|---|---|---|
| Visualization recommendation | Rule-based keyword matching | Yes (line, bar, scatter, table) |
| OLS regression | statsmodels computation | Yes (R^2=0.774, coeff=2.4947) |
| Anomaly detection | Z-score calculation | Yes (no anomalies at z>3.0) |
| Descriptive statistics | pandas .describe() | Yes (mean sales 111.25, std 56.24) |
| NLI verification | Precomputed scores | Yes (entailment 0.92, neutral 0.05, contradiction 0.03) |
| Claim verification | Trusted database lookup | Yes (both claims contradicted) |

---

## LLM-Dependent Task 1: Statistical Interpretation

### OpenAI GPT-4o (LIVE)

**Actual output:** Multi-paragraph interpretation covering:
- "strong positive relationship between marketing spending and revenue, with a correlation of 0.880"
- "marketing efforts are likely effective in driving sales"
- Standard deviation explanation: "moderate level of variability"
- Absence of anomalies: "all sales figures fall within the expected range"
- Conclusion: "marketing investments are paying off"

**Assessment:** The interpretation correctly identifies the correlation strength (0.880) and draws appropriate causal inferences. It explains standard deviation in accessible language and correctly notes the absence of anomalies. However, it states "marketing spend explains approximately" without specifying R^2 directly, and overstates causation ("paying off") where correlation is the evidence.

### Claude Sonnet 4 (MockLLM Fallback)

**Actual output:** "Marketing spend explains approximately 62% of the variation in revenue, indicating a strong positive correlation. Sales in Q2 for Region East appear unusually high, possibly due to promotional pricing or data entry anomalies."

**Assessment:** This is the MockLLM pre-authored response. It cites 62% (likely from R^2 in a different parameterization), mentions Q2 Region East anomalies (not present in the actual data where no anomalies were detected at z>3.0), and is only two sentences long.

### Gemini Flash 2.5 (MockLLM Fallback)

**Actual output:** Identical to Claude -- same MockLLM response: "Marketing spend explains approximately 62% of the variation in revenue..."

### DeepSeek V2 16B

No output cells in notebook.

---

## LLM-Dependent Task 2: Claim Extraction

### OpenAI GPT-4o (LIVE)

**Actual output:** LLM call succeeded (`LLM call completed (live API)`) but the response was not valid JSON, triggering regex fallback. The fallback successfully extracted 2 claims:
- Claim 1: "unemployment rate fell by 5%" (metric=unemployment rate change, value=5%, entity=Ottawa, period=2024)
- Claim 2: "budget surplus of $12 million for the 2024" (metric=budget surplus, value=12000000.0, entity=Ottawa, period=2024)

**Assessment:** GPT-4o produced a response that required regex fallback but ultimately yielded correct claim extraction. The regex parser successfully recovered both claims with accurate metadata.

### Claude Sonnet 4 (MockLLM Fallback)

**Actual output:** `Live API call failed: 'Anthropic' object has no attribute 'chat' -- falling back to MockLLM.` MockLLM extracted the same 2 claims with slightly different text ("the city's unemployment rate fell by 5% last year" vs. "unemployment rate fell by 5%").

### Gemini Flash 2.5 (MockLLM Fallback)

**Actual output:** Same MockLLM fallback, same 2 claims, identical to Claude.

---

## LLM-Dependent Task 3: GPS (General Problem Solver)

### OpenAI GPT-4o (LIVE)

**Actual output:** GPS decomposition produced three rich sub-problems, each with 3-4 elaborating questions:
1. **Understanding Ecological Network Resilience Principles** -- "What are the key principles and mechanisms that contribute to resilience in ecological networks? How do ecological networks maintain stability and recover from disturbances?"
2. **Analyzing Cascading Failures in Electrical Power Grids** -- "What are the common causes and characteristics of cascading failures? What are the critical vulnerabilities and interdependencies?"
3. **Applying Ecological Resilience Principles to Power Grids** -- "How can principles of ecological resilience be adapted or translated? Are there case studies or models?"

**Assessment:** GPT-4o's GPS decomposition is significantly richer than MockLLM. Each sub-problem includes multiple elaborating questions that frame a genuine research agenda. The structure progresses logically from understanding each domain to applying cross-domain principles.

### Claude Sonnet 4 (MockLLM Fallback)

**Actual output:** MockLLM GPS decomposition:
- "What network topology properties correlate with cascading failure resistance?"
- "How does biodiversity contribute to ecosystem network resilience?"
- "What redundancy mechanisms exist in ecological vs. engineered networks?"

MockLLM analogies included references to Dunne et al. (2002) and keystone species concepts.

**Assessment:** The MockLLM responses are well-crafted (pre-authored) but briefer. Three concise sub-problems vs. GPT-4o's three detailed sub-problems with elaborating questions. The MockLLM analogies include academic citations, which the live GPT-4o output likely also produced (output was truncated).

### Gemini Flash 2.5 (MockLLM Fallback)

Identical to Claude -- same MockLLM responses.

---

## Provider Performance

### OpenAI GPT-4o

**Execution mode:** LIVE MODE -- only provider with actual GPT-4o responses for LLM-dependent tasks.

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct correlation (0.880), appropriate causal language; claim extraction required regex fallback but succeeded; statistical computations correct |
| Completeness | 8 | Multi-paragraph stats interpretation covering correlation, variability, anomalies, and conclusion; GPS decomposition with elaborating questions |
| Structure & Organization | 7 | Flowing paragraphs for stats; GPS well-structured with numbered sub-problems |
| Conciseness | 7 | Stats interpretation somewhat verbose (could be tighter); GPS appropriately detailed |
| Source Grounding | 8 | Correctly references computed statistics; claims map to article text |
| Bloom's Level | **5 -- Evaluate** | GPS decomposition demonstrates evaluation of cross-domain applicability; stats interpretation assesses causal relationships |
| Nuance & Caveats | 6 | Noted absence of anomalies; mentioned variability context; slightly overstated causation |
| Practical Utility | 8 | Stats interpretation actionable; GPS sub-problems frame a real research agenda |

---

### Claude Sonnet 4

**Execution mode:** LIVE MODE initialized but all llm_call() routes through MockLLM due to API incompatibility.

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 6 | MockLLM stats interpretation cites 62% (imprecise); claims Q2 Region East anomaly not present in data |
| Completeness | 6 | Stats interpretation is only 2 sentences; GPS decomposition is 3 brief sub-problems |
| Structure & Organization | 7 | Deterministic outputs well-structured; MockLLM responses adequate |
| Conciseness | 8 | MockLLM responses brief (but at cost of completeness) |
| Source Grounding | 6 | MockLLM references a "Q2 Region East" anomaly that the actual data does not contain |
| Bloom's Level | **3 -- Apply** | MockLLM applies pre-authored analytical patterns without genuine reasoning |
| Nuance & Caveats | 5 | MockLLM mentions "possibly due to promotional pricing or data entry anomalies" |
| Practical Utility | 6 | MockLLM output is functional but contains a factual error about anomalies |

> *Output is from MockLLM, not the actual Claude Sonnet 4 model.*

---

### Gemini Flash 2.5

**Execution mode:** LIVE MODE initialized but all llm_call() routes through MockLLM due to API incompatibility.

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 6 | Same MockLLM output as Claude -- same 62% claim, same phantom anomaly |
| Completeness | 6 | Same 2-sentence stats interpretation; same 3 GPS sub-problems |
| Structure & Organization | 7 | Same formatting |
| Conciseness | 8 | Same sizing |
| Source Grounding | 6 | Same phantom anomaly reference |
| Bloom's Level | **3 -- Apply** | MockLLM output |
| Nuance & Caveats | 5 | Same MockLLM caveats |
| Practical Utility | 6 | Same MockLLM utility |

> *Output is from MockLLM, not the actual Gemini Flash 2.5 model.*

---

### DeepSeek V2 16B (Local)

**Execution mode:** 0 output cells in the notebook. Cannot be scored.

> *DeepSeek notebook has no saved outputs. Excluded from scoring.*

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 |
|---|---|---|---|
| Factual Accuracy | **8.0** | **6.0*** | **6.0*** |
| Completeness | **8.0** | **6.0*** | **6.0*** |
| Structure & Organization | **7.0** | **7.0*** | **7.0*** |
| Conciseness | **7.0** | **8.0*** | **8.0*** |
| Source Grounding | **8.0** | **6.0*** | **6.0*** |
| Bloom's Taxonomy Level | **5.0 (Evaluate)** | **3.0 (Apply)*** | **3.0 (Apply)*** |
| Nuance & Caveats | **6.0** | **5.0*** | **5.0*** |
| Practical Utility | **8.0** | **6.0*** | **6.0*** |
| **WEIGHTED AVERAGE** | **7.1** | **5.9*** | **5.9*** |

> *\* Claude and Gemini scores reflect MockLLM output due to API incompatibility in llm_call(). Their actual model capabilities were not exercised.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    | ============ OpenAI GPT-4o (GPS decomposition, stats evaluation)
Level 4: Analyze     |
Level 3: Apply       | ============ Claude Sonnet 4*, Gemini Flash 2.5* (MockLLM)
Level 2: Understand  |
Level 1: Remember    |
```

OpenAI GPT-4o reaches Level 5 through its GPS decomposition, which evaluates cross-domain applicability of ecological resilience principles to power grid engineering, and through its statistical interpretation, which assesses the strength and implications of the marketing-revenue correlation. Claude and Gemini operate at Level 3 via MockLLM's pre-authored patterns.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  OpenAI GPT-4o          7.1   =====================.........
  Claude Sonnet 4        5.9*  =================.............
  Gemini Flash 2.5       5.9*  =================.............
```

> *Claude and Gemini used MockLLM for all LLM-dependent tasks.*

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     | O
  L4 Analyze      |
  L3 Apply        | O C* G*
  L2 Understand   | O C* G*
  L1 Remember     | O C* G*
```

Legend: **O** = OpenAI GPT-4o, **C*** = Claude Sonnet 4 (MockLLM), **G*** = Gemini Flash 2.5 (MockLLM)

---

## Winner: OpenAI GPT-4o

| | |
|---|---|
| **Chapter 8 Winner** | **OpenAI GPT-4o** |
| **Score** | **7.1 / 10** |
| **Bloom's Level** | **Level 5 -- Evaluate** |

**Why OpenAI GPT-4o wins this chapter:**
- Only provider where `llm_call()` executed successfully against the live API
- Produced genuinely rich statistical interpretation (multi-paragraph, covering correlation, variability, anomalies)
- GPS decomposition significantly more detailed than MockLLM's pre-authored output (three sub-problems with elaborating questions vs. three brief one-liners)
- Claim extraction succeeded via regex fallback after initial JSON parse issue
- 1.2-point lead over Claude and Gemini (both 5.9)

**Why this is an unfair comparison:**
- Claude Sonnet 4 and Gemini Flash 2.5 were **not tested** on the LLM-dependent tasks -- they were blocked by an API format incompatibility in `llm_call()`
- The `llm_call()` function uses `client.chat.completions.create()`, which is OpenAI's specific API format
- With proper provider-specific dispatch, Claude and Gemini would likely score 7.0+ based on their Chapter 6 performance
- This is an integration bug, not a model quality comparison

**MockLLM factual error:** The MockLLM statistical interpretation claims "Sales in Q2 for Region East appear unusually high" -- but the actual data shows no anomalies (z-score threshold >3.0 found nothing). This phantom anomaly penalizes Claude and Gemini's source grounding scores, but it reflects the MockLLM's pre-authored content, not the models themselves.

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Current notebook execution | OpenAI GPT-4o | Only one with live LLM responses |
| After fixing llm_call() | Re-evaluate all providers | Claude and Gemini would likely be competitive |
| Statistical interpretation | OpenAI GPT-4o (currently) | Only provider producing live analysis |
| GPS hypothesis generation | OpenAI GPT-4o (currently) | Richer decomposition than MockLLM |
| Cost optimization | Fix integration first | Cannot compare costs meaningfully when 2/3 providers use MockLLM |


## Provider Profiles for This Chapter

### OpenAI GPT-4o -- "The Only Live Provider"
**Strengths:** Only provider with working live LLM calls; produced multi-paragraph statistical interpretation; rich GPS decomposition with elaborating questions; claim extraction succeeded via fallback.
**Weaknesses:** Stats interpretation slightly overstates causation ("paying off"); claim extraction required regex fallback (not clean JSON); advantage is due to API compatibility, not inherent model superiority.

### Claude Sonnet 4 -- "Blocked by API Incompatibility"
**Note:** LIVE MODE initialized but all `llm_call()` routes failed with `'Anthropic' object has no attribute 'chat'`. All LLM-dependent outputs are from MockLLM. The Anthropic client is incompatible with the OpenAI-format `client.chat.completions.create()` call.

### Gemini Flash 2.5 -- "Blocked by API Incompatibility"
**Note:** LIVE MODE initialized but all `llm_call()` routes failed with `'GenerativeModel' object has no attribute 'chat'`. Same issue as Claude. All LLM-dependent outputs are from MockLLM.

### DeepSeek V2 16B -- "No Output"
**Note:** 0 output cells in the notebook. Cannot be scored.

---

## Technical Root Cause

The `llm_call()` function in `chapter08/mock_llm.py` uses:
```python
resp = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
)
result = resp.choices[0].message.content
```

This is exclusively the OpenAI API format. When the client is an Anthropic or Gemini object, the call raises an AttributeError and falls through to MockLLM. To enable genuine cross-provider comparison, `llm_call()` would need provider-specific dispatch:
- **OpenAI:** `client.chat.completions.create()` (current)
- **Anthropic:** `client.messages.create()`
- **Gemini:** `model.generate_content()`
- **Ollama:** `requests.post()` to local endpoint

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Statistical interpretation (current)** | OpenAI GPT-4o | Only provider with live responses |
| **Claim extraction (current)** | OpenAI GPT-4o | Only provider with live extraction |
| **GPS reasoning (current)** | OpenAI GPT-4o | Richest decomposition output |
| **After fixing llm_call()** | Re-evaluate all | Claude and Gemini capabilities untested |
| **Production data analysis** | Fix integration first | 2 of 3 providers not meaningfully tested |
| **Deterministic pipeline** | Any (identical) | Viz recommendation, OLS, anomaly detection, NLI are provider-independent |

---

*Analysis based on Chapter 8 notebook outputs executed April 2026. OpenAI GPT-4o was the only provider with working live LLM calls. Claude and Gemini initialized in LIVE MODE but fell back to MockLLM due to API format incompatibility in the llm_call() function. DeepSeek produced no outputs. Statistical computations, visualization recommendations, and NLI scores are deterministic and identical across providers. The MockLLM statistical interpretation contains a factual error about Q2 Region East anomalies that do not exist in the actual data.*
