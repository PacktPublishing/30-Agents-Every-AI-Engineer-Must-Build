# Troubleshooting Guide — Chapter 14

**Book:** *30 Agents Every AI Engineer Must Build* — Imran Ahmad (Packt Publishing)
**Chapter:** 14 — Financial and Legal Domain Agents

This guide covers the 10 most common issues you may encounter when setting up
and running the Chapter 14 notebook.

---

## T1: LangChain / LangGraph Version Conflicts

**Symptom:** `ImportError: cannot import name 'create_react_agent' from 'langgraph.prebuilt'`
or `AttributeError: module 'langgraph' has no attribute 'StateGraph'`

**Cause:** LangChain and LangGraph have tightly coupled version dependencies. Installing
mismatched versions breaks imports.

**Fix:**
```bash
pip install --force-reinstall \
    langchain==0.2.16 \
    langchain-openai==0.1.23 \
    langchain-community==0.2.16 \
    langgraph==0.2.28
```

If you are using a newer LangChain (0.3.x+), note that the `langchain-community` package
was restructured. Either downgrade to the pinned versions above, or consult the
LangChain 0.3 migration guide at https://python.langchain.com/docs/versions/

---

## T2: Pydantic V1 vs V2 Conflicts

**Symptom:** `pydantic.errors.PydanticUserError: If you use @root_validator...`
or `TypeError: BaseModel.__init_subclass__() takes no keyword arguments`

**Cause:** LangChain 0.2.x requires Pydantic V2 but some community packages may
still use V1-style validators.

**Fix:**
```bash
pip install pydantic==2.8.2
```

If a community package forces V1, add a bridge:
```bash
pip install langchain-core[pydantic-v1-compat]
```

---

## T3: yfinance Returns Empty Data

**Symptom:** `ticker.info` returns an empty dict or `ticker.history()` returns an
empty DataFrame.

**Cause:** Yahoo Finance periodically changes its API structure. The `yfinance` library
depends on web scraping, which can break without notice.

**Fix:**
1. Update yfinance: `pip install --upgrade yfinance`
2. If still failing, the notebook's Simulation Mode provides identical
   functionality using `MOCK_STOCK_DATA` and `generate_mock_price_history()`
   from `mock_data.py`.
3. For persistent issues, check https://github.com/ranaroussi/yfinance/issues

---

## T4: Finnhub API Rate Limits

**Symptom:** `finnhub.exceptions.FinnhubAPIException: API limit reached`

**Cause:** Finnhub free tier allows 60 API calls per minute.

**Fix:**
1. Add a delay between calls: `import time; time.sleep(1)`
2. Or run in Simulation Mode (leave `FINNHUB_API_KEY` empty in `.env`)
3. The `@graceful_fallback` decorator will catch rate limit errors and
   return mock data automatically.

---

## T5: Tavily API Key Not Recognized

**Symptom:** `tavily.exceptions.InvalidAPIKeyError`

**Cause:** Tavily requires a separate API key from https://tavily.com

**Fix:**
1. Sign up at https://tavily.com and get a free API key
2. Add to `.env`: `TAVILY_API_KEY=tvly-xxxxx`
3. Or leave blank to use Simulation Mode with `MOCK_TAVILY_NEWS`

---

## T6: NumPy Compatibility with Python 3.12+

**Symptom:** `RuntimeError: module compiled against API version...`

**Cause:** NumPy 1.26.4 may not have pre-built wheels for Python 3.13+

**Fix:**
```bash
pip install numpy>=1.26.4,<2.0
```

If using Python 3.13+, you may need NumPy 2.x:
```bash
pip install numpy>=2.0
```

Note: NumPy 2.0 changes some default behaviors. The code in this repository
uses only basic NumPy operations (std, sqrt, percentile, cumprod, cummax)
that are stable across versions.

---

## T7: Jupyter Kernel Not Finding Installed Packages

**Symptom:** `ModuleNotFoundError` in Jupyter despite `pip install` succeeding

**Cause:** Jupyter may be running a different Python kernel than the one
where packages were installed.

**Fix:**
```bash
# Ensure ipykernel is installed in your environment
pip install ipykernel

# Register the environment as a Jupyter kernel
python -m ipykernel install --user --name=chapter14 --display-name="Chapter 14"

# Then select "Chapter 14" as your kernel in Jupyter
```

---

## T8: Windows-Specific: ANSI Color Codes Not Displaying

**Symptom:** Color-coded log output shows raw escape codes like `\033[94m`

**Cause:** Windows Command Prompt does not support ANSI escape codes by default.

**Fix:**
The `ColorLogger` class in `mock_llm.py` uses standard ANSI codes. On Windows:
1. Use Windows Terminal (supports ANSI natively)
2. Or run in VS Code's integrated terminal
3. Or add to the top of the notebook:
```python
import os
os.system('')  # Enables ANSI on Windows cmd
```

---

## T9: OpenAI API — Model Not Found

**Symptom:** `openai.NotFoundError: model 'gpt-4o-mini-2024-07-18' not found`

**Cause:** The specific model snapshot may be deprecated. OpenAI periodically
retires dated model versions.

**Fix:**
Replace the model string with the current equivalent:
```python
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
```

Or use Simulation Mode (leave `OPENAI_API_KEY` empty) to avoid model
availability issues entirely.

---

## T10: Memory / Large Context Issues

**Symptom:** Notebook kernel crashes or becomes unresponsive during the
Legal Knowledge Base section.

**Cause:** The `MockVectorStore` stores embeddings in memory. With large
numbers of ingested cases, memory usage can spike.

**Fix:**
1. Restart the kernel and run cells sequentially
2. The mock dataset contains only 6 cases — if you extend it, keep
   the in-memory store under ~1000 documents
3. For production use, switch to a proper vector database
   (Pinecone, Weaviate, ChromaDB)

---

## Still Having Issues?

If your issue is not covered above:

1. **Check the ServiceConfig dashboard** — Run the first notebook cell and verify
   which services are LIVE vs SIMULATED.
2. **Review the `@graceful_fallback` logs** — RED log messages show caught exceptions
   with section references for traceability.
3. **Try Simulation Mode first** — Leave all API keys blank in `.env` to isolate
   whether the issue is environment-related or API-related.
4. **Verify dependency versions** — Run `pip list | grep -E "langchain|langgraph|pydantic|numpy"`
   and compare against `requirements.txt`.

---

*Book: 30 Agents Every AI Engineer Must Build — Imran Ahmad (Packt Publishing)*
*Chapter: 14 — Financial and Legal Domain Agents*
