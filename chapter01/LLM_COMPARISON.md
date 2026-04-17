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
Clean, minimal JSON with four fields. Correct sentiment classification. The `null` for emotion is honest but provides less signal for downstream modules. No intent or topic classification at this stage, which is appropriate -- the perception phase should observe, not interpret.

### Claude Sonnet 4

**Actual output:**
```json
{
  "sentiment": {"polarity": "neutral", "confidence": 0.85, "emotional_tone": "help-seeking", "urgency": "moderate"},
  "intent": {"primary": "billing_assistance", "category": "customer_support", "specificity": "low"},
  "context": {"customer_state": "requesting_help", "topic": "billing", "complexity": "unknown", "escalation_potential": "low"},
  "keywords": ["help", "billing"],
  "response_recommendation": {"tone": "helpful", "approach": "clarifying_questions", "priority": "standard"}
}
```
Five nested objects with domain-specific classification. Includes a confidence score (0.85), urgency assessment, and a `response_recommendation` block that pre-computes downstream decisions. This is both a strength (rich metadata for orchestration) and a weakness (the perception phase is doing work that belongs to reasoning and planning).

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
Notable inclusion of `speech_act` (a pragmatic linguistics concept) and a natural-language `details` field explaining *why* the sentiment is neutral. The `entities: []` is accurate for this input. The explanation aids auditability -- a human reviewer can verify the model's reasoning, not just its label.

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
Minimal but functional. Uses `customer_need` instead of richer intent classification. Rates intensity as "moderate" -- debatable for a polite help request, but not clearly wrong. Valid JSON produced consistently.

---

## Task 2: Cognitive Loop -- Reasoning Phase (Intent Classification)

### OpenAI GPT-4o

**Actual output:**
```json
{"intent": "request_assistance", "priority": "medium"}
```
Two-field JSON. Generic intent label (`request_assistance`) rather than domain-specific (`billing_assistance`). Priority "medium" is a reasonable default for a routine billing inquiry.

### Claude Sonnet 4

**Actual output (truncated):**
```json
{
  "intent_classification": {"primary_intent": "billing_assistance", "intent_category": "customer_support", "confidence_level": "high", "specificity": "low"},
  "priority_assessment": {"priority_level": "standard", "urgency_score": 5, "escalation_risk": "low", "response_timeframe": "within_4_hours"},
  "reasoning": {"intent_factors": ["clear_billing_request", "help_seeking_behavior", "customer_support_context"], "priority_factors": ["moderate_urgency_indicated", "neutral_sentiment_stable", "low_complexity_assumed", "standard_support_channel"], "risk_assessment": "minimal_escalation_potential"}
}
```
Deeply nested with explicit `intent_factors` and `priority_factors` arrays. The `response_timeframe: "within_4_hours"` and `urgency_score: 5` are operationally useful for SLA-driven systems. Uses domain-specific `billing_assistance` rather than a generic label.

### Gemini Flash 2.5

**Actual output:**
```json
{"intent": "billing_assistance", "priority": "high"}
```
Two-field JSON like GPT-4o, but with the domain-specific `billing_assistance` label -- a better classification. However, it rated priority as "high" for a routine billing help request, which is a miscalibration that could cause false urgency in production triage systems.

### DeepSeek V2 16B (Local)

**Actual output:**
```json
{"intent": "request_assistance", "priority": "medium"}
```
Identical structure and labels to GPT-4o. Generic `request_assistance` intent. Functional but undifferentiated.

---

## Task 3: Cognitive Loop -- Action Phase (Customer Response)

### OpenAI GPT-4o

Generated a 6-step plan with formal salutation ("Hello [Customer's Name]"), acknowledgment, investigation steps, resolution communication, and a follow-up message. Tone was professional and polished. Notably included a follow-up step for ongoing satisfaction tracking. Used placeholder brackets (`[Customer's Name]`, `[Your Name]`) indicating template-awareness -- the model understands this will be customized before sending.

