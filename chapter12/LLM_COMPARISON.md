# Chapter 12 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 12 Ethical Agent tasks: deontic logic, ethical reasoning, EU AI Act compliance, bias detection, and fair hiring.

---

## Agent Tasks in This Chapter

- **Deontic Operator Verification** -- Testing obligatory, permitted, and forbidden operators with axiom propagation
- **Ethical Reasoning Agent** -- Principle-based action checking (human rights, accountability) with mitigation
- **EU AI Act Compliance** -- Seven-requirement compliance checking with regression detection
- **Bias Detection and Monitoring** -- Disparate impact ratio, demographic parity, equal opportunity metrics
- **Fair Hiring Agent** -- LLM-assisted candidate evaluation with bias mitigation (reweighting) and anonymization

## Scoring Dimensions

Each provider is rated 0-10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of ethical framework applications and bias identification |
| **Completeness** | Coverage of all ethical perspectives and compliance dimensions |
| **Structure & Organization** | Quality of ethical analysis reports and reasoning traces |
| **Conciseness** | Appropriate depth without unnecessary philosophical tangents |
| **Source Grounding** | Adherence to the chapter's ethical reasoning frameworks |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Handling of ethical trade-offs, conflicting principles, and edge cases |
| **Practical Utility** | How useful outputs would be for ethics review boards or compliance teams |

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

## Key Observation: Deterministic Pipeline -- LLM Not Invoked for Ethical Reasoning

Chapter 12 implements a **fully deterministic ethical reasoning pipeline**. Every component is rule-based:

1. **Deontic operators**: Pure logic -- `O(phi)`, `P(phi)`, `F(phi)` with axiom propagation. Zero LLM involvement.
2. **Ethical Reasoning Agent**: Keyword-based principle checking with string-match violation detection. Zero LLM involvement.
3. **EU AI Act compliance**: Static requirement checkers with threshold-based pass/fail. Zero LLM involvement.
4. **Bias detection**: Statistical computation -- disparate impact ratio, demographic parity, equal opportunity. Zero LLM involvement.
5. **Bias monitoring pipeline**: Sliding-window metric emission with threshold alerting. Zero LLM involvement.
6. **Fair Hiring Agent**: Uses `MockLLM` for candidate evaluation even in "Live Mode" notebooks -- confirmed by the log line `MockLLM initialized with 7 handler methods` appearing in all four provider outputs.

**Critical finding:** Although three providers (Claude, Gemini, OpenAI) successfully initialized in Live Mode (confirmed by "API key detected -- provider: X. Live Mode enabled"), the ethical reasoning pipeline never calls the live LLM. The FairHiringAgent explicitly instantiates MockLLM regardless of provider setting. All four notebooks produce functionally identical outputs, differing only in timestamps and provider name strings.

**Note on ch12_02:** Only `ch12_01_ethical_reasoning_agent` has provider-specific notebooks. `ch12_02_explainable_agent` exists only as a Simulation notebook, so explainability analysis is excluded from this comparison.

---

## Provider Execution Status

| Provider | Output Cells | Declared Mode | Actual LLM Usage |
|---|---|---|---|
| Claude Sonnet 4 | 14 | Live Mode (Anthropic) | MockLLM for FairHiringAgent; all else deterministic |
| Gemini Flash 2.5 | 14 | Live Mode (Google) | MockLLM for FairHiringAgent; all else deterministic |
| OpenAI GPT-4o | 14 | Live Mode (OpenAI) | MockLLM for FairHiringAgent; all else deterministic |
| DeepSeek V2 16B | 14 | Fallback (Ollama key missing) | MockLLM for FairHiringAgent; all else deterministic |

**DeepSeek note:** The Ollama notebook logged `LLM_PROVIDER=ollama but OLLAMA_API_KEY not set. Falling back.` It then fell back to using the OpenAI key, which initialized Live Mode -- but this is irrelevant since the pipeline never calls the LLM.

---

## Observed Outputs (Functionally Identical Across All Four Providers)

### Deontic Operator Verification (Cell 3)
- Three operators verified: `O(phi)` = obligatory+permitted, `P(phi)` = permitted only, `F(phi)` = forbidden only
- Three axioms verified: `O(prioritize_emergency) <-> F(omit_prioritize_emergency)`, `P(adjust_crosswalk) <-> not F(adjust_crosswalk)`, conditional obligation propagation
- Pure logic computation -- zero LLM involvement

