# Chapter 15 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of two LLM providers running the Chapter 15 Education Intelligence and Collective Intelligence tasks: adaptive tutoring with Bayesian Knowledge Tracing and multi-agent consensus building.

---

## Agent Tasks in This Chapter

- **Education Intelligence Agent** -- POMDP-based adaptive tutoring: knowledge graph curriculum, ZPD-aligned objective selection, IRT 2PL placement testing, Bayesian Knowledge Tracing, SM-2 spaced repetition, and two-stage misconception detection with pedagogical feedback
- **Collective Intelligence Agent** -- Multi-agent collaboration: CollaborativeAgent propose/critique pathways, ConsensusEngine with expertise-weighted scoring and adversarial critic rotation

## Scoring Dimensions

Each provider is rated 0--10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of educational content and assessment items |
| **Completeness** | Coverage of learning objectives, assessment dimensions, and collective perspectives |
| **Structure & Organization** | Quality of learning paths, assessment rubrics, and debate synthesis |
| **Conciseness** | Appropriate depth for educational communication |
| **Source Grounding** | Adherence to the chapter's pedagogical and collective intelligence frameworks |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Handling of learner diversity, knowledge gaps, and minority viewpoints |
| **Practical Utility** | How useful outputs would be for educators or organizational decision-making |

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

## Key Observation: One Live Provider, One Simulation

This chapter has a genuinely meaningful comparison because the two active providers ran in **different modes**:

- **OpenAI GPT-4o**: Ran in **MockLLM (Simulation Mode)** -- 17 output cells. All LLM calls routed through pre-authored mock responses.
- **Gemini Flash 2.5**: Ran in **LiveLLM mode** with actual Gemini 2.5 Flash API calls -- 66 output cells. Every feedback generation, proposal, evaluation, and consensus synthesis was produced by real Gemini API calls.
- **Claude Sonnet 4**: 0 output cells (notebook not executed)
- **DeepSeek V2 16B**: 0 output cells (notebook not executed)

This creates an unusual comparison: the OpenAI column reflects carefully curated mock responses (representing an idealized baseline), while the Gemini column shows actual live LLM behavior with real latency, occasional parsing challenges, and genuine generative output.

---

## Provider Performance

### OpenAI GPT-4o (MockLLM / Simulation Mode)

**Response characteristics:**
- Feedback: "Great work on the overall structure of your solution! Your use of a for loop to iterate through the list is correct, and..." (pre-authored mock, 1345 chars)
- Evaluation scores returned full 4-dimension breakdown: `{correctness: 7.0, completeness: 6.0, feasibility: 8.0, overall: 6.5}`
- Consensus: converged in **1 round**, score **6.50**
- All timestamps identical (11:58:46) -- zero latency, pure simulation

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Mock responses are pre-authored and factually curated |
| Completeness | 8 | 4-dimension evaluation scores; complete pedagogical contract followed |
| Structure & Organization | 8 | Flowing narrative feedback; structured evaluation with labeled dimensions |
| Conciseness | 8 | Well-calibrated length for educational feedback |
| Source Grounding | 9 | Mock responses explicitly keyed to chapter concepts (feedback_generator, propose_pedagogy) |
| Bloom's Level | **4 -- Analyze** | Feedback identifies specific code elements and analyzes error patterns |
| Nuance & Caveats | 7 | Acknowledges correct elements before addressing errors; follows 4-part pedagogical contract |
| Practical Utility | 7 | Good reference implementation; simulation outputs are curated but static |

> *Note: Scores reflect the quality of the pre-authored MockLLM responses, not actual GPT-4o API output.*

---

### Gemini Flash 2.5 (Live API)

