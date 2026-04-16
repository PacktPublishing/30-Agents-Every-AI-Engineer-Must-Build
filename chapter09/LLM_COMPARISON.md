# Chapter 9 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of three LLM providers running the Chapter 9 Software Development tasks: code generation, security hardening, compliance scanning, and self-improving agents.

---

## Agent Tasks in This Chapter

- **Code Generation Agent (TDG)** -- Producing code from natural language specifications with test-driven generation
- **Full-Stack Workflow** -- Backend (Flask API), Frontend (React), and Integration agents via LangGraph
- **Compliance Agent** -- PCI DSS and HIPAA violation detection, semantic code analysis, contextual remediation
- **Self-Improving Agent** -- Sensing-Critic-Planner-Learning loop with KPI evaluation and hypothesis generation

## Scoring Dimensions

Each provider is rated 0-10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of generated code and security assessments |
| **Completeness** | Coverage of specifications, edge cases, and security vectors |
| **Structure & Organization** | Code quality, documentation, and logical organization |
| **Conciseness** | Code efficiency without unnecessary complexity |
| **Source Grounding** | Adherence to the chapter's software engineering patterns |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Acknowledgment of trade-offs, potential issues, and limitations |
| **Practical Utility** | How production-ready the generated code would be |

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

## Key Observation: Mixed Live and Simulation Mode Outputs

Chapter 9 uses a **deterministic orchestration pipeline** with LLM-generated code as the key differentiator. The compliance scanning (policy engine, data flow analysis) and self-improvement pipeline (sensing, critic, HITL) are largely deterministic, but the LLM drives code generation, semantic analysis, and hypothesis generation.

**Execution modes observed:**
- **Gemini Flash 2.5**: Live Mode (ChatGoogleGenerativeAI) -- real LLM outputs for all code generation and analysis tasks
- **DeepSeek V2 16B**: Live Mode (ChatOllama) -- real LLM outputs, running locally
- **OpenAI GPT-4o**: Simulation Mode (MockLLM) -- pre-authored responses only
- **Claude Sonnet 4**: No saved outputs (0 output cells)

Only Gemini and DeepSeek provide actual LLM-generated outputs for comparison. OpenAI ran on MockLLM (identical to simulation). Claude notebook was not executed.

---

## Provider Performance

### Gemini Flash 2.5

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Code generation is correct with proper type annotations and docstrings. The `calculate_shipping` function uses appropriate constants and validation. However, test suite uses mismatched parameters (weight, distance vs cart_total, weight). |
| Completeness | 8 | Comprehensive code with extensive docstrings, input validation, examples in docstrings, and configurable constants. Generates parametrized test classes. But the LLM occasionally drifts from the spec -- the refined version adds an `item_type` parameter not in the original spec. |
| Structure & Organization | 8 | Well-organized code with clear sections, named constants, and comprehensive docstrings. Flask API uses proper factory pattern with blueprints, models, and error handlers. |
| Conciseness | 6 | Verbose. Code generation includes extensive configuration parameters, setup instructions, and explanatory prose. The Flask API response is a full multi-file project layout rather than a focused code snippet. The React component output includes mock API setup instructions instead of just the component. |
| Source Grounding | 7 | Follows the chapter's TDG pattern but diverges in details. Semantic analysis produces a compliance report format instead of the compact structured output. The Planner Agent failed to parse LLM response (JSON parse error), triggering fallback with generic hypotheses. |
| Bloom's Level | **4 -- Analyze** | Analyzes code structure in semantic compliance scanning (identifying retained fields, regulatory implications). Breaks down the problem into components. But hypotheses are generic ("Investigate and improve X") rather than specific actionable changes. |
| Nuance & Caveats | 7 | Code includes good caveats -- "CUSTOMIZE THESE TO YOUR BUSINESS RULES", validation edge cases, and separate error messages for different invalid inputs. Semantic analysis identifies the docstring-vs-behavior mismatch well. |
| Practical Utility | 7 | Generated code is mostly production-adjacent. The Flask API is over-engineered for the task (full migration, config system). The Planner failing JSON parse means the self-improvement loop degraded to fallback behavior. Encountered a 504 DEADLINE_EXCEEDED timeout during workflow execution. |

