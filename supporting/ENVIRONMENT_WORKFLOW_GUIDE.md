# Pass 3: The Gold Standard Ubuntu Workflow

## 30 Agents Every AI Engineer Must Build — Environment Management Guide

---

## 1. Ubuntu System Prerequisites

Before running anything, install these system-level packages:

```bash
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    python3.11 python3.11-dev python3.11-venv \
    python3-pip \
    tesseract-ocr libtesseract-dev \
    poppler-utils \
    git curl jq
```

**Why each matters:**

| Package | Required By |
|---------|-------------|
| `build-essential`, `python3.11-dev` | Compiling C extensions (numpy, faiss-cpu, shap) |
| `python3.11-venv` | Creating venvs natively (no conda needed) |
| `tesseract-ocr`, `libtesseract-dev` | Ch06 — Document Intelligence Agent (OCR) |
| `poppler-utils` | Ch06 — pdf2image requires `pdftoppm` |
| `git` | Cloning the repo |

**Optional (GPU users only):**
```bash
# NVIDIA CUDA toolkit for Ch11 multimodal + Ch08/Ch13 transformers
# Follow: https://developer.nvidia.com/cuda-downloads (select Ubuntu)
nvidia-smi  # verify driver is working
```

---

## 2. One-Command Setup

```bash
# Clone & run
git clone https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build.git
cd 30-Agents-Every-AI-Engineer-Must-Build

# Download the setup script (or copy from the provided file)
chmod +x setup-agents-envs.sh
./setup-agents-envs.sh .
```

This script will:
1. Verify Python 3.10+
2. Install system packages
3. Create 6–7 venvs under `~/.venvs/agents/`
4. Register each as a Jupyter kernel
5. Generate `activate-chapter.sh` switcher
6. Create a `.env` template for API keys

---

## 3. The Chapter Switching Guide

### Option A: Terminal workflow (recommended for development)

```bash
# From repo root:
source activate-chapter.sh 9
cd chapter09
jupyter notebook
```

Running `source activate-chapter.sh` with no argument prints the full map:

```
Chapter → Environment mapping:
  Ch  1 → agents-foundation
  Ch  2 → agents-foundation
  Ch  3 → agents-langchain-modern
  Ch  4 → agents-foundation
  Ch  5 → agents-foundation
  Ch  6 → agents-rag-research
  Ch  7 → agents-foundation
  Ch  8 → agents-foundation
  Ch  9 → agents-langchain-modern
  Ch 10 → agents-legacy-conversational
  Ch 11 → agents-foundation  (or agents-multimodal for GPU)
  Ch 12 → agents-langchain-modern
  Ch 13 → agents-rag-research
  Ch 14 → agents-legacy-finance
  Ch 15 → agents-foundation
  Ch 16 → agents-legacy-embodied
  Ch 17 → agents-foundation
```

### Option B: Jupyter kernel selector (recommended for readers)

Since each venv registers as a Jupyter kernel, readers can:
1. Launch Jupyter from *any* terminal
2. Open a notebook
3. Go to **Kernel → Change Kernel** and select the right environment (e.g., `Python (agents-rag-research)`)

No terminal activation needed — this is the smoothest reader experience.

### Option C: VS Code

In VS Code, open any `.ipynb`, click the kernel picker in the top-right, and select the appropriate `agents-*` kernel. VS Code auto-discovers registered ipykernel environments.

---

## 4. API Key Management

All chapters use `python-dotenv` and look for a `.env` file. Place **one** `.env` at the repo root:

```bash
# .env (repo root — already gitignored)
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
TAVILY_API_KEY=tvly-your-key-here
FINNHUB_API_KEY=your-key-here
HUGGINGFACEHUB_API_TOKEN=hf_your-token-here
```

Most chapters also support **Simulation Mode** — they run without any API key using mock responses. This is ideal for testing the environment setup.

---

## 5. Maintenance Commands

```bash
# Rebuild a single environment
rm -rf ~/.venvs/agents/agents-rag-research
./setup-agents-envs.sh .

# List all registered Jupyter kernels
jupyter kernelspec list

# Remove a kernel
jupyter kernelspec uninstall agents-multimodal

# Update packages in a specific env
source ~/.venvs/agents/agents-foundation/bin/activate
pip install --upgrade openai langchain
deactivate

# Nuclear option — remove everything and start fresh
rm -rf ~/.venvs/agents
./setup-agents-envs.sh .
```

---

## 6. Disk Space Budget

| Environment | Approximate Size |
|---|---|
| `agents-foundation` | ~200 MB |
| `agents-langchain-modern` | ~400 MB |
| `agents-rag-research` | ~3.0 GB (PyTorch + transformers) |
| `agents-legacy-conversational` | ~300 MB |
| `agents-legacy-finance` | ~350 MB |
| `agents-legacy-embodied` | ~300 MB |
| `agents-multimodal` (optional) | ~4.0 GB (PyTorch + LLaVA) |
| **Total (without GPU)** | **~4.5 GB** |
| **Total (with GPU)** | **~8.5 GB** |

---

## 7. Recommended Reading Order vs Environment Switches

A reader going sequentially through the book will switch environments at these points:

```
Ch01  ─┐
Ch02   │  agents-foundation
Ch03  ─┘→ SWITCH → agents-langchain-modern
Ch04  ─── SWITCH → agents-foundation
Ch05   │
Ch06  ─┘→ SWITCH → agents-rag-research
Ch07  ─── SWITCH → agents-foundation
Ch08   │
Ch09  ─┘→ SWITCH → agents-langchain-modern
Ch10  ─── SWITCH → agents-legacy-conversational
Ch11  ─── SWITCH → agents-foundation (or agents-multimodal)
Ch12  ─── SWITCH → agents-langchain-modern
Ch13  ─── SWITCH → agents-rag-research
Ch14  ─── SWITCH → agents-legacy-finance
Ch15  ─── SWITCH → agents-foundation
Ch16  ─── SWITCH → agents-legacy-embodied
Ch17  ─── SWITCH → agents-foundation
```

That's **~11 switches across 17 chapters** — but with the `activate-chapter.sh` script or Jupyter kernel picker, each switch is a single command or click.

---

## 8. Architectural Decision Record

**Why `venv` over `conda`?**
- Readers are more likely to have `python3 -m venv` than conda
- Lighter footprint, faster creation
- No channel conflict issues
- The book's own instructions use `pip install -r requirements.txt`

**Why not Docker?**
- Adds complexity for readers who just want to run notebooks
- GPU passthrough requires nvidia-docker setup
- Overkill for a book repo with no long-running services

**Why not one venv per chapter?**
- 17 venvs × ~300MB avg = 5+ GB of duplicated packages
- Reader fatigue from constant switching
- Most chapters share 80%+ of their dependencies

**Why not one venv for all?**
- `langchain==0.2.16` and `langchain>=0.3.0` cannot coexist
- Three mutually incompatible `langgraph` pins (0.1.4, 0.2.28, >=0.3.0)
- Would require impossible constraint resolution
