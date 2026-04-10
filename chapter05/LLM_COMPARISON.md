# Chapter 5 — LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 5 Foundational Architectures tasks: autonomous decision-making, planning agents, and memory-augmented agents.

---

## Agent Tasks in This Chapter

- **Autonomous Decision Agent** — Strategy scoring across four weighted axes (autonomy, urgency, complexity, escalation) to select between full autonomous resolution, immediate escalation, or guided resolution
- **Planning Agent** — Hierarchical task decomposition with dependency graphs and execution ordering
- **Memory-Augmented Agent** — Working memory (session), episodic memory (history), and semantic memory (facts) for context-aware responses

## Scoring Dimensions

Each provider is rated 0–10 across eight dimensions:

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

## Key Observation: Mixed Deterministic and LLM-Dependent Logic

Chapter 5 uses a **hybrid approach**:
- **Strategy scoring** is deterministic (weighted axis calculations) — identical across providers
- **LLM-dependent cells** include: autonomous reasoning (interpreting perception data), plan generation (decomposing tasks into steps), and memory-augmented responses (synthesizing from working + episodic + semantic memory)
- The strategy selection outcome (`full_autonomous_resolution`, score 0.775) is identical across all providers because it's calculated from fixed weights

**Execution mode note:** Claude and OpenAI ran in LIVE mode. Gemini and DeepSeek V2 ran in SIMULATION mode (using MockLLM) for this chapter, meaning their LLM-dependent outputs are from the MockLLM engine rather than the actual models.

---

## Provider Performance

### Claude Sonnet 4

**LLM-dependent cell behavior:**
- Autonomous reasoning: Produced structured decision rationale with confidence levels
- Plan generation: Created hierarchical task breakdown with dependency annotations
- Memory synthesis: Combined working + episodic + semantic memory into coherent, context-aware responses
- Ran in LIVE mode

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Correct strategy reasoning; sound plan decomposition |
| Completeness | 9 | All three architectures fully exercised with rich detail |
| Structure & Organization | 10 | Nested decision logs, dependency graphs, memory citation |
| Conciseness | 7 | Comprehensive but verbose decision rationales |
| Source Grounding | 9 | Closely mirrors chapter's three-architecture framework |
| Bloom's Level | **5 — Evaluate** | Assessed trade-offs between strategies; evaluated memory relevance |
| Nuance & Caveats | 9 | Confidence scores, escalation thresholds, memory decay acknowledgment |
| Practical Utility | 9 | Decision logs suitable for production audit trails |

---

### Gemini Flash 2.5

**LLM-dependent cell behavior:**
- Ran in SIMULATION mode — outputs are from MockLLM, not the actual Gemini model
- Deterministic cells (strategy scoring) produced identical results to other providers
- LLM-dependent cells used pre-authored MockLLM responses

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | MockLLM responses are correct (pre-authored) |
| Completeness | 7 | MockLLM provides standard coverage |
| Structure & Organization | 7 | MockLLM formatting is adequate |
| Conciseness | 8 | MockLLM responses are appropriately sized |
| Source Grounding | 8 | MockLLM responses follow chapter patterns |
| Bloom's Level | **3 — Apply** | MockLLM applies patterns without analytical depth |
| Nuance & Caveats | 5 | MockLLM includes basic caveats |
| Practical Utility | 7 | Functional demonstration output |

> *Gemini ran in Simulation Mode — scores reflect MockLLM output, not Gemini Flash 2.5 capabilities.*

---

### DeepSeek V2 16B (Local)

**LLM-dependent cell behavior:**
- Ran in SIMULATION mode — outputs are from MockLLM
- Deterministic cells produced identical strategy scoring results
- No differentiation from Gemini's MockLLM output

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | MockLLM responses are correct |
| Completeness | 7 | Standard MockLLM coverage |
| Structure & Organization | 7 | MockLLM formatting |
| Conciseness | 8 | MockLLM sizing |
| Source Grounding | 8 | MockLLM follows patterns |
| Bloom's Level | **3 — Apply** | MockLLM applies without analysis |
| Nuance & Caveats | 5 | Basic MockLLM caveats |
| Practical Utility | 7 | Demonstration-quality output |

> *DeepSeek ran in Simulation Mode — scores reflect MockLLM output, not DeepSeek V2 capabilities.*

---

### OpenAI GPT-4o

**LLM-dependent cell behavior:**
- Autonomous reasoning: Clear decision rationale with strategy justification
- Plan generation: Logical task decomposition with estimated durations
- Memory synthesis: Good integration of memory types with contextual responses
- Ran in LIVE mode

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Correct reasoning and plan structure |
| Completeness | 8 | All architectures covered with good detail |
| Structure & Organization | 8 | Clean output with logical flow |
| Conciseness | 8 | Balanced detail level |
| Source Grounding | 8 | Follows chapter frameworks |
| Bloom's Level | **4 — Analyze** | Analyzed dependencies and decomposed tasks logically |
| Nuance & Caveats | 6 | Some acknowledgment of decision uncertainty |
| Practical Utility | 8 | Functional production output |

---

## Overall Scorecard

