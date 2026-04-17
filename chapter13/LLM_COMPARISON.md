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

## Key Observation: Deterministic Simulation Pipeline with Provider-Agnostic Outputs

All four provider notebooks were executed with live API keys detected:

- **OpenAI GPT-4o**: "Live API mode active. Key loaded (ends ...RNQA)." / "Live OpenAI LLM client initialized (gpt-4o)."
- **Claude Sonnet 4**: "Live API mode active. Key loaded (ends ...tAAA)." / "Live Anthropic LLM client initialized (claude-sonnet-4-20250514)."
- **Gemini Flash 2.5**: "Live API mode active. Key loaded (ends ...s9hA)." / "Live Gemini LLM client initialized (gemini-2.5-flash)."
- **DeepSeek V2 16B**: "SIMULATION MODE ACTIVE" / "MockLLM initialized with 6-context response registry."

Despite three providers initializing live LLM clients, the chapter's agent pipeline uses deterministic simulation stubs for all substantive outputs. The live LLM client is instantiated but never called for the core healthcare/scientific tasks. All diagnostic reasoning, FHIR normalization, safety escalation, literature synthesis, knowledge gap detection, hypothesis generation, and experimental feedback use hard-coded simulation paths that produce identical results regardless of provider.

**Evidence of identical substantive outputs across all four providers:**
- Bayesian posterior: urosepsis 0.412, pneumonia_sepsis 0.327, biliary_sepsis 0.136, viral_syndrome 0.080, dehydration 0.045
- Safety escalation: 8 critical alerts for urosepsis (confidence 0.70) and pneumonia_sepsis (confidence 0.24)
- Knowledge gaps: 3 detected -- block copolymer architectures (composite 0.817), humidity-dependent degradation (0.73), long-term creep behavior (0.653)
- Hypotheses: 5 generated with consistency >= 0.70 and testability >= 0.60
- Closed-loop feedback: error reduction 11.1% -> 3.8% -> 1.0% across 3 rounds

The only differences between provider notebooks are initialization messages (API key suffix, client name, provider label in log lines). No LLM-generated content varies.

---

## Shared Simulation Output Quality

The simulation outputs demonstrate:
- **Factual Accuracy:** Correct Bayesian inference mechanics; proper sepsis clinical presentation (tachycardia, hypotension, fever); appropriate drug interaction warnings (warfarin + aspirin bleeding risk, evidence grade 1A)
- **Completeness:** Full diagnostic pipeline from FHIR normalization through Bayesian belief update, differential generation, Platt-calibrated confidence scoring, safety escalation, and audience-adapted explanation (clinician + patient)
- **Structure:** Professional clinical report format; SHAP-attributed clinician explanation; plain-language patient explanation ("Your temperature, heart rate, and blood test results together suggest your body may be fighting a serious infection"); immutable audit trail with hash
- **Safety Awareness:** Escalation threshold of 0.15 correctly triggers for sepsis-related conditions; 4 critical conditions monitored (myocardial_infarction, pulmonary_embolism, sepsis, stroke)
- **Scientific Rigor:** Literature scan across 4 databases (PubMed, arXiv, Scopus, IEEE) with 15 papers in 5 thematic clusters; 3 knowledge gaps via 3 detection strategies (negative space, cross-domain, temporal trend); 5 hypotheses with abductive reasoning; closed-loop experimental feedback across 3 rounds showing prediction refinement

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

> *All four providers produce identical simulation outputs. Scores reflect shared output quality, not LLM differentiation.*

### Score Rationale

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct Bayesian mechanics (posterior sums to 1.0); accurate sepsis presentation; proper drug interaction severity (warfarin + aspirin = high bleeding risk). Deducted 2 for simulation-only data (no real literature retrieval). |
| Completeness | 8 | Full pipeline coverage: FHIR normalization, Bayesian belief update, differential generation, confidence calibration, safety escalation, audience-adapted explanation, literature synthesis, gap detection, hypothesis generation, experimental feedback. Both healthcare and scientific agents demonstrated end-to-end. |
| Structure & Organization | 9 | Excellent clinical report format with clear sections; SHAP attribution for clinicians; plain language for patients; well-structured knowledge gap report with composite scores. |
| Conciseness | 7 | Appropriately detailed for medical context; simulation scaffolding (46 mock stub classes, 9 mock datasets) adds verbosity to execution trace. |
| Source Grounding | 9 | All outputs explicitly reference chapter sections (SS13.1--13.8); page numbers cited (pp. 367, 374--375, 387). |
| Bloom's Level | 4 (Analyze) | Pipeline analyzes clinical data through multiple lenses (Bayesian, safety, explanation); hypothesis generator analyzes gaps across domains. Does not evaluate trade-offs between diagnostic approaches. |
| Nuance & Caveats | 8 | Safety escalation with explicit thresholds (0.15); confidence calibration via Platt scaling; audit trail with hash; guideline conflict flagged rather than auto-resolved ("agent amplifies clinical judgment rather than replacing it"). |
| Practical Utility | 7 | Good demonstration of architecture; closed-loop feedback shows prediction refinement. Would need live LLM integration for actual clinical use. |

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

The simulation pipeline reaches Level 4 (Analyze) through multi-dimensional clinical analysis (Bayesian belief update across 5 diagnoses, safety escalation across 4 critical conditions, knowledge gap detection via 3 strategies). It does not reach Level 5 because the simulation follows a fixed pipeline without evaluating trade-offs between diagnostic approaches or weighing competing clinical evidence.

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
- All four provider notebooks produce identical simulation outputs for all substantive agent tasks
- The live LLM client is instantiated for OpenAI, Claude, and Gemini but never called for core agent operations
- DeepSeek runs in explicit simulation mode with MockLLM, producing the same results
- All deterministic pipeline components (Bayesian update, FHIR normalization, safety escalation, literature scan, gap detection, hypothesis generation, experimental feedback) are code-identical

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality | Any (identical) | Simulation outputs are the same |
| Cost-efficient production | Gemini Flash 2.5 | Lowest per-token cost for equivalent output |
| Air-gapped / private data | DeepSeek V2 (Local) | Only option with zero cloud dependency |
| Rapid prototyping | DeepSeek V2 (Local) | No API key needed, instant iteration, zero cost |

## Provider Profiles for This Chapter

### All Providers -- "The Simulation Pipeline"
**Strengths:** Well-architected healthcare and scientific discovery pipeline; correct Bayesian mechanics; proper safety escalation with configurable thresholds; audience-adapted explanations (clinician vs. patient); closed-loop hypothesis feedback with error reduction demonstration.
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

*Analysis based on Chapter 13 notebook outputs executed April 2026. All four providers (OpenAI, Claude, Gemini, DeepSeek) produce identical simulation-mode agent outputs despite three having live API clients initialized. The retrieval pipeline, Bayesian inference, safety escalation, and scientific discovery components are entirely deterministic.*
