# Chapter 10: Conversational and Content Creation Agents

**Book:** *30 Agents Every AI Engineer Must Build*
**Author:** Imran Ahmad
**Publisher:** Packt Publishing, 2026
**Chapter Pages:** pp. 281–306
**License:** MIT

---

## Overview

This repository contains the complete companion code for **Chapter 10** of
*30 Agents Every AI Engineer Must Build*. The chapter examines two agent
architectures that operate at the boundary between algorithmic capability
and human experience:

1. **The Empathetic Mental Health Support Agent** (Section 10.1, pp. 282–293) — A
   safety-aware conversational agent with a dual-memory hierarchy (working
   memory via `ConversationSummaryBufferMemory` and semantic long-term
   recall via FAISS), a deterministic `SafetyLayer` sentinel, and a
   `PersonaEngine` that enforces empathetic, non-directive behavior as a
   constraint layer.

2. **The Marketing Content Assistant** (Section 10.2, pp. 293–305) — A multi-agent
   content creation pipeline built on the SMPA (Sense-Model-Plan-Act)
   paradigm. Specialist agents (Email, SEO, Ad Creative) produce
   brand-constrained drafts validated by an `EditorAgent` using a CSP
   (Constraint Satisfaction Problem) framework, with an `AnalyticsEngine`
   closing the adaptive feedback loop.

All code runs in two modes: **LIVE MODE** (with an OpenAI API key) or
**SIMULATION MODE** (using `mock_llm.py` with chapter-derived responses).

---

## Quickstart

**Step 1 — Clone and install:**

```bash
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd chapter10
pip install -r requirements.txt
```

**Step 2 — (Optional) Configure your API key:**

```bash
cp .env.template .env
# Edit .env and add your OpenAI API key
# Skip this step to run in SIMULATION MODE
```

**Step 3 — Launch the notebook:**

```bash
jupyter notebook Chapter_10_Conversational_and_Content_Creation_Agents.ipynb
```

Run all cells. The first cell prints a colored banner indicating your mode:
- **Green [SUCCESS]** — LIVE MODE with OpenAI API connectivity
- **Blue [INFO]** — SIMULATION MODE using pre-written mock responses

---

## Repository Structure

```
chapter10-conversational-content-agents/
│
├── README.md                   ← You are here
├── AGENTS.md                   ← 2026 Agentic AI Foundation metadata
├── LICENSE                     ← MIT License
├── requirements.txt            ← Pinned dependencies (Python 3.10+)
├── .env.template               ← API key placeholder
├── .gitignore                  ← Repository hygiene
├── TROUBLESHOOTING.md          ← 7 known issues with fixes
│
├── mock_llm.py                 ← Simulation layer (MockChatOpenAI,
│                                  MockOpenAIEmbeddings, MOCK_RESPONSES)
│
└── Chapter_10_Conversational_and_Content_Creation_Agents.ipynb
    ├── Cell Group 1: Setup & Configuration
    ├── Cell Group 2: The Conversational Agent (Section 10.1)
    ├── Cell Group 3: The Content Creation Agent (Section 10.2)
    └── Cell Group 4: Summary & Reflection
```

---

## Chapter Section Index

