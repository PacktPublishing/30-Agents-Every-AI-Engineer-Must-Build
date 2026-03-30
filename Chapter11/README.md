# Chapter 11: Multi-Modal Perception Agents

**Book:** *30 Agents Every AI Engineer Must Build*
**Author:** Imran Ahmad
**Publisher:** Packt Publishing

---

## Overview

This repository contains the complete, runnable code for **Chapter 11 — Multi-Modal Perception Agents**. The chapter explores three agent domains that extend AI perception beyond text:

1. **Vision-Language Agents** — Answering natural-language questions about images using architecture inspired by LLaVA 1.5, including alignment mechanisms between vision encoders and language models.
2. **Audio Processing Agents** — Transcribing speech with filler-word removal and detecting caller emotion through prosodic feature analysis (pitch, speech rate, energy) mapped to a Valence-Arousal-Dominance model.
3. **Physical World Sensing Agents** — Managing smart building zones with event detection through pattern matching, proportional control with deadband logic, and sensor fusion through temporal averaging.

Every agent is built with a **Sense → Model → Plan → Act** loop and is fully functional in **Simulation Mode** — no GPU, API keys, or hardware required.

---

## Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy the environment template (optional — only for Live Mode)
cp .env.template .env

# 3. Run the notebook
jupyter notebook chapter_11_multimodal_agents.ipynb
```

The notebook auto-detects your environment. If no GPU or Hugging Face token is found, it activates **Simulation Mode** and uses high-fidelity mock backends that produce chapter-sourced output.

---

## Simulation Mode vs. Live Mode

| Feature | Simulation Mode | Live Mode |
|---|---|---|
| GPU required | No | Yes (16+ GB VRAM) |
| Hugging Face token | Not needed | Required |
| Model weights | Mock backends | LLaVA 1.5 (7B) + Whisper |
| Output fidelity | Chapter-sourced responses | Real model inference |
| Install time | ~10 seconds | ~15 minutes (model download) |
| Recommended for | Learning, CI/CD, review | Research, production prototyping |

**How it works:** Cell 1 of the notebook checks for `torch`, CUDA availability, and a valid `HUGGINGFACE_TOKEN`. If any are missing, `SIMULATION_MODE` is set to `True`, and all agent classes receive mock backends injected at construction time. The agent class code is identical in both modes — only the backend differs.

---

## Repository Structure

```
chapter11/
├── README.md                              # This file
├── AGENTS.md                              # Agentic metadata & AI persona contract
├── requirements.txt                       # Pinned dependencies (core + optional)
├── .env.template                          # Token template (copy to .env)
├── .gitignore                             # Standard Python/Jupyter ignores
│
├── chapter_11_multimodal_agents.ipynb     # Primary notebook — all 3 agent domains
│
├── mock_backends.py                       # MockVLM, MockWhisperBackend, MockSensorStream
├── agent_logger.py                        # Color-coded logging + @graceful_fallback
│
├── troubleshooting.md                     # Dependency conflict resolutions
│
└── assets/
    └── (generated at runtime)             # sample_workspace.png created by notebook
```

---

## Chapter Sections Covered

| # | Section | Domain | Notebook Part |
|---|---|---|---|
| 1 | Architecture of Vision-Language Agents | Vision | Part 1 |
| 2 | Building a Vision QA Agent | Vision | Part 1 |
| 3 | Integration Patterns | Vision | Part 1 |
| 4 | Architecture of Audio Processing Agents | Audio | Part 2 |
| 5 | Building a Speech Recognition Agent | Audio | Part 2 |
| 6 | Voice Sentiment Analysis | Audio | Part 2 |
| 7 | Smart Building Management Architecture | Physical | Part 3 |
| 8 | Event Detection Through Pattern Matching | Physical | Part 3 |
| 9 | Control Management and Feedback Loops | Physical | Part 3 |
| 10 | Sensor Fusion Through Data Aggregation | Physical | Part 3 |

---

## Prerequisites

- **Python** >= 3.10
- **Core packages:** `numpy`, `Pillow`, `python-dotenv` (installed via `requirements.txt`)
- **Optional (Live Mode only):** `torch >= 2.2`, `transformers >= 4.40`, `accelerate >= 0.28`

See [troubleshooting.md](troubleshooting.md) for common installation issues and the environment compatibility matrix.

---

## Color-Coded Log Output

The notebook uses a custom `AgentLogger` that produces ANSI-colored output:

- 🔵 **BLUE** `[INFO]` — Status and mode detection messages
- 🟢 **GREEN** `[SUCCESS]` — Successful agent operations
- 🔴 **RED** `[ERROR]` — Failures, critical alerts, and intentional error demos

If ANSI codes render as raw text in your environment, see [troubleshooting.md](troubleshooting.md) — Issue 7.

---

## License

This code accompanies *30 Agents Every AI Engineer Must Build* by Imran Ahmad, published by Packt Publishing. See the repository root LICENSE for terms.

---

*Author: Imran Ahmad — Packt Publishing, 2026*
