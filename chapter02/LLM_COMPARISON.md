# Chapter 2 — LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 2 Agent Toolkit tasks: framework comparison, model routing, embeddings, and function calling.

---

## Agent Tasks in This Chapter

- **Framework Comparison** — Evaluating LangChain, CrewAI, AutoGen, and custom frameworks
- **Model Routing** — Selecting the appropriate model tier based on task complexity
- **Embeddings** — Vector representations for semantic search and similarity
- **Function Calling** — Structured tool invocation via LLM-generated JSON

## Scoring Dimensions

Each provider is rated 0–10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of framework comparisons and routing decisions |
| **Completeness** | Coverage of all toolkit components and routing scenarios |
| **Structure & Organization** | Use of tables, JSON formatting, logical flow |
| **Conciseness** | Information density without unnecessary padding |
| **Source Grounding** | Adherence to the chapter's prescribed toolkit patterns |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Acknowledgment of trade-offs between frameworks |
| **Practical Utility** | How useful the output would be for an engineer choosing tools |

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

Chapter 2's toolkit demonstrations are **primarily deterministic**. The notebook implements framework comparisons, routing logic, and function-calling schemas using predefined rules. The LLM is used for:

1. **Model routing decisions** — classifying task complexity to select the right model tier
2. **Function call generation** — producing structured JSON for tool invocation
3. **Embedding quality** — generating vector representations (provider-specific)

The majority of notebook cells produce identical output regardless of provider because the logic is hardcoded. Scoring therefore focuses on the few LLM-dependent cells.

---

## Provider Performance

### Claude Sonnet 4

**LLM-dependent cell behavior:**
- Model routing: Correctly classified task complexity with detailed reasoning
- Function calling: Produced well-structured JSON with all required parameters
- Execution: All cells completed successfully in LIVE mode

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Correct routing decisions and function call schemas |
| Completeness | 9 | All routing scenarios handled with reasoning |
| Structure & Organization | 9 | Clean JSON, proper parameter typing |
| Conciseness | 8 | Slightly verbose reasoning in routing explanations |
| Source Grounding | 9 | Follows the chapter's routing taxonomy precisely |
| Bloom's Level | **4 — Analyze** | Compared task characteristics to select appropriate tier |
| Nuance & Caveats | 7 | Noted edge cases in routing decisions |
| Practical Utility | 9 | Production-ready function call schemas |

---

### Gemini Flash 2.5

**LLM-dependent cell behavior:**
- Model routing: Fast, accurate classification with minimal explanation
- Function calling: Clean JSON output with correct parameter types
- Execution: All cells completed successfully in LIVE mode

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Correct classifications across all scenarios |
| Completeness | 8 | All scenarios handled but with less reasoning detail |
| Structure & Organization | 8 | Valid JSON; slightly less structured explanations |
| Conciseness | 9 | Tightest outputs — minimal overhead |
| Source Grounding | 8 | Follows routing patterns accurately |
| Bloom's Level | **3 — Apply** | Applied routing rules correctly without deeper analysis |
| Nuance & Caveats | 5 | No discussion of edge cases or trade-offs |
| Practical Utility | 8 | Functional schemas, ready for integration |

---

### DeepSeek V2 16B (Local)

**LLM-dependent cell behavior:**
- Model routing: Correct basic classifications; occasional over-simplification
- Function calling: Valid JSON but sometimes missing optional parameters
- Execution: All cells completed successfully in LIVE mode (via Ollama)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Core classifications correct |
| Completeness | 7 | Basic coverage; missed some optional parameters |
| Structure & Organization | 7 | Valid JSON but minimal field annotations |
| Conciseness | 9 | Very compact outputs |
| Source Grounding | 7 | Follows basic patterns but misses nuances |
| Bloom's Level | **3 — Apply** | Applied routing rules to scenarios |
| Nuance & Caveats | 4 | No trade-off discussion |
| Practical Utility | 7 | Functional but may need enrichment |

---

### OpenAI GPT-4o

**LLM-dependent cell behavior:**
- Model routing: Accurate classification with concise reasoning
- Function calling: Well-formed JSON with appropriate parameter types
- Execution: All cells completed successfully in LIVE mode

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | All routing decisions correct |
| Completeness | 8 | Good coverage of scenarios |
| Structure & Organization | 8 | Clean JSON formatting |
| Conciseness | 8 | Balanced output length |
| Source Grounding | 8 | Follows chapter patterns |
| Bloom's Level | **4 — Analyze** | Compared characteristics for routing decisions |
| Nuance & Caveats | 6 | Some mention of trade-offs |
| Practical Utility | 8 | Ready for integration |

---

## Overall Scorecard

| Dimension | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) | OpenAI GPT-4o |
|---|---|---|---|---|
| Factual Accuracy | **9.0** | **9.0** | **8.0** | **9.0** |
| Completeness | **9.0** | **8.0** | **7.0** | **8.0** |
| Structure & Organization | **9.0** | **8.0** | **7.0** | **8.0** |
| Conciseness | **8.0** | **9.0** | **9.0** | **8.0** |
| Source Grounding | **9.0** | **8.0** | **7.0** | **8.0** |
| Bloom's Taxonomy Level | **4.0 (Analyze)** | **3.0 (Apply)** | **3.0 (Apply)** | **4.0 (Analyze)** |
| Nuance & Caveats | **7.0** | **5.0** | **4.0** | **6.0** |
| Practical Utility | **9.0** | **8.0** | **7.0** | **8.0** |
| **WEIGHTED AVERAGE** | **8.1** | **7.3** | **6.5** | **7.4** |

> *Note: Since Chapter 2 is heavily deterministic, the differences between providers are modest. The scoring above reflects only the LLM-dependent cells (routing decisions, function call generation).*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     | ████████████ Claude Sonnet 4, OpenAI GPT-4o
Level 3: Apply       | ████████████ Gemini Flash 2.5, DeepSeek V2 (Local)
Level 2: Understand  |
Level 1: Remember    |
```

The toolkit chapter primarily exercises Level 3–4 capabilities. Claude and GPT-4o demonstrate analytical reasoning in routing decisions (comparing task characteristics), while Gemini and DeepSeek apply routing rules without deeper comparative analysis.

---

## Provider Profiles for This Chapter

### Claude Sonnet 4 — "The Careful Router"
**Strengths:** Most detailed routing reasoning; best function call schemas with complete parameter sets.
**Weaknesses:** Slightly over-verbose for simple routing decisions.

### Gemini Flash 2.5 — "The Speed Router"
**Strengths:** Fastest execution; cleanest minimal JSON outputs.
**Weaknesses:** Minimal reasoning explanation; no edge case handling.

### DeepSeek V2 16B — "The Local Router"
**Strengths:** Zero-cost local execution; produces valid JSON consistently.
**Weaknesses:** Occasionally misses optional parameters; generic outputs.

### OpenAI GPT-4o — "The Balanced Router"
**Strengths:** Good balance of reasoning depth and conciseness.
**Weaknesses:** No significant weaknesses for this task type.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Production model routing** | Claude Sonnet 4 or GPT-4o | Best analytical depth for complex routing |
| **High-volume function calling** | Gemini Flash 2.5 | Lowest cost per call with valid schemas |
| **Local development/testing** | Ollama DeepSeek V2 | Zero cost, valid JSON for schema testing |
| **Framework evaluation** | Any (deterministic) | Output is identical across providers |

---

*Analysis based on Chapter 2 notebook outputs executed April 2026. All four providers ran in LIVE mode. Most chapter output is deterministic — scores reflect the LLM-dependent routing and function-calling cells only.*
