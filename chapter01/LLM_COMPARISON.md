# Chapter 1 — LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 1 Foundations of Agent Engineering tasks: cognitive loop implementation (perceive/reason/plan/act/learn), agent brain patterns, and multi-agent interaction paradigms.

---

## Agent Tasks in This Chapter

- **Cognitive Loop** — Five-phase cycle (perceive, reason, plan, act, learn) applied to a customer billing scenario
- **Agent Brain Patterns** — Reactive, deliberative, and hybrid architectures
- **Interaction Paradigms** — Five levels from direct LLM calls to multi-agent A2A messaging
- **Resilience Testing** — Graceful fallback under 100% failure conditions

## Scoring Dimensions

Each provider is rated 0–10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of JSON outputs and classification results |
| **Completeness** | Coverage of all cognitive loop phases and interaction levels |
| **Structure & Organization** | Quality of JSON formatting, field naming, hierarchical output |
| **Conciseness** | Information density without unnecessary padding |
| **Source Grounding** | Adherence to the chapter's prescribed architectures and patterns |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Acknowledgment of edge cases, confidence levels, reasoning factors |
| **Practical Utility** | How actionable the agent outputs would be in a real customer service system |

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

## Task 1: Cognitive Loop — Intent Classification & Planning

The LLM receives "I need help with my billing" and must classify intent, assess priority, and generate an action plan.

### Claude Sonnet 4

**Response characteristics:**
- Highly structured JSON with nested objects: `intent_classification` containing `primary_intent`, `intent_category`; separate `priority_assessment` with `priority_level`
- Included `reasoning` block with explicit `intent_factors` and `priority_factors` arrays
- Action plan produced a formal `plan_id` ("billing_assistance_standard_001") with detailed execution steps
- Execution output included quantitative details ("12-month billing history examined") and a courtesy credit offer
- Learning phase generated improvement recommendations with specific metrics

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | All classifications correct; appropriately identified billing_assistance intent |
| Completeness | 10 | Every cognitive loop phase produced rich, multi-field output |
| Structure & Organization | 10 | Deeply nested JSON with semantic field names, plan IDs, factor arrays |
| Conciseness | 7 | Verbose — many nested fields that could be simpler for a triage system |
| Source Grounding | 9 | Closely follows the chapter's pseudocode architecture |
| Bloom's Level | **5 — Evaluate** | Assessed priority factors, recommended improvements in learning phase |
| Nuance & Caveats | 9 | Included confidence scoring, multiple intent factors, improvement axes |
| Practical Utility | 9 | Production-ready structure; could drive a real ticketing system |

---

### Gemini Flash 2.5

**Response characteristics:**
- Clean JSON with `intent: "billing_assistance"` and `priority: "high"`
- Provided a detailed action plan with markdown-formatted steps including bold headers
- Execution narrative described account review, determination of validity, and adjustment execution
- Used structured bullet points for each plan phase

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Correct intent classification; rated priority as "high" (debatable for routine billing) |
| Completeness | 8 | All phases covered but with less depth in reasoning factors |
| Structure & Organization | 8 | Clean JSON and markdown, but flatter hierarchy than Claude |
| Conciseness | 9 | Tight responses with good information density |
| Source Grounding | 8 | Follows the cognitive loop pattern faithfully |
| Bloom's Level | **4 — Analyze** | Decomposed the problem into distinct phases with relationships |
| Nuance & Caveats | 6 | No explicit confidence scoring or factor enumeration |
| Practical Utility | 8 | Actionable plan; slight over-prioritization ("high") may cause false urgency |

---

### DeepSeek V2 16B (Local)

**Response characteristics:**
- Minimal JSON: `intent: "request_assistance"` and `priority: "medium"`
- Used generic intent label ("request_assistance") rather than domain-specific ("billing_assistance")
- Action plan produced a competent but generic customer service workflow
- Execution narrative was formulaic but complete

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct but generic — "request_assistance" is accurate but less specific |
| Completeness | 7 | All phases present but with minimal detail in reasoning |
| Structure & Organization | 6 | Valid JSON but flat structure, single-level fields |
| Conciseness | 9 | Very compact outputs |
| Source Grounding | 7 | Follows the pattern but doesn't leverage the chapter's domain vocabulary |
| Bloom's Level | **3 — Apply** | Correctly applied the cognitive loop pattern to the scenario |
| Nuance & Caveats | 4 | No confidence scoring, no factor enumeration, no caveats |
| Practical Utility | 6 | Functional but would need enrichment for production use |

---

### OpenAI GPT-4o

**Response characteristics:**
- Clean JSON: `intent: "request_assistance"`, `priority: "medium"`
- Action execution produced a natural, conversational customer response
- Plan steps were detailed with clear headers (Acknowledge, Investigate, Analyze, Execute, Communicate)
- Included a follow-up message demonstrating proactive customer care

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct classification; used generic "request_assistance" like DeepSeek |
| Completeness | 8 | All phases covered with good natural-language execution |
| Structure & Organization | 7 | Good markdown formatting but less structured JSON than Claude |
| Conciseness | 8 | Balanced — neither too sparse nor too verbose |
| Source Grounding | 8 | Follows the cognitive loop architecture faithfully |
| Bloom's Level | **4 — Analyze** | Decomposed into clear phases; follow-up shows evaluation of customer journey |
| Nuance & Caveats | 5 | No explicit confidence or factor enumeration; no self-assessment |
| Practical Utility | 8 | Natural customer-facing language; good for template generation |

---

## Overall Scorecard

