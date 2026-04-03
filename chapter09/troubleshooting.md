# Troubleshooting Guide — Chapter 9 Repository
# Book: "Agents" by Imran Ahmad (Packt, 2026)

## Quick Diagnostics

Before diving into specific issues, run this diagnostic cell
in the notebook:

```python
import sys
print(f"Python: {sys.version}")

import pydantic; print(f"Pydantic: {pydantic.__version__}")
import langgraph; print(f"LangGraph: {langgraph.__version__}")
from dotenv import load_dotenv; print("python-dotenv: OK")

from src.utils import ColorLog
ColorLog.info("Blue test")
ColorLog.success("Green test")
ColorLog.error("Red test")
```

If any import fails, see the relevant section below.


## Issue 1: Pydantic V1 vs V2 Conflict

SYMPTOMS:
  - "PydanticUserError: Field 'model_fields' ... is not supported"
  - "ConfigDict is not defined"
  - LangChain imports fail with Pydantic errors

CAUSE:
  LangChain historically depended on Pydantic V1. As of 2025-2026,
  langchain-core >=0.3.x requires Pydantic V2. Older LangChain
  installations may pin Pydantic V1.

RESOLUTION:
  pip install --upgrade langchain-core langchain-openai pydantic

  Verify: python -c "import pydantic; print(pydantic.__version__)"
  Expected: 2.7.x or higher


## Issue 2: LangGraph Import Errors

SYMPTOMS:
  - "ModuleNotFoundError: No module named 'langgraph'"
  - "ImportError: cannot import name 'StateGraph'"

CAUSE:
  LangGraph is a separate package from LangChain. It is not
  included in a base langchain install.

RESOLUTION:
  pip install langgraph

  If you see version conflicts with langchain-core:
  pip install langgraph langchain-core --upgrade


## Issue 3: Colors Not Displaying

SYMPTOMS:
  - Output shows raw escape codes: \033[94m[INFO]\033[0m
  - No color differentiation in logs

CAUSE:
  Some Jupyter environments or terminals do not support ANSI
  escape codes. Google Colab and VS Code terminals support them.
  JupyterLab classic may strip them.

RESOLUTION:
  Option A — Use a terminal-friendly environment (VS Code, Colab).

  Option B — The notebook includes a fallback. If ANSI codes are
  not rendering, set this environment variable before running:

    import os
    os.environ["NO_COLOR"] = "1"

  This switches ColorLog to plain-text prefixes: [INFO], [SUCCESS],
  [HANDLED ERROR] without escape codes.


## Issue 4: LangChain / LangGraph Version Mismatch

SYMPTOMS:
  - "TypeError: StateGraph.__init__() got an unexpected keyword"
  - "AttributeError: 'CompiledGraph' object has no attribute 'invoke'"

CAUSE:
  langgraph and langchain-core must be version-compatible.
  Mixing 0.2.x langgraph with 0.3.x langchain-core causes
  API signature mismatches.

RESOLUTION:
  Install compatible versions together:
  pip install "langgraph>=0.3.0,<0.4.0" "langchain-core>=0.3.0,<0.4.0"


## Issue 5: API Key Not Detected

SYMPTOMS:
  - Notebook enters Simulation Mode even though you set a key
  - "Enter OPENAI_API_KEY (or press Enter for Simulation Mode):"
    appears unexpectedly

CAUSE:
  The .env file is not in the correct location, or the variable
  name does not match.

RESOLUTION:
  1. Copy .env.template to .env in the repository root.
  2. Add your key: OPENAI_API_KEY=sk-your-key-here
  3. Ensure no leading/trailing spaces around the = sign.
  4. Restart the Jupyter kernel after creating/editing .env.

  Verify: python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(bool(os.getenv('OPENAI_API_KEY')))"


## Issue 6: Notebook Execution Hangs or Times Out

SYMPTOMS:
  - Cell appears to run indefinitely
  - No output, no error

CAUSE:
  In Live Mode, LLM API calls may timeout due to rate limiting
  or network issues. The @fail_gracefully decorator should catch
  these, but network-level hangs may not raise Python exceptions
  immediately.

RESOLUTION:
  Option A — Run in Simulation Mode (leave .env blank). All code
  paths execute instantly with mock data.

  Option B — If using Live Mode, set a timeout in Cell 3:
    llm = ChatOpenAI(
        model="gpt-4o",
        api_key=api_key,
        temperature=0.2,
        request_timeout=30
    )


## Issue 7: Kernel Dies During LangGraph Execution

SYMPTOMS:
  - "Kernel Restarting" message
  - Cell execution abruptly stops

CAUSE:
  Memory exhaustion from large state objects or infinite
  refinement loops. The iteration limit (default: 3) should
  prevent this, but corrupted state can bypass it.

RESOLUTION:
  1. Restart kernel and run from Cell 1.
  2. If persists, check that conditional edges in the StateGraph
     enforce iteration < 3 (search for "iterations < 3" in the
     notebook).
  3. Reduce iteration limit to 2 for memory-constrained
     environments.


## Issue 8: typing_extensions Incompatibility

SYMPTOMS:
  - "ImportError: cannot import name 'TypedDict' from 'typing'"
  - "ImportError: cannot import name 'Annotated'"

CAUSE:
  Python 3.9 lacks native TypedDict and Annotated support.
  The repository requires Python 3.10+.

RESOLUTION:
  Upgrade to Python 3.10 or higher.
  Verify: python --version

  If stuck on 3.9:
  pip install typing-extensions>=4.9.0
  Then change imports in state_models.py:
    from typing_extensions import TypedDict, Annotated
