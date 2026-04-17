# Chapter 15 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of three LLM providers running the Chapter 15 Education Intelligence and Collective Intelligence tasks: adaptive tutoring with Bayesian Knowledge Tracing and multi-agent consensus building.

---

## Agent Tasks in This Chapter

- **Education Intelligence Agent** -- POMDP-based adaptive tutoring: knowledge graph curriculum (10 objectives, 11 prerequisite edges), ZPD-aligned objective selection, IRT 2PL placement testing, Bayesian Knowledge Tracing, SM-2 spaced repetition, and two-stage misconception detection with pedagogical feedback
- **Collective Intelligence Agent** -- Multi-agent collaboration: CollaborativeAgent propose/critique pathways, ConsensusEngine with expertise-weighted scoring and adversarial critic rotation, emergent cross-pollination

## Scoring Dimensions

Each provider is rated 0--10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of educational content, assessment items, and pedagogical reasoning |
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

## Provider Execution Status

| Provider | Output Cells | LLM Mode | Key Observation |
|---|---|---|---|
| OpenAI GPT-4o | 17 | **Live API** (gpt-4o) | "LLM client: LiveLLM (OpenAI gpt-4o)" -- actual GPT-4o API calls for feedback, proposals, evaluations, consensus, and cross-pollination. |
| Claude Sonnet 4 | 0 | Not executed | Notebook has no saved outputs. Excluded from scoring. |
| Gemini Flash 2.5 | 17 | **Live API** (gemini-2.5-flash) | "LLM client: LiveLLM (Gemini gemini-2.5-flash)" -- actual Gemini API calls. Deprecated `google.generativeai` warning present. |
| DeepSeek V2 16B | 17 | MockLLM (simulation) | "LLM client: MockLLM (Simulation Mode)" -- pre-authored mock responses. |

### Critical Finding: Two Live Providers Enable Real Comparison

This is one of the few chapters where two cloud providers ran with actual live API calls. OpenAI GPT-4o and Gemini Flash 2.5 both generated real feedback, proposals, evaluations, and consensus syntheses. DeepSeek used pre-authored mock responses. This enables a genuine three-way comparison across live-live-mock modes.

**Deterministic components (identical across all providers):** Knowledge graph (10 objectives, 11 edges), topological sort, StudentModel mastery tracking, IRT 2PL placement test, BKT belief update, SM-2 spaced repetition scheduling. These are pure algorithmic components with no LLM involvement.

---

## Provider-Specific Results

### OpenAI GPT-4o (Live API)

**Feedback generation (Alex case study):**
- Feedback text: "Great job on setting up the loop to iterate over the numbers and correctly checking for even numbers and negative values..." (1141 chars)
- Style: Flowing narrative paragraph acknowledging correct elements before addressing the `break` placement misconception
- Misconception detected: `ctrl_flow_break_placement` (confidence=0.82) -- rule-based detection, identical across providers
- Latency: ~5 seconds for feedback generation (20:51:16 to 20:51:21)

**Collaborative agent evaluation:**
- Evaluation returned detailed multi-dimension scores: `{correctness: 9.0, completeness: 8.0, feasibility: 9.0, overall: 8.666666666666666}`
- This is the richest evaluation output of all three providers

**Consensus engine (3-agent rubric design):**
- Agent test consensus: converged in **2 rounds**, score **5.17**
  - Round 1 scores: pedagogy=6.83, domain=5.00, assessment=5.00
  - Round 2 scores: pedagogy=5.00, domain=5.00, assessment=5.50
- Rubric case study consensus: converged in **1 round**, score **5.00**
  - All 3 proposals scored identically at 5.00
- Total consensus pipeline: ~2 minutes (20:51:45 to 20:53:45)

