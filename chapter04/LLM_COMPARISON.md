# Chapter 4 — LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 4 Agent Deployment tasks: infrastructure scaling, cost management, and prompt injection defenses.

---

## Agent Tasks in This Chapter

- **Infrastructure Scaling** — Auto-scaling agent deployments based on load patterns
- **Cost Management** — Token budgeting, model tier selection, caching strategies
- **Prompt Injection Defenses** — Detecting and mitigating adversarial prompt attacks
- **Deployment Pipeline** — CI/CD patterns for agent systems

## Scoring Dimensions

Each provider is rated 0–10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of scaling decisions and injection detection |
| **Completeness** | Coverage of all deployment scenarios |
| **Structure & Organization** | Quality of structured outputs (JSON configs, detection reports) |
| **Conciseness** | Information density without unnecessary padding |
| **Source Grounding** | Adherence to the chapter's deployment patterns |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Acknowledgment of trade-offs in scaling and security decisions |
| **Practical Utility** | How useful outputs are for actual deployment decisions |

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

## Key Observation: Deterministic Agent Logic

Chapter 4's deployment agents use **primarily deterministic logic**. The scaling decisions, cost calculations, and injection detection patterns are rule-based. The LLM is invoked for:

1. **Prompt injection classification** — Determining whether a given input is adversarial
2. **Scaling recommendations** — Natural-language explanations of scaling decisions
3. **Cost optimization suggestions** — Recommending tier changes based on usage patterns

The core pipeline logic (load balancing, token counting, caching) is identical across all providers.

---

## Provider Performance

### Claude Sonnet 4

**LLM-dependent cell behavior:**
- Prompt injection detection: Correctly identified all test cases with detailed reasoning about attack vector type
- Scaling recommendations: Produced structured explanations referencing specific metrics
- Ran in LIVE mode (Provider: ANTHROPIC)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | All injection cases correctly classified with attack type identified |
| Completeness | 9 | Covered all attack vectors including subtle indirect injections |
| Structure & Organization | 9 | Structured detection reports with confidence scores |
| Conciseness | 8 | Detailed but every element serves a purpose |
| Source Grounding | 9 | Follows chapter's security taxonomy |
| Bloom's Level | **5 — Evaluate** | Assessed severity and recommended specific countermeasures |
| Nuance & Caveats | 8 | Noted false positive risks and confidence thresholds |
| Practical Utility | 9 | Detection reports could feed directly into a security pipeline |

---

### Gemini Flash 2.5

**LLM-dependent cell behavior:**
- Prompt injection detection: Correct classification with concise reasoning
- Scaling recommendations: Brief but accurate
- Ran in LIVE mode (Provider: GOOGLE)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | All injections correctly flagged |
| Completeness | 7 | Correct but less detail on attack vector taxonomy |
| Structure & Organization | 7 | Clean output, less structured than Claude |
| Conciseness | 9 | Minimal overhead per detection |
| Source Grounding | 8 | Follows chapter patterns |
| Bloom's Level | **3 — Apply** | Applied detection rules without deeper evaluation |
| Nuance & Caveats | 5 | No false-positive discussion |
| Practical Utility | 8 | Fast classification suitable for high-throughput screening |

---

### DeepSeek V2 16B (Local)

**LLM-dependent cell behavior:**
- Prompt injection detection: Mostly correct; missed one subtle indirect injection
- Scaling recommendations: Basic but functional
- Ran in LIVE mode (Provider: OPENAI via Ollama endpoint)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | Missed one subtle injection; others correct |
| Completeness | 6 | Basic detection without attack type classification |
| Structure & Organization | 6 | Simple binary output with minimal structure |
| Conciseness | 9 | Very brief classification |
| Source Grounding | 7 | Follows basic pattern |
| Bloom's Level | **2 — Understand** | Recognized patterns but didn't evaluate severity |
| Nuance & Caveats | 3 | No confidence scoring or caveats |
| Practical Utility | 6 | Would need additional processing for production security |

---

