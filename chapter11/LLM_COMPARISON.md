# Chapter 11 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 11 Multimodal Agent tasks: vision-language processing, audio processing, and physical world sensing.

---

## Agent Tasks in This Chapter

- **Vision-Language Agent** -- Image understanding, visual question answering, scene description with chain-of-thought reasoning
- **Audio Processing Agent** -- Speech transcription (clean and verbatim modes), voice sentiment analysis
- **Physical World Sensing Agent** -- HVAC zone monitoring with temperature, CO2, and occupancy anomaly detection

## Scoring Dimensions

Each provider is rated 0-10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of visual descriptions, audio transcriptions, sensor interpretations |
| **Completeness** | Coverage of all visual elements, audio features, and sensor readings |
| **Structure & Organization** | Quality of multimodal output formatting and integration |
| **Conciseness** | Appropriate detail level for each modality |
| **Source Grounding** | Adherence to the chapter's multimodal processing patterns |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Handling of perception uncertainty, confidence levels |
| **Practical Utility** | How useful outputs would be for multimodal application development |

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

## Key Observation: All Four Providers Ran in Simulation Mode with Byte-Identical Outputs

Chapter 11 uses **mock backends** for all multimodal processing. The mock system activates because `torch` is not installed and no `HUGGINGFACE_TOKEN` is present in the environment. The LLM provider selection has zero effect on outputs.

**Mode banner (identical for all four providers):**
```
Simulation Mode active. Reasons: torch not installed; No valid HUGGINGFACE_TOKEN in environment
All agents will use mock backends from mock_backends.py. No GPU or API token required.
```

**Verification:** All four notebooks (Claude Sonnet 4, OpenAI GPT-4o, Gemini Flash 2.5, DeepSeek V2 16B) produce byte-identical outputs -- 10,676 characters of combined output text, with zero character differences across any provider pair.

The LLM is never invoked. Mock backends return pre-authored responses for vision queries, audio transcription, and sentiment analysis regardless of which provider notebook is run.

---

## Provider Execution Status

| Provider | Output Cells | Mode | Outputs Identical |
|---|---|---|---|
| Claude Sonnet 4 | 30 | Simulation (mock backends) | Yes -- byte-identical |
| OpenAI GPT-4o | 30 | Simulation (mock backends) | Yes -- byte-identical |
| Gemini Flash 2.5 | 30 | Simulation (mock backends) | Yes -- byte-identical |
| DeepSeek V2 16B | 30 | Simulation (mock backends) | Yes -- byte-identical |

---

## Observed Outputs (Mock Backends -- Identical Across All Providers)

### Vision-Language Agent (Section 11.1)
- **Test image**: Programmatic 640x480 RGB image with colored rectangles simulating workspace objects
- **Scene description**: "This is a cluttered workspace containing a laptop, papers, a coffee cup precariously balanced on a stack of documents, and a desk lamp." Includes chain-of-thought reasoning traces.
- **People counting**: "2 people are visible in the image" with systematic left-to-right scanning reasoning
- **Spatial relationships**: Describes laptop (center), coffee cup (right, 15cm from laptop edge), desk lamp (upper-left)
- **Error handling**: `@graceful_fallback` correctly catches NoneType image input after 2 retry attempts

### Audio Processing Agent (Section 11.2)
- **Clean mode**: Removes filler words. 4 segments with confidence 0.91-0.98. Output: "Yes I've been waiting for three weeks now and nobody has called me back."
- **Verbatim mode**: Preserves filler words ("So um the Q3 results are in and uh we exceeded targets"). 3 segments with confidence 0.90-0.95.
- **Sentiment analysis**: Detects "angry" emotion with 0.975 confidence. Prosodic features: pitch 260Hz, rate 6.2 words/sec.

### Physical World Sensing Agent (Section 11.3)
- **Normal office**: 72F, CO2 650ppm -- 0 alerts, 0 commands (within deadband)
- **Server room overheat**: 96.5F -- CRITICAL alert, cooling at 100% intensity
- **After-hours intrusion**: Occupancy 0.9 at 23:00 -- unexpected occupancy alert, heating 40%
- **High CO2 lab**: 1350ppm -- ventilation command at 85% intensity

---

## Scoring

Because all four providers produce byte-identical outputs from mock backends, individual provider scoring is meaningless. A single quality assessment applies:

### Mock Backend Response Quality

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | Mock descriptions are internally consistent. People count, spatial relationships, and sentiment scores are plausible for simulated data. Sensor thresholds produce correct alert levels. |
| Completeness | 7 | All three modalities (vision, audio, sensor) are covered with multiple scenarios. Vision has 3 queries + error handling demo. Audio has 2 transcription modes + sentiment. Sensors have 4 zone scenarios. |
| Structure & Organization | 8 | Clear chain-of-thought reasoning in vision outputs. Segmented transcriptions with per-segment timestamps and confidence scores. Structured zone state reports with alert severity levels. |
| Conciseness | 8 | Scene descriptions are focused. Transcriptions are clean. Sensor reports use tabular format without padding. No unnecessary verbosity in any modality. |
| Source Grounding | 8 | Mock responses implement the chapter's multimodal agent patterns faithfully: VisionQuestionAnsweringAgent with CoT, AudioProcessingAgent with clean/verbatim modes, and zone monitoring with deadband logic. |
| Bloom's Level | **3 -- Apply** | Mock responses apply multimodal processing patterns without analysis or evaluation. CoT traces are pre-authored, not genuinely reasoned. Real LLMs would show differentiation in reasoning depth. |
| Nuance & Caveats | 6 | Confidence scores are included for transcription segments (0.90-0.98) and sentiment (0.975). Zone monitoring uses proper deadband logic to avoid alert chatter. But uncertainty is simulated, not genuinely assessed. |
| Practical Utility | 7 | Mock outputs validate the pipeline architecture. Sensor fusion scenarios are realistic and actionable (CRITICAL cooling command, after-hours intrusion alert). Demonstrates the full multimodal agent pattern. |