### Ethical Consistency Theorem (Cell 5)
- `a1` (general explanation): consistent=True, permitted=True
- `a2` (share medical details): consistent=False, permitted=False, blocked by `['share_medical_details']`
- Rule-based consistency check against policy set

### Ethical Reasoning Agent (Cells 7-8)
- Compliant action (`send_general_explanation_to_patient`): passes all 5 ethical checks, severity: LOW
- Single violation (`share_medical_details with external employer`): human_rights violation, severity: HIGH, mitigated to `[REDACTED]`
- Multi-violation (`bypass_consent and disable_audit to share_medical_details externally`): 2 violations (human_rights, accountability), mitigated
- Audit log: 3 entries recorded

### EU AI Act Compliance (Cell 10)
- Initial state: COMPLIANT (7/7 requirements met)
- After regression: NON_COMPLIANT (5/7) -- `transparency` and `diversity_fairness` failing
- Failure details: "Explanation generation timeout for 12% of decisions" and "Disparate impact ratio dropped to 0.73"

### Bias Detection (Cells 14-15)
- Dataset: 200 synthetic HR candidates. Gender distribution: female=81, male=111, non_binary=8
- Qualification rates: female=0.4815, male=0.6667 -- clear disparity
- Disparate Impact Ratio: 0.642 (below four-fifths rule threshold of 0.8)
- Severity: HIGH. Demographic parity difference: 0.2685
- Recommendations: reweighting, anonymization review, threshold adjustment per group

### Bias Monitoring Pipeline (Cell 18)
- 200 decisions streamed through sliding-window monitor
- 2 CRITICAL alerts: DI=0.785 and DI=0.708 (both below 0.8 threshold)

### Fair Hiring Agent (Cells 20-22)
- MockLLM evaluates 200 candidates for "Senior Data Scientist"
- Bias detected (severity=HIGH), FairnessEnforcer applies reweighting
- Anonymization removes `education_institution` and `gender` fields
- Mitigation result: DI improved from 0.732 to 2.136 (above 0.8 threshold)
- 1 audit trail entry recorded

---

## Scoring

Because the entire pipeline is deterministic and all providers produce functionally identical outputs (differing only in timestamps), individual provider scoring is not meaningful. A single pipeline quality assessment applies:

### Pipeline Quality Assessment (Applies to All Providers)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Deontic logic operators are formally correct with proper axiom verification. Bias metrics (DI=0.642, demographic parity difference=0.2685) are computed accurately against the synthetic dataset. The four-fifths rule violation is correctly identified. EU AI Act requirements map to real regulatory categories. |
| Completeness | 8 | Covers six distinct ethical analysis tasks: deontic logic, consistency theorem, principle-based reasoning, EU AI Act compliance (7 requirements), three fairness metrics, monitoring pipeline, mitigation, and anonymization. Missing: ch12_02 explainable agent (separate notebook with only simulation version). |
| Structure & Organization | 8 | Well-structured severity-coded logging (SUCCESS/ERROR/WARNING). Audit trails with timestamped entries. Compliance status reports with pass/fail per requirement. Monitoring pipeline emits Prometheus-style gauge metrics. |
| Conciseness | 7 | Most sections are appropriately concise. The FairnessEnforcer reweighting section is verbose -- logs individual score adjustments for each candidate, which could be summarized. Bias detection output is well-scoped. |
| Source Grounding | 9 | Faithfully implements the chapter's ethical frameworks: deontic operators from Standard Deontic Logic, EU AI Act seven-requirement structure, EEOC four-fifths rule for disparate impact, and the Amazon HR bias case study reference. |
| Bloom's Level | **4 -- Analyze** | The pipeline analyzes decisions through multiple ethical lenses (human rights, accountability, transparency, fairness, privacy) and identifies which principles conflict. It also analyzes bias across demographic groups using multiple statistical measures. However, all analysis is rule-based, not LLM-reasoned. |
| Nuance & Caveats | 7 | The impossibility theorem visualization demonstrates trade-offs between fairness criteria (individual fairness vs. group fairness vs. calibration). Recommendations include multiple mitigation strategies. However, nuance is pre-authored and deterministic, not dynamically generated. |
| Practical Utility | 8 | The bias detection and monitoring pipeline is production-grade. Disparate impact alerts with configurable thresholds, sliding-window monitoring, anonymization layer, and audit trails are directly useful for compliance teams. The DI improvement from 0.732 to 2.136 demonstrates measurable mitigation effectiveness. |

**Pipeline Weighted Average: 7.6 / 10**

---

## Overall Scorecard

