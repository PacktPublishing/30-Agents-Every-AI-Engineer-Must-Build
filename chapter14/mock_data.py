# mock_data.py
# Chapter 14: Financial and Legal Domain Agents
# Book: 30 Agents Every AI Engineer Must Build — Imran Ahmad (Packt Publishing)
# Author: Imran Ahmad
#
# Synthetic data derived directly from Chapter 14's code examples, case studies,
# and narrative descriptions. Every data structure maps to a specific chapter
# section and is designed to produce chapter-faithful output in Simulation Mode.

import random
import math


# ═══════════════════════════════════════════════════════════════════════════════
# B8: MOCK_STOCK_DATA — yfinance .info schema
# Ref: Section 14.1.1 (p.5), get_market_data() — fields: currentPrice,
#      marketCap, trailingPE, dayHigh, dayLow, volume
# ═══════════════════════════════════════════════════════════════════════════════

MOCK_STOCK_DATA = {
    "AAPL": {
        "currentPrice": 178.72,
        "marketCap": 2_800_000_000_000,
        "trailingPE": 28.5,
        "dayHigh": 179.80,
        "dayLow": 176.50,
        "volume": 52_340_000,
        "shortName": "Apple Inc.",
        "sector": "Technology",
        "fiftyTwoWeekHigh": 199.62,
        "fiftyTwoWeekLow": 143.90,
    },
    "MSFT": {
        "currentPrice": 378.91,
        "marketCap": 2_810_000_000_000,
        "trailingPE": 34.2,
        "dayHigh": 380.15,
        "dayLow": 376.40,
        "volume": 22_180_000,
        "shortName": "Microsoft Corporation",
        "sector": "Technology",
        "fiftyTwoWeekHigh": 420.82,
        "fiftyTwoWeekLow": 309.45,
    },
    "GOOGL": {
        "currentPrice": 141.55,
        "marketCap": 1_770_000_000_000,
        "trailingPE": 25.1,
        "dayHigh": 142.80,
        "dayLow": 139.95,
        "volume": 28_700_000,
        "shortName": "Alphabet Inc.",
        "sector": "Technology",
        "fiftyTwoWeekHigh": 155.20,
        "fiftyTwoWeekLow": 115.83,
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# B9: MOCK_FINNHUB_QUOTES — Finnhub quote() response schema
# Ref: Section 14.1.2 (p.10), risk_assessment() — key field: dp (daily %)
#
# Risk classification thresholds from chapter (p.10):
#   abs(dp) > 5  → HIGH RISK
#   abs(dp) > 2  → MODERATE RISK
#   else         → LOW RISK
#
# AAPL: dp=0.71 → LOW (abs < 2)
# MSFT: dp=-5.23 → HIGH (abs > 5)
# GOOGL: dp=2.99 → MODERATE (abs > 2, < 5)
# ═══════════════════════════════════════════════════════════════════════════════

MOCK_FINNHUB_QUOTES = {
    "AAPL": {
        "c": 178.72,     # Current price
        "d": 1.27,       # Change
        "dp": 0.71,      # Percent change → LOW RISK
        "h": 179.80,     # High
        "l": 176.50,     # Low
        "o": 177.45,     # Open
        "pc": 177.45,    # Previous close
        "t": 1705334400, # Timestamp
    },
    "MSFT": {
        "c": 378.91,
        "d": -20.95,
        "dp": -5.23,     # Percent change → HIGH RISK
        "h": 400.10,
        "l": 376.40,
        "o": 399.86,
        "pc": 399.86,
        "t": 1705334400,
    },
    "GOOGL": {
        "c": 141.55,
        "d": 4.10,
        "dp": 2.99,      # Percent change → MODERATE RISK
        "h": 142.80,
        "l": 137.45,
        "o": 137.45,
        "pc": 137.45,
        "t": 1705334400,
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# B10: MOCK_FINNHUB_FINANCIALS — company_basic_financials response
# Ref: Section 14.1.1 (p.6), portfolio_analysis() — fields: peRatio,
#      revenueGrowth, 52WeekHigh, 52WeekLow
# ═══════════════════════════════════════════════════════════════════════════════

MOCK_FINNHUB_FINANCIALS = {
    "AAPL": {
        "metric": {
            "peRatio": 28.5,
            "revenueGrowth": 7.8,
            "52WeekHigh": 199.62,
            "52WeekLow": 143.90,
            "marketCapitalization": 2800000,
            "dividendYield": 0.56,
            "epsGrowth": 10.2,
        },
        "symbol": "AAPL",
    },
    "MSFT": {
        "metric": {
            "peRatio": 34.2,
            "revenueGrowth": 12.4,
            "52WeekHigh": 420.82,
            "52WeekLow": 309.45,
            "marketCapitalization": 2810000,
            "dividendYield": 0.74,
            "epsGrowth": 15.3,
        },
        "symbol": "MSFT",
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# B11: generate_mock_price_history() — Deterministic daily closes
# Ref: Section 14.1.2 (p.11-12), RiskScorer.compute_risk_score() needs
#      hist['Close'].pct_change().dropna() for VaR/volatility computation.
#      Uses seeded random walk for reproducibility.
# ═══════════════════════════════════════════════════════════════════════════════

def generate_mock_price_history(symbol: str = "AAPL",
                                days: int = 90,
                                seed: int = 42) -> dict:
    """Generate deterministic mock price history for risk scoring.

    Returns a dict with 'Close' list suitable for pandas DataFrame
    construction: pd.DataFrame(data). The pct_change() of Close values
    produces valid returns for VaR, volatility, and drawdown computation.

    Args:
        symbol: Stock ticker symbol (affects base price).
        days: Number of trading days to generate.
        seed: Random seed for reproducibility.

    Returns:
        dict with 'Close' key containing a list of daily close prices.

    Author: Imran Ahmad
    Ref: Chapter 14, Section 14.1.2 (p.11-12)
    """
    rng = random.Random(seed)

    base_prices = {
        "AAPL": 178.72,
        "MSFT": 378.91,
        "GOOGL": 141.55,
    }
    base = base_prices.get(symbol.upper(), 150.00)

    closes = []
    price = base
    for _ in range(days):
        # Daily return: slight upward drift with realistic volatility
        daily_return = rng.gauss(0.0003, 0.015)
        price *= (1 + daily_return)
        closes.append(round(price, 2))

    return {"Close": closes}


# ═══════════════════════════════════════════════════════════════════════════════
# B12: MOCK_TAVILY_NEWS — TavilySearchResults output format
# Ref: Section 14.1.1 (p.7), financial_news_tool = TavilySearchResults(
#      max_results=5). Exactly 5 results with title, url, content, score.
# ═══════════════════════════════════════════════════════════════════════════════

MOCK_TAVILY_NEWS = [
    {
        "title": "Federal Reserve Signals Cautious Approach to Rate Adjustments",
        "url": "https://example.com/fed-rate-outlook",
        "content": (
            "The Federal Reserve indicated it will maintain a cautious approach "
            "to interest rate adjustments in the coming quarter, citing stable "
            "inflation data and resilient labor markets. Analysts expect rates "
            "to remain unchanged through mid-year."
        ),
        "score": 0.95,
    },
    {
        "title": "Technology Sector Posts Strong Q4 Earnings",
        "url": "https://example.com/tech-q4-earnings",
        "content": (
            "Major technology companies reported better-than-expected fourth "
            "quarter earnings. Apple, Microsoft, and Alphabet all beat analyst "
            "estimates, driven by cloud computing growth and AI investment."
        ),
        "score": 0.91,
    },
    {
        "title": "Global Trade Outlook Improves Amid Diplomatic Progress",
        "url": "https://example.com/trade-outlook",
        "content": (
            "Global markets responded positively to improved trade negotiations "
            "between major economies. Supply chain constraints continue to ease, "
            "supporting manufacturing recovery across emerging markets."
        ),
        "score": 0.87,
    },
    {
        "title": "ESG Investing Reaches Record Inflows in 2025",
        "url": "https://example.com/esg-investing-2025",
        "content": (
            "Environmental, social, and governance focused funds attracted "
            "record capital inflows, with total ESG assets under management "
            "surpassing $50 trillion globally. Regulatory mandates in the EU "
            "and Asia drove institutional adoption."
        ),
        "score": 0.83,
    },
    {
        "title": "Cryptocurrency Market Stabilizes After Regulatory Clarity",
        "url": "https://example.com/crypto-regulation",
        "content": (
            "Cryptocurrency markets experienced reduced volatility following "
            "the passage of comprehensive digital asset legislation. Market "
            "participants welcomed the regulatory certainty, which is expected "
            "to encourage institutional participation."
        ),
        "score": 0.79,
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# B13: MOCK_CLIENT_PROFILES — Client investment profiles
# Ref: Section 14.1.3–14.1.4 (p.14-18), case study (p.18):
#   Moderate client: "$50,000 to invest", "moderate growth", "ten years"
#   Conservative client: $25,000, 5-year horizon
# ═══════════════════════════════════════════════════════════════════════════════

MOCK_CLIENT_PROFILES = {
    "retail_client_4521": {
        "client_id": "retail_client_4521",
        "name": "Sarah Chen",
        "risk_tolerance": "moderate",
        "max_risk_tolerance": 6.5,
        "investment_horizon": "10 years",
        "initial_investment": 50000,
        "financial_goals": ["moderate growth", "retirement savings"],
        "constraints": [
            "No tobacco stocks",
            "ESG preference",
        ],
        "age": 35,
        "income_bracket": "middle",
        "experience_level": "intermediate",
    },
    "retail_client_7832": {
        "client_id": "retail_client_7832",
        "name": "Robert Martinez",
        "risk_tolerance": "conservative",
        "max_risk_tolerance": 4.0,
        "investment_horizon": "5 years",
        "initial_investment": 25000,
        "financial_goals": ["capital preservation", "emergency fund growth"],
        "constraints": [
            "No international exposure above 15%",
            "Minimum 40% fixed income",
        ],
        "age": 58,
        "income_bracket": "upper-middle",
        "experience_level": "beginner",
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# B14: MOCK_LEGAL_CASES — Legal case database
# Ref: Section 14.2.1–14.2.2 (p.20-23)
#      6 cases with court hierarchy, jurisdiction, authority levels 0-10.
#      Case 5 (index 5) is the FABRICATED "Varghese" case from the
#      Schwartz incident (p.23 Note box) — designed to be caught by
#      verify_citations().
# ═══════════════════════════════════════════════════════════════════════════════

MOCK_LEGAL_CASES = [
    {
        "name": "Smith v. TechCorp International",
        "citation": "589 U.S. 412 (2024)",
        "court": "Supreme Court of the United States",
        "jurisdiction": "federal",
        "date": "2024-03-15",
        "authority_level": 10,
        "status": "good_law",
        "issues": ["data privacy", "corporate liability", "duty of care"],
        "holdings": [
            "Corporations have an affirmative duty to implement reasonable "
            "data protection measures proportional to the sensitivity of "
            "the data they collect."
        ],
        "text": (
            "Smith v. TechCorp International established that technology "
            "companies bear an affirmative duty of care in protecting user "
            "data. The Court held that the standard of reasonableness must "
            "be evaluated against industry best practices at the time of "
            "the alleged breach."
        ),
    },
    {
        "name": "Johnson v. DataFlow Systems",
        "citation": "78 F.4th 231 (9th Cir. 2023)",
        "court": "United States Court of Appeals, Ninth Circuit",
        "jurisdiction": "federal",
        "date": "2023-08-22",
        "authority_level": 8,
        "status": "good_law",
        "issues": ["personal jurisdiction", "e-commerce", "due process"],
        "holdings": [
            "Personal jurisdiction over foreign e-commerce entities "
            "requires proof of purposeful direction of activities toward "
            "forum residents, not mere accessibility of a website."
        ],
        "text": (
            "Johnson v. DataFlow Systems addressed the scope of personal "
            "jurisdiction over foreign corporations in e-commerce disputes. "
            "The Ninth Circuit refined the purposeful direction test, holding "
            "that website accessibility alone does not confer jurisdiction."
        ),
    },
    {
        "name": "Williams v. SecureNet Holdings",
        "citation": "45 Cal.App.5th 892 (2023)",
        "court": "California Court of Appeal",
        "jurisdiction": "california",
        "date": "2023-11-08",
        "authority_level": 5,
        "status": "good_law",
        "issues": ["negligence", "cybersecurity", "damages"],
        "holdings": [
            "Plaintiffs in data breach cases must demonstrate actual harm "
            "beyond speculative risk of future identity theft to establish "
            "standing for damages."
        ],
        "text": (
            "Williams v. SecureNet Holdings clarified the damages standard "
            "in California data breach litigation, requiring plaintiffs to "
            "show concrete injury rather than speculative future harm."
        ),
    },
    {
        "name": "Anderson v. CloudFirst Inc.",
        "citation": "312 F.Supp.3d 445 (S.D.N.Y. 2024)",
        "court": "United States District Court, Southern District of New York",
        "jurisdiction": "federal",
        "date": "2024-01-19",
        "authority_level": 3,
        "status": "good_law",
        "issues": ["GDPR compliance", "cross-border data transfer",
                    "contractual obligations"],
        "holdings": [
            "Contractual data processing agreements that fail to address "
            "cross-border transfer mechanisms are insufficient to establish "
            "GDPR compliance."
        ],
        "text": (
            "Anderson v. CloudFirst Inc. examined GDPR compliance obligations "
            "for US-based cloud service providers handling EU citizen data. "
            "The court emphasized the need for explicit contractual provisions "
            "covering cross-border data transfer mechanisms."
        ),
    },
    {
        "name": "Brown v. National Insurance Group",
        "citation": "156 N.E.3d 789 (Ill. 2022)",
        "court": "Supreme Court of Illinois",
        "jurisdiction": "illinois",
        "date": "2022-06-30",
        "authority_level": 7,
        "status": "good_law",
        "issues": ["biometric data", "statutory damages", "BIPA"],
        "holdings": [
            "Under the Illinois Biometric Information Privacy Act, each "
            "unauthorized collection of biometric data constitutes a "
            "separate violation subject to statutory damages."
        ],
        "text": (
            "Brown v. National Insurance Group interpreted the Illinois BIPA "
            "to allow per-violation statutory damages for unauthorized "
            "biometric data collection, significantly expanding potential "
            "liability for covered entities."
        ),
    },
    # ─── FABRICATED CASE (index 5) ───
    # Ref: Section 14.2.2 (p.23 Note box) — the Schwartz/Varghese incident.
    # This case does NOT exist. It is included so verify_citations() can
    # demonstrate detection of hallucinated precedent.
    {
        "name": "Varghese v. China Southern Airlines",
        "citation": "No. 22-cv-1234 (S.D.N.Y. 2023)",
        "court": "United States District Court, Southern District of New York",
        "jurisdiction": "federal",
        "date": "2023-06-15",
        "authority_level": 0,
        "status": "fabricated",
        "issues": ["personal injury", "international aviation"],
        "holdings": [
            "THIS CASE DOES NOT EXIST. It was hallucinated by a generative "
            "AI system and cited in a real court filing, leading to sanctions."
        ],
        "text": (
            "Varghese v. China Southern Airlines is a fabricated case "
            "hallucinated by a generative AI system. It was cited in a 2023 "
            "court filing by attorney Steven Schwartz, who was subsequently "
            "sanctioned by the court. This entry exists in the mock database "
            "solely to test the citation verification gate."
        ),
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# B15: MOCK_CONTRACT — Multi-clause contract for analysis
# Ref: Section 14.2.3 (p.27-30), ContractAnalysisAgent pipeline.
#      8 clauses with identifiable risk areas: indemnification (HIGH),
#      liability cap (HIGH), missing GDPR addendum (CRITICAL compliance gap).
# ═══════════════════════════════════════════════════════════════════════════════

MOCK_CONTRACT = {
    "title": "Master Services Agreement",
    "parties": {
        "provider": "TechSolutions Inc.",
        "client": "GlobalRetail Corp.",
    },
    "effective_date": "2025-01-15",
    "governing_law": "State of New York",
    "sections": [
        {
            "id": "1",
            "title": "Scope of Services",
            "type": "scope",
            "text": (
                "Provider shall deliver cloud-based analytics services "
                "including data processing, storage, and reporting as "
                "described in Exhibit A. Services shall be available 99.9% "
                "of the time measured on a monthly basis."
            ),
        },
        {
            "id": "2",
            "title": "Term and Termination",
            "type": "term",
            "text": (
                "This Agreement shall commence on the Effective Date and "
                "continue for an initial term of thirty-six (36) months. "
                "Either party may terminate for cause upon sixty (60) days "
                "written notice following an uncured material breach."
            ),
        },
        {
            "id": "3",
            "title": "Payment Terms",
            "type": "payment",
            "text": (
                "Client shall pay Provider a monthly fee of $45,000 due "
                "within thirty (30) days of invoice. Late payments shall "
                "accrue interest at 1.5% per month or the maximum rate "
                "permitted by law, whichever is lower."
            ),
        },
        {
            "id": "4",
            "title": "Intellectual Property",
            "type": "ip",
            "text": (
                "All intellectual property developed by Provider in the "
                "course of performing Services shall be owned by Provider. "
                "Client receives a non-exclusive, non-transferable license "
                "to use deliverables for internal business purposes only."
            ),
        },
        {
            "id": "5",
            "title": "Indemnification",
            "type": "indemnification",
            "text": (
                "Client shall indemnify, defend, and hold harmless Provider "
                "against all claims, damages, losses, and expenses arising "
                "from Client's use of the Services, including but not limited "
                "to claims of intellectual property infringement by third "
                "parties. This indemnification obligation survives termination "
                "of this Agreement without limitation."
            ),
            "risk_notes": "One-sided indemnification favoring Provider; "
                          "unlimited survival clause.",
        },
        {
            "id": "6",
            "title": "Limitation of Liability",
            "type": "liability",
            "text": (
                "In no event shall Provider's total aggregate liability "
                "exceed the fees paid by Client in the three (3) months "
                "preceding the claim. Provider shall not be liable for "
                "indirect, incidental, consequential, or punitive damages "
                "under any circumstances."
            ),
            "risk_notes": "Liability cap at 3 months of fees is very low "
                          "for a 36-month agreement; excludes all "
                          "consequential damages.",
        },
        {
            "id": "7",
            "title": "Confidentiality",
            "type": "confidentiality",
            "text": (
                "Each party shall protect the other's Confidential "
                "Information using the same degree of care it uses for its "
                "own confidential information, but in no event less than "
                "reasonable care. Obligations under this section survive "
                "for five (5) years following disclosure."
            ),
        },
        {
            "id": "8",
            "title": "Data Processing",
            "type": "data_processing",
            "text": (
                "Provider shall process Client data in accordance with "
                "applicable law. Provider may transfer data to subprocessors "
                "upon written notice to Client. Provider shall maintain "
                "commercially reasonable security measures."
            ),
            "risk_notes": "No GDPR Data Processing Addendum; no Standard "
                          "Contractual Clauses for cross-border transfer; "
                          "'commercially reasonable' is vague.",
        },
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
# B16: MOCK_INTER_AGENT_MESSAGE — Inter-agent communication protocol
# Ref: Section 14.1.4 (p.19), exact JSON message format from chapter.
#      Allocation: us_equities 0.45, international_equities 0.20,
#                  fixed_income 0.25, alternatives 0.10
# ═══════════════════════════════════════════════════════════════════════════════

MOCK_INTER_AGENT_MESSAGE = {
    "sender_id": "portfolio_construction_agent",
    "recipient_id": "compliance_agent",
    "message_type": "recommendation_validation_request",
    "timestamp": "2025-01-15T14:30:00Z",
    "confidence_score": 0.87,
    "data_payload": {
        "client_id": "retail_client_4521",
        "recommendation_type": "initial_allocation",
        "asset_allocation": {
            "us_equities": 0.45,
            "international_equities": 0.20,
            "fixed_income": 0.25,
            "alternatives": 0.10,
        },
        "risk_score": 6.2,
        "expected_annual_return": 0.078,
        "max_drawdown_estimate": -0.18,
    },
    "context_references": [
        "risk_profile_4521",
        "market_analysis_20250115",
    ],
    "requires_response": True,
    "priority_level": "high",
}
