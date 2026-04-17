# Chapter 2 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 2 Agent Toolkit tasks: framework comparison, LangChain ReAct agents, LangGraph workflows, memory systems, hybrid model routing, RAG pipelines, tool abstraction, function calling, and cloud platform deployment.

---

## Agent Tasks in This Chapter

- **Framework Comparison** -- Six-framework survey (LangChain, LangGraph, LlamaIndex, AutoGPT, CrewAI, AutoGen) with structured table output
- **LangChain ReAct Agent** -- Calculator + web search tool chain for "What's the square root of 144?"
- **LangGraph Workflow** -- Research/analyze/decide/respond cycle on quantum computing
- **Memory Systems** -- Buffer vs. summary memory comparison across 3 turns
- **Hybrid Model Routing** -- Factual/creative/analytical query classification and model dispatch
- **RAG Pipeline** -- Vector search + LLM synthesis for semantic search question
- **Tool Abstraction** -- StockPriceTool with error handling for invalid tickers
- **Function Calling** -- Weather function schema, argument generation, execution, and synthesis
- **Cloud Platform Survey** -- AWS Bedrock, Azure AI Foundry, Google Vertex AI comparison

## Important Observation: Limited LLM Differentiation

Chapter 2 is primarily a **framework and tooling** chapter. Most cells demonstrate architectural patterns (LangChain, LangGraph, memory systems, RAG pipelines) using MockLLM simulation for the framework demonstrations. The LLM provider primarily affects:

1. **Intent classification** in the hybrid routing demo (classify_intent)
2. **Cloud platform descriptions** (minor provider-aware text variations)
3. **Function calling schema** descriptions (provider-specific naming)

The framework demonstrations (ReAct agent, LangGraph workflow, memory systems, RAG pipeline, tool abstraction) all use MockLLM regardless of which provider is active, producing identical outputs. This means **the comparison surface is narrow** for this chapter compared to Chapters 1, 3, and 4.

## Scoring Dimensions

Each provider is rated 0-10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of framework descriptions and classification results |
| **Completeness** | Coverage of all toolkit demos and framework comparisons |
| **Structure & Organization** | Quality of table formatting, JSON output, workflow visualization |
| **Conciseness** | Information density without unnecessary padding |
| **Source Grounding** | Adherence to the chapter's prescribed framework comparisons and patterns |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Acknowledgment of framework tradeoffs, integration patterns |
| **Practical Utility** | How actionable the toolkit guidance would be for a developer |

---

## Task 1: Framework Comparison Table

All four providers produced identical framework comparison tables (this is a static rendering, not LLM-generated). The table correctly lists all six frameworks with stars, strengths, limitations, and ideal use cases. No differentiation here.

## Task 2: LangChain ReAct Agent

All four providers produced identical MockLLM-driven output: the calculator fell back to simulation mode (`ModuleNotFoundError: No module named 'sympy'`), and the web search returned the same canned response about the number 12. Final synthesized answer was identical across all providers. No differentiation.

## Task 3: LangGraph Workflow

All four providers produced identical workflow output: quantum computing research at 85% confidence, proceeding directly to respond. Same iteration count, same final response. No differentiation.

## Task 4: Memory Systems

Buffer and summary memory outputs were identical across all providers -- MockLLM returns the same canned 3-exchange history. No differentiation.

## Task 5: Hybrid Model Routing (Intent Classification)

This is where the LLM provider's `classify_intent()` function is actually called. All four providers classified the three test queries identically:
- "What is the capital of France?" -> `factual` -> Mistral-7B
- "Write a poetic description of AI agents." -> `creative` -> Claude
- "Analyze the year-over-year revenue growth." -> `analytical` -> GPT-4o

**Observation:** The classification was correct across all providers. The routed responses were MockLLM simulation, so the actual differentiation is limited to whether the LLM correctly identified the query type. All four succeeded.

## Task 6: RAG Pipeline

Identical MockLLM output across all providers. Vector search returned the same 3 chunks (scores 0.92, 0.87, 0.81). Synthesized answer was identical.

## Task 7: Tool Abstraction (StockPriceTool)

Identical simulated stock prices across all providers (AAPL: $187.42, GOOGL: $175.30, MSFT: $420.15, NVDA: $890.25). Invalid ticker error handling was identical.

## Task 8: Function Calling

All four providers displayed the same `get_weather` schema, generated the same function call (`get_weather('Toronto')`), and produced the same simulated weather result (18C, Partly cloudy, 62% humidity). The only difference was provider-specific naming in the section header:
- **OpenAI:** "OpenAI Function Calling, p.55"
- **Claude:** "Anthropic Tool Use, p.55"
- **Gemini:** "Google Gemini Function Calling, p.55"
- **DeepSeek:** "Google Gemini Function Calling, p.55" (fell back to OpenAI)

## Task 9: Cloud Platform Survey

Minor provider-aware differences in the Azure AI Foundry description:
- **OpenAI notebook:** "Direct access to GPT-4/GPT-4o via Azure OpenAI Service"
- **Claude notebook:** "Direct access to Claude Sonnet 4 via Azure AI Service"
- **Gemini notebook:** "Direct access to Gemini models via Google Cloud AI"
- **DeepSeek notebook:** Same as Gemini (fell back)

These are cosmetic adaptations, not substantive differences in analytical quality.

## DeepSeek Fallback Issue

