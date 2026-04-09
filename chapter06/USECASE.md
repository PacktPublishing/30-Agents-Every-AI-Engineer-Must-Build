# Use Case: Lexington Legal Partners — Knowledge Agents for a Law Firm Drowning in Documents

**Chapter 6: Information Retrieval and Knowledge Agents**
**Book: "30 Agents Every AI Engineer Must Build" by Imran Ahmad (Packt, 2026)**

---

## The Company

**Lexington Legal Partners** is a 120-lawyer commercial litigation firm in Toronto, specializing in securities regulation, M&A disputes, and class action defense. They manage 340 active matters at any given time, with a document corpus of 14 million pages across case files, regulatory filings, court decisions, contracts, and internal memoranda. Annual revenue: CAD $62M. Knowledge management team: 6 research librarians, 3 IT staff, and a recently hired Director of Legal Innovation.

## The People

- **Rebecca Stern, Managing Partner** — Sponsor. Lexington lost a $4.2M arbitration because an associate missed a relevant precedent buried in a 2019 Ontario Securities Commission bulletin. The opposing counsel found it. Rebecca's mandate: "Never again. Build me a system that knows everything we know."
- **Jonathan Kwame, Director of Legal Innovation** — Technical lead. Hired 6 months ago to modernize the firm's knowledge infrastructure. He inherited a Relativity e-discovery platform, a SharePoint document management system, and six research librarians who are the firm's living index.
- **Maya Singh, Senior Associate** — Power user. She spends 12-15 hours per week on legal research — reading case law, tracing precedent chains, pulling relevant clauses from contracts across related matters. "I know the answer exists somewhere in our files. I just can't find it before the deadline."
- **Paul LaRoche, Head of Compliance** — Responsible for client confidentiality and privilege. Any system that touches case files must enforce ethical walls — information from Client A's matter must never surface in Client B's research results, even if the underlying legal principle is relevant.

## The Problem

Lexington's 14 million pages of institutional knowledge might as well not exist. The firm generates intelligence daily — legal memoranda, deposition summaries, contract analyses, regulatory interpretations — but has no way to find, connect, or reuse it. Three agents from Chapter 6 address three distinct dimensions of this crisis:

### Problem 1: Finding relevant knowledge (Knowledge Retrieval)

Maya needs to answer: "Has any Ontario court addressed the duty of care for AI-generated financial recommendations in the past 3 years?" The answer exists across court decisions (CanLII), securities bulletins (OSC), firm memos (SharePoint), and academic commentary. But:

- **Keyword search fails.** Searching "AI financial recommendations duty of care" misses decisions that discuss "algorithmic advisory services" or "automated investment guidance" — semantically identical but lexically different. The refund policy diagnosis from page 152 applies directly: the query uses terminology absent from the embedded corpus.
- **Sources are siloed.** CanLII, WestlawNext, the OSC website, and SharePoint each have separate search interfaces. Maya runs the same search four times with slightly different terms.
- **No provenance.** When Maya finds a relevant passage, she must manually trace it to the original source, verify the citation, and confirm it hasn't been overturned. This verification step takes longer than the initial search.

### Problem 2: Understanding documents (Document Intelligence)

Lexington's M&A practice reviews 200-300 contracts per deal during due diligence. Each contract contains clauses buried across 40-80 pages: indemnification limits, change of control provisions, assignment restrictions, IP ownership. Currently:

- **Manual review takes 4-6 hours per contract.** An associate reads each page, highlights relevant clauses, and enters extracted terms into a comparison spreadsheet.
- **OCR quality varies wildly.** Older contracts are scanned PDFs from the 1990s. Some are faxed copies of faxed copies. Tesseract produces garbage on 15% of pages, and no one knows which 15% until a lawyer spots an error.
- **No schema enforcement.** Each associate extracts clauses differently. One records the indemnification cap as "$5M"; another as "$5,000,000"; another as "five million dollars (USD)." The comparison spreadsheet becomes unreliable.

### Problem 3: Synthesizing across a research corpus (Scientific Research)

For class action defense, Lexington needs to synthesize evidence across hundreds of documents — expert reports, statistical analyses, regulatory proceedings — to identify patterns, contradictions, and gaps. A partner asks: "Across all the expert reports filed in Canadian securities class actions in the past 5 years, what methodologies were used to calculate damages, and where do the experts disagree?"

