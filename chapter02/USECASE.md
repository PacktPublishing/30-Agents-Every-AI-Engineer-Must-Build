# Use Case: NorthStar Wealth — Choosing the Right Agent Stack for Autonomous Financial Research

**Chapter 2: The Agent Engineer's Toolkit**
**Book: "30 Agents Every AI Engineer Must Build" by Imran Ahmad (Packt, 2026)**

---

## The Company

**NorthStar Wealth Advisors** is a boutique investment research firm in Montreal with 45 financial analysts serving 200 institutional clients. They produce 120 research reports per month covering equities, fixed income, and alternative investments across North American markets. Annual revenue: CAD $28M. Technology team: 8 developers, 1 data engineer, and a CTO who writes code on weekends.

## The People

- **Grace Liu, CTO** — Technical decision-maker. She has 90 days to deliver a working prototype of an AI research assistant that can autonomously gather market data, analyze trends, and draft preliminary research reports. She's read every framework comparison blog post and is more confused than when she started.
- **Youssef Benali, Head of Equity Research** — Primary user. His analysts spend 60% of their time on data gathering and formatting before the actual analysis begins. "By the time we finish pulling data from Bloomberg, scraping filings from SEDAR+, and formatting the tables, the market has already moved."
- **Claire Fontaine, Compliance Officer** — Every research report is a regulatory document. IIROC (Investment Industry Regulatory Organization of Canada) requires that all factual claims in published research be traceable to primary sources. "If your AI invents a revenue figure, we don't just lose a client — we lose our license."
- **Raj Patel, Senior Analyst** — Skeptical power user. He's tried ChatGPT for research drafts and found it confidently wrong 15% of the time. "It cited a Bloomberg article that doesn't exist and made up an earnings figure for Shopify. I can't use a tool I can't trust."

## The Problem

NorthStar's research workflow is manual, slow, and doesn't scale:

1. **Data gathering** (4-6 hours per report): Analysts manually pull data from Bloomberg Terminal, SEDAR+ filings, StatCan, company investor relations pages, and news feeds. Each source has a different interface, format, and access method. There is no unified way to query across sources.

2. **Analysis** (3-4 hours): Analysts build financial models in Excel, run comparisons against sector peers, identify trends, and form investment theses. This is where the actual intellectual value lives — but it's compressed into a fraction of the workday.

3. **Report drafting** (2-3 hours): Formatting tables, writing executive summaries, ensuring style consistency, inserting proper citations. Template-heavy work that senior analysts resent doing.

4. **Compliance review** (1-2 hours): Claire's team verifies every factual claim against source documents. When they find an error, it goes back to the analyst — adding a day to the cycle.

**Total: 10-15 hours per report.** NorthStar needs to produce 120/month with 45 analysts. The math doesn't work. Reports are late, quality is inconsistent, and clients are starting to notice.

Grace needs an AI research assistant that can cut the data gathering and drafting time by 80% while maintaining the factual rigor that Claire demands. But she faces a paralyzing toolkit decision: Which framework? Which models? Which vector database? Which cloud platform? Each choice has cascading consequences for the entire system.

## The Toolkit Decisions (Mapped to Chapter 2 Sections)

### Decision 1: Development Framework — LangChain + LangGraph (Section 2.1)

Grace evaluates the frameworks from Table 2.1 against NorthStar's requirements:

| Framework | Why considered | Why chosen/rejected |
|---|---|---|
| **LangChain** | Modular design, 100+ integrations, strong tool ecosystem | **Chosen as foundation** — Bloomberg API wrapper, SEDAR+ scraper, and StatCan connector can all be wrapped as LangChain Tools |
| **LangGraph** | Stateful workflows, conditional branching, loop support | **Chosen for orchestration** — research workflow needs loops (gather → analyze → is data sufficient? → gather more) exactly like the research_node/decide_node example on page 42-43 |
| **LlamaIndex** | Best-in-class document retrieval and semantic compression | **Chosen for RAG layer** — NorthStar's 50,000+ past reports and 200,000+ filings need sophisticated retrieval, not just keyword search |
| **CrewAI** | Role-based multi-agent coordination | **Rejected for now** — early-stage maturity; NorthStar needs production reliability, not experimental collaboration |
| **AutoGPT** | Autonomous goal decomposition | **Rejected** — "low reliability, fragile control" (Table 2.1). Claire won't accept a system that pursues research goals autonomously without checkpoints |