The DeepSeek V2 notebook displayed `[WARNING] LLM_PROVIDER=ollama but OLLAMA_API_KEY not set. Falling back.` and then ran as OpenAI GPT-4o. This means the DeepSeek column in this chapter effectively mirrors GPT-4o for all tasks. This is a configuration issue, not a model capability difference, but it means we cannot fairly evaluate DeepSeek's performance on Chapter 2 tasks.

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|---|
| Factual Accuracy | **7.0** | **7.0** | **7.0** | **6.5*** |
| Completeness | **7.0** | **7.0** | **7.0** | **7.0** |
| Structure & Organization | **7.0** | **7.0** | **7.0** | **7.0** |
| Conciseness | **7.0** | **7.0** | **7.0** | **7.0** |
| Source Grounding | **7.0** | **7.0** | **7.0** | **7.0** |
| Bloom's Taxonomy Level | **3.0 (Apply)** | **3.0 (Apply)** | **3.0 (Apply)** | **3.0 (Apply)** |
| Nuance & Caveats | **5.0** | **5.0** | **5.0** | **5.0** |
| Practical Utility | **7.0** | **7.0** | **7.0** | **6.5*** |
| **WEIGHTED AVERAGE** | **6.3** | **6.3** | **6.3** | **6.1** |

*\* DeepSeek scores are penalized slightly because the notebook fell back to OpenAI rather than running on the local Ollama model. The provider-under-test was not actually exercised.*

**Scoring notes:**
- All scores are depressed compared to other chapters because the LLM comparison surface is narrow -- most outputs are MockLLM-driven framework demos
- The 7.0 baseline reflects correct execution of all cells with proper framework demonstrations
- Bloom's is capped at Level 3 (Apply) because the LLM's role is limited to intent classification and cosmetic text adaptation -- there is no deep reasoning or evaluation task
- Nuance is low (5.0) because the MockLLM provides identical canned responses regardless of provider, offering no opportunity for the LLM to demonstrate edge-case awareness

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     |
Level 3: Apply       | OpenAI GPT-4o, Claude Sonnet 4, Gemini Flash 2.5, DeepSeek V2
Level 2: Understand  |
Level 1: Remember    |
```

All four providers operate at Level 3 (Apply) for this chapter. The LLM correctly applies the classify_intent pattern to route queries, but there is no evaluation, analysis, or creative synthesis task that would differentiate cognitive levels.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  1. OpenAI GPT-4o          6.3  ###################-----------
     Claude Sonnet 4        6.3  ###################-----------
     Gemini Flash 2.5       6.3  ###################-----------
  4. DeepSeek V2 (Local)    6.1  ##################------------
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     |
  L4 Analyze      |
  L3 Apply        | C G D O
  L2 Understand   | C G D O
  L1 Remember     | C G D O
```

Legend: **C** = Claude Sonnet 4, **G** = Gemini Flash 2.5, **D** = DeepSeek V2, **O** = OpenAI GPT-4o

---

## Winner: Three-Way Tie (GPT-4o / Claude / Gemini)

| | |
|---|---|
| **Chapter 2 Winner** | **Three-way tie** |
| **Score** | **6.3 / 10** |
| **Bloom's Level** | **Level 3 -- Apply** |

**Why this chapter produces a tie:**
- Chapter 2 is a framework and tooling chapter, not an LLM reasoning chapter
- The MockLLM simulation layer handles 90%+ of the visible outputs
- The only LLM-differentiated task (hybrid routing classification) was solved identically by all providers
- Cloud platform descriptions showed cosmetic provider-awareness but no substantive quality difference

**Key takeaway:** For framework demonstration chapters, the choice of LLM provider is nearly irrelevant. The value comes from the architectural patterns being demonstrated, not the LLM's reasoning capability. Any of the three cloud providers works equally well. DeepSeek is penalized only for the fallback configuration issue.

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Running Chapter 2 demos | Any cloud provider | All produce identical results for framework demos |
| Learning framework patterns | Gemini Flash 2.5 | Fastest inference for interactive notebook exploration |
| Cost-conscious exploration | DeepSeek V2 (Local) | Zero API cost, though requires correct Ollama configuration |
| Production framework evaluation | OpenAI GPT-4o | Widest framework ecosystem support and documentation |

## Provider Profiles for This Chapter

### All Providers -- "Equally Capable Framework Demonstrators"

**Strengths (shared):**
- All four notebooks executed end-to-end without errors (aside from the expected `sympy` fallback)
- Framework comparison table, workflow visualization, and tool abstraction demos rendered correctly
- Intent classification for hybrid routing was correct across all providers
- Section completion status shows all 7+ sections marked COMPLETE

**Weakness (shared):**
- The chapter design does not exercise LLM reasoning in a way that would differentiate providers
- MockLLM produces identical outputs regardless of provider for most tasks

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Framework evaluation** | Any provider | Identical results; choose by cost or convenience |
| **Interactive learning** | Gemini Flash 2.5 | Fastest response times for notebook experimentation |
| **Offline development** | Ollama DeepSeek V2 | Zero cost, but ensure correct OLLAMA_API_KEY configuration |
| **Production readiness** | OpenAI GPT-4o | Most mature function calling and tool integration ecosystem |

---

*Analysis based on Chapter 2 notebook outputs executed April 2026. All four providers ran in LIVE mode (DeepSeek fell back to OpenAI due to missing OLLAMA_API_KEY). Scores reflect the narrow comparison surface: most chapter outputs are MockLLM-driven framework demonstrations where provider choice has minimal impact.*
