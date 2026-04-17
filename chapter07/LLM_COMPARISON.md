# Chapter 7 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 7 Tool Orchestration tasks: tool-using agents, chain-of-agents, and agentic workflows with LLM-based fraud risk assessment.

---

## Agent Tasks in This Chapter

- **Tool-Using Agent** (Section 7.1-7.3) -- Selecting and invoking the correct tool from a registry based on user intent, via a Think/Plan/Act cycle
- **Chain-of-Agents** (Section 7.4-7.5) -- Sequential agent pipeline where specialist agents (Finance, News, Sentiment) feed results to a Manager agent for conflict-resolution synthesis
- **Agentic Workflows** (Section 7.6-7.7) -- Order-processing pipeline with inventory validation, LLM-based fraud risk assessment, and human-in-the-loop escalation

## Scoring Dimensions

Each provider is rated 0-10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of tool selections, risk assessments, and parameter extraction |
| **Completeness** | Coverage of all workflow branches and edge cases |
| **Structure & Organization** | Quality of tool call logs and workflow state management |
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

## Key Finding: Mostly Deterministic -- LLM Risk Assessment Failed for 3 of 4 Providers

Chapter 7's tool orchestration is **predominantly deterministic**:
- **Tool selection** uses `parse_query()` -- a template-based keyword matcher, not LLM inference
- **Chain-of-agents** specialist agents (Finance, News, Sentiment) return hardcoded mock data
- **Conflict resolution** uses a rule-based `conflict_score` formula (identical across providers)
- The **only LLM-dependent task** is the `llm_analyst_agent` risk assessment in Section 7.7

### Deterministic Outputs (Identical Across All 4 Providers)

All four providers produced identical outputs for:
- **Tool registry**: 4 tools (load_csv, group_by_and_aggregate, plot_bar_chart, plot_line_chart)
- **Intent classification**: "Show me spend by campaign" -> metric=spend, dimension=campaign_name, chart_type=bar
- **Orchestration runs**: Same Think/Plan/Act sequences for all queries
- **Error handling**: Identical graceful fallbacks for FileNotFoundError and column mismatch demos
- **Chain-of-agents**: Same TechCorp specialist results (PE ratio 24.5, revenue growth 12%, sentiment 0.72)
- **Conflict resolution**: Aligned scenario score 0.22, conflicting scenario score 1.52

### LLM Risk Assessment Results

The `llm_analyst_agent` asks the LLM to assess fraud risk for three orders and return structured JSON.

| Provider | Mode | ORD-1001 | ORD-1002 | ORD-1003 | Error |
|---|---|---|---|---|---|
| **OpenAI GPT-4o** | LIVE | high (fail) | high (fail) | high (fail) | "Expecting value: line 1 column 1 (char 0)" |
| **Claude Sonnet 4** | LIVE | high (fail) | high (fail) | high (fail) | "Expecting value: line 1 column 1 (char 0)" |
| **Gemini Flash 2.5** | LIVE | high (fail) | high (fail) | high (fail) | "Expecting value: line 1 column 1 (char 0)" |
| **DeepSeek V2 16B** | SIMULATION | low | medium | high | Mock correctly differentiated all 3 risk levels |

**Analysis:** All three live-mode providers (OpenAI, Claude, Gemini) failed with the same JSON parsing error. The LLMs returned text that could not be parsed as JSON (likely wrapped in markdown or natural language), causing all orders to default to "high" risk and trigger unnecessary HITL escalation. Only DeepSeek, running in SIMULATION MODE with a rule-based mock, produced the correct differentiated risk assessments.

**Root cause:** The `llm_analyst_agent` expects raw JSON (`{"risk_level": "low|medium|high", "reason": "..."}`) but the live LLMs returned responses that included markdown formatting or explanatory text around the JSON. This is an integration issue in the prompt/parsing code, not a model quality issue.

---

## Provider Performance

### OpenAI GPT-4o

**Execution mode:** LIVE MODE. All deterministic logic identical. LLM risk assessment failed.

**Key outputs:**
- Tool orchestration: All Think/Plan/Act cycles completed successfully
- Error handling: Both deliberate failure demos handled gracefully
- Chain-of-agents: All 3 specialists reported; conflict scenarios computed correctly
- Risk assessment: FAILED -- "LLM analysis failed: Expecting value: line 1 column 1 (char 0)" for all 3 orders
- All orders defaulted to "high" risk, triggering HITL escalation for every order

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 6 | Deterministic outputs correct; LLM risk assessment failed entirely |
| Completeness | 6 | Full pipeline coverage; risk differentiation absent |
| Structure & Organization | 7 | Clean workflow logs; error messages in risk section |
| Conciseness | 7 | Deterministic output appropriate; error noise added |
| Source Grounding | 7 | Follows patterns for deterministic parts; LLM portion diverges |
| Bloom's Level | **2 -- Understand** | Deterministic logic applied; LLM could not demonstrate reasoning |
| Nuance & Caveats | 3 | All orders classified as "high" -- zero nuance in risk triage |
| Practical Utility | 5 | Risk assessment failure means all orders escalated -- useless for triage |

