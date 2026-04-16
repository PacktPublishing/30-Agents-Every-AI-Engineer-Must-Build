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

## Critical Finding: All Providers Used MockLLM

Despite API keys being detected for OpenAI (ends with ...RNQA), Claude (ends with ...tAAA), and Gemini (ends with ...s9hA), **all four providers executed through MockLLM** for the actual agent logic. The evidence:

- Every provider's output shows `MockLLM: detected scenario 'service_outage'` for the Autonomous Decision Agent
- Every provider shows `MockLLM: detected scenario 'marketing_campaign_plan'` for the Planning Agent
- Every provider shows `MockLLM: detected scenario 'healthcare_query'` for the Memory-Augmented Agent
- The agent response text is identical across all notebooks: "Based on your history, I can see you've been managing ongoing fatigue. Let me review your previous v..."
- Strategy scoring is fully deterministic (identical `full_autonomous_resolution: 0.775` across all)

**Why this happened:** Chapter 5 uses a shared `MockLLM` class that intercepts all LLM calls via keyword routing. The API key detection occurs at initialization, but the `llm_client` variable is set to `MockLLM()` in the code path regardless of key presence. The architecture prioritizes the simulation pipeline over live API calls.

**Implication:** No meaningful LLM-quality differentiation is possible for this chapter. All scoring reflects MockLLM output quality, which is identical across providers.

---

## Provider Performance

### OpenAI GPT-4o

**Execution mode:** API key detected but MockLLM used for all agent logic. Strategy scoring is deterministic.

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | MockLLM responses are correct (pre-authored); deterministic scoring identical |
| Completeness | 7 | Standard MockLLM coverage of all three architectures |
| Structure & Organization | 7 | MockLLM formatting with color-coded logging |
| Conciseness | 8 | MockLLM responses appropriately sized |
| Source Grounding | 8 | MockLLM follows chapter patterns |
| Bloom's Level | **3 -- Apply** | MockLLM applies patterns without analytical depth |
| Nuance & Caveats | 5 | MockLLM includes basic caveats only |
| Practical Utility | 7 | Functional demonstration output |

> *Output is from MockLLM, not the actual GPT-4o model.*

---

### Claude Sonnet 4

**Execution mode:** API key detected but MockLLM used for all agent logic. Output identical to other providers.

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | MockLLM responses are correct (pre-authored) |
| Completeness | 7 | Standard MockLLM coverage |
| Structure & Organization | 7 | MockLLM formatting |
| Conciseness | 8 | MockLLM responses appropriately sized |
| Source Grounding | 8 | MockLLM follows chapter patterns |
| Bloom's Level | **3 -- Apply** | MockLLM applies patterns without analysis |
| Nuance & Caveats | 5 | Basic MockLLM caveats |
| Practical Utility | 7 | Demonstration quality output |

> *Output is from MockLLM, not the actual Claude Sonnet 4 model.*

---

### Gemini Flash 2.5

**Execution mode:** API key detected but MockLLM used for all agent logic. Output identical to other providers.

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | MockLLM responses correct |
| Completeness | 7 | Standard MockLLM coverage |
| Structure & Organization | 7 | MockLLM formatting |
| Conciseness | 8 | MockLLM sizing |
| Source Grounding | 8 | MockLLM follows patterns |
| Bloom's Level | **3 -- Apply** | MockLLM applies without analysis |
| Nuance & Caveats | 5 | Basic MockLLM caveats |
| Practical Utility | 7 | Demonstration quality output |

> *Output is from MockLLM, not the actual Gemini Flash 2.5 model.*

---

### DeepSeek V2 16B (Local)

**Execution mode:** SIMULATION MODE (no API key). MockLLM used. Output identical to other providers.

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | MockLLM responses correct |
| Completeness | 7 | Standard MockLLM coverage |
| Structure & Organization | 7 | MockLLM formatting |
| Conciseness | 8 | MockLLM sizing |
| Source Grounding | 8 | MockLLM follows patterns |
| Bloom's Level | **3 -- Apply** | MockLLM applies without analysis |
| Nuance & Caveats | 5 | Basic MockLLM caveats |
| Practical Utility | 7 | Demonstration quality output |

