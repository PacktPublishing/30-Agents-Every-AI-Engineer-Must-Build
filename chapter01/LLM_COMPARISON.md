# Chapter 1 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 1 Foundations of Agent Engineering tasks: cognitive loop implementation (perceive/reason/plan/act/learn), agent brain patterns, and multi-agent interaction paradigms.

---

## Agent Tasks in This Chapter

- **Cognitive Loop** -- Five-phase cycle (perceive, reason, plan, act, learn) applied to a customer billing scenario
- **Agent Brain Patterns** -- Reactive, deliberative, and hybrid architectures
- **Interaction Paradigms** -- Five levels from direct LLM calls to multi-agent A2A messaging
- **Resilience Testing** -- Graceful fallback under 100% failure conditions

## Scoring Dimensions

Each provider is rated 0-10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of JSON outputs and classification results |
| **Completeness** | Coverage of all cognitive loop phases and interaction levels |
| **Structure & Organization** | Quality of JSON formatting, field naming, hierarchical output |
| **Conciseness** | Information density without unnecessary padding |
| **Source Grounding** | Adherence to the chapter's prescribed architectures and patterns |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Acknowledgment of edge cases, confidence levels, reasoning factors |
| **Practical Utility** | How actionable the agent outputs would be in a real customer service system |

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

## Task 1: Cognitive Loop -- Perception Phase

The LLM receives "I need help with my billing" and must return structured perception data (sentiment, keywords, entities).

### OpenAI GPT-4o

**Actual output:**
```json
{
  "sentiment": "neutral",
  "intensity": "low",
  "keywords": ["help", "billing"],
  "emotion": null
}
```
Clean, minimal JSON. Four fields, correct sentiment. The `null` for emotion is honest but leaves downstream modules with less signal. No intent or topic classification at this stage.

### Claude Sonnet 4

**Actual output:**
```json
{
  "sentiment": {"polarity": "neutral", "confidence": 0.85, "emotional_tone": "help-seeking", "urgency": "moderate"},
  "intent": {"primary": "billing_assistance", "category": "customer_support", "specificity": "low"},
  "context": {"customer_state": "requesting_help", "topic": "billing", "complexity": "unknown", "escalation_potential": "low"},
  "keywords": ["help", "billing"],
  "metadata": {"priority": "standard"}
}
```
Deeply nested JSON with domain-specific classification. Includes confidence score (0.85), urgency assessment, and escalation potential. Significantly more fields than any other provider, which is both a strength (rich downstream data) and a weakness (over-engineering for a simple triage input).

### Gemini Flash 2.5

**Actual output:**
```json
{
  "entities": [],
  "sentiment": {"overall": "neutral", "details": "A direct request for assistance, no discernible positive or negative emotion expressed."},
  "keywords": ["help", "billing"],
  "speech_act": "request",
  "topic": "customer support"
}
```
Interesting inclusion of `speech_act` (pragmatic linguistics concept) and a natural-language sentiment explanation. The `entities: []` is accurate for this input. The `details` string is a useful touch -- it explains *why* the sentiment is neutral, which aids auditability.

### DeepSeek V2 16B (Local)

**Actual output:**
```json
{
  "sentiment": "neutral",
  "intensity": "moderate",
  "subject": "billing",
  "customer_need": "assistance"
}
```
Minimal but functional. Uses `customer_need` instead of the richer `intent` classification. Interestingly rates intensity as "moderate" (debatable for a polite help request). Produces valid JSON consistently.

---

## Task 2: Cognitive Loop -- Reasoning Phase (Intent Classification)

### OpenAI GPT-4o

**Actual output:**
```json
{"intent": "request_assistance", "priority": "medium"}
```
Two-field JSON. Generic intent label (`request_assistance`) rather than domain-specific (`billing_assistance`). Priority "medium" is reasonable for a routine billing inquiry.

### Claude Sonnet 4

**Actual output (truncated):**
```json
{
  "intent_classification": {"primary_intent": "billing_assistance", "intent_category": "customer_support", "confidence_level": "high", "specificity": "low"},
  "priority_assessment": {"priority_level": "standard", "urgency_score": 5, "escalation_risk": "low", "response_timeframe": "within_4_hours"},
  "reasoning": {"intent_factors": ["clear_billing_request", "help_seeking_behavior", "customer_support_context"], "priority_factors": [...]}
}
```
Deeply nested with explicit `intent_factors` and `priority_factors` arrays. The `response_timeframe: "within_4_hours"` and `urgency_score: 5` are operationally useful. Used domain-specific `billing_assistance` rather than generic label.

### Gemini Flash 2.5

**Actual output:**
```json
{"intent": "billing_assistance", "priority": "high"}
```
Two-field JSON like GPT-4o, but with the domain-specific `billing_assistance` label -- a better classification. However, it rated priority as "high" for a routine billing help request, which is a miscalibration that could cause false urgency in production triage.

### DeepSeek V2 16B (Local)

**Actual output:**
```json
{"intent": "request_assistance", "priority": "medium"}
```
Identical structure and labels to GPT-4o. Generic `request_assistance` intent. Functional but undifferentiated.

