# Chapter 5 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 5 Foundational Architectures tasks: autonomous decision-making, planning agents, and memory-augmented agents.

---

## Agent Tasks in This Chapter

- **Autonomous Decision Agent** -- Strategy scoring across four weighted axes (autonomy, urgency, complexity, escalation) to select between full autonomous resolution, immediate escalation, or guided resolution
- **Planning Agent** -- Hierarchical task decomposition with dependency graphs and execution ordering
- **Memory-Augmented Agent** -- Working memory (session), episodic memory (history), and semantic memory (facts) for context-aware responses

## Scoring Dimensions

Each provider is rated 0-10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of strategy selections and memory retrievals |
| **Completeness** | Coverage of all architectural patterns and edge cases |
| **Structure & Organization** | Quality of decision logs, plan hierarchies, memory structures |
| **Conciseness** | Information density without unnecessary padding |
| **Source Grounding** | Adherence to the chapter's three foundational architectures |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Acknowledgment of decision uncertainty and memory limitations |
| **Practical Utility** | How useful the agent outputs would be in production operations |

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

## Critical Finding: Deterministic Architecture Produces Identical Outputs

All four providers were run in LIVE MODE with real API keys:

- **OpenAI GPT-4o**: `LIVE MODE -- OpenAI GPT-4o (key ...RNQA)`
- **Claude Sonnet 4**: `LIVE MODE -- Claude claude-sonnet-4-20250514 (key ...tAAA)`
- **Gemini Flash 2.5**: `LIVE MODE -- Gemini 2.5 Flash (key ...s9hA)`
- **DeepSeek V2 16B**: `LIVE MODE -- DeepSeek V2 16B via Ollama (local)`

However, Chapter 5's architecture routes all critical agent logic through deterministic pipelines:

1. **Strategy scoring** uses a weighted formula (`full_autonomous_resolution: 0.775`, `immediate_escalation: 0.47`, `guided_autonomous_resolution: 0.5`) that is computed identically across all providers.
2. **Intent classification** uses keyword matching (`service_outage`, confidence 0.9) -- not LLM inference.
3. **Planning Agent** decomposes goals into the same 4-phase DAG (`analyze_requirements -> design_solution -> implement_solution -> validate_results`) regardless of provider.
4. **Memory-Augmented Agent** retrieves from MockVectorDB with identical relevance scores (0.5, 0.0, 0.0) across all providers.
5. **Safety checks** are rule-based (impact risk 0.3, threshold 0.35) and produce identical pass/fail decisions.

**Evidence of identical outputs across all four providers:**
- Cognition: `Strategy selected: 'full_autonomous_resolution' | Scores: {'full_autonomous_resolution': 0.775, 'immediate_escalation': 0.47, 'guided_autonomous_resolution': 0.5}`
- Action: `Plan created for 'service_outage': 6 tasks` with identical T1-T6 task ordering
- Planning: `Decomposed into 4 tasks across 4 phases` with identical G-T1 through G-T4
- Memory: `MockVectorDB: searched ... for user 'patient_42' -> 3 results`

The LLM is invoked for intent classification and goal decomposition, but the downstream code normalizes the results into the same deterministic categories regardless of the model's actual response text.

---

## Provider Performance

### OpenAI GPT-4o

**Execution mode:** LIVE MODE -- API key detected, real API calls enabled. Agent logic is deterministic.

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | All strategy scores, task DAGs, and memory retrievals correct |
| Completeness | 7 | Full pipeline coverage: perception, cognition, action, safety, planning, memory |
| Structure & Organization | 7 | Color-coded logging with section references; clean DAG output |
| Conciseness | 8 | Pipeline outputs are well-sized; no verbose padding |
| Source Grounding | 8 | Follows chapter's three architectures precisely |
| Bloom's Level | **3 -- Apply** | Applies predefined patterns to scenarios without analytical depth |
| Nuance & Caveats | 5 | Basic safety checks and escalation scoring; no uncertainty quantification |
| Practical Utility | 7 | Functional demonstration of all three architectures |

---

### Claude Sonnet 4

**Execution mode:** LIVE MODE -- API key detected, real API calls enabled. Output identical to OpenAI.

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Identical deterministic outputs |
| Completeness | 7 | Same pipeline coverage |
| Structure & Organization | 7 | Same logging and DAG formatting |
| Conciseness | 8 | Same output sizing |
| Source Grounding | 8 | Same pattern adherence |
| Bloom's Level | **3 -- Apply** | Same deterministic pattern application |
| Nuance & Caveats | 5 | Same basic caveats |
| Practical Utility | 7 | Same demonstration quality |

---

### Gemini Flash 2.5

**Execution mode:** LIVE MODE -- API key detected, real API calls enabled. Output identical to others. (Note: FutureWarning about deprecated `google.generativeai` package.)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Identical deterministic outputs |
| Completeness | 7 | Same pipeline coverage |
| Structure & Organization | 7 | Same formatting |
| Conciseness | 8 | Same sizing |
| Source Grounding | 8 | Same pattern adherence |
| Bloom's Level | **3 -- Apply** | Same deterministic application |
| Nuance & Caveats | 5 | Same basic caveats |
| Practical Utility | 7 | Same demonstration quality |

---

### DeepSeek V2 16B (Local)

