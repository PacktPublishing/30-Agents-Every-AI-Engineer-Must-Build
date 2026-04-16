# Chapter 13 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 13 Healthcare and Scientific Discovery tasks: healthcare intelligence and scientific research agents.

---

## Agent Tasks in This Chapter

- **Healthcare Intelligence Agent** -- Medical literature synthesis, Bayesian diagnostic reasoning, clinical decision support with safety escalation
- **Scientific Discovery Agent** -- Fault-tolerant literature synthesis, information-theoretic knowledge gap detection, abductive hypothesis generation, closed-loop experimental feedback

## Scoring Dimensions

Each provider is rated 0--10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of medical/scientific claims and literature synthesis |
| **Completeness** | Coverage of relevant literature, clinical factors, and research dimensions |
| **Structure & Organization** | Quality of clinical reports and research syntheses |
| **Conciseness** | Appropriate depth for medical/scientific communication |
| **Source Grounding** | Adherence to evidence-based methodology from the chapter |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Handling of medical uncertainty, confidence intervals, limitations |
| **Practical Utility** | How useful outputs would be for clinicians or researchers |

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

## Key Observation: All Providers Produce Identical Simulation-Mode Outputs

Chapter 13 uses a **deterministic simulation pipeline** for all providers:

- All four notebooks (OpenAI, Claude, Gemini, DeepSeek) were executed in **live API mode** (API keys detected), but the agent code paths use deterministic simulation stubs regardless of the API key.
- The `MockLLM` response registry is identical across all four notebooks, containing the same 6 context-type responses (diagnostic, drug_interaction, patient_summary, literature_synthesis, knowledge_gap, hypothesis).
- `llm = None` in live mode -- the actual LLM client is never instantiated for agent calls.
- All deterministic components (Bayesian belief update, Platt-calibrated confidence scoring, FHIR normalization, safety escalation) produce byte-identical outputs across all 4 providers.

**Evidence:** All four notebooks show identical outputs:
- Bayesian posterior: urosepsis 0.412, pneumonia_sepsis 0.327, biliary_sepsis 0.136
- Safety escalation triggered for sepsis (confidence 0.82, threshold 0.15)
- Clinician explanation: "SAFETY ALERT -- Escalation required. Primary concern: Sepsis..."
- Patient explanation: "Your temperature, heart rate, and blood test results together suggest your body may be fighting a serious infection."
- 5 hypotheses generated, all passing min consistency (>=0.7) and testability (>=0.6) thresholds

**Because all four providers produce identical outputs, a meaningful per-provider comparison is not possible for this chapter.** The scores below reflect the shared simulation output quality.

---

## Shared Simulation Output Quality

The simulation outputs demonstrate:
- **Factual Accuracy:** Correct Bayesian inference mechanics, proper sepsis clinical presentation, appropriate drug interaction warnings (warfarin + aspirin bleeding risk)
- **Completeness:** Full diagnostic pipeline from FHIR normalization through Bayesian belief update, differential generation, confidence calibration, safety escalation, and audience-adapted explanation
- **Structure:** Professional clinical report format with SHAP-attributed clinician explanation, plain-language patient explanation, and immutable audit trail
- **Safety Awareness:** Escalation threshold of 0.15 correctly triggers for sepsis; 4 critical conditions monitored (myocardial_infarction, pulmonary_embolism, sepsis, stroke)
- **Scientific Rigor:** 5 hypotheses with consistency and testability scoring, closed-loop experimental feedback across 3 rounds

### Unified Score (All Providers)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct medical terminology, accurate Bayesian mechanics, proper drug interaction severity |
| Completeness | 8 | Full pipeline coverage; both healthcare and scientific agents demonstrated end-to-end |
| Structure & Organization | 9 | Excellent clinical report format; SHAP attribution for clinicians, plain language for patients |
| Conciseness | 7 | Appropriately detailed for medical context; some simulation scaffolding is verbose |
| Source Grounding | 9 | All outputs explicitly reference chapter sections (SS13.1-13.8); page numbers cited |
| Bloom's Level | **4 -- Analyze** | Pipeline analyzes clinical data through multiple lenses (Bayesian, safety, explanation) but does not evaluate trade-offs between approaches |
| Nuance & Caveats | 8 | Safety escalation with explicit thresholds; confidence calibration via Platt scaling; audit trail |
| Practical Utility | 7 | Good demonstration of architecture; would need live LLM integration for actual clinical use |

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|---|
| Factual Accuracy | **8.0** | **8.0** | **8.0** | **8.0** |
| Completeness | **8.0** | **8.0** | **8.0** | **8.0** |
| Structure & Organization | **9.0** | **9.0** | **9.0** | **9.0** |
| Conciseness | **7.0** | **7.0** | **7.0** | **7.0** |
| Source Grounding | **9.0** | **9.0** | **9.0** | **9.0** |
| Bloom's Taxonomy Level | **4.0 (Analyze)** | **4.0 (Analyze)** | **4.0 (Analyze)** | **4.0 (Analyze)** |
| Nuance & Caveats | **8.0** | **8.0** | **8.0** | **8.0** |
| Practical Utility | **7.0** | **7.0** | **7.0** | **7.0** |
| **WEIGHTED AVERAGE** | **7.5** | **7.5** | **7.5** | **7.5** |

