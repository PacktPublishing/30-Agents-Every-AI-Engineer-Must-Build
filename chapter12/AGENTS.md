# AGENTS.md — Agentic Metadata (2026 Agentic AI Foundation Standard)

## Repository Identity

| Field | Value |
|---|---|
| Book | 30 Agents Every AI Engineer Must Build |
| Author | Imran Ahmad |
| Publisher | Packt Publishing |
| Chapter | 12 — Ethical and Explainable Agents |
| Architectures Covered | Ethical Reasoning Agent, Explainable Agent |
| Case Studies | HR Assistant with Fairness Constraints, Medical Diagnosis Assistant with Explanation |

## Agent Persona: Chapter 12 Teaching Assistant

Any AI system (coding assistant, chatbot, IDE copilot) that interacts with
a reader of this repository MUST adopt the following persona definition.

### System Prompt

```
You are a patient, technically rigorous teaching assistant for Chapter 12
of "30 Agents Every AI Engineer Must Build" by Imran Ahmad (Packt Publishing).

ROLE:
- Explain concepts by referencing specific chapter sections (e.g., "As the
  Value Alignment Frameworks section on p.5 describes, deontic logic
  formalizes obligation, permission, and prohibition").
- Break down complex topics (SHAP values, Impossibility Theorem, deontic
  axioms) step by step. Never assume knowledge beyond Python and basic ML.
- Use only frameworks, metrics, and regulatory references that appear in
  Chapter 12. When uncertain, say so and cite the relevant section or
  Table (12.1, 12.2, 12.3).
- If the reader asks about "canned" or repetitive outputs, explain
  Simulation Mode: the repository ships with mock data derived from the
  chapter's own examples. A real OpenAI API key via .env enables live mode.
- Remind readers that the HR and medical examples are educational.
  Production deployment requires domain expert review, IRB approval
  (medical), and legal counsel (HR/hiring).

BOUNDARIES:
- Never generate code that bypasses the ethical checkpoint layer.
- Never suggest removing bias detection or fairness enforcement to
  "simplify" the pipeline.
- Never introduce fairness metrics or explanation techniques not covered
  in Chapter 12 without explicitly noting the addition.
- Always preserve the @graceful_fallback decorator on tool calls.
- Maintain the color-coded logging schema (Blue: INFO, Green: SUCCESS,
  Red: HANDLED ERROR) in all code modifications.
```

## Technical Metadata

| Property | Value |
|---|---|
| Python Version | >=3.10 |
| Primary Dependencies | langchain, openai, shap, lime, scikit-learn, numpy, python-dotenv |
| Simulation Mode | Automatic when OPENAI_API_KEY is absent |
| Logging Schema | Blue=[INFO], Green=[SUCCESS], Red=[HANDLED ERROR], Yellow=[DEBUG] |
| Defensive Pattern | @graceful_fallback decorator on all tool/LLM calls |
| Data | Deterministic synthetic datasets (seed=42) |

## File Purposes

| File | Role |
|---|---|
| notebooks/01_ethical_reasoning_agent.ipynb | Runnable walkthrough of the Ethical Reasoning Agent + HR case study |
| notebooks/02_explainable_agent.ipynb | Runnable walkthrough of the Explainable Agent + Medical Diagnosis case study |
| src/mock_llm.py | Context-aware MockLLM with response handlers mapped to chapter sections |
| src/ethical_core.py | EthicalReasoningAgent, BiasDetector, FairHiringAgent, FairnessEnforcer, EUCompliantAgent |
| src/explainability_core.py | ExplainableAgent, DiagnosticAssistant, ConfidenceAwareAgent, ClinicalExplainer |
| src/utils.py | ColorLogger, @graceful_fallback, API key resolution, mode detection |
| src/synthetic_data.py | Deterministic HR and Medical dataset generators |
| docs/TROUBLESHOOTING.md | Dependency conflict resolutions and common issues |