**Cross-pollination output:**
- Generated "Integrated Framework: Process-Oriented Edge-Case Assessment" -- a structured framework combining edge-case testing with process-oriented assessment
- Used Markdown headers and numbered sections
- Latency: ~5 seconds (20:55:06 to 20:55:11)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Live GPT-4o feedback correctly identifies loop structure and `break` placement issue. Evaluation dimensions (correctness, completeness, feasibility) are appropriate. |
| Completeness | 8 | Full 3-dimension evaluation breakdown (only provider to return all 3 sub-scores plus overall). Consensus converged within round limits. |
| Structure & Organization | 7 | Feedback is a flowing paragraph (less structured than numbered lists). Consensus synthesis produced a well-organized rubric with 6 criteria. |
| Conciseness | 7 | Feedback at 1141 chars is appropriately detailed. Consensus scores tended toward 5.0 (undifferentiated), suggesting the LLM struggled to meaningfully rank proposals. |
| Source Grounding | 8 | Follows the pedagogical contract structure (acknowledge correct, identify error, guide discovery). Does not explicitly cite chapter section numbers in LLM output. |
| Bloom's Level | **5 -- Evaluate** | Evaluation scores across 3 dimensions demonstrate judgment. Cross-pollination explicitly assesses which elements to combine from competing proposals. |
| Nuance & Caveats | 7 | Feedback acknowledges correct code elements before addressing errors. Consensus scores clustered near 5.0 -- limited discrimination between proposals. |
| Practical Utility | 8 | Live API output demonstrates real deployment behavior. Multi-dimension evaluations enable finer-grained pedagogical adaptation. |

---

### Gemini Flash 2.5 (Live API)

**Feedback generation (Alex case study):**
- Feedback text: "Great start! You've correctly identified several key components for this problem:\n\n1. You've initialized `total` to `0`..." (1291 chars)
- Style: Numbered list decomposing the student's code into specific components -- pedagogically stronger for code-focused feedback
- Misconception detected: `ctrl_flow_break_placement` (confidence=0.82) -- same rule-based detection
- Latency: ~27 seconds for feedback generation (18:09:18 to 18:09:45)

**Collaborative agent evaluation:**
- Evaluation returned only overall score: `{overall: 5.0}`
- Missing the multi-dimension breakdown (correctness, completeness, feasibility) -- the live Gemini response did not parse into the expected JSON structure

**Consensus engine (3-agent rubric design):**
- Agent test consensus: **did not converge**, ran all 3 rounds, score **6.11**
  - Round 1 scores: pedagogy=7.17, domain=5.00, assessment=5.50
  - Round 2 scores: pedagogy=5.83, domain=9.17, assessment=5.00
  - Round 3 scores: pedagogy=6.00, domain=5.00, assessment=7.33
  - Score leadership shifted each round, showing genuine adversarial critique dynamics
- Rubric case study consensus: **did not converge**, ran all 3 rounds, score **6.00**
  - Round 1: pedagogy=5.00, domain=6.17, assessment=5.50
  - Round 2: pedagogy=5.00, domain=5.00, assessment=7.33
  - Round 3: pedagogy=5.00, domain=5.50, assessment=7.50
- Total consensus pipeline: ~9 minutes (18:10:37 to 18:19:15)
- The rotating score leadership (different proposals winning each round) demonstrates genuine multi-agent deliberation

**Cross-pollination output:**
- Generated: "This is an exciting challenge! Let's combine the robustness and foresight of edge-case testing with the iterative learning and reflection of process-oriented assessment..."
- Conversational tone with explicit reasoning about why neither agent would propose these independently
- Latency: ~21 seconds (18:27:32 to 18:27:53)

**Rubric case study synthesis:**
- Final rubric: 6401 chars total -- the most detailed synthesis of all providers
- Referenced individual agents by name: "The rubric, detailed by Agent pedagogy_01, is considered a robust and effective tool..."
- Explicitly attributed contributions from Agent domain_01 and Agent assessment_01

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Live Gemini feedback correctly identifies code components (`total` initialization, `for` loop structure, `break` placement). Numbered decomposition is pedagogically sound. |
| Completeness | 6 | Evaluation returned only `overall` score, losing the 3-dimension breakdown. Consensus required all 3 rounds without converging. However, the rubric synthesis was the most detailed (6401 chars). |
| Structure & Organization | 8 | Numbered-list feedback is superior for code-focused pedagogy. Rubric synthesis explicitly attributes contributions to each agent. But evaluation parsing lost dimensional detail. |
| Conciseness | 7 | Feedback at 1291 chars is slightly longer than OpenAI. Cross-pollination has conversational preamble before substance. |
| Source Grounding | 7 | Follows the feedback generator prompt structure but LLM output does not explicitly reference chapter concepts. |
| Bloom's Level | **5 -- Evaluate** | Cross-pollination explicitly evaluates what each agent would miss independently. Rubric synthesis attributes and assesses individual agent contributions. |
| Nuance & Caveats | 8 | Consensus score leadership rotated across rounds (pedagogy -> domain -> assessment), showing genuine deliberation. Cross-pollination explains why neither agent would propose the combined criterion alone. |
| Practical Utility | 8 | Numbered feedback format is immediately deployable for coding education. 3-round deliberation demonstrates realistic multi-agent behavior. Most detailed rubric synthesis. |

