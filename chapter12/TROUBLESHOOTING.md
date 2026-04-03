# Troubleshooting Guide

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad
**Chapter:** 12 — Ethical and Explainable Agents

---

## 1. Dependency Conflicts (2026 Resolutions)

### numpy 2.x vs. shap

**Symptom:** `AttributeError: module 'numpy' has no attribute 'bool'`

**Resolution:** Pin `numpy>=1.26.4,<2.1.0`. SHAP 0.45.x uses deprecated numpy aliases removed in numpy 2.0. If you need numpy 2.x, upgrade SHAP to >=0.46.0.

### langchain version split

**Symptom:** `ImportError: cannot import name 'ChatOpenAI' from 'langchain'`

**Resolution:** Since langchain 0.2, OpenAI integrations live in `langchain-openai`. Both packages must be installed. See `requirements.txt`.

### scikit-learn vs. SHAP

**Symptom:** `ImportError: cannot import name 'safe_indexing'`

**Resolution:** Pin `scikit-learn>=1.5.1`. The `safe_indexing` function was removed in sklearn 1.3. SHAP >=0.45 handles this.

### lime installation fails

**Symptom:** `error: subprocess-exited-with-error` on pip install

**Resolution:** Install build tools first: `pip install setuptools wheel`, then retry `pip install lime`. On Apple Silicon: `ARCHFLAGS="-arch arm64" pip install lime`.

### openai 1.x migration

**Symptom:** `openai.error.AuthenticationError` (old API)

**Resolution:** The openai >=1.0 SDK uses `from openai import OpenAI; client = OpenAI()`. The old `openai.ChatCompletion.create()` pattern is removed. This repo uses the 1.x client.

### Python 3.12+ type hints

**Symptom:** `TypeError` with older langchain

**Resolution:** Ensure `langchain>=0.2.16` which supports Python 3.12 type hint changes.

---

## 2. Common Runtime Issues

### "No module named 'src'"

**Symptom:** `ModuleNotFoundError` in notebook

**Resolution:** The first cell of each notebook adds the project root to `sys.path`. If running from a different directory, set `PYTHONPATH` to the repository root.

### "Running in Simulation Mode" unexpectedly

**Symptom:** Blue [INFO] log on every run

**Resolution:** Check that `.env` exists in the repo root (not in `notebooks/`) and contains `OPENAI_API_KEY=sk-...` with no quotes. Restart the kernel after editing `.env`.

### SHAP slow on large datasets

**Symptom:** Notebook hangs at SHAP cell

**Resolution:** The synthetic medical dataset is 50 records, which SHAP handles in <5 seconds. If you expanded the dataset, use `shap.Explainer` with `max_evals=500` or switch to `TreeExplainer` if using a tree model.

### Matplotlib plots not showing

**Symptom:** Blank output in notebook cells

**Resolution:** Ensure `%matplotlib inline` is in the setup cell. For VS Code, install the Jupyter extension >=2024.1.

### "getpass not working" in Colab

**Symptom:** Prompt doesn't appear

**Resolution:** Google Colab handles `getpass` via a separate input widget. If it doesn't appear, set the key directly: `import os; os.environ['OPENAI_API_KEY'] = 'sk-...'` in a cell before the setup cell.

---

## 3. Platform Notes

| Platform | Notes |
|---|---|
| **Google Colab** | Fully supported. Run `!pip install -r requirements.txt` in the first cell. Colab provides numpy and sklearn by default; only langchain, openai, shap, and lime need installation. |
| **VS Code + Jupyter** | Supported. Select the correct Python kernel. The `python-dotenv` integration works natively. |
| **JupyterLab 4.x** | Supported. No known conflicts with the dependency set. |
| **Windows** | All dependencies are cross-platform. Use `python -m pip install` if `pip` is not on PATH. |
| **Apple Silicon (M1/M2/M3/M4)** | All dependencies have native ARM wheels as of 2025. If lime fails, see the resolution above. |
