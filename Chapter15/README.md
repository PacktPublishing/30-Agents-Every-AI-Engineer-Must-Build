# Chapter 15: Education and Knowledge Agents

> From *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing)

## Overview

Two agent architectures demonstrating key patterns in adaptive learning and multi-agent collaboration:

1. **Education Intelligence Agent** — A POMDP-based personalized tutoring system that maintains a probabilistic model of student mastery and adapts instruction in real time. Implements Bayesian Knowledge Tracing (BKT), Item Response Theory (IRT 2PL) adaptive placement, Zone of Proximal Development (ZPD) curriculum planning, SM-2 spaced repetition scheduling, and two-stage LLM feedback generation.

2. **Collective Intelligence Agent** — A multi-agent consensus architecture where role-specialized agents (Pedagogy Specialist, Domain Expert, Assessment Specialist) propose, critique, and synthesize solutions through weighted voting, adversarial critic rotation, and emergent cross-pollination.

## Quickstart

```bash
git clone <repo-url> && cd chapter15
python -m venv ch15env && source ch15env/bin/activate
pip install -r requirements.txt
cp .env.template .env   # Optional: add your OpenAI key
jupyter notebook chapter15_education_and_knowledge_agents.ipynb
```

**No API key?** The notebook runs fully in **Simulation Mode** with pre-authored, educationally accurate mock responses. Every LLM call is wrapped in `@graceful_fallback` — even with an invalid key, the notebook never crashes.

## The Three Guarantees

1. **Runs without an API key** — Simulation Mode with educationally accurate mock responses
2. **Fails gracefully with a key** — `@graceful_fallback` catches all API errors, logs in Red, continues
3. **Self-documenting** — Every cell cites chapter pages, every error is color-coded, every decision is traceable

## Notebook Section Map

| Section | Pages | Key Concept |
|---|---|---|
| Part I, §1: Knowledge Graph | pp. 4–6 | DAG curriculum with prerequisite tracking |
| Part I, §2: Student Model | pp. 6–7 | Probabilistic mastery state per objective |
| Part I, §3: Curriculum Planner | pp. 8–9 | ZPD Gaussian expected-gain objective selection |
| Part I, §4: Placement Test | pp. 10–13 | IRT 2PL adaptive diagnostics with Fisher information |
| Part I, §5: BKT Update | pp. 13–16 | Bayesian mastery estimation (posterior + transition) |
| Part I, §6: Spaced Repetition | pp. 18–20 | SM-2 scheduling with ease factor adjustment |
| Part I, §7: Feedback Generator | pp. 22–24 | Two-stage misconception detection (rule-based → LLM) |
| Part I, §8: Case Study "Alex" | pp. 24–25 | End-to-end demo: Placement → BKT → Feedback → Review |
| Part II, §9: Collaborative Agent | pp. 27–29 | Propose/critique dual-pathway agent |
| Part II, §10: Consensus Engine | pp. 30–35 | Weighted multi-round consensus protocol |
| Part II, §11: Rubric Case Study | pp. 36–38 | Three-agent collaboration with adversarial critics |
| Part II, §12: Emergent Intelligence | pp. 38–39 | Cross-pollination, TRIZ constraint relaxation |

## Mathematical Foundations

| Formula | Location | Purpose |
|---|---|---|
| ZPD Gaussian Gain: `G(m,d) = α·exp(-(d-m-δ)²/(2σ²))` | p. 5 | Expected learning gain per candidate objective |
| 2PL IRT: `P(correct\|θ,a,b) = 1/(1+exp(-a(θ-b)))` | p. 10 | Adaptive placement probability model |
| BKT Posterior + Transition | pp. 14–15 | Mastery belief-state update after each observation |
| SM-2 Ease Factor: `ease = max(1.3, ease + 0.1 - (5-q)*(0.08+(5-q)*0.02))` | p. 19 | Spaced repetition interval scheduling |
| Consensus Score: `Score(p_j) = Σ_i [w_i · relevance_i · score_ij]` | p. 30 | Expertise-weighted proposal aggregation |

## Repository Structure

```
chapter15/
├── README.md                                           # This file
├── AGENTS.md                                           # Agentic metadata (2026 standard)
├── TROUBLESHOOTING.md                                  # Dependency & platform troubleshooting
├── requirements.txt                                    # Pinned dependencies
├── .env.template                                       # API key template (never contains real key)
├── .gitignore                                          # .env, __pycache__, .ipynb_checkpoints
├── LICENSE                                             # MIT License
├── chapter15_education_and_knowledge_agents.ipynb       # THE notebook (primary deliverable)
└── utils/
    ├── __init__.py                                     # Exports MockLLM, ColorLogger, graceful_fallback
    ├── mock_llm.py                                     # MockLLM + 9-key response registry
    └── resilience.py                                   # ColorLogger + @graceful_fallback decorator
```

## Color-Coded Logging

The notebook uses a visual logging system for execution tracing:

- 🔵 **Blue** `[INFO]` — Agent initialization, tool invocation, state transitions
- 🟢 **Green** `[SUCCESS]` — Completed steps, valid outputs, mastery threshold crossed
- 🔴 **Red** `[HANDLED ERROR]` — API failures, timeout, fallback activation
- 🟡 **Yellow** `[WARN]` — Degraded responses, low confidence, near-threshold values

## Technical Requirements

- **Python:** ≥3.10, <3.13
- **Core:** `openai==1.40.0`, `numpy==1.26.4`, `networkx==3.3`, `python-dotenv==1.0.1`
- **Runtime:** `jupyter>=1.0.0`, `ipykernel>=6.29.0`, `notebook>=7.0.0`
- **External API:** OpenAI `gpt-4o` access (optional — Simulation Mode requires zero external dependencies)

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed guidance on dependency conflicts, API key issues, platform-specific workarounds, and common "runs but looks wrong" scenarios.

## License

MIT License — see [LICENSE](LICENSE) for details.

## Author

**Imran Ahmad** — *30 Agents Every AI Engineer Must Build* (Packt Publishing)