---

### DeepSeek V2 16B (MockLLM / Simulation Mode)

**Feedback generation (Alex case study):**
- Feedback text: "Great work on the overall structure of your solution! Your use of a for loop to iterate through the list is correct, and..." (1345 chars)
- Style: Flowing paragraph (pre-authored mock response)
- MockLLM Call #1 routed to mock key `feedback_generator`

**Collaborative agent evaluation:**
- Evaluation returned 3-dimension scores: `{correctness: 7.0, completeness: 6.0, feasibility: 8.0, overall: 6.5}`
- Pre-authored mock evaluation with moderate, well-calibrated scores

**Consensus engine (3-agent rubric design):**
- Agent test consensus: converged in **1 round**, score **6.50**
  - Round 1 scores: all three proposals scored identically at 6.50 (deterministic mock)
- Rubric case study consensus: converged in **1 round**, score **6.50**
  - Same pattern: all proposals scored 6.50
- Total consensus pipeline: < 1 second (zero latency)

**Cross-pollination output:**
- Generated (mock): "## Cross-Pollination: Emergent Criterion\n\n### Novel Diagnostic-Trace Criterion\n\nBy examining the strongest elements from competing proposals, a new criterion has emerged..."
- Well-structured with Markdown headers, specific criterion name, and clear provenance
- MockLLM Call #24 routed to mock key `cross_pollination`

**Rubric case study synthesis:**
- Final rubric: 2018 chars -- structured table with 5 criteria x 3-point scale
- Each criterion attributed to a specific agent (Assessment Agent, Domain Expert, Pedagogy Agent)
- Most structured format of all providers (table with Absent/Partial/Complete columns)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Pre-authored mock responses are factually curated and correct. |
| Completeness | 8 | Full 3-dimension evaluation (like OpenAI); complete pedagogical contract; 5-criterion rubric table. |
| Structure & Organization | 9 | Best-structured rubric output (table format with Absent/Partial/Complete scale). Cross-pollination uses clear Markdown hierarchy. |
| Conciseness | 8 | Mock responses are well-calibrated in length (1345 chars feedback, 2018 chars rubric). |
| Source Grounding | 9 | Mock responses explicitly keyed to chapter concepts (feedback_generator, propose_pedagogy, evaluate_proposal, cross_pollination). |
| Bloom's Level | **4 -- Analyze** | Mock feedback analyzes code structure; evaluation breaks down into dimensions. Does not demonstrate true evaluation or synthesis (responses are pre-authored). |
| Nuance & Caveats | 7 | Follows the 4-part pedagogical contract. Rubric attributes criteria to specific agents. But mock consensus converges instantly with identical scores -- no genuine deliberation. |
| Practical Utility | 7 | Good reference implementation; mock rubric table format is immediately usable. But static responses do not demonstrate real LLM behavior. |

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|---|
| Factual Accuracy | **8.0** | N/A | **8.0** | **8.0** |
| Completeness | **8.0** | N/A | **6.0** | **8.0** |
| Structure & Organization | **7.0** | N/A | **8.0** | **9.0** |
| Conciseness | **7.0** | N/A | **7.0** | **8.0** |
| Source Grounding | **8.0** | N/A | **7.0** | **9.0** |
| Bloom's Taxonomy Level | **5.0 (Evaluate)** | N/A | **5.0 (Evaluate)** | **4.0 (Analyze)** |
| Nuance & Caveats | **7.0** | N/A | **8.0** | **7.0** |
| Practical Utility | **8.0** | N/A | **8.0** | **7.0** |
| **WEIGHTED AVERAGE** | **7.3** | **N/A** | **7.1** | **7.5** |