---

### Claude Sonnet 4

**Execution mode:** LIVE MODE. All deterministic logic identical. LLM risk assessment failed.

**Key outputs:**
- Same as OpenAI: all tool, chain, and conflict outputs identical
- Risk assessment: FAILED -- same JSON parse error for all 3 orders
- All orders defaulted to "high" risk

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 6 | Deterministic outputs correct; LLM risk assessment failed |
| Completeness | 6 | Full pipeline; risk differentiation absent |
| Structure & Organization | 7 | Clean workflow logs; error messages in risk section |
| Conciseness | 7 | Appropriate deterministic output; error noise |
| Source Grounding | 7 | Follows deterministic patterns; LLM portion diverges |
| Bloom's Level | **2 -- Understand** | Deterministic logic applied; LLM not exercised successfully |
| Nuance & Caveats | 3 | All orders classified as "high" -- no nuance |
| Practical Utility | 5 | Risk escalation useless when all orders are "high" |

---

### Gemini Flash 2.5

**Execution mode:** LIVE MODE. All deterministic logic identical. LLM risk assessment failed.

**Key outputs:**
- Same as OpenAI and Claude: all deterministic outputs identical
- Risk assessment: FAILED -- same JSON parse error for all 3 orders
- All orders defaulted to "high" risk

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 6 | Deterministic outputs correct; LLM risk assessment failed |
| Completeness | 6 | Full pipeline; risk differentiation absent |
| Structure & Organization | 7 | Clean workflow logs; error messages |
| Conciseness | 7 | Same as others |
| Source Grounding | 7 | Same pattern adherence |
| Bloom's Level | **2 -- Understand** | Same as others |
| Nuance & Caveats | 3 | All orders "high" |
| Practical Utility | 5 | Same triage failure |

---

### DeepSeek V2 16B (Local)

**Execution mode:** SIMULATION MODE (mock LLM). All deterministic logic identical. Rule-based mock produced correct risk differentiation.

**Key outputs:**
- All tool, chain, and conflict outputs identical to other providers
- Risk assessment via mock: ORD-1001 = low ("Standard order parameters. No risk indicators detected"), ORD-1002 = medium ("Order total exceeds typical range for a new customer"), ORD-1003 = high ("Shipping/billing address mismatch combined with high order value")
- Correct HITL escalation: only ORD-1003 escalated (high risk)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | All tool selections correct; risk assessment correctly applies chapter criteria |
| Completeness | 8 | Full pipeline coverage including differentiated risk levels |
| Structure & Organization | 8 | Clean workflow logs; proper state transitions; risk reasons logged |
| Conciseness | 8 | Appropriately detailed without padding |
| Source Grounding | 8 | Follows all chapter patterns precisely |
| Bloom's Level | **3 -- Apply** | Applied risk criteria rules to differentiate three order profiles |
| Nuance & Caveats | 7 | Three distinct risk levels with specific reasons for each |
| Practical Utility | 8 | Correct risk differentiation enables meaningful triage |

> *Scores reflect rule-based mock output, not actual DeepSeek V2 model capabilities.*

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|---|
| Factual Accuracy | **6.0** | **6.0** | **6.0** | **8.0** |
| Completeness | **6.0** | **6.0** | **6.0** | **8.0** |
| Structure & Organization | **7.0** | **7.0** | **7.0** | **8.0** |
| Conciseness | **7.0** | **7.0** | **7.0** | **8.0** |
| Source Grounding | **7.0** | **7.0** | **7.0** | **8.0** |
| Bloom's Taxonomy Level | **2.0 (Understand)** | **2.0 (Understand)** | **2.0 (Understand)** | **3.0 (Apply)** |
| Nuance & Caveats | **3.0** | **3.0** | **3.0** | **7.0** |
| Practical Utility | **5.0** | **5.0** | **5.0** | **8.0** |
| **WEIGHTED AVERAGE** | **5.4** | **5.4** | **5.4** | **7.3** |

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     |
Level 3: Apply       | ============ DeepSeek V2 (mock -- correct risk differentiation)
Level 2: Understand  | ============ OpenAI GPT-4o, Claude Sonnet 4, Gemini Flash 2.5
Level 1: Remember    |
```

DeepSeek's simulation mode reaches Level 3 (Apply) by correctly applying the chapter's multi-criteria risk assessment to differentiate three distinct order profiles. The three cloud providers stay at Level 2 because their LLM calls failed, leaving only deterministic (non-reasoning) outputs.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  DeepSeek V2 (Local)    7.3   =====================.........
  OpenAI GPT-4o          5.4   ================..............
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
  L3 Apply        | D
  L2 Understand   | O C G D
  L1 Remember     | O C G D
```

