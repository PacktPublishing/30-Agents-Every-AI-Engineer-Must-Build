# Chapter 7 — LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 7 Tool Orchestration tasks: tool-using agents, chain-of-agents, and agentic workflows.

---

## Agent Tasks in This Chapter

- **Tool-Using Agent** — Selecting and invoking the correct tool from a registry based on user intent
- **Chain-of-Agents** — Sequential agent pipeline where each agent's output feeds the next
- **Agentic Workflows** — Conditional branching, retry logic, and parallel tool execution

## Scoring Dimensions

Each provider is rated 0–10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of tool selections and parameter extraction |
| **Completeness** | Coverage of all workflow branches and edge cases |
| **Structure & Organization** | Quality of tool call JSON and workflow state management |
| **Conciseness** | Information density without unnecessary padding |
| **Source Grounding** | Adherence to the chapter's orchestration patterns |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Handling of ambiguous tool selection and error recovery |
| **Practical Utility** | How useful the orchestration outputs would be in production |

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

## Key Observation: Deterministic Orchestration Logic

Chapter 7's tool orchestration is **heavily deterministic**. The workflow engine, tool registry, chain-of-agents pipeline, and retry logic are all rule-based. The LLM is used for:

1. **Tool selection** — Interpreting user intent to choose the correct tool from the registry
2. **Parameter extraction** — Extracting structured parameters from natural language
3. **Result synthesis** — Summarizing multi-tool execution results

**Execution mode note:** Claude ran in LIVE mode. OpenAI ran in SIMULATION mode. Gemini and DeepSeek notebooks have outputs from LIVE/SIMULATION mixed execution.

---

## Provider Performance

### Claude Sonnet 4

**LLM-dependent cell behavior:**
- Tool selection: Correctly identified all tools with explicit reasoning about selection criteria
- Parameter extraction: Produced well-typed JSON with all required and optional fields
- Result synthesis: Coherent multi-tool summaries with execution metadata
- Ran in LIVE mode

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | All tool selections correct; parameters well-typed |
| Completeness | 9 | Handled all scenarios including ambiguous multi-tool cases |
| Structure & Organization | 9 | Clean tool call JSON with proper schema adherence |
| Conciseness | 8 | Thorough but efficient tool call formatting |
| Source Grounding | 9 | Follows chapter's registry and orchestration patterns |
| Bloom's Level | **4 — Analyze** | Analyzed user intent to differentiate between similar tools |
| Nuance & Caveats | 8 | Noted ambiguous cases and confidence in tool selection |
| Practical Utility | 9 | Production-ready tool orchestration output |

---

### Gemini Flash 2.5

**LLM-dependent cell behavior:**
- Tool selection: Fast, correct selections with minimal reasoning
- Parameter extraction: Valid JSON with required fields
- Mixed execution mode

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct tool selections |
| Completeness | 7 | Basic coverage without edge case handling |
| Structure & Organization | 8 | Valid tool call JSON |
| Conciseness | 9 | Minimal overhead per tool call |
| Source Grounding | 8 | Follows orchestration patterns |
| Bloom's Level | **3 — Apply** | Applied tool matching rules |
| Nuance & Caveats | 5 | No ambiguity handling |
| Practical Utility | 8 | Functional for straightforward orchestration |

---

### DeepSeek V2 16B (Local)

**LLM-dependent cell behavior:**
- Tool selection: Generally correct for obvious cases; less reliable for nuanced selection
- Parameter extraction: Valid JSON but occasionally missing optional parameters
- Mixed execution mode

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | Mostly correct; occasional wrong tool for ambiguous cases |
| Completeness | 6 | Basic tool calls without edge case coverage |
| Structure & Organization | 7 | Valid but minimal JSON |
| Conciseness | 9 | Very compact tool calls |
| Source Grounding | 7 | Follows basic patterns |
| Bloom's Level | **2 — Understand** | Understood tool descriptions but didn't analyze nuances |
| Nuance & Caveats | 3 | No confidence or ambiguity handling |
| Practical Utility | 6 | Needs validation layer for production use |