- **No human can read 400 expert reports.** Even with a team, it takes weeks.
- **Pattern recognition requires comparison.** The value isn't in any single report — it's in the patterns across them. Which damage methodologies appear most frequently? Which are criticized by courts? Where do plaintiff and defense experts systematically diverge?
- **Knowledge gaps matter.** If no expert has addressed a specific methodology for cryptocurrency securities, that gap is as valuable as the findings — it represents an uncontested argument.

## How Chapter 6's Code Solves This

### 1. Knowledge Retrieval Agent — Finding What the Firm Already Knows (Section 6.1)

Following the modular architecture from Figure 6.1, Jonathan builds a retrieval agent over Lexington's combined knowledge corpus:

**Query Understanding Layer:** When Maya asks about "AI-generated financial recommendations," the agent reformulates the query into a semantic search strategy — expanding to include "algorithmic advisory," "automated investment guidance," "robo-advisor liability," and "machine learning financial services regulation." This addresses the vocabulary mismatch problem from page 152.

**Retriever Module with hybrid search:** The agent uses the multi-stage retrieval pattern from page 148-149:
- **Stage 1:** Broad semantic search across the vector database (14M pages embedded and indexed) — retrieves 50 candidate passages
- **Stage 2:** Keyword refinement filtering for jurisdiction ("Ontario"), time period ("2022-2025"), and document type ("court decision," "regulatory bulletin")
- **Stage 3:** Reranking with a cross-encoder model that scores query-passage relevance

**RAG pipeline (page 149-150):** The top 5 retrieved passages are injected into the LLM's context with explicit instructions to synthesize an answer grounded only in the provided sources. The `return_source_documents=True` pattern from the code ensures every claim carries a citation.

**Provenance tracking:** Every answer links back to the original document — case name, paragraph number, date, and a direct link to the source in Relativity or SharePoint. Paul's compliance team can verify any claim in 30 seconds.

**Ethical wall enforcement (metadata filtering):** The retriever applies a mandatory metadata filter: `filter={"matter_id": {"$not_in": blocked_matters}}`. When Maya researches for Client A, documents from Client B's matters are excluded at the retrieval level — before any text reaches the LLM. This is the metadata filtering pattern from page 52, applied to legal privilege.

**Impact:** Maya's 12-hour research task completes in 45 minutes. The agent finds the 2019 OSC bulletin that lost the $4.2M arbitration — and surfaces three additional relevant precedents no one knew about.

### 2. Document Intelligence Agent — Reading 300 Contracts in a Day (Section 6.2)

For due diligence, Jonathan deploys the five-stage document intelligence pipeline from Figure 6.2:

**Stage 1 — Ingest & Triage:** Contracts arrive as PDFs (structured and scanned), Word documents, and occasional HTML. The classification sub-agent identifies document type (share purchase agreement, employment contract, IP license, lease) and routes to the appropriate extraction schema.

**Stage 2 — OCR & Preprocessing:** The `preprocess_and_ocr()` function from page 154 handles the scanned PDFs. Critically, it preserves **confidence scores** for every extracted word. When Tesseract produces a confidence below 60 on a dollar amount in an indemnification clause, that field is flagged for human review — not silently passed as correct. This solves the "which 15% is garbage" problem.

**Stage 3 — Layout Parsing:** The agent reconstructs table structures (critical for payment schedules and milestone tables), identifies section headings, and determines reading order. Contracts that bury material terms in footnotes or appendices are handled by the full-page layout analysis.

**Stage 4 — Information Extraction:** Schema-driven extraction using the `extract_fields_from_image()` pattern from page 155-157. For each contract type, the schema defines expected fields:

```
SHARE_PURCHASE_SCHEMA = {
    "purchase_price": ["purchase price", "aggregate consideration", "total price"],
    "indemnification_cap": ["indemnification cap", "indemnity limit", "liability cap"],
    "change_of_control": ["change of control", "change in control", "coc"],
    "assignment_restriction": ["assignment", "transfer restriction", "non-assignable"],
    "governing_law": ["governing law", "jurisdiction", "laws of"],
}
```

Fuzzy matching (`rapidfuzz`) handles variations — "Indemnification Cap" and "Maximum Indemnity Liability" both match the same field with different confidence scores.

**Stage 5 — Validation & Integration:** Extracted terms flow into a structured comparison table. High-confidence extractions (>90%) auto-populate. Low-confidence extractions (<80%) are queued for associate review, following the HITL pattern from page 160. The 95% accuracy target from page 160 means associates review fewer than 8% of extracted fields — down from 100%.

**Impact:** Due diligence on 300 contracts drops from 6 weeks (3 associates full-time) to 4 days (1 associate reviewing flagged fields). The structured comparison table is consistent — every indemnification cap is normalized to the same format, enabling instant cross-contract analysis.