> *Scores based on actual Live Mode outputs from ChatGoogleGenerativeAI.*

---

### DeepSeek V2 16B (Local)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 5 | Code has logic errors. The initial `calculate_shipping` uses `(cart_total * weight)` in the formula -- multiplying the cart total by weight is mathematically wrong for a shipping cost. The discount logic applies the discount percentage inconsistently (only when cart_total > 100, despite calculating it for lower tiers). |
| Completeness | 5 | Basic code with some comments but missing type annotations, docstrings, and examples. Test suite has hard-coded expected values that don't match the function's actual formula. The refined version reduces the function to a single-parameter `calculate_shipping(weight)` -- dropping cart_total entirely. |
| Structure & Organization | 5 | Minimal code structure. Flask API uses `flask_restx` but has syntax errors (`fields.integer` should be `fields.Integer`). React component output is mostly prose instructions rather than actual code. Integration agent output is a description, not code. |
| Conciseness | 7 | Code is compact and not over-engineered. The shipping function is straightforward, and the Flask API is a reasonable skeleton. Less verbose than Gemini. |
| Source Grounding | 6 | Follows the basic TDG pattern. The initial test run correctly fails on `test_negative_weight` (the mock runner simulates the expected failure). However, the Planner Agent also failed JSON parsing, falling back to generic hypotheses. |
| Bloom's Level | **3 -- Apply** | Applies coding patterns to specifications but does not analyze or evaluate. The semantic code analysis identifies the anonymization issue but uses hedging language ("appears to be attempting") rather than definitive analysis. |
| Nuance & Caveats | 4 | Minimal commentary. The shipping function includes a comment about "adjust these rules according to your needs" but lacks the detailed caveats Gemini provides. Semantic analysis mentions "potential issues" without specificity. |
| Practical Utility | 4 | Code would need significant revision for production. Formula errors, syntax errors in Flask code, and the refined function dropping a required parameter make outputs unreliable. |

> *Scores based on actual Live Mode outputs from ChatOllama (DeepSeek V2 16B local).*

---

### OpenAI GPT-4o

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | Ran in Simulation Mode (MockLLM). All outputs are pre-authored mock responses, not GPT-4o generated. The mock code is correct -- `calculate_shipping` uses the proper formula `(base_rate + weight_cost) * (1 - discount)`. |
| Completeness | 7 | Mock outputs include clean code, test suites, and workflow completion. But these are the same MockLLM responses that any provider would get in simulation mode. |
| Structure & Organization | 7 | MockLLM outputs are well-structured with proper formatting. |
| Conciseness | 8 | Mock outputs are concise and focused. |
| Source Grounding | 8 | Mock responses are specifically authored for this chapter, so they follow patterns perfectly. |
| Bloom's Level | **4 -- Analyze** | Mock responses include structured analysis (KPI evaluation, hypothesis generation with confidence scores). The Planner generates 3 specific hypotheses with evidence counts. |
| Nuance & Caveats | 7 | Mock responses include specific trade-offs and confidence levels. |
| Practical Utility | 7 | Mock outputs demonstrate the pipeline well but cannot be attributed to GPT-4o's actual capabilities. |

> *IMPORTANT: This notebook ran in Simulation Mode (MockLLM). Scores reflect mock response quality, not GPT-4o's actual performance. Included for pipeline completeness only.*

---

## Overall Scorecard

| Dimension | Gemini Flash 2.5 | DeepSeek V2 (Local) | OpenAI GPT-4o* |
|---|---|---|---|
| Factual Accuracy | **8.0** | **5.0** | *7.0* |
| Completeness | **8.0** | **5.0** | *7.0* |
| Structure & Organization | **8.0** | **5.0** | *7.0* |
| Conciseness | **6.0** | **7.0** | *8.0* |
| Source Grounding | **7.0** | **6.0** | *8.0* |
| Bloom's Taxonomy Level | **4.0 (Analyze)** | **3.0 (Apply)** | *4.0 (Analyze)* |
| Nuance & Caveats | **7.0** | **4.0** | *7.0* |
| Practical Utility | **7.0** | **4.0** | *7.0* |
| **WEIGHTED AVERAGE** | **6.9** | **4.9** | *6.9* |

