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

## Execution Modes

All three providers with outputs ran in **Live Mode** with real API calls. Claude Sonnet 4 had no saved outputs (notebook never executed).

| Provider | Output Cells | Mode | LLM Backend |
|---|---|---|---|
| Gemini Flash 2.5 | 32 | Live Mode | ChatGoogleGenerativeAI |
| OpenAI GPT-4o | 32 | Live Mode | ChatOpenAI |
| DeepSeek V2 16B | 32 | Live Mode | ChatOllama (local) |
| Claude Sonnet 4 | 0 | Not executed | -- |

**Note:** Compliance scanning (PolicyEngine, DataFlowAnalyzer), remediation, audit trails, sensing, critic KPI evaluation, and HITL checkpoint sections use deterministic pipelines and are identical across all providers. The LLM differentiates in code generation, test synthesis, semantic analysis, and hypothesis generation. All three providers encountered JSON parse failures in the PlannerAgent, triggering identical fallback hypotheses.

---

## Provider Performance

### OpenAI GPT-4o

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Code synthesis produces a correct `calculate_shipping(cart_total, weight)` with proper formula: `base_rate + weight * weight_cost_per_unit`, discount tiers at $50 and $100. The refined version correctly adds `ValueError` for negative weight. Semantic analysis accurately identifies four retained PII fields (email, phone_number, date_of_birth, ip_address). |
| Completeness | 7 | Initial code covers base rate, weight cost, and tiered discounts but lacks type annotations and docstrings. Test suite covers 5 cases including `test_negative_weight` with `pytest.raises`. The refined version drops the `cart_total` parameter entirely, reducing to `calculate_shipping(weight)` -- a significant spec regression. |
| Structure & Organization | 7 | Code is clean with inline comments explaining each step. Flask API starts with model definition (SQLAlchemy). React component uses TypeScript interfaces with `useState`/`useEffect` hooks. However, the refined function is oversimplified. |
| Conciseness | 8 | Initial code is compact (20 lines) without over-engineering. The task assignment prompt, while detailed, stays focused on requirements. Semantic analysis at 1830 chars is well-scoped. |
| Source Grounding | 7 | Follows the TDG cycle correctly. The initial code-then-test-then-refine loop works as designed. But the PlannerAgent fails JSON parsing (char 0), falling back to generic "Investigate and improve X" hypotheses identical to other providers. |
| Bloom's Level | **4 -- Analyze** | Semantic analysis breaks down the anonymization function's behavior vs. its docstring claim, identifying specific retained fields and their regulatory implications under HIPAA/GDPR. The task assignment prompt structures requirements into base cost, discounts, and edge cases. |
| Nuance & Caveats | 7 | Semantic analysis identifies "Incomplete Anonymization" and "Misleading Documentation" as separate violation categories. The task assignment includes explicit edge cases (weight over 20 kg, minimum shipping cost). |
| Practical Utility | 7 | Initial code is production-usable. React component with TypeScript interfaces is well-structured for real frontend work. The Flask API starts at the model layer, which is appropriate. However, the refined function dropping `cart_total` would break integration. |

> *Scores based on actual Live Mode outputs from ChatOpenAI (GPT-4o).*

---

### Gemini Flash 2.5

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Code synthesis produces a correct function with type annotations, `ValueError` for negative inputs, named constants (`BASE_RATE = 5.00`, `WEIGHT_UNIT_COST = 0.50`), and tiered discounts. Semantic analysis produces a 5068-char compliance report correctly identifying "severe semantic compliance violations" in the anonymization function. |
| Completeness | 8 | Most thorough code generation of all providers: comprehensive docstrings with Args/Returns/Raises sections, input validation from the start, and configurable constants. Test suite uses `@pytest.mark.parametrize` with multiple tiers (basic, tier one, tier two). However, the refined version adds `distance` and `bulky_item_surcharge` parameters not in the original spec. |
| Structure & Organization | 8 | Best organization of all providers. Code uses named constants, explicit discount tier thresholds, and complete type annotations. The Flask API attempts a full project layout with blueprints and factory pattern. Semantic analysis is formatted as a structured compliance report with code block, findings summary, and violation details. |
| Conciseness | 6 | Most verbose provider. The initial code has extensive docstrings (good for production, but increases output size). Flask API response includes full multi-file project scaffolding instead of focused code. React output includes mock API setup instructions rather than just the component. The refined function adds 3 extra parameters. |
| Source Grounding | 7 | Follows the TDG pattern with proper test parametrization. Semantic analysis uses a structured compliance report format aligned with the chapter's scan-evaluate-remediate pattern. The PlannerAgent also fails JSON parsing, falling back to generic hypotheses. |
| Bloom's Level | **4 -- Analyze** | Semantic compliance analysis identifies the docstring-vs-behavior mismatch, enumerates retained HIPAA identifiers, and categorizes the violation. The parametrized test suite shows systematic analysis of boundary conditions across discount tiers. |
| Nuance & Caveats | 7 | Code includes "CUSTOMIZE THESE TO YOUR BUSINESS RULES" comments and separate validation for each input parameter. The initial task assignment caveats that "specific shipping rates and discount rules were not provided." Semantic analysis distinguishes severity levels. |
| Practical Utility | 7 | Generated code is closest to production-ready with type annotations, docstrings, and input validation. But over-engineering is a concern -- Flask output is an entire project scaffold, and the refined function drifts from the spec by adding unrequested parameters. |

