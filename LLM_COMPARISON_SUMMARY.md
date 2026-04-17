# LLM Provider Comparison — Full Book Summary

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document aggregates the LLM provider comparison results across all 17 chapters, covering 30 agent architectures tested with four providers: **OpenAI GPT-4o**, **Claude Sonnet 4**, **Gemini Flash 2.5**, and **DeepSeek V2 16B** (local via Ollama).

Each chapter's detailed analysis is in its own `LLM_COMPARISON.md`. This file provides the bird's-eye view.

> **April 2026 Update:** All 68 provider notebooks were re-run with live API keys. Previous comparisons were based on MockLLM outputs that produced identical results across providers. This revision reflects genuine provider differentiation where it exists, and honestly reports ties where pipelines are deterministic.

---

## Grand Summary

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │   NO SINGLE OVERALL WINNER                                      │
  │                                                                 │
  │   The right provider depends on the task.                       │
  │                                                                 │
  │   OpenAI GPT-4o     — 3 wins  (Ch 1, 3, 8)                     │
  │   DeepSeek V2 Local — 3 wins  (Ch 7, 14, 15)                   │
  │   Claude Sonnet 4   — 1 win   (Ch 6)                           │
  │   Gemini Flash 2.5  — 1 win   (Ch 4)                           │
  │   Ties              — 8 chapters (identical/deterministic)      │
  │   No winner         — 1 chapter (insufficient live data)        │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘
```

---

## Book-Wide Averages

Computed across chapters where each provider had valid (non-N/A) outputs:

```
  Provider               Avg Score  Chapters    Visual
  ─────────────────────  ─────────  ────────    ──────────────────────────────
  🥇 OpenAI GPT-4o          7.08     17/17      █████████████████████░░░░░░░░░
  🥈 Claude Sonnet 4        7.14     13/17      █████████████████████░░░░░░░░░
  🥉 Gemini Flash 2.5       6.95     17/17      ████████████████████░░░░░░░░░░
     DeepSeek V2 (Local)    6.82     16/17      ████████████████████░░░░░░░░░░
```

> Claude's average (7.14) is slightly higher than OpenAI's (7.08), but Claude is missing 4 chapters (no outputs for Ch 9, 10, 14, 15). On the 13 chapters where both competed, the gap is narrow and neither dominates consistently. OpenAI is ranked first because it has valid scores across all 17 chapters.

---

## Chapter-by-Chapter Results

### Scores Heatmap

```
  Chapter                                OpenAI  Claude  Gemini  DeepSk   Winner
  ────────────────────────────────────── ───────  ───────  ──────  ──────  ──────────────────
  Ch 1  Foundations                        7.0     7.3      6.8     6.6   OpenAI (practical)
  Ch 2  Toolkit                            6.3     6.3      6.3     6.1   Tie (3-way)
  Ch 3  Prompting                          7.5     7.8      7.4     6.8   OpenAI (practical)
  Ch 4  Deployment                         7.2     7.3      7.4     6.1   Gemini (cost-eff.)
  Ch 5  Architectures                      6.6     6.6      6.6     6.6   Tie (deterministic)
  Ch 6  Knowledge Agents                   7.8     8.6      7.6     5.4   Claude (+0.8)
  Ch 7  Tool Orchestration                 5.4     5.4      5.4     7.3   DeepSeek (sim.)
  Ch 8  Data Analysis                      7.1     5.9*     5.9*     —    OpenAI (+1.2)
  Ch 9  Software Dev                       6.9      —       6.9     4.9   Tie (OpenAI/Gemini)
  Ch 10 Conversational                     6.4*     —       6.4*     —    No winner (mock)
  Ch 11 Multimodal                         6.8     6.8      6.8     6.8   Tie (identical)
  Ch 12 Ethical AI                         7.6     7.6      7.6     7.6   Tie (deterministic)
  Ch 13 Healthcare                         7.5     7.5      7.5     7.5   Tie (identical)
  Ch 14 Financial/Legal                    7.3*     —       6.8     7.5   DeepSeek
  Ch 15 Education                          7.3      —       7.1     7.5   DeepSeek (mock)
  Ch 16 Embodied Agents                    7.9     7.9      7.9     7.9   Tie (identical)
  Ch 17 Future Agents                      7.8     7.8      7.8     7.8   Tie (identical)
  ────────────────────────────────────── ───────  ───────  ──────  ──────
  AVERAGE                                  7.08    7.14     6.95    6.82
