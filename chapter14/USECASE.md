# Use Case: Meridian Wealth & Cartwright Legal — AI Agents for Financial Advisory and Legal Research

**Chapter 14: Financial and Legal Domain Agents**
**Book: "30 Agents Every AI Engineer Must Build" by Imran Ahmad (Packt, 2026)**

---

## Part A: Meridian Wealth Partners — Compliant AI-Powered Financial Advisory

### The Company

**Meridian Wealth Partners** is a registered investment advisory (RIA) firm in Charlotte, North Carolina, managing $2.8B in assets under management (AUM) for 4,200 retail clients. They specialize in retirement planning, moderate-growth portfolios, and ESG-conscious investing. The firm has 35 financial advisors, 8 compliance staff, and a 5-person technology team. Annual revenue: $22M from advisory fees (0.75–1.0% of AUM). They are regulated by the SEC under the Investment Advisers Act of 1940 and must comply with Reg BI (Regulation Best Interest).

### The People

- **Angela Torres, CEO** — Built Meridian from a two-person practice 15 years ago. She's watching robo-advisors like Betterment and Wealthfront capture the under-$100K market with automated portfolios while her advisors spend 40% of their time on sub-$50K accounts that generate minimal fees. She needs to serve smaller accounts profitably without abandoning the personalized touch that built her reputation.
- **David Kim, Chief Compliance Officer** — Former SEC examiner. He reviews every portfolio recommendation before it reaches a client — roughly 180 per week. His team of 8 is the bottleneck. Last year, an advisor recommended an aggressive allocation to a 62-year-old conservative client. The compliance review caught it before delivery, but David was on vacation that week and the backup reviewer missed it. The client signed, lost 18% in a correction, and filed a complaint. Meridian settled for $145K.
- **Sarah Chen, Client** — 35 years old, moderate risk tolerance, $50,000 to invest, 10-year horizon. She wants moderate growth with ESG constraints (no tobacco stocks). She represents Meridian's fastest-growing client segment: mid-career professionals with $25K–$100K portfolios. There are 1,800 clients like Sarah. Each one currently gets a personalized portfolio recommendation — which takes an advisor 2.5 hours to research, construct, validate, and present.
- **Robert Martinez, Client** — 58 years old, conservative risk tolerance, $25,000, 5-year horizon before retirement. He needs minimum 40% fixed income and no more than 15% international exposure. Robert represents the compliance-sensitive segment: clients with tight constraints where a wrong recommendation triggers regulatory scrutiny.
- **Marcus Webb, Head of Technology** — Manages Meridian's tech stack. He evaluated three "AI portfolio recommendation" vendors last year. All three could generate allocations, but none had built-in compliance validation. They'd generate a recommendation, hand it to David's team for manual review, and David would reject 23% of them for suitability violations. The vendors essentially shifted the compliance problem without solving it.

### The Problem

Meridian faces a classic scaling challenge in wealth management:

1. **Advisor capacity is maxed out.** 35 advisors × 120 active accounts each = 4,200 clients. Each new advisor costs $180K/year (salary + benefits + licensing). To grow to 6,000 clients, Meridian needs 15 more advisors — a $2.7M annual cost increase that the fee revenue from smaller accounts doesn't justify.