### 3. Scientific Research Agent — Synthesizing 400 Expert Reports (Section 6.3)

For the class action defense synthesis, Jonathan deploys the three-phase research agent from page 162-163:

**Phase 1 — Broad Literature Scanning:** The agent queries Lexington's document management system for all expert reports in Canadian securities class actions (2020-2025). Instead of keyword search, it uses semantic search to capture reports that discuss damage methodologies even when they use different terminology — "event study," "market-adjusted return," "constant expected return model" are all captured as related concepts.

**Phase 2 — Thematic Clustering:** Using the KMeans clustering approach from page 163, the agent groups the 400 expert reports by methodology:
- Cluster 1: Event study methodology (187 reports)
- Cluster 2: Comparable transaction analysis (94 reports)
- Cluster 3: Discounted cash flow projections (68 reports)
- Cluster 4: Statistical regression models (51 reports)

Within each cluster, the agent identifies sub-themes: which statistical tests were used, what significance thresholds were applied, which data sources were cited.

**Phase 3 — Synthesis and Insight Generation:** The agent produces a structured synthesis report:
- **Consensus:** Event study is the dominant methodology (47% of reports), accepted by courts in 23 of 26 relevant decisions
- **Divergence:** Plaintiff experts systematically use shorter estimation windows (60 days vs. 120 days for defense), producing larger damage estimates
- **Knowledge gap:** No expert report addresses cryptocurrency token securities — an uncontested methodological space where Lexington could establish favorable precedent

**Impact:** A synthesis that would take a research team 3 months is produced in 2 days. The knowledge gap finding leads directly to a winning defense strategy in a pending crypto-securities class action — the partner estimates $800K in value from that single insight.

## The Revenue Impact

| Metric | Before | After | Change |
|---|---|---|---|
| Legal research time per matter | 12-15 hours/week | 2-3 hours/week | -80% |
| Due diligence (300 contracts) | 6 weeks (3 associates) | 4 days (1 associate reviewing flags) | -90% |
| Research synthesis (400 reports) | 3 months (team) | 2 days (agent + partner review) | -98% |
| Missed precedent incidents | 3-4/year | 0 (semantic search + provenance) | -100% |
| Ethical wall violations | 1-2/year (accidental) | 0 (metadata filtering enforced) | -100% |
| Extraction accuracy (contracts) | 89% (manual, inconsistent) | 96% (schema-driven, normalized) | +8% |
| Billable hours recovered | 0 | 4,200 hours/year (research time → client work) | +$2.1M revenue |

**Projected annual impact:** 4,200 recovered billable hours × $500/hour average = $2.1M in additional revenue. Prevention of missed-precedent losses (conservatively $2M/year based on the arbitration incident) = $4.1M total annual impact.

## What This Code Covers vs. Next Steps

### What Chapter 6's code demonstrates (this notebook):
- RAG pipeline (LangChain + FAISS + OpenAI) with source document return
- Chunking strategies (fixed-size, recursive, semantic) with overlap tuning
- Hybrid retrieval (semantic + keyword) for vocabulary mismatch
- OCR preprocessing with confidence scoring (Tesseract + pdf2image)
- Schema-driven document extraction with fuzzy keyword matching (rapidfuzz)
- Five-stage document intelligence pipeline (ingest → OCR → layout → extract → integrate)
- Scientific research agent (arXiv API + sentence-transformers + KMeans clustering)
- Retrieval failure diagnosis and correction patterns

### Next steps Lexington would need:
- **Tool orchestration** — Connect retrieval and extraction agents to Relativity, WestlawNext, and SharePoint (see Chapter 7)
- **Multi-agent coordination** — Specialist agents for research, extraction, and synthesis collaborating on complex matters (see Chapter 7)
- **Conversational interface** — Let lawyers interact with the knowledge base through natural dialog (see Chapter 10)
- **Ethical reasoning** — Ensure the agent handles privilege, confidentiality, and conflicts of interest appropriately (see Chapter 12)
- **Legal domain specialization** — Case analysis and precedent finding tailored to legal reasoning (see Chapter 14)
- **Continuous learning** — Agent improves extraction accuracy from lawyer corrections over time (see Chapter 9)

---

*This use case is fictional and created for educational purposes. It demonstrates how the three types of knowledge agents in Chapter 6 — Knowledge Retrieval, Document Intelligence, and Scientific Research agents — apply to a realistic commercial litigation firm scenario.*
