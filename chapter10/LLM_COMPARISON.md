# Chapter 10 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of LLM providers running the Chapter 10 Conversational and Content Creation tasks: mental health support agent, marketing content assistant, and brand compliance pipeline.

---

## Agent Tasks in This Chapter

- **Mental Health Support Agent** -- Multi-turn dialogue with safety layer, crisis detection, working memory, semantic memory, and persona-driven responses
- **Marketing Content Assistant** -- Campaign brief to multi-asset output (email, SEO post, ad copy) with brand guideline enforcement
- **Brand Compliance Pipeline** -- Forbidden word detection, tone validation, consistency scoring, and revision loops

## Scoring Dimensions

Each provider is rated 0-10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of dialogue responses, content claims, and brand compliance |
| **Completeness** | Coverage of conversation context, content depth, asset variety |
| **Structure & Organization** | Dialogue coherence, content formatting, campaign structure |
| **Conciseness** | Natural conversation length without unnecessary verbosity |
| **Source Grounding** | Adherence to the chapter's conversational and brand patterns |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Handling of ambiguity, crisis detection, and context shifts |
| **Practical Utility** | How natural and useful the outputs would be in production |

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

## Key Observation: All Providers Used Simulation Mode

Chapter 10 uses a **LangChain-based pipeline** where memory management, safety layers, brand guidelines, and consistency scoring are all deterministic. The LLM drives dialogue generation and content creation.

**Critical finding:** No provider ran with live LLM outputs in this chapter:

- **OpenAI GPT-4o**: Simulation Mode (MockChatOpenAI) -- explicitly logged "SIMULATION MODE -- No API key found"
- **Gemini Flash 2.5**: Attempted Live Mode but fell back to MockChatOpenAI due to `ModelProfile` import error in `langchain_core.language_models`. Also failed on image generation (`'GenerativeModel' object has no attribute 'images'`). All dialogue and content outputs come from MockLLM.
- **Claude Sonnet 4**: No saved outputs (0 output cells)
- **DeepSeek V2 16B**: No saved outputs (0 output cells)

**Consequence:** The OpenAI and Gemini notebooks produce identical mock outputs -- the same pre-authored responses for dialogue turns, campaign assets, and brand compliance. There is no actual LLM differentiation to score.

---

## Provider Execution Status

| Provider | Output Cells | Mode | LLM Used |
|---|---|---|---|
| OpenAI GPT-4o | 19 | Simulation | MockChatOpenAI |
| Gemini Flash 2.5 | 19 | Fallback to Mock | MockChatOpenAI (import error) |
| Claude Sonnet 4 | 0 | Not executed | -- |
| DeepSeek V2 16B | 0 | Not executed | -- |

---

## Observed Outputs (MockLLM -- Identical Across Both Providers)

Both OpenAI and Gemini notebooks produce the same mock outputs:

### Mental Health Support Agent (Section 10.1)
- **Turn 1**: "It sounds like the pressure of exams is really weighing on you right now. That's a very common experience..."
- **Turn 2**: Identical response to Turn 1 (mock limitation -- no multi-turn adaptation)
- **Turn 3**: Semantic memory retrieval works (deterministic), but agent response is again identical
- **Crisis detection**: "I'm hearing that you're in a lot of pain. I am an AI and cannot provide emergency help. Please call 988 immediately."

### Marketing Content Assistant (Section 10.2)
- **Email draft**: "Subject: Unlock Enterprise-Grade Data Governance with DataVault Pro" -- professional, on-brief
- **SEO post**: "# Why Enterprise Data Governance Is No Longer Optional" -- targeted to CTOs
- **Ad copy**: "DataVault Pro -- Govern your data, accelerate your decisions." -- concise, on-brand
- **Analytics**: email_open_rate: 0.28, seo_click_rate: 0.14, ad_conversion: 0.04

### Brand Compliance Pipeline
- Correctly detects forbidden words ("cheap", "free trial")
- Consistency scoring formula: C = 1/n x Sigma phi(Ai, G)
- Clean artifact: C = 0.967; Violating artifact: C = 0.3

---

## Scoring

Because all executed notebooks used MockLLM with identical outputs, individual provider scoring is not meaningful. Instead, the mock response quality is assessed once:

