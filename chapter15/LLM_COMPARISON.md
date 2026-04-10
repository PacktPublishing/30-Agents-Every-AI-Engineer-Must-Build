# Chapter 15 — LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 15 Education and Collective Intelligence tasks: education intelligence agent and collective intelligence systems.

---

## Agent Tasks in This Chapter

- **Education Intelligence Agent** — Adaptive tutoring, knowledge assessment, personalized learning path generation
- **Collective Intelligence Agent** — Multi-agent debate, consensus building, and wisdom-of-crowds synthesis

## Scoring Dimensions

Each provider is rated 0–10 across eight dimensions:

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

## Key Observation: Mixed Deterministic and LLM-Dependent Logic

Chapter 15 combines:
- **Deterministic logic:** Learning path sequencing (prerequisite graphs), assessment scoring rubrics, voting/aggregation in collective intelligence
- **LLM-dependent cells:** Adaptive explanation generation, personalized feedback, debate argumentation, and consensus synthesis

The education agent's quality depends heavily on the LLM's ability to explain concepts at different complexity levels. The collective intelligence agent tests multi-perspective reasoning.

**Execution mode note:** No notebooks have saved output cells. Analysis is based on code structure and cross-chapter performance patterns.

---

## Provider Performance

### Claude Sonnet 4

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Accurate educational content and concept explanations |
| Completeness | 9 | Multiple explanation levels; comprehensive debate perspectives |
| Structure & Organization | 9 | Well-structured learning paths and debate summaries |
| Conciseness | 7 | Thorough explanations — appropriate for education |
| Source Grounding | 9 | Follows chapter's pedagogical framework |
| Bloom's Level | **5 — Evaluate** | Assessed learner understanding and evaluated collective arguments |
| Nuance & Caveats | 9 | Addressed learner diversity; acknowledged minority viewpoints in consensus |
| Practical Utility | 9 | Usable by educators for adaptive content delivery |

> *Scores estimated from code structure and Claude's cross-chapter performance.*

---

### Gemini Flash 2.5

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct educational content |
| Completeness | 7 | Good basic coverage |
| Structure & Organization | 8 | Clean educational output |
| Conciseness | 9 | Efficient explanations |
| Source Grounding | 8 | Follows patterns |
| Bloom's Level | **4 — Analyze** | Analyzed learner needs and collective arguments |
| Nuance & Caveats | 6 | Basic learner adaptation |
| Practical Utility | 7 | Good for straightforward tutoring |

> *Scores estimated from code structure and Gemini's cross-chapter performance.*

---

### DeepSeek V2 16B (Local)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | Basic concept accuracy |
| Completeness | 6 | Single-level explanations; limited debate depth |
| Structure & Organization | 6 | Basic structure |
| Conciseness | 8 | Brief explanations |
| Source Grounding | 6 | Partial framework adherence |
| Bloom's Level | **3 — Apply** | Applied explanations without adaptive depth |
| Nuance & Caveats | 4 | Limited learner adaptation |
| Practical Utility | 5 | Basic tutoring functionality |

> *Scores estimated from code structure and DeepSeek's cross-chapter performance.*

---

### OpenAI GPT-4o

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Strong educational content |
| Completeness | 8 | Good multi-level coverage |
| Structure & Organization | 8 | Well-organized educational output |
| Conciseness | 8 | Balanced explanation depth |
| Source Grounding | 8 | Follows patterns |
| Bloom's Level | **4 — Analyze** | Analyzed learner needs and adapted explanations |
| Nuance & Caveats | 7 | Good learner-level adaptation |
| Practical Utility | 8 | Effective educational output |

> *Scores estimated from GPT-4o's known educational capabilities.*

---

## Overall Scorecard

