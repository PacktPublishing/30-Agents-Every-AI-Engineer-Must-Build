# Chapter 2: The Agent Engineer's Toolkit

**Book:** *Agents* by **Imran Ahmad** (Packt, 2026)

Companion code repository for **Chapter 2 (pages 37–60)**, covering the full agent engineering stack: frameworks, LLMs, vector databases, RAG pipelines, tool integration, and cloud-native platforms.

---

## Quickstart

```bash
# Clone and enter the repository
git clone <repo-url>
cd chapter-02-agent-toolkit

# Install core dependencies
pip install -r requirements.txt

# Launch the notebook
jupyter notebook chapter_02_agent_toolkit.ipynb
```

**No API key needed.** The notebook runs in **Simulation Mode** by default, producing deterministic output derived from Chapter 2 content.

### Optional: Enable Live Mode

```bash
cp .env.template .env
# Edit .env and add your OPENAI_API_KEY
```

---

## Repository Structure

```
chapter-02-agent-toolkit/
├── README.md                            # This file
├── AGENTS.md                            # Agentic metadata + AI persona
├── LICENSE                              # MIT License
├── requirements.txt                     # Dependencies (core + optional)
├── .env.template                        # API key template
├── .gitignore                           # Git ignore rules
├── troubleshooting.md                   # Dependency conflict guide
├── chapter_02_agent_toolkit.ipynb       # Main notebook (all demos)
└── mock_llm_layer.py                    # Mock infrastructure module
```

---

## What's Inside the Notebook

| # | Section | Chapter Reference | What You'll See |
|---|---------|-------------------|-----------------|
| 1 | Environment Setup | — | Auto-detection of API keys, mode banner |
| 2 | Framework Landscape | Table 2.1 (p.38-39) | Comparison of LangChain, LangGraph, LlamaIndex, AutoGPT, CrewAI, AutoGen |
| 3 | LangChain Agent | p.40-41 | ReAct pattern with Calculator + WebSearch tools |
| 4 | LangChain Memory | p.41-42 | Buffer vs. Summary memory comparison |
| 5 | LangGraph Workflow | p.43-44 | Stateful graph: research → analyze → decide → respond |
| 6 | LangGraph State | p.44-45 | TypedDict schema + Mermaid diagram |
| 7 | Framework Guide | p.46-47 | Selection criteria + integration patterns |
| 8 | Hybrid Routing | p.48-49 | Multi-model query router (Mistral/Claude/GPT-4o) |
| 9 | RAG Pipeline | p.49-53 | Simulated vector search with similarity scores |
| 10 | LangChain Tool | p.53-54 | StockPriceTool abstraction pattern |
| 11 | Function Calling | p.55 | OpenAI JSON schema + mock execution |
| 12 | Cloud Platforms | p.55-60 | AWS / Azure / Google Cloud comparison |
| 13 | Summary | p.60 | Chapter takeaways and next steps |

---

## Simulation Mode vs. Live Mode

| Feature | Simulation Mode | Live Mode |
|---------|----------------|-----------|
| API key required | No | Yes |
| Dependencies | 3 packages (jupyter, dotenv, sympy) | Full stack (LangChain, OpenAI, etc.) |
| LLM responses | Deterministic, chapter-derived mocks | Real model inference |
| Tool calls | Mock implementations | Live API calls |
| Error handling | All errors caught, mock fallback | Errors caught, real fallback |
| Output prefix | `[SIMULATION]` | (none) |

Both modes use the same color-coded logging:
- **Blue** `[INFO]`: Agent initialization, step entry
- **Green** `[SUCCESS]`: Completed steps, valid returns
- **Red** `[HANDLED ERROR]`: Caught exceptions, fallback activation
- **Yellow** `[SIMULATION]`: Mock mode indicator

---

## For AI Assistants

If you are an AI agent helping a reader with this repository, please read [`AGENTS.md`](AGENTS.md) for the required persona and behavioral guidelines.

---

## Troubleshooting

See [`troubleshooting.md`](troubleshooting.md) for solutions to common dependency conflicts and environment issues.

---

## License

MIT License. See [`LICENSE`](LICENSE).

**Author:** Imran Ahmad
