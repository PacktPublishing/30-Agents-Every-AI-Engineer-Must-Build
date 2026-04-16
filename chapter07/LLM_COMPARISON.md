# Chapter 7 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of three LLM providers running the Chapter 7 Tool Orchestration tasks: tool-using agents, chain-of-agents, and agentic workflows. DeepSeek V2 16B produced 0 output cells and is excluded from scoring.

---

## Agent Tasks in This Chapter

- **Tool-Using Agent** (Section 7.1-7.3) -- Selecting and invoking the correct tool from a registry based on user intent, via a Think/Plan/Act cycle
- **Chain-of-Agents** (Section 7.4-7.5) -- Sequential agent pipeline where each specialist agent (Finance, News, Sentiment) feeds results to a Manager agent for conflict-resolution synthesis
- **Agentic Workflows** (Section 7.6-7.7) -- Order-processing pipeline with inventory validation, LLM-based fraud risk assessment, and human-in-the-loop escalation

## Scoring Dimensions

Each provider is rated 0-10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of tool selections, risk assessments, and parameter extraction |
| **Completeness** | Coverage of all workflow branches and edge cases |
| **Structure & Organization** | Quality of tool call JSON and workflow state management |
| **Conciseness** | Information density without unnecessary padding |
| **Source Grounding** | Adherence to the chapter's orchestration patterns |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Handling of ambiguous tool selection and error recovery |
| **Practical Utility** | How useful the orchestration outputs would be in production |

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

## Key Finding: Heavily Deterministic with LLM Failures in Live Mode

Chapter 7's tool orchestration is **predominantly deterministic**:
- **Tool selection** uses `parse_query()` -- a template-based keyword matcher, not LLM-dependent
- **Chain-of-agents** specialist agents (Finance, News, Sentiment) return hardcoded mock data
- **Synthesize_report** uses a rule-based conflict score formula
- The **only LLM-dependent task** is the `llm_analyst_agent` risk assessment in Section 7.7

### LLM Risk Assessment Results

The `llm_analyst_agent` asks the LLM to assess fraud risk for orders and return structured JSON (`{"risk_level": "low|medium|high", "reason": "..."}`).

| Provider | Mode | Order 1001 | Order 1002 | Order 1003 | Notes |
|---|---|---|---|---|---|
| **OpenAI GPT-4o** | SIMULATION | low | medium | high | Rule-based mock correctly differentiated all 3 risk levels |
| **Claude Sonnet 4** | LIVE | high (fail) | high (fail) | high (fail) | JSON parse error: "Expecting value: line 1 column 1 (char 0)" |
| **Gemini Flash 2.5** | LIVE | high (fail) | high (fail) | high (fail) | API error: "'GenerativeModel' object has no attribute 'chat'" |

**Analysis:** Both live-mode providers (Claude and Gemini) failed on the only LLM-dependent task. Claude's failure was a JSON parsing error (the model likely returned non-JSON text), while Gemini's was an API integration bug (wrong method call). The simulation mode (OpenAI) ironically produced the most useful output because the rule-based mock correctly applied the chapter's risk criteria (address mismatch, high value, new customer).

---

## Provider Performance

### OpenAI GPT-4o

**Execution mode:** SIMULATION MODE. Rule-based mock for risk assessment. All other logic deterministic.

**Key outputs:**
- Risk assessment: Correctly classified ORD-1001 as low risk ("Standard order parameters. No risk indicators detected"), ORD-1002 as medium ("Order total exceeds typical range for a new customer"), ORD-1003 as high ("Shipping/billing address mismatch combined with high order value")
- All tool calls, chain-of-agents, and workflow orchestration completed successfully
- Workflow Results: All 3 orders COMPLETED

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Rule-based risk correctly applies chapter criteria; all tool selections correct |
| Completeness | 8 | Full coverage of all workflow branches including escalation paths |
| Structure & Organization | 8 | Clean workflow logs, proper state transitions |
| Conciseness | 8 | Appropriately detailed -- no verbose padding |
| Source Grounding | 8 | Follows chapter's orchestration patterns precisely |
| Bloom's Level | **3 -- Apply** | Applied risk criteria rules correctly to varied order scenarios |
| Nuance & Caveats | 7 | Differentiated 3 risk levels with specific reasons |
| Practical Utility | 8 | Correct risk differentiation would be useful in production triage |