### MockLLM Response Quality

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | Dialogue responses are appropriate but repetitive across turns |
| Completeness | 6 | Multi-turn dialogue repeats Turn 1 response for all turns -- no adaptation |
| Structure & Organization | 8 | Campaign assets are well-formatted with clear structure |
| Conciseness | 8 | Responses are appropriately sized -- not verbose |
| Source Grounding | 8 | Mock responses follow the chapter's therapeutic and marketing patterns |
| Bloom's Level | **3 -- Apply** | Applies persona patterns without analyzing or adapting to new context |
| Nuance & Caveats | 5 | Crisis detection works well, but dialogue lacks nuance across turns |
| Practical Utility | 6 | Campaign output is solid; dialogue would need real LLM for multi-turn quality |

**MockLLM Weighted Average: 6.4 / 10**

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o* | Gemini Flash 2.5* | Claude Sonnet 4 | DeepSeek V2 |
|---|---|---|---|---|
| All dimensions | *MockLLM* | *MockLLM* | No outputs | No outputs |
| **WEIGHTED AVERAGE** | *6.4* | *6.4* | N/A | N/A |

> *Both providers ran on MockLLM -- scores are identical and reflect mock quality, not provider capability.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     |
Level 3: Apply       | ############ MockLLM (all providers)
Level 2: Understand  |
Level 1: Remember    |
```

The MockLLM applies persona patterns (reflective questioning, empathetic validation) but does not analyze conversation history or adapt across turns. A live LLM would likely reach Level 4 or 5 by analyzing accumulated context.

---

## Visual Summary

### Execution Status

```
  Provider              Status         Mode
  --------------------  ------------   ----------------
  OpenAI GPT-4o         Executed       Simulation (Mock)
  Gemini Flash 2.5      Executed       Fallback to Mock
  Claude Sonnet 4       Not executed   --
  DeepSeek V2 (Local)   Not executed   --
```

---

## Winner: No Winner -- Insufficient Live Data

| | |
|---|---|
| **Chapter 10 Winner** | **No winner declared** |
| **Reason** | No provider ran with live LLM outputs |

**All executed notebooks used MockLLM with identical outputs.** A meaningful comparison requires re-running with live API keys.

### Observations from Pipeline Design

The chapter architecture reveals important characteristics that would differentiate providers in live mode:

1. **Safety Layer** (deterministic): Crisis keyword detection, 988 referral -- identical across providers
2. **Working Memory** (deterministic): Token-limited buffer -- identical across providers
3. **Semantic Memory** (embedding-dependent): Would differentiate with live embeddings; mock embeddings give identical results
4. **Dialogue Generation** (LLM-dependent): The primary differentiator -- mock returns same response for all turns
5. **Campaign Content** (LLM-dependent): Would show real quality differences with live LLMs
6. **Brand Compliance** (deterministic): Forbidden word and consistency checks -- identical

### Best Provider by Scenario (Estimated)

| Scenario | Likely Best Choice | Why |
|---|---|---|
| Production chatbot | OpenAI GPT-4o or Claude | Historically strong at multi-turn dialogue |
| Content creation | Claude Sonnet 4 | Strong at structured content with depth |
| High-volume chat | Gemini Flash 2.5 | Fastest response times for conversational workloads |
| Local testing | DeepSeek V2 (Local) | Zero cost for pipeline development |

---

## Recommendations

| Use Case | Recommended Action | Why |
|---|---|---|
| **Comparing providers** | Re-run with live API keys | Current outputs are all MockLLM |
| **Pipeline validation** | Use current mock outputs | Mock mode proves pipeline correctness |
| **Content quality** | Any cloud provider | Campaign asset structure is well-designed |
| **Crisis detection** | Any provider | Safety layer is deterministic and works correctly |

---

*Analysis based on Chapter 10 notebook execution outputs, April 2026. Both OpenAI and Gemini notebooks ran in Simulation Mode (MockLLM) with identical outputs. Gemini attempted Live Mode but fell back due to langchain_core import errors. Claude and DeepSeek had no saved outputs. No meaningful LLM provider comparison is possible from current data.*