**The compose-over-build decision (page 47):** Grace follows the book's hybrid approach — LangChain for orchestration, LlamaIndex for document retrieval, LangGraph for stateful workflow management. She starts with LangChain's `ConversationBufferMemory` for prototyping, knowing she'll swap it for a production vector database later.

### Decision 2: LLM Selection — Hybrid Model Architecture (Section 2.2)

Following the `route_to_model()` pattern on page 48, Grace designs a three-tier model strategy:

```
Data extraction (FACTUAL)    → Mistral 7B   — fast, cheap, good at structured extraction
Analysis & reasoning (ANALYTICAL) → GPT-4    — best at complex financial reasoning
Report drafting (CREATIVE)   → Claude 3      — superior long-form writing quality
```

**Why this matters:** A single research report triggers 50+ LLM calls. Using GPT-4 for everything would cost $8-12 per report ($960-$1,440/month for 120 reports). The hybrid router cuts this to $2.50/report ($300/month) by using expensive models only where they add value.

**The confidence-based escalation pattern:** When Mistral extracts a revenue figure but its confidence is below 0.85, the extraction automatically escalates to GPT-4 for verification. This catches the hallucination problem Raj experienced — uncertain extractions get a second opinion from a more capable model.

### Decision 3: Vector Database — Chroma for Dev, Pinecone for Production (Section 2.3)

NorthStar's knowledge base includes:
- 50,000 past research reports (proprietary — competitive advantage)
- 200,000+ regulatory filings (SEDAR+, SEC EDGAR)
- 10 years of Bloomberg market data snapshots
- Analyst notes and investment committee minutes

Grace follows the book's guidance: **Chroma for prototyping** ("designed to make local development joyful... prototype a RAG system in minutes rather than hours") and **Pinecone for production** ("when milliseconds matter and you need cloud-native scaling").

**The RAG pipeline (page 51-52):**
1. **Chunk** — NorthStar uses hierarchical chunking: full reports stored alongside paragraph-level and table-level chunks. Financial tables get their own embedding strategy.
2. **Embed** — OpenAI's `text-embedding-ada-002` for text; a custom fine-tuned model for financial tables.
3. **Store with metadata** — Source authority (Bloomberg > news > social), recency, sector, and analyst who produced it.
4. **Retrieve on demand** — When the agent needs "Q3 2025 revenue for Shopify," it retrieves from filings first (highest authority), cross-references with Bloomberg data, and only uses news as supplementary context.
5. **Inject into prompts** — Retrieved context goes into the LLM call with source citations attached.

**The reranking step (page 52):** First-stage retrieval pulls 20 candidate chunks. A Cohere Rerank model narrows to the 5 most relevant. This is the difference between "here's everything about Shopify" and "here's Shopify's Q3 2025 revenue broken down by segment."

**Impact for Claire:** Every factual claim in a generated report carries a source citation traceable to a specific chunk in the vector database. The compliance team can click through to the original filing, Bloomberg snapshot, or analyst note. No more "the AI made it up" — every number has a provenance chain.

### Decision 4: Tool Integration — LangChain Tools + OpenAI Function Calling (Section 2.4)

Following the LangChain Tool abstraction pattern (page 54) and OpenAI function calling (page 54-55), Grace wraps NorthStar's data sources as agent-accessible tools:

| Tool | Function | Pattern |
|---|---|---|
| `BloombergDataTool` | Pull market data, financials, estimates | LangChain Tool wrapper |
| `SEDARFilingTool` | Search and retrieve Canadian regulatory filings | LangChain Tool + scraper |
| `CompanyFinancialsTool` | Extract structured data from 10-K/10-Q filings | OpenAI function calling (JSON schema) |
| `PeerComparisonTool` | Generate sector peer comparison tables | LangChain Tool |
| `ReportFormatterTool` | Apply NorthStar's report template and style guide | LangChain Tool |
| `SourceVerificationTool` | Cross-reference claims against primary sources | LangChain Tool + RAG |

