# Chapter 2 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 2 Agent Toolkit tasks: framework comparison, model routing, embeddings, and function calling.

---

## Agent Tasks in This Chapter

- **Framework Comparison** -- Evaluating LangChain, CrewAI, AutoGen, and custom frameworks
- **Model Routing** -- Selecting the appropriate model tier based on task complexity
- **Embeddings** -- Vector representations for semantic search and similarity
- **Function Calling** -- Structured tool invocation via LLM-generated JSON
- **RAG Pipeline** -- Simulated retrieval-augmented generation with scored chunks

## Scoring Dimensions

Each provider is rated 0-10 across eight dimensions:

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

## Critical Observation: Deterministic Output Across All Providers

**Chapter 2 uses MockLLM (simulation mode) for all LLM-dependent cells in every provider notebook.** Despite each notebook displaying a "LIVE MODE" banner, the actual LLM calls route through the MockLLM fallback, producing identical `[SIMULATION]`-tagged responses regardless of provider.

Evidence from the notebook outputs:
- **Hybrid routing demo:** All four notebooks produce identical text: `[SIMULATION][Mistral-7B] The capital of France is Paris...`, `[SIMULATION][Claude] In the garden of silicon dreams...`, `[SIMULATION][GPT-4o] Market analysis indicates a 23% year-over-year revenue increase...`
- **RAG pipeline:** All four produce: `[SIMULATION] Vector databases enable semantic search by representing meaning as direction in high-dimensional space...`
- **Function calling:** All four produce: `[SIMULATION] Weather for Toronto: 18C, Partly cloudy, 62% humidity, wind 12 km/h NW.`
- **Memory demo:** All four produce: `[SIMULATION] Summary of 3 exchanges: The conversation covered RAG and vector databases...`

The **only** provider-specific differences are:
1. Notebook title and provider banner text
2. Markdown references to the provider's function calling terminology (e.g., "OpenAI Function Calling" vs. "Anthropic Function Calling" vs. "Google Gemini Function Calling")
3. The analytical model name in the routing description text (e.g., "Analytical -> GPT-4o" vs. "Analytical -> Claude Sonnet 4")

**These are text-level template substitutions, not LLM output differences.**

---

## Provider Performance

Given that all outputs are identical MockLLM responses, the comparison below reflects the quality of the **simulated responses** (which are the same for all providers) and the minor **notebook presentation differences**.

### All Providers (Identical Output)

**Cell-by-cell results:**
- LangChain calculator tool: `[SIMULATION] Calculation error. Fallback: result = 0`
- LangGraph multi-step agent: `[SIMULATION]` keyword-matched response for "quantum computing"
- Buffer memory: 3 pre-authored exchanges returned
- Summary memory: Pre-authored compression of 3 exchanges
- Hybrid routing: Three deterministic routes (factual/creative/analytical) with pre-authored responses
- Vector DB & RAG: Pre-authored top-3 chunks with scoring
- StockPriceTool: Pre-authored price data
- Function calling: Pre-authored weather response

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | MockLLM responses are correct but generic; the simulated calculator returns a fallback error |
| Completeness | 7 | All 13 demo cells execute; every toolkit concept is demonstrated |
| Structure & Organization | 7 | Consistent formatting with colored logging; clear section headers |
| Conciseness | 8 | MockLLM responses are appropriately brief |
| Source Grounding | 8 | Every mock response traces to a specific page reference in Chapter 2 |
| Bloom's Level | **3 -- Apply** | Demonstrates each toolkit pattern without comparative analysis |
| Nuance & Caveats | 3 | No trade-off discussion -- simulated responses are declarative |
| Practical Utility | 6 | Demonstrates patterns but simulated responses lack real-world depth |

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|---|
| Factual Accuracy | **7.0** | **7.0** | **7.0** | **7.0** |
| Completeness | **7.0** | **7.0** | **7.0** | **7.0** |
| Structure & Organization | **7.0** | **7.0** | **7.0** | **7.0** |
| Conciseness | **8.0** | **8.0** | **8.0** | **8.0** |
| Source Grounding | **8.0** | **8.0** | **8.0** | **8.0** |
| Bloom's Taxonomy Level | **3.0 (Apply)** | **3.0 (Apply)** | **3.0 (Apply)** | **3.0 (Apply)** |
| Nuance & Caveats | **3.0** | **3.0** | **3.0** | **3.0** |
| Practical Utility | **6.0** | **6.0** | **6.0** | **6.0** |
| **WEIGHTED AVERAGE** | **6.1** | **6.1** | **6.1** | **6.1** |

