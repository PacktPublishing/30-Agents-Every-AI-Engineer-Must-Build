# Chapter 17 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 17 Future Agents tasks: self-architecting agents, agent societies, ethical governance, memory consolidation, and human-AI collaboration spectrums.

---

## Agent Tasks in This Chapter

- **Self-Architecting Agent** -- Meta-optimization over a 6-candidate architecture registry with alignment constraint filtering (C_1: network access, C_3: shell execution)
- **Agent Society Simulation** -- DeGroot weighted belief averaging (5 agents, 20 rounds), distributed reputation ledger, spontaneous specialization via comparative advantage
- **Ethics Circuit Breaker** -- Behavioral drift detection using KS statistic (4 escalation phases: log alert, oversight, restrict autonomy, halt operation)
- **Memory Consolidation** -- Episodic-to-semantic transfer: 12 episodes replayed, 4 generalizable patterns extracted (retry-with-backoff, cache-before-call, escalate-to-human, parallel-tool-invocation)
- **Human-AI Collaboration Spectrum** -- Task classification (15 tasks: 9 autonomous, 4 collaborative, 2 escalated) with Quandri-inspired efficiency metrics and crawl-walk-run maturity model

## Scoring Dimensions

Each provider is rated 0--10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of architecture descriptions, convergence mechanics, and behavior predictions |
| **Completeness** | Coverage of all evolutionary mechanisms, emergent patterns, and escalation levels |
| **Structure & Organization** | Quality of architecture catalogs, convergence reports, and escalation summaries |
| **Conciseness** | Appropriate depth for forward-looking research content |
| **Source Grounding** | Adherence to the chapter's future agent frameworks |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Handling of alignment vs. performance trade-offs, safety margins, and ethical boundaries |
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

## Provider Execution Status

| Provider | Output Cells | LLM Mode | Key Observation |
|---|---|---|---|
| OpenAI GPT-4o | 7 | Live API key detected | "Live API key detected. Running in LIVE MODE." All simulations use deterministic code paths; LLM analysis lines are `[SIMULATION MODE]` prefixed mock responses. |
| Claude Sonnet 4 | 7 | Live API key detected | Identical outputs to OpenAI. Same `[SIMULATION MODE]` mock analysis. |
| Gemini Flash 2.5 | 7 | Live API key detected | Identical outputs to OpenAI. Same `[SIMULATION MODE]` mock analysis. |
| DeepSeek V2 16B | 7 | Live API key detected | Identical outputs to OpenAI. Same `[SIMULATION MODE]` mock analysis. |

### Critical Finding: All Providers Produce Identical Outputs

Chapter 17 uses a shared `MockLLM` from `mock_engine.py` with a `RESPONSE_REGISTRY` keyed by prompt keywords. All five simulations (self-architecting, agent society, ethics circuit breaker, memory consolidation, collaboration spectrum) use deterministic algorithms with mock LLM analysis appended. The `[SIMULATION MODE]` prefix on all LLM analysis lines confirms that no actual API calls were made for the substantive outputs, despite live API keys being detected.

All four notebooks produce identical outputs:
- Architecture search: ReAct-v3 + FAISS-Memory + CodeInterpreter selected (P(a) = 0.91); 2 candidates excluded (Unconstrained-Optimizer violates C_3, MCTS-Planner violates C_1)
- DeGroot convergence: beliefs converge to [0.544, 0.544, 0.544, 0.544, 0.544] by round 6
- Specialization: Agent-3 -> coding (0.95), Agent-4 -> review (0.94), Agent-1 -> research (0.92), Agent-0 -> analysis (0.88)
- Ethics cascade: KS statistic escalates 0.345 -> 0.565 -> 0.885 -> 0.970 across 4 phases
- Memory consolidation: 12 episodes -> 4 semantic patterns, 11 pruned, 1 retained
- Collaboration spectrum: 9 autonomous (60%), 4 collaborative, 2 escalated; $30,000/month estimated value

---

## Shared Simulation Output Quality

### Simulation 1: Self-Architecting Agent
- **Architecture registry:** 6 candidates with performance scores, alignment compliance status, and human-readable descriptions
- **Constrained search:** Correctly excludes 2 high-scoring but non-compliant candidates (P(a) = 0.96 and 0.93) in favor of the highest-scoring compliant candidate (P(a) = 0.91)
- **Key insight:** Demonstrates that raw performance optimization without alignment constraints would select a dangerous pipeline (unrestricted shell execution)