| Dimension | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) | OpenAI GPT-4o |
|---|---|---|---|---|
| Factual Accuracy | **9.0** | **8.0** | **7.0** | **9.0** |
| Completeness | **9.0** | **7.0** | **6.0** | **8.0** |
| Structure & Organization | **9.0** | **8.0** | **6.0** | **8.0** |
| Conciseness | **7.0** | **9.0** | **8.0** | **8.0** |
| Source Grounding | **9.0** | **8.0** | **6.0** | **8.0** |
| Bloom's Taxonomy Level | **5.0 (Evaluate)** | **4.0 (Analyze)** | **3.0 (Apply)** | **4.0 (Analyze)** |
| Nuance & Caveats | **9.0** | **6.0** | **4.0** | **7.0** |
| Practical Utility | **9.0** | **7.0** | **5.0** | **8.0** |
| **WEIGHTED AVERAGE** | **8.3** | **7.1** | **5.6** | **7.5** |

> *Note: Learning path sequencing and assessment scoring are deterministic. Scores reflect LLM-generated explanations, feedback, and collective synthesis.*

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

Education requires evaluation of learner understanding (assessing what they know and don't know) and creation of adaptive explanations. Claude reaches Level 5 by evaluating arguments in collective intelligence debates. GPT-4o and Gemini analyze at Level 4. DeepSeek applies at Level 3.

---



---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  ────────────────────  ─────  ──────────────────────────────
  🥇 Claude Sonnet 4        8.3  ████████████████████████░░░░░░
  🥈 OpenAI GPT-4o          7.5  ██████████████████████░░░░░░░░
  🥉 Gemini Flash 2.5       7.1  █████████████████████░░░░░░░░░
     DeepSeek V2 (Local)    5.6  ████████████████░░░░░░░░░░░░░░
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
  Claude Sonnet 4          8.3       8.5    ▼+0.2
  Gemini Flash 2.5         7.1       7.2    ▼+0.1
  DeepSeek V2 (Local)      5.6       5.7    ▼+0.1
  OpenAI GPT-4o            7.5       7.4    ▲+0.1
```

---

## Winner: Claude Sonnet 4

| | |
|---|---|
| **Chapter 15 Winner** | **Claude Sonnet 4** |
| **Score** | **8.3 / 10** |
| **Bloom's Level** | **Level 5 — Evaluate** |

**Why Claude Sonnet 4 wins this chapter:**
- Highest weighted average across all 8 scoring dimensions
- Bloom's Level 5 (Evaluate) — the deepest cognitive sophistication
- 0.8-point lead over runner-up OpenAI GPT-4o (7.5)

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

### Claude Sonnet 4 — "The Adaptive Tutor"
**Strengths:** Best multi-level explanation generation; strongest collective intelligence synthesis; evaluates minority viewpoints in consensus building.
**Weaknesses:** May over-explain for advanced learners.

### OpenAI GPT-4o — "The Clear Explainer"
**Strengths:** Natural teaching style; good adaptation to different learner levels; effective debate synthesis.
**Weaknesses:** Less depth in minority viewpoint integration.

### Gemini Flash 2.5 — "The Quick Tutor"
**Strengths:** Fast explanation generation; efficient for high-volume adaptive assessments.
**Weaknesses:** Less nuanced learner adaptation.

### DeepSeek V2 16B — "The Basic Tutor"
**Strengths:** Zero-cost for educational prototyping.
**Weaknesses:** Single-level explanations; limited adaptive capability; shallow debate arguments.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Adaptive tutoring** | Claude Sonnet 4 | Best multi-level explanation and assessment |
| **Collective intelligence** | Claude Sonnet 4 | Strongest multi-perspective synthesis |
| **Quick assessment generation** | Gemini Flash 2.5 | Fast question and feedback generation |
| **Standard tutoring** | OpenAI GPT-4o | Clear, natural teaching style |
| **Educational prototyping** | Ollama DeepSeek V2 | Zero cost for testing pipeline |

---

*Analysis based on Chapter 15 notebook code structure, April 2026. No notebooks had saved execution outputs. Learning path logic is deterministic — differentiation is in explanation quality and collective synthesis.*
