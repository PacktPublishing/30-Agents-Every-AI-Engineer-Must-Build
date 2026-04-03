# Troubleshooting Guide — Chapter 17

**Book:** *AI Agents* by Imran Ahmad (Packt, 2025)
**Chapter:** 17 — Epilogue: The Future of Intelligent Agents

---

## 1. SciPy Import Error (KS Test)

**Symptom:** `ModuleNotFoundError: No module named 'scipy'`
**Context:** Simulation 3 (Ethical Circuit Breaker) uses `scipy.stats.ks_2samp`
**Fix:**
```bash
pip install scipy>=1.13.0
```

## 2. NumPy Version Conflict

**Symptom:** `AttributeError` or `ImportError` related to NumPy internals
**Context:** NumPy 2.x introduced breaking changes for downstream packages
**Fix:**
```bash
pip install numpy>=1.26.0,<2.1.0
```

## 3. python-dotenv Not Found

**Symptom:** `ModuleNotFoundError: No module named 'dotenv'`
**Context:** Environment detection in resilience.py
**Fix:**
```bash
pip install python-dotenv>=1.0.0
```
**Note:** The code handles this gracefully — it will fall back to `os.getenv` directly.

## 4. Jupyter Kernel Mismatch

**Symptom:** Imports fail even though packages are installed
**Context:** Jupyter may use a different Python than your terminal
**Fix:**
```bash
python -m ipykernel install --user --name=ch17-agents
# Then select 'ch17-agents' kernel in Jupyter
```

## 5. ANSI Color Codes Not Rendering

**Symptom:** Raw escape sequences like `\033[94m` appear in output
**Context:** Some Jupyter environments strip ANSI codes
**Fix:** Use JupyterLab (recommended) or install:
```bash
pip install ipython>=8.0
```
JupyterLab renders ANSI colors natively. Classic Notebook may require the
`ansi_up` extension.

## 6. Random Seed Reproducibility

**Symptom:** Output values differ from expected results in this guide
**Context:** `random.seed(42)` and `np.random.seed(42)` must be set before imports
**Fix:** Restart kernel and run cells sequentially from the top. Do not run cells
out of order.

## 7. getpass Blocking in Non-Interactive Environments

**Symptom:** Notebook hangs waiting for input
**Context:** getpass fallback in automated/CI environments
**Fix:** Set the environment variable directly:
```bash
export OPENAI_API_KEY=sk-your-key-here
```
Or create a `.env` file in the repository root.

## 8. Memory Usage with Large Simulations

**Symptom:** Kernel crashes on memory-constrained environments
**Context:** AgentSocietySimulator with many rounds or large populations
**Fix:** Reduce `rounds` parameter in `run_degroot_convergence()` from 20 to 10.
The convergence behavior is visible within 10 rounds.

---

## General Advice

1. Always use a virtual environment (`python -m venv venv`)
2. Run `pip install -r requirements.txt` before launching the notebook
3. If all else fails, restart the kernel and run all cells from the beginning
4. File issues at the GitHub repository with your Python version and error traceback

**Author:** Imran Ahmad | **Book:** AI Agents (Packt, 2025)