### Simulation 2: Agent Society
- **DeGroot convergence:** Mathematically correct weighted belief averaging; beliefs converge to 0.544 (consensus) from diverse starting points (0.2, 0.9, 0.5, 0.7, 0.3) by round 6
- **Reputation ledger:** 5 agents with distinct specializations assigned based on task-specific scores
- **Spontaneous specialization:** Comparative advantage correctly assigns agents to highest-reputation tasks

### Simulation 3: Ethics Circuit Breaker
- **Graduated response:** 4 escalation levels clearly demonstrated with KS statistic thresholds
- **Escalation summary table:** Clean presentation with phase, KS statistic, level, and response columns
- **Key insight:** Level 3 restricts to "pre-approved action set only"; Level 4 is "FULL HALT. Agent suspended pending human review"

### Simulation 4: Memory Consolidation
- **Episodic replay:** 12 episodes with diverse categories (API timeouts, cache hits, ethical dilemmas, parallel execution)
- **Pattern extraction:** 4 patterns with source episode attribution and generalization scope
- **Pruning:** 11 of 12 episodes pruned after consolidation; 1 retained (the ethical dilemma, appropriately -- hardest to generalize)
- **Analogical transfer:** retry-with-backoff generalized from API-call domain to database-connection domain

### Simulation 5: Collaboration Spectrum
- **Task routing:** 15 tasks across 3 complexity/stakes tiers, correctly classified
- **Quandri-inspired metrics:** 60% autonomous, 99.9% accuracy, ~$30,000/month value, 12 min avg processing
- **Crawl-walk-run model:** Progressive maturity assessment demonstrated

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|---|
| Factual Accuracy | **8.0** | **8.0** | **8.0** | **8.0** |
| Completeness | **9.0** | **9.0** | **9.0** | **9.0** |
| Structure & Organization | **8.0** | **8.0** | **8.0** | **8.0** |
| Conciseness | **7.0** | **7.0** | **7.0** | **7.0** |
| Source Grounding | **8.0** | **8.0** | **8.0** | **8.0** |
| Bloom's Taxonomy Level | **5.0 (Evaluate)** | **5.0 (Evaluate)** | **5.0 (Evaluate)** | **5.0 (Evaluate)** |
| Nuance & Caveats | **9.0** | **9.0** | **9.0** | **9.0** |
| Practical Utility | **8.0** | **8.0** | **8.0** | **8.0** |
| **WEIGHTED AVERAGE** | **7.8** | **7.8** | **7.8** | **7.8** |

> *All four providers produce identical outputs. Scores reflect shared simulation quality.*