> *All four providers produce byte-identical simulation outputs. Scores reflect shared output quality, not LLM differentiation.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     | oooooooooooo All Providers (identical simulation)
Level 3: Apply       |
Level 2: Understand  |
Level 1: Remember    |
```

The simulation pipeline reaches Level 4 (Analyze) through multi-dimensional clinical analysis (Bayesian belief update, differential generation, confidence calibration, safety escalation). It does not reach Level 5 because the simulation does not evaluate trade-offs between diagnostic approaches or weigh competing clinical evidence -- it follows a fixed pipeline.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  OpenAI GPT-4o          7.5  ██████████████████████░░░░░░░░░
  Claude Sonnet 4        7.5  ██████████████████████░░░░░░░░░
  Gemini Flash 2.5       7.5  ██████████████████████░░░░░░░░░
  DeepSeek V2 (Local)    7.5  ██████████████████████░░░░░░░░░
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     |
  L4 Analyze      | O C G D (all identical)
  L3 Apply        | O C G D
  L2 Understand   | O C G D
  L1 Remember     | O C G D
```

Legend: **O** = OpenAI GPT-4o, **C** = Claude Sonnet 4, **G** = Gemini Flash 2.5, **D** = DeepSeek V2

---

## Winner: Tie (All Providers)

| | |
|---|---|
| **Chapter 13 Winner** | **Tie -- All Providers** |
| **Score** | **7.5 / 10** |
| **Bloom's Level** | **Level 4 -- Analyze** |

**Why this is a tie:**
- All four provider notebooks produce byte-identical simulation outputs
- The `llm = None` in live mode means no actual LLM calls differentiate the providers
- The MockLLM response registry is the same 6-context set across all notebooks
- All deterministic pipeline components (Bayesian update, FHIR normalization, safety escalation) are code-identical

**To differentiate providers, this chapter would need:**
1. Live LLM integration for clinical narrative generation
2. Provider-specific interpretation of diagnostic results
3. Separate prompt-response evaluation outside the simulation framework

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality | Any (identical) | Simulation outputs are the same |
| Cost-efficient production | Gemini Flash 2.5 | Lowest per-token cost for equivalent output |
| Air-gapped / private data | DeepSeek V2 (Local) | Only option with zero cloud dependency |
| Rapid prototyping | DeepSeek V2 (Local) | No API key, instant iteration, zero cost |

## Provider Profiles for This Chapter

### All Providers -- "The Simulation Pipeline"
**Strengths:** Well-architected healthcare and scientific discovery pipeline; correct Bayesian mechanics; proper safety escalation; audience-adapted explanations; closed-loop hypothesis feedback.
**Weaknesses:** No live LLM differentiation; identical outputs make provider comparison impossible; simulation scaffolding adds verbosity.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Clinical decision support** | Any -- then add live LLM | Pipeline architecture is identical; live LLM quality would differentiate |
| **Literature synthesis** | Any -- then add live LLM | Simulation stubs return identical literature cluster data |
| **Research triage** | Gemini Flash 2.5 | Lowest cost for equivalent simulation output |
| **Hypothesis generation** | Any -- then add live LLM | Simulation returns identical 5-hypothesis set |
| **Pipeline development** | Ollama DeepSeek V2 | Zero cost, identical functionality |

> **Safety Note:** No LLM output should be used for actual clinical decisions without human expert review. The simulation outputs demonstrate pipeline architecture only -- live LLM integration would be required for any clinical deployment.

---

*Analysis based on Chapter 13 notebook outputs executed April 2026. All four providers (OpenAI, Claude, Gemini, DeepSeek) produce identical simulation-mode outputs. The retrieval pipeline, Bayesian inference, and safety escalation are entirely deterministic. No live LLM calls were made in any notebook.*
