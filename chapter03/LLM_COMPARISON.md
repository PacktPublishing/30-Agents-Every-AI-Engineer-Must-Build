# Chapter 3 — LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 3 Agent Prompting tasks: persona construction, chain-of-thought reasoning, and Tree-of-Thought synthesis for product launch strategy.

---

## Agent Tasks in This Chapter

- **Bare vs. Persona-Constrained Prompting** — Demonstrating how persona shaping changes response quality
- **Persona Consistency** — Multi-turn responses maintaining empathetic customer support persona
- **Enterprise Persona Construction** — Role, expertise, tone, reasoning style, context, and guardrails
- **Chain-of-Thought Reasoning** — Step-by-step problem decomposition
- **Tree-of-Thought (ToT)** — Multi-expert virtual strategy team (market analyst, finance director, CMO) synthesizing a product launch plan

## Scoring Dimensions

Each provider is rated 0–10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of generated strategies, market analysis, financial projections |
| **Completeness** | Coverage of all expert perspectives and synthesis quality |
| **Structure & Organization** | Use of sections, headers, analytical frameworks |
| **Conciseness** | Information density without unnecessary padding |
| **Source Grounding** | Adherence to the chapter's prompting patterns and constraints |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Acknowledgment of risks, market uncertainties, competing factors |
| **Practical Utility** | How useful the output would be for an actual product launch decision |

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

## Task 1: Persona-Constrained Response (Fitness Coach)

### Claude Sonnet 4

**Response characteristics:**
- Clear differentiation between bare and persona-constrained outputs
- Persona response used motivational language, structured workout progression, and safety caveats
- Maintained consistent empathetic tone across multi-turn interactions

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Fitness advice is sound and safe |
| Completeness | 9 | Covered warm-up, main workout, cool-down, and progression |
| Structure & Organization | 10 | Markdown headers, numbered steps, bold emphasis |
| Conciseness | 8 | Comprehensive but slightly verbose |
| Source Grounding | 9 | Persona constraints clearly reflected in output |
| Bloom's Level | **5 — Evaluate** | Assessed user's likely fitness level and adapted recommendations |
| Nuance & Caveats | 9 | Safety warnings, modification suggestions, "listen to your body" |
| Practical Utility | 9 | Actionable fitness plan a beginner could follow |

---

### Gemini Flash 2.5

**Response characteristics:**
- Good differentiation between bare and persona modes
- Persona response was energetic and concise
- Less detailed progression path than Claude

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Accurate fitness guidance |
| Completeness | 7 | Covered main points but less depth on modifications |
| Structure & Organization | 8 | Bullet points with clear sections |
| Conciseness | 9 | Tight, energetic language |
| Source Grounding | 8 | Good persona adherence |
| Bloom's Level | **4 — Analyze** | Broke down workout into logical phases |
| Nuance & Caveats | 6 | Basic safety note but less detailed |
| Practical Utility | 8 | Followable plan with less hand-holding |

---

### DeepSeek V2 16B (Local)

**Response characteristics:**
- Basic differentiation between modes
- Persona response was functional but generic
- Less motivational language, more clinical tone

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct basic fitness information |
| Completeness | 6 | Minimal workout detail |
| Structure & Organization | 6 | Simple list format |
| Conciseness | 9 | Very brief |
| Source Grounding | 6 | Partial persona adherence — tone not consistently motivational |
| Bloom's Level | **3 — Apply** | Applied fitness knowledge to the request |
| Nuance & Caveats | 4 | Minimal safety considerations |
| Practical Utility | 6 | Too sparse to follow without additional guidance |

---

### OpenAI GPT-4o

