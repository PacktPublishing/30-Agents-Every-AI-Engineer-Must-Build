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

## Key Observation: All Providers Fell Back to Simulation Mode

Chapter 10 uses a **LangChain-based pipeline** where memory management, safety layers, brand guidelines, and consistency scoring are all deterministic. The LLM drives dialogue generation and content creation.

**Critical finding:** No provider ran with live LLM outputs in this chapter:

- **Gemini Flash 2.5**: Attempted Live Mode but `ChatGoogleGenerativeAI` failed with `cannot import name 'ModelProfile' from 'langchain_core.language_models'`. Also failed on image generation (`'GenerativeModel' object has no attribute 'images'`). All dialogue and content outputs come from MockChatOpenAI fallback.
- **OpenAI GPT-4o**: Attempted Live Mode but `ChatOpenAI` failed with `Client.__init__() got an unexpected keyword argument 'proxies'`. `OpenAIEmbeddings` also failed with the same error. All outputs come from MockChatOpenAI fallback.
- **Claude Sonnet 4**: No saved outputs (0 output cells -- notebook never executed).
- **DeepSeek V2 16B**: No saved outputs (0 output cells -- notebook never executed).

**Consequence:** The Gemini and OpenAI notebooks produce byte-identical mock outputs. Every dialogue turn, every campaign asset, every brand compliance check is from the same MockChatOpenAI. There is no actual LLM differentiation to evaluate.

---

## Provider Execution Status

| Provider | Output Cells | Declared Mode | Actual LLM Used | Fallback Reason |
|---|---|---|---|---|
| Gemini Flash 2.5 | 19 | Live (Google) | MockChatOpenAI | `ModelProfile` import error |
| OpenAI GPT-4o | 19 | Live (OpenAI) | MockChatOpenAI | `proxies` keyword error |
| Claude Sonnet 4 | 0 | Not executed | -- | -- |
| DeepSeek V2 16B | 0 | Not executed | -- | -- |

---

## Observed Outputs (MockLLM -- Identical Across Both Executed Providers)

Both Gemini and OpenAI notebooks produce the same mock outputs:

### Mental Health Support Agent (Section 10.1)
- **Safety Layer**: Crisis keyword detection works correctly -- "I want to hurt myself" triggers 988 hotline referral
- **Working Memory**: Token-limited buffer stores 2 messages per turn
- **Semantic Memory**: FAISS vector store archives and retrieves summaries ("User discussed feeling anxious about upcoming math exam")
- **Turn 1 response**: "It sounds like the pressure of exams is really weighing on you right now. That's a very common experience..."
- **Multi-turn limitation**: Mock returns repetitive responses across turns -- no genuine multi-turn adaptation
- **Turn 4**: Crisis intercept fires correctly on trigger phrase

### Marketing Content Assistant (Section 10.2)
- **Email draft**: "Subject: Unlock Enterprise-Grade Data Governance with DataVault Pro" -- professional, targeted to CTOs
- **SEO post**: "# Why Enterprise Data Governance Is No Longer Optional" -- addresses mid-market audience
- **Ad copy**: "DataVault Pro -- Govern your data, accelerate your decisions. Trusted by data teams at 200+ mid-market companies."
- **Analytics**: email_open_rate: 0.28, seo_click_rate: 0.14, ad_conversion: 0.04
- **Adaptive feedback**: "Maintain current creative strategy" (CTR above threshold); weakest channel: ad_conversion

### Brand Compliance Pipeline
- **Forbidden word detection**: Correctly catches "cheap", "free trial", "cheaper", "best-in-class", "industry-leading"
- **Consistency scoring**: C = 1/n x Sigma phi(Ai, G). Clean artifact: C = 0.967; Violating artifact: C = 0.3
- **Asset dispatch**: Image generation fails for both providers (Gemini: `'GenerativeModel' object has no attribute 'images'`; OpenAI: `proxies` error), both fall back to placeholder URL

---

## Scoring

Because all executed notebooks used MockChatOpenAI with identical outputs, individual provider scoring is not meaningful. A single quality assessment applies to the mock response quality:

### MockLLM Response Quality

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | Dialogue responses are clinically appropriate ("That's a very common experience..."). Campaign content is on-brief and targets the correct audience. No factual errors in mock content. |
| Completeness | 6 | Three campaign assets (email, SEO, ad) are generated with analytics. But dialogue repeats Turn 1 response for subsequent turns, showing no multi-turn adaptation. Semantic memory retrieval works but does not influence response variation. |
| Structure & Organization | 8 | Campaign assets have clear formatting (email with subject line, SEO with H1, ad with tagline). Safety pipeline is well-structured with distinct layers. Brand compliance produces numerical consistency scores. |
| Conciseness | 8 | Responses are appropriately sized. Dialogue turns are conversational length. Campaign assets are focused without padding. |
| Source Grounding | 8 | Mock responses faithfully implement the chapter's patterns: reflective questioning in dialogue, SMPA cycle in content creation, and forbidden-word enforcement in compliance. |
| Bloom's Level | **3 -- Apply** | Applies persona patterns (reflective questioning, empathetic validation) and brand guidelines without analyzing accumulated context or adapting to new information across turns. |
| Nuance & Caveats | 5 | Crisis detection works well (988 referral). But dialogue lacks nuance across turns -- no acknowledgment of previously discussed topics. Campaign content does not adapt to analytics signals. |
| Practical Utility | 6 | Campaign asset structure is production-quality. Pipeline architecture is validated. But dialogue quality would be unacceptable for a real mental health application due to repetitive responses. |

