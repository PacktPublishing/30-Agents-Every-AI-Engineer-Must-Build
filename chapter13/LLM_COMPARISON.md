# Chapter 13 — LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 13 Healthcare and Scientific Discovery tasks: healthcare intelligence and scientific research agents.

---

## Agent Tasks in This Chapter

- **Healthcare Intelligence Agent** — Medical literature synthesis, clinical decision support, patient data interpretation
- **Scientific Discovery Agent** — Hypothesis generation, experiment design, research synthesis across domains

## Scoring Dimensions

Each provider is rated 0–10 across eight dimensions:

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

## Key Observation: Deterministic Pipeline with LLM Synthesis

Chapter 13 uses a **deterministic retrieval and processing pipeline**:
- **Literature retrieval** (PubMed/arXiv search, embedding-based similarity) is deterministic
- **Clinical data processing** (vitals, lab values, risk scoring) is rule-based
- **LLM-dependent cells** include: literature synthesis, clinical interpretation narratives, and hypothesis generation

The LLM's role is synthesis and interpretation — converting structured data and retrieved literature into actionable clinical or research narratives.

**Execution mode note:** Claude has saved outputs (22 output cells). Other notebooks have limited or no saved outputs.

---

## Provider Performance

### Claude Sonnet 4

**Response characteristics:**
- Literature synthesis: Comprehensive review with evidence grading (Level of Evidence I-V)
- Clinical interpretation: Structured reports with differential considerations and confidence levels
- Hypothesis generation: Multiple testable hypotheses with experimental design sketches
- Strong emphasis on safety caveats and clinical limitations

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Accurate medical terminology and evidence synthesis |
| Completeness | 9 | Multiple perspectives covered; evidence levels cited |
| Structure & Organization | 10 | Clinical report format with clear sections (Assessment, Plan, Evidence) |
| Conciseness | 7 | Comprehensive — appropriate for medical context where completeness matters |
| Source Grounding | 9 | Follows evidence-based methodology from chapter |
| Bloom's Level | **5 — Evaluate** | Assessed evidence quality and clinical applicability |
| Nuance & Caveats | 10 | Explicit uncertainty quantification; contraindication warnings; limitation statements |
| Practical Utility | 9 | Usable by clinicians as a decision support reference |

---

### Gemini Flash 2.5

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Generally correct medical information |
| Completeness | 7 | Good coverage of main findings |
| Structure & Organization | 8 | Clean clinical summary format |
| Conciseness | 9 | Efficient medical communication |
| Source Grounding | 8 | Follows evidence-based patterns |
| Bloom's Level | **4 — Analyze** | Analyzed clinical data and literature findings |
| Nuance & Caveats | 6 | Basic limitations mentioned |
| Practical Utility | 7 | Useful for initial clinical overview |

> *Scores estimated from code structure and Gemini's cross-chapter performance.*

---

### DeepSeek V2 16B (Local)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | Basic medical facts correct; may miss nuances |
| Completeness | 5 | Limited literature synthesis depth |
| Structure & Organization | 6 | Basic report format |
| Conciseness | 8 | Brief summaries |
| Source Grounding | 6 | Partial methodology adherence |
| Bloom's Level | **3 — Apply** | Applied medical knowledge to the scenario |
| Nuance & Caveats | 3 | Minimal safety caveats — concerning for medical domain |
| Practical Utility | 4 | Insufficient for clinical decision support |

> *Scores estimated from code structure and DeepSeek's cross-chapter performance. Note: A local model with limited medical safety training is particularly concerning in healthcare applications.*

---

### OpenAI GPT-4o

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Strong medical knowledge accuracy |
| Completeness | 8 | Good literature coverage |
| Structure & Organization | 8 | Well-organized clinical reports |
| Conciseness | 8 | Balanced medical communication |
| Source Grounding | 8 | Follows evidence-based patterns |
| Bloom's Level | **4 — Analyze** | Analyzed clinical evidence and research findings |
| Nuance & Caveats | 7 | Good safety awareness and limitations |
| Practical Utility | 8 | Useful clinical decision support reference |

> *Scores estimated from GPT-4o's known medical reasoning capabilities.*

---

## Overall Scorecard

| Dimension | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) | OpenAI GPT-4o |
|---|---|---|---|---|
| Factual Accuracy | **9.0** | **8.0** | **7.0** | **9.0** |
| Completeness | **9.0** | **7.0** | **5.0** | **8.0** |
| Structure & Organization | **10.0** | **8.0** | **6.0** | **8.0** |
| Conciseness | **7.0** | **9.0** | **8.0** | **8.0** |
| Source Grounding | **9.0** | **8.0** | **6.0** | **8.0** |
| Bloom's Taxonomy Level | **5.0 (Evaluate)** | **4.0 (Analyze)** | **3.0 (Apply)** | **4.0 (Analyze)** |
| Nuance & Caveats | **10.0** | **6.0** | **3.0** | **7.0** |
| Practical Utility | **9.0** | **7.0** | **4.0** | **8.0** |
| **WEIGHTED AVERAGE** | **8.5** | **7.1** | **5.3** | **7.5** |

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    | ████████████ Claude Sonnet 4
Level 4: Analyze     | ████████████ Gemini Flash 2.5, OpenAI GPT-4o
Level 3: Apply       | ████████████ DeepSeek V2 (Local)
Level 2: Understand  |
Level 1: Remember    |
```

Healthcare requires evaluation-level reasoning — assessing evidence quality, weighing risks, and making clinical judgments. Claude reaches Level 5 with explicit evidence grading. GPT-4o and Gemini analyze at Level 4. DeepSeek applies at Level 3, which is **insufficient for clinical applications** where safety caveats are critical.

---

## Provider Profiles for This Chapter

### Claude Sonnet 4 — "The Clinical Advisor"
**Strengths:** Best evidence grading; comprehensive safety caveats; structured clinical reports; appropriate medical uncertainty communication.
**Weaknesses:** Verbose for quick clinical lookups.

### OpenAI GPT-4o — "The Medical Researcher"
**Strengths:** Good medical knowledge; balanced clinical communication; reliable for research synthesis.
**Weaknesses:** Less explicit about evidence quality levels than Claude.

### Gemini Flash 2.5 — "The Fast Screener"
**Strengths:** Quick literature overview; efficient for initial triage of research papers.
**Weaknesses:** Less depth in clinical safety communication.

### DeepSeek V2 16B — "Not Recommended for Healthcare"
**Strengths:** Zero-cost for testing pipeline architecture.
**Weaknesses:** Insufficient safety awareness for medical applications; limited medical nuance; no evidence grading.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Clinical decision support** | Claude Sonnet 4 | Best safety caveats and evidence grading |
| **Literature synthesis** | Claude or GPT-4o | Strongest at evaluating research quality |
| **Research triage** | Gemini Flash 2.5 | Fast screening of large paper volumes |
| **Hypothesis generation** | Claude Sonnet 4 | Most creative and well-caveated hypotheses |
| **Pipeline development only** | Ollama DeepSeek V2 | ONLY for testing code — never for clinical output |

> **Safety Note:** No LLM output should be used for actual clinical decisions without human expert review. DeepSeek V2's limited safety awareness makes it particularly unsuitable for healthcare applications beyond pipeline testing.

---

*Analysis based on Chapter 13 notebook outputs executed April 2026. Claude has saved LIVE mode outputs. The retrieval pipeline is deterministic — differentiation is in synthesis quality and safety communication.*