> *Claude Sonnet 4 excluded (0 output cells). OpenAI and Gemini both ran live; DeepSeek used mock. Scores above 4.0 for Bloom's reflect live LLM output demonstrating genuine evaluation.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    | oooooooooo O, G (live LLM -- genuine evaluation)
Level 4: Analyze     | oooooooooooo D (mock -- pre-authored analysis)
Level 3: Apply       |
Level 2: Understand  |
Level 1: Remember    |
```

OpenAI and Gemini reach Level 5 (Evaluate) through their live LLM outputs: both generate evaluations that assess proposal quality with numeric scores and judge which elements to combine in cross-pollination. DeepSeek reaches only Level 4 because its mock responses, while analytically structured, are pre-authored rather than demonstrating genuine evaluative reasoning.

---

## Head-to-Head: Key Differences

| Dimension | OpenAI GPT-4o (Live) | Gemini Flash 2.5 (Live) | DeepSeek V2 (Mock) |
|---|---|---|---|
| **Feedback style** | Flowing narrative paragraph | Numbered list with code refs | Flowing narrative paragraph (pre-authored) |
| **Feedback length** | 1141 chars | 1291 chars | 1345 chars |
| **Evaluation detail** | 3 dimensions + overall (8.67) | Overall only (5.0) | 3 dimensions + overall (6.5) |
| **Consensus rounds (test)** | 2 rounds, score 5.17 | 3 rounds (max), score 6.11 | 1 round, score 6.50 |
| **Consensus rounds (rubric)** | 1 round, score 5.00 | 3 rounds (max), score 6.00 | 1 round, score 6.50 |
| **Rubric synthesis length** | 2219 chars | 6401 chars | 2018 chars |
| **Cross-pollination style** | Structured framework with headers | Conversational with explicit reasoning | Structured with named criterion |
| **Feedback latency** | ~5 sec | ~27 sec | < 1 sec |
| **Total consensus time** | ~2 min | ~9 min | < 1 sec |

**OpenAI GPT-4o's strengths:** Fastest live responses (~5 sec for feedback). Only live provider returning full 3-dimension evaluation scores. Quick consensus convergence.

**OpenAI GPT-4o's weaknesses:** Consensus scores clustered at 5.0 (undifferentiated -- the LLM defaulted to middle-of-road scores). Rubric case study converged in 1 round with all proposals at 5.0, showing limited discriminative evaluation.

**Gemini Flash 2.5's strengths:** Numbered-list feedback format is pedagogically superior for code education. Most detailed rubric synthesis (6401 chars). Consensus showed genuine deliberation with score leadership rotating across rounds. Cross-pollination explicitly reasons about agent limitations.

**Gemini Flash 2.5's weaknesses:** Evaluation parsing failed (only `overall` returned, not the 3-dimension breakdown). Higher latency (~27 sec per feedback, ~9 min for consensus). Consensus did not converge within 3 rounds.

**DeepSeek V2's strengths:** Best-structured rubric (table format with Absent/Partial/Complete scale). Full 3-dimension evaluation. Instant execution. Most structured cross-pollination output with named criterion.

**DeepSeek V2's weaknesses:** Pre-authored responses -- does not demonstrate real LLM behavior. Mock consensus converges instantly with identical scores (no genuine deliberation).

---

## Visual Summary

### Overall Score Comparison

```
  Provider                   Score  Visual
  -------------------------  -----  ------------------------------
  DeepSeek V2 (Local, Mock)    7.5  ██████████████████████░░░░░░░░░
  OpenAI GPT-4o (Live)         7.3  █████████████████████░░░░░░░░░░
  Gemini Flash 2.5 (Live)      7.1  █████████████████████░░░░░░░░░░
  Claude Sonnet 4              N/A  (no saved outputs)
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     | O G (live LLM evaluation)
  L4 Analyze      | O G D
  L3 Apply        | O G D
  L2 Understand   | O G D
  L1 Remember     | O G D