### Claude Sonnet 4

Produced a detailed execution log with plan ID `billing_assistance_standard_001`, checkmarks for each of 7 steps, specific durations ("Step 1: 7 minutes", "Step 3: 18 minutes"), concrete dollar amounts ("$45.99 charge", "$22.99 courtesy credit"), multi-factor authentication mention, and a customer satisfaction score (9/10). Reads like an actual CRM case log rather than a generic template. Total execution time: 82 minutes across all steps.

### Gemini Flash 2.5

Took an information-gathering approach, asking for specific details (bill date, disputed amount, nature of issue, supporting documentation) before proceeding. Then laid out a methodical investigation plan with bullet points covering billing history review, charge comparison, root cause analysis, and follow-up. This is a realistic customer service pattern -- gathering facts before acting.

### DeepSeek V2 16B (Local)

Generated a formal email with subject line ("Acknowledgment of Your Billing Issue"), salutation, reference number placeholder, and professional sign-off. Then described 8 follow-up steps. Format was appropriate but generic -- a standard acknowledgment template that would need substantial customization for production use.

---

## Task 4: Cognitive Loop -- Learning Phase

### OpenAI GPT-4o

Produced a `feedback` object with `success_score_update: 0.9` and a paragraph of commentary noting the process was "comprehensive and customer-centric." Suggested improvement: "explicitly confirming the receipt of requested account information before proceeding with verification." Reasonable but thin -- one recommendation for a multi-step process.

### Claude Sonnet 4

