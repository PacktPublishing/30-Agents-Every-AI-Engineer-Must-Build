# LLM Provider Comparison — Full Book Summary

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document aggregates the LLM provider comparison results across all 17 chapters, covering 30 agent architectures tested with four providers: **Claude Sonnet 4**, **Gemini Flash 2.5**, **OpenAI GPT-4o**, and **DeepSeek V2 16B** (local via Ollama).

Each chapter's detailed analysis is in its own `LLM_COMPARISON.md`. This file provides the bird's-eye view.

---

## Grand Winner

```
  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │   OVERALL WINNER:  Claude Sonnet 4                          │
  │                                                             │
  │   Book-Wide Average:  8.46 / 10                             │
  │   Chapters Won:       17 / 17                               │
  │   Peak Score:         9.1  (Ch 8 — Data Analysis)           │
  │   Peak Bloom's:       Level 6 — Create (Ch 3 — Prompting)   │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘
```

---

## Book-Wide Averages

```
  Provider               Avg Score   Chapters    Visual
  ─────────────────────  ─────────   ────────    ──────────────────────────────
  🥇 Claude Sonnet 4        8.46      17/17      █████████████████████████░░░░░
  🥈 OpenAI GPT-4o          7.42      16/17      ██████████████████████░░░░░░░░
  🥉 Gemini Flash 2.5       7.17      16/17      █████████████████████░░░░░░░░░
     DeepSeek V2 (Local)    5.69      16/17      █████████████████░░░░░░░░░░░░░
```

---

## Chapter-by-Chapter Results

### Scores Heatmap

```
  Chapter                                Claude   Gemini  DeepSeek  OpenAI   Winner
  ────────────────────────────────────── ───────  ───────  ────────  ───────  ─────────────
  Ch 1  Foundations                        8.5      7.5      6.3      7.0    Claude (+1.0)
  Ch 2  Toolkit                            8.1      7.3      6.5      7.4    Claude (+0.7)
  Ch 3  Prompting                          8.7      7.5      5.9      8.1    Claude (+0.6)
  Ch 4  Deployment                         8.4      7.0      5.8      7.4    Claude (+1.0)
  Ch 5  Architectures                      8.4      6.6      6.6      7.4    Claude (+1.0)
  Ch 6  Knowledge Agents                   8.8      7.2      5.5       —     Claude (+1.6)
  Ch 7  Tool Orchestration                 8.1      7.0      5.9      6.6    Claude (+1.1)
  Ch 8  Data Analysis                      9.1       —        —       6.5    Claude (+2.6)
  Ch 9  Software Dev                       8.4      7.3      5.9      7.5    Claude (+0.9)
  Ch 10 Conversational                     8.4      7.3      5.9      7.8    Claude (+0.6)
  Ch 11 Multimodal                         8.4      7.5      4.6      7.6    Claude (+0.8)
  Ch 12 Ethical AI                         8.6      7.1      5.4      7.8    Claude (+0.8)
  Ch 13 Healthcare                         8.5      7.1      5.3      7.5    Claude (+1.0)
  Ch 14 Financial/Legal                    8.5      7.1      5.3      7.5    Claude (+1.0)
  Ch 15 Education                          8.3      7.1      5.6      7.5    Claude (+0.8)
  Ch 16 Embodied Agents                    8.3      7.0      5.1      7.5    Claude (+0.8)
  Ch 17 Future Agents                      8.3      7.1      5.4      7.6    Claude (+0.7)
  ────────────────────────────────────── ───────  ───────  ────────  ───────  ─────────────
  AVERAGE                                  8.46     7.17     5.69     7.42
```

> *"—" indicates the provider ran in Simulation Mode or had no saved outputs for that chapter.*

### Score Distribution

```
  Claude Sonnet 4     ▁▂▃▅▅▅▆▅▅▅▅▅▅▅▅▅▅  Range: 8.1 – 9.1  (σ = 0.24)
  OpenAI GPT-4o       ▂▃▅▃▃ ▁ ▃▄▃▄▃▃▃▃▃  Range: 6.5 – 8.1  (σ = 0.41)
  Gemini Flash 2.5    ▃▂▃▁▁▂▁ ▂▂▃▁▁▁▁▁▁  Range: 6.6 – 7.5  (σ = 0.24)
  DeepSeek V2 (Local) ▁▂ ▁▂▁▁ ▁▁ ▁▁▁▁▁ ▁  Range: 4.6 – 6.6  (σ = 0.50)
```

---

## Bloom's Taxonomy Analysis

### Cognitive Depth by Provider