2. **Compliance is the bottleneck, not advice generation.** Generating a portfolio recommendation takes 2.5 hours. The compliance review adds another 1.5 hours (when David's team catches up). But 77% of recommendations pass compliance on the first try — meaning 77% of David's reviews are rubber stamps that consume capacity he needs for the 23% that actually require intervention.

3. **The $145K settlement was preventable.** The aggressive allocation to the conservative client happened because the compliance check was manual, sequential, and dependent on a single reviewer being present. A structural gap — not a judgment error — caused the failure.

4. **Market data gathering is redundant.** Every advisor independently pulls the same stock quotes, financial metrics, and news summaries from the same three sources (Yahoo Finance, Finnhub, Tavily). 35 people doing the same research 35 times.

### The Attempted Solutions

| Attempt | What happened |
|---|---|
| Robo-advisor white label | Evaluated Betterment for Advisors. The allocations were fine for simple cases but couldn't handle ESG constraints, concentration limits, or multi-asset-class alternatives. Too rigid for Meridian's personalized approach. |
| Compliance checklist in CRM | Added a 15-item compliance checklist to every recommendation. Advisors checked boxes without reading them. The aggressive-to-conservative mistake happened *with all boxes checked*. |
| AI vendor evaluation (3 vendors) | All three generated recommendations but had no compliance validation. David's team still had to review 100% of output. Rejection rate: 23%. Net time savings: negative (now reviewing AI output *plus* handling rejections). |

### How Chapter 14's Code Solves This

**The Financial Advisory Agent — Supervisor Pattern with Compliance-by-Architecture**

**Architecture: LangGraph Supervisor with Specialist Agents**

A supervisor agent routes each client query to three specialist agents in sequence:

```
Supervisor → Market Data Agent → Financial Analysis Agent → News Agent → FINISH
```

Each specialist has its own tool:
- **Market Data Agent** — `get_market_data()`: Retrieves current price, market cap, P/E ratio, 52-week range for any ticker. Live mode uses yfinance; simulation returns chapter-derived data (AAPL $178.72, MSFT $378.91, GOOGL $141.55).
- **Financial Analysis Agent** — `portfolio_analysis()`: Pulls fundamental metrics (P/E, revenue growth, EPS growth, dividend yield) from Finnhub. Enables comparative analysis across candidate holdings.
- **Financial News Agent** — `search_financial_news()`: Retrieves top 5 relevant news items with relevance scores (0.79–0.95) from Tavily. Captures Fed rate signals, sector earnings, ESG trends.

The supervisor eliminates the redundant research problem — market data is gathered once and shared across all client recommendations.

**Composite Risk Scoring:**

The `RiskScorer` computes a multi-factor risk score for every candidate holding:

```
composite = 0.40 × volatility_score + 0.35 × drawdown_score + 0.25 × VaR_score
```

- **Volatility** (40% weight): Annualized standard deviation of daily returns over 90 days
- **Max Drawdown** (35%): Largest peak-to-trough decline in the lookback period
- **Value at Risk 95%** (25%): 5th percentile of daily return distribution

Risk categories: LOW (< 4.0), MODERATE (4.0–7.0), HIGH (≥ 7.0)

This replaces the advisor's gut-feel risk assessment with a quantitative, auditable score.

**Compliance-by-Architecture (The Key Innovation):**

This is what the three vendors missed. Compliance is not a post-hoc review — it's a structural node in the LangGraph workflow:

```
recommend → comply → [PASS] → deliver
                  → [FAIL] → revise → comply → deliver
```

The compliance node validates two rules automatically:
1. **Suitability:** `recommendation.risk_score ≤ client.max_risk_tolerance`
2. **Concentration:** No single asset class > 25% of portfolio

If compliance fails, the workflow routes to a `revise` node that automatically adjusts the allocation (reduces over-concentrated positions, rebalances) and re-validates. The recommendation *cannot reach the client* without passing the compliance gate.

**Sarah Chen's Case (Moderate, $50K, 10 years):**

1. Profile loaded: risk_tolerance = "moderate", max_risk_tolerance = 6.5, ESG preference
2. Supervisor dispatches Market Data → Analysis → News agents
3. Risk scoring: candidate holdings scored (AAPL LOW, MSFT HIGH, GOOGL MODERATE)
4. Allocation generated: 45% US equities, 20% international, 25% fixed income, 10% alternatives → risk_score = 6.2
5. Compliance check: 6.2 ≤ 6.5 (suitability ✓), all positions ≤ 25% (concentration ✓)
6. **PASS** → Deliver to Sarah: "Expected annual return 7.8%, max drawdown estimate -18%"

**Robert Martinez's Case (Conservative, $25K, 5 years):**

1. Profile loaded: risk_tolerance = "conservative", max_risk_tolerance = 4.0, min 40% fixed income
2. Initial recommendation: moderate template with risk_score = 5.2
3. Compliance check: 5.2 > 4.0 → **FAIL** (suitability violation)
4. Auto-revision: reduce equities, increase fixed income to 50%, risk_score drops to 3.2
5. Re-validate: 3.2 ≤ 4.0 ✓, fixed income 50% ≥ 40% ✓
6. **PASS** → Deliver to Robert

The $145K settlement scenario is structurally impossible — the aggressive allocation to the conservative client would fail the suitability gate and be auto-revised before any human sees it.

**Inter-Agent Communication Protocol:**

Every recommendation passes between agents as a structured message with sender_id, recipient_id, confidence_score, and full data payload. David's compliance team can audit the exact data flow for any recommendation.

### Impact for Meridian Wealth

| Metric | Before | After | Change |
|---|---|---|---|
| Time per recommendation | 4.0 hours (2.5 research + 1.5 compliance) | 0.5 hours (advisor review only) | -88% |
| Compliance review volume | 180/week (100% manual) | 12/week (only edge cases) | -93% |
| Compliance rejection rate | 23% (caught post-generation) | 0% (prevented by architecture) | -100% |
| Suitability violations reaching clients | 1–2/year | 0 (structurally prevented) | -100% |
| Advisor capacity | 120 clients/advisor | 180 clients/advisor | +50% |
| Cost to serve sub-$50K accounts | $450/year per client | $120/year per client | -73% |

**Revenue impact:** Meridian can grow from 4,200 to 6,000 clients without hiring 15 advisors ($2.7M saved). The sub-$50K segment (1,800 clients) becomes profitable. Projected AUM growth from $2.8B to $3.6B, adding $6M in annual fee revenue. The $145K settlement risk is eliminated by architecture.

---

## Part B: Cartwright Legal — AI-Powered Legal Research with Citation Verification

### The Company

**Cartwright Legal Group** is a 45-attorney law firm in Washington, D.C., specializing in technology law, data privacy, and cross-border e-commerce disputes. Their clients include mid-size SaaS companies, fintech startups, and a Fortune 500 retailer navigating GDPR compliance. Annual revenue: $38M from billable hours. They employ 22 associates, 15 partners, 6 paralegals, and a 4-person knowledge management team.

### The People

- **Patricia Cartwright, Managing Partner** — Founded the firm 20 years ago. She's watching AI legal tools with interest and anxiety. Interest: associates spend 35% of their billable hours on research that could be accelerated. Anxiety: the Schwartz incident — where an attorney cited fabricated cases generated by ChatGPT and was sanctioned by a federal judge — is her nightmare scenario.
- **Jason Nakamura, Senior Associate** — Rising star, billing 2,100 hours/year. He spends 6–8 hours per legal memo on research: searching Westlaw, reading cases, verifying citations, checking case status (good law vs. overruled). He's efficient but there's a physical limit — he can't read faster.
- **Diana Osei, Junior Associate** — 2 years out of law school, billing 1,900 hours. She was assigned a complex jurisdictional research question last month and spent 12 hours on it. Her draft cited 8 cases — but during partner review, Patricia found that one citation didn't exist. Diana had copied it from a secondary source that itself had an error. It wasn't AI-generated — just human carelessness amplified by time pressure. But the partner review caught it, and Diana's memo was sent back for revision.
- **Martin Schultz, Knowledge Management Director** — Maintains Cartwright's internal case database and Westlaw subscription. He's been asked to evaluate AI research tools but his requirement is non-negotiable: "Every citation in a memo must be verified against an authoritative source before delivery. I don't care how good the AI is at generating text — if it hallucinates a single case, we're exposed to sanctions."
- **GlobalRetail Corp, Client** — Fortune 500 retailer negotiating a Master Services Agreement with a cloud analytics provider (TechSolutions Inc.). The contract involves cross-border data transfers, GDPR compliance, and $45,000/month in fees over 36 months ($1.62M total value). GlobalRetail's in-house counsel wants Cartwright to review the contract for risk.

### The Problem

Cartwright bills $450–$750/hour depending on attorney seniority. Research is their largest cost center:

1. **Research is slow and expensive.** Jason spends 6–8 hours per memo. At $550/hour, that's $3,300–$4,400 in research costs per memo. Cartwright produces ~40 research memos per month. Annual research cost: $1.6M–$2.1M in attorney time.

2. **Citation verification is manual and error-prone.** After writing a draft, attorneys must verify every citation: Does the case exist? Is it good law (not overruled or distinguished)? Is it from the right jurisdiction? Is it binding or merely persuasive? This verification adds 2–3 hours per memo. Diana's error — citing a non-existent case from a secondary source — shows that even careful attorneys make mistakes under time pressure.

3. **Authority ranking is subjective.** When an attorney finds 15 relevant cases, deciding which 5 to cite is a judgment call based on court hierarchy, recency, and relevance. Junior associates like Diana don't have the experience to rank authorities as effectively as Jason, leading to weaker memos that require more partner revision.

4. **Contract review is bottlenecked.** GlobalRetail's MSA review has been sitting in the queue for 3 weeks. The contract has 8 clauses, and reviewing each for risk, compliance gaps, and negotiation points takes a senior associate 10–12 hours. At $650/hour, that's $6,500–$7,800 per contract review. Cartwright reviews ~15 contracts per month.

### The Attempted Solutions

| Attempt | What happened |
|---|---|
| Westlaw AI-Assisted Research | Improved search relevance but still returns 50+ results that attorneys must read, rank, and verify manually. No authority weighting, no citation verification. |
| ChatGPT for draft memos | Patricia banned it after the Schwartz incident made national news. She's right — the risk of sanctions from hallucinated citations outweighs any time savings. |
| Paralegal pre-research | Paralegals pull initial case lists and summaries. This saves 2 hours per memo but the attorney still verifies every citation. Net savings: 25%. Not transformative. |
| Contract review templates | Martin created clause-by-clause review templates. Helps structure the analysis but doesn't reduce the reading and risk assessment time. |

### How Chapter 14's Code Solves This

**The Legal Intelligence Agent — Hybrid Retrieval with Citation Verification**

**Legal Knowledge Base with Authority-Weighted Ranking:**

Cartwright's case database is encoded in a `LegalKnowledgeBase` with vector embeddings, metadata (court, jurisdiction, authority level 0–10, case status), and hybrid search:

```
final_score = 0.50 × semantic_similarity + 0.30 × (authority_level / 10) + 0.20 × recency_score
```

This formula solves Diana's authority ranking problem. A Supreme Court case (authority 10) from 2024 with moderate semantic relevance will outrank a district court case (authority 3) with high relevance — matching how experienced attorneys like Jason intuitively prioritize authorities.

Court hierarchy encoded in the system:
- Supreme Court: authority 10
- Circuit Courts of Appeals: authority 7–8
- State Supreme Courts: authority 6–7
- State Appellate Courts: authority 5
- District Courts: authority 3

**Three-Stage Precedent Finding:**

**Stage 1: Issue Extraction.** The `PrecedentFinder` decomposes a research query into discrete legal issues. "What is the current standard for personal jurisdiction over foreign corporations in e-commerce disputes?" becomes:
- Issue 1: Standard of care in personal jurisdiction (priority 1)
- Issue 2: Elements of purposeful direction in e-commerce (priority 1)
- Issue 3: Due process requirements for foreign corporations (priority 2)

**Stage 2: Multi-Dimensional Retrieval.** For each issue, hybrid search retrieves cases filtered by jurisdiction and minimum authority level (≥ 3), then re-ranked by the authority-weighted formula.

**Stage 3: Authority Analysis.** Results are categorized:
- **Binding authorities** (authority ≥ 7): Must be cited and addressed
- **Persuasive authorities** (3 ≤ authority < 7): May be cited to strengthen argument

**Citation Verification Gate (The Critical Innovation):**

This is Martin's non-negotiable requirement implemented as code. After the research memo draft is generated, *every citation is verified* against the legal knowledge base:

```python
verify_citation(citation, jurisdiction, check_precedential=True, check_good_law=True)
```

The verification checks:
- Does the case exist in the database?
- Is it "good law" (not overruled, distinguished, or questioned)?
- Does it meet the minimum authority level for the jurisdiction?

**The Schwartz Test:** The mock database deliberately includes a fabricated case — *Varghese v. China Southern Airlines, No. 22-cv-1234 (S.D.N.Y. 2023)* — with authority_level = 0 and status = "fabricated." If the LLM hallucinates this citation into a memo, the verification gate catches it:

```
[VERIFIED]   Johnson v. DataFlow Systems, 78 F.4th 231 (9th Cir. 2023) ✓
[VERIFIED]   Smith v. TechCorp International, 589 U.S. 412 (2024) ✓
[UNVERIFIED] Varghese v. China Southern Airlines, No. 22-cv-1234 ✗ — FLAGGED
```

The unverified citation is prefixed with `[UNVERIFIED]` in the draft and flagged in red. The memo's quality score (verified/total citations) drops, and the attorney is alerted.

**Five-Stage Contract Analysis:**

For GlobalRetail's MSA review, the `ContractAnalysisAgent` runs a 5-stage pipeline:

1. **Structure extraction:** Identifies 8 clauses (scope, term, payment, IP, indemnification, liability, confidentiality, data processing)

2. **Clause classification and risk assessment:**
   - Indemnification: **HIGH RISK** — one-sided, unlimited survival clause favoring TechSolutions
   - Liability cap: **HIGH RISK** — capped at 3 months of fees ($135K) for a 36-month, $1.62M agreement
   - Data processing: **CRITICAL** — no GDPR Data Processing Addendum, no Standard Contractual Clauses, vague "commercially reasonable" security standard

3. **Compliance validation:** Checks for required clauses and GDPR compliance markers. Flags: data processing clause missing GDPR DPA and SCCs.

4. **Recommendation generation:** Actionable items per risk finding:
   - Negotiate mutual indemnification with a 12-month survival cap
   - Increase liability cap to 12 months of fees ($540K)
   - Require a GDPR-compliant DPA with Standard Contractual Clauses for cross-border transfers

The contract review that took a senior associate 10–12 hours is completed in 45 minutes with structured findings. The associate reviews, adds client-specific context, and delivers.

### Impact for Cartwright Legal

| Metric | Before | After | Change |
|---|---|---|---|
| Research time per memo | 6–8 hours | 1.5–2 hours | -73% |
| Citation verification errors | 1–2/quarter (manual misses) | 0 (automated gate) | -100% |
| Authority ranking quality (junior associates) | Inconsistent, requires partner revision | Authority-weighted, consistent | Qualitative |
| Contract review time | 10–12 hours | 2–3 hours (review + client context) | -75% |
| Research cost per memo | $3,300–$4,400 | $825–$1,100 | -75% |
| Annual research cost | $1.6M–$2.1M | $400K–$525K | -75% |
| Memos requiring partner revision for citation issues | 15% | < 2% | -87% |

**Revenue impact:** The 75% reduction in research time frees ~4,200 attorney hours per year. At $550/hour average, that's $2.3M in capacity that can be redirected to higher-value client work. The citation verification gate eliminates sanctions risk entirely. GlobalRetail's contract review, delivered in 2 days instead of 3 weeks, leads to a retainer expansion ($180K/year → $320K/year).

---

## What This Code Covers vs. Next Steps

### What Chapter 14's code solves:
- LangGraph supervisor pattern with specialist financial agents (market data, analysis, news)
- Composite risk scoring (volatility 40% + drawdown 35% + VaR 25%)
- Compliance-by-architecture — suitability and concentration gates as structural workflow nodes
- Personalized portfolio recommendations with client profile constraints
- Inter-agent communication protocol with confidence scoring
- Legal knowledge base with authority-weighted hybrid retrieval (similarity 50% + authority 30% + recency 20%)
- Three-stage precedent finding (issue extraction → retrieval → authority analysis)
- Five-stage contract analysis with clause-level risk assessment and GDPR compliance checking
- Citation verification gate that detects hallucinated cases before delivery
- Full simulation mode with chapter-derived financial and legal mock data

### Next steps:
- **Self-improving advisory** — Learn from client feedback and market outcomes to refine allocation models over time (see Chapter 9)
- **Conversational interface** — Let clients like Sarah ask follow-up questions about their portfolio recommendation in natural language (see Chapter 10)
- **Explainable recommendations** — Provide SHAP-style attribution showing which factors drove the allocation and risk score (see Chapter 12)
- **Document intelligence** — Process scanned contracts and legal filings via OCR and NLP (see Chapter 6 for RAG-based document agents)
- **Real-time market monitoring** — Continuous portfolio risk monitoring with proportional alerting when positions breach thresholds (see Chapter 11 for physical world sensing patterns)
- **Multi-firm coordination** — For complex deals involving multiple law firms and financial advisors, coordinate specialist agents across organizational boundaries (see Chapter 7 for tool orchestration)

---

*This use case is fictional and created for educational purposes. It demonstrates how the code patterns in Chapter 14 apply to realistic financial advisory and legal research scenarios.*
