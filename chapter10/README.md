# Chapter 10: Conversational and Content Creation Agents

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 10** of *30 Agents Every AI Engineer Must Build*. It examines two agent architectures that operate at the boundary between algorithmic capability and human experience: the Empathetic Mental Health Support Agent (dual-memory hierarchy with SafetyLayer sentinel and PersonaEngine constraint layer) and the Marketing Content Assistant (multi-agent SMPA pipeline with specialist agents, CSP-based brand enforcement via EditorAgent, and adaptive feedback via AnalyticsEngine).

Every code cell runs **without an API key** in Simulation Mode, powered by a `MockChatOpenAI` and `MockOpenAIEmbeddings` layer that returns chapter-derived responses. When an OpenAI API key is provided, the notebook seamlessly switches to Live Mode.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter10

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Add your OpenAI API key for Live Mode
cp .env.template .env
# Edit .env and add your key, or skip this step for Simulation Mode

# 5. Launch the notebook
jupyter notebook Chapter_10_Conversational_and_Content_Creation_Agents.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **1** | Setup & Configuration | Imports, ColorLogger, API detection, LLM factory |
| **2.1** | §10.1 — Safety Layer | Crisis sentinel with deterministic bypass |
| **2.2** | §10.1 — Working Memory | `ContextManager` with `ConversationSummaryBufferMemory` |
| **2.3** | §10.1 — Semantic Memory | FAISS vector store for long-term recall |
| **2.4** | §10.1 — Persona Engine | `SystemMessage` persona as controlled bias |
| **2.5–2.6** | §10.1 — Case Study | Multi-turn dialogue with memory recall and crisis demo |
| **3.1** | §10.2 — SMPA Foundation | `Agent(ABC)` base class — Sense/Model/Plan/Act |
| **3.2–3.3** | §10.2 — Brand Constraints | CSP validation with `BrandGuidelines` dataclass |
| **3.4** | §10.2 — Editor Agent | Quality control layer with consistency scoring |
| **3.5** | §10.2 — Multimodal Orchestration | `AssetRequest` + `dispatch_asset_request()` |
| **3.6** | §10.2 — Adaptive Optimization | `AnalyticsEngine` with CTR-based feedback |
| **3.7–3.9** | §10.2 — Campaign Demo | End-to-end campaign walkthrough with DataVault Pro brief |
| **4** | Summary | Key takeaways and pointer to Chapter 11 |

## Real-World Use Case: MindBridge Health

What happens when a campus wellness platform scales from 3 universities to 8 and both the chatbot and content engine start breaking? The companion case study follows **MindBridge Health** — a healthtech startup serving 31,000 students — as they deploy the SafetyLayer crisis protocol, dual-memory conversation architecture, and CSP-validated content generation to restore student trust and eliminate brand compliance violations.

Read the full case study: **[USECASE.md](USECASE.md)** — includes the crisis detection accuracy improvement, content scaling metrics, and revenue protection analysis.

## Repository Structure

```
chapter10/
│
├── README.md                              # This file
├── AGENTS.md                              # Agentic AI metadata
├── LICENSE                                # MIT License
├── requirements.txt                       # Pinned Python dependencies
├── .env.template                          # API key template (zero-hardcode policy)
├── .gitignore                             # Standard Python + .env exclusions
├── TROUBLESHOOTING.md                     # Dependency conflict resolution guide
│
├── Chapter_10_Conversational_and_Content_Creation_Agents.ipynb   # Primary deliverable
│
└── mock_llm.py                            # MockChatOpenAI, MockOpenAIEmbeddings, MOCK_RESPONSES
```

## Simulation Mode

When no API key is detected, the notebook activates **Simulation Mode**:

- `MockChatOpenAI` replaces the OpenAI chat client transparently
- `MockOpenAIEmbeddings` provides deterministic 256-dimensional hash-based embeddings for reproducible FAISS behavior
- Context-aware mock responses cover both case studies
- Every cell executes successfully with no external dependencies

API key detection follows a three-tier cascade: `.env` file → environment variable → interactive prompt → Simulation Mode.

## Resilience Architecture

All agent operations are wrapped in the `@fail_gracefully` decorator:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

Key architectural patterns include Dual-Memory Hierarchy, Safety-First Pipeline, Persona as Constraint, CSP Brand Enforcement, and the SMPA Cycle.

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt`
- **API Key:** Optional (Simulation Mode works without one)

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to common dependency conflicts and runtime issues.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