```
  Level 6: Create      ┃ C
  Level 5: Evaluate    ┃ C · · · · · · · · · · · · · · · O
  Level 4: Analyze     ┃ C C · C C · C C C C C C C C C C C    O O · O O · O · O O O O O O O O O
  Level 3: Apply       ┃ G G G G G · G · G G G G G G G G G    D · D · D · D · D D · D · · D · D
  Level 2: Understand  ┃ D D D D D D D · D D D D D D D D D
  Level 1: Remember    ┃
                         1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7  ← Chapter number
```

### Average Bloom's Level

```
  Provider              Avg Level   Name            Visual
  ─────────────────────  ─────────  ──────────────  ─────────────────
  Claude Sonnet 4          4.9      Evaluate        ██████████████████████████████
  OpenAI GPT-4o            3.9      Analyze         ████████████████████████
  Gemini Flash 2.5         3.1      Apply           ███████████████████
  DeepSeek V2 (Local)      2.2      Understand      █████████████
```

### What Each Level Looks Like in Practice

| Level | Provider | Example from the Book |
|---|---|---|
| **L6 Create** | Claude (Ch 3) | Synthesized a novel launch strategy integrating market, financial, and marketing expert analyses into a coherent framework with original recommendations |
| **L5 Evaluate** | Claude (Ch 6) | Assessed RAG limitations, judged relative severity, and flagged that its own evidence base was incomplete |
| **L4 Analyze** | OpenAI (Ch 1) | Decomposed a billing complaint into structured categories: sentiment, entities, priority, and recommended actions |
| **L3 Apply** | Gemini (Ch 6) | Correctly mapped retrieved document content to answer a refund policy question with accurate details |
| **L2 Understand** | DeepSeek (Ch 6) | Paraphrased RAG limitations from source documents accurately but without categorization or evaluation |

---

## Provider Profiles

### Claude Sonnet 4 — "The Analyst"

```
  Accuracy     ██████████████████████████████  9.5
  Completeness ██████████████████████████████  9.3
  Structure    ██████████████████████████████  10.0
  Conciseness  ████████████████████████████    8.7
  Grounding    ██████████████████████████████  9.3
  Bloom's      ██████████████████████████████  5.0
  Nuance       ██████████████████████████████  9.0
  Utility      ██████████████████████████████  9.3
```

| Attribute | Detail |
|---|---|
| **Wins** | 17/17 chapters |
| **Signature move** | Hierarchical markdown structure with self-aware caveats |
| **Peak** | Ch 8 Data Analysis (9.1) — deepest analytical reasoning |
| **Bloom's peak** | Level 6 Create (Ch 3) — synthesized novel strategy from expert analyses |
| **Weakness** | Slightly verbose; requires `max_tokens` parameter |
| **Best for** | Analytical depth, compliance docs, research synthesis, structured decision support |

### OpenAI GPT-4o — "The Balanced Generalist"

```
  Accuracy     ████████████████████████████    8.5
  Completeness ██████████████████████████      8.0
  Structure    ██████████████████████████      8.0
  Conciseness  ████████████████████████████    8.5
  Grounding    ████████████████████████████    8.0
  Bloom's      ████████████████████████        4.0
  Nuance       ██████████████████████████      7.5
  Utility      ████████████████████████████    8.0
```

| Attribute | Detail |
|---|---|
| **Wins** | 0/17 (runner-up in 11 chapters) |
| **Signature move** | Balanced depth and conciseness with structured JSON outputs |
| **Peak** | Ch 3 Prompting (8.1) — strong strategic synthesis |
| **Bloom's peak** | Level 5 Evaluate (Ch 3) |
| **Weakness** | API key management; slightly less structured than Claude |
| **Best for** | General-purpose agents, balanced workloads, team familiarity |

### Gemini Flash 2.5 — "The Efficient Extractor"

```
  Accuracy     ██████████████████████████████  9.0
  Completeness ██████████████████████          7.0
  Structure    ████████████████████            6.5
  Conciseness  ██████████████████████████████  9.0
  Grounding    ████████████████████████████    8.5
  Bloom's      ██████████████████              3.0
  Nuance       ██████████████████              5.5
  Utility      ████████████████████████        7.0
```

| Attribute | Detail |
|---|---|
| **Wins** | 0/17 (runner-up in 5 chapters) |
| **Signature move** | Tight, accurate extractions with minimal padding |
| **Peak** | Ch 1, 3, 11 (7.5 each) |
| **Bloom's peak** | Level 4 Analyze (Ch 2, 12) |
| **Weakness** | Flat structure; depth on one aspect at cost of breadth |
| **Best for** | High-volume extraction, cost-sensitive production, speed-critical pipelines |

