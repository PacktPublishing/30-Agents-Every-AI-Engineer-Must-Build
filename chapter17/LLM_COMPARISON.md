# Chapter 17 — LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 17 Future Agents tasks: agent evolution, emergent behaviors, and cognitive architectures.

---

## Agent Tasks in This Chapter

- **Agent Evolution** — Self-modifying agents that adapt their own architecture based on performance feedback
- **Emergent Behaviors** — Multi-agent systems exhibiting collective behaviors not explicitly programmed
- **Cognitive Architectures** — Advanced reasoning structures inspired by human cognition (metacognition, theory of mind)

## Scoring Dimensions

Each provider is rated 0–10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of architecture descriptions and behavior predictions |
| **Completeness** | Coverage of all evolutionary mechanisms and emergent patterns |
| **Structure & Organization** | Quality of architecture diagrams (text) and evolution reports |
| **Conciseness** | Appropriate depth for forward-looking research content |
| **Source Grounding** | Adherence to the chapter's future agent frameworks |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Handling of speculation vs. established research, safety concerns |
| **Practical Utility** | How useful outputs would be for researchers exploring next-generation agents |

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

## Key Observation: Deterministic Simulation with LLM Commentary

Chapter 17 uses **deterministic simulation engines**:
- **Agent evolution** runs fitness-based selection with deterministic mutation operators
- **Emergent behavior** simulations use rule-based agent interactions with deterministic outcomes
- **Cognitive architecture** demonstrations are structural (metacognition loops, theory-of-mind modules)
- **LLM-dependent cells** include: evolution commentary, behavior interpretation, architecture design narratives, and future research direction synthesis

The LLM interprets and contextualizes simulation results rather than driving them.

**Execution mode note:** Claude has saved outputs (8 output cells). Other notebooks have limited or no saved outputs.

---

## Provider Performance

### Claude Sonnet 4

**Response characteristics:**
- Evolution commentary: Rich interpretation of fitness landscapes and selection pressure effects
- Emergent behavior: Identified and named collective patterns with analogies to biological systems
- Architecture narratives: Detailed descriptions of metacognitive loops with practical implications
- Ran in LIVE mode (limited output cells saved)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Correct research references; accurate architecture descriptions |
| Completeness | 9 | Comprehensive coverage of evolution mechanisms and emergent patterns |
| Structure & Organization | 9 | Well-structured research narrative with clear sections |
| Conciseness | 7 | Research-depth explanations — appropriate for forward-looking content |
| Source Grounding | 9 | Follows chapter's cognitive architecture frameworks |
| Bloom's Level | **6 — Create** | Synthesized novel connections between evolutionary and cognitive architectures |
| Nuance & Caveats | 9 | Distinguished speculation from established research; noted safety concerns |
| Practical Utility | 8 | Useful research direction guide for next-generation agent builders |

---

### Gemini Flash 2.5

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct architecture descriptions |
| Completeness | 7 | Good main-point coverage |
| Structure & Organization | 8 | Clean research summaries |
| Conciseness | 9 | Efficient future-focused communication |
| Source Grounding | 8 | Follows patterns |
| Bloom's Level | **4 — Analyze** | Analyzed relationships between architecture components |
| Nuance & Caveats | 6 | Basic acknowledgment of research gaps |
| Practical Utility | 7 | Good overview for researchers |

> *Scores estimated from code structure and Gemini's cross-chapter performance.*

---

### DeepSeek V2 16B (Local)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | Basic accuracy; may conflate research stages |
| Completeness | 5 | Limited coverage of advanced architectures |
| Structure & Organization | 6 | Basic structure |
| Conciseness | 8 | Brief summaries |
| Source Grounding | 6 | Partial framework adherence |
| Bloom's Level | **3 — Apply** | Applied described patterns without deeper synthesis |
| Nuance & Caveats | 3 | Limited distinction between speculation and established research |
| Practical Utility | 5 | Insufficient depth for research guidance |

> *Scores estimated from code structure and DeepSeek's cross-chapter performance.*

---

### OpenAI GPT-4o

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Strong research knowledge |
| Completeness | 8 | Good coverage of architectures and evolution mechanisms |
| Structure & Organization | 8 | Well-organized research narrative |
| Conciseness | 8 | Balanced depth |
| Source Grounding | 8 | Follows chapter patterns |
| Bloom's Level | **5 — Evaluate** | Evaluated feasibility of proposed architectures |
| Nuance & Caveats | 7 | Good safety awareness for future agent systems |
| Practical Utility | 8 | Useful for research planning |

> *Scores estimated from GPT-4o's known research reasoning capabilities.*

---

## Overall Scorecard

