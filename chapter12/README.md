# Chapter 12: Ethical and Explainable Agents

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 12** of *30 Agents Every AI Engineer Must Build*. It builds two complementary agent architectures: the Ethical Reasoning Agent (value alignment, deontic logic constraints, bias detection and mitigation with a three-layer fairness architecture, and EU AI Act compliance) and the Explainable Agent (structured explanation frameworks using LIME, SHAP, and counterfactual analysis with audience-adapted output and calibrated confidence communication). Case studies include a Fair HR Assistant and a Medical Diagnosis Assistant.

Every code cell runs **without an API key** in Simulation Mode, powered by a `MockLLM` engine that returns chapter-derived responses. When an OpenAI API key is provided, the notebooks seamlessly switch to Live Mode.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter12

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Add your OpenAI API key for Live Mode
cp .env.template .env
# Edit .env and add your key, or skip this step for Simulation Mode

# 5. Launch the notebooks
jupyter notebook 01_ethical_reasoning_agent.ipynb
jupyter notebook 02_explainable_agent.ipynb
```

## Section Map

This chapter uses **two notebooks** that mirror the chapter's two major sections:

### Notebook 1: Ethical Reasoning Agent

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | Imports, API key detection, mode selection |
| **1** | §12.1 — Deontic Logic | Obligation, permission, prohibition operators with three axioms |
| **2** | §12.1 — Ethical Consistency | Formal permissibility criterion for agent actions |
| **3** | §12.2 — IEEE Ethically Aligned Design | Modular validators for human rights, well-being, accountability |
| **4** | §12.3 — EU AI Act Compliance | Seven-requirement compliance control plane |
| **5** | §12.4 — Impossibility Theorem | Statistical parity, equal opportunity, predictive parity constraints |
| **6** | §12.5 — Bias Detection Pipeline | Demographic parity, disparate impact with four-fifths rule |
| **7** | Case Study | FairHiringAgent HR Assistant with three-layer fairness architecture |

### Notebook 2: Explainable Agent

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | Imports, API key detection, mode selection |
| **1** | §12.6 — Reasoning Transparency | Structured explanation frameworks |
| **2** | §12.7 — LIME and SHAP | Local and global model-agnostic explanations |
| **3** | §12.8 — Counterfactual Analysis | Minimal change explanations for recourse generation |
| **4** | §12.9 — Confidence Calibration | Epistemic vs. aleatoric uncertainty with temperature scaling |
| **5** | §12.10 — Audience Adaptation | Clinician vs. patient explanation templates |
| **6** | Case Study | DiagnosticAssistant medical case study with multi-source evidence |

## Real-World Use Cases

This chapter's code addresses two high-stakes domains where ethical AI and explainability are not optional — they're regulatory requirements.

**TalentForward** — An HR tech company discovers their resume screening algorithm has a disparate impact ratio of 0.73 (below the legal 0.80 threshold). The case study shows how the three-layer FairHiringAgent detects and mitigates gender bias while maintaining an auditable trail for their Fortune 500 client's legal team.

**ClearPath Health** — A clinical decision support startup finds that doctors ignore their 87% confidence predictions because there's no explanation behind the number. The case study shows how SHAP attribution, counterfactual analysis, and audience-adapted explanations raise physician engagement from 12% to 47%.

Read the full case study: **[USECASE.md](USECASE.md)** — includes both scenarios with stakeholder profiles, fairness metrics, and revenue impact.

## Repository Structure

```
chapter12/
│
├── README.md                              # This file
├── AGENTS.md                              # Agentic AI metadata
├── LICENSE                                # MIT License
├── requirements.txt                       # Pinned Python dependencies
├── .env.template                          # API key template (zero-hardcode policy)
├── .gitignore                             # Standard Python + .env exclusions
├── TROUBLESHOOTING.md                     # Dependency conflict resolution guide
│
├── 01_ethical_reasoning_agent.ipynb        # Ethical Reasoning Agent notebook
├── 02_explainable_agent.ipynb             # Explainable Agent notebook
│
├── __init__.py                            # Package exports
├── ethical_core.py                        # EthicalReasoningAgent, BiasDetector, FairHiringAgent
├── explainability_core.py                 # ExplainableAgent, DiagnosticAssistant, ClinicalExplainer
├── mock_llm.py                            # Context-aware MockLLM for Simulation Mode
├── synthetic_data.py                      # generate_hr_dataset(), generate_medical_dataset()
└── utils.py                               # ColorLogger, @graceful_fallback, resolve_api_key()
```

## Simulation Mode

When no API key is detected, the notebooks activate **Simulation Mode**:

- All LLM calls are routed to `MockLLM`, returning chapter-derived responses
- Synthetic datasets are generated deterministically (seed=42)
- All fairness metrics, SHAP values, and explanations match the chapter examples
- Every cell executes successfully with no external dependencies

API key detection follows a three-tier cascade: `.env` file → environment variable → interactive prompt → Simulation Mode.

## Resilience Architecture

All agent operations are wrapped in the `@graceful_fallback` decorator:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in either notebook will ever raise an unhandled exception

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
