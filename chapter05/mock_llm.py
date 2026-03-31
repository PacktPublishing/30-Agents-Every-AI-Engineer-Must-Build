"""
Chapter 05 — Foundational Cognitive Architectures
Book: 30 Agents Every AI Engineer Must Build
Author: Imran Ahmad
Publisher: Packt Publishing

Mock layer providing drop-in replacements for an LLM client and
a vector database. Enables full Simulation Mode so the notebook
runs end-to-end without any API key.

Classes:
    MockResponse  — Structured LLM response (dataclass, 8 fields).
    MockLLM       — Keyword-routed mock that returns pre-built
                    MockResponse objects for 6 chapter scenarios.
    MockVectorDB  — In-memory vector store with Jaccard-overlap
                    search, pre-seeded with 4 episodic records.

Ref: Technical Requirements (p. 2); all agent sections (pp. 3-28)
"""

from dataclasses import dataclass, field

from color_logger import log_info, log_warn


# ── MockResponse dataclass ─────────────────────────────────────────

@dataclass
class MockResponse:
    """Structured response returned by MockLLM.generate().

    Mirrors the fields a real LLM integration would produce after
    parsing a function-call or structured-output response.

    Args:
        content: Generated text response.
        intent: Classified intent label.
        confidence: Score in [0.0, 1.0].
        reasoning_steps: Chain-of-thought trace.
        strategy: Selected strategy name.
        required_tools: List of tools the agent should invoke.
        escalation_risk: Risk score in [0.0, 1.0].
        metadata: Extensible dict (always includes chapter_ref).

    Chapter Reference:
        Used across Sections 5.1-5.3 (pp. 3-28)
    """

    content: str
    intent: str
    confidence: float
    reasoning_steps: list[str]
    strategy: str
    required_tools: list[str]
    escalation_risk: float
    metadata: dict = field(default_factory=dict)


# ── Pre-built mock responses (6 scenarios) ─────────────────────────