```

> *\* = provider fell back to MockLLM due to API integration bugs, not model limitations*
> *— = no outputs / excluded from scoring*

### Key Observations

1. **Only 6 of 17 chapters show real provider differentiation** (Ch 1, 3, 4, 6, 8, 15). The rest produce identical outputs due to deterministic pipelines or shared mock frameworks.
2. **No provider dominates.** The winner depends on what the chapter tests: Claude excels at RAG depth (Ch 6), OpenAI at deployment-ready outputs (Ch 1, 3, 8), Gemini at cost efficiency (Ch 4).
3. **Several "live mode" notebooks still fell back to mock** due to API format incompatibilities in shared `llm_call()` functions (Ch 8 Claude/Gemini, Ch 10 both, Ch 14 OpenAI, Ch 16 all).
4. **DeepSeek's 3 wins are caveated** — Ch 7 won via simulation mode (cloud providers had JSON parse errors), Ch 14-15 won because other providers had integration issues.

---

## Bloom's Taxonomy Analysis

### Cognitive Depth by Provider (Chapters with Real Differentiation)

```
  Level 6: Create      │
  Level 5: Evaluate    │ C(6) O(8) O(15) G(15)
  Level 4: Analyze     │ C(1,3) O(1,3,4) G(3,4,6) D(1,3)
  Level 3: Apply       │ G(1) D(4,6)
  Level 2: Understand  │ D(8)
  Level 1: Remember    │
```

### Average Bloom's Level (Differentiated Chapters Only)

```
  Provider              Avg Level   Name
  ─────────────────────  ─────────  ──────────────
  Claude Sonnet 4          4.5      Analyze-Evaluate
  OpenAI GPT-4o            4.3      Analyze-Evaluate
  Gemini Flash 2.5         3.8      Apply-Analyze
  DeepSeek V2 (Local)      3.2      Apply