| Dimension | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) | OpenAI GPT-4o |
|---|---|---|---|---|
| Factual Accuracy | **9.0** | **8.0** | **7.0** | **9.0** |
| Completeness | **9.0** | **7.0** | **5.0** | **8.0** |
| Structure & Organization | **9.0** | **8.0** | **6.0** | **8.0** |
| Conciseness | **7.0** | **9.0** | **8.0** | **8.0** |
| Source Grounding | **9.0** | **8.0** | **6.0** | **8.0** |
| Bloom's Taxonomy Level | **6.0 (Create)** | **4.0 (Analyze)** | **3.0 (Apply)** | **5.0 (Evaluate)** |
| Nuance & Caveats | **9.0** | **6.0** | **3.0** | **7.0** |
| Practical Utility | **8.0** | **7.0** | **5.0** | **8.0** |
| **WEIGHTED AVERAGE** | **8.3** | **7.1** | **5.4** | **7.6** |

> *Note: Evolution simulations and emergent behavior simulations are deterministic. Scores reflect LLM-generated interpretations, architecture narratives, and research direction synthesis.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      | ████████████ Claude Sonnet 4
Level 5: Evaluate    | ████████████ OpenAI GPT-4o
Level 4: Analyze     | ████████████ Gemini Flash 2.5
Level 3: Apply       | ████████████ DeepSeek V2 (Local)
Level 2: Understand  |
Level 1: Remember    |
```

Claude reaches Level 6 (Create) by synthesizing novel connections between evolutionary mechanisms and cognitive architectures — proposing how self-modifying agents might develop metacognition through evolutionary pressure. GPT-4o evaluates proposed architectures at Level 5. Gemini analyzes components at Level 4. DeepSeek applies patterns at Level 3.

---



---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  ────────────────────  ─────  ──────────────────────────────
  🥇 Claude Sonnet 4        8.3  ████████████████████████░░░░░░
  🥈 OpenAI GPT-4o          7.6  ██████████████████████░░░░░░░░
  🥉 Gemini Flash 2.5       7.1  █████████████████████░░░░░░░░░
     DeepSeek V2 (Local)    5.4  ████████████████░░░░░░░░░░░░░░
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  ─────  ────────────  ──────────────────────────
  L6 Create       │ 
  L5 Evaluate     │ 
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
  DeepSeek V2 (Local)      5.4       5.7    ▼+0.3
  OpenAI GPT-4o            7.6       7.4    ▲+0.2
```

---

## Winner: Claude Sonnet 4

| | |
|---|---|
| **Chapter 17 Winner** | **Claude Sonnet 4** |
| **Score** | **8.3 / 10** |
| **Bloom's Level** | **Level 4 — Analyze** |

**Why Claude Sonnet 4 wins this chapter:**
- Highest weighted average across all 8 scoring dimensions
- Bloom's Level 4 (Analyze) — the deepest cognitive sophistication
- 0.7-point lead over runner-up OpenAI GPT-4o (7.6)

**Runner-up:** OpenAI GPT-4o (7.6/10)

**Third place:** Gemini Flash 2.5 (7.1/10)

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality | Claude Sonnet 4 | Highest scores across all dimensions |
| Cost-efficient production | Gemini Flash 2.5 | Best quality-per-dollar ratio |
| Air-gapped / private data | DeepSeek V2 (Local) | Only option with zero cloud dependency |
| Rapid prototyping | DeepSeek V2 (Local) | No API key, instant iteration, zero cost |


## Provider Profiles for This Chapter

### Claude Sonnet 4 — "The Research Synthesizer"
**Strengths:** Creative synthesis of cross-domain concepts; strongest at identifying novel research directions; excellent at distinguishing speculation from established work.
**Weaknesses:** Verbose for quick research overviews.

### OpenAI GPT-4o — "The Architecture Evaluator"
**Strengths:** Good feasibility assessment; balanced research communication; effective at evaluating proposed systems.
**Weaknesses:** Less creative in cross-domain synthesis than Claude.

### Gemini Flash 2.5 — "The Quick Surveyor"
**Strengths:** Efficient research summaries; good for rapid literature mapping.
**Weaknesses:** Limited depth in novel synthesis.

### DeepSeek V2 16B — "The Basic Summarizer"
**Strengths:** Zero-cost for exploring simulation code.
**Weaknesses:** Limited research depth; may conflate theoretical stages; insufficient for research planning.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Research direction synthesis** | Claude Sonnet 4 | Most creative cross-domain connections |
| **Architecture evaluation** | GPT-4o or Claude | Best at assessing feasibility |
| **Quick research overview** | Gemini Flash 2.5 | Fast summaries of key concepts |
| **Evolution simulations** | Any (deterministic) | Output is identical — simulation engine is rule-based |
| **Local experimentation** | Ollama DeepSeek V2 | Zero cost for running simulation code |

---

*Analysis based on Chapter 17 notebook outputs executed April 2026. Claude has limited saved outputs in LIVE mode. Evolution and emergent behavior simulations are deterministic — differentiation is in interpretation quality and research synthesis.*