**Execution mode:** LIVE MODE -- Ollama local model. Output identical to cloud providers.

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Identical deterministic outputs |
| Completeness | 7 | Same pipeline coverage |
| Structure & Organization | 7 | Same formatting |
| Conciseness | 8 | Same sizing |
| Source Grounding | 8 | Same pattern adherence |
| Bloom's Level | **3 -- Apply** | Same deterministic application |
| Nuance & Caveats | 5 | Same basic caveats |
| Practical Utility | 7 | Same demonstration quality |

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|---|
| Factual Accuracy | **8.0** | **8.0** | **8.0** | **8.0** |
| Completeness | **7.0** | **7.0** | **7.0** | **7.0** |
| Structure & Organization | **7.0** | **7.0** | **7.0** | **7.0** |
| Conciseness | **8.0** | **8.0** | **8.0** | **8.0** |
| Source Grounding | **8.0** | **8.0** | **8.0** | **8.0** |
| Bloom's Taxonomy Level | **3.0 (Apply)** | **3.0 (Apply)** | **3.0 (Apply)** | **3.0 (Apply)** |
| Nuance & Caveats | **5.0** | **5.0** | **5.0** | **5.0** |
| Practical Utility | **7.0** | **7.0** | **7.0** | **7.0** |
| **WEIGHTED AVERAGE** | **6.6** | **6.6** | **6.6** | **6.6** |

> All scores reflect deterministic pipeline outputs. Every provider produced identical results because the chapter's architecture normalizes LLM responses into fixed categories before passing them to downstream logic.

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     |
Level 3: Apply       | ============ All Providers (deterministic pipeline)
Level 2: Understand  |
Level 1: Remember    |
```

All providers operate at Level 3 (Apply) because the pipeline applies predefined patterns to keyword-matched scenarios. The LLM contributes to intent classification, but outputs are normalized into fixed strategy scores.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  OpenAI GPT-4o          6.6   ===================...........
  Claude Sonnet 4        6.6   ===================...........
  Gemini Flash 2.5       6.6   ===================...........
  DeepSeek V2 (Local)    6.6   ===================...........
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     |
  L4 Analyze      |
  L3 Apply        | O C G D (all identical)
  L2 Understand   | O C G D
  L1 Remember     | O C G D
```

Legend: **O** = OpenAI GPT-4o, **C** = Claude Sonnet 4, **G** = Gemini Flash 2.5, **D** = DeepSeek V2

---

## Winner: Tie (All Providers)

| | |
|---|---|
| **Chapter 5 Winner** | **Tie -- No Differentiation** |
| **Score** | **6.6 / 10** |
| **Bloom's Level** | **Level 3 -- Apply** |

**Why there is no winner:**
- All four providers ran in LIVE MODE with real API keys
- Despite live API calls, the chapter's deterministic architecture normalizes LLM outputs into fixed categories
- Strategy scoring formula, task DAGs, safety thresholds, and memory retrieval are all rule-based
- The identical `full_autonomous_resolution: 0.775` score across all providers confirms no model differentiation in the pipeline

**Architectural explanation:** The LLM is used for intent classification and goal decomposition, but the results are mapped to a small set of predefined categories (`service_outage`, `billing_inquiry`, etc.). Once classified, all downstream logic is deterministic. This is actually good engineering for production systems -- it makes the pipeline reliable and testable -- but it means the choice of LLM provider has no observable effect on output quality.

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality | Any (identical) | All providers produce identical pipeline outputs |
| Cost-efficient production | DeepSeek V2 (Local) | Zero API cost for identical results |
| Air-gapped / private data | DeepSeek V2 (Local) | Only option with zero cloud dependency |
| Rapid prototyping | DeepSeek V2 (Local) | No API key needed, instant iteration |
| Lowest latency | DeepSeek V2 (Local) | Local inference avoids network round-trips |


## Provider Profiles for This Chapter

### OpenAI GPT-4o -- "Identical Output (Deterministic Pipeline)"
**Note:** LIVE MODE active. API calls made for intent classification and decomposition, but outputs normalized into identical categories.

### Claude Sonnet 4 -- "Identical Output (Deterministic Pipeline)"
**Note:** LIVE MODE active. Same normalization produces identical pipeline results.

### Gemini Flash 2.5 -- "Identical Output (Deterministic Pipeline)"
**Note:** LIVE MODE active. Deprecated SDK warning logged but does not affect output quality.

### DeepSeek V2 16B -- "Identical Output (Deterministic Pipeline)"
**Note:** LIVE MODE via Ollama. Local inference produces identical pipeline results at zero cost.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Strategy scoring** | Any (deterministic) | Output is identical -- scoring logic is rule-based |
| **Planning agent demos** | Any (deterministic) | Task DAG construction is provider-independent |
| **Memory-augmented agent** | Any (deterministic) | MockVectorDB retrieval is provider-independent |
| **Cost optimization** | DeepSeek V2 (Local) | Zero cost for identical results |
| **Production deployment** | Any | Choose based on latency, cost, or organizational preference |

---

*Analysis based on Chapter 5 notebook outputs executed April 2026. All four providers ran in LIVE MODE with real API keys. Despite live API calls, the chapter's deterministic architecture produces identical outputs across all providers. No meaningful LLM differentiation was possible.*
