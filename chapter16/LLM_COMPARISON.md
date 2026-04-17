# Chapter 16 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 16 Embodied Intelligence tasks: warehouse robot manipulation with safety constraints, domain-transforming city infrastructure integration, and an Ottawa drone mission case study with a Unified Constraint Envelope.

---

## Agent Tasks in This Chapter

- **Embodied Intelligence Agent** -- Three-layer control hierarchy (strategic reasoning, motion planning, low-level control) with safety-constrained execution via `execute_with_safety()` and `@fail_gracefully` decorator
- **Domain-Transforming Integration Agent** -- Cross-domain city infrastructure (energy, transportation, emergency) with influence propagation tracing cascading failures across domain boundaries
- **Ottawa Drone Case Study** -- Unified Constraint Envelope across 5 domains (weather, battery, airspace, parks, mission) with conservative constraint fusion and multiple failure scenarios (wind, battery, NOTAM, API timeout, stale data)

## Scoring Dimensions

Each provider is rated 0--10 across eight dimensions:

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

## Provider Execution Status

| Provider | Output Cells | SIMULATION_MODE | LLM Client | Key Observation |
|---|---|---|---|---|
| OpenAI GPT-4o | 19 | False | MockChatOpenAI (fallback) | ChatOpenAI init failed: `1 validation error for ChatOpenAI`. Fell back to MockChatOpenAI. |
| Claude Sonnet 4 | 19 | False | MockChatOpenAI (fallback) | Same ChatOpenAI init failure. Same MockChatOpenAI fallback. |
| Gemini Flash 2.5 | 19 | False | MockChatOpenAI (fallback) | Same ChatOpenAI init failure. Same MockChatOpenAI fallback. |
| DeepSeek V2 16B | 19 | True | MockChatOpenAI (explicit) | "Simulation Mode active -- using MockChatOpenAI with chapter-accurate mock data." |

### Critical Finding: All Providers Used MockChatOpenAI

All four notebooks attempted to initialize ChatOpenAI but failed with a validation error. OpenAI, Claude, and Gemini all fell back to MockChatOpenAI despite having SIMULATION_MODE=False. DeepSeek ran in explicit simulation mode. Since all four use the same MockChatOpenAI backend, the agent outputs are functionally identical.

**Evidence:** All four providers show:
- Three-layer control pipeline: strategic -> motion -> low-level (pick_and_place executed)
- Influence propagation: Substation-7 (strength=1.00) -> TrafficController-12 (0.85) -> 14 intersections (0.59 each)
- Unified Constraint Envelope: ALL GREEN for normal conditions
- Waypoint dispatched: (45.3876N, 75.6960W) at 120.0m AGL, 40.0 km/h
- 5 failure scenarios: wind (32.0 km/h > 25 km/h ceiling), battery (22% < 30% floor), NOTAM (active NOTAM-CYOW-2025-0099), API timeout (3 retries exhausted), stale data (8772.0 hours)

The only differences are:
1. **DeepSeek** shows "SIMULATION_MODE = True" vs "False" for the other three
2. **DeepSeek** shows "[SIMULATION]" log prefix instead of "[ERROR]" for the ChatOpenAI init message
3. Minor differences in timeout retry log messages between OpenAI/Claude (which show 3 retry attempts) and Gemini/DeepSeek (which show 2)

---

## Shared Simulation Output Quality

The simulation outputs demonstrate:

- **Three-Layer Control:** Strategic reasoning -> motion planning -> low-level control. Safety-constrained execution with `execute_with_safety()` wrapping every action.
- **Influence Propagation:** Cascading failure from energy domain (Substation-7 outage) through transportation domain (TrafficController-12) to 14 intersections. Strength decay: 1.00 -> 0.85 -> 0.59 (correctly modeled with edge weights).
- **Unified Constraint Envelope:** Conservative fusion across 5 domains. A single RED domain vetoes the entire envelope. Demonstrated with 5 distinct failure scenarios:
  - Wind: 32.0 km/h exceeds 25 km/h operational ceiling
  - Battery: SoC 22% below 30% departure floor
  - Airspace: Active NOTAM vetoes entire envelope
  - API timeout: 3 retries exhausted, `@fail_gracefully` prevents crash, conservative fallback treats failure as constraint violation
  - Stale data: 8772.0 hours since last update exceeds staleness threshold
- **Safety Architecture:** `@fail_gracefully` decorator handles API timeouts gracefully. Conservative fusion treats any failure as a RED constraint.

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|---|
| Factual Accuracy | **8.0** | **8.0** | **8.0** | **8.0** |
| Completeness | **9.0** | **9.0** | **9.0** | **9.0** |
| Structure & Organization | **8.0** | **8.0** | **8.0** | **8.0** |
| Conciseness | **7.0** | **7.0** | **7.0** | **7.0** |
| Source Grounding | **9.0** | **9.0** | **9.0** | **9.0** |
| Bloom's Taxonomy Level | **5.0 (Evaluate)** | **5.0 (Evaluate)** | **5.0 (Evaluate)** | **5.0 (Evaluate)** |
| Nuance & Caveats | **9.0** | **9.0** | **9.0** | **9.0** |
| Practical Utility | **8.0** | **8.0** | **8.0** | **8.0** |
| **WEIGHTED AVERAGE** | **7.9** | **7.9** | **7.9** | **7.9** |

> *All four providers use MockChatOpenAI and produce functionally identical outputs. Scores reflect the shared simulation quality.*

