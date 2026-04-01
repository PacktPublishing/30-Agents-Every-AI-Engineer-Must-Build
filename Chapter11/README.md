# Chapter 11: Multi-Modal Perception Agents

**Book:** *30 Agents Every AI Engineer Must Build*
**Author:** Imran Ahmad
**Publisher:** Packt Publishing
**Chapter:** 11 — Multi-Modal Perception Agents

---

## Overview

This repository contains the complete companion code for Chapter 11, which explores how intelligent agents perceive and act upon information beyond text — including images, audio waveforms, and physical sensor streams. The chapter implements three distinct agent domains:

1. **Vision-Language Agents** — Pair a visual encoder with a large language model to reason jointly over images and natural language questions. Demonstrates Chain-of-Thought prompting for systematic visual analysis.

2. **Audio Processing Agents** — Transcribe speech with mode-aware normalization (verbatim vs. clean), and analyze vocal emotion using the Valence-Arousal-Dominance (VAD) model through prosodic feature extraction.

3. **Physical World Sensing Agents** — Fuse heterogeneous sensor streams (temperature, CO2, occupancy) into coherent zone state, detect anomalies via pattern matching, and issue proportional control commands with deadband hysteresis.

All three domains follow the **Sense-Model-Plan-Act** loop introduced in Chapter 1.

---

## Quickstart

```bash
# 1. Clone and enter the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd 30-Agents-Every-AI-Engineer-Must-Build/chapter11

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the notebook (Simulation Mode — no GPU or API key required)
jupyter notebook chapter_11_multimodal_agents.ipynb
```

The notebook auto-detects your environment and activates **Simulation Mode** if no Hugging Face token or CUDA GPU is found. Every cell runs successfully in Simulation Mode.

---

## Simulation Mode vs. Live Mode

| Aspect | Simulation Mode | Live Mode |
|--------|----------------|-----------|
| **GPU required** | No | Yes (16+ GB VRAM) |
| **API token required** | No | Yes (Hugging Face) |
| **Activated when** | No `.env` token or no CUDA GPU detected | Valid token + CUDA GPU present |
| **Backend used** | `mock_backends.py` (chapter-accurate responses) | `transformers` + `torch` (real inference) |
| **Output quality** | Deterministic, pre-built responses | Full model inference |
| **Purpose** | Learning, code review, CI/CD testing | Production experimentation |

To switch to Live Mode:
1. Copy `.env.template` to `.env`
2. Add your Hugging Face token
3. Uncomment the GPU dependencies in `requirements.txt`
4. Install: `pip install -r requirements.txt`

---

## Repository Structure

```
chapter11/
├── README.md                              # This file
├── AGENTS.md                              # Agentic metadata and AI persona definition
├── requirements.txt                       # Pinned dependencies (core + optional GPU)
├── .env.template                          # Token template — copy to .env for Live Mode
├── .gitignore                             # Excludes .env, __pycache__, checkpoints
├── LICENSE                                # MIT License
│
├── chapter_11_multimodal_agents.ipynb     # Primary notebook — all 3 agent domains
│
├── mock_backends.py                       # MockVLM, MockWhisperBackend, MockSensorStream
├── agent_logger.py                        # Color-coded logging + @graceful_fallback decorator
│
├── troubleshooting.md                     # 8 common issues with fixes + compatibility matrix
│
└── assets/
    └── (generated at runtime)             # sample_workspace.png created by notebook
```

---

## Chapter Sections Covered

| Section | Notebook Part | Key Concepts |
|---------|--------------|-------------|
| Architecture of Vision-Language Agents | Part 1 | Visual encoder (ViT), alignment mechanism, cross-modal attention |
| Building a Vision Question-Answering Agent | Part 1 | LLaVA 1.5, Chain-of-Thought prompting, structured output parsing |
| Integration Patterns and Production Considerations | Part 1 | Adapter-based, cross-attention, early fusion; latency management |
| Architecture of Audio Processing Agents | Part 2 | STFT, spectrograms, Whisper encoder architecture |
| Building a Speech Recognition Agent | Part 2 | TranscriptionMode (verbatim/clean/normalized), RMS normalization |
| Voice Sentiment Analysis | Part 2 | Prosodic features, VAD model, emotion profile matching |
| Smart Building Management Architecture | Part 3 | ZoneConfig/ZoneState separation, digital twin concept |
| Event Detection Through Pattern Matching | Part 3 | EventPattern with lambda conditions, severity levels |
| Control Management and Feedback Loops | Part 3 | Proportional control, deadband hysteresis, short-cycling prevention |
| Smart Building Agent Integration and Sensor Fusion | Part 3 | Temporal averaging, 5-minute fusion window, process_zone loop |

---

## Prerequisites

**For Simulation Mode (default):**
- Python 3.10 or later
- `numpy`, `Pillow`, `python-dotenv` (installed via `requirements.txt`)

**For Live Mode (optional):**
- CUDA-capable GPU with 16+ GB VRAM
- Hugging Face account with LLaVA 1.5 access
- `torch>=2.2.0`, `transformers>=4.40.0`, `accelerate>=0.28.0`

See [troubleshooting.md](troubleshooting.md) for environment-specific guidance.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

*Part of the companion code for "30 Agents Every AI Engineer Must Build" by Imran Ahmad (Packt Publishing, 2026).*