The agent uses the ReAct (Reasoning and Acting) pattern from page 41 — it reasons about which tools to use, invokes them in the appropriate order, and synthesizes the results. When asked "Draft a Q3 earnings preview for Shopify," it autonomously determines it needs Bloomberg data (revenue estimates), SEDAR filings (management guidance), peer comparison (vs. other Canadian tech), and the report template.

### Decision 5: Cloud Platform — AWS with Bedrock (Section 2.5)

NorthStar already runs on AWS. Grace chooses **Amazon Bedrock** for:
- Access to multiple foundation models (Claude, Llama, Titan) through a single API — enabling the hybrid model architecture
- **Bedrock Knowledge Bases** for managed RAG — reducing operational overhead of maintaining the vector database pipeline
- Canadian data residency (ca-central-1) — required by Claire for client-identifiable research data
- Integration with existing AWS security (IAM, VPC, CloudTrail) — audit trail for every LLM call

## The Resulting Architecture

```
User: "Draft Q3 earnings preview for Shopify"
  │
  ▼
[LangGraph Orchestrator] ← stateful workflow with conditional branching
  │
  ├─ Research Node ──► BloombergDataTool, SEDARFilingTool
  │                    (data gathering with Mistral 7B extraction)
  │
  ├─ Analyze Node ──► CompanyFinancialsTool, PeerComparisonTool
  │                   (financial reasoning with GPT-4)
  │
  ├─ Decide Node ──► Is data sufficient?
  │                   NO → loop back to Research Node
  │                   YES → proceed to Draft Node
  │
  ├─ Draft Node ──► ReportFormatterTool
  │                 (long-form writing with Claude 3)
  │
  └─ Verify Node ──► SourceVerificationTool + RAG
                      (every claim cross-referenced against primary sources)
  │
  ▼
[Output: Draft report with source citations]
```

## The Revenue Impact

| Metric | Before | After | Change |
|---|---|---|---|
| Time per research report | 10-15 hours | 3-4 hours | -70% |
| Reports per analyst per month | 2.7 | 6.5 | +141% |
| Data gathering time | 4-6 hours | 20 minutes (agent) | -94% |
| Factual error rate | 3.2% (human fatigue) | 0.8% (RAG + verification) | -75% |
| Compliance review time | 1-2 hours | 15 minutes (source-linked) | -85% |
| Monthly LLM cost | $0 | $300 (hybrid routing) | New cost |
| Client report satisfaction | 7.2/10 | 8.9/10 | +24% |

**Projected annual impact:** Analysts freed from data gathering produce 2.4× more reports. Higher throughput + better quality = 3 new institutional clients in Q1 ($840K annual revenue). The $300/month LLM cost is trivial against the revenue gain.

## What This Code Covers vs. Next Steps

### What Chapter 2's code demonstrates (this notebook):
- LangChain agent setup with Calculator + WebSearch tools (ReAct pattern)
- LangGraph stateful workflow with research → analyze → decide → respond loop
- Hybrid model router (`route_to_model()` for factual/creative/analytical routing)
- LangChain Tool abstraction (wrapping functions as agent tools)
- OpenAI function calling (JSON schema for structured tool invocation)
- LangChain memory systems (`ConversationBufferMemory`, `ConversationSummaryMemory`)
- Vector database concepts (embedding, similarity search, metadata filtering)

### Next steps NorthStar would need:
- **Agent prompting** — Design PTCF-compliant prompts for each specialist role (see Chapter 3)
- **Production deployment** — Cost tracking, circuit breakers, and compliance audit trails (see Chapter 4)
- **Cognitive architecture** — Full autonomous research loop with planning and memory (see Chapter 5)
- **RAG implementation** — Production knowledge retrieval pipeline over NorthStar's document corpus (see Chapter 6)
- **Tool orchestration** — Chain-of-agents pattern for complex multi-source research tasks (see Chapter 7)
- **Data analysis** — Statistical reasoning and visualization for financial modeling (see Chapter 8)

---

*This use case is fictional and created for educational purposes. It demonstrates how the toolkit selection decisions in Chapter 2 — frameworks, models, vector databases, tool integration, and cloud platforms — apply to a realistic investment research scenario.*