> *Scores based on actual Live Mode outputs from ChatGoogleGenerativeAI.*

---

### DeepSeek V2 16B (Local)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 5 | Initial `calculate_shipping` has a logic error: applies discount as `cart_total * (discount / 100)` instead of applying the percentage to the shipping cost. This means a $120 cart with 10 units of weight would subtract $24 (20% of cart_total) from a $10 shipping cost, yielding a negative result. Test suite references a `discount` parameter that the function does not accept (`calculate_shipping(100, 50, discount=0.2)`). |
| Completeness | 5 | Basic implementation with no type annotations, no docstrings, and no input validation in the initial version. The refined version reduces to a single-parameter `calculate_shipping(weight)` with a trivial `weight * 1.23` formula, losing all business logic. Test assertions use hard-coded expected values that do not match the function's formula. |
| Structure & Organization | 5 | Minimal code structure. Flask API output is prose instructions ("Step 4: Implement Error Handling") rather than actual code. React component output starts with project setup instructions before showing any code. Integration agent output is a single sentence about wrapping with Router. |
| Conciseness | 7 | The most compact outputs of all providers. Code is short and direct. No unnecessary scaffolding or configuration. The downside is that brevity comes at the cost of correctness and completeness. |
| Source Grounding | 6 | Follows the basic TDG cycle. The initial test run simulates expected failure on `test_negative_weight`. But the PlannerAgent also fails JSON parsing (char 1), and the test suite references parameters the function does not accept. |
| Bloom's Level | **3 -- Apply** | Applies basic coding patterns to the specification without analyzing requirements or evaluating edge cases. Semantic analysis uses hedging ("appears to be attempting") rather than definitive identification of violations. Does not break down the problem into structured categories. |
| Nuance & Caveats | 4 | Minimal commentary. One comment about "adjust these rules according to your needs." No mention of trade-offs, limitations, or edge cases. The semantic analysis mentions "potential issues" without specifying regulatory frameworks. |
| Practical Utility | 4 | Code would need significant revision. The core shipping formula is wrong, the refined version drops required parameters, test assertions are mismatched, and frontend/backend outputs are instructions rather than code. Only usable as rough scaffolding. |

> *Scores based on actual Live Mode outputs from ChatOllama (DeepSeek V2 16B, running locally).*

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|
| Factual Accuracy | 8.0 | 8.0 | 5.0 |
| Completeness | 7.0 | 8.0 | 5.0 |
| Structure & Organization | 7.0 | 8.0 | 5.0 |
| Conciseness | 8.0 | 6.0 | 7.0 |
| Source Grounding | 7.0 | 7.0 | 6.0 |
| Bloom's Taxonomy Level | 4.0 (Analyze) | 4.0 (Analyze) | 3.0 (Apply) |
| Nuance & Caveats | 7.0 | 7.0 | 4.0 |
| Practical Utility | 7.0 | 7.0 | 4.0 |
| **WEIGHTED AVERAGE** | **6.9** | **6.9** | **4.9** |

