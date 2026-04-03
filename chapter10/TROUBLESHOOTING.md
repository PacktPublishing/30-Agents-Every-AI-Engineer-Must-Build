# Troubleshooting Guide

**Book:** 30 Agents Every AI Engineer Must Build
**Author:** Imran Ahmad
**Chapter:** 10 — Conversational and Content Creation Agents

---

## Issue 1: `numpy` 2.x Breaks FAISS

**Symptom:** `ImportError: numpy.core.multiarray failed to import` or
`faiss` segfaults on import.

**Cause:** `faiss-cpu==1.8.0` was compiled against numpy 1.x ABI. numpy 2.0
(released June 2024) introduced breaking C API changes.

**Fix:**
```bash
pip install "numpy>=1.24.0,<2.0.0"
pip install faiss-cpu==1.8.0 --force-reinstall --no-deps
```

---

## Issue 2: LangChain Import Path Changes (0.2.x → 0.3.x)

**Symptom:** `ImportError: cannot import name 'ConversationSummaryBufferMemory' from 'langchain.memory'`

**Cause:** LangChain 0.3.x moved memory classes to `langchain_community`.
This repository pins `langchain==0.2.16` where the import path is `langchain.memory`.

**Fix:** Ensure exact version pins from `requirements.txt`:
```bash
pip install langchain==0.2.16 langchain-community==0.2.16
```

---

## Issue 3: `tiktoken` Not Found

**Symptom:** `ModuleNotFoundError: No module named 'tiktoken'`

**Cause:** `tiktoken` is a runtime dependency of `langchain-openai` for token
counting but is not always installed transitively.

**Fix:**
```bash
pip install tiktoken>=0.7.0
```

---

## Issue 4: FAISS on Apple Silicon (M1/M2/M3/M4)

**Symptom:** `faiss-cpu` installation fails with compiler errors.

**Cause:** Pre-built wheels may not exist for `arm64` at all versions.

**Fix:**
```bash
# Option A: Use conda (recommended for Apple Silicon)
conda install -c conda-forge faiss-cpu=1.8.0

# Option B: Install from source
pip install faiss-cpu==1.8.0 --no-binary faiss-cpu
```

---

## Issue 5: `getpass` Hangs in Non-Interactive Environment

**Symptom:** Notebook cell hangs indefinitely when running in CI/CD, Docker,
or headless Jupyter.

**Cause:** `getpass.getpass()` blocks waiting for TTY input when no TTY exists.

**Fix:** Set the environment variable before launching:
```bash
export OPENAI_API_KEY="your-key"  # or leave empty for simulation
jupyter notebook
```
The `get_api_key()` function checks `os.getenv` first and only falls through
to `getpass` if the environment variable is absent.

---

## Issue 6: `langchain-core` Version Mismatch

**Symptom:** `pydantic` validation errors or `TypeError` in LangChain internals.

**Cause:** Mixing `langchain-core` 0.2.x with `langchain` 0.3.x (or vice versa).

**Fix:** Install all LangChain packages at compatible versions:
```bash
pip install langchain==0.2.16 langchain-core==0.2.38 langchain-community==0.2.16 langchain-openai==0.1.23
```

---

## Issue 7: Jupyter Kernel Not Showing Python Environment

**Symptom:** Notebook opens but kernel shows wrong Python or missing packages.

**Fix:**
```bash
pip install ipykernel
python -m ipykernel install --user --name=chapter10 --display-name="Chapter 10 (Python 3.x)"
```
Then select the "Chapter 10" kernel in Jupyter.