Produced a detailed `learning_outcome` with `plan_id` reference, `success_score: 0.92`, arrays of `strengths` (6 items), `areas_for_improvement` (2 items noting Step 3's 18-minute duration), `key_insights` (transparency + goodwill gestures), and concrete `model_updates` including timing targets ("step_3_target_duration: 12-15 minutes", "overall_target_duration: 70-75 minutes"). Self-critical analysis of its own execution.

### Gemini Flash 2.5

Produced `success_score: 0.98` with extensive prose-style `feedback` covering strengths (empathy, transparency, process outline, comprehensive approach, professional tone, expectation management) and noting "negligible" areas for refinement. Higher success score than any other provider, but the self-assessment lacks the specificity of Claude's timing-based improvements. The 0.98 score feels generous given no system was actually tested.

### DeepSeek V2 16B (Local)

Produced a well-structured learning output with `outcome` (boolean checklist of completed tasks), `feedback` with `success_score: 0.95`, `strengths` array, and two `areas_for_improvement`: "Include a specific timeline for updates" and "Consider adding a direct contact method for urgent inquiries." Surprisingly actionable output for a 16B local model.

---

## Task 5: Agent Brain Patterns -- Hybrid Agent

The hybrid agent receives "Obstacle detected in aisle 5" and must demonstrate both reactive (immediate) and deliberative (strategic) layers.

### OpenAI GPT-4o

Reactive layer correctly produced `EMERGENCY_STOP` with 15ms latency. Deliberative layer returned a 4-waypoint reroute path with `status: "in_progress"`. Clean structure with proper layer coordination.

### Claude Sonnet 4

Reactive layer matched other providers. Deliberative layer produced a detailed 5-step `action_sequence` including `ACKNOWLEDGE_EMERGENCY`, `HALT_ALL_MOTORS`, `SENSOR_SCAN_360` (200ms, HIGH resolution), `OBSTACLE_CLASSIFICATION` (0.95 detection confidence), and `PATH_REPLANNING` with A* algorithm specification, 1.5m safety buffer, and 3 fallback options. Estimated resolution time: 800ms. Significantly more detailed than other providers.

### Gemini Flash 2.5

Both layers returned identical `EMERGENCY_STOP` responses -- the deliberative layer essentially duplicated the reactive output instead of producing a reroute plan. This is a material failure: the deliberative layer should plan a strategic response, not echo the reactive one.

### DeepSeek V2 16B (Local)

Reactive layer correct. Deliberative layer produced a `REROUTE` action with a 4-waypoint path, similar to GPT-4o. Clean differentiation between reactive and deliberative responses.

---

## Task 6: Interaction Levels -- Proxy Agent and Assistant System

### Proxy Agent (Natural Language to API Translation)

All four providers correctly translated "Find restaurants near me that are open now" into structured JSON with action/search type, location, and `open_now: true` filter. Minor field naming variations:
- **GPT-4o:** `"action": "search", "category": "restaurant"`
- **Claude:** `"action": "restaurant_search", "search_type": "proximity_based"`
- **Gemini:** `"search_type": "restaurant_search", "location": {"type": "current_location"}`
- **DeepSeek:** `"action": "search_restaurants"`

Claude added a `search_type: "proximity_based"` parameter. Gemini nested location as an object. All valid.

### Assistant System (Multi-Turn Conversation)

GPT-4o asked 6 follow-up questions (departure city, time, airline, round-trip, seating, passengers). Professional tone.

Claude added a disclaimer: "I cannot actually book flights or hotels directly" -- an honest limitation acknowledgment that other providers omitted. Also offered booking platform recommendations.

Gemini was the most concise: 3 questions (departure city, one-way vs round-trip, passengers), then smoothly transitioned to hotel details in turn 2.

DeepSeek asked 6 questions similar to GPT-4o's but in a slightly more structured format with bold headers.

---

## Task 7: Autonomous Agent -- Trip Planning

### OpenAI GPT-4o

Generated a 7-day Paris itinerary with visa requirements (Schengen), travel insurance details (provider name "TravelSafe Insurance", policy number), and 6 daily activity plans. Used dated language ("November 2023") -- a temporal grounding issue.

### Claude Sonnet 4

Produced a trip plan but included the disclaimer about not being able to book directly. Recommended booking platforms instead. Focused on providing guidance rather than simulating actual booking.

### Gemini Flash 2.5

Generated a 5-day themed itinerary ("Arrival & Seine Charm", "Iconic Landmarks & Art Immersion", "Impressionist Masterpieces & Latin Quarter") with detailed per-day activities, recommended timing ("pre-book tickets for summit access"), and practical advice. Most polished travel content.

### DeepSeek V2 16B (Local)

Produced a 5-day itinerary with visa requirements (including a step-by-step application process) and insurance recommendations (named providers: Allianz, AXA, World Nomads). Well-structured JSON. The visa process detail was more thorough than other providers.

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|---|
| Factual Accuracy | **7.5** | **8.0** | **7.0** | **7.0** |
| Completeness | **7.5** | **8.5** | **7.0** | **7.0** |
| Structure & Organization | **7.5** | **8.5** | **7.5** | **7.5** |
| Conciseness | **8.0** | **5.5** | **8.0** | **8.0** |
| Source Grounding | **7.5** | **8.0** | **7.0** | **7.0** |
| Bloom's Taxonomy Level | **4.0 (Analyze)** | **5.0 (Evaluate)** | **3.5 (Apply/Analyze)** | **3.5 (Apply/Analyze)** |
| Nuance & Caveats | **5.5** | **7.5** | **6.5** | **6.0** |
| Practical Utility | **8.0** | **7.5** | **7.5** | **7.0** |

| **Provider** | **WEIGHTED AVERAGE** |
|---|---|
| **Claude Sonnet 4** | **7.3** |
| **OpenAI GPT-4o** | **7.0** |
| **Gemini Flash 2.5** | **6.8** |
| **DeepSeek V2 (Local)** | **6.6** |

**Scoring notes:**
- Claude's Conciseness is penalized to 5.5 because its perception output had 5 nested objects for a simple triage input, and the action phase produced 82 minutes of simulated CRM detail for a single billing inquiry -- this over-engineering costs real tokens in production
- Gemini's Factual Accuracy is penalized because it rated a routine billing request as "high" priority (miscalibration) and its hybrid agent's deliberative layer duplicated the reactive response instead of producing a distinct strategic plan
- GPT-4o's Practical Utility is highest at 8.0 because its customer-facing language was the most natural and deployment-ready; its generic intent label (`request_assistance`) slightly reduces Factual Accuracy
- DeepSeek's learning phase was surprisingly strong with actionable timeline and contact method suggestions, partially offsetting weaker earlier phases
- Claude's disclaimer about not being able to book directly (assistant system) is scored positively for Nuance but negatively for Practical Utility in a simulation context

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    | Claude Sonnet 4
Level 4: Analyze     | OpenAI GPT-4o
Level 3: Apply       | Gemini Flash 2.5, DeepSeek V2 (Local)
Level 2: Understand  |
Level 1: Remember    |
```

**Claude Sonnet 4** reaches Level 5 (Evaluate) by explicitly assessing step durations against targets in the learning phase, producing self-critical analysis ("Step 3 duration exceeded optimal range"), and generating concrete timing improvements. However, its tendency to over-produce metadata means the evaluation is partly self-referential.

**OpenAI GPT-4o** operates at Level 4 (Analyze) -- decomposes the billing scenario into six clear phases with relationships between them, and includes a follow-up step showing customer journey awareness. Does not reach Level 5 because its learning phase lacks specific self-critique.

**Gemini Flash 2.5** operates at Level 3-4 -- its `speech_act` classification in perception shows analytical capability, but the hybrid agent failure (duplicating reactive output in deliberative layer) and the inflated 0.98 success score in learning weaken its analytical credibility.

**DeepSeek V2** operates at Level 3-4 -- correctly applies the cognitive loop pattern with consistent JSON and good learning-phase suggestions, but uses generic labels throughout and shows minimal self-reflection.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  1. Claude Sonnet 4        7.3  ######################--------
  2. OpenAI GPT-4o          7.0  #####################---------
  3. Gemini Flash 2.5       6.8  ####################----------
  4. DeepSeek V2 (Local)    6.6  ####################----------
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     | C
  L4 Analyze      | C O
  L3 Apply        | C G D O
  L2 Understand   | C G D O
  L1 Remember     | C G D O
```

Legend: **C** = Claude Sonnet 4, **G** = Gemini Flash 2.5, **D** = DeepSeek V2, **O** = OpenAI GPT-4o

---

## Winner: OpenAI GPT-4o (by practical margin)

| | |
|---|---|
| **Chapter 1 Winner** | **OpenAI GPT-4o** |
| **Score** | **7.0 / 10** |
| **Bloom's Level** | **Level 4 -- Analyze** |

**Why GPT-4o wins this chapter on balance:**
- While Claude scores 0.3 points higher on the weighted average, GPT-4o delivers the best cost-to-value ratio for the cognitive loop tasks that define Chapter 1
- Most natural and polished customer-facing language in the action phase -- the output requires minimal editing before deployment
- Correct priority calibration ("medium") where Gemini miscalibrated to "high"
- Clean, consistent JSON across all phases with predictable token consumption
- No over-engineering: every field in its output serves a clear purpose

**Why not Claude despite highest raw score:**
- Claude's 0.3-point lead is driven by Completeness and Structure scores that reflect *quantity* of output rather than *quality per token*
- Its perception output is 3-4x larger than necessary for simple triage, increasing latency and cost in production
- The detailed CRM simulation in the action phase (82 minutes, $22.99 credits, plan IDs) is impressive but fictional -- a real system would need actual database lookups, not simulated case numbers
- Its Conciseness penalty (5.5) is the most severe of any provider across any dimension

**Runner-up:** Claude Sonnet 4 (7.3/10) -- Highest raw score. Best for systems that need rich metadata for downstream processing. The learning phase with timing targets is genuinely useful for self-improving agent loops. Choose Claude when token cost is not a constraint and you need maximum auditability.

**Third place:** Gemini Flash 2.5 (6.8/10) -- The `speech_act` analysis was linguistically sophisticated and the information-gathering approach in the action phase was realistic. Penalized for hybrid agent failure (deliberative layer echoed reactive) and priority miscalibration.

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Customer-facing responses | OpenAI GPT-4o | Most natural conversational tone; deployment-ready templates |
| Self-improving agent loops | Claude Sonnet 4 | Timing targets and self-critical learning enable iterative optimization |
| High-throughput triage | Gemini Flash 2.5 | Domain-specific intent labels with concise output; fastest inference |
| Air-gapped / private data | DeepSeek V2 (Local) | Only option with zero cloud dependency |
| Rapid prototyping | DeepSeek V2 (Local) | No API key required, instant iteration, zero cost |

## Provider Profiles for This Chapter

### OpenAI GPT-4o -- "The Practical Professional"

**Strengths:**
- Most natural and polished customer-facing language across all action phase outputs
- Correct priority calibration and consistent JSON formatting
- 6-step action plan with follow-up shows end-to-end customer journey thinking
- Predictable output size makes token budgeting straightforward

**Weaknesses:**
- Generic `request_assistance` intent label misses domain-specific vocabulary
- Learning phase output was thin -- single improvement suggestion for a multi-step process
- No confidence scoring in reasoning phase

---

### Claude Sonnet 4 -- "The Over-Engineer"

**Strengths:**
- Deepest JSON structures with semantic field naming (plan_id, intent_factors, priority_factors)
- Only provider to include confidence scores, urgency assessments, and escalation potential in perception
- Learning phase produced concrete timing targets and process improvement recommendations
- Hybrid agent deliberative layer was the most detailed (A* pathfinding, 5-step sequence, fallback options)

**Weaknesses:**
- Most verbose output by a significant margin -- perception alone had 5 nested objects with a `response_recommendation` block
- Higher token consumption per cognitive loop iteration makes it expensive at scale
- Added booking disclaimers in the assistant system that, while honest, reduce utility in a simulation exercise

---

### Gemini Flash 2.5 -- "The Fast Analyst"

**Strengths:**
- Unique `speech_act` classification in perception shows linguistic sophistication
- Domain-specific `billing_assistance` intent (unlike GPT-4o and DeepSeek)
- Information-gathering approach in action phase reflects realistic customer service workflow
- Concise output with good information density

**Weaknesses:**
- Miscalibrated priority to "high" for a routine billing inquiry -- a production-impacting classification error
- Hybrid agent's deliberative layer duplicated reactive output instead of producing a reroute plan
- Learning phase gave itself 0.98 success score with generic improvement suggestions

---

### DeepSeek V2 16B -- "The Reliable Minimalist"

**Strengths:**
- Runs entirely locally with zero cloud dependency
- Produces valid, parseable JSON consistently across all phases
- Surprisingly strong learning phase with actionable improvement suggestions (timeline and contact method)
- Visa application process detail in trip planning was more thorough than cloud providers

**Weaknesses:**
- Generic labels throughout (same `request_assistance` as GPT-4o)
- Minimal structure limits downstream utility for complex orchestration
- Perception phase lacks the nuance of cloud providers

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Production cognitive loop** | OpenAI GPT-4o | Best cost-to-quality ratio; natural language output ready for customers |
| **Metadata-rich orchestration** | Claude Sonnet 4 | Deepest reasoning structures; machine-parseable output with plan IDs |
| **High-throughput triage** | Gemini Flash 2.5 | Best speed/cost with domain-specific classification |
| **Offline development** | Ollama DeepSeek V2 | Zero cost, valid JSON, privacy-preserving |
| **Self-improving agents** | Claude Sonnet 4 | Learning phase with timing targets enables iterative optimization |

---

*Analysis based on Chapter 1 notebook outputs executed April 2026. All four providers ran in LIVE mode with real API keys. Scores reflect actual output from the perceive/reason/plan/act/learn cognitive loop cells, hybrid agent demonstrations, and interaction level tasks, with specific output text cited as evidence.*
