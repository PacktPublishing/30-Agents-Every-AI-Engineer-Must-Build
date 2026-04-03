# Troubleshooting Guide
# Chapter 1: Foundations of Agent Engineering
# Book: "AI Agents" by Imran Ahmad (Packt, 2026)

## Quick Fixes

### "ModuleNotFoundError: No module named 'src'"
**Cause:** Jupyter kernel's working directory is not the repository root.
**Fix:** Add this to the first code cell:
```python
import sys, os
sys.path.insert(0, os.path.dirname(os.getcwd()))
```
Or restart the kernel from the repository root directory.

### "ModuleNotFoundError: No module named 'openai'"
**Cause:** The `openai` package is not installed in the active Python environment.
**Fix:**
```bash
pip install openai>=1.52.0
```
**Note:** This is only required for LIVE mode. The notebook runs fully
in SIMULATION mode without it.

### "ModuleNotFoundError: No module named 'dotenv'"
**Cause:** `python-dotenv` not installed.
**Fix:**
```bash
pip install python-dotenv>=1.0.1
```
**Note:** The notebook handles this gracefully with a [WARNING] log and
falls through to os.getenv / getpass detection.

### ANSI colors not rendering (no colors in output)
**Cause:** Some Jupyter frontends (JupyterLab <4.0, some VS Code versions)
strip ANSI escape codes from print output.
**Fixes (choose one):**
- Upgrade to JupyterLab 4.0+ or Jupyter Notebook 7+
- Install `ansi_escape` extension: `jupyter labextension install @juno/ansi-escape`
- For VS Code: enable "Terminal > Integrated: ANSI Colors" in settings

### "ConnectionError: MockLLM: Simulated API timeout"
**Cause:** This is intentional! The MockLLM's `failure_rate` parameter is
set above 0.0, simulating API failures to demonstrate the resilience layer.
**Fix:** This is expected behavior in the Resilience Demo cell. The
@graceful_fallback decorator catches this and returns a fallback value.
No action needed.

### "openai.AuthenticationError: Incorrect API key"
**Cause:** An invalid key was provided in .env or via getpass.
**Fix:**
1. Verify your key at https://platform.openai.com/api-keys
2. Ensure .env contains: `OPENAI_API_KEY=sk-...`
3. Or delete .env to run in SIMULATION mode instead.

### Python version compatibility
**Minimum:** Python 3.10+
**Recommended:** Python 3.11 or 3.12
**Known issue:** Python 3.13 may have compatibility issues with some
packages as of early 2026. If you encounter issues, use Python 3.12.
**Fix:** Use pyenv or conda to manage Python versions:
```bash
pyenv install 3.12.7
pyenv local 3.12.7
```

### pip dependency resolver conflicts
**Cause:** Conflicting version requirements between packages.
**Fix:** Create a fresh virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### Jupyter kernel not finding installed packages
**Cause:** Jupyter is using a different Python kernel than where packages
were installed.
**Fix:**
```bash
pip install ipykernel
python -m ipykernel install --user --name=ch01-agents
```
Then select the "ch01-agents" kernel in Jupyter.

## Getting Help

If you encounter an issue not listed here:
1. Check the GitHub Issues page for this repository
2. Ensure you are using the recommended Python version (3.11+)
3. Try running in a fresh virtual environment
4. Open a new issue with your Python version, OS, and the full error traceback
