# Troubleshooting Guide

**Chapter 8 — Data Analysis and Reasoning Agents**
**Book:** *Agents* by Imran Ahmad (Packt, 2026)

---

## 7.1 — `ModuleNotFoundError: No module named 'openai'`

**Cause:** The `openai` package is not installed.

**Fix:**
```bash
pip install openai>=1.30.0
```
If you do not have an API key, the notebook runs in Simulation Mode automatically. You still need the package installed for import resolution.

---

## 7.2 — `AuthenticationError` from OpenAI

**Cause:** API key is invalid, expired, or has insufficient credits.

**Fix:**
1. Verify your key at https://platform.openai.com/api-keys
2. Ensure `.env` contains: `OPENAI_API_KEY=sk-...`
3. Or simply press Enter at the `getpass` prompt to enter Simulation Mode.

---

## 7.3 — `ImportError: cannot import name 'OpenAI' from 'openai'`

**Cause:** You have openai < 1.0 installed (the legacy SDK).

**Fix:**
```bash
pip install --upgrade openai>=1.30.0
```

---

## 7.4 — BART-MNLI Model Fails to Download

**Cause:** No internet, firewall, or disk space < 2 GB.

**Fix:** The notebook automatically falls back to precomputed NLI scores. No action needed. If you want live inference:
```bash
pip install transformers torch
python -c "from transformers import AutoModel; AutoModel.from_pretrained('facebook/bart-large-mnli')"
```

---

## 7.5 — `numpy` / `pandas` Version Conflict

**Cause:** numpy 2.x incompatibility with older pandas or statsmodels.

**Fix:**
```bash
pip install "numpy>=1.26.0,<2.0.0" "pandas>=2.2.0" "statsmodels>=0.14.0"
```
Or use a virtual environment:
```bash
python -m venv ch08-env
source ch08-env/bin/activate  # Linux/Mac
ch08-env\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## 7.6 — `statsmodels` ImportError on Apple Silicon

**Cause:** Pre-built wheels may not be available for ARM64.

**Fix:**
```bash
pip install --no-binary statsmodels statsmodels
```
This compiles from source (requires Xcode command line tools).

---

## 7.7 — Jupyter Kernel Not Found

**Cause:** The virtual environment kernel is not registered with Jupyter.

**Fix:**
```bash
pip install ipykernel
python -m ipykernel install --user --name=ch08-agents --display-name "Ch08 Agents"
```
Then select "Ch08 Agents" as the kernel in Jupyter.

---

## 7.8 — Color Codes Appear as Raw `\033[...` Text

**Cause:** Your terminal or notebook frontend does not support ANSI escape codes.

**Fix:** Use Jupyter Notebook, JupyterLab, or VS Code (all support ANSI). If using a plain-text logger, set the environment variable:
```bash
export CH08_NO_COLOR=1
```
The `color_logger.py` module checks for this and strips ANSI codes when set.

---

## 7.9 — `dotenv` Not Found but `.env` File Exists

**Cause:** `python-dotenv` is not installed. The `.env` file alone does nothing.

**Fix:**
```bash
pip install python-dotenv
```
The notebook's Tier 2 fallback (`os.getenv`) still works if the key is set as a system environment variable.