**Mock Response Weighted Average: 6.8 / 10**

---

## Overall Scorecard

| Dimension | Claude Sonnet 4 | OpenAI GPT-4o | Gemini Flash 2.5 | DeepSeek V2 |
|---|---|---|---|---|
| All dimensions | Mock backends | Mock backends | Mock backends | Mock backends |
| **WEIGHTED AVERAGE** | 6.8 | 6.8 | 6.8 | 6.8 |

> *All four providers produce byte-identical outputs from mock backends. No LLM differentiation exists.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     |
Level 3: Apply       | ############ All providers (mock backends)
Level 2: Understand  |
Level 1: Remember    |
```

Mock backends apply pre-authored multimodal processing patterns. In live mode, providers would differentiate significantly in vision understanding and reasoning quality.

---

## Visual Summary

### Execution Status

```
  Provider              Outputs  Mode                 Identical
  --------------------  -------  -------------------  ---------
  Claude Sonnet 4          30   Mock backends         Yes
  OpenAI GPT-4o            30   Mock backends         Yes
  Gemini Flash 2.5         30   Mock backends         Yes
  DeepSeek V2 (Local)      30   Mock backends         Yes
```

---

## Winner: No Winner -- All Outputs Byte-Identical

| | |
|---|---|
| **Chapter 11 Winner** | **No winner declared** |
| **Reason** | All four providers produce byte-identical mock outputs |

**All notebooks ran on mock backends** because `torch` is not installed and no `HUGGINGFACE_TOKEN` is available. The multimodal mock system bypasses the LLM entirely, returning pre-authored responses for vision, audio, and sensor tasks. The LLM provider key is irrelevant for this chapter's execution.

### Why This Chapter Is Provider-Agnostic

Chapter 11 uses HuggingFace models (LLaVA for vision, Whisper for audio) rather than cloud LLM APIs. The provider-specific notebooks differ only in the `LLM_PROVIDER` environment variable, which controls the text LLM -- but Chapter 11's multimodal agents use dedicated multimodal models, not the text LLM. Even in live mode, the provider choice would only matter for any text-based reasoning layers, not for the core vision/audio processing.

### Expected Differentiation in Live Mode

If run with `torch` installed and a valid `HUGGINGFACE_TOKEN`:

| Component | Differentiation Level | Notes |
|---|---|---|
| Vision-Language (LLaVA) | None across providers | Uses HuggingFace model, not provider API |
| Audio Transcription (Whisper) | None across providers | Uses HuggingFace model, not provider API |
| Sentiment Analysis | None across providers | Uses HuggingFace model, not provider API |
| Sensor Fusion | None (deterministic) | Threshold-based alerting, no LLM involvement |

**Key insight:** Even with live backends, this chapter would show minimal provider differentiation because the multimodal models are HuggingFace-hosted, not provider-specific. Only if the architecture were redesigned to use GPT-4o Vision, Claude Vision, or Gemini multimodal APIs would provider differences emerge.

### If Redesigned for Cloud Multimodal APIs

| Scenario | Likely Best Choice | Why |
|---|---|---|
| Vision-language tasks | GPT-4o or Gemini Flash | Native multimodal APIs with strong image understanding |
| Audio transcription | Any provider | Whisper-based transcription is provider-agnostic |
| Combined vision + text reasoning | Claude Sonnet 4 | Strong at structured analysis of visual content |
| Local multimodal | DeepSeek + local models | Zero cloud dependency |

---

## Recommendations

| Use Case | Recommended Action | Why |
|---|---|---|
| **Comparing multimodal providers** | Install torch + obtain HF token, or redesign for cloud vision APIs | Current outputs bypass all models entirely |
| **Pipeline validation** | Use current mock outputs | Mock mode proves architecture correctness for all three modalities |
| **Production multimodal agents** | Benchmark with actual images and audio | Mock data cannot predict real-world model quality |
| **Vision capabilities comparison** | Use provider-native vision APIs (GPT-4V, Gemini, Claude) | HuggingFace LLaVA is provider-agnostic |

---

*Analysis based on Chapter 11 notebook execution outputs, April 2026. All four provider notebooks ran on mock backends (torch not installed, no HuggingFace token) producing byte-identical outputs with 10,676 total characters. No LLM provider comparison is possible from current data. The chapter uses HuggingFace multimodal models, making it inherently provider-agnostic even in live mode.*