**Response characteristics:**
- Feedback: "Great start! You've correctly identified several key components for this problem:\n\n1. You've initialized `total` to `0`..." (live Gemini output)
- Evaluation scores returned only overall: `{overall: 5.0}` (Gemini did not return the expected multi-dimension JSON structure)
- Consensus: converged in **3 rounds**, score **6.11**
- Proposals took ~20 seconds each; full consensus pipeline ran ~10 minutes (18:09-18:19)
- 66 output cells -- significantly more verbose execution trace due to real API round-trips

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Live Gemini feedback correctly identifies code elements (`total` initialization, `for` loop structure) |
| Completeness | 6 | Evaluation returned only `overall` score, not the 4-dimension breakdown; consensus required 3 rounds to converge |
| Structure & Organization | 7 | Feedback uses numbered list format (good for students); but evaluation parsing lost dimension detail |
| Conciseness | 7 | Numbered list is pedagogically clear but truncated at 120 chars in preview |
| Source Grounding | 7 | Follows the feedback generator prompt structure but does not explicitly reference chapter concepts |
| Bloom's Level | **4 -- Analyze** | Identifies specific code components and analyzes what the student did correctly before addressing errors |
| Nuance & Caveats | 7 | Acknowledges correct elements; uses numbered decomposition to guide discovery |
| Practical Utility | 8 | Live output demonstrates real deployment behavior; consensus took 3 rounds showing genuine deliberation |

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o (Mock) | Gemini Flash 2.5 (Live) |
|---|---|---|
| Factual Accuracy | **8.0** | **8.0** |
| Completeness | **8.0** | **6.0** |
| Structure & Organization | **8.0** | **7.0** |
| Conciseness | **8.0** | **7.0** |
| Source Grounding | **9.0** | **7.0** |
| Bloom's Taxonomy Level | **4.0 (Analyze)** | **4.0 (Analyze)** |
| Nuance & Caveats | **7.0** | **7.0** |
| Practical Utility | **7.0** | **8.0** |
| **WEIGHTED AVERAGE** | **7.4** | **6.8** |

> *Critical caveat: OpenAI scores reflect curated mock responses (idealized baseline), not actual GPT-4o API output. Gemini scores reflect actual live API behavior. A fair comparison would require both providers in live mode.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     | oooooooooooo OpenAI (mock), Gemini (live)
Level 3: Apply       |
Level 2: Understand  |
Level 1: Remember    |
```

Both providers reach Level 4 (Analyze). The feedback generators in both cases decompose student submissions into correct and incorrect elements, then analyze the specific error pattern. Neither reaches Level 5 because neither evaluates competing pedagogical strategies or assesses which explanation approach would be most effective for this particular learner.

---

## Head-to-Head: Key Differences

| Dimension | OpenAI GPT-4o (Mock) | Gemini Flash 2.5 (Live) |
|---|---|---|
| **Mode** | Simulation (MockLLM) | Live API (Gemini 2.5 Flash) |
| **Feedback style** | Flowing narrative paragraph | Numbered list with code references |
| **Evaluation detail** | 4-dimension scores (correctness, completeness, feasibility, overall) | Single overall score only |
| **Consensus rounds** | 1 round (deterministic) | 3 rounds (genuine deliberation) |
| **Consensus score** | 6.50 | 6.11 |
| **Latency** | 0 ms (simulation) | ~20 sec per proposal |
| **Output cells** | 17 | 66 |

**Gemini's strength:** Actual deployment behavior -- the 3-round consensus convergence shows genuine multi-agent deliberation with real critique-revision cycles. The numbered feedback format is arguably better for students learning to code.

**Gemini's weakness:** Evaluation parsing returned only an overall score, losing the dimensional breakdown that enables finer-grained pedagogical adaptation.

**OpenAI mock's strength:** Curated responses demonstrate ideal behavior -- complete 4-dimension evaluations, immediate convergence.

**OpenAI mock's weakness:** Being a simulation, it does not reveal actual GPT-4o behavior, latency, or failure modes.

---

## Visual Summary

### Overall Score Comparison

```
  Provider                  Score  Visual
  ------------------------  -----  ------------------------------
  OpenAI GPT-4o (Mock)       7.4  ██████████████████████░░░░░░░░░
  Gemini Flash 2.5 (Live)    6.8  ████████████████████░░░░░░░░░░░
  Claude Sonnet 4            N/A  (no saved outputs)
  DeepSeek V2 (Local)        N/A  (no saved outputs)
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     |
  L4 Analyze      | O G
  L3 Apply        | O G
  L2 Understand   | O G
  L1 Remember     | O G
