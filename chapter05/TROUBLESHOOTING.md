# Troubleshooting Guide — Chapter 05

**Book:** *30 Agents Every AI Engineer Must Build*
**Author:** Imran Ahmad
**Publisher:** Packt Publishing

This guide covers common issues when running the Chapter 5 notebook
and supporting modules. Solutions are organized by category.

---

## 1. Dependency Conflicts

| Problem | Symptom | Resolution |
|---|---|---|
| `python-dotenv` version clash | `ImportError` or `AttributeError` on `load_dotenv` | Pin `python-dotenv>=1.1.0`. If conflict with another package: `pip install python-dotenv --force-reinstall` |
| Jupyter kernel cannot find local modules | `ModuleNotFoundError` for `mock_llm` or `color_logger` | Run the notebook from the `Chapter-05/` directory. The notebook includes `sys.path.insert(0, '.')` as a safety fallback |
| `openai` SDK v1 vs v0 incompatibility | `openai.ChatCompletion` no longer exists | This repo targets `openai>=1.60.0` (the v1+ API). Use `client.chat.completions.create()`, not the legacy `openai.ChatCompletion.create()` |
| `chromadb` SQLite version error on Linux | `RuntimeError: sqlite3 version too old` | Install `pysqlite3-binary`: `pip install pysqlite3-binary` and add the override per the ChromaDB documentation |
| ANSI colors not rendering in Jupyter | Raw escape codes visible as text | Ensure you are running in Jupyter Notebook, JupyterLab, or VS Code (all support ANSI). Google Colab also works natively |
| `getpass` hangs in non-interactive environments | Cell appears frozen waiting for input | The environment detection cell includes a timeout fallback. In CI/CD or non-interactive mode, provide an `.env` file or leave blank for mock mode |
| Python 3.9 or lower | `dataclasses` field issues or `\|` union syntax errors | This repo requires **Python 3.10+**. Verify with `python --version`. See Technical Requirements (p. 2) |
| `pip install` permission errors | `Permission denied` on system Python | Always use a virtual environment: `python -m venv .venv && source .venv/bin/activate` |

---

## 2. Runtime Issues

| Problem | Symptom | Resolution |
|---|---|---|
| Mock mode not activating | `log_success("API key detected")` even though you have no key | Check for a stale `.env` file with a leftover key. Delete or empty the `OPENAI_API_KEY=` line |
| Mock responses don't match expected scenario | MockLLM returns `default_fallback` instead of expected scenario | Check that the prompt text contains the required keywords. The keyword router is case-insensitive but requires at least one trigger word. See keyword routing map in `mock_llm.py` |
| `MemoryAugmentedAgent` returns empty memory | `search()` returns `[]` despite seeded data | Ensure `MockVectorDB` was initialized (not `None`). In live mode, verify your vector DB is configured and the collection exists |
| Task DAG execution order looks wrong | Tasks execute out of dependency order | Check `depends_on` lists. The executor resolves dependencies via topological sort. Circular dependencies will raise a `ValueError` (caught by `@fail_gracefully`) |
| `@fail_gracefully` retry delay is slow | Decorator waits during retries | This is by design — exponential backoff (`2^attempt` seconds) prevents cascading failures. For testing, temporarily set `max_retries=0` |

---

## 3. Platform-Specific Notes

| Platform | Notes |
|---|---|
| **macOS (Apple Silicon)** | All dependencies work natively on M1/M2/M3/M4. No special flags needed |
| **Windows (PowerShell)** | Activate venv with `.venv\Scripts\Activate.ps1`. ANSI colors work in Windows Terminal and modern PowerShell |
| **Linux (Ubuntu 22+)** | Standard setup. If using system Python, prefer `python3 -m venv` |
| **Google Colab** | Upload the 3 `.py` files (`color_logger.py`, `resilience.py`, `mock_llm.py`) to the session. Install deps: `!pip install python-dotenv`. ANSI colors work natively |
| **Docker** | Use `python:3.12-slim` base image. Copy all files to `/app/`. Run: `jupyter notebook --ip=0.0.0.0` |

---

## 4. Getting Help

If your issue is not listed above:

1. Check the notebook's color-coded output — error messages include
   chapter references (e.g., `(ref: Section 5.1, p. 14)`) that
   point to the relevant book section.

2. Verify your Python version: `python --version` (must be 3.10+).

3. Verify your working directory: the notebook must be launched from
   the `Chapter-05/` folder.

4. Consult the [main repository](https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build)
   for updates and errata.