> *Output is from MockLLM.*

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|---|
| Factual Accuracy | **8.0*** | **8.0*** | **8.0*** | **8.0*** |
| Completeness | **7.0*** | **7.0*** | **7.0*** | **7.0*** |
| Structure & Organization | **7.0*** | **7.0*** | **7.0*** | **7.0*** |
| Conciseness | **8.0*** | **8.0*** | **8.0*** | **8.0*** |
| Source Grounding | **8.0*** | **8.0*** | **8.0*** | **8.0*** |
| Bloom's Taxonomy Level | **3.0 (Apply)*** | **3.0 (Apply)*** | **3.0 (Apply)*** | **3.0 (Apply)*** |
| Nuance & Caveats | **5.0*** | **5.0*** | **5.0*** | **5.0*** |
| Practical Utility | **7.0*** | **7.0*** | **7.0*** | **7.0*** |
| **WEIGHTED AVERAGE** | **6.6*** | **6.6*** | **6.6*** | **6.6*** |

> *\* All scores reflect MockLLM output (Simulation Mode), not actual model performance. Every provider produced identical outputs because the same MockLLM handled all agent logic.*

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

All providers operate at Level 3 (Apply) because the MockLLM applies pre-authored patterns to keyword-matched scenarios without analysis, evaluation, or synthesis.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  OpenAI GPT-4o          6.6*  ===================...........
  Claude Sonnet 4        6.6*  ===================...........
  Gemini Flash 2.5       6.6*  ===================...........
  DeepSeek V2 (Local)    6.6*  ===================...........
```

> *All identical -- MockLLM output.*

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     |
  L4 Analyze      |
  L3 Apply        | O C G D (all MockLLM)
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
- All four providers produced identical outputs through MockLLM
- Strategy scoring is fully deterministic (rule-based, not LLM-dependent)
- Memory-augmented responses use the same pre-authored MockLLM text
- No provider's actual model capabilities were exercised

**Key takeaway:** Chapter 5's architecture routes all LLM calls through MockLLM regardless of API key presence. To produce a meaningful comparison, the chapter code would need to be modified to use the live LLM client for agent reasoning, planning, and memory synthesis.

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality | Any (identical) | All providers produce the same MockLLM output |
| Cost-efficient production | DeepSeek V2 (Local) | Zero cost, identical output |
| Air-gapped / private data | DeepSeek V2 (Local) | Only option with zero cloud dependency |
| Rapid prototyping | DeepSeek V2 (Local) | No API key needed, instant iteration |


## Provider Profiles for This Chapter

### OpenAI GPT-4o -- "Not Differentiated (MockLLM)"
**Note:** API key detected but not used for agent logic. Output identical to all other providers.

### Claude Sonnet 4 -- "Not Differentiated (MockLLM)"
**Note:** API key detected but not used for agent logic. Output identical to all other providers.

### Gemini Flash 2.5 -- "Not Differentiated (MockLLM)"
**Note:** API key detected but not used for agent logic. Output identical to all other providers.

### DeepSeek V2 16B -- "Not Differentiated (MockLLM)"
**Note:** Ran in explicit Simulation Mode. Output identical to all other providers.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Strategy scoring** | Any (deterministic) | Output is identical -- the scoring logic is rule-based |
| **Agent architecture demos** | Any (MockLLM) | All providers show the same pipeline behavior |
| **Cost optimization** | DeepSeek V2 (Local) | Zero cost for identical results |
| **Production deployment** | Re-run with live LLM calls | Current outputs do not reflect actual model capabilities |

---

*Analysis based on Chapter 5 notebook outputs executed April 2026. All four providers used MockLLM for agent logic despite API keys being detected for OpenAI, Claude, and Gemini. Strategy scoring is deterministic and identical across all providers. No meaningful LLM differentiation was possible.*
