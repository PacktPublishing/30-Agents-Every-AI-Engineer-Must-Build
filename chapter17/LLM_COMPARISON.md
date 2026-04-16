# Chapter 17 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 17 Future Agents tasks: self-architecting agents, agent societies, ethical governance, memory consolidation, and human-AI collaboration spectrums.

---

## Agent Tasks in This Chapter

- **Self-Architecting Agent** -- Meta-optimization over an architecture registry to find optimal pipeline configurations
- **Agent Society Simulation** -- DeGroot weighted belief averaging with emergent specialization
- **Ethics Circuit Breaker** -- Behavioral drift detection (KS statistic) with graduated autonomy restriction
- **Memory Consolidation** -- Episodic-to-semantic memory transfer with analogical pattern extraction
- **Human-AI Collaboration Spectrum** -- Task classification (autonomous, collaborative, escalated) with the crawl-walk-run maturity model

## Scoring Dimensions

Each provider is rated 0--10 across eight dimensions:

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

## Key Observation: All Four Providers Produce Identical Simulation Outputs

Chapter 17 uses a shared `MockLLM` from `mock_engine.py` across all four provider notebooks:

- All four notebooks call `MockLLM.generate(prompt)` which routes by keyword matching to pre-authored responses
- The `RESPONSE_REGISTRY` is defined in `mock_engine.py` (shared module) -- identical across all providers
- No live LLM API calls are made in any notebook
- All four notebooks have exactly **8 output cells** each

**Evidence -- all four providers produce these identical LLM Analysis outputs:**

1. **Architecture search**: "The meta-optimization search evaluated 6 candidate pipelines from the architecture registry. Pipeline 'ReAct-v3 + FAISS-memory' emerged as winner..."

2. **Agent society**: "After 20 rounds of DeGroot weighted belief averaging, the 5-agent society converged to consensus belief vector [0.72, 0.74, 0.71, 0.73, 0.72]. Agent-3 emerged as the dominant specialist in 'code-review' tasks (reputation: 0.94)..."

3. **Ethics circuit breaker**: "Behavioral drift detected across 4 phases. KS statistic escalated from 0.08 to 0.55. Graduated response triggered: Phase 1 -> log alert, Phase 2 -> increased oversight, Phase 3 -> autonomy restricted, Phase 4 -> full halt."

4. **Memory consolidation**: "Consolidation batch complete. 12 episodes replayed, 4 generalizable patterns extracted to semantic memory, 8 fully consolidated episodes pruned. Analogical transfer: 'retry-with-backoff' generalized from API-call domain to database-connection domain."

5. **Human-AI collaboration**: "Task routing complete. 15 tasks classified: 9 autonomous (routine), 4 collaborative (complex multi-step), 2 escalated to human (high-stakes). Estimated efficiency gain: 74%. Modeled after Quandri case study: 99.9% accuracy, <15 min processing."

---

## Shared Simulation Output Quality

The simulation outputs demonstrate the chapter's five key future agent concepts:

- **Self-architecting agents:** Architecture registry search correctly selects optimal pipeline from 6 candidates based on fitness evaluation
- **Emergent specialization:** DeGroot convergence produces meaningful specialization (Agent-3 in code-review at 0.94 reputation, Agent-1 in research at 0.89)
- **Graduated governance:** KS statistic correctly escalates through 4 severity phases with proportional autonomy restriction
- **Memory transfer:** Episodic-to-semantic transfer with analogical generalization (retry-with-backoff pattern generalized across domains)
- **Task classification:** Crawl-walk-run model correctly triages 15 tasks with appropriate confidence levels (9/4/2 split)

