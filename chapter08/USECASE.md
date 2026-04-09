# Use Case: CanadaFirst News — Data Analysis and Verification Agents for Investigative Journalism

**Chapter 8: Data Analysis and Reasoning Agents**
**Book: "30 Agents Every AI Engineer Must Build" by Imran Ahmad (Packt, 2026)**

---

## The Company

**CanadaFirst News** is an independent investigative news organization based in Ottawa, covering federal politics, economics, and public policy. They publish 40 investigative stories per month, supported by a team of 18 journalists, 4 data reporters, and a 3-person technology team. Annual operating budget: CAD $6.2M (a mix of subscriptions, grants, and philanthropic funding). Their reputation depends entirely on factual accuracy — a single retraction costs more than money; it costs trust.

## The People

- **Diane Lafleur, Editor-in-Chief** — Sponsor. After a competitor published an AI-generated story with fabricated statistics that went viral before the correction, Diane wants the opposite: AI that makes CanadaFirst *more* accurate, not less. "I want every number in every story verified against primary sources before it reaches the reader."
- **Kwesi Asante, Lead Data Reporter** — Technical user. He investigates federal spending, infrastructure budgets, and economic policy using data from Statistics Canada, the Parliamentary Budget Office, and Open Canada. His stories take 3-4 weeks each because 60% of his time is spent cleaning, analyzing, and visualizing data — not writing.
- **Sophie Tremblay, Political Correspondent** — She covers fast-breaking political stories where officials cite statistics in press conferences, parliamentary debates, and scrums. She needs to verify claims in real time: "The Minister just said unemployment in Ottawa dropped 4.8% this year. Is that true? I have 20 minutes before deadline."
- **Raj Mehta, Fact-Check Editor** — Every story passes through Raj before publication. He manually cross-references every factual claim against primary sources. A typical investigative piece has 30-50 verifiable claims. Raj's bottleneck limits CanadaFirst to 40 stories/month.

## The Problem

CanadaFirst faces three interconnected challenges that map directly to Chapter 8's three agent types:

### Problem 1: Data analysis is manual and slow (Data Analysis agent)

Kwesi is investigating whether federal infrastructure spending actually reaches the communities it's announced for. He has:
- 5 years of federal budget allocation data (Treasury Board CSV files)
- Municipal spending reports from 200 communities (PDF and Excel, inconsistent formats)
- Census demographics for matching (Statistics Canada API)
- Construction permit data from provincial registries

To answer "How much of the $14B announced infrastructure budget actually resulted in construction activity in rural communities?", Kwesi must:
1. Clean and normalize 5 different data formats
2. Join datasets on community identifiers (which are inconsistent across sources)
3. Calculate per-capita spending by community type (rural vs. urban)
4. Identify statistical anomalies (communities with large allocations but no construction permits)
5. Visualize the results as publication-ready charts

This takes Kwesi **3 weeks**. The data cleaning alone takes 8 days. And he can't iterate — if the editor asks "What about provincial co-funding?", the analysis restarts.

### Problem 2: Fact-checking is the publication bottleneck (Verification and Validation agent)

Sophie files a story: "Federal government spending on AI research increased 340% between 2021 and 2025, reaching $890M, according to the Parliamentary Budget Office." Raj must verify:
- Did the PBO actually publish this figure? (Source verification)
- Is $890M the correct number? (Factual accuracy)
- Is 340% the correct growth rate from the base year? (Mathematical verification)
- Is the claim about "AI research" specifically, or does it include broader "digital innovation"? (Scope verification)

Raj checks 4 sources, recalculates the percentage, and discovers the PBO figure is $847M and includes some non-AI digital programs. The 340% figure is correct only if you use 2020 as the base year (not 2021 as the story states). These are exactly the kinds of subtle errors that destroy credibility.

With 30-50 claims per story and 40 stories per month, Raj processes **1,200-2,000 claims monthly** — each requiring manual source verification. He's the single point of failure for the entire newsroom.

### Problem 3: Complex investigations require cross-domain reasoning (General Problem Solver)

For a major investigation — "Is Canada's immigration system creating regional economic disparities?" — the answer isn't in any single dataset. It requires synthesizing:
- Immigration data (IRCC settlement patterns)
- Economic data (GDP growth by province, employment rates)
- Housing data (CMHC vacancy rates, price indices)
- Healthcare data (physician-to-patient ratios by region)
- Education data (school enrollment growth)

