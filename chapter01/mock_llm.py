"""
Mock LLM simulation engine for Chapter 1: Foundations of Agent Engineering.
Book: "AI Agents" by Imran Ahmad (Packt, 2026)

Provides:
    - MockResponse: Lightweight response object mirroring OpenAI structure.
    - MockLLM: Full simulation engine with chapter-derived response bank,
      keyword-scoring routing, configurable latency, and failure injection.

Ref: Strategy §3.3 (class specs), §4 (response bank)
"""

import json
import time
import random

from .utils import log_info, log_warning


# ============================================================
# MockResponse — Lightweight Response Object
# Ref: Strategy §3.3 — MockResponse class spec
# ============================================================

class MockResponse:
    """Simulated LLM response object.

    Attributes:
        content (str): The response text.
        model (str): Model identifier (default: "mock-gpt-4").
        usage (dict): Simulated token usage counts.

    Author: Imran Ahmad
    """

    def __init__(self, content, model="mock-gpt-4", usage=None):
        self.content = content
        self.model = model
        self.usage = usage or {
            "prompt_tokens": len(content.split()) * 2,
            "completion_tokens": len(content.split()),
        }

    def __repr__(self):
        preview = self.content[:80] + "..." if len(self.content) > 80 else self.content
        return f"MockResponse(model='{self.model}', content='{preview}')"


# ============================================================
# MockLLM — Simulation Engine
# Ref: Strategy §3.3 (class spec), §4 (response bank)
# ============================================================

