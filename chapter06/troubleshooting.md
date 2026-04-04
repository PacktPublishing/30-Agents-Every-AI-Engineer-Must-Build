# Troubleshooting Guide — Chapter 6: Information Retrieval and Knowledge Agents

**Book:** AI Agents (Packt, 2026)
**Author:** Imran Ahmad

---

## 1. FAISS Installation Failures

**Symptom:** `pip install faiss-cpu` fails with build errors on Apple Silicon or Windows.

**Resolution:**
- **macOS (Apple Silicon):** Use `conda install -c conda-forge faiss-cpu` instead of pip. The conda package includes pre-built ARM64 binaries.
- **Windows:** Ensure Visual C++ Build Tools 2022 are installed. Alternatively: `conda install -c conda-forge faiss-cpu`.
- **Linux:** `pip install faiss-cpu` should work. If not, install `libopenblas-dev` first: `sudo apt-get install libopenblas-dev`.

---

## 2. Tesseract Not Found

**Symptom:** `pytesseract.TesseractNotFoundError` — Tesseract is not installed or not in PATH.

**Resolution:**
- **macOS:** `brew install tesseract`
- **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr`
- **Windows:** Download installer from https://github.com/UB-Mannheim/tesseract/wiki. Add install directory to PATH.
- **Verification:** Run `tesseract --version` in terminal.
- **Notebook workaround:** If Tesseract cannot be installed, the notebook automatically falls back to `MockOCR` output with a clear `[ERROR]` log message. No code changes needed.

---

## 3. `pdf2image` Requires Poppler

**Symptom:** `pdf2image.exceptions.PDFInfoNotInstalledError`

**Resolution:**
- **macOS:** `brew install poppler`
- **Ubuntu/Debian:** `sudo apt-get install poppler-utils`
- **Windows:** Download poppler for Windows, extract, add `bin/` to PATH.
- **Notebook workaround:** The Document Intelligence section generates a synthetic PNG invoice directly (bypassing PDF conversion), so Poppler is only needed if you want to process your own PDFs.

---

## 4. `sentence-transformers` Model Download Hangs or Fails

**Symptom:** First run of `SentenceTransformer("all-MiniLM-L6-v2")` stalls or throws a connection error.

**Resolution:**
- Ensure internet connectivity for first run (model is ~80MB download).
- **Behind corporate proxy:** Set `HTTPS_PROXY` environment variable.
- **Offline environment:** Pre-download the model: `python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"` on a connected machine, then copy `~/.cache/huggingface/` to the target machine.
- **Notebook workaround:** If the model fails to load, the Scientific Research section uses pre-computed mock cluster assignments instead.

---

## 5. NumPy 2.x Compatibility Issues

**Symptom:** `AttributeError` or `ImportError` related to NumPy internals after upgrading.

**Resolution:**
- Pin NumPy below 2.1: `pip install "numpy>=1.26.0,<2.1"`
- This ensures compatibility with FAISS, scikit-learn, and sentence-transformers as of early 2026.

---

## 6. LangChain Import Errors / Deprecation Warnings

**Symptom:** `ImportError: cannot import name 'X' from 'langchain'`

**Resolution:**
- LangChain reorganized its package structure in 2025. This repo uses the split packages:
  - `langchain` (core)
  - `langchain-openai` (OpenAI integrations)
  - `langchain-community` (FAISS and other community integrations)
  - `langchain-text-splitters` (text splitting utilities)
- If you see import errors, ensure all four packages are installed and at version `>=0.3.0`.

---

## 7. `rapidfuzz` vs. `fuzzywuzzy`

**Symptom:** Import error if `rapidfuzz` is not installed but `fuzzywuzzy` is.

**Resolution:**
- This repo uses `rapidfuzz` (MIT-licensed, faster). Do not substitute `fuzzywuzzy` without changing import statements.
- Install: `pip install rapidfuzz>=3.10.0`

---

## 8. Jupyter Kernel Not Found

**Symptom:** Notebook opens but shows "Kernel not found."

**Resolution:**
- Install the kernel: `python -m ipykernel install --user --name=ch06-agents`
- Select `ch06-agents` as the kernel in Jupyter.
