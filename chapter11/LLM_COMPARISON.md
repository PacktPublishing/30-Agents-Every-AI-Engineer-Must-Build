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

## Key Observation: All Providers Ran in Simulation Mode with Identical Outputs

Chapter 11 uses **mock backends** for all multimodal processing (vision, audio, sensor fusion). The mock system activates because torch is not installed and no HUGGINGFACE_TOKEN is in the environment. All four provider notebooks produce byte-identical outputs (verified via MD5 hash comparison).

**Execution mode for all providers:**
```
Simulation Mode active. Reasons: torch not installed; No valid HUGGINGFACE_TOKEN in environment
All agents will use mock backends from mock_backends.py. No GPU or API token required.
```

**Hash verification:** All four notebooks (OpenAI, Claude, Gemini, DeepSeek) produce identical output with MD5 hash `d278b7a08b19ba6aa755975260bd38dc` and total character count of 10,675.

This means the LLM is not invoked at all -- the mock backends return pre-authored responses for vision queries, audio transcription, and sentiment analysis. Provider differentiation is zero.

---

## Provider Execution Status

| Provider | Output Cells | Mode | Outputs Identical |
|---|---|---|---|
| OpenAI GPT-4o | 30 | Simulation (mock backends) | Yes -- byte-identical |
| Claude Sonnet 4 | 30 | Simulation (mock backends) | Yes -- byte-identical |
| Gemini Flash 2.5 | 30 | Simulation (mock backends) | Yes -- byte-identical |
| DeepSeek V2 16B | 30 | Simulation (mock backends) | Yes -- byte-identical |

---

## Observed Outputs (Mock Backends -- Identical Across All Providers)

### Vision-Language Agent
- **Scene description**: "This is a cluttered workspace containing a laptop, papers, a coffee cup precariously balanced on a stack of documents, and a desk lamp." Chain-of-thought reasoning traces are included.
- **People counting**: "2 people are visible in the image" with systematic left-to-right scanning reasoning
- **Spatial relationships**: Describes laptop center, coffee cup right, desk lamp upper-left with distance estimates (15cm from laptop edge)
- **Error handling**: @graceful_fallback correctly catches NoneType image input after 2 retry attempts

### Audio Processing Agent
- **Clean mode**: Removes filler words. 4 segments with confidence 0.91-0.98. "Yes I've been waiting for three weeks now and nobody has called me back."
- **Verbatim mode**: Preserves filler words ("So um the Q3 results are in and uh we exceeded targets"). 3 segments with confidence 0.90-0.95.
- **Sentiment analysis**: Detects "angry" emotion with 0.975 confidence. Prosodic features: pitch 260Hz, rate 6.2 words/sec.

### Physical World Sensing Agent
- **Normal office**: 72F, CO2 650ppm -- 0 alerts, 0 commands (within deadband)
- **Server room overheat**: 96.5F -- CRITICAL alert, cooling at 100% intensity
- **After-hours intrusion**: Occupancy 0.9 at 23:00 -- unexpected occupancy alert, heating 40%
- **High CO2 lab**: 1350ppm -- ventilation command at 85% intensity

---

## Mock Response Quality Assessment

Since all providers produce identical outputs, a single quality assessment applies:

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | Mock descriptions are plausible and internally consistent. People count, spatial relationships, and sentiment analysis are reasonable for simulated data. |
| Completeness | 7 | All three modalities (vision, audio, sensor) are covered with multiple scenarios. Vision has 3 queries + error demo; audio has 2 transcription modes + sentiment; sensors have 4 scenarios. |
| Structure & Organization | 8 | Outputs are well-structured with clear CoT reasoning, segmented transcriptions with timestamps and confidence scores, and structured zone state reports. |
| Conciseness | 8 | Mock outputs are appropriately sized -- scene descriptions are focused, transcriptions are clean, sensor reports are tabular. |
| Source Grounding | 8 | Mock responses faithfully implement the chapter's multimodal agent patterns. |
| Bloom's Level | **3 -- Apply** | Mock responses apply multimodal processing patterns without analyzing or evaluating. Real LLMs would show differentiation in reasoning quality. |
| Nuance & Caveats | 6 | Confidence scores are included for transcription segments and sentiment. Zone monitoring has proper deadband logic. But uncertainty is simulated, not genuinely reasoned. |
| Practical Utility | 7 | Mock outputs demonstrate the pipeline architecture well. Sensor fusion scenarios are realistic and actionable. |

**Mock Response Weighted Average: 6.8 / 10**

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 |
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

Mock backends apply pre-authored multimodal processing patterns. In live mode, providers would differentiate significantly:
- **Vision**: Claude and GPT-4o have native vision; Gemini has strong multimodal integration; DeepSeek V2 is text-only
- **Audio**: Whisper-based transcription would be identical; sentiment analysis would vary
- **Sensors**: LLM synthesis of sensor data would show quality differences

---

## Visual Summary

### Execution Status

```
  Provider              Outputs  Mode                 Hash Match
  --------------------  -------  -------------------  ----------
  OpenAI GPT-4o            30   Mock backends         d278b7a0...
  Claude Sonnet 4          30   Mock backends         d278b7a0...
  Gemini Flash 2.5         30   Mock backends         d278b7a0...
  DeepSeek V2 (Local)      30   Mock backends         d278b7a0...
```

---

## Winner: No Winner -- All Outputs Identical

| | |
|---|---|
| **Chapter 11 Winner** | **No winner declared** |
| **Reason** | All four providers produce byte-identical mock outputs |

**All notebooks ran on mock backends (no torch, no HuggingFace token).** The multimodal mock system bypasses the LLM entirely, returning pre-authored responses for vision, audio, and sensor tasks.

### Expected Differentiation in Live Mode

If run with live multimodal backends, provider differences would emerge in:

1. **Vision-Language** (strongest differentiator):
   - GPT-4o and Claude have native vision APIs with direct image understanding
   - Gemini Flash has integrated multimodal processing
   - DeepSeek V2 16B is text-only and would need caption-based fallback

2. **Audio Processing** (moderate differentiator):
   - All providers would use Whisper for transcription (similar quality)
   - Sentiment analysis from prosodic features would vary by LLM reasoning quality

3. **Sensor Fusion** (weakest differentiator):
   - Threshold-based alerting is deterministic
   - LLM synthesis of multi-zone summaries would show minor quality differences

### Best Provider by Scenario (Estimated for Live Mode)

| Scenario | Likely Best Choice | Why |
|---|---|---|
| Vision-language tasks | GPT-4o or Gemini | Strong native vision capabilities |
| Audio transcription | Any provider | Whisper-based; provider-agnostic |
| Sensor fusion | Any cloud provider | Deterministic pipeline dominates |
| Local multimodal | DeepSeek + local models | Zero cloud dependency |

---

## Recommendations

| Use Case | Recommended Action | Why |
|---|---|---|
| **Comparing multimodal providers** | Re-run with torch + HF token | Current outputs bypass LLM entirely |
| **Pipeline validation** | Use current mock outputs | Mock mode proves architecture correctness |
| **Vision capabilities** | Test GPT-4o and Gemini first | Native multimodal APIs |
| **Production deployment** | Benchmark with actual images/audio | Mock data cannot predict real-world quality |

---

*Analysis based on Chapter 11 notebook execution outputs, April 2026. All four provider notebooks ran on mock backends (torch not installed, no HuggingFace token) producing byte-identical outputs. No LLM provider comparison is possible from current data. Provider differentiation would require live multimodal backends with actual image, audio, and sensor inputs.*
