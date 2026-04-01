# Troubleshooting Guide

> Chapter 15: Education and Knowledge Agents
> Book: *30 Agents Every AI Engineer Must Build* by **Imran Ahmad** (Packt Publishing, 2026)

---

## 1. Dependency Conflicts

| Symptom | Root Cause | Resolution |
|---|---|---|
| `pip's dependency resolver` error on `openai` | Conflicting `httpx`/`pydantic` versions | Isolated venv: `python -m venv ch15env && source ch15env/bin/activate && pip install -r requirements.txt` |
| `ImportError: cannot import name 'OpenAI'` | Old `openai` SDK (pre-1.0) installed | `pip install --force-reinstall openai==1.40.0` |
| `numpy` build fails on Apple Silicon | Missing `accelerate` framework | `pip install numpy==1.26.4 --only-binary=:all:` or use conda |
| `networkx` import OK but `get_dependents()` missing | `networkx<3.0` has different API | Verify: `python -c "import networkx; print(networkx.__version__)"` — must be `3.3` |
| `ModuleNotFoundError: No module named 'dotenv'` | Package name mismatch | `pip install python-dotenv==1.0.1` (not `pip install dotenv`) |
| Kernel dies on first cell | Kernel not linked to venv | `python -m ipykernel install --user --name=ch15 --display-name "Ch15 Agents"` |
| `getpass()` hangs in Jupyter | Some environments don't support interactive input | Handled: code catches `EOFError` and falls back to Simulation Mode |
| Key set but still Simulation Mode | `.env` not in notebook directory | Ensure `.env` is co-located with the notebook. Alternative: `export OPENAI_API_KEY=<your-key>` before starting Jupyter |
| `openai.RateLimitError` in Live Mode | API quota exceeded | `@graceful_fallback` catches this automatically and continues with MockLLM |
| `openai.AuthenticationError` | Invalid or expired key | Check at https://platform.openai.com/api-keys. Update `.env`. Restart kernel. |
| All outputs show `[MOCK]` with valid key | `SIMULATION_MODE` set before key loaded | `.env` must exist before Cell 0 runs. If key was set after, restart kernel. |

---

## 2. Platform-Specific Issues

| Platform | Issue | Workaround |
|---|---|---|
| **Windows** | ANSI colors don't render in `cmd.exe` | Use Windows Terminal, VSCode terminal, or add `colorama` to your environment. Jupyter renders ANSI natively. |
| **Google Colab** | No local `.env` support | Use Colab Secrets manager or the `getpass` prompt (Tier 3 in the key resolution chain). Colab supports ANSI color codes natively. |
| **Docker** | `getpass` fails in non-interactive mode | Set key as environment variable: `docker run -e OPENAI_API_KEY=<your-key> ...` or accept Simulation Mode. |
| **Python 3.13+** | `numpy==1.26.4` may lack pre-built wheels | Use `numpy>=2.0.0` or stay on Python 3.12. The notebook's numpy usage is version-agnostic. |

---

## 3. "Runs But Looks Wrong"

| Observation | Likely Cause | Fix |
|---|---|---|
| BKT mastery never increases | `p_transit` too low or `p_guess` too high | Check defaults: `p_transit=0.1`, `p_slip=0.05`, `p_guess=0.2` (Ch.15, pp. 13–15) |
| Planner always returns same objectives | `update_mastery()` not called after BKT update | Ensure the shared `StudentModel` instance is updated after each interaction |
| Consensus never converges | Tolerance too tight for mock responses | Mock responses converge at `tolerance=0.5`. For real LLM, increase `max_rounds` or `tolerance` |
| Placement test uses all 15 items | `se_threshold` too low | Default `0.3` works with the provided item bank. Custom items need discrimination `a >= 1.0` |
| Alex case study doesn't cross 0.85 | BKT parameters modified or steps skipped | Run the full 5-stage sequence without modification. Check that each `bkt_update()` call uses the output of the previous one. |
| Spaced repetition interval never grows | Quality score always below 3 | `update_schedule(quality=4)` or higher triggers interval growth. Quality 0–2 resets to interval=1 (SM-2 algorithm, p. 19). |
| Mock responses look generic | Prompt doesn't match routing keywords | Check `_match_prompt()` rules in `utils/mock_llm.py`. The first two keywords in each rule must appear in the prompt. |

---

## 4. Debug Order

When something goes wrong, follow this diagnostic sequence:

1. **Environment** — Is the virtual environment activated? Is Python 3.10+?
2. **Dependencies** — Does `pip list` show the correct versions from `requirements.txt`?
3. **API Key** — Is `.env` present and co-located with the notebook? Does the key work? (Test: `python -c "from openai import OpenAI; print(OpenAI().models.list())"`)
4. **Code Logic** — Is the notebook running cells in order? Are shared objects (StudentModel, KnowledgeGraph) initialized before use?

---

## 5. Getting Help

- **Book GitHub repository:** https://github.com/PacktPublishing/30-Agents-Every-AI-Engineer-Must-Build
- **Chapter reference:** Chapter 15, pp. 1–40
- **Key cross-references:** Chapter 1 (cognitive loop), Chapter 12 (explainability), Chapter 13 (stochastic decision-making)