_MOCK_RESPONSES: dict[str, MockResponse] = {
    # ── Scenario 1: Service outage ─────────────────────────────
    # Ref: Section 5.1, Case Study pp. 15-16
    "service_outage": MockResponse(
        content=(
            "I've detected a service outage affecting your area. "
            "Initiating autonomous diagnostic sequence: checking "
            "service area status, identifying intermittent issues, "
            "and scheduling a priority technician visit."
        ),
        intent="service_outage",
        confidence=0.94,
        reasoning_steps=[
            "Parsed user message: internet connectivity complaint",
            "Cross-referenced system alerts: area outage confirmed",
            "Assessed user tier: premium business account",
            "Selected strategy: full autonomous resolution",
            "Planned actions: diagnostic + technician + backup",
        ],
        strategy="full_autonomous_resolution",
        required_tools=[
            "check_service_area_status",
            "identify_intermittent_issues",
            "schedule_priority_technician",
            "provide_mobile_hotspot_backup",
        ],
        escalation_risk=0.15,
        metadata={"chapter_ref": "Section 5.1, pp. 3-16, Case Study p. 16"},
    ),

    # ── Scenario 2: Billing issue ──────────────────────────────
    # Ref: Section 5.1, Action execution pp. 7-8
    "billing_issue": MockResponse(
        content=(
            "I understand you have a billing concern. Let me pull "
            "up your account details and analyze your recent billing "
            "history to identify any discrepancies."
        ),
        intent="billing_issue",
        confidence=0.91,
        reasoning_steps=[
            "Parsed user message: billing/charge complaint",
            "Identified intent: billing_issue",
            "Checked autonomous credit limit: within threshold",
            "Selected strategy: full autonomous resolution",
            "Planned DAG: fetch → analyze → identify → adjust → confirm",
        ],
        strategy="full_autonomous_resolution",
        required_tools=[
            "fetch_account_details",
            "analyze_billing_history",
            "identify_discrepancies",
            "calculate_adjustments",
        ],
        escalation_risk=0.20,
        metadata={"chapter_ref": "Section 5.1, Action execution, pp. 7-8"},
    ),

    # ── Scenario 3: Complex escalation ─────────────────────────
    # Ref: Section 5.1, Escalation criteria pp. 14-15
    "complex_escalation": MockResponse(
        content=(
            "This issue involves multiple interconnected problems "
            "that require specialist attention. I'm preparing a "
            "comprehensive handoff package for a senior agent."
        ),
        intent="complex_technical",
        confidence=0.52,
        reasoning_steps=[
            "Parsed user message: multiple interleaved issues",
            "Confidence below 0.8 threshold — flagging for review",
            "Complexity score: 0.85 — exceeds autonomous threshold",
            "Selected strategy: immediate escalation",
            "Preparing escalation package with full context",
        ],
        strategy="immediate_escalation",
        required_tools=[
            "prepare_escalation_package",
            "initiate_human_handoff",
        ],
        escalation_risk=0.82,
        metadata={
            "chapter_ref": "Section 5.1, Escalation criteria, pp. 14-15"
        },
    ),

    # ── Scenario 4: Marketing campaign planning ────────────────
    # Ref: Section 5.2, Planning Agent pp. 17-21
    "marketing_campaign_plan": MockResponse(
        content=(
            "I'll decompose this marketing campaign into a "
            "structured execution plan with phased tasks: market "
            "research, content creation, ad setup, and launch event "
            "coordination."
        ),
        intent="planning_request",
        confidence=0.89,
        reasoning_steps=[
            "Identified high-level goal: launch product campaign",
            "Applying hierarchical decomposition (Figure 5.2)",
            "Phase 1: Market research + audience definition",
            "Phase 2: Content creation + banner design",
            "Phase 3: Ad setup + launch event booking",
            "Phase 4: Monitoring + adaptive revision",
        ],
        strategy="hierarchical_decomposition",
        required_tools=[
            "market_research_platform",
            "content_generation_api",
            "calendar_booking_api",
        ],
        escalation_risk=0.10,
        metadata={
            "chapter_ref": "Section 5.2, Planning Agent, pp. 17-21"
        },
    ),

    # ── Scenario 5: Healthcare query (memory-augmented) ────────
    # Ref: Section 5.3, Healthcare Case Study pp. 25-28
    "healthcare_query": MockResponse(
        content=(
            "Based on your history, I can see you've been managing "
            "ongoing fatigue. Let me review your previous visits and "
            "recent dietary changes to provide updated guidance."
        ),
        intent="health_followup",
        confidence=0.88,
        reasoning_steps=[
            "Retrieved episodic memory: prior fatigue reports",
            "Identified continuity: patient follow-up interaction",
            "Cross-referenced semantic memory: iron deficiency data",
            "Strategy: memory-augmented personalized response",
        ],
        strategy="memory_augmented_response",
        required_tools=[
            "episodic_memory_search",
            "semantic_knowledge_lookup",
        ],
        escalation_risk=0.12,
        metadata={
            "chapter_ref": "Section 5.3, Healthcare Case Study, pp. 25-28"
        },
    ),

    # ── Scenario 6: Default fallback ───────────────────────────
    # Ref: Chapter 5, General
    "default_fallback": MockResponse(
        content=(
            "I understand your request. Let me analyze the situation "
            "and determine the best approach to assist you."
        ),
        intent="general_inquiry",
        confidence=0.65,
        reasoning_steps=[
            "Parsed user message: no strong intent signal",
            "Applying guided autonomous resolution as baseline",
            "Requesting additional context if needed",
        ],
        strategy="guided_autonomous_resolution",
        required_tools=["analyze_issue", "research_solutions"],
        escalation_risk=0.30,
        metadata={"chapter_ref": "Chapter 5, General"},
    ),
}


# ── Keyword routing map ────────────────────────────────────────────

_KEYWORD_ROUTES: list[tuple[list[str], str]] = [
    # Order matters: first match wins
    (["internet", "outage", "down", "slow", "connect"],  "service_outage"),
    (["bill", "charge", "payment", "invoice"],            "billing_issue"),
    (["complex", "multiple issues", "can't figure"],      "complex_escalation"),
    (["campaign", "launch", "marketing"],                 "marketing_campaign_plan"),
    (["fatigue", "tired", "health", "symptom", "diet"],   "healthcare_query"),
]


def _route_prompt(prompt: str) -> str:
    """Match prompt text against keyword routes.

    Returns the scenario key for the first matching route,
    or 'default_fallback' if no keywords match.

    Args:
        prompt: The user/agent prompt text.

    Returns:
        Scenario key string.
    """
    lower = prompt.lower()
    for keywords, scenario in _KEYWORD_ROUTES:
        if any(kw in lower for kw in keywords):
            return scenario
    return "default_fallback"


# ── MockLLM ────────────────────────────────────────────────────────

class MockLLM:
    """Drop-in mock replacement for an LLM client.

    Routes prompts to one of 6 pre-built MockResponse objects
    using keyword matching. Enables full Simulation Mode so the
    notebook demonstrates all agent architectures without any
    API key.

    Attributes:
        is_mock: Always True. Downstream code can check this flag
            to adjust behavior for simulation vs. live mode.

    Chapter Reference:
        Used across all agent sections (pp. 3-28)
    """

    is_mock: bool = True

    def generate(self, prompt: str) -> MockResponse:
        """Generate a mock LLM response for the given prompt.

        Routes the prompt through a keyword map and returns the
        matching pre-built MockResponse. Logs the detected
        scenario for observability.

        Args:
            prompt: The prompt text (from agent cognition layer).

        Returns:
            MockResponse with intent, confidence, strategy, etc.

        Chapter Reference:
            Practical implementation with modern LLMs (pp. 11-14)
        """
        scenario = _route_prompt(prompt)
        response = _MOCK_RESPONSES[scenario]
        ref = response.metadata.get("chapter_ref", "")
        log_info(
            f"MockLLM: detected scenario '{scenario}' "
            f"(ref: {ref})"
        )
        return response