```

Legend: **O** = OpenAI GPT-4o (mock), **G** = Gemini Flash 2.5 (live)

---

## Winner: OpenAI GPT-4o (Mock) -- with caveats

| | |
|---|---|
| **Chapter 15 Winner** | **OpenAI GPT-4o (Mock)** |
| **Score** | **7.4 / 10** |
| **Bloom's Level** | **Level 4 -- Analyze** |

**Why OpenAI wins on paper:**
- Higher weighted average (7.4 vs 6.8) driven by completeness and structure scores
- 4-dimension evaluation scores vs Gemini's single-dimension
- Faster consensus convergence (1 round vs 3)

**Why this result is unreliable:**
- OpenAI ran in MockLLM mode with pre-authored responses -- these are curated ideal outputs, not actual GPT-4o behavior
- Gemini ran in LiveLLM mode with actual API calls -- its scores reflect real-world performance including parsing challenges and multi-round deliberation
- A fair comparison would require both providers in live mode

**Gemini Flash 2.5 deserves credit for:**
- Being the only provider with actual live API outputs in this chapter
- Demonstrating genuine multi-agent consensus convergence (3 rounds of propose-evaluate-critique)
- Producing pedagogically sound feedback with specific code references

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality (actual API) | Gemini Flash 2.5 | Only provider with live API outputs for this chapter |
| Curated reference outputs | OpenAI (mock) | Pre-authored responses demonstrate ideal behavior |
| Air-gapped / private data | DeepSeek V2 (Local) | Zero cloud dependency (no saved outputs for this chapter) |
| Rapid prototyping | Any mock mode | Zero cost, instant iteration |

## Provider Profiles for This Chapter

### OpenAI GPT-4o -- "The Curated Reference"
**Strengths:** Complete 4-dimension evaluations; clean pedagogical contract adherence; fast (simulated) convergence.
**Weaknesses:** Mock mode -- does not demonstrate actual GPT-4o API behavior or reveal real failure modes.

### Gemini Flash 2.5 -- "The Live Deployment"
**Strengths:** Real API outputs; genuine multi-round consensus; pedagogically sound numbered-list feedback; specific code-level references in student feedback.
**Weaknesses:** Evaluation parsing returns only overall score (lost dimensional detail); higher latency (~20s per proposal); consensus score lower than mock baseline (6.11 vs 6.50).

### Claude Sonnet 4 -- Not Evaluated
**Status:** 0 output cells saved. Notebook was not executed.

### DeepSeek V2 16B -- Not Evaluated
**Status:** 0 output cells saved. Notebook was not executed.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Adaptive tutoring (production)** | Gemini Flash 2.5 | Only provider with demonstrated live API output for educational feedback |
| **Collective intelligence** | Gemini Flash 2.5 | Genuine 3-round consensus with adversarial critique |
| **Reference implementation** | OpenAI (mock) | Curated responses demonstrate ideal pipeline behavior |
| **Quick assessment generation** | Gemini Flash 2.5 | Fast API calls (~20s) for real-time tutoring |
| **Educational prototyping** | Any mock mode | Zero cost for testing pipeline architecture |

---

*Analysis based on Chapter 15 notebook outputs executed April 2026. OpenAI ran in MockLLM (Simulation Mode) with pre-authored responses. Gemini ran in LiveLLM mode with actual Gemini 2.5 Flash API calls. Learning path logic, BKT updates, and spaced repetition scheduling are deterministic -- differentiation is in feedback generation, proposal content, and consensus synthesis.*
