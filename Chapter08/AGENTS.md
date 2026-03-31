# AGENTS.md — Agentic Repository Metadata

**Book:** *Agents* by Imran Ahmad (Packt, 2026) — ISBN B34135
**Chapter:** 8 — Data Analysis and Reasoning Agents
**Author:** Imran Ahmad
**Standard:** 2026 Agentic AI Foundation

---

## 1. Repository Identity

This repository is the companion code for Chapter 8 of *Agents* by Imran Ahmad
(Packt Publishing, 2026). It implements three agent archetypes — the **Data
Analysis Agent**, the **Verification & Validation Agent**, and the **General
Problem Solver** — followed by two extended case studies (a newsroom
fact-checker and a cross-disciplinary hypothesis engine) and a unifying
tri-agent pipeline.

The primary deliverable is a single Jupyter notebook
(`ch08_data_analysis_reasoning_agents.ipynb`) supported by a thin `utils/`
layer. The repository is designed to run end-to-end in both live-API and fully
offline **Simulation Mode**.

---

## 2. Agent Persona Prompt

The following system prompt governs the behavior of any AI assistant working
with this repository:

```
You are an expert AI Engineering Tutor assisting a reader of
"Agents" by Imran Ahmad (Packt, 2026), Chapter 8: Data Analysis
and Reasoning Agents.

TONE: Academic, patient, and precise. Assume the reader is an
intermediate Python developer learning agentic AI patterns for
the first time. Explain *why* before *how*. Never condescend.

TECHNICAL STANCE:
- Reference specific chapter section numbers (e.g., "As introduced
  in Section 8.2.1 on Fact-Checking...").
- Use the book's architectural vocabulary: "cognitive loop",
  "perception-reasoning-action", "meta-learning engine",
  "trust-then-escalate".
- When suggesting code changes, maintain the @fail_gracefully
  decorator + MockLLM fallback pattern.

CONSTRAINTS:
- Never introduce live API calls without a corresponding mock path.
- Never hardcode API keys or secrets.
- Always preserve color-coded logging (Blue/Green/Red).
- Attribute all work to the author, Imran Ahmad.
- Do not sign or watermark any generated content with LLM names.
```

---

## 3. Simulation Mode Contract

When the environment variable `OPENAI_API_KEY` is absent (or the user presses
Enter at the `getpass` prompt), the notebook activates **Simulation Mode**:

- All LLM calls route through `MockLLM` (defined in `utils/mock_llm.py`).
- Outputs are **deterministic** and **chapter-accurate**: every mock response
  is derived verbatim from the expected outputs described in Chapter 8.
- The notebook produces identical logical results in both modes.
- Color-coded logging (Blue/Green/Red) remains active in both modes.
- No API key is ever required to run the full notebook.

---

## 4. File Roles

| File | Purpose | Modifiable? |
|:-----|:--------|:------------|
| `ch08_data_analysis_reasoning_agents.ipynb` | Primary notebook — all 6 section groups | Yes (with care) |
| `utils/__init__.py` | Public API exports | Append only |
| `utils/config.py` | Three-tier API key resolution | Stable — modify only to add new providers |
| `utils/color_logger.py` | ANSI color-coded logging | Stable |
| `utils/mock_llm.py` | MockLLM, mock registry, `llm_call()`, `@fail_gracefully` | Extend registry for new sections |
| `data/sample_sales_data.csv` | Synthetic dataset (100 rows, seed=42) | Regenerate only via documented script |
| `requirements.txt` | Pinned dependencies | Update versions conservatively |
| `troubleshooting.md` | Common issues and fixes | Append new scenarios as needed |
| `.env.template` | API key placeholder | Never add real keys |
| `.gitignore` | Repository hygiene | Append only |
| `LICENSE` | MIT License | Do not modify |
| `README.md` | Overview, quickstart, section map | Keep synchronized with notebook |
| `AGENTS.md` | This file — agentic metadata | Keep synchronized with repo changes |

---

## 5. Contribution Guidelines

Any AI agent or human contributor working on this repository must:

1. **Never introduce live API calls without a corresponding mock path.**
   Every function that calls an LLM must route through `llm_call()` and
   have a matching entry in the `MOCK_REGISTRY`.

2. **Never hardcode API keys or secrets.** Use the three-tier resolution
   in `utils/config.py`.

3. **Preserve color-coded logging.** All agent actions must produce
   Blue (INFO), Green (SUCCESS), or Red (HANDLED ERROR) log output.

4. **Reference chapter sections in docstrings.** Every function and
   markdown cell must cite the relevant section number (e.g., §8.1.1).

5. **Wrap all tool/LLM calls in `@fail_gracefully`.** Specify a typed
   `fallback_value` and the chapter `section` reference.

6. **Attribute all work to the author, Imran Ahmad.** Do not sign or
   watermark generated content with LLM tool names.
