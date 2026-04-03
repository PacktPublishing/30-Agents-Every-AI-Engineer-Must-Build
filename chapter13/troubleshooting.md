# Troubleshooting Guide

**Chapter 13: Healthcare and Scientific Agents**
**Book:** *30 Agents Every AI Engineer Must Build*
**Author:** Imran Ahmad

This guide covers known dependency conflicts and runtime issues. Each entry includes the symptom, root cause, and fix.

---

## Issue 1: NumPy 2.x Breaking Changes

**Symptom:** `AttributeError: module 'numpy' has no attribute 'float_'` or similar errors referencing removed aliases.

**Cause:** NumPy 2.0+ removed deprecated aliases (`np.float_`, `np.int_`, `np.object_`). Some older versions of `scipy` and `transformers` reference these.

**Fix:**
```bash
pip install "numpy>=1.24,<2.1"
# If conflict persists:
pip install "numpy==1.26.4"
```

---

## Issue 2: LangChain Version Mismatch

**Symptom:** `ImportError` or `AttributeError` when importing LangChain components.

**Cause:** LangChain packages must have matching minor versions. Mixing `0.2.x` with `0.3.x` breaks imports.

**Fix:**
```bash
pip install "langchain-core>=0.3,<0.4" "langchain-community>=0.3,<0.4"
```

---

## Issue 3: fhir.resources Import Error

**Symptom:** `ModuleNotFoundError: No module named 'fhir.resources'` or Pydantic v1/v2 conflict.

**Cause:** `fhir.resources` 7.x requires Pydantic v2. If Pydantic v1 is installed (common with older LangChain), there is a conflict.

**Fix:**
```bash
pip install "pydantic>=2.0,<3.0" "fhir.resources>=7.0,<8.0"
```

---

## Issue 4: nest_asyncio Not Applied

**Symptom:** `RuntimeError: This event loop is already running` when running async scanner cells in Jupyter.

**Cause:** Jupyter runs its own event loop. `asyncio.run()` cannot start a new one inside it.

**Fix:** The notebook applies `nest_asyncio` automatically in the setup cell:
```python
import nest_asyncio
nest_asyncio.apply()
```
If the error persists, run the above manually before executing async cells.

---

## Issue 5: Transformers Slow Import / CUDA Warnings

**Symptom:** Importing `transformers` takes 30+ seconds or prints CUDA warnings on a CPU-only machine.

**Cause:** `transformers` attempts to detect GPU hardware at import time.

**Fix:** This is cosmetic. The notebook uses `transformers` only for tokenizer references in live mode. In Simulation Mode, it is not imported. To suppress warnings:
```python
import os
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
```

---

## Issue 6: aiohttp SSL Certificate Errors

**Symptom:** `aiohttp.client_exceptions.ClientConnectorCertificateError` when running the literature scanner.

**Cause:** Corporate proxy or outdated `certifi` bundle.

**Fix:**
```bash
pip install --upgrade certifi
# If behind corporate proxy:
pip install aiohttp[speedups]
```

---

## Issue 7: Color Codes Render as Escape Sequences

**Symptom:** `\033[94m[INFO]\033[0m` appears as raw text instead of colored output.

**Cause:** Non-ANSI-compatible terminal or IDE output panel (some VS Code configurations, Windows CMD without ANSI support).

**Fix:** The notebook detects this and falls back to plain-text logging:
```python
import sys
SUPPORTS_COLOR = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
# Fallback: strip ANSI codes if not supported
```
In Jupyter notebooks, ANSI colors are supported by default. This issue primarily affects execution via `nbconvert --execute` or non-interactive terminals.
