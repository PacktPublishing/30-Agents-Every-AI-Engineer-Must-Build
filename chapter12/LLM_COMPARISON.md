# Chapter 12 — LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 12 Ethical Agent tasks: ethical reasoning, explainable agents, bias detection, and compliance monitoring.

---

## Agent Tasks in This Chapter

- **Ethical Reasoning Agent** — Analyzing decisions through multiple ethical frameworks (utilitarian, deontological, virtue ethics)
- **Explainable Agent** — Providing transparent reasoning traces for agent decisions
- **Bias Detection Agent** — Identifying demographic and cognitive biases in data and model outputs
- **Compliance Agent** — Checking decisions against regulatory frameworks

## Scoring Dimensions

Each provider is rated 0–10 across eight dimensions:

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

## Key Observation: Deterministic Framework with LLM Ethical Reasoning

Chapter 12 uses a **deterministic compliance pipeline** with LLM-generated ethical analysis:
- **Bias detection metrics** (disparate impact ratios, statistical parity) are computed deterministically
- **Ethical framework application** is LLM-dependent — the model must reason about trade-offs between frameworks
- **Compliance checking** uses rule-based evaluation with LLM-generated explanations
- **Explainability traces** combine deterministic decision paths with LLM-generated natural language explanations

**Execution mode note:** Claude has saved outputs (17 output cells). Other notebooks may have limited output.

---

## Provider Performance

### Claude Sonnet 4

**Response characteristics:**
- Ethical reasoning: Applied multiple frameworks simultaneously with explicit tension identification
- Explainability: Detailed reasoning traces with causal chains
- Bias detection: Identified both statistical and cognitive biases with remediation suggestions
- Compliance: Mapped decisions to specific regulatory requirements

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Correct ethical framework applications; accurate bias metrics interpretation |
| Completeness | 10 | All ethical perspectives covered; cross-framework comparison |
| Structure & Organization | 10 | Structured ethical analysis with framework sections, tension identification |
| Conciseness | 7 | Thorough but verbose — ethics requires depth |
| Source Grounding | 9 | Follows chapter's multi-framework approach precisely |
| Bloom's Level | **5 — Evaluate** | Evaluated competing ethical claims and judged which framework is most applicable |
| Nuance & Caveats | 10 | Explicit tension between frameworks; acknowledged irreconcilable trade-offs |
| Practical Utility | 9 | Usable by ethics review boards for decision documentation |

---

### Gemini Flash 2.5

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct framework applications |
| Completeness | 7 | Covers main frameworks but less cross-referencing |
| Structure & Organization | 8 | Clean ethical analysis structure |
| Conciseness | 9 | Efficient ethical summaries |
| Source Grounding | 8 | Follows patterns |
| Bloom's Level | **4 — Analyze** | Analyzed decision through different ethical lenses |
| Nuance & Caveats | 6 | Some tension identification but less depth |
| Practical Utility | 7 | Good summary for quick ethical review |

> *Scores estimated from code structure and Gemini's cross-chapter performance.*

---

### DeepSeek V2 16B (Local)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | Basic ethical framework knowledge |
| Completeness | 5 | Tends to favor one framework over multi-perspective analysis |
| Structure & Organization | 6 | Basic analysis structure |
| Conciseness | 8 | Brief ethical assessments |
| Source Grounding | 6 | Partial framework coverage |
| Bloom's Level | **3 — Apply** | Applied single ethical framework without comparison |
| Nuance & Caveats | 3 | Limited acknowledgment of competing perspectives |
| Practical Utility | 5 | Too thin for ethics review use |

> *Scores estimated from code structure and DeepSeek's cross-chapter performance.*

---

### OpenAI GPT-4o

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Strong ethical reasoning accuracy |
| Completeness | 8 | Good multi-framework coverage |
| Structure & Organization | 8 | Well-organized ethical analysis |
| Conciseness | 8 | Balanced depth |
| Source Grounding | 8 | Follows chapter patterns |
| Bloom's Level | **5 — Evaluate** | Evaluates ethical trade-offs between frameworks |
| Nuance & Caveats | 8 | Good tension identification |
| Practical Utility | 8 | Useful for ethics documentation |

> *Scores estimated from code structure and GPT-4o's cross-chapter performance.*

---

## Overall Scorecard

| Dimension | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) | OpenAI GPT-4o |
|---|---|---|---|---|
| Factual Accuracy | **9.0** | **8.0** | **7.0** | **9.0** |
| Completeness | **10.0** | **7.0** | **5.0** | **8.0** |
| Structure & Organization | **10.0** | **8.0** | **6.0** | **8.0** |
| Conciseness | **7.0** | **9.0** | **8.0** | **8.0** |
| Source Grounding | **9.0** | **8.0** | **6.0** | **8.0** |
| Bloom's Taxonomy Level | **5.0 (Evaluate)** | **4.0 (Analyze)** | **3.0 (Apply)** | **5.0 (Evaluate)** |
| Nuance & Caveats | **10.0** | **6.0** | **3.0** | **8.0** |
| Practical Utility | **9.0** | **7.0** | **5.0** | **8.0** |
| **WEIGHTED AVERAGE** | **8.6** | **7.1** | **5.4** | **7.8** |

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    | ████████████ Claude Sonnet 4, OpenAI GPT-4o
Level 4: Analyze     | ████████████ Gemini Flash 2.5
Level 3: Apply       | ████████████ DeepSeek V2 (Local)
Level 2: Understand  |
Level 1: Remember    |
```

Ethical reasoning inherently requires evaluation (Level 5) — judging between competing ethical claims. Claude and GPT-4o both reach this level, with Claude being more explicit about irreconcilable tensions. Gemini analyzes through frameworks at Level 4. DeepSeek applies a single framework at Level 3.

---

## Provider Profiles for This Chapter

### Claude Sonnet 4 — "The Ethics Board"
**Strengths:** Multi-framework reasoning with explicit tension identification; best bias detection explanations; comprehensive compliance mapping.
**Weaknesses:** Verbose ethical analyses may be too detailed for quick decisions.

### OpenAI GPT-4o — "The Principled Advisor"
**Strengths:** Good ethical evaluation with balanced perspectives; clear trade-off articulation.
**Weaknesses:** Slightly less explicit about framework conflicts than Claude.

### Gemini Flash 2.5 — "The Quick Assessor"
**Strengths:** Fast ethical screening; efficient for high-volume compliance checking.
**Weaknesses:** Less depth in multi-framework comparison.

### DeepSeek V2 16B — "The Single Lens"
**Strengths:** Zero-cost local ethical screening; basic compliance checking.
**Weaknesses:** Tends toward single-framework analysis; limited nuance for complex ethical dilemmas.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Ethics review documentation** | Claude Sonnet 4 | Most comprehensive multi-framework analysis |
| **Compliance monitoring** | Claude or GPT-4o | Best at mapping decisions to regulations |
| **Bias detection** | Claude Sonnet 4 | Strongest at identifying subtle biases |
| **High-volume screening** | Gemini Flash 2.5 | Fast compliance checking at scale |
| **Local ethics testing** | Ollama DeepSeek V2 | Zero cost for basic ethical screening |

---

*Analysis based on Chapter 12 notebook outputs executed April 2026. Claude has saved outputs. Bias detection metrics are deterministic — LLM differentiation is in ethical reasoning and explanation quality.*