| Dimension | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) | OpenAI GPT-4o |
|---|---|---|---|---|
| Factual Accuracy | **9.0** | **8.0*** | **8.0*** | **9.0** |
| Completeness | **9.0** | **7.0*** | **7.0*** | **8.0** |
| Structure & Organization | **10.0** | **7.0*** | **7.0*** | **8.0** |
| Conciseness | **7.0** | **8.0*** | **8.0*** | **8.0** |
| Source Grounding | **9.0** | **8.0*** | **8.0*** | **8.0** |
| Bloom's Taxonomy Level | **5.0 (Evaluate)** | **3.0 (Apply)*** | **3.0 (Apply)*** | **4.0 (Analyze)** |
| Nuance & Caveats | **9.0** | **5.0*** | **5.0*** | **6.0** |
| Practical Utility | **9.0** | **7.0*** | **7.0*** | **8.0** |
| **WEIGHTED AVERAGE** | **8.4** | **6.6*** | **6.6*** | **7.4** |

> *\* Gemini and DeepSeek scores reflect MockLLM output (Simulation Mode), not actual model performance. With live API keys, scores would likely be higher.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    | ████████████ Claude Sonnet 4
Level 4: Analyze     | ████████████ OpenAI GPT-4o
Level 3: Apply       | ████████████ Gemini* / DeepSeek* (*MockLLM)
Level 2: Understand  |
Level 1: Remember    |
```

Claude reaches Level 5 by evaluating trade-offs between autonomous resolution strategies and assessing memory relevance with confidence weighting. GPT-4o analyzes task dependencies at Level 4. The MockLLM outputs for Gemini and DeepSeek apply the patterns at Level 3 without deeper reasoning.

---



---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  ────────────────────  ─────  ──────────────────────────────
  🥇 Claude Sonnet 4        8.4  █████████████████████████░░░░░
  🥈 OpenAI GPT-4o          7.4  ██████████████████████░░░░░░░░
  🥉 Gemini Flash 2.5       6.6  ███████████████████░░░░░░░░░░░
     DeepSeek V2 (Local)    6.6  ███████████████████░░░░░░░░░░░
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  ─────  ────────────  ──────────────────────────
  L6 Create       │ 
  L5 Evaluate     ┃ C
  L4 Analyze      ┃ C O
  L3 Apply        ┃ C G D O
  L2 Understand   ┃ C G D O
  L1 Remember     ┃ C G D O
```

Legend: **C** = Claude Sonnet 4, **G** = Gemini Flash 2.5, **D** = DeepSeek V2, **O** = OpenAI GPT-4o

### Cross-Chapter Context

How this chapter compares to the book-wide average:

```
  Provider              Ch Score  Book Avg  Delta
  ────────────────────  ────────  ────────  ─────
  Claude Sonnet 4          8.4       8.5    ▼+0.1
  Gemini Flash 2.5         6.6       7.2    ▼+0.6
  DeepSeek V2 (Local)      6.6       5.7    ▲+0.9
  OpenAI GPT-4o            7.4       7.4    ▼+0.0
```

---

## Winner: Claude Sonnet 4

| | |
|---|---|
| **Chapter 5 Winner** | **Claude Sonnet 4** |
| **Score** | **8.4 / 10** |
| **Bloom's Level** | **Level 5 — Evaluate** |

**Why Claude Sonnet 4 wins this chapter:**
- Highest weighted average across all 8 scoring dimensions
- Bloom's Level 5 (Evaluate) — the deepest cognitive sophistication
- 1.0-point lead over runner-up OpenAI GPT-4o (7.4)

**Runner-up:** OpenAI GPT-4o (7.4/10)

**Third place:** Gemini Flash 2.5 (6.6/10)

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality | Claude Sonnet 4 | Highest scores across all dimensions |
| Cost-efficient production | Gemini Flash 2.5 | Best quality-per-dollar ratio |
| Air-gapped / private data | DeepSeek V2 (Local) | Only option with zero cloud dependency |
| Rapid prototyping | DeepSeek V2 (Local) | No API key, instant iteration, zero cost |


## Provider Profiles for This Chapter

### Claude Sonnet 4 — "The Decision Architect"
**Strengths:** Richest autonomous reasoning with confidence scoring; best memory synthesis integrating all three memory types; production-quality audit trails.
**Weaknesses:** Verbose decision rationales increase token cost.

### OpenAI GPT-4o — "The Practical Planner"
**Strengths:** Clean task decomposition with duration estimates; good balance of depth and brevity.
**Weaknesses:** Less nuance in decision confidence and memory decay modeling.

### Gemini Flash 2.5 — "Not Scored (Simulation)"
**Note:** Ran in Simulation Mode. With a valid API key, Gemini would likely perform at the Analyze level based on its Chapter 1–4 performance patterns.

### DeepSeek V2 16B — "Not Scored (Simulation)"
**Note:** Ran in Simulation Mode. With Ollama running, DeepSeek would likely perform at the Apply/Understand level based on other chapter results.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Autonomous operations** | Claude Sonnet 4 | Best decision rationale with audit trails |
| **Task planning/decomposition** | OpenAI GPT-4o | Clean dependency graphs with duration estimates |
| **Strategy scoring** | Any (deterministic) | Output is identical — the scoring logic is rule-based |
| **Memory-augmented agents** | Claude Sonnet 4 | Best at synthesizing across memory types |
| **Local prototyping** | Ollama DeepSeek V2 | Zero cost for testing pipeline architecture |

---

*Analysis based on Chapter 5 notebook outputs executed April 2026. Claude and OpenAI ran in LIVE mode; Gemini and DeepSeek ran in SIMULATION mode. Deterministic strategy scoring is identical across all providers.*