### OpenAI GPT-4o

**LLM-dependent cell behavior:**
- Prompt injection detection: Correct classification with concise attack vector labels
- Scaling recommendations: Well-structured with metric references
- Ran in LIVE mode (Provider: OPENAI)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | All injections correctly identified |
| Completeness | 8 | Good coverage with attack vector labeling |
| Structure & Organization | 8 | Clean structured output |
| Conciseness | 8 | Good balance |
| Source Grounding | 8 | Follows chapter taxonomy |
| Bloom's Level | **4 — Analyze** | Classified attacks by type and analyzed characteristics |
| Nuance & Caveats | 6 | Some mention of confidence levels |
| Practical Utility | 8 | Usable detection output |

---

## Overall Scorecard

| Dimension | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) | OpenAI GPT-4o |
|---|---|---|---|---|
| Factual Accuracy | **9.0** | **9.0** | **7.0** | **9.0** |
| Completeness | **9.0** | **7.0** | **6.0** | **8.0** |
| Structure & Organization | **9.0** | **7.0** | **6.0** | **8.0** |
| Conciseness | **8.0** | **9.0** | **9.0** | **8.0** |
| Source Grounding | **9.0** | **8.0** | **7.0** | **8.0** |
| Bloom's Taxonomy Level | **5.0 (Evaluate)** | **3.0 (Apply)** | **2.0 (Understand)** | **4.0 (Analyze)** |
| Nuance & Caveats | **8.0** | **5.0** | **3.0** | **6.0** |
| Practical Utility | **9.0** | **8.0** | **6.0** | **8.0** |
| **WEIGHTED AVERAGE** | **8.4** | **7.0** | **5.8** | **7.4** |

> *Note: The majority of Chapter 4 output is deterministic (scaling logic, cost calculations). Scores reflect only the LLM-dependent cells: injection detection, scaling explanations, and cost recommendations.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    | ████████████ Claude Sonnet 4
Level 4: Analyze     | ████████████ OpenAI GPT-4o
Level 3: Apply       | ████████████ Gemini Flash 2.5
Level 2: Understand  | ████████████ DeepSeek V2 (Local)
Level 1: Remember    |
```

Claude reaches Level 5 by evaluating attack severity and recommending specific countermeasures. GPT-4o analyzes attack characteristics at Level 4. Gemini applies detection rules at Level 3. DeepSeek recognizes patterns at Level 2 but doesn't classify or evaluate.

---

## Provider Profiles for This Chapter

### Claude Sonnet 4 — "The Security Analyst"
**Strengths:** Best injection detection with attack vector taxonomy and severity assessment; production-ready security reports.
**Weaknesses:** Higher latency per detection — may not suit real-time high-throughput screening.

### Gemini Flash 2.5 — "The Fast Screener"
**Strengths:** Fastest classification; excellent for high-volume pre-screening where speed matters.
**Weaknesses:** No depth in attack analysis; binary classification without nuance.

### DeepSeek V2 16B — "The Basic Guard"
**Strengths:** Zero-cost local screening; no data leaves the network.
**Weaknesses:** Missed a subtle indirect injection; insufficient for production security.

### OpenAI GPT-4o — "The Balanced Detector"
**Strengths:** Good attack classification with reasonable speed; solid production choice.
**Weaknesses:** Less depth than Claude in severity assessment.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Security-critical detection** | Claude Sonnet 4 | Deepest analysis with severity assessment |
| **High-throughput screening** | Gemini Flash 2.5 | Fastest with acceptable accuracy |
| **Air-gapped environments** | Ollama DeepSeek V2 | Only local option; acceptable for first-pass screening |
| **Balanced production use** | OpenAI GPT-4o | Good accuracy with reasonable speed |
| **Cost/scaling calculations** | Any (deterministic) | Output is identical across providers |

---

*Analysis based on Chapter 4 notebook outputs executed April 2026. All four providers ran in LIVE mode. Most chapter output is deterministic — scores reflect only the LLM-dependent security and recommendation cells.*