# ── MockVectorDB ───────────────────────────────────────────────────

def _jaccard_score(query: str, text: str) -> float:
    """Compute Jaccard word-overlap similarity between two strings.

    Args:
        query: Search query string.
        text: Document text to compare against.

    Returns:
        Float in [0.0, 1.0] representing word overlap.
    """
    q_words = set(query.lower().split())
    t_words = set(text.lower().split())
    if not q_words or not t_words:
        return 0.0
    intersection = q_words & t_words
    union = q_words | t_words
    return len(intersection) / len(union)


# Pre-seeded episodic records (2 healthcare + 2 customer service)
# Ref: Section 5.3, Healthcare Case Study pp. 25-28
_SEED_RECORDS: list[dict] = [
    {
        "user_id": "patient_42",
        "query": "I've been feeling very fatigued lately",
        "response_summary": (
            "Dietary changes suggested, B12 check recommended"
        ),
        "timestamp": "2025-01-15T10:00:00",
    },
    {
        "user_id": "patient_42",
        "query": "The diet change helped a bit, still tired",
        "response_summary": (
            "Sleep study recommended, follow-up blood panel"
        ),
        "timestamp": "2025-03-20T14:30:00",
    },
    {
        "user_id": "patient_42",
        "query": "My allergist said I'm low on iron",
        "response_summary": (
            "Iron deficiency noted, dietary recs adjusted"
        ),
        "timestamp": "2025-05-10T09:15:00",
    },
    {
        "user_id": "premium_biz_123",
        "query": "Internet was slow last Tuesday",
        "response_summary": (
            "Remote diagnostic run, router config reset"
        ),
        "timestamp": "2025-06-01T16:45:00",
    },
]


class MockVectorDB:
    """In-memory mock vector database for episodic memory.

    Provides add/search/reset operations using Jaccard word-overlap
    scoring as a stand-in for real embedding-based similarity search.
    Pre-seeded with 4 episodic records spanning healthcare and
    customer service scenarios.

    Chapter Reference:
        Section 5.3, Memory-Augmented Agent (pp. 22-28)
        Vector Databases & Retrieval (p. 25)
    """

    def __init__(self) -> None:
        """Initialize with pre-seeded episodic records."""
        self._records: list[dict] = list(_SEED_RECORDS)
        log_info(
            f"MockVectorDB initialized with {len(self._records)} "
            f"pre-seeded episodic records"
        )

    def add(self, record: dict) -> None:
        """Append a new interaction record to memory.

        Args:
            record: Dict with at minimum 'user_id', 'query',
                'response_summary', and 'timestamp' keys.

        Chapter Reference:
            Section 5.3, process_interaction() (pp. 25-26)
        """
        self._records.append(record)
        log_info(
            f"MockVectorDB: stored record for user "
            f"'{record.get('user_id', 'unknown')}' "
            f"(total records: {len(self._records)})"
        )

    def search(
        self,
        query: str,
        user_id: str,
        limit: int = 3,
    ) -> list[dict]:
        """Search episodic memory using Jaccard word-overlap scoring.

        Filters by user_id, then ranks remaining records by
        word overlap with the query string. Returns top-N results
        sorted by descending relevance score.

        Args:
            query: Natural-language search query.
            user_id: Filter to this user's records only.
            limit: Maximum number of results to return.

        Returns:
            List of record dicts, each augmented with a
            'relevance_score' key.

        Chapter Reference:
            Section 5.3, Vector Databases & Retrieval (p. 25)
        """
        user_records = [
            r for r in self._records if r.get("user_id") == user_id
        ]

        scored = []
        for record in user_records:
            searchable = (
                f"{record.get('query', '')} "
                f"{record.get('response_summary', '')}"
            )
            score = _jaccard_score(query, searchable)
            scored.append({**record, "relevance_score": round(score, 3)})

        scored.sort(key=lambda r: r["relevance_score"], reverse=True)
        results = scored[:limit]

        log_info(
            f"MockVectorDB: searched '{query}' for user "
            f"'{user_id}' → {len(results)} results "
            f"(from {len(user_records)} user records)"
        )
        return results

    def reset(self) -> None:
        """Clear all records and re-seed with defaults.

        Chapter Reference:
            Section 5.3, Memory-Augmented Agent (pp. 22-28)
        """
        self._records = list(_SEED_RECORDS)
        log_warn(
            f"MockVectorDB: reset to {len(self._records)} "
            f"seed records"
        )