> *Scores reflect rule-based mock output, not actual GPT-4o capabilities. However, the mock correctly implements the chapter's risk assessment logic.*

---

### Claude Sonnet 4

**Execution mode:** LIVE MODE for LLM calls. Tool selection and workflow logic are deterministic.

**Key outputs:**
- Risk assessment: FAILED for all 3 orders with "Expecting value: line 1 column 1 (char 0)" -- Claude returned non-JSON text that could not be parsed
- Defaulted to "high" risk for all orders, causing unnecessary HITL escalation
- All tool calls and chain-of-agents worked correctly (deterministic)
- Workflow Results: All 3 orders COMPLETED (workflow is resilient to risk assessment failure)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 6 | Deterministic outputs correct; LLM risk assessment failed entirely |
| Completeness | 6 | Tool pipeline complete but risk assessment produced no useful differentiation |
| Structure & Organization | 7 | Workflow logs clean; risk assessment output is error messages |
| Conciseness | 7 | Deterministic output appropriate; error messages add noise |
| Source Grounding | 7 | Follows patterns for deterministic parts; LLM portion diverges |
| Bloom's Level | **2 -- Understand** | Deterministic logic applied; LLM could not demonstrate higher reasoning |
| Nuance & Caveats | 3 | All orders classified as "high" -- no nuance in risk differentiation |
| Practical Utility | 5 | Risk assessment failure means all orders escalated -- useless for triage |

---

### Gemini Flash 2.5

**Execution mode:** LIVE MODE for LLM calls. Tool selection and workflow logic are deterministic.

**Key outputs:**
- Risk assessment: FAILED for all 3 orders with "'GenerativeModel' object has no attribute 'chat'" -- an API integration bug
- Defaulted to "high" risk for all orders
- All tool calls and chain-of-agents worked correctly (deterministic)
- Workflow Results: All 3 orders COMPLETED

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 6 | Deterministic outputs correct; LLM risk assessment failed |
| Completeness | 6 | Tool pipeline complete; risk differentiation absent |
| Structure & Organization | 7 | Clean workflow logs; error messages in risk section |
| Conciseness | 7 | Deterministic output fine; error messages add noise |
| Source Grounding | 7 | Follows deterministic patterns; LLM portion fails |
| Bloom's Level | **2 -- Understand** | Deterministic logic applied; LLM not exercised |
| Nuance & Caveats | 3 | All orders classified as "high" -- zero nuance |
| Practical Utility | 5 | Risk assessment failure renders triage useless |

---

### DeepSeek V2 16B (Local)

**Execution mode:** 0 output cells in the notebook. Cannot be scored.

> *DeepSeek notebook has no saved outputs. Excluded from scoring.*

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 |
|---|---|---|---|
| Factual Accuracy | **8.0** | **6.0** | **6.0** |
| Completeness | **8.0** | **6.0** | **6.0** |
| Structure & Organization | **8.0** | **7.0** | **7.0** |
| Conciseness | **8.0** | **7.0** | **7.0** |
| Source Grounding | **8.0** | **7.0** | **7.0** |
| Bloom's Taxonomy Level | **3.0 (Apply)** | **2.0 (Understand)** | **2.0 (Understand)** |
| Nuance & Caveats | **7.0** | **3.0** | **3.0** |
| Practical Utility | **8.0** | **5.0** | **5.0** |
| **WEIGHTED AVERAGE** | **7.3** | **5.4** | **5.4** |

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     |
Level 3: Apply       | ============ OpenAI GPT-4o (mock -- correct risk differentiation)
Level 2: Understand  | ============ Claude Sonnet 4, Gemini Flash 2.5 (LLM failures)
Level 1: Remember    |
```

OpenAI's simulation mode reaches Level 3 (Apply) by correctly applying the chapter's multi-criteria risk assessment to differentiate three distinct order profiles. Claude and Gemini stay at Level 2 because their LLM calls failed, leaving only deterministic (non-reasoning) outputs.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  OpenAI GPT-4o          7.3   =====================.........
  Claude Sonnet 4        5.4   ================..............
  Gemini Flash 2.5       5.4   ================..............
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     |
  L4 Analyze      |
  L3 Apply        | O
  L2 Understand   | O C G
  L1 Remember     | O C G
```