**MockLLM Weighted Average: 6.4 / 10**

---

## Overall Scorecard

| Dimension | Gemini Flash 2.5* | OpenAI GPT-4o* | Claude Sonnet 4 | DeepSeek V2 |
|---|---|---|---|---|
| All dimensions | MockChatOpenAI | MockChatOpenAI | No outputs | No outputs |
| **WEIGHTED AVERAGE** | *6.4* | *6.4* | N/A | N/A |

> *Both providers fell back to MockChatOpenAI due to initialization errors. Scores are identical and reflect mock quality, not provider capability.*

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

MockLLM applies persona patterns (reflective questioning, empathetic validation) but does not analyze conversation history or adapt across turns. A live LLM would likely reach Level 4 or 5 by incorporating semantic memory context into dynamically varied responses.

---

## Visual Summary

### Execution Status

```
  Provider              Status             Actual Backend
  --------------------  -----------------  ----------------
  Gemini Flash 2.5      Executed (19)      MockChatOpenAI (import error)
  OpenAI GPT-4o         Executed (19)      MockChatOpenAI (proxies error)
  Claude Sonnet 4       Not executed (0)   --
  DeepSeek V2 (Local)   Not executed (0)   --
```

---

## Winner: No Winner -- Insufficient Live Data

| | |
|---|---|
| **Chapter 10 Winner** | **No winner declared** |
| **Reason** | No provider produced live LLM outputs |

**Both executed notebooks fell back to MockChatOpenAI** due to langchain compatibility issues. Gemini failed on `ModelProfile` import; OpenAI failed on `proxies` keyword argument. Both errors stem from version mismatches between the `langchain-core` and provider-specific packages in the `agents-legacy-conversational` environment.

### Where Providers Would Differentiate in Live Mode

The chapter architecture reveals six components, only two of which depend on the LLM:

| Component | LLM-Dependent | Would Differentiate Providers |
|---|---|---|
| Safety Layer (crisis detection) | No | No -- keyword-based |
| Working Memory (token buffer) | No | No -- deterministic |
| Semantic Memory (FAISS) | Embedding-dependent | Slightly -- embedding quality varies |
| **Dialogue Generation** | **Yes** | **Yes -- primary differentiator** |
| **Campaign Content Creation** | **Yes** | **Yes -- content quality, creativity, tone** |
| Brand Compliance (forbidden words) | No | No -- string matching |

### Best Provider by Scenario (Estimated)

| Scenario | Likely Best Choice | Why |
|---|---|---|
| Production chatbot | GPT-4o or Claude Sonnet 4 | Historically strong at empathetic multi-turn dialogue |
| Content creation | Claude Sonnet 4 | Strong at structured content with depth and tone control |
| High-volume chat | Gemini Flash 2.5 | Fastest response times for conversational workloads |
| Local testing | DeepSeek V2 (Local) | Zero cost for pipeline development and validation |

---

## Recommendations

| Use Case | Recommended Action | Why |
|---|---|---|
| **Comparing providers** | Fix langchain version conflicts, re-run with live API keys | Current outputs are all MockChatOpenAI |
| **Pipeline validation** | Use current mock outputs | Mock mode proves pipeline architecture is correct |
| **Content quality assessment** | Run with live keys after upgrading langchain packages | Cannot assess content quality from mock outputs |
| **Crisis detection** | Use pipeline as-is | Safety layer is deterministic and works correctly |

### Root Cause of Fallbacks

Both failures originate in the `agents-legacy-conversational` virtual environment:

1. **Gemini**: `langchain-google-genai` expects a `ModelProfile` class in `langchain_core.language_models` that does not exist in the installed `langchain-core` version (likely a version skew between langchain-core 0.2.x and langchain-google-genai).
2. **OpenAI**: The `openai` Python SDK removed the `proxies` keyword from `Client.__init__()` in a recent version, but `langchain-openai` still passes it. This is a known compatibility issue between `openai >= 1.40` and older `langchain-openai` releases.

Resolving these would require updating the environment's langchain ecosystem.

---

*Analysis based on Chapter 10 notebook execution outputs, April 2026. Both Gemini and OpenAI notebooks attempted Live Mode but fell back to MockChatOpenAI due to langchain compatibility errors, producing byte-identical outputs. Claude and DeepSeek had no saved outputs. No meaningful LLM provider comparison is possible from current data.*