> **Important:** All four providers receive identical scores because all four produce identical MockLLM outputs. Any differentiation claimed for this chapter would be fabricated. The honest assessment is that Chapter 2 does not test LLM capabilities -- it tests the notebook infrastructure and MockLLM keyword routing.

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     |
Level 3: Apply       | All four providers (identical MockLLM output)
Level 2: Understand  |
Level 1: Remember    |
```

All providers operate at Level 3 (Apply) because the MockLLM responses demonstrate each toolkit pattern (routing, RAG, function calling) without any comparative analysis, evaluation, or creative synthesis. The responses are keyword-matched templates.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  All four providers      6.1  ##################------------
```

All providers tied at 6.1 -- no differentiation possible with identical MockLLM outputs.

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     |
  L4 Analyze      |
  L3 Apply        | C G D O (all identical)
  L2 Understand   | C G D O
  L1 Remember     | C G D O
```

Legend: **C** = Claude Sonnet 4, **G** = Gemini Flash 2.5, **D** = DeepSeek V2, **O** = OpenAI GPT-4o

---

## Winner: Tie (No Differentiation)

| | |
|---|---|
| **Chapter 2 Winner** | **Tie -- All Providers** |
| **Score** | **6.1 / 10** |
| **Bloom's Level** | **Level 3 -- Apply** |

**Why there is no winner:** Chapter 2 is an infrastructure and toolkit demonstration chapter. All LLM calls are routed through MockLLM with keyword-matched pre-authored responses. The four provider notebooks produce byte-identical LLM outputs (aside from template-substituted provider names in markdown cells). No provider had the opportunity to demonstrate superior capability.

### What This Means for Readers

Chapter 2 is designed to teach **toolkit architecture** (LangChain, LangGraph, memory types, routing patterns, function calling schemas) rather than to showcase LLM output quality. The value is in understanding the **pipeline patterns**, not in comparing LLM responses. This is appropriate for an introductory toolkit chapter.

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Learning the toolkit | Any provider | Identical output; choose based on cost preference |
| Cost optimization | DeepSeek V2 (Local) | Zero cost for identical results |
| Verifying pipeline integrity | Any provider | All produce consistent MockLLM output |

## Provider Profiles for This Chapter

### All Providers -- "Identical Pipeline Runners"

Since all four notebooks produce the same MockLLM responses, individual provider profiles are not meaningful for this chapter. The key differentiators (natural language quality, reasoning depth, structured output) are not exercised.

**What varies between notebooks:**
- Provider name in the banner (OPENAI / ANTHROPIC / GOOGLE / OPENAI via Ollama)
- Function calling terminology in markdown headers ("OpenAI Function Calling" vs. "Anthropic Function Calling")
- Analytical model name in routing description

These are cosmetic template substitutions, not LLM capability differences.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Studying Chapter 2 patterns** | Any -- or DeepSeek (free) | Output is identical; save API costs |
| **Live-mode toolkit testing** | Re-run with `OPENAI_API_KEY` set | Current notebooks use MockLLM regardless |
| **Framework evaluation** | N/A (deterministic) | Output is identical across providers |

---

*Analysis based on Chapter 2 notebook outputs executed April 2026. Despite "LIVE MODE" banners, all four provider notebooks route LLM calls through MockLLM, producing identical simulated responses. Scores reflect the quality of the shared MockLLM output, not provider-specific LLM capabilities.*