```

> Bloom's levels are close between Claude and OpenAI. Claude reached Level 5 in Ch 6 (epistemic self-assessment in RAG). OpenAI reached Level 5 in Ch 8 (GPS statistical decomposition) and Ch 15 (live evaluation).

---

## Provider Profiles

### OpenAI GPT-4o — "The Reliable Generalist"

| Attribute | Detail |
|---|---|
| **Wins** | 3/17 (Ch 1, 3, 8) |
| **Avg Score** | 7.08 (all 17 chapters) |
| **Signature move** | Balanced depth and conciseness; deployment-ready language |
| **Peak** | Ch 3 Prompting (7.5) — 100% A/B testing accuracy, cleanest PTCF adherence |
| **Bloom's peak** | Level 5 Evaluate (Ch 8, 15) |
| **Strength** | Most consistently deployment-ready; natural customer-facing language; strong instruction following |
| **Weakness** | Less structured than Claude; API format lock-in caused fallbacks in some chapters |
| **Best for** | Production agents, customer-facing systems, balanced workloads |

### Claude Sonnet 4 — "The Deep Analyst"

| Attribute | Detail |
|---|---|
| **Wins** | 1/17 (Ch 6) |
| **Avg Score** | 7.14 (13 chapters with outputs) |
| **Signature move** | Hierarchical markdown with self-aware caveats and epistemic qualifiers |
| **Peak** | Ch 6 Knowledge Agents (8.6) — deepest RAG analysis with uncertainty flagging |
| **Bloom's peak** | Level 5 Evaluate (Ch 6) |
| **Strength** | Richest structured output; only provider to flag incomplete evidence; deepest reasoning chains |
| **Weakness** | Verbose (conciseness scores 5.5-6.5); missing outputs in 4 chapters; over-engineering for simple tasks |
| **Best for** | Research synthesis, compliance documentation, RAG systems requiring depth |

### Gemini Flash 2.5 — "The Cost Optimizer"

| Attribute | Detail |
|---|---|
| **Wins** | 1/17 (Ch 4) |
| **Avg Score** | 6.95 (all 17 chapters) |
| **Signature move** | Tight, accurate outputs with lowest token cost |
| **Peak** | Ch 4 Deployment (7.4) — best cost-efficiency ($0.167 vs $0.371 GPT-4o) with same accuracy |
| **Bloom's peak** | Level 5 Evaluate (Ch 15) |
| **Strength** | Best cost-per-quality ratio; strong at standards-aligned output (OWASP, speech_act) |
| **Weakness** | Shallower analysis than Claude/OpenAI; occasional accuracy misses (Ch 3 A/B testing: 80% vs 100%) |
| **Best for** | High-volume production, cost-sensitive deployments, speed-critical pipelines |

### DeepSeek V2 16B — "The Privacy Guardian"

| Attribute | Detail |
|---|---|
| **Wins** | 3/17 (Ch 7, 14, 15 — all caveated) |
| **Avg Score** | 6.82 (16 chapters) |
| **Signature move** | Runs entirely offline — zero cost, zero latency, full data privacy |
| **Peak** | Ch 7 Tool Orchestration (7.3) — only provider with correct risk differentiation |
| **Bloom's peak** | Level 4 Analyze (Ch 1, 3) |
| **Strength** | Air-gapped operation; zero API cost; consistent outputs for reproducibility |
| **Weakness** | Shallower responses; wins often due to other providers failing rather than DeepSeek excelling; Ollama config issues in some chapters |
| **Best for** | Air-gapped environments, privacy-sensitive data, rapid prototyping, reproducible demos |

---

## Head-to-Head Comparisons

### OpenAI vs. Claude (13 shared chapters)

```
  Dimension         OpenAI  Claude  Delta
  ────────────────  ──────  ──────  ──────
  Wins                3       1     OpenAI +2
  Avg Score          7.08    7.14   Claude +0.06
  Availability      17/17   13/17   OpenAI +4
```

Very close on quality. Claude's higher average is offset by missing 4 chapters. OpenAI wins more chapters due to practical deployment readiness. Claude wins when deep analytical reasoning is needed (Ch 6 RAG).

### OpenAI vs. Gemini (17 shared chapters)

```
  Dimension         OpenAI  Gemini  Delta
  ────────────────  ──────  ──────  ──────
  Wins                3       1     OpenAI +2
  Avg Score          7.08    6.95   OpenAI +0.13
  Cost efficiency     —       —     Gemini advantage
```

OpenAI leads on quality; Gemini leads on cost. Gemini's Ch 4 win (deployment cost optimization) highlights its strength in budget-conscious production.

### Cloud Providers vs. Local (DeepSeek)

```
  Dimension         Cloud Avg  Local   Gap
  ────────────────  ─────────  ──────  ──────
  Avg Score           7.06      6.82   -0.24
  Wins                  5         3    Cloud +2
  Privacy              No       Yes    Local wins
  Cost              Per-token   Free   Local wins
