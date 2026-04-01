# Chapter 15: Education and Knowledge Agents

> From *30 Agents Every AI Engineer Must Build* by **Imran Ahmad** (Packt Publishing, 2026)

Two agent architectures that apply the cognitive loop to teaching and collective reasoning:

1. **Education Intelligence Agent** — A POMDP-based adaptive tutor that maintains probabilistic mastery estimates, plans curricula via zone-of-proximal-development heuristics, traces knowledge with Bayesian updates, schedules spaced repetition, and generates targeted feedback through a two-stage misconception detector.

2. **Collective Intelligence Agent** — A multi-agent collaboration pattern where role-specialized agents propose, critique, and synthesize solutions through weighted consensus with adversarial critic rotation and cross-pollination for emergent insight.

---

## Quickstart

```bash
git clone <repo-url> && cd chapter15
python -m venv ch15env && source ch15env/bin/activate
pip install -r requirements.txt
cp .env.template .env   # Optional: add your OpenAI API key
jupyter notebook chapter15_education_and_knowledge_agents.ipynb
```

**No API key?** The notebook runs fully in **Simulation Mode** with pre-authored mock responses that are educationally accurate and mapped to specific chapter sections. No external dependency is required.

---

## Repository Structure

```
chapter15/
├── chapter15_education_and_knowledge_agents.ipynb   # Primary notebook (all domain logic inline)
├── utils/
│   ├── __init__.py              # Package exports
│   ├── mock_llm.py              # MockLLM + 9-key section-mapped response registry
│   └── resilience.py            # ColorLogger + @graceful_fallback decorator
├── requirements.txt             # Pinned dependencies (Ch.15, p. 2)
├── .env.template                # API key placeholder (3-tier resolution)
├── .gitignore                   # Repository hygiene
├── README.md                    # This file
├── AGENTS.md                    # Agentic metadata (2026 standard)
├── TROUBLESHOOTING.md           # Dependency, platform, and runtime guide
└── LICENSE                      # MIT License
```

---

## Notebook Section Map

| Section | Cell Group | Chapter Pages | Key Concept |
|---|---|---|---|
| **Setup** | Cells 1–3 | p. 2 | Imports, API key detection, Simulation Mode switch |
| **Dataclasses** | Cells 4–5 | pp. 6–7 | Supporting type definitions (12 dataclasses) |
| **Part I, §1: Knowledge Graph** | Cells 6–8 | pp. 4–6 | DAG curriculum with 10 Python learning objectives |
| **Part I, §2: Student Model** | Cells 9–11 | pp. 6–7 | Per-student probabilistic mastery state |
| **Part I, §3: Curriculum Planner** | Cells 12–15 | pp. 8–9 | ZPD-aligned Gaussian expected-gain objective selection |
| **Part I, §4: Placement Test** | Cells 16–20 | pp. 10–13 | IRT 2PL adaptive diagnostics with Fisher information |
| **Part I, §5: BKT Update** | Cells 21–24 | pp. 13–16 | Bayesian Knowledge Tracing (posterior + transition) |
| **Part I, §6: Spaced Repetition** | Cells 25–28 | pp. 18–20 | SM-2 algorithm with overdue priority scoring |
| **Part I, §7: Feedback Generator** | Cells 29–32 | pp. 22–24 | Two-stage misconception detection + pedagogical nudge |
| **Part I, §8: Case Study "Alex"** | Cells 33–35 | pp. 24–25 | End-to-end demo: Placement → BKT → Feedback → Review |
| **Part II, §9: Collaborative Agent** | Cells 36–39 | pp. 27–29 | Propose/critique dual pathway with confidence metadata |
| **Part II, §10: Consensus Engine** | Cells 40–45 | pp. 30–35 | Weighted multi-round consensus with adversarial rotation |
| **Part II, §11: Rubric Case Study** | Cells 46–52 | pp. 36–39 | Three-agent rubric design + emergent intelligence |
| **Summary** | Final cell | p. 40 | Key takeaways and further reading |

---

## Mathematical Foundations

The notebook implements five core mathematical models from the chapter:

| Formula | Location | Purpose |
|---|---|---|
| `G(m,d) = α·exp(-(d-m-δ)²/(2σ²))` | p. 5 | ZPD Gaussian expected learning gain |
| `P(correct\|θ,a,b) = 1/(1+exp(-a(θ-b)))` | p. 10 | 2PL Item Response Theory probability |
| BKT posterior + learning transition | pp. 14–15 | Bayesian mastery belief-state update |
| `ease = max(1.3, ease + 0.1 - (5-q)*(0.08+(5-q)*0.02))` | p. 19 | SM-2 spaced repetition scheduling |
| `Score(p_j) = Σ_i [w_i · relevance_i · score_ij]` | p. 30 | Expertise-weighted consensus aggregation |

---

## Simulation Mode vs. Live Mode

| Feature | Simulation Mode | Live Mode |
|---|---|---|
| API key required | No | Yes (OpenAI gpt-4o) |
| LLM responses | Pre-authored, section-mapped mocks | Generative (model-produced) |
| BKT / IRT / SM-2 | Full computation (pure math) | Full computation (pure math) |
| Feedback quality | Illustrative (educationally accurate) | Generative (contextually dynamic) |
| Consensus protocol | Runs all rounds with mock proposals | Runs all rounds with LLM proposals |

The `@graceful_fallback` decorator ensures that even in Live Mode, any API failure (timeout, rate limit, invalid key) is caught, logged in red, and the system continues with mock responses.

---

## Visual Logging Schema

All notebook output uses color-coded logging for clear execution tracing:

| Level | Color | Prefix | Use Case |
|---|---|---|---|
| INFO | 🔵 Blue | `[INFO]` | Agent initialization, state transitions |
| SUCCESS | 🟢 Green | `[SUCCESS]` | Completed steps, mastery threshold crossed |
| WARN | 🟡 Yellow | `[WARN]` | Degraded responses, low confidence |
| ERROR | 🔴 Red | `[HANDLED ERROR]` | API failures, fallback activation |

---

## Technical Requirements

From Chapter 15, p. 2:

- **Python:** 3.10+ (tested up to 3.12)
- **Core packages:** `openai==1.40.0`, `numpy==1.26.4`, `networkx==3.3`, `python-dotenv==1.0.1`
- **Runtime:** Jupyter Notebook or JupyterLab

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for dependency conflicts, platform-specific issues, and common runtime problems.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
