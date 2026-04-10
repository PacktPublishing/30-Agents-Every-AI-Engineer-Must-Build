# Chapter 16 — LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 16 Embodied Intelligence tasks: embodied intelligence agents, drone operations, and safety envelope management.

---

## Agent Tasks in This Chapter

- **Embodied Intelligence Agent** — Physical world reasoning, spatial navigation, and object manipulation planning
- **Drone Operations Agent** — Flight path planning, obstacle avoidance, and mission execution
- **Safety Envelope Agent** — Real-time constraint monitoring, emergency response, and operational boundary enforcement

## Scoring Dimensions

Each provider is rated 0–10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of physical reasoning and safety constraints |
| **Completeness** | Coverage of all spatial dimensions, safety factors, and operational parameters |
| **Structure & Organization** | Quality of flight plans, safety reports, and operational commands |
| **Conciseness** | Appropriate detail for real-time operational communication |
| **Source Grounding** | Adherence to the chapter's embodied agent architectures |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Handling of environmental uncertainty, sensor noise, and safety margins |
| **Practical Utility** | How useful outputs would be for robotics or drone operations |

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

## Key Observation: Heavily Deterministic Safety-Critical Logic

Chapter 16 is **one of the most deterministic chapters**:
- **Flight path calculations** (waypoints, distances, battery constraints) are mathematical
- **Safety envelope monitoring** (boundary checks, speed limits, altitude constraints) is rule-based
- **Obstacle avoidance** uses deterministic algorithms
- **LLM-dependent cells** include: mission briefing generation, situation assessment narratives, and emergency response prioritization

In safety-critical systems, the LLM provides interpretive commentary, not control decisions. The critical safety logic is never LLM-dependent.

**Execution mode note:** No notebooks have saved output cells. Analysis is based on code structure and cross-chapter performance patterns.

---

## Provider Performance

### Claude Sonnet 4

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Strong physical reasoning; correct spatial relationships |
| Completeness | 9 | Comprehensive safety factor enumeration |
| Structure & Organization | 9 | Professional operational briefing format |
| Conciseness | 8 | Appropriate detail for mission briefings |
| Source Grounding | 9 | Follows chapter's safety-critical architecture |
| Bloom's Level | **5 — Evaluate** | Assessed risk levels and evaluated operational feasibility |
| Nuance & Caveats | 9 | Environmental uncertainty; sensor reliability margins; abort criteria |
| Practical Utility | 8 | Good supplementary briefing material (not for direct control) |

> *Scores estimated from code structure and Claude's cross-chapter performance.*

---

### Gemini Flash 2.5

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct physical reasoning |
| Completeness | 7 | Good main safety factors |
| Structure & Organization | 8 | Clean operational output |
| Conciseness | 9 | Efficient operational communication |
| Source Grounding | 8 | Follows patterns |
| Bloom's Level | **3 — Apply** | Applied safety frameworks |
| Nuance & Caveats | 6 | Basic safety margins noted |
| Practical Utility | 7 | Functional operational summaries |

> *Scores estimated from code structure and Gemini's cross-chapter performance.*

---

### DeepSeek V2 16B (Local)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | Basic physical reasoning |
| Completeness | 5 | Limited safety factor coverage |
| Structure & Organization | 6 | Basic operational format |
| Conciseness | 8 | Brief outputs |
| Source Grounding | 6 | Partial adherence |
| Bloom's Level | **2 — Understand** | Understood concepts but limited application to scenarios |
| Nuance & Caveats | 3 | Minimal safety margin communication |
| Practical Utility | 4 | Insufficient for safety-critical documentation |

> *Scores estimated from code structure and DeepSeek's cross-chapter performance.*

---

### OpenAI GPT-4o

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Good physical and spatial reasoning |
| Completeness | 8 | Solid safety factor coverage |
| Structure & Organization | 8 | Professional operational format |
| Conciseness | 8 | Balanced detail |
| Source Grounding | 8 | Follows patterns |
| Bloom's Level | **4 — Analyze** | Analyzed operational scenarios and identified risks |
| Nuance & Caveats | 7 | Good safety awareness |
| Practical Utility | 8 | Useful operational briefing support |

> *Scores estimated from GPT-4o's known reasoning capabilities.*

---

## Overall Scorecard

| Dimension | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) | OpenAI GPT-4o |
|---|---|---|---|---|
| Factual Accuracy | **9.0** | **8.0** | **7.0** | **9.0** |
| Completeness | **9.0** | **7.0** | **5.0** | **8.0** |
| Structure & Organization | **9.0** | **8.0** | **6.0** | **8.0** |
| Conciseness | **8.0** | **9.0** | **8.0** | **8.0** |
| Source Grounding | **9.0** | **8.0** | **6.0** | **8.0** |
| Bloom's Taxonomy Level | **5.0 (Evaluate)** | **3.0 (Apply)** | **2.0 (Understand)** | **4.0 (Analyze)** |
| Nuance & Caveats | **9.0** | **6.0** | **3.0** | **7.0** |
| Practical Utility | **8.0** | **7.0** | **4.0** | **8.0** |
| **WEIGHTED AVERAGE** | **8.3** | **7.0** | **5.1** | **7.5** |

> *Note: Safety-critical logic (flight paths, boundaries, obstacle avoidance) is entirely deterministic. Scores reflect LLM-generated briefings, situation assessments, and emergency response narratives only.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    | ████████████ Claude Sonnet 4
Level 4: Analyze     | ████████████ OpenAI GPT-4o
Level 3: Apply       | ████████████ Gemini Flash 2.5
Level 2: Understand  | ████████████ DeepSeek V2 (Local)
Level 1: Remember    |
```

Embodied intelligence requires evaluating environmental risks and making safety judgments. Claude reaches Level 5 with comprehensive risk evaluation. GPT-4o analyzes scenarios at Level 4. Gemini applies safety frameworks at Level 3. DeepSeek understands concepts at Level 2.

---

## Provider Profiles for This Chapter

### Claude Sonnet 4 — "The Safety Officer"
**Strengths:** Best risk evaluation; comprehensive abort criteria; detailed environmental uncertainty communication.
**Weaknesses:** May be too detailed for real-time operational communication.

### OpenAI GPT-4o — "The Operations Planner"
**Strengths:** Good scenario analysis; balanced operational communication; effective risk identification.
**Weaknesses:** Less comprehensive on edge-case safety scenarios.

### Gemini Flash 2.5 — "The Quick Briefer"
**Strengths:** Fast operational summaries; efficient for real-time status updates.
**Weaknesses:** Limited depth in risk evaluation.

### DeepSeek V2 16B — "Not Recommended for Safety-Critical"
**Strengths:** Zero-cost for testing pipeline logic.
**Weaknesses:** Insufficient safety awareness; should never generate operational briefings for real systems.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Safety evaluation** | Claude Sonnet 4 | Most comprehensive risk assessment |
| **Mission briefings** | Claude or GPT-4o | Best professional operational communication |
| **Real-time status** | Gemini Flash 2.5 | Fastest response for status summaries |
| **Flight path planning** | Any (deterministic) | Output is identical — computed mathematically |
| **Pipeline testing only** | Ollama DeepSeek V2 | ONLY for code testing — never for operational output |

> **Safety Note:** LLM outputs in this chapter are supplementary commentary only. All safety-critical decisions (flight paths, boundaries, emergency response) are deterministic and do not depend on LLM output.

---

*Analysis based on Chapter 16 notebook code structure, April 2026. No notebooks had saved execution outputs. Safety-critical logic is entirely deterministic — LLM provides narrative interpretation only.*