| Notebook Section | Chapter Reference | Book Pages | Key Concepts |
|:---|:---|:---|:---|
| Cell 1.1–1.4 | Technical requirements | pp. 281–282 | Imports, ColorLogger, API detection, LLM factory |
| Cell 2.1 | Implementing the vertical pipeline | p. 289 | `SafetyLayer` — crisis sentinel with deterministic bypass |
| Cell 2.2 | Memory hierarchy in practice — working memory | p. 290 | `ContextManager` with `ConversationSummaryBufferMemory` |
| Cell 2.3 | Memory hierarchy in practice — semantic memory | pp. 290–291 | `SemanticMemory` with FAISS vector store |
| Cell 2.4 | The persona engine as a constraint layer | p. 293 | `SystemMessage` persona — "controlled bias" |
| Cell 2.5 | Case study: Empathetic mental health support agent | pp. 287–292 | `MentalHealthAgent` — full vertical pipeline |
| Cell 2.6 | Full Section 10.1 integration | pp. 282–293 | Multi-turn dialogue with memory recall and crisis demo |
| Cell 3.1 | The SMPA foundation | p. 299 | `Agent(ABC)` base class — Sense/Model/Plan/Act |
| Cell 3.2 | Implementing brand constraints as a CSP | p. 300 | `BrandGuidelines` dataclass with `validate_content()` |
| Cell 3.3 | Brand consistency as a constraint satisfaction problem | pp. 294–296 | `validate_against_brand()` — Editor pre-check |
| Cell 3.4 | The editor agent: The quality control layer | p. 300 | `EditorAgent` — consistency score C = 1/n × Σ φ(Aᵢ, G) |
| Cell 3.5 | Multimodal orchestration via function calling | p. 301 | `AssetRequest` + `dispatch_asset_request()` |
| Cell 3.6 | The adaptive optimization cycle | pp. 298, 302 | `AnalyticsEngine` — CTR-based feedback, J(θ) formulation |
| Cell 3.7–3.8 | End-to-end campaign walkthrough | pp. 302–305 | `CampaignBrief`, `CampaignAssets`, `execute_campaign()` |
| Cell 3.9 | Full Section 10.2 integration | pp. 293–305 | Campaign demo with DataVault Pro brief |
| Cell 4.1–4.2 | Summary | pp. 305–306 | Key takeaways and pointer to Chapter 11 |

---

## Simulation Mode

This repository ships with **SIMULATION MODE** enabled by default. When no
`OPENAI_API_KEY` is detected, the notebook automatically imports
`MockChatOpenAI` and `MockOpenAIEmbeddings` from `mock_llm.py`.

**What Simulation Mode provides:**
- Context-aware mock responses for both case studies (Mental Health Agent
  and Marketing Content Assistant)
- Deterministic 256-dimensional hash-based embeddings for reproducible
  FAISS behavior
- Identical cell execution flow and output structure as LIVE MODE
- Zero external dependencies — no network access required

**Switching to LIVE MODE:**
1. Copy `.env.template` to `.env`
2. Add your OpenAI API key (requires access to `gpt-4o` and
   `text-embedding-3-small` models)
3. Restart the Jupyter kernel

---

## Key Architectural Patterns

- **Dual-Memory Hierarchy:** Working memory (recent turns, summarized
  progressively) + Semantic memory (FAISS vector store for long-term
  recall by similarity)
- **Safety-First Pipeline:** The `SafetyLayer` sentinel sits upstream of
  all generative logic — crisis detection bypasses the LLM entirely
- **Persona as Constraint:** The `PersonaEngine` reshapes the model's
  output distribution toward a stable behavioral region, not random tone
- **CSP Brand Enforcement:** Brand guidelines modeled as hard constraints
  with an `EditorAgent` feedback loop that retries until compliance
- **SMPA Cycle:** Sense-Model-Plan-Act decomposition prevents monolithic
  prompt drift in content generation
- **@fail_gracefully Decorator:** Every external call wrapped with
  exponential backoff and mock fallback — failures produce red-logged
  diagnostics, never stack traces

---

## Dependencies

| Package | Version | Purpose |
|:---|:---|:---|
| `langchain` | 0.2.16 | Agent framework, `ConversationSummaryBufferMemory` |
| `langchain-openai` | 0.1.23 | `ChatOpenAI`, `OpenAIEmbeddings` |
| `langchain-community` | 0.2.16 | FAISS vector store integration |
| `langchain-core` | 0.2.38 | `BaseMessage`, `SystemMessage`, `AIMessage` |
| `openai` | 1.40.0 | Image generation API (`dall-e-3`) |
| `faiss-cpu` | 1.8.0 | Local vector similarity search |
| `python-dotenv` | 1.0.1 | `.env` file loading |
| `numpy` | ≥1.24, <2.0 | Numerical operations (FAISS compatibility) |
| `tiktoken` | ≥0.7.0 | Token counting for LangChain |
| `ipykernel` | ≥6.29.0 | Jupyter notebook runtime |

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for known dependency issues
and platform-specific fixes.

---

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build*
(Packt Publishing, 2026).

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.