### Score Rationale

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct physical reasoning: wind speed limits, battery SoC thresholds, NOTAM interpretation, influence propagation decay. Coordinates are realistic for Ottawa. |
| Completeness | 9 | Excellent coverage: 3 architectures (warehouse robot, city infrastructure, drone mission), 5 failure scenarios, conservative fusion logic, `@fail_gracefully` demonstration, stale data handling. |
| Structure & Organization | 8 | Clear section structure with Listing references (16.1--16.7). Constraint envelope presented as domain-by-domain status. Influence propagation shows clear path tracing. |
| Conciseness | 7 | Appropriate detail for operational context. Influence propagation listing all 14 intersections is verbose but necessary for completeness. |
| Source Grounding | 9 | Explicit page references throughout (pp. 468--490). Each component references its Listing number. Section references match chapter structure. |
| Bloom's Level | 5 (Evaluate) | The Unified Constraint Envelope evaluates multiple domain constraints and makes go/no-go decisions. Conservative fusion explicitly judges that "a single RED domain vetoes the entire envelope." Failure scenarios evaluate trade-offs between safety and mission completion. |
| Nuance & Caveats | 9 | Conservative constraint fusion is the standout feature: treats API failures as constraint violations (safe default), treats stale data as RED (not merely yellow), and explains rationale for each abort decision. 5 distinct failure modes demonstrate comprehensive edge-case handling. |
| Practical Utility | 8 | Directly applicable to real drone operations. Conservative fusion is industry-standard for safety-critical systems. Failure scenario demonstrations would be valuable for operational testing. |

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    | oooooooooo All Providers (constraint evaluation + go/no-go)
Level 4: Analyze     |
Level 3: Apply       |
Level 2: Understand  |
Level 1: Remember    |
```

The simulation reaches Level 5 (Evaluate) because the Unified Constraint Envelope explicitly evaluates competing constraints and makes judgment calls: "FLIGHT ABORTED -- failed domain(s): ['wind']. Wind speed 32.0 km/h exceeds 25 km/h operational ceiling." The conservative fusion rule ("a single RED domain vetoes the entire envelope") is an evaluative principle applied across 5 failure scenarios. This goes beyond analysis (Level 4) because it does not merely decompose constraints -- it judges whether to fly or abort.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  OpenAI GPT-4o          7.9  ███████████████████████░░░░░░░░
  Claude Sonnet 4        7.9  ███████████████████████░░░░░░░░
  Gemini Flash 2.5       7.9  ███████████████████████░░░░░░░░
  DeepSeek V2 (Local)    7.9  ███████████████████████░░░░░░░░
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     | O C G D (all identical)
  L4 Analyze      | O C G D
  L3 Apply        | O C G D
  L2 Understand   | O C G D
  L1 Remember     | O C G D
```

Legend: **O** = OpenAI GPT-4o, **C** = Claude Sonnet 4, **G** = Gemini Flash 2.5, **D** = DeepSeek V2

---

## Winner: Tie (All Providers)

| | |
|---|---|
| **Chapter 16 Winner** | **Tie -- All Providers** |
| **Score** | **7.9 / 10** |
| **Bloom's Level** | **Level 5 -- Evaluate** |

**Why this is a tie:**
- All four providers fell back to the same MockChatOpenAI backend
- Agent outputs are functionally identical across all notebooks
- The only differences are init log messages (SIMULATION_MODE flag, error vs simulation prefix)
- The ChatOpenAI validation error affected OpenAI, Claude, and Gemini equally

**Why the score is higher than Chapters 13--14:**
- Chapter 16 demonstrates a richer safety architecture with 5 distinct failure scenarios
- The Unified Constraint Envelope reaches Bloom's Level 5 (Evaluate) through explicit go/no-go decisions
- Influence propagation across 3 domains (energy, transportation, emergency) shows sophisticated cross-domain analysis
- The `@fail_gracefully` + API timeout demonstration has direct practical utility for production systems

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality | Any (identical) | All use same MockChatOpenAI backend |
| Cost-efficient production | Gemini Flash 2.5 | Lowest per-token cost if live LLM were integrated |
| Air-gapped / private data | DeepSeek V2 (Local) | Zero cloud dependency; cleanest init (explicit simulation, no error fallback) |
| Rapid prototyping | DeepSeek V2 (Local) | No API key needed, instant iteration |

## Provider Profiles for This Chapter

### All Providers -- "The Safety Pipeline"
**Strengths:** Comprehensive embodied agent architecture with three-layer control, cross-domain influence propagation, and a production-grade Unified Constraint Envelope. Conservative fusion principle correctly implemented. Five distinct failure scenarios cover wind, battery, airspace, API timeout, and stale data. `@fail_gracefully` prevents crashes on external API failures.
**Weaknesses:** All fell back to MockChatOpenAI -- no live LLM differentiation. ChatOpenAI validation error should be fixed to enable live comparison. Influence propagation listing 14 intersections is verbose.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Drone mission planning** | Any -- then fix ChatOpenAI init | Conservative fusion is code-identical across all providers |
| **Cross-domain infrastructure** | Any (deterministic) | Influence propagation is pure algorithmic computation |
| **Safety-critical prototyping** | DeepSeek V2 (Local) | Zero cost, explicit simulation mode, no error fallback surprises |
| **Production deployment** | Fix langchain compatibility, then benchmark live | Current notebooks do not test live LLM reasoning for embodied tasks |

> **Safety Note:** Conservative constraint fusion (a single RED vetoes the entire envelope) is the correct approach for safety-critical systems. This principle should be preserved regardless of which LLM provider is used.

---

*Analysis based on Chapter 16 notebook outputs executed April 2026. All four providers (OpenAI, Claude, Gemini, DeepSeek) use MockChatOpenAI due to ChatOpenAI validation errors. Outputs are functionally identical. The embodied agent architecture demonstrates Level 5 (Evaluate) through explicit constraint evaluation and go/no-go decisions across 5 failure scenarios.*
