# ─────────────────────────────────────────────────────────────────────────────
# mock_data.py — Synthetic Data Layer
# Chapter 14: Financial and Legal Domain Agents
# Book: 30 Agents Every AI Engineer Must Build — Imran Ahmad (Packt Publishing)
#
# This module provides all synthetic data required to run the notebook in
# Simulation Mode (no API keys needed). Every data structure is derived from
# and cross-referenced against a specific passage in Chapter 14.
#
# Exports:
#   - MOCK_STOCK_DATA              (B8,  Sec 14.1.1)
#   - MOCK_FINNHUB_QUOTES          (B9,  Sec 14.1.2)
#   - MOCK_FINNHUB_FINANCIALS      (B10, Sec 14.1.1)
#   - generate_mock_price_history() (B11, Sec 14.1.2)
#   - MOCK_TAVILY_NEWS             (B12, Sec 14.1.1)
#   - MOCK_CLIENT_PROFILES         (B13, Sec 14.1.3-14.1.4)
#   - MOCK_LEGAL_CASES             (B14, Sec 14.2.1-14.2.2)
#   - MOCK_CONTRACT                (B15, Sec 14.2.3)
#   - MOCK_INTER_AGENT_MESSAGE     (B16, Sec 14.1.4)
#
# Author: Imran Ahmad
# ─────────────────────────────────────────────────────────────────────────────

import numpy as np
from typing import Dict, List, Any


# ═══════════════════════════════════════════════════════════════════════════════
# B8: MOCK_STOCK_DATA — yfinance .info Schema
# Chapter Ref: Section 14.1.1, p.5
# Fidelity: Field names match ticker.info.get() keys used in get_market_data()
#           Fields: regularMarketPrice, marketCap, trailingPE, dayLow, dayHigh, volume
# ═══════════════════════════════════════════════════════════════════════════════

