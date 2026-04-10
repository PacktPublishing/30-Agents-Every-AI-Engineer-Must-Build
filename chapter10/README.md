# Chapter 10: Conversational and Content Creation Agents

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 10** of *30 Agents Every AI Engineer Must Build*. It examines two agent architectures that operate at the boundary between algorithmic capability and human experience: the Empathetic Mental Health Support Agent (dual-memory hierarchy with SafetyLayer sentinel and PersonaEngine constraint layer) and the Marketing Content Assistant (multi-agent SMPA pipeline with specialist agents, CSP-based brand enforcement via EditorAgent, and adaptive feedback via AnalyticsEngine).

Every code cell runs **without an API key** in Simulation Mode, powered by a `MockLLM` and `MockEmbeddings` replace the LLM client transparently (works identically across all providers). When an API key is provided (OpenAI, Anthropic, or Google) or Ollama is running locally, the notebook seamlessly switches to Live Mode. Each provider has its own pre-executed notebook variant.

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

# Then add your provider's dependencies:
pip install -r requirements-openai.txt    # For OpenAI GPT-4o
pip install -r requirements-claude.txt    # For Anthropic Claude Sonnet 4
pip install -r requirements-gemini.txt    # For Google Gemini Flash 2.5
pip install -r requirements-ollama.txt    # For local Ollama (DeepSeek V2)

# 4. (Optional) Configure your LLM provider for Live Mode
cp .env.template .env
# Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY — or use Ollama locally

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
├── LOCAL_LLM_SETUP.md                     # Ollama setup guide (Win/Mac/Linux)
├── AGENTS.md                              # Agentic AI metadata
├── LICENSE                                # MIT License
├── requirements.txt                       # Base/shared dependencies
├── requirements-openai.txt                # + OpenAI provider deps
├── requirements-claude.txt                # + Anthropic Claude provider deps
├── requirements-gemini.txt                # + Google Gemini provider deps
├── requirements-ollama.txt                # + Local Ollama provider deps
├── .env.template                          # API key template (zero-hardcode policy)
├── .gitignore                             # Standard Python + .env exclusions
├── TROUBLESHOOTING.md                     # Dependency conflict resolution guide
│
├── Chapter_10_Conversational_and_Content_Creation_Agents.ipynb   # Primary deliverable
│
└── mock_llm.py                            # MockLLM, MockEmbeddings, MOCK_RESPONSES
```

## Simulation Mode

When no API key is detected, the notebook activates **Simulation Mode**:

- `MockLLM` replaces the LLM client transparently (works identically across all providers)
- `MockOpenAIEmbeddings` provides deterministic 256-dimensional hash-based embeddings for reproducible FAISS behavior
- Context-aware mock responses cover both case studies
- Every cell executes successfully with no external dependencies

API key detection follows a three-tier cascade: `.env` file → environment variable → interactive prompt → Simulation Mode.

## Pre-Executed Notebook Variants

Every notebook is pre-executed with outputs saved. Pick the variant that matches your setup:

| Notebook | Provider | Description |
|---|---|---|
| [ch10_conversational_and_content_creation_agents__RUN_NO_KEY_SIMULATION.ipynb](ch10_conversational_and_content_creation_agents__RUN_NO_KEY_SIMULATION.ipynb) | Simulation | No API key — MockLLM responses |
| [ch10_conversational_and_content_creation_agents__RUN_OPENAI_GPT4o.ipynb](ch10_conversational_and_content_creation_agents__RUN_OPENAI_GPT4o.ipynb) | OpenAI GPT-4o | Live LLM via `OPENAI_API_KEY` |
| [ch10_conversational_and_content_creation_agents__RUN_CLAUDE_Sonnet4.ipynb](ch10_conversational_and_content_creation_agents__RUN_CLAUDE_Sonnet4.ipynb) | Claude Sonnet 4 | Live LLM via `ANTHROPIC_API_KEY` |
| [ch10_conversational_and_content_creation_agents__RUN_GEMINI_Flash25.ipynb](ch10_conversational_and_content_creation_agents__RUN_GEMINI_Flash25.ipynb) | Gemini Flash 2.5 | Live LLM via `GOOGLE_API_KEY` |
| [ch10_conversational_and_content_creation_agents__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb](ch10_conversational_and_content_creation_agents__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb) | Local Ollama | DeepSeek V2 16B — no API key |

All variants produce equivalent output. Compare them to see how different providers handle the same agent tasks.

For local LLM setup instructions (Ollama + DeepSeek on Windows, macOS, and Linux), see **[LOCAL_LLM_SETUP.md](LOCAL_LLM_SETUP.md)**.

## Resilience Architecture

All agent operations are wrapped in the `@fail_gracefully` decorator:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

Key architectural patterns include Dual-Memory Hierarchy, Safety-First Pipeline, Persona as Constraint, CSP Brand Enforcement, and the SMPA Cycle.

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt` (base) and `requirements-<provider>.txt` for your LLM provider
- **API Key:** Optional — any of OpenAI, Anthropic, Google, or local Ollama. Simulation Mode works without any.

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions to common dependency conflicts and runtime issues.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