> *OpenAI GPT-4o ran in Simulation Mode -- scores reflect MockLLM, not actual GPT-4o output. Claude Sonnet 4 had no saved outputs and is excluded.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     | ############ Gemini Flash 2.5
Level 3: Apply       | ############ DeepSeek V2 (Local)
Level 2: Understand  |
Level 1: Remember    |
```

Gemini reaches Level 4 by analyzing code structure and identifying compliance violations with specific regulatory citations. DeepSeek applies coding patterns at Level 3 but does not break down problems systematically. OpenAI (MockLLM) is excluded from Bloom's ranking since outputs are pre-authored.

---

## Visual Summary

### Overall Score Comparison (Live Providers Only)

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  Gemini Flash 2.5       6.9  ####################..........
  DeepSeek V2 (Local)    4.9  ##############................
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     |
  L4 Analyze      | G
  L3 Apply        | G D
  L2 Understand   | G D
  L1 Remember     | G D
```

Legend: **G** = Gemini Flash 2.5, **D** = DeepSeek V2

---

## Winner: Gemini Flash 2.5

| | |
|---|---|
| **Chapter 9 Winner** | **Gemini Flash 2.5** |
| **Score** | **6.9 / 10** |
| **Bloom's Level** | **Level 4 -- Analyze** |

**Why Gemini Flash 2.5 wins this chapter:**
- Only live cloud provider with actual outputs (Claude had no outputs, OpenAI ran on MockLLM)
- Generated well-structured, documented code with type annotations and comprehensive docstrings
- Produced meaningful semantic compliance analysis identifying retained HIPAA identifiers
- 2.0-point lead over DeepSeek V2 (4.9)

**Runner-up:** DeepSeek V2 16B (4.9/10) -- functional but significant accuracy issues

**Not ranked (Simulation Mode):** OpenAI GPT-4o (MockLLM only), Claude Sonnet 4 (no outputs)

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality | Gemini Flash 2.5 | Only live cloud provider with real outputs |
| Air-gapped / private data | DeepSeek V2 (Local) | Zero cloud dependency; code stays on machine |
| Rapid prototyping | DeepSeek V2 (Local) | No API key, instant iteration, zero cost |
| Cost-efficient production | Gemini Flash 2.5 | Competitive pricing with solid code quality |


## Provider Profiles for This Chapter

### Gemini Flash 2.5 -- "The Verbose Architect"
**Strengths:** Comprehensive code generation with extensive documentation; good semantic analysis; proper input validation.
**Weaknesses:** Overly verbose -- generates full project scaffolding when focused snippets are needed; occasional spec drift (adding unrequested parameters); Planner JSON parsing failures requiring fallback; timeout errors during workflow execution.

### DeepSeek V2 16B -- "The Rough Draft Generator"
**Strengths:** Compact code; fast local execution; zero API cost.
**Weaknesses:** Formula errors in core logic; syntax errors in Flask code; refined code drops required parameters; generic prose instead of code for frontend tasks; Planner JSON parsing failures.

### OpenAI GPT-4o -- "Simulation Only"
**Note:** Ran in Simulation Mode (MockLLM). All outputs are pre-authored mock responses identical to any simulation run. Cannot assess actual GPT-4o code generation quality from this chapter's outputs.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Code generation** | Gemini Flash 2.5 | Best actual code quality observed in live outputs |
| **Compliance scanning** | Gemini Flash 2.5 | Produced detailed semantic compliance analysis |
| **Rapid local prototyping** | Ollama DeepSeek V2 | Zero cost; immediate feedback; acceptable for scaffolding |
| **Self-improving agents** | Gemini Flash 2.5 | Better (though still imperfect) structured output parsing |

---

*Analysis based on actual Chapter 9 notebook execution outputs, April 2026. Gemini and DeepSeek ran in Live Mode with real LLM outputs. OpenAI ran in Simulation Mode (MockLLM). Claude had no saved outputs. Compliance scanning, data flow analysis, and measured outcomes sections use deterministic pipelines -- identical across providers.*