Legend: **O** = OpenAI GPT-4o, **C** = Claude Sonnet 4, **G** = Gemini Flash 2.5, **D** = DeepSeek V2

---

## Winner: DeepSeek V2 16B (via Simulation Mode)

| | |
|---|---|
| **Chapter 7 Winner** | **DeepSeek V2 16B (Local)** |
| **Score** | **7.3 / 10** |
| **Bloom's Level** | **Level 3 -- Apply** |

**Why DeepSeek V2 wins this chapter:**
- Only provider to produce differentiated risk assessments (low/medium/high)
- Rule-based mock correctly implemented the chapter's risk criteria for all 3 orders
- 1.9-point lead over all three cloud providers (each 5.4)
- Correct HITL escalation: only the genuinely high-risk order was escalated

**Important caveats:**
1. DeepSeek's advantage comes entirely from the simulation mode's rule-based mock, not from the actual DeepSeek V2 model
2. All three cloud providers (OpenAI, Claude, Gemini) failed due to the **same JSON parsing bug** -- the LLMs likely returned valid risk assessments wrapped in markdown or explanatory text, but the code expected raw JSON
3. With corrected parsing (e.g., regex extraction of JSON from the response), all three cloud providers would likely produce superior risk assessments
4. The vast majority of Chapter 7 logic (tool selection, chain-of-agents, conflict resolution) is deterministic and identical across all providers

**Tied for second: OpenAI GPT-4o / Claude Sonnet 4 / Gemini Flash 2.5 (all 5.4/10)** -- all three showed the same behavior: correct deterministic pipeline execution but failed LLM risk assessment.

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Current notebook execution | DeepSeek V2 (simulation) | Only one with working risk differentiation |
| After fixing JSON parsing | Any cloud provider | Live LLM would produce richer analysis than rule-based mock |
| Deterministic tool orchestration | Any (identical) | Tool selection, chain-of-agents, workflow logic are all rule-based |
| Air-gapped / local | DeepSeek V2 | Zero cloud dependency; correct pipeline execution |
| Cost optimization | DeepSeek V2 | Zero cost for better results than cloud providers (in current code) |


## Provider Profiles for This Chapter

### OpenAI GPT-4o -- "JSON Parse Failure"
**Strengths:** All deterministic pipeline stages work correctly; resilient workflow design keeps orders flowing despite LLM failure.
**Weaknesses:** LLM returned non-JSON output that caused parse failure; all orders defaulted to "high" risk.
**Root cause:** "Expecting value: line 1 column 1 (char 0)" -- GPT-4o likely returned JSON wrapped in markdown code fences or explanatory text.

### Claude Sonnet 4 -- "JSON Parse Failure"
**Strengths:** Same as OpenAI for deterministic stages.
**Weaknesses:** Same JSON parse failure; same "high" default for all orders.
**Root cause:** Identical to OpenAI -- Claude likely returned structured text around the JSON.

### Gemini Flash 2.5 -- "JSON Parse Failure"
**Strengths:** Same as others for deterministic stages.
**Weaknesses:** Same JSON parse failure; same "high" default.
**Root cause:** Identical to others -- Gemini likely returned JSON with surrounding text.

### DeepSeek V2 16B -- "The Working Mock"
**Strengths:** Rule-based mock correctly differentiates risk levels; clean workflow execution; only provider where HITL escalation is meaningful.
**Weaknesses:** Running in SIMULATION MODE -- not exercising the actual DeepSeek V2 model; risk reasons are pre-authored, not generated.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Tool orchestration** | Any (deterministic) | parse_query, tool registry, and workflow engine are provider-independent |
| **Risk assessment (current code)** | DeepSeek V2 (simulation) | Only one with functional risk differentiation |
| **Risk assessment (fixed parsing)** | Any cloud provider | Fix JSON extraction to handle markdown-wrapped responses |
| **Chain-of-agents** | Any (deterministic) | Specialist agents and synthesis are rule-based |
| **Local prototyping** | DeepSeek V2 | Zero cost, correct pipeline execution, data stays local |

---

*Analysis based on Chapter 7 notebook outputs executed April 2026. All four providers ran in LIVE MODE except DeepSeek (SIMULATION). OpenAI, Claude, and Gemini all failed on the LLM risk assessment with the same JSON parsing error. DeepSeek's rule-based mock was the only provider to produce differentiated risk levels. The majority of Chapter 7 logic is deterministic and provider-independent.*
