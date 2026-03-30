# Chapter 13: Healthcare and Scientific Agents

**Book:** *30 Agents Every AI Engineer Must Build*
**Author:** Imran Ahmad
**Publisher:** Packt Publishing
**Year:** 2026

---

## Overview

This repository contains the companion code for **Chapter 13** of
*30 Agents Every AI Engineer Must Build*. The chapter explores two
high-stakes agentic AI domains:

1. **Healthcare Intelligence Agent (Sections 13.1–13.4)** — A clinical
   decision-support pipeline featuring Bayesian belief updating,
   FHIR-compliant data normalization, multi-specialist diagnostic
   coordination, and audience-adapted explanations.

2. **Scientific Discovery Agent (Sections 13.5–13.8)** — A research
   acceleration pipeline featuring asynchronous literature scanning,
   knowledge-gap detection, abductive hypothesis generation, and
   closed-loop experiment tracking.

Both agents are built using production-grade patterns from the book,
including resilience decorators, color-coded logging, and a full
simulation mode that lets readers run every cell without any API keys.

## Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd chapter13-healthcare-scientific-agents

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Configure API keys
cp .env.template .env
# Edit .env with your keys — or skip this step for Simulation Mode

# 5. Launch the notebook
jupyter notebook chapter13_healthcare_scientific_agents.ipynb
```

## Simulation Mode

**No API keys are required.** The notebook automatically detects missing
keys and activates Simulation Mode, which provides context-aware mock
responses derived directly from the chapter content. Every cell produces
meaningful, deterministic output in this mode.

## Repository Structure

```
chapter13-healthcare-scientific-agents/
├── chapter13_healthcare_scientific_agents.ipynb   # Main notebook
├── AGENTS.md              # Agentic metadata and AI collaborator persona
├── README.md              # This file
├── requirements.txt       # Pinned dependencies
├── .env.template          # API key placeholders (all optional)
└── troubleshooting.md     # Dependency conflict resolutions
```

## Author

**Imran Ahmad** — Author of *30 Agents Every AI Engineer Must Build*,
published by Packt Publishing.

## License

This project is provided as companion material for the book. Please
refer to the publisher's license terms at
[Packt Publishing](https://www.packtpub.com/) for usage rights.

Copyright (c) 2026 Packt Publishing. All rights reserved.