### DeepSeek V2 16B — "The Privacy Guardian"

```
  Accuracy     ████████████████████████        7.5
  Completeness ████████████████                5.0
  Structure    ████████████                    4.0
  Conciseness  ██████████████████████████████  9.0
  Grounding    ████████████████████            6.5
  Bloom's      ████████████                    2.0
  Nuance       ██████████                      3.0
  Utility      ████████████████                5.0
```

| Attribute | Detail |
|---|---|
| **Wins** | 0/17 (third place in most chapters) |
| **Signature move** | Runs entirely offline — zero cost, zero latency, full data privacy |
| **Peak** | Ch 2, 5 (6.5, 6.6) — deterministic tasks suit it best |
| **Bloom's peak** | Level 3 Apply (Ch 1, 5) |
| **Weakness** | Shallow responses; minimal structure; misses edge cases |
| **Best for** | Air-gapped environments, privacy-sensitive data, rapid prototyping, education |

---

## Head-to-Head Comparisons

### Claude vs. OpenAI GPT-4o

```
  Dimension         Claude  GPT-4o  Delta
  ────────────────  ──────  ──────  ──────
  Accuracy           9.5     8.5    +1.0  Claude
  Completeness       9.3     8.0    +1.3  Claude
  Structure         10.0     8.0    +2.0  Claude  ← biggest gap
  Conciseness        8.7     8.5    +0.2  ~tied
  Grounding          9.3     8.0    +1.3  Claude
  Bloom's            5.0     4.0    +1.0  Claude
  Nuance             9.0     7.5    +1.5  Claude
  Utility            9.3     8.0    +1.3  Claude
```

Claude leads in every dimension. The largest gap is **Structure (+2.0)** — Claude consistently uses hierarchical markdown while GPT-4o tends toward flatter lists. The narrowest gap is **Conciseness (+0.2)** — both are efficient with words.

### Claude vs. Gemini Flash 2.5

```
  Dimension         Claude  Gemini  Delta
  ────────────────  ──────  ──────  ──────
  Accuracy           9.5     9.0    +0.5  ~close
  Completeness       9.3     7.0    +2.3  Claude  ← biggest gap
  Structure         10.0     6.5    +3.5  Claude  ← biggest gap
  Conciseness        8.7     9.0    -0.3  Gemini  ← Gemini wins
  Grounding          9.3     8.5    +0.8  Claude
  Bloom's            5.0     3.0    +2.0  Claude
  Nuance             9.0     5.5    +3.5  Claude  ← biggest gap
  Utility            9.3     7.0    +2.3  Claude
```

Gemini's only advantage is **Conciseness (+0.3)** — it's slightly tighter. Claude dominates in **Nuance** and **Structure** (both +3.5), which reflects Gemini's tendency to extract accurately but shallowly.

### Cloud Providers vs. Local (DeepSeek V2)

```
  Dimension         Cloud Avg  Local   Gap
  ────────────────  ─────────  ──────  ──────
  Accuracy            9.0       7.5    -1.5
  Completeness        8.1       5.0    -3.1  ← biggest gap
  Structure           8.2       4.0    -4.2  ← biggest gap
  Conciseness         8.7       9.0    +0.3  Local wins
  Grounding           8.6       6.5    -2.1
  Bloom's             4.0       2.0    -2.0
  Nuance              7.3       3.0    -4.3  ← biggest gap
  Utility             8.1       5.0    -3.1
```

The local model trades quality for privacy and cost. The largest gaps are **Nuance (-4.3)** and **Structure (-4.2)** — DeepSeek rarely flags caveats or formats output hierarchically. Its one advantage: **Conciseness (+0.3)** — brevity by necessity.

---

## The 4-Provider Stack: When to Use What

```
  ┌──────────────────────────────────────────────────────────────────┐
  │                     DECISION MATRIX                              │
  │                                                                  │
  │  Need maximum quality?                                           │
  │  ├─ YES → Claude Sonnet 4                                       │
  │  │                                                               │
  │  Need to minimize cost?                                          │
  │  ├─ YES → Gemini Flash 2.5                                      │
  │  │                                                               │
  │  Data cannot leave your machine?                                 │
  │  ├─ YES → DeepSeek V2 (Local via Ollama)                        │
  │  │                                                               │
  │  Team already uses OpenAI?                                       │
  │  ├─ YES → OpenAI GPT-4o (strong generalist, familiar API)       │
  │  │                                                               │
  │  Need all four for comparison?                                   │
  │  └─ Every chapter has all 4 variants ready to run                │
  └──────────────────────────────────────────────────────────────────┘
```