---

## Task 3: Cognitive Loop -- Action Phase (Customer Response)

### OpenAI GPT-4o

**Actual output:** A 6-step plan executed as customer-facing messages. Included formal salutation ("Hello [Customer's Name]"), acknowledgment, investigation steps, resolution communication, and a follow-up message. The tone was professional but template-like with placeholder brackets. Notably included a follow-up step for ongoing satisfaction tracking.

### Claude Sonnet 4

**Actual output:** A detailed execution log with plan ID `billing_assistance_standard_001`, checkmarks for each step, specific durations ("Step 1: 7 minutes"), concrete dollar amounts ("$45.99 charge", "$22.99 courtesy credit"), multi-factor authentication mention, and a customer satisfaction score (9/10). This reads like an actual CRM case log rather than a generic template.

### Gemini Flash 2.5

**Actual output:** Conversational response asking for specific information (bill date, disputed amount, nature of issue, supporting documentation) before proceeding. Then laid out a methodical investigation plan with bullet points. Practical and focused on information gathering before action -- a realistic customer service pattern.

### DeepSeek V2 16B (Local)

**Actual output:** Generated a formal email with subject line, salutation, reference number placeholder, and professional sign-off. Then described 8 follow-up steps. The format was appropriate but generic -- a standard acknowledgment template that would need substantial customization.

---

## Task 4: Cognitive Loop -- Learning Phase

### OpenAI GPT-4o

Produced a `feedback` object with `success_score_update: 0.9`. The learning output was compact but shallow -- lacked specific improvement recommendations.

### Claude Sonnet 4

Produced a detailed `learning_outcome` with `plan_id` reference, `success_score: 0.92`, arrays of `strengths`, `areas_for_improvement` (noting Step 3's 18-minute duration), `key_insights` (transparency + goodwill gestures), and concrete `model_updates` including timing targets ("step_3_target_duration: 12-15 minutes").

### Gemini Flash 2.5

Produced `success_score: 0.98` with `model_update_suggestions` containing six named improvement strategies (e.g., "prioritize_empathy_and_reassurance", "be_transparent_about_the_process"). Higher success score than Claude, but the suggestions were more generic coaching principles than data-driven improvements.

### DeepSeek V2 16B (Local)

Produced a well-structured learning output with `outcome` (boolean checklist of completed tasks), `feedback` with `success_score: 0.95`, `strengths` array, and two `areas_for_improvement`. Surprisingly strong output for the learning phase -- included actionable items like "Include a specific timeline for updates."

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|---|
| Factual Accuracy | **8.0** | **9.0** | **8.0** | **7.0** |
| Completeness | **8.0** | **9.0** | **8.0** | **7.0** |
| Structure & Organization | **7.0** | **9.0** | **8.0** | **7.0** |
| Conciseness | **8.0** | **6.0** | **8.0** | **8.0** |
| Source Grounding | **8.0** | **9.0** | **8.0** | **7.0** |
| Bloom's Taxonomy Level | **4.0 (Analyze)** | **5.0 (Evaluate)** | **4.0 (Analyze)** | **3.0 (Apply)** |
| Nuance & Caveats | **5.0** | **8.0** | **7.0** | **6.0** |
| Practical Utility | **8.0** | **8.0** | **8.0** | **7.0** |
| **WEIGHTED AVERAGE** | **7.0** | **7.9** | **7.4** | **6.5** |

**Scoring notes:**
- Claude's Conciseness is penalized to 6.0 because its perception output had 5 nested objects for a simple triage input -- this level of structure is over-engineered for the use case
- Gemini's Factual Accuracy takes a hit because it classified a routine billing request as "high" priority -- a material miscalibration
- GPT-4o's generic `request_assistance` intent label (vs. Claude and Gemini's `billing_assistance`) reduces its Factual Accuracy slightly
- DeepSeek's Learning phase output was surprisingly strong (6.0 Nuance), partially offsetting its weaker earlier phases

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    | Claude Sonnet 4
Level 4: Analyze     | OpenAI GPT-4o, Gemini Flash 2.5
Level 3: Apply       | DeepSeek V2 (Local)
Level 2: Understand  |
Level 1: Remember    |
```

**Claude Sonnet 4** reaches Level 5 (Evaluate) by explicitly assessing priority factors, generating improvement recommendations with specific timing targets in the learning phase, and producing self-critical analysis of step durations.

**OpenAI GPT-4o** operates at Level 4 (Analyze) -- decomposes the billing scenario into six clear phases with relationships between them, and includes a follow-up step showing customer journey awareness.

**Gemini Flash 2.5** also reaches Level 4 (Analyze) -- its perception phase includes a natural-language explanation of sentiment reasoning (`speech_act` classification), and the learning phase suggests multiple named improvement strategies.

**DeepSeek V2** stays at Level 3 (Apply) -- correctly applies the cognitive loop pattern but with generic labels and minimal self-reflection on output quality.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  1. Claude Sonnet 4        7.9  ########################------
  2. Gemini Flash 2.5       7.4  ######################--------
  3. OpenAI GPT-4o          7.0  #####################---------
     DeepSeek V2 (Local)    6.5  ###################-----------
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     | C
  L4 Analyze      | C G O
  L3 Apply        | C G D O
  L2 Understand   | C G D O
  L1 Remember     | C G D O
```

