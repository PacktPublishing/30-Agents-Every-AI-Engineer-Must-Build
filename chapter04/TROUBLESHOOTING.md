# Troubleshooting Guide

**Book:** *Agents* by Imran Ahmad (Packt, 2026)
**Chapter:** 4 — Agent Deployment and Responsible Development

This guide covers the most common issues encountered when running the Chapter 4 companion notebook, along with their causes and solutions.

---

## Issue 1: `ModuleNotFoundError: No module named 'src'`

**Cause:** The notebook kernel's working directory is not the repository root, so Python cannot locate the `src/` package.

**Fix:**

Add this to the first cell of the notebook (or verify it is already present):

```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(".")))
```

Alternatively, ensure the notebook is opened from the `chapter-04-agent-deployment/` directory:

```bash
cd chapter-04-agent-deployment
jupyter notebook chapter_04_agent_deployment.ipynb
```

---

## Issue 2: `ImportError: cannot import name 'retry' from 'tenacity'`

**Cause:** An outdated version of `tenacity` is installed. The API changed in the 9.x release series.

**Fix:**

```bash
pip install --upgrade tenacity>=9.1.0
```

---

## Issue 3: ANSI color codes render as raw text (no colors)

**Cause:** Some Jupyter environments (JupyterLab versions before 4.0, older VS Code notebook extensions) strip ANSI escape codes from cell output.

**Fix:**

Install the ANSI rendering extension:

```bash
pip install ipywidgets
jupyter labextension install @jupyterlab/ansi-rendering
```

Alternatively, the `AgentLogger` includes an `html_mode=True` option that uses IPython HTML display instead of ANSI codes:

```python
from src.agent_utils import AgentLogger
logger = AgentLogger(html_mode=True)
```

---

## Issue 4: `httpx.ConnectError` in Simulation Mode

**Cause:** A code path is accidentally hitting a real endpoint instead of being intercepted by the mock layer.

**Fix:**

1. Verify that `SIMULATION_MODE` is `True` in the Cell 0 output banner.
2. If it is `True`, this indicates a bug where the mock layer is being bypassed. Check that `src/mock_llm.py` is importable:

```python
from src.mock_llm import MockLLM
print("Mock layer loaded successfully.")
```

3. If the import fails, reinstall from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Issue 5: `pandas` version conflict with `numpy`

**Cause:** `pandas>=2.2.0` requires `numpy>=1.26.0`. Older numpy installations create an incompatibility.

**Fix:**

```bash
pip install --upgrade numpy>=2.1.0 pandas>=2.2.0
```

---

## Issue 6: Notebook kernel dies on Cell 3 (Circuit Breaker)

**Cause:** The simulated retry loop with `time.sleep()` can conflict with certain async Jupyter kernels, especially in resource-constrained environments.

**Fix:**

Reduce the simulated latency when instantiating the mock LLM:

```python
mock_llm = MockLLM(latency_ms=50)  # Lower from default 150ms
```

---

## Issue 7: `.env` file not loading

**Cause:** `python-dotenv` requires the `.env` file to be in the current working directory or at an explicitly specified path.

**Fix:**

Pass an explicit path to `load_dotenv`:

```python
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")  # Adjust path relative to your notebook location
```

Or ensure the notebook is launched from the repository root where the `.env` file resides.

---

## Issue 8: `Permission denied` when writing to `figures/`

**Cause:** The notebook is running in a read-only environment (Docker container, Binder, Google Colab).

**Fix:**

No action needed. The notebook detects read-only filesystems and automatically falls back to inline matplotlib display instead of file export. If you see this warning, all visualisations will still render correctly within the notebook cells.

---

## Still Having Issues?

1. Confirm you are using Python 3.10 or later: `python --version`
2. Install all dependencies in a fresh virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Check the [README.md](../README.md) for the latest setup instructions.
