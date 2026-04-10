# Running with a Local LLM (Ollama)

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

---

Every chapter includes a `__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb` notebook that runs entirely on your machine using [Ollama](https://ollama.com) — no API keys, no cloud calls, no cost. This guide walks you through setup on **Windows**, **macOS**, and **Linux**.

## What You Need

| Requirement | Minimum | Recommended |
|---|---|---|
| **RAM** | 16 GB | 32 GB |
| **Disk** | 15 GB free | 25 GB free |
| **GPU** | Not required (CPU works) | NVIDIA GPU with 8 GB+ VRAM |
| **OS** | Windows 10+, macOS 12+, Linux (glibc 2.31+) | — |

The notebooks use two models:

| Model | Role | Size | Purpose |
|---|---|---|---|
| `deepseek-v2:16b` | LLM (generation) | ~9 GB | Reasoning, answering questions, synthesis |
| `llama3.1:8b` | Embeddings | ~5 GB | Vector embeddings for RAG and similarity search |

---

## Step 1: Install Ollama

### macOS

```bash
# Option A: Direct download
# Download from https://ollama.com/download/mac and drag to Applications

# Option B: Homebrew
brew install ollama
```

After installation, Ollama runs as a background service automatically.

### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Start the service:

```bash
# Systemd (Ubuntu, Debian, Fedora, etc.)
sudo systemctl start ollama
sudo systemctl enable ollama   # auto-start on boot

# Or run manually
ollama serve &
```

### Windows

1. Download the installer from [ollama.com/download/windows](https://ollama.com/download/windows)
2. Run the `.exe` installer and follow the prompts
3. Ollama starts automatically as a background service

Alternatively, with `winget`:

```powershell
winget install Ollama.Ollama
```

---

## Step 2: Pull the Required Models

Open a terminal (or PowerShell on Windows) and run:

```bash
ollama pull deepseek-v2:16b
ollama pull llama3.1:8b
```

This downloads both models. The first pull takes a few minutes depending on your connection.

Verify they are installed:

```bash
ollama list
```

You should see both models listed:

```
NAME               SIZE
deepseek-v2:16b    8.9 GB
llama3.1:8b        4.9 GB
```

---

## Step 3: Verify Ollama is Running

```bash
# Quick health check
curl http://localhost:11434/api/tags
```

You should get a JSON response listing your models. If you get a connection error, start the service:

```bash
# macOS: Ollama runs automatically after install — open the app if needed
# Linux: sudo systemctl start ollama
# Windows: Open "Ollama" from the Start menu, or restart the service
```

Test a quick generation to confirm everything works:

```bash
ollama run deepseek-v2:16b "What is an AI agent? Answer in one sentence."
```

---

## Step 4: Run the Notebook

Navigate to any chapter and open the local LLM notebook:

```bash
cd chapter01   # or any chapter

jupyter notebook *__RUN_LOCAL_OLLAMA_DeepSeek_V2_16B.ipynb
```

The notebook will:
1. Detect that Ollama is running locally
2. Initialize `ChatOllama` with `deepseek-v2:16b` for generation
3. Initialize `OllamaEmbeddings` with `llama3.1:8b` for vector operations
4. Execute all agent tasks locally — no API key needed

If Ollama is not running, the notebook falls back to **Simulation Mode** (MockLLM) automatically.

---

## Performance Tips

### Use GPU acceleration (recommended)

Ollama automatically uses your GPU if available:

- **NVIDIA**: Install [CUDA drivers](https://developer.nvidia.com/cuda-downloads). Ollama detects CUDA automatically.
- **Apple Silicon (M1/M2/M3/M4)**: Metal acceleration is used automatically — no extra setup.
- **AMD (Linux)**: ROCm support is available. See [Ollama GPU docs](https://github.com/ollama/ollama/blob/main/docs/gpu.md).

### Adjust context window

If you encounter truncated responses on long documents:

```bash
# Increase context length (default is 2048)
OLLAMA_NUM_CTX=4096 ollama serve
```

### CPU-only mode

If you have no GPU, Ollama runs on CPU. Expect slower generation (~2-10 tokens/sec on modern CPUs vs. ~30-80 tokens/sec on GPU). The notebooks still work — they just take longer.

### Memory management

If you are low on RAM:

- Close other memory-intensive applications before running
- Use one model at a time — Ollama loads/unloads models dynamically
- The 16B model needs ~10 GB RAM; the 8B model needs ~6 GB

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `connection refused` on port 11434 | Start Ollama: `ollama serve` (Linux), open the app (macOS/Windows) |
| `model not found` | Run `ollama pull deepseek-v2:16b` and `ollama pull llama3.1:8b` |
| Out of memory error | Close other apps, or try a smaller model: `ollama pull deepseek-v2:lite` |
| Very slow generation | Check GPU is being used: `ollama ps` shows VRAM usage. Install CUDA if on NVIDIA. |
| Windows firewall blocks Ollama | Allow `ollama.exe` through Windows Firewall for localhost access |
| `langchain_ollama` import error | Run `pip install langchain-ollama` in your environment |
| Notebook falls back to Simulation | Ollama isn't running or models aren't pulled — check Steps 2 and 3 |

---

## Uninstalling

### macOS
Move Ollama from Applications to Trash. Models are stored in `~/.ollama` — delete that folder to reclaim disk space.

### Linux
```bash
sudo systemctl stop ollama
sudo rm /usr/local/bin/ollama
rm -rf ~/.ollama
```

### Windows
Uninstall from **Settings > Apps > Ollama**. Delete `C:\Users\<you>\.ollama` to remove downloaded models.

---

## Further Reading

- [Ollama documentation](https://github.com/ollama/ollama)
- [Ollama model library](https://ollama.com/library)
- [LangChain Ollama integration](https://python.langchain.com/docs/integrations/llms/ollama)