Legend: **C** = Claude Sonnet 4, **G** = Gemini Flash 2.5, **D** = DeepSeek V2, **O** = OpenAI GPT-4o

---

## Winner: Claude Sonnet 4

| | |
|---|---|
| **Chapter 1 Winner** | **Claude Sonnet 4** |
| **Score** | **7.9 / 10** |
| **Bloom's Level** | **Level 5 -- Evaluate** |

**Why Claude Sonnet 4 wins this chapter:**
- Highest weighted average (7.9) driven by strong scores in Completeness, Structure, Source Grounding, and Nuance
- Only provider to reach Bloom's Level 5 with explicit self-evaluation in the learning phase
- Produced the most operationally useful output (plan IDs, timing data, customer satisfaction scores)
- 0.5-point lead over runner-up Gemini Flash 2.5

**Key weakness:** Verbose perception output with deeply nested JSON is over-engineered for a simple triage input. A production system might prefer Gemini's cleaner structure for the perception phase.

**Runner-up:** Gemini Flash 2.5 (7.4/10) -- Best balance of conciseness and domain-specific classification. The `speech_act` analysis in perception was a unique and useful touch. Penalized for miscalibrating priority as "high."

**Third place:** OpenAI GPT-4o (7.0/10) -- Strongest natural-language customer responses with professional tone. The follow-up step in the action phase showed customer journey awareness. Weakened by generic intent labels.

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Production cognitive loop | Claude Sonnet 4 | Richest metadata for downstream processing and auditability |
| Customer-facing responses | OpenAI GPT-4o | Most natural conversational tone; best email/message templates |
| High-throughput triage | Gemini Flash 2.5 | Domain-specific intent labels with concise output |
| Air-gapped / private data | DeepSeek V2 (Local) | Only option with zero cloud dependency |
| Rapid prototyping | DeepSeek V2 (Local) | No API key required, instant iteration, zero cost |

## Provider Profiles for This Chapter

### Claude Sonnet 4 -- "The Over-Engineer"

**Strengths:**
- Deepest JSON structures with semantic field naming (plan_id, intent_factors, priority_factors)
- Only provider to include confidence scores, urgency assessments, and escalation potential
- Learning phase produced concrete timing targets and process improvement recommendations
- Best at producing machine-parseable output for downstream agent systems

**Weaknesses:**
- Most verbose output by a significant margin -- perception output alone had 5 nested objects
- Higher token consumption per cognitive loop iteration
- The depth may be unnecessary overhead for simple triage scenarios

---

### Gemini Flash 2.5 -- "The Pragmatic Analyst"

**Strengths:**
- Unique `speech_act` classification in perception shows linguistic sophistication
- Domain-specific `billing_assistance` intent (unlike GPT-4o and DeepSeek)
- Learning phase produced six named improvement strategies with clear labels
- Good information density without excessive nesting

**Weaknesses:**
- Miscalibrated priority to "high" for a routine billing inquiry -- a production-impacting error
- Less depth in reasoning justification than Claude

---

### OpenAI GPT-4o -- "The Professional Communicator"

**Strengths:**
- Most natural and polished customer-facing language in the action phase
- Six-step execution plan with follow-up demonstrates end-to-end customer journey thinking
- Clean, consistent formatting across all phases

**Weaknesses:**
- Generic `request_assistance` intent label misses domain-specific vocabulary
- Learning phase output was thin -- lacked specific improvement recommendations
- No confidence scoring or factor enumeration in reasoning phase

---

### DeepSeek V2 16B -- "The Reliable Minimalist"

**Strengths:**
- Runs entirely locally with zero cloud dependency
- Produces valid, parseable JSON consistently across all phases
- Surprisingly strong learning phase with actionable improvement suggestions
- Extremely concise -- lowest token overhead

**Weaknesses:**
- Generic labels throughout (same `request_assistance` as GPT-4o)
- Minimal structure limits downstream utility for complex orchestration
- Perception phase lacks the nuance of cloud providers

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Production cognitive loop** | Claude Sonnet 4 | Deepest reasoning structures; machine-parseable output with plan IDs |
| **Customer-facing agent** | OpenAI GPT-4o | Most natural conversational tone in execution phase |
| **High-throughput triage** | Gemini Flash 2.5 | Best speed/cost with domain-specific classification |
| **Offline development** | Ollama DeepSeek V2 | Zero cost, valid JSON, privacy-preserving |
| **Multi-agent orchestration** | Claude Sonnet 4 | Richest metadata for inter-agent message passing |

---

*Analysis based on Chapter 1 notebook outputs executed April 2026. All four providers ran in LIVE mode. Scores reflect actual output from the perceive/reason/plan/act/learn cognitive loop cells, with specific output text cited as evidence.*