**Response characteristics:**
- Strong differentiation between bare and persona-constrained modes
- Natural, encouraging tone with practical progression tips
- Included rest day recommendations and hydration reminders

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Sound fitness advice |
| Completeness | 8 | Good coverage including recovery |
| Structure & Organization | 9 | Well-organized with clear sections |
| Conciseness | 8 | Good balance of detail and brevity |
| Source Grounding | 9 | Strong persona adherence |
| Bloom's Level | **4 — Analyze** | Analyzed user needs and structured a progressive plan |
| Nuance & Caveats | 7 | Included rest and recovery guidance |
| Practical Utility | 9 | Actionable and motivating |

---

## Task 2: Tree-of-Thought — Product Launch Strategy

This is the primary LLM-differentiated task. Three virtual experts (Market Analyst, Finance Director, CMO) analyze independently, then a Synthesis Expert integrates their perspectives into a unified launch strategy.

### Claude Sonnet 4

**Response characteristics:**
- Market analysis included TAM/SAM/SOM estimates with percentage breakdowns
- Finance branch produced pricing models with sensitivity analysis
- Marketing branch developed multi-channel strategy with timeline
- Synthesis was deeply integrative — identified tensions between branches and proposed resolutions
- Final output included risk matrix and contingency triggers

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Plausible market data and financial projections |
| Completeness | 10 | All three branches plus deep synthesis with risk assessment |
| Structure & Organization | 10 | Each branch clearly delineated; synthesis referenced specific branch outputs |
| Conciseness | 7 | Extensive — 4 detailed sections |
| Source Grounding | 9 | Follows the ToT architecture precisely as designed in the chapter |
| Bloom's Level | **6 — Create** | Synthesized three independent analyses into a novel integrated strategy |
| Nuance & Caveats | 10 | Risk matrix, contingency triggers, acknowledged expert disagreements |
| Practical Utility | 10 | Could serve as an actual board-level strategy document |

---

### Gemini Flash 2.5

**Response characteristics:**
- Market analysis focused on competitive positioning with clear segments
- Finance branch provided pricing tiers and break-even analysis
- Marketing branch outlined digital-first launch strategy
- Synthesis combined perspectives into a phased rollout plan

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Reasonable projections; less granular than Claude |
| Completeness | 8 | All branches covered; synthesis less integrative |
| Structure & Organization | 8 | Clear sections with bullet points |
| Conciseness | 9 | Efficient delivery of key points |
| Source Grounding | 8 | Follows ToT structure |
| Bloom's Level | **5 — Evaluate** | Evaluated market position and recommended strategy based on assessment |
| Nuance & Caveats | 7 | Mentioned competitive risks and market uncertainties |
| Practical Utility | 8 | Good executive summary; needs more detail for execution |

---

### DeepSeek V2 16B (Local)

**Response characteristics:**
- Each branch produced basic analysis with limited depth
- Market analysis mentioned key segments without quantification
- Finance section had simplified pricing model
- Synthesis was more summary than integration — listed branch conclusions sequentially

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | General claims without specific backing |
| Completeness | 6 | Branches present but thin; synthesis lacks integration |
| Structure & Organization | 6 | Basic sections without deep structure |
| Conciseness | 8 | Short but at cost of depth |
| Source Grounding | 7 | Follows ToT format but with less sophistication |
| Bloom's Level | **3 — Apply** | Applied the ToT pattern without true analytical depth per branch |
| Nuance & Caveats | 4 | Minimal risk discussion |
| Practical Utility | 5 | Too high-level for actionable strategy |

---

### OpenAI GPT-4o

**Response characteristics:**
- Market analysis included competitor mapping and positioning strategy
- Finance branch produced tiered pricing with customer segment alignment
- Marketing developed a go-to-market timeline with KPIs
- Synthesis identified key trade-offs and recommended a balanced approach

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Well-reasoned market and financial projections |
| Completeness | 9 | Strong branch outputs with good synthesis |
| Structure & Organization | 9 | Clear hierarchy with actionable recommendations |
| Conciseness | 8 | Well-balanced verbosity |
| Source Grounding | 9 | Follows ToT architecture closely |
| Bloom's Level | **5 — Evaluate** | Evaluated trade-offs between branches and made judgment calls |
| Nuance & Caveats | 8 | Acknowledged uncertainties and trade-offs |
| Practical Utility | 9 | Near-production quality strategy document |

