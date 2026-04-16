# Chapter 16 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of two LLM providers running the Chapter 16 Embodied Intelligence tasks: warehouse robot manipulation with safety constraints, domain-transforming city infrastructure integration, and an Ottawa drone mission case study with a Unified Constraint Envelope.

---

## Agent Tasks in This Chapter

- **Embodied Intelligence Agent** -- Three-layer control hierarchy (strategic reasoning, motion planning, low-level control) with safety-constrained execution
- **Domain-Transforming Integration Agent** -- Cross-domain city infrastructure (energy, transportation, emergency) with influence propagation
- **Ottawa Drone Case Study** -- Unified Constraint Envelope across 5 domains (weather, battery, airspace, parks, mission) with conservative constraint fusion

## Scoring Dimensions

Each provider is rated 0--10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of physical reasoning and safety constraints |
| **Completeness** | Coverage of all spatial dimensions, safety factors, and operational parameters |
| **Structure & Organization** | Quality of flight plans, safety reports, and operational commands |
| **Conciseness** | Appropriate detail for real-time operational communication |
| **Source Grounding** | Adherence to the chapter's embodied agent architectures |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Handling of environmental uncertainty, sensor noise, and safety margins |
| **Practical Utility** | How useful outputs would be for robotics or drone operations |

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

## Key Observation: Both Providers Use MockChatOpenAI with Identical Outputs

Despite different SIMULATION_MODE settings, both active providers use the same MockChatOpenAI backend:

- **OpenAI GPT-4o**: SIMULATION_MODE = True, "LLM initialized: MockChatOpenAI" -- 26 output cells
- **Gemini Flash 2.5**: SIMULATION_MODE = False (Google API key detected), but `get_llm()` still returned MockChatOpenAI -- 22 output cells
- **Claude Sonnet 4**: 0 output cells (notebook not executed)
- **DeepSeek V2 16B**: 0 output cells (notebook not executed)

**Evidence of identical outputs:**

1. **Warehouse robot task** -- Both providers produce identical tool-calling sequences:
   - [1] AIMessage -> tool_calls=['query_world_model']
   - [2] ToolMessage: {"package_A_pose": {"x": 2.3, "y": 1.1, "z": 0.8}...}
   - [3] AIMessage -> tool_calls=['check_safety_constraints']
   - [4] ToolMessage: {"is_safe": true, "reason": "All constraints satisfied"...}
   - [5] AIMessage -> tool_calls=['dispatch_motion_command']
   - [6] ToolMessage: {"success": true, "target": "shelf_B"...}
   - [7] AIMessage: "Mission complete. Package A has been picked from its current location and placed on shelf B. All safety constraints were..."

2. **Ottawa drone mission** -- Both produce identical output:
   "Mission authorized and first waypoint dispatched. Unified Constraint Envelope: ALL GREEN. Weather: -6.2C (limit -10C), wind 18.5 km/h (limit 25 km/h), no precipitation. Battery SoC: 82% (floor 30%)."

3. **Failure scenarios** -- Both correctly demonstrate:
   - Wind RED: wind_speed_kmh exceeds mission threshold
   - Battery RED: 22% SoC below 30% departure floor
   - Stale data RED: 12+ hour old weather data treated as RED by conservative fusion

The 4-cell difference in output count (26 vs 22) reflects cell splitting differences, not substantive output differences.

---

## Provider Availability

| Provider | Output Cells | Mode | Status |
|---|---|---|---|
| OpenAI GPT-4o | 26 | Simulation (MockChatOpenAI) | Identical outputs |
| Gemini Flash 2.5 | 22 | Simulation (MockChatOpenAI despite live key) | Identical outputs |
| Claude Sonnet 4 | 0 | Not executed | Excluded from scoring |
| DeepSeek V2 16B | 0 | Not executed | Excluded from scoring |

---

## Shared Simulation Output Quality

The simulation outputs demonstrate strong embodied agent architecture:

- **Tool-calling precision:** MockChatOpenAI correctly sequences query_world_model -> check_safety_constraints -> dispatch_motion_command (3-step plan matching the control hierarchy)
- **Safety enforcement:** Safety-Constrained Execution (Listing 16.3) validates each proposed action against A_safe(s) before execution, correctly reporting GREEN/RED
- **Conservative constraint fusion:** Single RED domain correctly vetoes the entire envelope across all failure scenarios
- **Cross-domain integration:** Influence propagation traced through Energy -> Transportation -> Emergency domains, identifying 2 critical, 14 high, 1 moderate impact entities
- **Unified Constraint Envelope:** All 5 domains (weather, battery, airspace, parks, mission) checked with specific thresholds from the book