### Score Rationale

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | DeGroot convergence is mathematically correct. KS statistic escalation is well-calibrated. Architecture search correctly filters by alignment constraints. Memory consolidation pattern extraction is logically sound. |
| Completeness | 9 | Five distinct simulations covering self-architecting, society formation, ethical governance, memory consolidation, and collaboration spectrum. Each simulation has multiple phases (architecture search has 6 candidates; ethics has 4 escalation levels; memory has 12 episodes -> 4 patterns). |
| Structure & Organization | 8 | Clean section headers for each simulation. Escalation summary table is well-formatted. Architecture registry uses consistent format (name, score, compliance, description). Task routing uses color-coded severity levels. |
| Conciseness | 7 | Some simulations are redundant: the collaboration spectrum is run 3 times (routing, efficiency metrics, maturity assessment) with identical task routing output repeated each time. This is the main verbosity issue. |
| Source Grounding | 8 | Each `[SIMULATION MODE]` LLM analysis references chapter sections (e.g., "Ref: Ch.17, pp.1-2, 'Autonomous agent evolution and adaptation'"). Page references are consistent. |
| Bloom's Level | 5 (Evaluate) | Architecture search evaluates alignment vs. performance trade-offs (excluding P(a)=0.96 in favor of P(a)=0.91 for safety). Ethics circuit breaker evaluates behavioral drift severity and judges appropriate response level. Memory consolidation evaluates which episodes contain generalizable patterns. |
| Nuance & Caveats | 9 | Strongest feature across all simulations. Architecture search explicitly shows that the highest-performing pipeline is the most dangerous. Ethics circuit breaker uses graduated response (not binary on/off). Memory consolidation retains the ethical dilemma episode (hardest to generalize). Collaboration spectrum routes high-stakes tasks to human escalation. |
| Practical Utility | 8 | Architecture registry format is directly usable. Ethics circuit breaker escalation table is deployable. Collaboration spectrum with Quandri metrics provides concrete ROI estimates. Memory consolidation pattern library is a useful design pattern. |

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    | oooooooooo All Providers (alignment trade-offs + ethical escalation)
Level 4: Analyze     |
Level 3: Apply       |
Level 2: Understand  |
Level 1: Remember    |
```

The simulations reach Level 5 (Evaluate) through multiple evaluative mechanisms:
1. **Architecture search:** Evaluates the trade-off between raw performance (P(a)=0.96) and alignment compliance, explicitly choosing a lower-scoring but safe pipeline
2. **Ethics circuit breaker:** Evaluates behavioral drift severity using KS statistic and judges when to restrict vs. halt agent autonomy
3. **Memory consolidation:** Evaluates which episodic patterns are generalizable enough to promote to semantic memory
4. **Collaboration spectrum:** Evaluates task complexity and stakes to judge appropriate autonomy level (autonomous vs. collaborative vs. escalated)

The simulations do not reach Level 6 (Create) because they follow pre-defined evaluation frameworks rather than generating novel architectures or governance structures.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  OpenAI GPT-4o          7.8  ███████████████████████░░░░░░░░
  Claude Sonnet 4        7.8  ███████████████████████░░░░░░░░
  Gemini Flash 2.5       7.8  ███████████████████████░░░░░░░░
  DeepSeek V2 (Local)    7.8  ███████████████████████░░░░░░░░
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
| **Chapter 17 Winner** | **Tie -- All Providers** |
| **Score** | **7.8 / 10** |
| **Bloom's Level** | **Level 5 -- Evaluate** |

**Why this is a tie:**
- All four providers produce identical outputs from the shared `mock_engine.py` RESPONSE_REGISTRY
- All simulations use deterministic algorithms (DeGroot averaging, KS statistic, constrained search) with mock LLM analysis appended
- No live LLM calls were made for any substantive output despite live API keys being detected
- The `[SIMULATION MODE]` prefix on all LLM analysis lines confirms uniform mock behavior

**Why the score is high (7.8):**
- Five distinct simulations covering the full scope of future agent research
- Evaluative reasoning demonstrated across multiple dimensions (alignment, ethics, memory, collaboration)
- Strong nuance: alignment vs. performance trade-offs, graduated ethical response, selective memory retention
- Practical utility: architecture registry format, escalation table, and ROI metrics are directly deployable

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality | Any (identical) | All produce the same simulation outputs |
| Cost-efficient production | Gemini Flash 2.5 | Lowest per-token cost for equivalent output |
| Air-gapped / private data | DeepSeek V2 (Local) | Zero cloud dependency |
| Rapid prototyping | DeepSeek V2 (Local) | No API key needed, instant iteration, zero cost |

## Provider Profiles for This Chapter

### All Providers -- "The Future Simulation Suite"
**Strengths:** Five well-designed simulations covering the frontier of agent research. Architecture search demonstrates constrained optimization with alignment awareness. Ethics circuit breaker provides a graduated response framework. Memory consolidation shows analogical transfer across domains. Collaboration spectrum includes concrete ROI metrics.
**Weaknesses:** All outputs are simulation-mode; no live LLM differentiation. Collaboration spectrum output is repeated 3 times (verbosity). Mock LLM analysis text is generic and does not match the actual simulation numbers in some cases (e.g., mock analysis reports convergence to [0.72, 0.74] but simulation shows [0.544, 0.544]).

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Architecture registry design** | Any (deterministic) | Constrained search is algorithmic, not LLM-dependent |
| **Agent society simulation** | Any (deterministic) | DeGroot convergence is mathematical |
| **Ethics governance prototyping** | Any -- then add live LLM | Graduated response framework is code-identical; live LLM could enhance behavioral analysis |
| **Memory architecture research** | Any -- then add live LLM | Pattern extraction is algorithmic; live LLM could improve analogical transfer quality |
| **Pipeline development** | DeepSeek V2 (Local) | Zero cost, identical functionality |

> **Research Note:** The mock LLM analysis text in Simulation 2 reports different convergence values ([0.72, 0.74]) than the actual simulation output ([0.544, 0.544]). This discrepancy exists across all providers since the mock text is shared. The simulation output is correct; the mock analysis text should be updated for consistency.

---

*Analysis based on Chapter 17 notebook outputs executed April 2026. All four providers (OpenAI, Claude, Gemini, DeepSeek) produce identical simulation-mode outputs from the shared mock_engine.py response registry. Five simulations demonstrate future agent architectures at Bloom's Level 5 (Evaluate) through alignment trade-offs, ethical escalation, and selective memory consolidation.*