Legend: **O** = OpenAI GPT-4o, **C** = Claude Sonnet 4, **G** = Gemini Flash 2.5

---

## Winner: OpenAI GPT-4o (via Simulation Mode)

| | |
|---|---|
| **Chapter 7 Winner** | **OpenAI GPT-4o** |
| **Score** | **7.3 / 10** |
| **Bloom's Level** | **Level 3 -- Apply** |

**Why OpenAI GPT-4o wins this chapter:**
- Only provider to produce differentiated risk assessments (low/medium/high)
- Rule-based mock correctly implemented the chapter's risk criteria
- 1.9-point lead over Claude and Gemini (both 5.4)

**Important caveats:**
1. OpenAI's advantage comes from the simulation mode's rule-based mock, not from the actual GPT-4o model
2. Claude and Gemini's failures are **integration bugs**, not model quality issues -- Claude's JSON parsing error and Gemini's API method error would both be fixable
3. With corrected integrations, Claude and Gemini would likely produce superior risk assessments to the rule-based mock
4. The vast majority of Chapter 7 logic is deterministic and provider-independent

**Runner-up:** Claude Sonnet 4 / Gemini Flash 2.5 (tied at 5.4/10)

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Current notebook execution | OpenAI GPT-4o (simulation) | Only one with working risk differentiation |
| After fixing integration bugs | Claude or Gemini (LIVE) | Live LLM would outperform rule-based mock |
| Deterministic tool orchestration | Any (identical) | Tool selection, chain-of-agents, workflow logic are all rule-based |
| Air-gapped / local | DeepSeek V2 (not tested) | Zero cloud dependency when Ollama is available |


## Provider Profiles for This Chapter

### OpenAI GPT-4o -- "The Reliable Mock"
**Strengths:** Rule-based mock correctly differentiates risk levels; clean workflow execution; all orders properly triaged.
**Weaknesses:** Not actually exercising GPT-4o -- the simulation mode is the winner, not the model.

### Claude Sonnet 4 -- "Integration Bug"
**Strengths:** All deterministic pipeline stages work correctly; resilient workflow design keeps orders flowing despite LLM failure.
**Weaknesses:** LLM returned non-JSON output that caused parse failure; all orders defaulted to "high" risk.
**Root cause:** "Expecting value: line 1 column 1 (char 0)" suggests Claude returned markdown or natural language instead of raw JSON.

### Gemini Flash 2.5 -- "API Integration Bug"
**Strengths:** Same as Claude for deterministic stages.
**Weaknesses:** "'GenerativeModel' object has no attribute 'chat'" indicates the code used the wrong Gemini SDK method.
**Root cause:** The `llm.generate()` wrapper uses a `.chat` attribute that doesn't exist on the Gemini `GenerativeModel` object.

### DeepSeek V2 16B -- "Not Tested"
**Note:** Notebook has 0 output cells. Cannot be scored.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Tool orchestration** | Any (deterministic) | parse_query, tool registry, and workflow engine are provider-independent |
| **Risk assessment (current code)** | OpenAI GPT-4o (simulation) | Only one with functional risk differentiation |
| **Risk assessment (fixed code)** | Claude or Gemini | Live LLM would produce richer analysis than rule-based mock |
| **Chain-of-agents** | Any (deterministic) | Specialist agents and synthesis are rule-based |
| **Local prototyping** | DeepSeek V2 (when available) | Zero cost, data stays local |

---

*Analysis based on Chapter 7 notebook outputs executed April 2026. Claude and Gemini ran in LIVE mode but their LLM calls failed due to integration bugs. OpenAI ran in Simulation Mode with a rule-based mock. DeepSeek produced no outputs. The majority of Chapter 7 logic is deterministic and provider-independent.*