---

## Overall Scorecard

| Dimension | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) | OpenAI GPT-4o |
|---|---|---|---|---|
| Factual Accuracy | **9.0** | **8.5** | **7.5** | **9.0** |
| Completeness | **9.5** | **7.5** | **6.0** | **8.5** |
| Structure & Organization | **10.0** | **8.0** | **6.0** | **9.0** |
| Conciseness | **7.5** | **9.0** | **8.5** | **8.0** |
| Source Grounding | **9.0** | **8.0** | **6.5** | **9.0** |
| Bloom's Taxonomy Level | **5.5 (Evaluate/Create)** | **4.5 (Analyze/Evaluate)** | **3.0 (Apply)** | **4.5 (Analyze/Evaluate)** |
| Nuance & Caveats | **9.5** | **6.5** | **4.0** | **7.5** |
| Practical Utility | **9.5** | **8.0** | **5.5** | **9.0** |
| **WEIGHTED AVERAGE** | **8.7** | **7.5** | **5.9** | **8.1** |

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      | ████████████ Claude Sonnet 4 (ToT synthesis)
Level 5: Evaluate    | ████████████ Claude (persona), Gemini (ToT), GPT-4o (ToT)
Level 4: Analyze     | ████████████ Gemini (persona), GPT-4o (persona)
Level 3: Apply       | ████████████ DeepSeek V2 (Local)
Level 2: Understand  |
Level 1: Remember    |
```

Claude's ToT synthesis reaches **Level 6 (Create)** by producing a genuinely novel integrated strategy that resolves tensions between the three expert branches — this goes beyond evaluation into creative synthesis. GPT-4o and Gemini reach Level 5 in the ToT task by evaluating trade-offs, while DeepSeek stays at Level 3 by applying the pattern without deep analytical reasoning in each branch.

---

## Provider Profiles for This Chapter

### Claude Sonnet 4 — "The Strategist"
**Strengths:** Deepest Tree-of-Thought synthesis; identifies inter-branch tensions; risk matrices; production-quality strategy output.
**Weaknesses:** Most verbose — high token consumption for comprehensive analysis.

### Gemini Flash 2.5 — "The Executive Summary"
**Strengths:** Efficient branch analysis; good evaluation of market positioning; fastest execution.
**Weaknesses:** Synthesis less integrative — more sequential summary than true integration.

### DeepSeek V2 16B — "The Outline Generator"
**Strengths:** Follows ToT structure correctly; zero cloud cost; good for testing pipeline architecture.
**Weaknesses:** Branches lack quantitative depth; synthesis doesn't integrate — just concatenates.

### OpenAI GPT-4o — "The Balanced Strategist"
**Strengths:** Strong across all branches; good balance of depth and clarity; actionable KPIs in marketing branch.
**Weaknesses:** Slightly less creative in synthesis than Claude; doesn't explicitly identify branch conflicts.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Strategic planning (ToT)** | Claude Sonnet 4 | Deepest multi-perspective synthesis with conflict resolution |
| **Quick strategy drafts** | OpenAI GPT-4o | Strong quality with faster turnaround |
| **Persona-driven chatbots** | Claude or GPT-4o | Best persona adherence and natural tone |
| **High-volume prompt testing** | Gemini Flash 2.5 | Lowest cost for iterating on prompt designs |
| **Local prompt engineering** | Ollama DeepSeek V2 | Free iteration on pipeline architecture |

---

*Analysis based on Chapter 3 notebook outputs executed April 2026. All four providers ran in LIVE mode. Chapter 3 shows significant LLM differentiation, especially in the Tree-of-Thought synthesis task.*
