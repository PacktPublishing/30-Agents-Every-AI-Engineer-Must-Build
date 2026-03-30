# Troubleshooting Guide

**Book:** *30 Agents Every AI Engineer Must Build*
**Author:** Imran Ahmad
**Chapter:** 12 — Ethical and Explainable Agents

---

## 1. Dependency Conflicts (2026 Resolutions)

| Issue | Symptom | Resolution |
|---|---|---|
| **numpy 2.x vs. shap** | `AttributeError: module 'numpy' has no attribute 'bool'` | Pin `numpy>=1.26.4,<2.1.0`. SHAP 0.45.x uses deprecated numpy aliases removed in numpy 2.0. If you need numpy 2.x, upgrade SHAP to >=0.46.0. |
| **shap vs. scipy** | `ImportError: cannot import name 'comb' from 'scipy.misc'` | Pin `shap>=0.45.1`. The `scipy.misc.comb` function was removed in scipy 1.12. SHAP 0.45+ uses `scipy.special.comb`. |
| **langchain version split** | `ImportError: cannot import name 'ChatOpenAI' from 'langchain'` | Since langchain 0.2, OpenAI integrations live in `langchain-openai`. Both packages must be installed. See `requirements.txt`. |
| **scikit-learn vs. SHAP** | `ImportError: cannot import name 'safe_indexing'` | Pin `scikit-learn>=1.5.1`. The `safe_indexing` function was removed in sklearn 1.3. SHAP >=0.45 handles this. |
| **lime installation fails** | `error: subprocess-exited-with-error` on pip install | Install build tools first: `pip install setuptools wheel`, then retry `pip install lime`. On Apple Silicon: `ARCHFLAGS="-arch arm64" pip install lime`. |
| **openai 1.x migration** | `openai.error.AuthenticationError` (old API) | The openai >=1.0 SDK uses `from openai import OpenAI; client = OpenAI()`. The old `openai.ChatCompletion.create()` pattern is removed. This repo uses the 1.x client. |
| **Python 3.12+ type hints** | `TypeError` with older langchain | Ensure `langchain>=0.2.16` which supports Python 3.12 type hint changes. |

---

## 2. Common Runtime Issues

| Issue | Symptom | Resolution |
|---|---|---|
| **"No module named 'src'"** | `ModuleNotFoundError` in notebook | The first cell of each notebook adds the project root to `sys.path`. If running from a different directory, set `PYTHONPATH` to the repository root: `export PYTHONPATH=/path/to/chapter12-ethical-explainable-agents`. |
| **"Running in Simulation Mode" unexpectedly** | Blue `[INFO]` log on every run | Check that `.env` exists in the repo root (not in `notebooks/`) and contains `OPENAI_API_KEY=sk-...` with no quotes around the value. Restart the kernel after editing `.env`. |
| **SHAP slow on large datasets** | Notebook hangs at SHAP cell | The synthetic medical dataset is 50 records, which SHAP handles in <5 seconds. If you expanded the dataset, use `shap.Explainer` with `max_evals=500` or switch to `TreeExplainer` if using a tree model. |
| **Matplotlib plots not showing** | Blank output in notebook cells | Ensure `%matplotlib inline` is in the setup cell. For VS Code, install the Jupyter extension >=2024.1. |
| **"getpass not working" in Colab** | Prompt doesn't appear | Google Colab handles `getpass` via a separate input widget. If it doesn't appear, set the key directly: `import os; os.environ['OPENAI_API_KEY'] = 'sk-...'` in a cell before the setup cell. |

---

## 3. Platform Notes

| Platform | Notes |
|---|---|
| **Google Colab** | Fully supported. Run `!pip install -r requirements.txt` in the first cell. Colab provides numpy and sklearn by default; only langchain, openai, shap, and lime need installation. |
| **VS Code + Jupyter** | Supported. Select the correct Python kernel. The `python-dotenv` integration works natively. |
| **JupyterLab 4.x** | Supported. No known conflicts with the dependency set. |
| **Windows** | All dependencies are cross-platform. Use `python -m pip install` if `pip` is not on PATH. |
| **Apple Silicon (M1/M2/M3/M4)** | All dependencies have native ARM wheels as of 2025. If lime fails, see the resolution in Section 1 above. |

---

## 4. Simulation Mode Details

The repository detects the operating mode automatically at startup:

1. Check `OPENAI_API_KEY` environment variable (loaded from `.env` via `python-dotenv`).
2. If empty, prompt via `getpass` (interactive environments only).
3. If still empty, activate **Simulation Mode**.

In Simulation Mode:
- All LLM calls are routed to `MockLLM`, which returns deterministic responses derived from chapter examples.
- All synthetic datasets are generated with `seed=42` for reproducibility.
- Every mock response includes a `_mock_meta` field (stripped before display) for traceability.
- Output schemas are identical in both modes (Live/Simulation Parity Contract).

To force Simulation Mode even with a key present, unset the variable:

```python
import os
os.environ.pop('OPENAI_API_KEY', None)
# Restart kernel, then re-run setup cell
```

---

## 5. Failure Mode Reference

The `@graceful_fallback` decorator handles all failure modes. Here is the complete matrix:

| # | Failure Mode | Trigger | Response | Log Level |
|---|---|---|---|---|
| F1 | No API key | `os.getenv` empty + getpass skipped | Global Simulation Mode | `[INFO]` Blue |
| F2 | Invalid API key | HTTP 401 from OpenAI | Switch to Simulation Mode | `[HANDLED ERROR]` Red |
| F3 | Rate limit | HTTP 429 from OpenAI | Backoff (2s/4s/8s), then mock | `[HANDLED ERROR]` Red |
| F4 | API timeout | Response >30s | Mock for that call only | `[HANDLED ERROR]` Red |
| F5 | SHAP timeout | Computation >60s | Simplified feature importance | `[HANDLED ERROR]` Red |
| F6 | LIME import error | `lime` not installed | Skip LIME cells, show message | `[HANDLED ERROR]` Red |
| F7 | Sensor data missing | Patient lacks biometrics | Degrade confidence, flag stale | `[DEBUG]` Yellow |
| F8 | Bias threshold breach | Disparate impact < 0.80 | Trigger FairnessEnforcer | `[HANDLED ERROR]` Red |
| F9 | Dataset generation error | Disk/memory issue | Regenerate with default seed | `[HANDLED ERROR]` Red |
| F10 | Model serving failure | Diagnostic model unavailable | Rule-based triage fallback | `[HANDLED ERROR]` Red |

---

*Author: Imran Ahmad — Packt Publishing*
*Chapter 12: Ethical and Explainable Agents*