No single analyst has expertise across all five domains. The investigation requires cross-domain reasoning: do immigration settlement patterns correlate with housing shortages? Does increased settlement in smaller cities correspond to healthcare strain or economic growth? Where do the data sources agree, and where do they contradict?

## How Chapter 8's Code Solves This

### 1. Data Analysis Agent — From Question to Insight in Minutes (Section 8.1)

Following the cognitive loop from Figure 8.1, Kwesi gets a conversational data analyst:

**Intent analysis and planning:** Kwesi asks: "Show me per-capita federal infrastructure spending by community type, rural vs urban, for the past 5 years." The LLM Reasoning Core (page 205) interprets this as:
- Data source: Treasury Board budget allocations + census community classifications
- Metric: spending / population, grouped by rural/urban designation
- Time dimension: 2020-2025, annual
- Output: comparison visualization

**Code formulation and execution:** The agent generates Python (Pandas) code to:
```python
# Load and join datasets
merged = budget_df.merge(census_df, on='community_id')
merged['per_capita'] = merged['allocation'] / merged['population']
summary = merged.groupby(['year', 'community_type'])['per_capita'].mean()
```

**Visualization recommendation (page 207):** The agent recognizes "past 5 years" as a temporal dimension and "rural vs urban" as a categorical comparison. Following the decision branching logic from Figure 8.2, it recommends a **grouped bar chart** (categorical comparison across time) rather than a line chart.

**Statistical reasoning (page 209-210):**
- **Descriptive:** Rural communities received $342/capita vs. $1,240/capita for urban — a 3.6× gap
- **Inferential:** OLS regression shows the gap is statistically significant (p < 0.001) even after controlling for province and existing infrastructure
- **Anomaly detection:** The z-score analysis (page 210) flags 12 communities with large budget allocations but zero construction permits — potential "announcement without delivery" cases

**Presentation and refinement:** The agent delivers the chart + narrative summary. Kwesi asks: "Now break it down by province." The feedback loop (page 205) reactivates — no need to restart from scratch.

**Impact:** 3-week analysis compressed to 45 minutes. Kwesi spends his time on the story, not the spreadsheet.

### 2. Verification and Validation Agent — Automated Fact-Checking (Section 8.2)

Following the newsroom fact-checker case study from pages 220-225, Raj gets an automated verification pipeline:

**Claim extraction:** The agent scans Sophie's draft and extracts verifiable claims:
```
Claim 1: "Federal government spending on AI research increased 340%"
  → metric: spending_growth, entity: federal_ai_research, value: 340%
Claim 2: "reaching $890M"
  → metric: spending_total, entity: federal_ai_research, value: $890M
Claim 3: "according to the Parliamentary Budget Office"
  → source_attribution: PBO
```

**Evidence retrieval:** For each claim, the agent queries the trusted data store — in CanadaFirst's case, a curated database of verified figures from Statistics Canada, PBO, IRCC, and other federal sources (matching the `trusted_database` pattern from page 221).

**Factual verification using NLI (page 214-215, Figure 8.3):** The agent applies the BART-based Natural Language Inference model to compare claims against sources:
- **Claim:** "$890M" → **Source A (PBO report):** "$847M for digital innovation including AI" → **Verdict:** `Mostly True` — the number is close but the category is broader
- **Claim:** "340% increase" → **Source B (PBO 2020 baseline):** $193M → calculated growth to $847M = 339% → **Verdict:** `Confirmed` if base year is 2020, `Contradicted` if base year is 2021 as stated

**Logical coherence check (page 212):** The agent detects the base year inconsistency — the story says "between 2021 and 2025" but the 340% figure only works with a 2020 baseline. This is the premise-conclusion mismatch pattern from page 212.

**Handling conflicting evidence (Figure 8.3):** When Source A reports $847M and Sophie's claim says $890M, the agent weighs source credibility (PBO > press release > speech transcript), assigns a confidence score, and produces a structured verdict with explanation.

**Impact:** Raj's 1-2 hour per-story verification drops to 15 minutes (reviewing agent findings). Throughput increases from 40 to 65 stories/month. The $890M error is caught before publication — preserving CanadaFirst's credibility.