| Dimension | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) | OpenAI GPT-4o |
|---|---|---|---|---|
| Factual Accuracy | **9.0** | **9.0** | **8.0** | **8.0** |
| Completeness | **10.0** | **8.0** | **7.0** | **8.0** |
| Structure & Organization | **10.0** | **8.0** | **6.0** | **7.0** |
| Conciseness | **7.0** | **9.0** | **9.0** | **8.0** |
| Source Grounding | **9.0** | **8.0** | **7.0** | **8.0** |
| Bloom's Taxonomy Level | **5.0 (Evaluate)** | **4.0 (Analyze)** | **3.0 (Apply)** | **4.0 (Analyze)** |
| Nuance & Caveats | **9.0** | **6.0** | **4.0** | **5.0** |
| Practical Utility | **9.0** | **8.0** | **6.0** | **8.0** |
| **WEIGHTED AVERAGE** | **8.5** | **7.5** | **6.3** | **7.0** |

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

**Claude Sonnet 4** reaches Level 5 (Evaluate) by explicitly assessing priority factors, generating improvement recommendations in the learning phase, and producing nested reasoning structures that judge the relative importance of different signals.

**Gemini Flash 2.5 and OpenAI GPT-4o** operate at Level 4 (Analyze) — they decompose the billing scenario into distinct phases and identify relationships between them, but don't assess or critique their own outputs.

**DeepSeek V2** stays at Level 3 (Apply) — correctly applying the cognitive loop pattern but without deeper analysis of why certain classifications or priorities were chosen.

---



---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  ────────────────────  ─────  ──────────────────────────────
  🥇 Claude Sonnet 4        8.5  █████████████████████████░░░░░
  🥈 Gemini Flash 2.5       7.5  ██████████████████████░░░░░░░░
  🥉 OpenAI GPT-4o          7.0  █████████████████████░░░░░░░░░
     DeepSeek V2 (Local)    6.3  ██████████████████░░░░░░░░░░░░
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  ─────  ────────────  ──────────────────────────
  L6 Create       │ 
  L5 Evaluate     ┃ C
  L4 Analyze      ┃ C G O
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
  Claude Sonnet 4          8.5       8.5    ▲+0.0
  Gemini Flash 2.5         7.5       7.2    ▲+0.3
  DeepSeek V2 (Local)      6.3       5.7    ▲+0.6
  OpenAI GPT-4o            7.0       7.4    ▼+0.4
```

---

## Winner: Claude Sonnet 4

| | |
|---|---|
| **Chapter 1 Winner** | **Claude Sonnet 4** |
| **Score** | **8.5 / 10** |
| **Bloom's Level** | **Level 5 — Evaluate** |

**Why Claude Sonnet 4 wins this chapter:**
- Highest weighted average across all 8 scoring dimensions
- Bloom's Level 5 (Evaluate) — the deepest cognitive sophistication
- 1.0-point lead over runner-up Gemini Flash 2.5 (7.5)

**Runner-up:** Gemini Flash 2.5 (7.5/10)

**Third place:** OpenAI GPT-4o (7.0/10)

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality | Claude Sonnet 4 | Highest scores across all dimensions |
| Cost-efficient production | Gemini Flash 2.5 | Best quality-per-dollar ratio |
| Air-gapped / private data | DeepSeek V2 (Local) | Only option with zero cloud dependency |
| Rapid prototyping | DeepSeek V2 (Local) | No API key, instant iteration, zero cost |


## Provider Profiles for This Chapter

### Claude Sonnet 4 — "The Architect"

**Strengths:**
- Deepest JSON structures with semantic field naming (plan_id, intent_factors, priority_factors)
- Only provider to include explicit reasoning chains and confidence metadata
- Learning phase produced actionable improvement recommendations
- Best at producing machine-parseable output for downstream systems

**Weaknesses:**
- Most verbose output — may be over-engineered for simple triage
- Higher token consumption per cognitive loop iteration

---

### Gemini Flash 2.5 — "The Pragmatist"

**Strengths:**
- Clean, actionable outputs with good balance of structure and brevity
- Strong domain-specific intent classification ("billing_assistance")
- Fast execution with lowest token cost

**Weaknesses:**
- Over-prioritized a routine request as "high" priority
- Less depth in reasoning justification

---

### DeepSeek V2 16B — "The Minimalist"

**Strengths:**
- Runs entirely locally with zero cloud dependency
- Produces valid, parseable JSON consistently
- Extremely concise — lowest token overhead

**Weaknesses:**
- Generic intent labels miss domain-specific vocabulary
- No confidence scoring or reasoning factors
- Minimal structure limits downstream utility

---

### OpenAI GPT-4o — "The Communicator"

**Strengths:**
- Most natural customer-facing language in execution phase
- Proactive follow-up demonstrates customer journey awareness
- Good balance of structure and readability

**Weaknesses:**
- Generic intent classification like DeepSeek
- Less structured JSON compared to Claude

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Production cognitive loop** | Claude Sonnet 4 | Deepest reasoning structures, machine-parseable output |
| **Customer-facing agent** | OpenAI GPT-4o | Most natural conversational tone in execution phase |
| **High-throughput triage** | Gemini Flash 2.5 | Best speed/cost with strong domain classification |
| **Offline development** | Ollama DeepSeek V2 | Zero cost, valid JSON, privacy-preserving |
| **Multi-agent orchestration** | Claude Sonnet 4 | Richest metadata for inter-agent message passing |

---

*Analysis based on Chapter 1 notebook outputs executed April 2026. All four providers ran in LIVE mode. Scores reflect performance on cognitive loop, brain pattern, and interaction paradigm tasks.*
