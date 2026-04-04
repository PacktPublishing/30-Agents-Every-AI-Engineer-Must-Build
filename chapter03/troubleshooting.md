# Troubleshooting Guide
## Chapter 3: The Art of Agent Prompting
### Author: Imran Ahmad

This guide addresses the most common dependency conflicts and runtime
issues when setting up the Chapter 3 companion repository.

---

### Issue 1: Pydantic v1 vs. v2 Conflict

**Symptom:** `ImportError: cannot import name 'field_validator' from 'pydantic'`
or `PydanticUserError: 'fields' is not supported in Pydantic v2`.

**Cause:** langchain-core 0.3.x requires Pydantic v2. An older package in your
environment has pinned Pydantic v1.

**Fix:**
```
pip install --upgrade pydantic>=2.9.0
pip install --upgrade langchain-core
```

If the conflict persists, create a fresh virtual environment:
```
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

---

### Issue 2: langchain vs. langchain-core Import Confusion

**Symptom:** `ModuleNotFoundError: No module named 'langchain_core'`

**Cause:** The older `langchain` monolith package (pre-0.1.0) used
`from langchain.schema import ...`. The modern split-package architecture
uses `from langchain_core.messages import AIMessage`.

**Fix:** This repository uses the split-package architecture. Install:
```
pip install langchain-core langchain-openai
```

Do NOT install the monolith `langchain` package unless you need other
components. If you have both installed, the split packages take priority.

---

### Issue 3: ANSI Color Codes Not Rendering

**Symptom:** Log output shows raw escape codes like `\033[94m[INFO]`
instead of colored text.

**Cause:** Your terminal or notebook environment does not support ANSI
escape sequences. Common in some Windows terminals and older Jupyter
versions.

**Fix (Jupyter):** Upgrade Jupyter:
```
pip install --upgrade jupyter ipykernel
```

**Fix (Windows):** Use Windows Terminal (not cmd.exe) or enable ANSI:
```python
import os
os.system("")  # Enables ANSI on Windows cmd
```

**Fix (VS Code):** ANSI colors work by default in VS Code's integrated
terminal and notebook output.

---

### Issue 4: getpass Hangs in Jupyter

**Symptom:** The `getpass.getpass()` call hangs or produces a
`WARNING:getpass:Can not control echo on the terminal` message.

**Cause:** Some Jupyter frontends cannot handle interactive password
input natively.

**Fix:** Skip the interactive fallback by setting your key in `.env`:
```
cp .env.template .env
# Edit .env and paste your API key
# Restart the kernel
```

The code detects `.env` first and only falls back to `getpass` if no
`.env` key is found. If you have no API key at all, Simulation Mode
activates automatically — no input needed.

---

### Issue 5: MockLLM Not Recognized by LangChain Chains

**Symptom:** `TypeError: Expected a Runnable, callable or mapping` when
using `prompt | mock_llm`.

**Cause:** The `MockLLM` class must subclass `BaseChatModel` from
`langchain_core` to be pipe-operator compatible.

**Fix:** Ensure you are importing from this repository's `mock_llm.py`,
not a different mock:
```python
from mock_llm import MockLLM
llm = MockLLM()
# Verify:
from langchain_core.language_models import BaseChatModel
assert isinstance(llm, BaseChatModel)
```

---

### Issue 6: Python Version Incompatibility

**Symptom:** `SyntaxError` on f-strings with `=` sign, or type hint
errors.

**Cause:** This repository requires Python 3.11 or higher.

**Fix:** Check your version:
```
python --version
```

If below 3.11, upgrade Python. We recommend using pyenv:
```
pyenv install 3.11.9
pyenv local 3.11.9
```

---

### Issue 7: OpenAI API Rate Limits or Quota Errors

**Symptom:** `openai.RateLimitError: Rate limit reached` or
`openai.AuthenticationError: Incorrect API key`.

**Cause:** Invalid key, expired key, or free-tier quota exhausted.

**Fix:** The entire notebook runs in Simulation Mode without an API key.
To use Simulation Mode intentionally, simply leave `.env` empty or
delete it. All demos produce meaningful mock output derived from the
chapter content.

---

### Issue 8: Notebook Kernel Dies on Import

**Symptom:** Kernel crashes silently when running the first cell.

**Cause:** Typically a C-extension conflict between numpy, pydantic,
or other compiled packages.

**Fix:**
```
pip install --upgrade --force-reinstall langchain-core pydantic
```

Or use a fresh virtual environment (see Issue 1).