> *Claude Sonnet 4 had no saved outputs and is excluded.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     | ############ OpenAI GPT-4o, Gemini Flash 2.5
Level 3: Apply       | ############ DeepSeek V2 (Local)
Level 2: Understand  |
Level 1: Remember    |
```

OpenAI and Gemini both reach Level 4 through structured semantic analysis of code behavior vs. documentation claims, identifying specific regulatory implications. DeepSeek applies coding patterns at Level 3 but does not systematically analyze or evaluate.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  OpenAI GPT-4o          6.9  ####################..........
  Gemini Flash 2.5       6.9  ####################..........
  DeepSeek V2 (Local)    4.9  ##############................
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     |
  L4 Analyze      | O G
  L3 Apply        | O G D
  L2 Understand   | O G D
  L1 Remember     | O G D
```

Legend: **O** = OpenAI GPT-4o, **G** = Gemini Flash 2.5, **D** = DeepSeek V2

---

## Winner: Tied -- OpenAI GPT-4o and Gemini Flash 2.5

| | |
|---|---|
| **Chapter 9 Winner** | **Tied: OpenAI GPT-4o and Gemini Flash 2.5** |
| **Score** | **6.9 / 10** |
| **Bloom's Level** | **Level 4 -- Analyze** |

**Why the tie:** Both providers score identically at 6.9. They trade strengths in complementary areas: OpenAI produces more concise, focused code (8.0 vs 6.0 on Conciseness), while Gemini produces more complete, documented code (8.0 vs 7.0 on Completeness and Structure). Both achieve Level 4 Bloom's through semantic compliance analysis. Both suffer from PlannerAgent JSON parse failures.

**Key differentiators:**
- **OpenAI GPT-4o**: Cleaner initial code, better-scoped outputs, TypeScript React component with interfaces. But the refined function drops `cart_total`, a notable spec regression.
- **Gemini Flash 2.5**: Best documentation with type annotations, parametrized tests, and structured compliance reports. But over-engineers outputs (full project scaffolding, unrequested parameters in refinement).

**Third place:** DeepSeek V2 16B (4.9/10) -- functional but has formula errors, mismatched test parameters, and outputs that are instructions rather than code.

**Not ranked:** Claude Sonnet 4 (no saved outputs)

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum code quality | Gemini Flash 2.5 | Type annotations, docstrings, comprehensive validation |
| Concise code generation | OpenAI GPT-4o | Compact, focused output without over-engineering |
| Air-gapped / private data | DeepSeek V2 (Local) | Zero cloud dependency; code stays on machine |
| Rapid prototyping | DeepSeek V2 (Local) | No API key, instant iteration, zero cost |
| Semantic compliance analysis | Gemini Flash 2.5 or OpenAI GPT-4o | Both produce structured, regulation-aware analysis |

## Provider Profiles for This Chapter

### OpenAI GPT-4o -- "The Pragmatic Coder"
**Strengths:** Concise, readable code; proper discount logic; TypeScript React component with interfaces; well-scoped semantic analysis (1830 chars).
**Weaknesses:** No type annotations or docstrings in initial code; refined version drops `cart_total` parameter entirely; PlannerAgent JSON parse failure at char 0.

### Gemini Flash 2.5 -- "The Thorough Documenter"
**Strengths:** Type annotations, comprehensive docstrings, named constants, parametrized test cases, structured compliance report format (5068 chars).
**Weaknesses:** Verbose -- Flask output is full project scaffold; refined version adds 3 unrequested parameters (`distance`, `shipping_rate_per_kg`, `bulky_item_surcharge`); PlannerAgent JSON parse failure.

### DeepSeek V2 16B -- "The Quick Sketcher"
**Strengths:** Compact output; fast local execution; zero API cost.
**Weaknesses:** Formula error (subtracts percentage of cart_total from shipping cost); test suite references non-existent `discount` parameter; refined version reduces to trivial `weight * 1.23`; frontend/backend outputs are prose instructions, not code.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Code generation** | OpenAI GPT-4o or Gemini Flash 2.5 | Both produce correct, usable code; choice depends on verbosity preference |
| **Compliance scanning** | Gemini Flash 2.5 | Most detailed semantic compliance report (5068 chars vs 1830) |
| **Rapid local prototyping** | DeepSeek V2 16B (Ollama) | Zero cost; immediate feedback; acceptable for quick scaffolding |
| **Self-improving agents** | Any cloud provider | All three fail PlannerAgent JSON parsing; pipeline needs structured output enforcement |

---

*Analysis based on actual Chapter 9 notebook execution outputs, April 2026. Gemini, OpenAI, and DeepSeek all ran in Live Mode with real LLM outputs. Claude had no saved outputs. Compliance scanning, data flow analysis, sensing, critic, HITL, and learning sections use deterministic pipelines identical across all providers.*