class MockLLM:
    """Chapter-derived mock LLM that simulates OpenAI chat completions.

    Provides a keyword-scoring routing engine backed by 22 pre-authored
    response bank entries faithful to Chapter 1 content. Supports
    configurable latency simulation and failure injection for resilience
    testing.

    Args:
        simulate_latency (bool): Whether to add 0.3-0.8s delay per call.
        failure_rate (float): Probability [0.0, 1.0] of raising a
            ConnectionError to simulate API failures.

    Author: Imran Ahmad
    """

    def __init__(self, simulate_latency=True, failure_rate=0.0):
        self.simulate_latency = simulate_latency
        self.failure_rate = failure_rate
        self._response_bank = self._build_response_bank()

    def chat(self, messages, temperature=0.7, model="mock-gpt-4"):
        """Main interface — mirrors OpenAI chat completions API.

        Args:
            messages (list[dict]): Conversation messages with 'role' and 'content'.
            temperature (float): Sampling temperature (unused in mock, accepted for API parity).
            model (str): Model name (unused in mock, accepted for API parity).

        Returns:
            MockResponse: Simulated response with content and usage.

        Raises:
            ConnectionError: If failure_rate check triggers (simulated API failure).

        Author: Imran Ahmad
        """
        # Simulate network latency
        if self.simulate_latency:
            delay = random.uniform(0.3, 0.8)
            time.sleep(delay)

        # Simulate API failure
        if self.failure_rate > 0 and random.random() < self.failure_rate:
            raise ConnectionError(
                "MockLLM: Simulated API timeout. This is intentional for "
                "resilience testing. The @graceful_fallback decorator handles this."
            )

        # Extract user content and route to best-matching response
        user_content = self._extract_user_content(messages)
        response_text, section_ref = self._route_response(user_content)

        return MockResponse(content=response_text, model=model)

    def _extract_user_content(self, messages):
        """Extract the last user message content from the messages list.

        Iterates in reverse to find the most recent 'user' role message.

        Author: Imran Ahmad
        """
        for msg in reversed(messages):
            if isinstance(msg, dict) and msg.get("role") == "user":
                return msg.get("content", "").lower()
        return ""

    def _route_response(self, user_content):
        """Route user content to the best-matching response bank entry.

        Uses keyword-overlap scoring: each bank entry's keywords are checked
        against the user content. The entry with the highest number of
        keyword matches wins. Ties are broken by list order (first match).

        Args:
            user_content (str): Lowercased user message text.

        Returns:
            tuple: (response_text, section_ref) from the best-matching entry.

        Author: Imran Ahmad
        """
        best_score = 0
        best_response = None
        best_ref = ""

        for entry in self._response_bank:
            score = sum(1 for kw in entry["keywords"] if kw in user_content)
            if score > best_score:
                best_score = score
                best_response = entry["response"]
                best_ref = entry["section_ref"]

        if best_response is not None:
            return best_response, best_ref

        return self._default_response()

    def _default_response(self):
        """Fallback response when no keywords match.

        Author: Imran Ahmad
        """
        return (
            "This is a simulated response from MockLLM. The requested topic "
            "was not matched to a specific chapter section. Please refer to "
            "Chapter 1 of 'AI Agents' by Imran Ahmad for comprehensive coverage "
            "of agent engineering foundations.",
            "§1 General"
        )

    def _build_response_bank(self):
        """Construct the full response bank with 22 chapter-derived entries.

        Every response is faithful to the chapter's actual examples, data,
        and domain content. JSON responses are serialized as strings for
        consistent return type.

        Ref: Strategy §4 — Mock Response Bank

        Author: Imran Ahmad
        """
        return [
            # ── §1.2.1 Cognitive Loop ────────────────────────────
            {
                "keywords": ["perceive", "input", "sentiment", "customer", "capture"],
                "response": json.dumps({
                    "message": "I need help with my billing",
                    "timestamp": "2026-03-30T10:15:00",
                    "user_id": "USR-4421",
                    "session_state": "active",
                    "sentiment": "frustrated"
                }, indent=2),
                "section_ref": "§1.2.1 Perception"
            },
            {
                "keywords": ["reason", "intent", "classify", "priority", "meaning"],
                "response": json.dumps({
                    "intent": "billing_issue",
                    "priority": "high",
                    "confidence": 0.92,
                    "context": "recurring_customer"
                }, indent=2),
                "section_ref": "§1.2.1 Reasoning"
            },
            {
                "keywords": ["plan", "action_plan", "billing", "steps", "decompose"],
                "response": json.dumps([
                    "fetch_account_details",
                    "analyze_billing_history",
                    "generate_explanation",
                    "offer_resolution"
                ], indent=2),
                "section_ref": "§1.2.1 Planning"
            },
            {
                "keywords": ["execute", "action", "fetch_account", "generate_response"],
                "response": (
                    "Based on your account history, the $49.99 charge on March 15 "
                    "corresponds to your Premium plan renewal. I can process a refund "
                    "if this charge was not authorized."
                ),
                "section_ref": "§1.2.1 Action"
            },
            {
                "keywords": ["learn", "feedback", "success_score", "outcome", "update"],
                "response": json.dumps({
                    "success_score": 0.85,
                    "model_updated": True,
                    "flagged_for_review": False,
                    "preference_logged": "prefers_email_support"
                }, indent=2),
                "section_ref": "§1.2.1 Learning"
            },

            # ── §1.2.3 Agent Brain Patterns ──────────────────────
            {
                "keywords": ["reactive", "stimulus", "thermostat", "temperature", "rule"],
                "response": json.dumps({
                    "action": "ACTIVATE_HEATING",
                    "trigger": "temperature_below_20C",
                    "latency_ms": 12,
                    "stateless": True
                }, indent=2),
                "section_ref": "§1.2.3 Reactive"
            },
            {
                "keywords": ["fire", "alarm", "smoke", "detection", "emergency"],
                "response": json.dumps({
                    "action": "TRIGGER_SUPPRESSION",
                    "trigger": "smoke_detected",
                    "latency_ms": 8,
                    "confidence": 1.0
                }, indent=2),
                "section_ref": "§1.2.3 Reactive"
            },
            {
                "keywords": ["deliberative", "travel", "tokyo", "trip", "sense", "model"],
                "response": json.dumps({
                    "destination": "Tokyo",
                    "timeframe": "next_month",
                    "tasks": [
                        "search_flights",
                        "verify_visa_requirements",
                        "suggest_hotels"
                    ],
                    "preferences": {
                        "budget": "to_be_determined",
                        "airline": "no_preference"
                    }
                }, indent=2),
                "section_ref": "§1.2.3 Deliberative"
            },
            {
                "keywords": ["hybrid", "warehouse", "obstacle", "robot", "layer"],
                "response": json.dumps({
                    "reactive_layer": {
                        "action": "EMERGENCY_STOP",
                        "trigger": "obstacle_detected",
                        "latency_ms": 15
                    },
                    "deliberative_layer": {
                        "action": "REROUTE_VIA_AISLE_3",
                        "reasoning": "shortest_clear_path"
                    },
                    "coordination": "reactive_executes_first_then_deliberative_replans"
                }, indent=2),
                "section_ref": "§1.2.3 Hybrid"
            },

            # ── §1.3.1 Model Context Protocol ────────────────────
            {
                "keywords": ["mcp", "tool", "discover", "capability", "schema", "registry"],
                "response": json.dumps({
                    "name": "SearchFlights",
                    "description": "Retrieve available flight options based on input parameters",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "origin": {"type": "string"},
                            "destination": {"type": "string"},
                            "departure_date": {"type": "string", "format": "date"}
                        },
                        "required": ["origin", "destination", "departure_date"]
                    },
                    "output_schema": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "airline": {"type": "string"},
                                "price": {"type": "number"},
                                "duration": {"type": "string"}
                            }
                        }
                    }
                }, indent=2),
                "section_ref": "§1.3.1 MCP"
            },
            {
                "keywords": ["invoke", "flight", "paris", "airline", "price", "search"],
                "response": json.dumps([
                    {"airline": "Air France", "price": 450, "duration": "11h 20m"},
                    {"airline": "JAL", "price": 520, "duration": "12h 05m"},
                    {"airline": "Delta", "price": 480, "duration": "13h 45m"}
                ], indent=2),
                "section_ref": "§1.3.1 MCP"
            },

            # ── §1.3.2 Agent-to-Agent Protocols ──────────────────
            {
                "keywords": ["a2a", "triage", "agent", "delegate", "message", "role"],
                "response": json.dumps({
                    "state": {
                        "ticket_id": "TK-8891",
                        "issue": "billing_discrepancy",
                        "amount": 149.99
                    },
                    "role": "billing_specialist",
                    "status": "assigned",
                    "source_agent": "triage_agent"
                }, indent=2),
                "section_ref": "§1.3.2 A2A"
            },
            {
                "keywords": ["compliance", "validator", "forward", "status"],
                "response": json.dumps({
                    "state": {
                        "ticket_id": "TK-8891",
                        "resolution": "refund_approved"
                    },
                    "role": "compliance_validator",
                    "status": "validated",
                    "checks_passed": [
                        "amount_threshold",
                        "policy_adherence",
                        "fraud_screening"
                    ]
                }, indent=2),
                "section_ref": "§1.3.2 A2A"
            },

            # ── §1.5 Agent Interaction Paradigms ─────────────────
            {
                "keywords": ["capital", "canada", "ottawa", "simple", "stateless"],
                "response": "Ottawa",
                "section_ref": "§1.5.1 Direct LLM"
            },
            {
                "keywords": ["proxy", "restaurant", "structured", "translate", "near"],
                "response": json.dumps({
                    "intent": "search_restaurants",
                    "location": "current_user_location",
                    "time_filter": "open_now",
                    "format": "list"
                }, indent=2),
                "section_ref": "§1.5.2 Proxy Agent"
            },
            {
                "keywords": ["assistant", "book", "flight", "paris", "hotel", "session"],
                "response": (
                    "I found 3 flights to Paris for next Friday. The best value is "
                    "Air France departing at 8:45 AM for $450 (11h 20m). Shall I "
                    "also search for hotels near the Eiffel Tower as you mentioned?"
                ),
                "section_ref": "§1.5.3 Assistant"
            },
            {
                "keywords": ["autonomous", "itinerary", "visa", "insurance", "plan_trip"],
                "response": json.dumps({
                    "itinerary": {
                        "flights": [
                            {"airline": "Air France", "price": 450, "duration": "11h 20m"}
                        ],
                        "hotels": [
                            {"name": "Hotel Le Marais", "price_per_night": 180, "rating": 4.5}
                        ],
                        "visa_status": "not_required_for_90_days",
                        "insurance": {
                            "provider": "TravelGuard",
                            "coverage": "comprehensive"
                        }
                    },
                    "adaptations_made": 2,
                    "memory_used": True
                }, indent=2),
                "section_ref": "§1.5.4 Autonomous"
            },
            {
                "keywords": ["multi-agent", "analyze", "data", "retrieval", "cleaning"],
                "response": json.dumps({
                    "agent_a": {
                        "role": "data_retrieval",
                        "status": "complete",
                        "records": 15420
                    },
                    "agent_b": {
                        "role": "data_cleaning",
                        "status": "complete",
                        "records_cleaned": 15388,
                        "duplicates_removed": 32
                    },
                    "agent_c": {
                        "role": "visualization",
                        "status": "complete",
                        "charts_generated": 3
                    }
                }, indent=2),
                "section_ref": "§1.5.5 MAS"
            },

            # ── §1.6 Progression Framework ───────────────────────
            {
                "keywords": ["progression", "framework", "maturity", "level", "assessment"],
                "response": json.dumps({
                    "levels": {
                        "0": "Manual Operations",
                        "1": "Reactive Agents",
                        "2": "Tool-Using Agents",
                        "3": "Planning Agents",
                        "4": "Learning Agents"
                    },
                    "dimensions": ["autonomy", "reasoning", "adaptability"]
                }, indent=2),
                "section_ref": "§1.6 Framework"
            },

            # ── §1.7 Real-World Business Impact ──────────────────
            {
                "keywords": ["quandri", "insurance", "processing", "policy", "accuracy"],
                "response": json.dumps({
                    "policies_processed": 1247,
                    "accuracy_rate": 0.999,
                    "avg_processing_time_sec": 42,
                    "monthly_recurring_revenue": 30000,
                    "comparison": "15min vs hours of manual processing"
                }, indent=2),
                "section_ref": "§1.7 Quandri"
            },
            {
                "keywords": ["myaskai", "financial", "support", "inquiry", "30_second"],
                "response": json.dumps({
                    "avg_resolution_time_sec": 28,
                    "satisfaction_score": 0.993,
                    "monthly_recurring_revenue": 25000,
                    "autonomous_resolution_rate": 0.87
                }, indent=2),
                "section_ref": "§1.7 My AskAI"
            },
            {
                "keywords": ["enterprise_bot", "sales", "lead", "outreach", "qualified"],
                "response": json.dumps({
                    "qualified_leads_multiplier": 3.0,
                    "acquisition_cost_reduction": 0.50,
                    "annual_recurring_revenue": 2000000,
                    "pipeline": "lead_enrichment → qualification → outreach → meeting_coordination"
                }, indent=2),
                "section_ref": "§1.7 Enterprise Bot"
            },
        ]