---

### OpenAI GPT-4o

**LLM-dependent cell behavior:**
- Ran in SIMULATION mode — outputs are from MockLLM
- Deterministic workflow cells produced identical results
- MockLLM provided standard tool selection responses

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | MockLLM responses correct (pre-authored) |
| Completeness | 7 | Standard MockLLM coverage |
| Structure & Organization | 7 | MockLLM formatting |
| Conciseness | 8 | Appropriately sized |
| Source Grounding | 8 | Follows patterns |
| Bloom's Level | **3 — Apply** | MockLLM applies without analysis |
| Nuance & Caveats | 5 | Basic MockLLM caveats |
| Practical Utility | 7 | Demonstration quality |

> *OpenAI ran in Simulation Mode — scores reflect MockLLM output.*

---

## Overall Scorecard

| Dimension | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) | OpenAI GPT-4o |
|---|---|---|---|---|
| Factual Accuracy | **9.0** | **8.0** | **7.0** | **8.0*** |
| Completeness | **9.0** | **7.0** | **6.0** | **7.0*** |
| Structure & Organization | **9.0** | **8.0** | **7.0** | **7.0*** |
| Conciseness | **8.0** | **9.0** | **9.0** | **8.0*** |
| Source Grounding | **9.0** | **8.0** | **7.0** | **8.0*** |
| Bloom's Taxonomy Level | **4.0 (Analyze)** | **3.0 (Apply)** | **2.0 (Understand)** | **3.0 (Apply)*** |
| Nuance & Caveats | **8.0** | **5.0** | **3.0** | **5.0*** |
| Practical Utility | **9.0** | **8.0** | **6.0** | **7.0*** |
| **WEIGHTED AVERAGE** | **8.1** | **7.0** | **5.9** | **6.6*** |

> *\* OpenAI scores reflect MockLLM (Simulation Mode) output.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     | ████████████ Claude Sonnet 4
Level 3: Apply       | ████████████ Gemini Flash 2.5, OpenAI* (MockLLM)
Level 2: Understand  | ████████████ DeepSeek V2 (Local)
Level 1: Remember    |
```

Claude analyzes user intent to differentiate between similar tools in the registry, demonstrating Level 4 reasoning. Gemini applies tool matching rules at Level 3. DeepSeek understands tool descriptions but struggles with nuanced selection.

---

## Provider Profiles for This Chapter

### Claude Sonnet 4 — "The Precise Orchestrator"
**Strengths:** Best tool selection accuracy including ambiguous cases; clean JSON schemas; confidence-annotated selections.
**Weaknesses:** Slightly more tokens per tool call than Gemini.

### Gemini Flash 2.5 — "The Fast Dispatcher"
**Strengths:** Fastest tool call generation; good for high-throughput orchestration.
**Weaknesses:** No ambiguity handling; binary tool selection.

### DeepSeek V2 16B — "The Basic Caller"
**Strengths:** Zero-cost local execution; valid JSON output.
**Weaknesses:** Unreliable for nuanced tool selection; missing optional parameters.

### OpenAI GPT-4o — "Not Scored (Simulation)"
**Note:** Ran in Simulation Mode. With a valid API key, GPT-4o would likely perform at the Analyze level for tool orchestration.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Complex tool orchestration** | Claude Sonnet 4 | Best disambiguation and parameter extraction |
| **High-throughput tool dispatch** | Gemini Flash 2.5 | Fastest with acceptable accuracy |
| **Local tool testing** | Ollama DeepSeek V2 | Zero cost for pipeline development |
| **Workflow logic** | Any (deterministic) | Orchestration engine is provider-independent |

---

*Analysis based on Chapter 7 notebook outputs executed April 2026. Claude ran in LIVE mode; OpenAI ran in SIMULATION mode. The majority of orchestration logic is deterministic.*