| Dimension | Claude Sonnet 4 | Gemini Flash 2.5 | OpenAI GPT-4o | DeepSeek V2 |
|---|---|---|---|---|
| All dimensions | Deterministic | Deterministic | Deterministic | Deterministic |
| **WEIGHTED AVERAGE** | 7.6 | 7.6 | 7.6 | 7.6 |

> *All four providers produce functionally identical outputs. The ethical reasoning pipeline is entirely deterministic. Scores reflect pipeline quality, not provider capability.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     | ############ Deterministic pipeline (all providers)
Level 3: Apply       |
Level 2: Understand  |
Level 1: Remember    |
```

The pipeline reaches Level 4 (Analyze) through multi-framework ethical analysis -- evaluating actions against human rights, accountability, transparency, fairness, and privacy principles, then identifying conflicts and computing statistical bias measures across demographic groups. This analysis is rule-based and mathematically grounded rather than LLM-generated.

---

## Visual Summary

### Execution Status

```
  Provider              Outputs  Declared Mode     Actual LLM Usage
  --------------------  -------  ----------------  ----------------
  Claude Sonnet 4          14   Live (Anthropic)   MockLLM / deterministic
  Gemini Flash 2.5         14   Live (Google)      MockLLM / deterministic
  OpenAI GPT-4o            14   Live (OpenAI)      MockLLM / deterministic
  DeepSeek V2 (Local)      14   Fallback (Ollama)  MockLLM / deterministic
```

---

## Winner: No Winner -- Pipeline Is Provider-Agnostic by Design

| | |
|---|---|
| **Chapter 12 Winner** | **No winner declared** |
| **Reason** | All providers produce functionally identical outputs from a deterministic pipeline |

This is an intentional design choice. Ethical guardrails, bias metrics, and compliance checks should be mathematically grounded and deterministic -- they should not depend on which LLM is answering. The deontic logic is formally verified, the bias statistics use established metrics (EEOC four-fifths rule), and the EU AI Act requirements map to specific regulatory categories. An LLM generating different ethical judgments per provider would be a liability, not an advantage.

### Where LLMs Would Add Value (If Pipeline Were Extended)

The current pipeline handles detection and metric computation. LLMs could enhance the following areas:

| Extension | LLM Value | Why |
|---|---|---|
| Natural language explanations | High | Generating human-readable justifications for why a decision was flagged |
| Ethical dilemma reasoning | High | Analyzing novel scenarios not covered by keyword rules |
| Counterfactual analysis | Medium | "What would change if we adjusted the DI threshold to 0.85?" |
| Stakeholder impact narratives | Medium | Describing how mitigation affects different demographic groups |
| Policy recommendation synthesis | High | Combining multiple metric violations into actionable policy changes |

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Bias detection and monitoring | Any provider | Pipeline is fully deterministic |
| EU AI Act compliance | Any provider | Rule-based requirement checking |
| Ethical reasoning | Any provider | Principle matching is keyword-based |
| Production deployment | Any cloud provider | For audit trail persistence and alerting infrastructure |
| Air-gapped compliance | DeepSeek V2 (Local) | Zero cloud dependency for processing sensitive HR data |
| Explainability extension | Re-run ch12_02 with live providers | Only simulation notebook exists |

---

## Recommendations

| Use Case | Recommended Action | Why |
|---|---|---|
| **Comparing ethical reasoning quality** | Extend pipeline to use live LLM for dilemma analysis | Current pipeline does not invoke LLM for ethical reasoning |
| **Bias monitoring in production** | Use pipeline as-is | Deterministic metrics are more reliable than LLM-based bias detection |
| **Compliance auditing** | Use pipeline as-is | Rule-based checking is appropriate and auditable for regulatory compliance |
| **Explainability analysis** | Create provider-specific notebooks for ch12_02 | Only simulation version exists; explainable agent would benefit from live LLM comparison |
| **Fair hiring evaluation** | Replace MockLLM with live provider in FairHiringAgent | Current implementation hardcodes MockLLM even in Live Mode |

---

*Analysis based on Chapter 12 notebook execution outputs, April 2026. All four provider notebooks were executed. Three (Claude, Gemini, OpenAI) initialized in Live Mode; DeepSeek fell back due to missing Ollama key. However, the ethical reasoning pipeline is entirely deterministic -- the live LLM is never called. The FairHiringAgent uses MockLLM for all providers. All outputs are functionally identical, differing only in timestamps. No meaningful LLM provider comparison is possible from current data.*
