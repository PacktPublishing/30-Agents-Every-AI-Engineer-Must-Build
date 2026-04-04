# Chapter 8 — Data Analysis and Reasoning Agents

**Book:** *Agents* by Imran Ahmad (Packt Publishing, 2026)
**Author:** Imran Ahmad
**Chapter:** 8 — Data Analysis and Reasoning Agents (pp. 203–233)

---

## Overview

This repository is the companion code for Chapter 8 of *Agents*. It implements
three agent archetypes that transform raw data into defensible, actionable
intelligence:

1. **Data Analysis Agent** (§8.1) — Cognitive loop for intent analysis,
   statistical reasoning, visualization recommendation, and anomaly detection.
2. **Verification & Validation Agent** (§8.2) — Fact-checking, logical
   coherence, NLI-based evidence scoring, and consistency analysis.
3. **General Problem Solver** (§8.3) — Five-stage meta-reasoning cycle:
   decompose → analogy search → hypothesize → test → meta-learn.

Two extended case studies demonstrate these patterns in practice:

- **Case Study 1** (§8.4): A newsroom fact-checking assistant that extracts
  claims from articles and verifies them against a trusted database.
- **Case Study 2** (§8.5): A cross-disciplinary hypothesis engine that applies
  ecological resilience principles to power grid stability.

A unifying **Tri-Agent Pipeline** (§8.6) wires all three agents into a
trust-then-escalate architecture.

---

## Quickstart

```bash
# 1. Clone and enter the repository
git clone <repo-url>
cd chapter-08-data-analysis-reasoning-agents

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the notebook
jupyter notebook ch08_data_analysis_reasoning_agents.ipynb
```

No API key is required. The notebook runs fully in **Simulation Mode** with
chapter-accurate mock outputs. See the section below for live-mode instructions.

---

## Section Map

| Notebook Section | Chapter Ref | Book Pages | Topic |
|:---|:---|:---|:---|
| Section 0 | — | — | Environment setup, API key resolution, Simulation Mode |
| Section 1 | §8.1, §8.1.1, §8.1.2 | pp. 204–211 | Data Analysis Agent: visualization recommender, OLS regression, anomaly detection |
| Section 2 | §8.2–§8.2.5 | pp. 211–215 | V&V Agent: theory narrative, BART-MNLI NLI demo |
| Section 3 | §8.3–§8.3.4 | pp. 215–219 | General Problem Solver: theory, pseudocode class |
| Section 4 | §8.4 | pp. 220–226 | Case Study 1: News fact-checking assistant |
| Section 5 | §8.5 | pp. 226–231 | Case Study 2: Cross-disciplinary GPS hypothesis engine |
| Section 6 | §8.6 | pp. 231–232 | Tri-Agent Pipeline integration demo |

---

## Simulation Mode

When no `OPENAI_API_KEY` is detected, the notebook activates Simulation Mode
automatically:

- All LLM calls route to `MockLLM` (`utils/mock_llm.py`), which returns
  deterministic, chapter-accurate responses.
- Color-coded logging (Blue/Green/Red) traces the agent's reasoning.
- Every cell completes without errors or tracebacks.
- Outputs are logically identical to live-mode results.

No API key, no internet connection, and no GPU are required.

---

## Live Mode

To run with a real OpenAI API:

1. Copy `.env.template` to `.env`:
   ```bash
   cp .env.template .env
   ```
2. Edit `.env` and insert your key:
   ```
   OPENAI_API_KEY=sk-...
   ```
3. Run the notebook. The setup cell will detect the key and initialize the
   OpenAI client. Live API calls replace mock responses; fallback to
   `MockLLM` activates automatically if any API call fails.

---

## File Descriptions

| File | Purpose |
|:---|:---|
| `ch08_data_analysis_reasoning_agents.ipynb` | Primary notebook (6 section groups) |
| `utils/__init__.py` | Public exports: `load_api_key`, `log`, `MockLLM`, `llm_call`, `fail_gracefully` |
| `utils/config.py` | Three-tier API key resolution (`.env` → `os.getenv` → `getpass`) |
| `utils/color_logger.py` | ANSI color-coded logging: Blue (INFO), Green (SUCCESS), Red (ERROR) |
| `utils/mock_llm.py` | MockLLM class, 7-entry mock registry, `llm_call()` wrapper, `@fail_gracefully` decorator |
| `data/sample_sales_data.csv` | Synthetic sales dataset (100 rows, `seed=42`) for §8.1.2 demos |
| `requirements.txt` | Pinned dependencies (core + optional NLI + Jupyter) |
| `troubleshooting.md` | 9 common issues with copy-paste fixes |
| `AGENTS.md` | Agentic metadata: persona prompt, simulation contract, file roles |
| `.env.template` | API key placeholder |
| `.gitignore` | Repository hygiene |
| `LICENSE` | MIT License |

---

## License

MIT License. Copyright (c) 2026 Imran Ahmad. See [LICENSE](LICENSE) for details.