```

Legend: **O** = OpenAI GPT-4o, **G** = Gemini Flash 2.5, **D** = DeepSeek V2

---

## Winner: DeepSeek V2 (Local) -- with important caveats

| | |
|---|---|
| **Chapter 15 Winner** | **DeepSeek V2 (Local)** |
| **Score** | **7.5 / 10** |
| **Bloom's Level** | **Level 4 -- Analyze** |

**Why DeepSeek wins on score:**
- Best-structured outputs (table-format rubric, named cross-pollination criterion)
- Full 3-dimension evaluation scores (matching OpenAI, exceeding Gemini)
- Clean execution with zero latency
- Highest source grounding (mock responses explicitly keyed to chapter concepts)

**Why this result should be interpreted carefully:**
- DeepSeek's scores reflect curated pre-authored responses, not actual LLM generation
- OpenAI and Gemini both demonstrate Level 5 (Evaluate) Bloom's taxonomy -- genuine evaluative reasoning that mock responses cannot replicate
- Gemini's 3-round consensus deliberation with rotating score leadership is more educationally valuable than DeepSeek's instant convergence at identical scores
- For real deployment, the live providers (OpenAI and Gemini) better represent actual system behavior

**Best live provider: OpenAI GPT-4o** -- faster responses, full multi-dimension evaluations, and adequate consensus convergence.

**Most realistic deployment demo: Gemini Flash 2.5** -- genuine multi-round deliberation, pedagogically superior numbered-list feedback, and the most detailed rubric synthesis.

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Live deployment (speed) | OpenAI GPT-4o | ~5 sec feedback, ~2 min consensus; full eval dimensions |
| Live deployment (pedagogy) | Gemini Flash 2.5 | Numbered-list feedback; genuine multi-round deliberation |
| Curated reference | DeepSeek V2 (Mock) | Pre-authored ideal outputs; best-structured rubric |
| Air-gapped / private | DeepSeek V2 (Local) | Zero cloud dependency |
| Multi-agent research | Gemini Flash 2.5 | Most realistic consensus dynamics (3 rounds, rotating leadership) |

## Provider Profiles for This Chapter

### OpenAI GPT-4o -- "The Fast Evaluator"
**Strengths:** Fastest live responses (~5 sec). Only live provider returning full 3-dimension evaluation scores (correctness=9.0, completeness=8.0, feasibility=9.0). Quick consensus convergence (2 rounds).
**Weaknesses:** Consensus scores clustered at 5.0 -- limited discrimination between proposals. Rubric case study converged in 1 round with undifferentiated scores. Feedback uses flowing paragraph rather than structured code-level references.

### Claude Sonnet 4 -- Not Evaluated
**Status:** 0 output cells saved. Notebook was not executed.

### Gemini Flash 2.5 -- "The Thorough Deliberator"
**Strengths:** Numbered-list feedback is pedagogically strongest for code education. Most detailed rubric synthesis (6401 chars). Consensus showed genuine deliberation with score leadership rotating each round (pedagogy -> domain -> assessment). Cross-pollination explicitly reasons about agent limitations.
**Weaknesses:** Evaluation parsing returned only `overall` score (lost 3 sub-dimensions). Higher latency (~27 sec per feedback, ~9 min consensus). Consensus did not converge within 3 rounds.

### DeepSeek V2 (Local) -- "The Structured Reference"
**Strengths:** Best-structured rubric (table format). Full 3-dimension evaluation. Fastest execution. Named cross-pollination criterion with clear provenance.
**Weaknesses:** Pre-authored responses -- no real LLM behavior. Mock consensus converges instantly with identical scores (no genuine deliberation). Only reaches Bloom's Level 4.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Adaptive tutoring feedback** | Gemini Flash 2.5 | Numbered-list format is best for code-focused pedagogy |
| **Multi-agent consensus** | Gemini Flash 2.5 | Genuine multi-round deliberation with rotating critique |
| **Evaluation scoring** | OpenAI GPT-4o | Only live provider returning full multi-dimension evaluations |
| **Rubric design** | DeepSeek V2 (reference) / Gemini (live) | Mock gives best structure; live gives most detailed synthesis |
| **Pipeline development** | DeepSeek V2 (Local) | Zero cost, instant iteration |

---

*Analysis based on Chapter 15 notebook outputs executed April 2026. OpenAI and Gemini both ran with live API calls, enabling genuine comparison. DeepSeek used mock responses. Claude had no saved outputs. Key differentiators: evaluation dimensionality, consensus convergence behavior, feedback formatting style, and rubric synthesis depth.*
