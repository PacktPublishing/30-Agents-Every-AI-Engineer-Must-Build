# Troubleshooting Guide

**Chapter 7: Tool Manipulation and Orchestration Agents**
**Book:** *Agents* by Imran Ahmad (Packt, 2026 — B34135)

---

## 1. Dependency Conflicts

| Symptom | Cause | Resolution |
|:---|:---|:---|
| `ImportError: cannot import name 'DataFrame'` | pandas not installed or wrong version | `pip install pandas>=2.2` |
| `ModuleNotFoundError: No module named 'dotenv'` | Package name mismatch — `dotenv` and `python-dotenv` are different packages | `pip uninstall dotenv && pip install python-dotenv` |
| `TypeError: Client.__init__() got unexpected keyword` | openai < 1.0 installed (Live Mode only) | `pip install openai>=1.60` |
| Matplotlib plot appears blank in notebook | Backend mismatch | Add `%matplotlib inline` in the Section 0 Setup cell |
| `Permission denied` writing to `outputs/` | Directory permissions or missing directory | `chmod 755 outputs/` or create it: `mkdir -p outputs` |
| `JSONDecodeError` from MockLLM | Prompt triggered the DEFAULT route instead of the intended route | Check your prompt keywords against the routing table in `helpers/mock_llm.py` (Routes R1–R6) |

---

## 2. Environment Issues

| Symptom | Cause | Resolution |
|:---|:---|:---|
| Notebook runs in Simulation Mode despite `.env` having a key | `.env` file not loaded | Ensure `load_dotenv()` is called before `os.getenv()` in Section 0. Verify `.env` is in the repository root (not inside `helpers/` or `data/`). |
| `getpass` prompt hangs in Colab or CI | Non-interactive environment cannot display `input()` prompts | Set `INTERACTIVE_MODE = False` in the Section 0 Setup cell |
| Colors not showing in terminal output | Non-ANSI terminal (e.g., legacy `cmd.exe`) | Set `ENABLE_COLOR = False` in `helpers/color_logger.py` |
| Colors show raw escape codes in Jupyter | Older notebook version without ANSI support | Upgrade: `pip install notebook>=7.2` |

---

## 3. Runtime Issues

| Symptom | Cause | Resolution |
|:---|:---|:---|
| `data_viz_agent` returns no chart | `parse_query` returned `None` — the query was not understood | The query must contain a metric keyword (`spend`, `clicks`, or `conversions`) **and** a dimension keyword (`by campaign`, `which campaign`, `over time`, or `trend`). Example: *"Show me the trend of clicks over time."* |
| HITL cell blocks forever waiting for input | `INTERACTIVE_MODE = True` in a non-interactive environment | Set `INTERACTIVE_MODE = False` in the Section 0 Setup cell. The notebook will auto-approve after a 2-second delay. |
| Insurance claims all auto-approve (no escalation) | Confidence threshold is too low or test data does not trigger high-risk path | Verify the classifier returns `confidence_score < 0.85` for escalation cases. Check that CLM-5099 uses the R6 mock route (`high_risk` keyword). |
| `AgentError` not defined | Missing custom exception class | Ensure the Section 0 Setup cell defines `class AgentError(Exception): pass` before any workflow cells. |
| Charts saved but not visible in notebook | Missing `%matplotlib inline` magic or `plt.show()` not called | Add `%matplotlib inline` in Section 0. Alternatively, call `plt.show()` after each plot. |

---

## 4. Platform-Specific Notes

| Platform | Notes |
|:---|:---|
| **Google Colab** | Set `INTERACTIVE_MODE = False` to avoid blocking `input()` prompts. Install dependencies with `!pip install -r requirements.txt` in a code cell. Upload `.env` via the Colab file panel or set environment variables directly. |
| **VS Code Jupyter** | Works out of the box. Select the correct Python kernel from the kernel picker. ANSI colors render natively. |
| **JupyterLab** | Color output works natively. No special configuration needed. |
| **GitHub Codespaces** | Clone and run directly. Set your API key via Codespace Secrets (`Settings > Secrets > Codespaces`) to enable Live Mode. |
| **Windows** | ANSI colors work in Windows Terminal and VS Code integrated terminal. Legacy `cmd.exe` may display raw escape codes — install `colorama` or use Windows Terminal instead. |

---

## Quick Diagnostic Checklist

If something is not working, run through these checks in order:

1. **Python version:** Verify `python --version` shows 3.11 or higher.
2. **Dependencies:** Run `pip install -r requirements.txt` in your active environment.
3. **Working directory:** Ensure you launch the notebook from the repository root so relative paths (`data/`, `helpers/`, `outputs/`) resolve correctly.
4. **`.env` location:** The `.env` file must be in the same directory as the notebook, not inside a subdirectory.
5. **Kernel:** Confirm the Jupyter kernel matches the environment where you installed dependencies.
6. **Run order:** Execute cells top-to-bottom. Section 0 must run first — it defines shared imports, configuration flags, and the `AgentError` exception class used by later sections.

---

*For additional support, refer to the book text or open an issue in the repository.*