### Unified Score (All Providers)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct DeGroot convergence mechanics; valid KS statistic interpretation; proper memory consolidation terminology |
| Completeness | 8 | All 5 future agent themes demonstrated; each with quantitative simulation outputs |
| Structure & Organization | 7 | Simulation outputs are concise but lack the structured report format of earlier chapters |
| Conciseness | 8 | Appropriately brief for simulation summaries; each output is 2-3 sentences |
| Source Grounding | 9 | Every output includes explicit chapter references (pp.2-8); Quandri case study cited |
| Bloom's Level | **3 -- Apply** | Simulations apply described patterns (DeGroot, KS statistic, SM-2) to specific scenarios but do not analyze trade-offs |
| Nuance & Caveats | 6 | Limited nuance -- outputs report results without discussing limitations or uncertainty in the simulations |
| Practical Utility | 7 | Good conceptual demos; would need live LLM for actual research synthesis or architecture evaluation |

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|---|
| Factual Accuracy | **8.0** | **8.0** | **8.0** | **8.0** |
| Completeness | **8.0** | **8.0** | **8.0** | **8.0** |
| Structure & Organization | **7.0** | **7.0** | **7.0** | **7.0** |
| Conciseness | **8.0** | **8.0** | **8.0** | **8.0** |
| Source Grounding | **9.0** | **9.0** | **9.0** | **9.0** |
| Bloom's Taxonomy Level | **3.0 (Apply)** | **3.0 (Apply)** | **3.0 (Apply)** | **3.0 (Apply)** |
| Nuance & Caveats | **6.0** | **6.0** | **6.0** | **6.0** |
| Practical Utility | **7.0** | **7.0** | **7.0** | **7.0** |
| **WEIGHTED AVERAGE** | **7.0** | **7.0** | **7.0** | **7.0** |

> *All four providers produce byte-identical simulation outputs from shared MockLLM. Scores reflect shared output quality.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     |
Level 3: Apply       | oooooooooooo All Providers (identical simulation)
Level 2: Understand  |
Level 1: Remember    |
```

The simulation outputs reach Level 3 (Apply) -- they apply established algorithms (DeGroot averaging, KS test, memory consolidation) to specific scenarios and report results. They do not reach Level 4 because the MockLLM outputs do not compare or contrast approaches (e.g., "DeGroot vs. other consensus mechanisms" or "KS test vs. chi-squared for drift detection"). The outputs state what happened without analyzing why one approach was chosen over alternatives.

This is a notable limitation for a chapter about "future agents" -- one would expect Level 5 (Evaluate) or Level 6 (Create) outputs that assess which future directions are most promising or synthesize novel architectural proposals. The simulation framework constrains cognitive depth.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  OpenAI GPT-4o          7.0  █████████████████████░░░░░░░░░░
  Claude Sonnet 4        7.0  █████████████████████░░░░░░░░░░
  Gemini Flash 2.5       7.0  █████████████████████░░░░░░░░░░
  DeepSeek V2 (Local)    7.0  █████████████████████░░░░░░░░░░
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
| **Chapter 17 Winner** | **Tie -- All Providers** |
| **Score** | **7.0 / 10** |
| **Bloom's Level** | **Level 3 -- Apply** |

**Why this is a tie:**
- All four provider notebooks use the same `MockLLM` from `mock_engine.py`
- The `RESPONSE_REGISTRY` routes by keyword to identical pre-authored responses
- All four notebooks have exactly 8 output cells with byte-identical content
- No live LLM API calls differentiate the providers

**To differentiate providers, this chapter would need:**
1. Live LLM calls for architecture evaluation commentary
2. Provider-specific research synthesis on future agent directions
3. Open-ended prompts where LLM creativity and nuance would vary

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality | Any (identical) | Simulation outputs are the same |
| Cost-efficient production | Gemini Flash 2.5 | Lowest per-token cost for equivalent output |
| Air-gapped / private data | DeepSeek V2 (Local) | Only option with zero cloud dependency |
| Rapid prototyping | DeepSeek V2 (Local) | No API key, instant iteration, zero cost |

## Provider Profiles for This Chapter

### All Providers -- "The Simulation Engine"
**Strengths:** Demonstrates 5 key future agent concepts with quantitative simulation outputs; correct application of DeGroot averaging, KS statistics, and memory consolidation; explicit chapter references throughout.
**Weaknesses:** No live LLM differentiation; simulation outputs are formulaic summaries rather than creative research synthesis; Bloom's Level 3 is low for a chapter about future research directions.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Research direction synthesis** | Any -- then add live LLM | Simulation provides structure; live LLM would add evaluative depth |
| **Architecture evaluation** | Any -- then add live LLM | Meta-optimization results are deterministic |
| **Quick concept demo** | Any mock mode | All 5 simulations run in seconds |
| **Future agent prototyping** | Any mock mode | Zero cost for exploring the architecture |
| **Local experimentation** | Ollama DeepSeek V2 | Zero cost, identical simulation results |

---

*Analysis based on Chapter 17 notebook outputs executed April 2026. All four providers (OpenAI, Claude, Gemini, DeepSeek) produce identical simulation-mode outputs from shared MockLLM (mock_engine.py). Evolution simulations, society dynamics, and governance mechanisms are entirely deterministic. No live LLM calls were made in any notebook.*
