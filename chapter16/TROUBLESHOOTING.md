# TROUBLESHOOTING.md — Chapter 16 Dependency Resolutions

**Author:** Imran Ahmad
**Ref:** Chapter 16 — Embodied and Physical World Agents, §Technical requirements (p. 2)

---

## Issue 1: `langchain` / `langchain-core` Version Mismatch

**Symptom:** `ImportError: cannot import name 'create_react_agent' from 'langgraph.prebuilt'`

**Cause:** `langgraph==0.1.4` requires `langchain-core>=0.2.38`. If pip resolves a
lower version, the import fails.

**Fix:**
```bash
pip install langchain-core>=0.2.38,<0.3.0
```

---

## Issue 2: `pydantic` V1 vs V2 Conflict

**Symptom:** `PydanticUserError: If you use @validator, you must use pydantic v1`

**Cause:** LangChain 0.2.x internally bridges pydantic v1 and v2. Some older
LangChain extensions still use v1-style validators.

**Fix:** The book pins `pydantic==2.8.2`. If errors persist:
```bash
pip install pydantic==2.8.2 pydantic-settings>=2.0
```

---

## Issue 3: `openai` SDK Breaking Changes

**Symptom:** `AttributeError: module 'openai' has no attribute 'ChatCompletion'`

**Cause:** `openai>=1.0.0` replaced the old `openai.ChatCompletion` API with
`openai.OpenAI().chat.completions.create()`. The book uses `openai==1.40.0`
which follows the new pattern. Ensure no legacy code is imported.

**Fix:** Verify version:
```bash
pip show openai  # Should show 1.40.0
```

---

## Issue 4: Jupyter Kernel Does Not See Installed Packages

**Symptom:** `ModuleNotFoundError: No module named 'langchain'` despite pip
install succeeding.

**Cause:** Jupyter may use a different Python environment than your terminal.

**Fix:**
```bash
python -m ipykernel install --user --name=ch16-agents
# Then select 'ch16-agents' kernel in Jupyter
```

---

## Issue 5: `langgraph` Import Errors on Apple Silicon (M1/M2/M3/M4)

**Symptom:** Segfault or `ImportError` when importing langgraph on macOS ARM.

**Cause:** Some native dependencies are not yet built for ARM64.

**Fix:**
```bash
# Force x86_64 via Rosetta
arch -x86_64 pip install langgraph==0.1.4
```

---

## Issue 6: `python-dotenv` Not Loading `.env` File

**Symptom:** `OPENAI_API_KEY` is `None` despite `.env` file existing.

**Cause:** `load_dotenv()` searches from the current working directory upward.
If Jupyter's CWD differs from the repo root, it won't find `.env`.

**Fix:**
```python
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).parent / ".env")
# Or in notebook:
load_dotenv("path/to/chapter16-embodied-agents/.env")
```

---

## Issue 7: Simulation Mode Activates Unexpectedly

**Symptom:** Yellow `[SIMULATION]` log appears even though you have an API key.

**Cause:** `.env` file may have a trailing space, quotes around the value, or
a wrong variable name.

**Fix:** Verify `.env` contents:
```
# Correct:
OPENAI_API_KEY=sk-abc123...

# Wrong (trailing space, quotes, or wrong name):
OPENAI_API_KEY = sk-abc123...
OPENAI_API_KEY="sk-abc123..."
OPENAI_KEY=sk-abc123...
```