### Recommended Stack by Domain

| Domain | Primary | Secondary | Why |
|---|---|---|---|
| **Research & Analysis** | Claude Sonnet 4 | Gemini Flash 2.5 | Claude for depth; Gemini for volume |
| **Production RAG** | Claude Sonnet 4 | OpenAI GPT-4o | Both strong at grounding; Claude more complete |
| **Document Processing** | Gemini Flash 2.5 | Claude Sonnet 4 | Gemini for throughput; Claude for complex schemas |
| **Compliance & Ethics** | Claude Sonnet 4 | OpenAI GPT-4o | Claude best at surfacing caveats and edge cases |
| **Education & Tutoring** | OpenAI GPT-4o | Claude Sonnet 4 | GPT-4o's balanced tone; Claude for advanced learners |
| **Healthcare / Legal** | Claude Sonnet 4 | — | Only Claude consistently flags uncertainty |
| **IoT / Embodied** | DeepSeek V2 (Local) | Gemini Flash 2.5 | Local for edge devices; Gemini for cloud fallback |
| **Rapid Prototyping** | DeepSeek V2 (Local) | Gemini Flash 2.5 | Zero cost iteration; Gemini when ready to scale |

---

## Methodology

### Scoring Framework

Each provider was rated 0–10 across eight dimensions per chapter:

| Dimension | What It Measures |
|---|---|
| Factual Accuracy | Correctness of claims against source documents |
| Completeness | Coverage of all relevant points from retrieved context |
| Structure & Organization | Use of headings, bullet points, logical flow |
| Conciseness | Information density without unnecessary padding |
| Source Grounding | Faithfulness to retrieved documents |
| Bloom's Taxonomy Level | Highest cognitive level demonstrated (1–6) |
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
- 68 notebooks executed across 17 chapters (4 providers x 17 chapters)
- Chapters where a provider ran in Simulation Mode are noted; simulation outputs are not scored
- Detailed per-chapter analysis available in each chapter's `LLM_COMPARISON.md`

### Per-Chapter Comparison Files

| Chapter | File | Winner | Score |
|---|---|---|---|
| [Ch 1 — Foundations](chapter01/LLM_COMPARISON.md) | `chapter01/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.5 |
| [Ch 2 — Toolkit](chapter02/LLM_COMPARISON.md) | `chapter02/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.1 |
| [Ch 3 — Prompting](chapter03/LLM_COMPARISON.md) | `chapter03/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.7 |
| [Ch 4 — Deployment](chapter04/LLM_COMPARISON.md) | `chapter04/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.4 |
| [Ch 5 — Architectures](chapter05/LLM_COMPARISON.md) | `chapter05/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.4 |
| [Ch 6 — Knowledge Agents](chapter06/LLM_COMPARISON.md) | `chapter06/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.8 |
| [Ch 7 — Tool Orchestration](chapter07/LLM_COMPARISON.md) | `chapter07/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.1 |
| [Ch 8 — Data Analysis](chapter08/LLM_COMPARISON.md) | `chapter08/LLM_COMPARISON.md` | Claude Sonnet 4 | 9.1 |
| [Ch 9 — Software Dev](chapter09/LLM_COMPARISON.md) | `chapter09/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.4 |
| [Ch 10 — Conversational](chapter10/LLM_COMPARISON.md) | `chapter10/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.4 |
| [Ch 11 — Multimodal](chapter11/LLM_COMPARISON.md) | `chapter11/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.4 |
| [Ch 12 — Ethical AI](chapter12/LLM_COMPARISON.md) | `chapter12/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.6 |
| [Ch 13 — Healthcare](chapter13/LLM_COMPARISON.md) | `chapter13/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.5 |
| [Ch 14 — Financial/Legal](chapter14/LLM_COMPARISON.md) | `chapter14/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.5 |
| [Ch 15 — Education](chapter15/LLM_COMPARISON.md) | `chapter15/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.3 |
| [Ch 16 — Embodied](chapter16/LLM_COMPARISON.md) | `chapter16/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.3 |
| [Ch 17 — Future](chapter17/LLM_COMPARISON.md) | `chapter17/LLM_COMPARISON.md` | Claude Sonnet 4 | 8.3 |

---

*Analysis based on 68 notebook executions across 17 chapters, April 2026. All notebooks, outputs, and scoring data are included in this repository for full reproducibility.*
