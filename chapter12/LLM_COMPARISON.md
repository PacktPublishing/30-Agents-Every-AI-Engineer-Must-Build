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

## Key Observation: Deterministic Pipeline Dominates -- LLM Minimally Involved

Chapter 12 uses a **heavily deterministic ethical reasoning pipeline**. The core components are all rule-based:

1. **Deontic operators**: Pure logic -- `O(phi)`, `P(phi)`, `F(phi)` with axiom propagation (zero LLM involvement)
2. **Ethical reasoning agent**: Keyword-based principle checking with string-match violation detection (zero LLM involvement)
3. **EU AI Act compliance**: Static requirement checkers with threshold-based pass/fail (zero LLM involvement)
4. **Bias detection**: Statistical computation -- disparate impact ratio, demographic parity, equal opportunity (zero LLM involvement)
5. **Bias monitoring pipeline**: Sliding-window metric emission with threshold alerting (zero LLM involvement)
6. **Fair Hiring Agent**: Uses MockLLM for candidate evaluation even in "Live Mode" notebooks -- all providers use `MockLLM initialized with 7 handler methods`

**Critical finding:** Even the three "Live Mode" notebooks (Claude, Gemini, DeepSeek) use MockLLM for the FairHiringAgent. The LLM provider key enables Live Mode initialization, but the actual ethical reasoning pipeline is entirely deterministic. The only differences between notebook outputs are timestamps.

---

## Provider Execution Status

| Provider | Output Cells | Mode | Actual LLM Usage |
|---|---|---|---|
| Claude Sonnet 4 | 14 | Live Mode (Anthropic) | MockLLM for FairHiringAgent |
| Gemini Flash 2.5 | 14 | Live Mode (Google) | MockLLM for FairHiringAgent |
| DeepSeek V2 16B | 14 | Live Mode (Ollama) | MockLLM for FairHiringAgent |
| OpenAI GPT-4o | 14 | Simulation Mode | MockLLM for FairHiringAgent |

**Note on Ch12 notebooks:** Only `ch12_01_ethical_reasoning_agent` has provider notebooks. `ch12_02_explainable_agent` only has a Simulation notebook.

---

## Observed Outputs (Functionally Identical Across All Providers)

### Deontic Operator Verification (Cell 3)
- All three axioms verified: `O(prioritize_emergency) <-> F(omit_prioritize_emergency)`, `P(adjust_crosswalk) <-> not F(adjust_crosswalk)`, conditional obligation propagation
- Output is pure logic -- identical across all providers

### Ethical Consistency Theorem (Cell 5)
- `a1` (general explanation): consistent=True, permitted=True
- `a2` (share medical details): consistent=False, permitted=False, blocked
- Identical across all providers

### Ethical Reasoning Agent (Cells 7-8)
- Compliant action (`send_general_explanation_to_patient`): passes all 5 ethical checks
- Single violation (`share_medical_details with external employer`): human_rights violation, mitigated to `[REDACTED]`
- Multi-violation (`bypass_consent and disable_audit to share_medical_details`): 2 violations (human_rights, accountability), mitigated
- Audit log: 3 entries recorded -- identical across all providers

### EU AI Act Compliance (Cell 10)
- Initial: COMPLIANT (7/7)
- After regression: NON_COMPLIANT (5/7) -- transparency and diversity_fairness failing
- Failure details: "Explanation generation timeout for 12% of decisions" and "Disparate impact ratio dropped to 0.73"
- Identical across all providers

### Bias Detection (Cells 14-15)
- Dataset: 200 candidates, gender distribution: female=81, male=111, non_binary=8
- Disparate Impact Ratio: 0.7321 (female/male) -- VIOLATION of four-fifths rule
- Severity: HIGH. DI=0.642, demographic parity difference=0.2685
- Recommendations: reweighting, anonymization review, threshold adjustment per group
- Identical across all providers

### Bias Monitoring Pipeline (Cell 18)
- 2 CRITICAL alerts fired: DI=0.785 and DI=0.708 (both below 0.8 threshold)
- Identical across all providers

### Fair Hiring Agent (Cells 20-22)
- MockLLM used by ALL providers (including "Live" ones)
- 200 candidates evaluated for "Senior Data Scientist"
- Bias detected (severity=HIGH), FairnessEnforcer applies reweighting
- Anonymization removes `education_institution` and `gender` fields
- Mitigation effective: DI improved from 0.732 to 2.136
- Identical across all providers

---

## Scoring

Because the entire ethical reasoning pipeline is deterministic and all providers produce functionally identical outputs (differing only in timestamps), individual provider scoring is not meaningful.

