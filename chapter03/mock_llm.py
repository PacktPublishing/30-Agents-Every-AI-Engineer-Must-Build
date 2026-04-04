"""
MockLLM Simulation Engine for Chapter 3: The Art of Agent Prompting
Book: Agents by Imran Ahmad (Packt Publishing, 2026)
Author: Imran Ahmad

Drop-in replacement for ChatOpenAI that enables all notebook demos
to run without an API key. Subclasses BaseChatModel for full LangChain
pipe-operator (|) compatibility, which is critical for the ToT chain
demonstration in Section 3.6.

Routes responses via keyword matching on prompt content to return
chapter-appropriate synthetic data from a built-in response registry.
"""

from typing import Any, List, Optional
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import Field
import json


class MockLLM(BaseChatModel):
    """
    Simulation LLM for Chapter 3 demos.

    Subclasses BaseChatModel for full LangChain compatibility including
    the pipe operator (prompt | llm) used in Section 3.6.

    Author: Imran Ahmad
    """

    model_name: str = Field(default="mock-chapter3")

    @property
    def _llm_type(self) -> str:
        return "mock-chapter3"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Required by BaseChatModel. Joins message content and routes response."""
        prompt_text = " ".join(
            msg.content for msg in messages if hasattr(msg, "content")
        ).lower()
        response_text = self._route_response(prompt_text)
        message = AIMessage(content=response_text)
        generation = ChatGeneration(message=message)
        return ChatResult(generations=[generation])

    def _route_response(self, prompt_text: str) -> str:
        """Iterate response registry and return first keyword match."""
        for keywords, response_fn in self._RESPONSE_REGISTRY:
            if any(kw in prompt_text for kw in keywords):
                return response_fn()
        return self._default_response()

    # ------------------------------------------------------------------
    # Response Registry — 14 entries mapped to chapter sections
    # ------------------------------------------------------------------

    _RESPONSE_REGISTRY: list = [
        # #1 — §3.6 ToT Branch A: Market Analyst
        (
            ["market analyst", "target market", "educational app"],
            lambda: (
                "**Market Analysis: AI-Powered Educational App**\n\n"
                "After evaluating three target segments, I recommend "
                "**university students** as the primary market.\n\n"
                "**Rationale:**\n"
                "1. High demand — University students actively seek supplemental "
                "learning tools and are digitally native.\n"
                "2. Acceptable willingness-to-pay — Students invest in educational "
                "resources, especially those offering competitive advantages.\n"
                "3. Lower saturation — The high school market is overcrowded with "
                "free alternatives; corporate training involves long sales cycles "
                "and complex procurement processes.\n\n"
                "**Rejected segments:**\n"
                "- High school students: Market saturated with free tools (Khan Academy, etc.)\n"
                "- Corporate training: Long sales cycles (6–12 months), complex procurement\n\n"
                "[Simulation Mode — connect a live API key for dynamic analysis]"
            ),
        ),
        # #2 — §3.6 ToT Branch B: Financial Planner
        (
            ["financial planner", "business model", "subscription", "revenue"],
            lambda: (
                "**Financial Model Recommendation**\n\n"
                "Given the university student target market, I recommend a "
                "**freemium subscription model** with tiered pricing.\n\n"
                "**Pricing tiers:**\n"
                "- **Free tier:** Core features, limited usage (drives adoption)\n"
                "- **Pro tier ($9.99/month):** Full feature access, unlimited usage\n"
                "- **Team tier ($7.99/user/month):** Group licenses for study groups\n\n"
                "**Justification:**\n"
                "- Recurring revenue aligns with long academic cycles (4+ years)\n"
                "- Freemium eliminates the adoption barrier for budget-conscious students\n"
                "- One-time purchase model rejected: does not support continuous "
                "development or generate predictable revenue\n\n"
                "[Simulation Mode — connect a live API key for dynamic analysis]"
            ),
        ),
        # #3 — §3.6 ToT Branch C: Marketing Specialist
        (
            ["marketing specialist", "awareness", "campaign", "influencer"],
            lambda: (
                "**Marketing Campaign Plan**\n\n"
                "Based on the university student segment and freemium model, "
                "I recommend a combined **influencer + content marketing** strategy.\n\n"
                "**Channels:**\n"
                "- Campus micro-influencers (TikTok, Instagram) — authentic reach\n"
                "- Educational YouTube content — long-form tutorials featuring the app\n"
                "- Blog SEO — target search queries like 'best study tools for university'\n\n"
                "**Messaging:** 'Study smarter, not harder — powered by AI'\n\n"
                "**KPI:** 10,000 sign-ups within 60 days of launch\n\n"
                "**Rejected channels:**\n"
                "- LinkedIn ads: Wrong demographic for university students\n"
                "- Traditional paid search: High CPA for student audience\n\n"
                "[Simulation Mode — connect a live API key for dynamic analysis]"
            ),
        ),
        # #4 — §3.6 ToT Synthesis
        (
            ["synthesis", "launch strategy", "integrate", "strategic"],
            lambda: (
                "**Integrated Launch Strategy — AI-Powered Educational App**\n\n"
                "**1. Target Segment: University Students**\n"
                "University students represent the optimal balance of demand, "
                "willingness-to-pay, and market accessibility. The high school market "
                "is oversaturated, and corporate training has prohibitive sales cycles.\n\n"
                "**2. Revenue Model: Freemium with Pro Tier at $9.99/month**\n"
                "A freemium model drives adoption with zero friction, while the Pro tier "
                "at $9.99/month captures recurring revenue across multi-year academic "
                "journeys. Team pricing at $7.99/user/month targets study groups.\n\n"
                "**3. Go-to-Market Plan: Influencer Seeding + Content Funnel**\n"
                "Phase 1 (Weeks 1–4): Campus micro-influencer partnerships on TikTok "
                "and Instagram for authentic awareness.\n"
                "Phase 2 (Weeks 3–8): Educational YouTube content and blog SEO to "
                "build organic discovery.\n"
                "Phase 3 (Weeks 6–12): Referral program leveraging existing users "
                "for viral growth within university networks.\n\n"
                "**Success metric:** 10,000 sign-ups within 60 days.\n\n"
                "[Simulation Mode — connect a live API key for dynamic synthesis]"
            ),
        ),
        # #5 — §3.5 Few-Shot Ticket Classification
        (
            ["ticket", "support", "urgency", "triage", "classify"],
            lambda: json.dumps(
                {
                    "Urgency": "Critical",
                    "Category": "Access/Outage",
                    "Action": "Escalate to Tier-2 Engineering",
                    "Reasoning": (
                        "System-wide access failure with imminent client impact. "
                        "Matches pattern of total outage with financial consequences. "
                        "Immediate escalation required per SLA guidelines."
                    ),
                },
                indent=2,
            ),
        ),
        # #6 — §3.3 PTCF Enterprise Billing Agent
        (
            ["billing", "charge", "invoice", "payment"],
            lambda: (
                "**Customer Support Response — Billing Inquiry**\n\n"
                "1. **Acknowledge:** I completely understand your concern about "
                "the billing discrepancy, and I want to assure you that resolving "
                "this is my top priority.\n\n"
                "2. **Diagnose:** I've reviewed your account and identified a "
                "duplicate charge on your March invoice. This appears to be a "
                "system processing error during our recent billing cycle update.\n\n"
                "3. **Resolution:** Here are the steps to resolve this:\n"
                "   - A refund of $149.99 has been initiated to your payment method\n"
                "   - Processing time: 3–5 business days\n"
                "   - Your next invoice will reflect the corrected amount\n\n"
                "4. **Escalation:** If the refund does not appear within 5 business "
                "days, I will escalate this directly to our Billing Supervisor "
                "(Case #BIL-2024-0847).\n\n"
                "5. **Follow-up:** I will personally check back with you in 48 hours "
                "to confirm the refund has been processed. You can also reach me "
                "directly using reference number BIL-2024-0847.\n\n"
                "[Simulation Mode — connect a live API key for dynamic responses]"
            ),
        ),
        # #7 — §3.7 Multi-Agent Risk Assessment Protocol
        (
            ["risk", "credit", "compliance", "assessment", "regulatory"],
            lambda: json.dumps(
                {
                    "sender_id": "agent_alpha",
                    "recipient_id": "agent_beta",
                    "message_type": "risk_assessment_update",
                    "timestamp": "2024-03-15T14:30:00Z",
                    "confidence_score": 0.85,
                    "data_payload": {
                        "risk_category": "credit",
                        "assessment_summary": (
                            "Credit risk remains low based on Q4 data. "
                            "Revenue streams are stable and debt ratio is within acceptable bounds."
                        ),
                        "key_factors": ["stable_revenue", "low_debt_ratio"],
                        "recommendations": ["maintain_current_rating"],
                    },
                    "context_references": ["previous_analysis_id_123"],
                    "requires_response": False,
                    "priority_level": "medium",
                },
                indent=2,
            ),
        ),
        # #8 — Case Study 3: Automated Code Review
        (
            ["code review", "pull request", "security", "owasp"],
            lambda: (
                "## Code Review Report\n\n"
                "| # | Category | Severity | Line Ref | Recommendation |\n"
                "|---|----------|----------|----------|----------------|\n"
                "| 1 | Security (OWASP A03) | **Critical** | L42–L45 | "
                "SQL injection vulnerability: user input concatenated directly "
                "into query string. Use parameterized queries. |\n"
                "| 2 | Security (OWASP A03) | **Major** | L78–L82 | "
                "Missing input validation on file upload endpoint. Add "
                "file type and size validation. |\n"
                "| 3 | Reliability | **Major** | L105–L110 | "
                "Insufficient error handling in database connection. "
                "Add try-except with proper logging and connection cleanup. |\n\n"
                "**overall_verdict:** Request Changes\n\n"
                "[Simulation Mode — connect a live API key for dynamic code analysis]"
            ),
        ),
        # #9 — §3.4 Task Decomposition (Business Trip)
        (
            ["decompos", "plan", "business trip", "break down", "tokyo"],
            lambda: (
                "**Task Decomposition: Plan Business Trip to Tokyo**\n\n"
                "I'll break this down into sequential, dependency-ordered sub-tasks:\n\n"
                "1. **Confirm travel dates and budget** — Verify approved dates "
                "with your calendar, confirm departmental travel budget allocation, "
                "and check for any scheduling conflicts.\n\n"
                "2. **Search for flights** — Compare options for direct and connecting "
                "flights within budget. Consider departure times relative to "
                "meeting schedule. Book preferred option.\n\n"
                "3. **Check visa requirements** — Verify current visa policy for "
                "your nationality. If visa-free entry applies (up to 90 days for "
                "many countries), confirm passport validity exceeds 6 months.\n\n"
                "4. **Propose itinerary** — Draft day-by-day schedule including "
                "meeting locations, hotel recommendations near venues, "
                "transportation passes (Suica/PASMO), and contingency time "
                "for travel delays.\n\n"
                "[Simulation Mode — connect a live API key for personalized planning]"
            ),
        ),
        # #10 — §3.1/§3.3 Persona (Fitness Coach)
        (
            ["persona", "fitness", "coach", "workout"],
            lambda: (
                "**Your Daily Workout Plan** 💪\n\n"
                "Hey there, champion! Let's crush today's session!\n\n"
                "**Warm-up (5 minutes):**\n"
                "- Light jogging in place — 2 minutes\n"
                "- Dynamic stretches (arm circles, leg swings) — 3 minutes\n\n"
                "**Main Circuit (20 minutes — 3 rounds):**\n"
                "- Push-ups: 12 reps (modify on knees if needed)\n"
                "- Bodyweight squats: 15 reps\n"
                "- Plank hold: 30 seconds\n"
                "- Lunges: 10 each leg\n"
                "- Rest: 60 seconds between rounds\n\n"
                "**Cool-down (5 minutes):**\n"
                "- Walking in place — 2 minutes\n"
                "- Static stretches (hamstrings, quads, shoulders) — 3 minutes\n\n"
                "Remember: consistency beats intensity! You showed up today, "
                "and that's what matters. See you tomorrow! 🎯\n\n"
                "[Simulation Mode — connect a live API key for personalized plans]"
            ),
        ),
        # #11 — §3.2 System/User Demo (Customer Support)
        (
            ["customer", "internet", "not working", "help"],
            lambda: (
                "I'm sorry to hear you're experiencing internet connectivity issues. "
                "I understand how frustrating this can be, and I'm here to help you "
                "get back online as quickly as possible.\n\n"
                "Let's work through this together step by step:\n\n"
                "**Step 1:** Could you check if the router's power light is on? "
                "If not, please try unplugging it for 30 seconds and plugging it back in.\n\n"
                "**Step 2:** Once the router restarts, check if the WiFi indicator "
                "light is active (usually a blinking or solid green/blue light).\n\n"
                "**Step 3:** Try connecting from a different device if possible — "
                "this helps us determine if the issue is device-specific or network-wide.\n\n"
                "If none of these steps resolve the issue, I'll escalate this to our "
                "network team for further investigation. You'll receive an update "
                "within 2 hours.\n\n"
                "Is there anything else I can help you with while we work on this?\n\n"
                "[Simulation Mode — connect a live API key for dynamic support]"
            ),
        ),
        # #12 — §3.5 Sentiment/Feedback Classification
        (
            ["sentiment", "feedback", "happy", "thanks"],
            lambda: json.dumps(
                {
                    "Urgency": "Low",
                    "Category": "Feedback",
                    "Action": "None",
                    "Reasoning": (
                        "Positive sentiment detected. Customer expressing satisfaction "
                        "with no actionable request. No follow-up needed."
                    ),
                },
                indent=2,
            ),
        ),
        # #13 — Case Study 2: Compliance Pre-Screening
        (
            ["mifid", "fca", "flag", "pre-screen"],
            lambda: json.dumps(
                {
                    "review_id": "COMP-2024-0312",
                    "risk_level": "Medium",
                    "flagged_passages": [
                        {
                            "text_excerpt": "This investment is expected to yield 15% returns...",
                            "policy_reference": "FCA COBS 4.2 — Fair, clear, and not misleading",
                            "concern": "Performance projection without required risk disclaimer",
                        },
                        {
                            "text_excerpt": "We recommend moving all assets into...",
                            "policy_reference": "MiFID II Article 25 — Suitability assessment",
                            "concern": "Recommendation without documented suitability assessment",
                        },
                    ],
                    "reasoning": (
                        "Two passages contain language that may not comply with FCA COBS "
                        "and MiFID II requirements. The first makes forward-looking performance "
                        "claims without mandatory risk disclaimers. The second provides a "
                        "specific recommendation without reference to a suitability assessment."
                    ),
                    "escalation_required": False,
                    "reviewer_action": "Route to compliance officer for detailed review",
                },
                indent=2,
            ),
        ),
        # #14 — Case Study 1: SaaS Triage
        (
            ["sla", "severity", "route", "queue"],
            lambda: json.dumps(
                {
                    "ticket_id": "TKT-2024-1847",
                    "category": "Performance",
                    "severity": "Severity-2",
                    "assigned_queue": "backend-eng",
                    "suggested_action": "Investigate DB query latency",
                    "sla_deadline": "4 hours",
                    "reasoning": (
                        "Customer reports intermittent slowness affecting core workflows. "
                        "Pattern matches database query performance degradation. "
                        "Severity-2 assigned per SLA: not a total outage but impacts productivity."
                    ),
                },
                indent=2,
            ),
        ),
    ]

    @staticmethod
    def _default_response() -> str:
        """Generic fallback when no keywords match."""
        return (
            "**Structured Recommendation**\n\n"
            "Based on the provided context, here are my recommendations:\n\n"
            "1. **Analysis:** The input has been processed and evaluated "
            "against relevant criteria.\n"
            "2. **Recommendation:** Proceed with the proposed approach, "
            "incorporating the constraints specified.\n"
            "3. **Next steps:** Validate outcomes against expected benchmarks "
            "and iterate as needed.\n\n"
            "[Simulation Mode — connect a live API key for dynamic output]"
        )