MOCK_STOCK_DATA: Dict[str, Dict[str, Any]] = {
    "AAPL": {
        "shortName": "Apple Inc.",
        "symbol": "AAPL",
        "regularMarketPrice": 178.72,
        "marketCap": 2_800_000_000_000,
        "trailingPE": 28.5,
        "forwardPE": 26.8,
        "dayLow": 176.80,
        "dayHigh": 179.45,
        "volume": 58_432_100,
        "averageVolume": 62_150_000,
        "fiftyTwoWeekLow": 124.17,
        "fiftyTwoWeekHigh": 182.34,
        "dividendYield": 0.0055,
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "currency": "USD",
    },
    "MSFT": {
        "shortName": "Microsoft Corporation",
        "symbol": "MSFT",
        "regularMarketPrice": 338.11,
        "marketCap": 2_500_000_000_000,
        "trailingPE": 32.1,
        "forwardPE": 29.4,
        "dayLow": 335.20,
        "dayHigh": 339.88,
        "volume": 25_617_300,
        "averageVolume": 28_440_000,
        "fiftyTwoWeekLow": 245.61,
        "fiftyTwoWeekHigh": 349.67,
        "dividendYield": 0.0082,
        "sector": "Technology",
        "industry": "Software - Infrastructure",
        "currency": "USD",
    },
    "GOOGL": {
        "shortName": "Alphabet Inc.",
        "symbol": "GOOGL",
        "regularMarketPrice": 141.80,
        "marketCap": 1_780_000_000_000,
        "trailingPE": 24.3,
        "forwardPE": 22.1,
        "dayLow": 139.50,
        "dayHigh": 142.60,
        "volume": 31_289_400,
        "averageVolume": 34_870_000,
        "fiftyTwoWeekLow": 100.48,
        "fiftyTwoWeekHigh": 153.78,
        "dividendYield": 0.0,
        "sector": "Technology",
        "industry": "Internet Content & Information",
        "currency": "USD",
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# B9: MOCK_FINNHUB_QUOTES — Finnhub Quote Response Schema
# Chapter Ref: Section 14.1.2, p.10
# Fidelity: quote.get("dp", 0) for price change percentage
#   AAPL  dp=0.71   → abs(0.71) < 2    → "Low Risk"
#   MSFT  dp=-1.24  → abs(-1.24) < 2   → "Low Risk"
#   GOOGL dp=2.99   → abs(2.99) > 2    → "Moderate Risk" (abs > 2 but < 5)
# ═══════════════════════════════════════════════════════════════════════════════

MOCK_FINNHUB_QUOTES: Dict[str, Dict[str, Any]] = {
    "AAPL": {
        "c": 178.72,       # Current price
        "d": 1.27,         # Dollar change
        "dp": 0.71,        # Percent change → Low Risk (abs < 2)
        "h": 179.45,       # High of the day
        "l": 176.80,       # Low of the day
        "o": 177.45,       # Open price
        "pc": 177.45,      # Previous close
        "t": 1700000000,   # Timestamp (Unix)
    },
    "MSFT": {
        "c": 338.11,
        "d": -4.23,
        "dp": -1.24,       # Percent change → Low Risk (abs < 2)
        "h": 339.88,
        "l": 335.20,
        "o": 342.34,
        "pc": 342.34,
        "t": 1700000000,
    },
    "GOOGL": {
        "c": 141.80,
        "d": 4.12,
        "dp": 2.99,        # Percent change → Moderate Risk (abs > 2 but < 5)
        "h": 142.60,
        "l": 139.50,
        "o": 137.68,
        "pc": 137.68,
        "t": 1700000000,
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# B10: MOCK_FINNHUB_FINANCIALS — company_basic_financials Response
# Chapter Ref: Section 14.1.1, p.6
# Fidelity: portfolio_analysis() reads metrics.get('peRatio'),
#           'revenueGrowth', '52WeekHigh', '52WeekLow'
#           All four keys present in each symbol's mock data.
# ═══════════════════════════════════════════════════════════════════════════════

MOCK_FINNHUB_FINANCIALS: Dict[str, Dict[str, Any]] = {
    "AAPL": {
        "symbol": "AAPL",
        "metric": {
            "peRatio": 28.5,
            "revenueGrowth": 0.078,
            "52WeekHigh": 182.34,
            "52WeekLow": 124.17,
            "epsGrowth": 0.112,
            "dividendYield": 0.55,
            "marketCapitalization": 2800000,
            "roeTTM": 0.1607,
            "currentRatio": 1.07,
            "debtEquity": 1.76,
            "grossMarginTTM": 0.4518,
            "netProfitMarginTTM": 0.2531,
        },
        "metricType": "all",
    },
    "MSFT": {
        "symbol": "MSFT",
        "metric": {
            "peRatio": 32.1,
            "revenueGrowth": 0.124,
            "52WeekHigh": 349.67,
            "52WeekLow": 245.61,
            "epsGrowth": 0.201,
            "dividendYield": 0.82,
            "marketCapitalization": 2500000,
            "roeTTM": 0.3891,
            "currentRatio": 1.77,
            "debtEquity": 0.42,
            "grossMarginTTM": 0.6912,
            "netProfitMarginTTM": 0.3604,
        },
        "metricType": "all",
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# B11: generate_mock_price_history() — Deterministic Price Series
# Chapter Ref: Section 14.1.2, p.11-12
# Fidelity: RiskScorer.compute_risk_score() needs hist['Close'].pct_change()
#           Returns dict with 'Close' list for 90 trading days.
#           Seeded random walk ensures reproducibility and valid VaR/volatility.
# ═══════════════════════════════════════════════════════════════════════════════

def generate_mock_price_history(
    symbol: str = "AAPL",
    days: int = 90,
    seed: int = 42,
) -> Dict[str, List[float]]:
    """Generate deterministic mock daily closing prices for a given symbol.

    Uses a geometric random walk with symbol-specific parameters to produce
    realistic price series suitable for VaR, CVaR, and volatility calculations.

    Args:
        symbol: Stock ticker symbol (affects base price and volatility seed)
        days:   Number of trading days to generate (default 90)
        seed:   Random seed for reproducibility

    Returns:
        Dict with 'Close' key containing a list of daily closing prices.
        Compatible with pd.DataFrame(data)['Close'].pct_change() workflow.

    Author: Imran Ahmad
    Chapter Ref: Section 14.1.2, p.11-12
    """
    # Symbol-specific base prices and volatility characteristics
    symbol_params = {
        "AAPL":  {"base_price": 170.00, "annual_vol": 0.22, "drift": 0.0003},
        "MSFT":  {"base_price": 330.00, "annual_vol": 0.20, "drift": 0.0004},
        "GOOGL": {"base_price": 135.00, "annual_vol": 0.26, "drift": 0.0002},
    }

    params = symbol_params.get(symbol, {"base_price": 100.0, "annual_vol": 0.25, "drift": 0.0003})

    # Deterministic seed: combine provided seed with symbol hash for uniqueness
    symbol_seed = seed + sum(ord(c) for c in symbol)
    rng = np.random.RandomState(symbol_seed)

    # Generate daily returns via geometric Brownian motion
    daily_vol = params["annual_vol"] / np.sqrt(252)
    daily_returns = rng.normal(loc=params["drift"], scale=daily_vol, size=days)

    # Convert returns to price series
    prices = [params["base_price"]]
    for ret in daily_returns:
        next_price = prices[-1] * (1 + ret)
        prices.append(round(next_price, 2))

    # Return the closing prices (drop the initial seed price, keep 'days' points)
    close_prices = prices[1:]

    return {
        "Close": close_prices,
        "Volume": [int(rng.uniform(20_000_000, 80_000_000)) for _ in range(days)],
        "High": [round(p * (1 + rng.uniform(0.002, 0.015)), 2) for p in close_prices],
        "Low": [round(p * (1 - rng.uniform(0.002, 0.015)), 2) for p in close_prices],
        "Open": [round(p * (1 + rng.uniform(-0.005, 0.005)), 2) for p in close_prices],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# B12: MOCK_TAVILY_NEWS — TavilySearchResults Output Format
# Chapter Ref: Section 14.1.1, p.7
# Fidelity: TavilySearchResults(max_results=5) returns exactly 5 results
#           Each result has: title, url, content, score
# ═══════════════════════════════════════════════════════════════════════════════

MOCK_TAVILY_NEWS: List[Dict[str, Any]] = [
    {
        "title": "Federal Reserve Holds Interest Rates Steady, Signals Patience on Cuts",
        "url": "https://example.com/news/fed-rates-steady-2024",
        "content": (
            "The Federal Reserve voted unanimously to maintain the federal funds rate "
            "at its current level, citing persistent inflation above the 2% target. "
            "Chair Powell indicated the committee needs further evidence of cooling "
            "price pressures before considering rate reductions. Bond markets adjusted "
            "expectations, now pricing in the first cut for Q3."
        ),
        "score": 0.97,
    },
    {
        "title": "Tech Earnings Season: Mixed Results Highlight AI Investment Surge",
        "url": "https://example.com/news/tech-earnings-ai-2024",
        "content": (
            "Major technology companies reported mixed quarterly results, with revenue "
            "growth slowing at several firms while capital expenditure on artificial "
            "intelligence infrastructure surged. Analysts noted that AI-related spending "
            "is expected to exceed $200 billion industry-wide this fiscal year, raising "
            "questions about near-term return on investment."
        ),
        "score": 0.94,
    },
    {
        "title": "S&P 500 Reaches New All-Time High on Strong Employment Data",
        "url": "https://example.com/news/sp500-record-high-2024",
        "content": (
            "The S&P 500 index closed at a new record high, buoyed by a stronger-than-"
            "expected jobs report showing the economy added 275,000 positions in the "
            "latest month. The unemployment rate held steady at 3.7%, supporting the "
            "soft-landing narrative. Technology and healthcare sectors led the advance."
        ),
        "score": 0.91,
    },
    {
        "title": "Global Supply Chain Recovery Eases Inflation Pressures",
        "url": "https://example.com/news/supply-chain-inflation-2024",
        "content": (
            "A comprehensive analysis of global shipping data shows container freight "
            "rates have declined 40% from their peak, signaling meaningful improvement "
            "in supply chain bottlenecks. Economists expect this trend to contribute to "
            "disinflation in goods categories over the coming quarters, potentially "
            "giving central banks more room to ease monetary policy."
        ),
        "score": 0.88,
    },
    {
        "title": "Semiconductor Sector Rallies on Data Center Demand Forecast",
        "url": "https://example.com/news/semiconductor-rally-2024",
        "content": (
            "Semiconductor stocks rallied broadly after industry forecasters projected "
            "a 25% increase in data center chip demand for the coming year, driven by "
            "enterprise AI adoption and cloud expansion. Leading chipmakers reported "
            "order backlogs extending into 2025, with advanced node capacity fully "
            "booked across major foundries."
        ),
        "score": 0.85,
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# B13: MOCK_CLIENT_PROFILES — Investor Profiles
# Chapter Ref: Section 14.1.3-14.1.4, p.18
# Fidelity:
#   retail_client_4521: "$50,000 to invest", "moderate growth", "ten years"
#   conservative_client_7832: "$25,000 to invest", "conservative", "five years"
# ═══════════════════════════════════════════════════════════════════════════════

MOCK_CLIENT_PROFILES: Dict[str, Dict[str, Any]] = {
    "retail_client_4521": {
        "client_id": "retail_client_4521",
        "name": "Sarah Chen",
        "initial_investment": 50_000,
        "risk_tolerance": "moderate",
        "investment_horizon": "10 years",
        "investment_goal": "moderate growth",
        "age": 34,
        "annual_income": 95_000,
        "existing_portfolio_value": 120_000,
        "tax_filing_status": "single",
        "state_of_residence": "CA",
        "experience_level": "intermediate",
        "constraints": [
            "No tobacco or firearms companies",
            "Maximum 40% in any single sector",
        ],
    },
    "conservative_client_7832": {
        "client_id": "conservative_client_7832",
        "name": "Robert Martinez",
        "initial_investment": 25_000,
        "risk_tolerance": "conservative",
        "investment_horizon": "5 years",
        "investment_goal": "capital preservation with modest income",
        "age": 58,
        "annual_income": 72_000,
        "existing_portfolio_value": 450_000,
        "tax_filing_status": "married_filing_jointly",
        "state_of_residence": "TX",
        "experience_level": "beginner",
        "constraints": [
            "No cryptocurrency exposure",
            "Minimum 40% fixed income",
            "Prefer dividend-paying equities",
        ],
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# B14: MOCK_LEGAL_CASES — Legal Knowledge Base Cases
# Chapter Ref: Section 14.2.1-14.2.2, p.20-23
# Fidelity:
#   6 cases with: case_name, citation, court, jurisdiction, authority_level, status
#   Cases 0-4: Real-style cases with proper court hierarchy and authority 3-10
#   Case 5 (Varghese): fabricated case, status="fabricated", authority=0
#              Designed to be caught by verify_citations() per Schwartz incident
# ═══════════════════════════════════════════════════════════════════════════════

MOCK_LEGAL_CASES: List[Dict[str, Any]] = [
    {
        "case_id": "case_001",
        "case_name": "SEC v. Capital Growth Financial Services",
        "citation": "SEC v. Capital Growth, 391 F.3d 311 (2d Cir. 2004)",
        "court": "United States Court of Appeals, Second Circuit",
        "jurisdiction": "federal",
        "authority_level": 8,
        "year": 2004,
        "status": "verified",
        "key_issues": ["fiduciary duty", "investment advisor regulation", "SEC enforcement"],
        "summary": (
            "The Second Circuit upheld the SEC's enforcement action against an investment "
            "advisory firm for failing to disclose material conflicts of interest to clients. "
            "The court established that investment advisors have an affirmative duty of utmost "
            "good faith and full disclosure of all material facts, as well as an obligation "
            "to employ reasonable care to avoid misleading clients."
        ),
        "holding": (
            "Investment advisors owe fiduciary duties under the Investment Advisers Act of "
            "1940 that include both a duty of loyalty and a duty of care, requiring full "
            "disclosure of material conflicts."
        ),
    },
    {
        "case_id": "case_002",
        "case_name": "Transamerica Mortgage Advisors v. Lewis",
        "citation": "Transamerica v. Lewis, 444 U.S. 11 (1979)",
        "court": "Supreme Court of the United States",
        "jurisdiction": "federal",
        "authority_level": 10,
        "year": 1979,
        "status": "verified",
        "key_issues": ["implied private right of action", "Investment Advisers Act", "fiduciary duty"],
        "summary": (
            "The Supreme Court held that the Investment Advisers Act of 1940 creates a "
            "limited implied private right of action for rescission of investment advisory "
            "contracts but does not authorize awards of monetary damages. This case defined "
            "the boundaries of private enforcement under the Act."
        ),
        "holding": (
            "Section 215 of the Investment Advisers Act grants courts the authority to void "
            "investment advisory contracts obtained through fraud, but the Act does not "
            "provide for a general damages remedy."
        ),
    },
    {
        "case_id": "case_003",
        "case_name": "Goldstein v. SEC",
        "citation": "Goldstein v. SEC, 451 F.3d 873 (D.C. Cir. 2006)",
        "court": "United States Court of Appeals, D.C. Circuit",
        "jurisdiction": "federal",
        "authority_level": 8,
        "year": 2006,
        "status": "verified",
        "key_issues": ["hedge fund regulation", "client definition", "SEC rulemaking authority"],
        "summary": (
            "The D.C. Circuit vacated an SEC rule that required hedge fund advisors to "
            "register under the Investment Advisers Act by 'looking through' funds to count "
            "individual investors as clients. The court found the SEC's interpretation of "
            "'client' to be unreasonable and beyond its statutory authority."
        ),
        "holding": (
            "Hedge fund investors are not 'clients' of the fund's investment advisor for "
            "purposes of the registration threshold under the Investment Advisers Act."
        ),
    },
    {
        "case_id": "case_004",
        "case_name": "Jones v. Harris Associates L.P.",
        "citation": "Jones v. Harris Associates, 559 U.S. 335 (2010)",
        "court": "Supreme Court of the United States",
        "jurisdiction": "federal",
        "authority_level": 10,
        "year": 2010,
        "status": "verified",
        "key_issues": ["excessive fees", "mutual fund advisory fees", "fiduciary duty to fund shareholders"],
        "summary": (
            "The Supreme Court held that the standard for evaluating whether an investment "
            "advisor's fee is excessive under the Investment Company Act is whether the fee "
            "is so disproportionately large that it bears no reasonable relationship to the "
            "services rendered and could not have been the product of arm's-length bargaining. "
            "The Court rejected the Seventh Circuit's proposed sole reliance on market forces."
        ),
        "holding": (
            "To establish that an investment advisor has breached fiduciary duty with respect "
            "to fees, plaintiffs must show the fee is outside the range of arm's-length "
            "bargaining, applying the Gartenberg standard."
        ),
    },
    {
        "case_id": "case_005",
        "case_name": "In re Bernard L. Madoff Investment Securities LLC",
        "citation": "In re Madoff, 654 F.3d 229 (2d Cir. 2011)",
        "court": "United States Court of Appeals, Second Circuit",
        "jurisdiction": "federal",
        "authority_level": 8,
        "year": 2011,
        "status": "verified",
        "key_issues": ["Ponzi scheme", "clawback actions", "Securities Investor Protection Act"],
        "summary": (
            "The Second Circuit addressed the methodology for calculating net equity claims "
            "of investors in the Madoff Ponzi scheme, holding that the 'net investment method' "
            "(cash in minus cash out) rather than the 'last statement method' was the "
            "appropriate measure for determining customer claims under SIPA."
        ),
        "holding": (
            "In a Ponzi scheme liquidation under SIPA, net equity is properly calculated "
            "using the net investment method based on actual cash deposits and withdrawals, "
            "not fictitious account statements."
        ),
    },
    {
        "case_id": "case_006",
        "case_name": "Varghese v. Tech Corp International",
        "citation": "Varghese v. Tech Corp, No. 23-cv-1847 (S.D.N.Y. 2023)",
        "court": "United States District Court, Southern District of New York",
        "jurisdiction": "federal",
        "authority_level": 0,
        "year": 2023,
        "status": "fabricated",
        "key_issues": ["trade secret misappropriation", "non-compete enforcement", "injunctive relief"],
        "summary": (
            "This case involves allegations of trade secret misappropriation by a former "
            "employee who joined a competing firm. The plaintiff sought a preliminary "
            "injunction to prevent the defendant from using proprietary algorithms. "
            "NOTE: This is a FABRICATED case entry — it does not exist in any court record. "
            "It is included specifically to test the citation verification pipeline described "
            "in Section 14.2.4 of the chapter, inspired by the Schwartz v. Avianca incident "
            "where attorneys submitted hallucinated case citations generated by an LLM."
        ),
        "holding": (
            "FABRICATED — No holding exists. This entry is designed to be caught by "
            "the verify_citations() function."
        ),
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# B15: MOCK_CONTRACT — 8-Clause Contract for Analysis
# Chapter Ref: Section 14.2.3, p.28-30
# Fidelity: 8 sections including:
#   - Indemnification (HIGH risk)
#   - Liability cap (HIGH risk)
#   - Missing GDPR addendum (CRITICAL compliance gap)
#   - Termination clause (MEDIUM risk — lacks mutual termination rights)
# ═══════════════════════════════════════════════════════════════════════════════

MOCK_CONTRACT: Dict[str, Any] = {
    "contract_id": "SVC-2024-00847",
    "title": "Master Services Agreement",
    "parties": {
        "party_a": "Acme Financial Technologies, Inc.",
        "party_b": "GlobalData Analytics, Ltd.",
    },
    "effective_date": "2024-01-15",
    "term": "36 months",
    "governing_law": "State of New York",
    "clauses": [
        {
            "section": 1,
            "title": "Scope of Services",
            "classification": "operational",
            "risk_level": "LOW",
            "text": (
                "Provider agrees to deliver data analytics services including portfolio "
                "risk modeling, market sentiment analysis, and automated compliance "
                "reporting as further described in Exhibit A (Statement of Work). "
                "Services shall be performed in accordance with industry best practices "
                "and applicable regulatory requirements."
            ),
        },
        {
            "section": 2,
            "title": "Fees and Payment Terms",
            "classification": "financial",
            "risk_level": "LOW",
            "text": (
                "Client shall pay Provider a monthly fee of $45,000 for the Base "
                "Services package, with additional charges for Enhanced Analytics as "
                "set forth in Exhibit B (Fee Schedule). Payment is due within thirty "
                "(30) days of invoice date. Late payments shall accrue interest at "
                "1.5% per month."
            ),
        },
        {
            "section": 3,
            "title": "Data Protection and Privacy",
            "classification": "compliance",
            "risk_level": "MEDIUM",
            "text": (
                "Provider shall implement reasonable administrative, technical, and "
                "physical safeguards to protect Client Data in accordance with "
                "applicable data protection laws. Provider shall promptly notify "
                "Client of any data breach affecting Client Data. Provider shall "
                "process Client Data only as necessary to perform the Services."
            ),
            "compliance_note": (
                "WARNING: This clause references generic 'applicable data protection "
                "laws' but does not include a specific GDPR Data Processing Addendum "
                "(DPA). If either party processes personal data of EU/EEA residents, "
                "a DPA with Standard Contractual Clauses is required under GDPR "
                "Article 28."
            ),
        },
        {
            "section": 4,
            "title": "Indemnification",
            "classification": "liability",
            "risk_level": "HIGH",
            "text": (
                "Provider shall indemnify, defend, and hold harmless Client and its "
                "officers, directors, employees, and agents from and against any and "
                "all claims, damages, losses, liabilities, costs, and expenses "
                "(including reasonable attorneys' fees) arising out of or relating to "
                "(a) Provider's breach of this Agreement, (b) Provider's negligence "
                "or willful misconduct, (c) any violation of applicable law by "
                "Provider, or (d) any infringement of third-party intellectual "
                "property rights by the Services or deliverables."
            ),
            "risk_note": (
                "HIGH RISK: Indemnification is asymmetric — Provider bears unlimited "
                "indemnification obligations with no reciprocal indemnification from "
                "Client. The scope is broad, covering all claims 'arising out of or "
                "relating to' the agreement, which courts may interpret expansively."
            ),
        },
        {
            "section": 5,
            "title": "Limitation of Liability",
            "classification": "liability",
            "risk_level": "HIGH",
            "text": (
                "EXCEPT FOR INDEMNIFICATION OBLIGATIONS UNDER SECTION 4, IN NO EVENT "
                "SHALL EITHER PARTY'S AGGREGATE LIABILITY UNDER THIS AGREEMENT EXCEED "
                "THE TOTAL FEES PAID BY CLIENT IN THE THREE (3) MONTHS PRECEDING THE "
                "EVENT GIVING RISE TO LIABILITY. IN NO EVENT SHALL EITHER PARTY BE "
                "LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR "
                "PUNITIVE DAMAGES."
            ),
            "risk_note": (
                "HIGH RISK: The liability cap of three (3) months of fees ($135,000) "
                "is significantly below industry standard, which typically sets the "
                "cap at twelve (12) months of fees. Combined with the unlimited "
                "indemnification in Section 4, this creates an imbalanced risk "
                "allocation heavily favoring the Client."
            ),
        },
        {
            "section": 6,
            "title": "Intellectual Property Rights",
            "classification": "ip",
            "risk_level": "MEDIUM",
            "text": (
                "All intellectual property created by Provider in the course of "
                "performing Services ('Work Product') shall be owned by Client upon "
                "full payment. Provider retains rights to its pre-existing "
                "intellectual property and general knowledge, skills, and experience "
                "gained during performance of the Services."
            ),
        },
        {
            "section": 7,
            "title": "Termination",
            "classification": "operational",
            "risk_level": "MEDIUM",
            "text": (
                "Client may terminate this Agreement for convenience upon sixty (60) "
                "days' written notice. Either party may terminate for cause upon "
                "thirty (30) days' written notice of a material breach, provided "
                "the breaching party fails to cure such breach within the notice "
                "period. Upon termination, Provider shall deliver all Work Product "
                "and Client Data within fifteen (15) business days."
            ),
            "risk_note": (
                "MEDIUM RISK: Termination for convenience is unilateral — only Client "
                "has the right to terminate without cause. Provider lacks a reciprocal "
                "convenience termination right, creating a lock-in risk for the full "
                "36-month term."
            ),
        },
        {
            "section": 8,
            "title": "Confidentiality",
            "classification": "compliance",
            "risk_level": "LOW",
            "text": (
                "Each party agrees to hold in confidence all Confidential Information "
                "of the other party and to use such information only for purposes of "
                "this Agreement. Confidential Information shall not include information "
                "that (a) is or becomes publicly available without breach, (b) was "
                "known to the receiving party prior to disclosure, (c) is independently "
                "developed without use of Confidential Information, or (d) is received "
                "from a third party without restriction."
            ),
        },
    ],
    "missing_provisions": [
        {
            "provision": "GDPR Data Processing Addendum (DPA)",
            "severity": "CRITICAL",
            "description": (
                "No Data Processing Addendum with Standard Contractual Clauses is "
                "included. If either party processes personal data of EU/EEA data "
                "subjects, this omission creates a GDPR compliance gap under Article 28. "
                "Remediation: Attach a DPA as an exhibit before contract execution."
            ),
        },
        {
            "provision": "Insurance Requirements",
            "severity": "MEDIUM",
            "description": (
                "No requirement for Provider to maintain professional liability "
                "(errors and omissions) insurance. Given the financial data services "
                "being provided, a minimum coverage of $2M per occurrence is "
                "industry standard."
            ),
        },
        {
            "provision": "Dispute Resolution Mechanism",
            "severity": "LOW",
            "description": (
                "No arbitration or mediation clause is included. In the absence of "
                "an alternative dispute resolution provision, disputes default to "
                "litigation in New York courts, which may be slower and more expensive."
            ),
        },
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
# B16: MOCK_INTER_AGENT_MESSAGE — Inter-Agent Communication Protocol
# Chapter Ref: Section 14.1.4, p.19
# Fidelity: Exact JSON message protocol from chapter
#   us_equities: 0.45, international_equities: 0.20,
#   fixed_income: 0.25, alternatives: 0.10
# ═══════════════════════════════════════════════════════════════════════════════

MOCK_INTER_AGENT_MESSAGE: Dict[str, Any] = {
    "message_id": "msg_advisor_20240115_001",
    "source_agent": "financial_planning_agent",
    "target_agent": "compliance_validation_agent",
    "timestamp": "2024-01-15T14:32:18Z",
    "message_type": "advisory_plan_submission",
    "client_id": "retail_client_4521",
    "payload": {
        "plan_summary": "Moderate growth portfolio for 10-year investment horizon",
        "initial_investment": 50_000,
        "risk_tolerance": "moderate",
        "investment_horizon": "10 years",
        "recommended_allocation": {
            "us_equities": 0.45,
            "international_equities": 0.20,
            "fixed_income": 0.25,
            "alternatives": 0.10,
        },
        "allocation_details": {
            "us_equities": {
                "percentage": 0.45,
                "amount": 22_500,
                "strategy": "Diversified large-cap growth and value blend via index funds",
                "primary_vehicles": ["VTI", "VOO", "QQQ"],
            },
            "international_equities": {
                "percentage": 0.20,
                "amount": 10_000,
                "strategy": "Developed markets core with emerging market satellite",
                "primary_vehicles": ["VXUS", "VWO"],
            },
            "fixed_income": {
                "percentage": 0.25,
                "amount": 12_500,
                "strategy": "Investment-grade corporate and government bond ladder",
                "primary_vehicles": ["BND", "VCIT", "VGSH"],
            },
            "alternatives": {
                "percentage": 0.10,
                "amount": 5_000,
                "strategy": "REITs and broad commodity exposure for inflation hedge",
                "primary_vehicles": ["VNQ", "DJP"],
            },
        },
        "expected_metrics": {
            "expected_annual_return": 0.072,
            "expected_annual_volatility": 0.124,
            "sharpe_ratio_estimate": 0.42,
            "max_drawdown_estimate": -0.18,
        },
        "risk_assessment": {
            "portfolio_risk_score": 5.8,
            "risk_category": "Moderate",
            "var_95_daily": -0.0234,
            "cvar_95_daily": -0.0312,
        },
        "compliance_checklist": {
            "suitability_matched": True,
            "concentration_limit_check": True,
            "disclosure_requirements_met": True,
            "regulatory_filing_needed": False,
        },
    },
    "status": "pending_compliance_review",
}


# ═══════════════════════════════════════════════════════════════════════════════
# Module Exports
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "MOCK_STOCK_DATA",
    "MOCK_FINNHUB_QUOTES",
    "MOCK_FINNHUB_FINANCIALS",
    "generate_mock_price_history",
    "MOCK_TAVILY_NEWS",
    "MOCK_CLIENT_PROFILES",
    "MOCK_LEGAL_CASES",
    "MOCK_CONTRACT",
    "MOCK_INTER_AGENT_MESSAGE",
]
