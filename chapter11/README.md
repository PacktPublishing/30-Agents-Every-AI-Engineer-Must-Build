# Chapter 11: Multi-Modal Perception Agents

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

## Overview

This repository is the executable companion to **Chapter 11** of *30 Agents Every AI Engineer Must Build*. It explores how intelligent agents perceive and act upon information beyond text — including images, audio waveforms, and physical sensor streams. Three distinct agent domains are implemented: Vision-Language Agents (visual encoder paired with LLM for joint reasoning using Chain-of-Thought prompting), Audio Processing Agents (speech transcription with mode-aware normalization and vocal emotion analysis via the VAD model), and Physical World Sensing Agents (heterogeneous sensor fusion, anomaly detection via pattern matching, and proportional control with deadband hysteresis).

Every code cell runs **without an API key** in Simulation Mode, powered by mock backends (`MockVLM`, `MockWhisperBackend`, `MockSensorStream`) that return chapter-derived responses. When a Hugging Face token and CUDA GPU are available, the notebook seamlessly switches to Live Mode.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd ./30-Agents-Every-AI-Engineer-Must-Build/
cd chapter11

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Add your Hugging Face token for Live Mode
cp .env.template .env
# Edit .env and add your token, or skip this step for Simulation Mode

# 5. Launch the notebook
jupyter notebook chapter_11_multimodal_agents.ipynb
```

## Section Map

The notebook is organized into cell groups that mirror the chapter's sections:

| Cell Group | Chapter Section | Concept Demonstrated |
|---|---|---|
| **0** | Setup | Imports, environment detection, Simulation Mode activation |
| **1** | §11.1 — Vision-Language Architecture | Visual encoder (ViT), alignment mechanism, cross-modal attention |
| **2** | §11.1 — Vision QA Agent | LLaVA 1.5, Chain-of-Thought prompting, structured output parsing |
| **3** | §11.1 — Integration Patterns | Adapter-based, cross-attention, early fusion; latency management |
| **4** | §11.2 — Audio Architecture | STFT, spectrograms, Whisper encoder architecture |
| **5** | §11.2 — Speech Recognition | TranscriptionMode (verbatim/clean/normalized), RMS normalization |
| **6** | §11.2 — Voice Sentiment | Prosodic features, VAD model, emotion profile matching |
| **7** | §11.3 — Smart Building Architecture | ZoneConfig/ZoneState separation, digital twin concept |
| **8** | §11.3 — Event Detection | EventPattern with lambda conditions, severity levels |
| **9** | §11.3 — Control Management | Proportional control, deadband hysteresis, short-cycling prevention |
| **10** | §11.3 — Sensor Fusion | Temporal averaging, 5-minute fusion window, process_zone loop |

## Real-World Use Case: Meridian Facilities

How does a commercial property firm managing 22 buildings use multimodal agents to cut energy costs, eliminate security alert fatigue, and prevent data center SLA breaches? The companion case study follows **Meridian Facilities** as they deploy vision-language agents for contextual occupancy analysis, audio agents for tenant call routing, and physical sensing agents with proportional HVAC control and CO2 monitoring.

Read the full case study: **[USECASE.md](USECASE.md)** — includes the 4 building scenarios (normal office, server overheat, after-hours intrusion, high CO2), energy savings, and tenant retention impact.

## Repository Structure

```
chapter11/
│
├── README.md                              # This file
├── AGENTS.md                              # Agentic AI metadata
├── LICENSE                                # MIT License
├── requirements.txt                       # Pinned Python dependencies
├── .env.template                          # Token template (zero-hardcode policy)
├── .gitignore                             # Standard Python + .env exclusions
├── troubleshooting.md                     # Dependency conflict resolution guide
│
├── chapter_11_multimodal_agents.ipynb     # Primary deliverable
│
├── mock_backends.py                       # MockVLM, MockWhisperBackend, MockSensorStream
└── agent_logger.py                        # Color-coded logging + @graceful_fallback decorator
```

## Simulation Mode

When no Hugging Face token or CUDA GPU is detected, the notebook activates **Simulation Mode**:

- `MockVLM`, `MockWhisperBackend`, and `MockSensorStream` replace live backends transparently
- All responses are pre-authored from Chapter 11 content
- Every cell executes successfully with no GPU or external dependencies
- Outputs are deterministic and chapter-accurate

## Resilience Architecture

All agent operations are wrapped in the `@graceful_fallback` decorator:

- **On success:** `[INFO]` (blue) → `[SUCCESS]` (green)
- **On failure:** `[INFO]` (blue) → `[HANDLED ERROR]` (red) → fallback value returned
- **Guarantee:** No cell in the notebook will ever raise an unhandled exception

## Requirements

- **Python:** 3.10+ (recommended: 3.11 or 3.12)
- **Dependencies:** See `requirements.txt`
- **API Key / GPU:** Optional (Simulation Mode works without either)

For Live Mode: CUDA-capable GPU with 16+ GB VRAM and a Hugging Face account with LLaVA 1.5 access.

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for environment-specific guidance, compatibility matrix, and solutions to common issues.

## License

This code is provided as educational companion material for *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026). See the book for full terms of use.

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build* (Packt Publishing, 2026)