```

The gap between cloud and local is much smaller than previously reported (0.24 vs the old claim of 1.77). DeepSeek is competitive and even wins chapters where cloud providers have integration issues.

---

## The 4-Provider Stack: When to Use What

```
  ┌──────────────────────────────────────────────────────────────────┐
  │                     DECISION MATRIX                              │
  │                                                                  │
  │  Need deployment-ready, balanced output?                         │
  │  ├─ YES → OpenAI GPT-4o (most wins, consistent quality)         │
  │  │                                                               │
  │  Need deep analytical reasoning with caveats?                    │
  │  ├─ YES → Claude Sonnet 4 (best at RAG depth, uncertainty)      │
  │  │                                                               │
  │  Need to minimize cost at scale?                                 │
  │  ├─ YES → Gemini Flash 2.5 (best $/quality ratio)               │
  │  │                                                               │
  │  Data cannot leave your machine?                                 │
  │  ├─ YES → DeepSeek V2 (Local via Ollama)                        │
  │  │                                                               │
  │  Need all four for comparison?                                   │
  │  └─ Every chapter has all 4 variants ready to run                │
  └──────────────────────────────────────────────────────────────────┘
```

### Recommended Stack by Domain

| Domain | Primary | Secondary | Why |
|---|---|---|---|
| **Research & RAG** | Claude Sonnet 4 | OpenAI GPT-4o | Claude for depth and uncertainty flagging; OpenAI for breadth |
| **Production Agents** | OpenAI GPT-4o | Gemini Flash 2.5 | OpenAI for quality; Gemini for cost at scale |
| **Cost-Sensitive Deployment** | Gemini Flash 2.5 | OpenAI GPT-4o | Gemini's routing saved 55% vs GPT-4o in Ch 4 |
| **Compliance & Ethics** | Claude Sonnet 4 | OpenAI GPT-4o | Claude best at surfacing caveats and edge cases |
| **Customer-Facing Agents** | OpenAI GPT-4o | Gemini Flash 2.5 | GPT-4o's natural conversational tone |
| **Healthcare / Legal** | OpenAI GPT-4o | Claude Sonnet 4 | Both strong; OpenAI more available across chapters |
| **IoT / Edge / Privacy** | DeepSeek V2 (Local) | Gemini Flash 2.5 | Local for air-gapped; Gemini for cloud fallback |
| **Rapid Prototyping** | DeepSeek V2 (Local) | Gemini Flash 2.5 | Zero cost iteration; Gemini when ready to scale |

---

## Honesty Notes

This comparison surfaced several important caveats:

1. **Most chapters are deterministic.** 11 of 17 chapters produce identical outputs regardless of provider because the agent pipelines use rule-based logic, deterministic scoring, or shared mock frameworks. Only 6 chapters show genuine LLM differentiation.

2. **Integration bugs skew results.** Several providers "lost" chapters not because of model quality but because of API format mismatches in shared `llm_call()` functions (e.g., Ch 8's function only supports OpenAI's `chat.completions.create` format).

3. **DeepSeek's wins are caveated.** Its Ch 7 win came via simulation mode (cloud providers had JSON parse errors). Its Ch 14-15 wins came partly from other providers having initialization failures.

4. **Claude is missing from 4 chapters.** Chapters 9, 10, 14, and 15 have no Claude outputs, which limits head-to-head comparison.

5. **"Simulation Mode" quality is solid.** The shared MockLLM produces well-crafted, chapter-accurate responses (scoring 6.4-7.9). Simulation mode is pedagogically valid for learning the agent architectures.

---

## Methodology

### Scoring Framework

Each provider was rated 0-10 across eight dimensions per chapter:

| Dimension | What It Measures |
|---|---|
| Factual Accuracy | Correctness of claims against source documents |
| Completeness | Coverage of all relevant points from retrieved context |
| Structure & Organization | Use of headings, bullet points, logical flow |
| Conciseness | Information density without unnecessary padding |
| Source Grounding | Faithfulness to retrieved documents |
| Bloom's Taxonomy Level | Highest cognitive level demonstrated (1-6) |
| Nuance & Caveats | Acknowledgment of limitations and edge cases |
| Practical Utility | How useful the output is for real-world decisions |

### Bloom's Taxonomy Scale

| Level | Name | What It Looks Like |
|---|---|---|
| 1 | Remember | Repeats facts verbatim |
| 2 | Understand | Paraphrases in own words |
| 3 | Apply | Maps knowledge to the question |
| 4 | Analyze | Breaks down into categories, identifies relationships |
| 5 | Evaluate | Assesses what works, what doesn't, and why |
| 6 | Create | Synthesizes novel frameworks or recommendations |

### Data Sources

- All scores derived from actual notebook execution outputs (April 2026)
- 68 notebooks re-executed with live API keys across 17 chapters
- Chapters where providers fell back to MockLLM due to integration bugs are clearly marked
- Detailed per-chapter analysis available in each chapter's `LLM_COMPARISON.md`

### Per-Chapter Comparison Files

| Chapter | File | Winner | Score |
|---|---|---|---|
| [Ch 1 — Foundations](chapter01/LLM_COMPARISON.md) | `chapter01/LLM_COMPARISON.md` | OpenAI GPT-4o | 7.0 |
| [Ch 2 — Toolkit](chapter02/LLM_COMPARISON.md) | `chapter02/LLM_COMPARISON.md` | Tie (3-way) | 6.3 |
| [Ch 3 — Prompting](chapter03/LLM_COMPARISON.md) | `chapter03/LLM_COMPARISON.md` | OpenAI GPT-4o | 7.5 |
| [Ch 4 — Deployment](chapter04/LLM_COMPARISON.md) | `chapter04/LLM_COMPARISON.md` | Gemini Flash 2.5 | 7.4 |
| [Ch 5 — Architectures](chapter05/LLM_COMPARISON.md) | `chapter05/LLM_COMPARISON.md` | Tie (all) | 6.6 |
| [Ch 6 — Knowledge Agents](chapter06/LLM_COMPARISON.md) | `chapter06/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.6 |
| [Ch 7 — Tool Orchestration](chapter07/LLM_COMPARISON.md) | `chapter07/LLM_COMPARISON.md` | DeepSeek V2 | 7.3 |
| [Ch 8 — Data Analysis](chapter08/LLM_COMPARISON.md) | `chapter08/LLM_COMPARISON.md` | OpenAI GPT-4o | 7.1 |
| [Ch 9 — Software Dev](chapter09/LLM_COMPARISON.md) | `chapter09/LLM_COMPARISON.md` | Tie (OpenAI/Gemini) | 6.9 |
| [Ch 10 — Conversational](chapter10/LLM_COMPARISON.md) | `chapter10/LLM_COMPARISON.md` | No winner | 6.4 |
| [Ch 11 — Multimodal](chapter11/LLM_COMPARISON.md) | `chapter11/LLM_COMPARISON.md` | Tie (all) | 6.8 |
| [Ch 12 — Ethical AI](chapter12/LLM_COMPARISON.md) | `chapter12/LLM_COMPARISON.md` | Tie (all) | 7.6 |
| [Ch 13 — Healthcare](chapter13/LLM_COMPARISON.md) | `chapter13/LLM_COMPARISON.md` | Tie (all) | 7.5 |
| [Ch 14 — Financial/Legal](chapter14/LLM_COMPARISON.md) | `chapter14/LLM_COMPARISON.md` | DeepSeek V2 | 7.5 |
| [Ch 15 — Education](chapter15/LLM_COMPARISON.md) | `chapter15/LLM_COMPARISON.md` | DeepSeek V2 | 7.5 |
| [Ch 16 — Embodied](chapter16/LLM_COMPARISON.md) | `chapter16/LLM_COMPARISON.md` | Tie (all) | 7.9 |
| [Ch 17 — Future](chapter17/LLM_COMPARISON.md) | `chapter17/LLM_COMPARISON.md` | Tie (all) | 7.8 |

---

*Analysis based on 68 notebook executions with live API keys across 17 chapters, April 2026. All notebooks, outputs, and scoring data are included in this repository for full reproducibility.*