### Unified Score (Both Active Providers)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Correct physical reasoning; accurate constraint thresholds (temp > -10C, wind < 25 km/h, battery >= 30%) |
| Completeness | 8 | Full embodied agent pipeline: warehouse robot, city infrastructure, drone mission, 3 failure scenarios |
| Structure & Organization | 8 | Clean tool-calling traces; color-coded constraint status (GREEN/RED); structured audit trail |
| Conciseness | 8 | Operational communication is appropriately terse; constraint fusion reports are clear |
| Source Grounding | 9 | Explicit page references throughout (pp. 458-490); Listing numbers (16.1-16.7) cited |
| Bloom's Level | **4 -- Analyze** | Agent decomposes tasks into tool-call sequences and analyzes constraint domains independently |
| Nuance & Caveats | 8 | Conservative fusion treats stale data as RED; escalation threshold logic prevents false confidence |
| Practical Utility | 7 | Good architecture demo; MockChatOpenAI tool-calling matches LangGraph react agent pattern |

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Gemini Flash 2.5 |
|---|---|---|
| Factual Accuracy | **8.0** | **8.0** |
| Completeness | **8.0** | **8.0** |
| Structure & Organization | **8.0** | **8.0** |
| Conciseness | **8.0** | **8.0** |
| Source Grounding | **9.0** | **9.0** |
| Bloom's Taxonomy Level | **4.0 (Analyze)** | **4.0 (Analyze)** |
| Nuance & Caveats | **8.0** | **8.0** |
| Practical Utility | **7.0** | **7.0** |
| **WEIGHTED AVERAGE** | **7.5** | **7.5** |

> *Both providers use MockChatOpenAI and produce identical outputs. Claude and DeepSeek excluded (0 output cells).*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    |
Level 4: Analyze     | oooooooooooo O, G (both identical simulation)
Level 3: Apply       |
Level 2: Understand  |
Level 1: Remember    |
```

The embodied agent pipeline reaches Level 4 (Analyze) through constraint domain decomposition: each domain (weather, battery, airspace, parks, mission) is analyzed independently, then fused via conservative conjunction. The tool-calling agent decomposes tasks into sequential tool invocations. It does not reach Level 5 because the agent does not evaluate trade-offs between mission objectives and safety constraints -- it follows a strict safety-first rule.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  OpenAI GPT-4o          7.5  ██████████████████████░░░░░░░░░
  Gemini Flash 2.5       7.5  ██████████████████████░░░░░░░░░
  Claude Sonnet 4        N/A  (no saved outputs)
  DeepSeek V2 (Local)    N/A  (no saved outputs)
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     |
  L4 Analyze      | O G (identical)
  L3 Apply        | O G
  L2 Understand   | O G
  L1 Remember     | O G
```

Legend: **O** = OpenAI GPT-4o, **G** = Gemini Flash 2.5

---

## Winner: Tie (OpenAI / Gemini)

| | |
|---|---|
| **Chapter 16 Winner** | **Tie -- Both Active Providers** |
| **Score** | **7.5 / 10** |
| **Bloom's Level** | **Level 4 -- Analyze** |

**Why this is a tie:**
- Both notebooks use MockChatOpenAI despite Gemini's live API key detection
- Tool-calling sequences are identical (query_world_model -> check_safety -> dispatch_motion)
- Constraint envelope outputs are byte-identical
- Failure scenario demonstrations produce the same RED/GREEN patterns

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality | Any (identical) | Simulation outputs are the same |
| Cost-efficient production | Gemini Flash 2.5 | Lowest per-token cost for equivalent output |
| Air-gapped / private data | DeepSeek V2 (Local) | Zero cloud dependency (no saved outputs for this chapter) |
| Rapid prototyping | Any mock mode | Zero cost, instant iteration |

## Provider Profiles for This Chapter

### OpenAI GPT-4o and Gemini Flash 2.5 -- "The Safety Pipeline"
**Strengths:** Correct tool-calling sequences; comprehensive constraint envelope with conservative fusion; proper failure scenario handling (wind, battery, stale data); cross-domain influence propagation.
**Weaknesses:** No live LLM differentiation; identical MockChatOpenAI outputs; mock tool-calling does not test actual LLM planning capability.

### Claude Sonnet 4 -- Not Evaluated
**Status:** 0 output cells saved. Notebook was not executed.

### DeepSeek V2 16B -- Not Evaluated
**Status:** 0 output cells saved. Notebook was not executed.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Safety evaluation** | Any -- then add live LLM | Constraint logic is deterministic; live LLM would add narrative quality |
| **Mission briefings** | Any -- then add live LLM | Pipeline architecture is identical |
| **Flight path planning** | Any (deterministic) | Waypoint computation is mathematical, not LLM-dependent |
| **Failure testing** | Any mock mode | Conservative fusion demonstrations are deterministic |
| **Pipeline development** | Any mock mode | Zero cost for testing embodied agent architecture |

> **Safety Note:** LLM outputs in this chapter are supplementary tool-calling orchestration only. All safety-critical decisions (constraint envelope, emergency halt, conservative fusion) are deterministic and do not depend on LLM output quality. In production, the LLM would plan high-level actions, but every action passes through the deterministic A_safe(s) safety check before execution.

---

*Analysis based on Chapter 16 notebook outputs executed April 2026. Both providers (OpenAI, Gemini) use MockChatOpenAI and produce identical simulation-mode outputs. Safety-critical logic is entirely deterministic. The tool-calling agent (create_react_agent) sequences are identical across providers.*