### Pipeline Quality Assessment (Applies to All Providers)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Deontic logic is formally correct. Bias metrics (DI, demographic parity, equal opportunity) are computed accurately. Four-fifths rule violation correctly identified at DI=0.7321. |
| Completeness | 8 | Covers deontic logic, principle-based reasoning, EU AI Act (7 requirements), three fairness metrics, monitoring pipeline, mitigation, and anonymization. Only missing: explainable agent (separate notebook). |
| Structure & Organization | 8 | Well-structured audit trails, severity-coded logging, and clear compliance status reports. The monitoring pipeline emits Prometheus-style gauges. |
| Conciseness | 7 | Some sections (reweighting log) are verbose -- 20+ FairnessEnforcer lines for individual score adjustments. Could summarize. |
| Source Grounding | 9 | Faithfully implements the chapter's ethical frameworks -- deontic operators from SDL, EU AI Act requirements, EEOC four-fifths rule. |
| Bloom's Level | **4 -- Analyze** | The pipeline analyzes decisions through multiple ethical lenses (human rights, accountability, transparency, fairness) and identifies conflicts. But analysis is rule-based, not LLM-reasoned. |
| Nuance & Caveats | 7 | The impossibility theorem visualization shows trade-offs between fairness criteria. Recommendations include multiple mitigation strategies. But nuance is pre-authored, not dynamically generated. |
| Practical Utility | 8 | The bias detection and monitoring pipeline is production-grade. Disparate impact alerts, audit trails, and anonymization are directly useful for compliance teams. |

**Pipeline Weighted Average: 7.6 / 10**

---

## Overall Scorecard

| Dimension | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 | OpenAI GPT-4o |
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

The pipeline reaches Level 4 (Analyze) through multi-framework ethical analysis -- checking actions against human rights, accountability, transparency, fairness, and privacy principles, then identifying which principles conflict. However, this analysis is rule-based rather than LLM-generated.

---

## Visual Summary

### Execution Status

```
  Provider              Outputs  Declared Mode   Actual LLM Usage
  --------------------  -------  -------------   ----------------
  Claude Sonnet 4          14   Live (Anthropic)  MockLLM
  Gemini Flash 2.5         14   Live (Google)     MockLLM
  DeepSeek V2 (Local)      14   Live (Ollama)     MockLLM
  OpenAI GPT-4o            14   Simulation        MockLLM
```

---

## Winner: No Winner -- Pipeline Is Provider-Agnostic

| | |
|---|---|
| **Chapter 12 Winner** | **No winner declared** |
| **Reason** | All providers produce identical outputs from a deterministic pipeline |

The ethical reasoning pipeline in Chapter 12 is **designed to be provider-agnostic**. This is actually a strength -- ethical guardrails should not depend on which LLM is behind them. The deontic logic, bias metrics, and compliance checks are mathematically grounded and deterministic.

### Where LLMs Would Differentiate (If Pipeline Were Extended)

1. **Ethical dilemma analysis**: Asking the LLM to reason about trolley-problem-style trade-offs
2. **Natural language explanations**: Generating human-readable justifications for compliance decisions
3. **Counterfactual reasoning**: "What would change if we lowered the threshold?"
4. **Stakeholder impact assessment**: Analyzing how decisions affect different groups

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Bias detection | Any provider | Pipeline is deterministic |
| EU AI Act compliance | Any provider | Rule-based checking |
| Ethical reasoning | Any provider | Principle matching is keyword-based |
| Production deployment | Any cloud provider | For audit trail persistence and monitoring |
| Air-gapped compliance | DeepSeek V2 (Local) | Zero cloud dependency for sensitive data |

---

## Recommendations

| Use Case | Recommended Action | Why |
|---|---|---|
| **Comparing ethical reasoning** | Integrate LLM for dilemma analysis | Current pipeline does not use LLM for ethical reasoning |
| **Bias monitoring** | Use pipeline as-is | Deterministic metrics are more reliable than LLM-based detection |
| **Compliance auditing** | Use pipeline as-is | Rule-based checking is appropriate for regulatory compliance |
| **Explainability** | Run ch12_02 with live providers | Only simulation notebook exists for explainable agent |

---

*Analysis based on Chapter 12 notebook execution outputs, April 2026. Three providers (Claude, Gemini, DeepSeek) ran in Live Mode but the ethical reasoning pipeline uses MockLLM for all LLM calls. OpenAI ran in Simulation Mode. All four providers produce functionally identical outputs differing only in timestamps. The pipeline is intentionally deterministic -- ethical guardrails should be mathematically grounded, not LLM-dependent.*