### 3. General Problem Solver — Cross-Domain Investigation (Section 8.3)

For the immigration-economic disparities investigation, the team deploys the five-stage General Problem Solver from Figure 8.4:

**Stage 1 — Decompose:** The agent breaks the question into sub-problems:
- SP1: Where are immigrants settling? (IRCC data)
- SP2: How do settlement patterns correlate with economic growth? (GDP, employment)
- SP3: Do high-settlement areas experience housing pressure? (CMHC data)
- SP4: Do healthcare systems scale with population growth? (provincial health data)
- SP5: What's the net effect — does immigration create disparities or reduce them?

**Stage 2 — Cross-Domain Analogy Search:** The agent identifies analogies from other domains:
- Urban planning research on "absorption capacity" of cities
- European studies on refugee settlement and regional economics
- Australian regional migration incentive program outcomes

These analogies provide analytical frameworks that no single Canadian dataset could suggest.

**Stage 3 — Synthesize and Hypothesize:** The agent generates testable hypotheses:
- H1: Cities with settlement rates >2% annual population growth AND housing vacancy <1% experience negative economic sentiment despite positive GDP growth
- H2: Healthcare strain (wait times, physician ratios) is a leading indicator of anti-immigration sentiment, preceding economic data by 6-12 months

**Stage 4 — Test and Reflect:** The agent tests hypotheses against the data. H1 is partially supported (4 of 6 high-growth cities show the pattern). H2 is strongly supported (correlation of 0.73 with 8-month lag).

**Stage 5 — Meta-Learn:** The agent records that healthcare capacity is a stronger predictor of regional integration outcomes than pure economic metrics — a finding that informs future investigations on regional policy.

**Impact:** An investigation that would take 3 months of multi-disciplinary research produces its core findings in 2 weeks. The healthcare-as-leading-indicator insight becomes the story's central thesis — an original finding that no single dataset could have revealed.

## The Revenue Impact

| Metric | Before | After | Change |
|---|---|---|---|
| Data analysis time per investigation | 3 weeks | 45 minutes (iterative) | -97% |
| Fact-check time per story | 1-2 hours | 15 minutes (review mode) | -85% |
| Stories published per month | 40 | 65 | +63% |
| Factual errors reaching publication | 2-3/year | 0 | -100% |
| Time for cross-domain investigations | 3 months | 2 weeks | -83% |
| Subscriber growth (accuracy reputation) | 2%/year | 8%/year (projected) | +300% |
| Grant funding competitiveness | Moderate | Strong (demonstrable rigor) | — |

**Projected annual impact:** 63% increase in story output + zero retractions + cross-domain investigation capability = stronger subscriber growth and grant competitiveness. Conservative estimate: $1.2M in additional annual revenue from subscriptions and expanded grant funding.

## What This Code Covers vs. Next Steps

### What Chapter 8's code demonstrates (this notebook):
- Data Analysis agent cognitive loop (intent → code → visualize → refine)
- Visualization recommendation system (query analysis → schema recognition → chart selection)
- Statistical reasoning (descriptive stats, OLS regression, z-score anomaly detection)
- Verification and Validation agent (claim extraction, evidence retrieval, NLI classification)
- BART-based NLI for fact-checking with confidence scoring
- Handling conflicting evidence across multiple sources (Figure 8.3)
- General Problem Solver five-stage cycle (decompose → analogy → hypothesize → test → meta-learn)
- Newsroom fact-checking case study with trusted database pattern

### Next steps CanadaFirst would need:
- **Knowledge retrieval** — RAG pipeline over federal databases, PBO reports, and CanadaFirst's archive (see Chapter 6)
- **Tool orchestration** — Connect agents to Statistics Canada API, SEDAR+, and Open Canada (see Chapter 7)
- **Ethical reasoning** — Ensure analysis doesn't amplify biases in government data (see Chapter 12)
- **Content generation** — Draft story sections from verified analysis (see Chapter 10)
- **Multi-agent coordination** — Data analyst, fact-checker, and General Problem Solver working as a research team (see Chapter 7)

---

*This use case is fictional and created for educational purposes. It demonstrates how the three agent types in Chapter 8 — Data Analysis, Verification and Validation, and General Problem Solver — apply to a realistic investigative journalism scenario. The newsroom fact-checker case study on pages 220-225 of the book directly inspired the verification pipeline.*
