# src/mock_layer.py
# Author: Imran Ahmad
# Ref: Chapter 16 — Embodied and Physical World Agents
# Listings 16.1–16.7 + §Constraint formalization (p. 29)
#
# Provides:
#   - MockChatOpenAI: BaseChatModel subclass compatible with create_react_agent
#   - MockGraph:      Graph with outgoing_edges() for propagate_influence()
#   - Edge:           Named tuple for graph edges
#   - get_llm():      Factory returning MockChatOpenAI or ChatOpenAI
#   - MOCK_*:         Failure scenario dicts for notebook demos

import json
import uuid
from collections import namedtuple
from typing import Any, Dict, List, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from resilience import logger


# ---------------------------------------------------------------------------
# Agent Protocol Definitions
# ---------------------------------------------------------------------------
# Each protocol is an ordered list of tool_calls that the mock LLM produces
# in sequence. The agent loop in create_react_agent counts ToolMessage
# responses to determine which step to execute next.
#
# Protocol detection is based on keywords in the first HumanMessage.
# ---------------------------------------------------------------------------

# Protocol 1: Embodied Agent — warehouse robot (Listing 16.2, pp. 15–16)
_EMBODIED_STEPS = [
    {"name": "query_world_model",
     "args": {"query": "package A location, grasp difficulty, and path to shelf B"}},
    {"name": "check_safety_constraints",
     "args": {"action": "pick_and_navigate", "target": "package_A"}},
    {"name": "dispatch_motion_command",
     "args": {"target": "shelf_B", "action": "place_package_A"}},
]
_EMBODIED_TERMINAL = (
    "Mission complete. Package A has been picked from its current location "
    "and placed on shelf B. All safety constraints were validated before each "
    "action via check_safety_constraints. The world model confirmed collision-free "
    "path and stable placement (ΣF_i = 0, Στ_i = 0)."
)

# Protocol 2: Graph Builder — cross-domain knowledge graph (Listing 16.4, pp. 23–24)
_GRAPH_BUILDER_STEPS = [
    {"name": "query_energy_grid",
     "args": {"region": "downtown_corridor"}},
    {"name": "query_traffic_network",
     "args": {"region": "downtown_corridor"}},
    {"name": "register_cross_domain_edge",
     "args": {"source_id": "Substation-7", "target_id": "TrafficController-12",
              "relation": "powers", "weight": 0.85}},
]
_GRAPH_BUILDER_TERMINAL = (
    "Knowledge graph constructed. Registered node clusters: "
    "Energy (Substation-7, capacity=45MW, load=38MW) and "
    "Transportation (TrafficController-12, 14 intersections). "
    "Cross-domain edge: Substation-7 --powers--> TrafficController-12 (weight=0.85)."
)

# Protocol 3: Mission Supervisor — drone flight (Listing 16.6, pp. 31–34)
_MISSION_SUPERVISOR_STEPS = [
    {"name": "query_flight_state",
     "args": {"drone_id": "drone-1"}},
    # check_flight_safety receives state JSON from query_flight_state
    # Ref: §Constraint formalization (p. 29) thresholds
    {"name": "check_flight_safety",
     "args": {"state_json": json.dumps({
         "temperature_c": -6.2,       # > -10°C limit (p. 29)
         "wind_speed_kmh": 18.5,      # < 25 km/h limit (p. 29)
         "precipitation_active": False,
         "battery_soc": 0.82,         # > 0.30 departure floor (p. 29)
     })}},
    # Waypoint: corridor from Centerpointe to Ottawa River (p. 27)
    {"name": "dispatch_waypoint_command",
     "args": {"waypoint_lat": 45.3876, "waypoint_lon": -75.6960,
              "altitude_m": 120.0, "airspeed_kmh": 40.0}},
]
_MISSION_SUPERVISOR_TERMINAL = (
    "Mission authorized and first waypoint dispatched. "
    "Unified Constraint Envelope: ALL GREEN. "
    "Weather: -6.2°C (limit -10°C), wind 18.5 km/h (limit 25 km/h), no precipitation. "
    "Battery SoC: 82% (floor 30%). "
    "Waypoint: (45.3876°N, 75.6960°W) at 120m AGL, 40 km/h airspeed."
)

# Protocol 4: Constraint Assembler — 5-domain envelope (Listing 16.7, pp. 34–38)
_CONSTRAINT_ASSEMBLER_STEPS = [
    {"name": "query_weather_constraints",
     "args": {"corridor_id": "CENTERPOINTE_OTTAWARIVER"}},
    {"name": "query_airspace_notams",
     "args": {"corridor_id": "CENTERPOINTE_OTTAWARIVER"}},
    {"name": "query_battery_state",
     "args": {"drone_id": "drone-1"}},
    {"name": "query_parks_restrictions",
     "args": {"route_geojson": "{}"}},
    {"name": "register_constraint_node",
     "args": {"domain": "ENVELOPE", "node_id": "unified-envelope",
              "constraint_met": True, "weight": 1.0}},
]
_CONSTRAINT_ASSEMBLER_TERMINAL = json.dumps({
    "unified_envelope_green": True,
    "domain_status": {
        "weather": True,
        "airspace": True,
        "battery": True,
        "parks": True,
        "mission_geometry": True,
    },
    "constraint_margins": {
        "temperature_margin_c": 3.8,    # -6.2 vs -10.0 limit
        "wind_margin_kmh": 6.5,         # 18.5 vs 25.0 limit
        "battery_margin_pct": 0.52,     # 0.82 vs 0.30 floor
    },
})

# Protocol registry: keyword → (steps, terminal_message)
_PROTOCOLS: Dict[str, tuple] = {
    "mission_supervisor":   (_MISSION_SUPERVISOR_STEPS, _MISSION_SUPERVISOR_TERMINAL),
    "constraint_assembler": (_CONSTRAINT_ASSEMBLER_STEPS, _CONSTRAINT_ASSEMBLER_TERMINAL),
    "graph_builder":        (_GRAPH_BUILDER_STEPS, _GRAPH_BUILDER_TERMINAL),
    "embodied":             (_EMBODIED_STEPS, _EMBODIED_TERMINAL),
}


# ---------------------------------------------------------------------------
# MockChatOpenAI
# ---------------------------------------------------------------------------

class MockChatOpenAI(BaseChatModel):
    """Drop-in mock for ChatOpenAI compatible with LangGraph create_react_agent.

    Subclasses BaseChatModel and implements _generate() to return AIMessage
    objects with correctly formatted tool_calls fields. Protocol detection
    is based on keywords in the first HumanMessage; step sequencing uses the
    count of ToolMessage objects in the conversation history.

    Ref: Strategy §7 — MockChatOpenAI Compatibility
    """

    model_name: str = "mock-gpt-4o-simulation"
    """Identifier shown in logs."""

    scenario: str = "default"
    """Scenario key for failure demos: 'default', 'wind_red', 'battery_red',
    'notam_active'. Controls which protocol variant is used."""

    class Config:
        arbitrary_types_allowed = True

    @property
    def _llm_type(self) -> str:
        return "mock-chat-openai"

    # --- bind_tools support for create_react_agent ---

    def bind_tools(self, tools: list, **kwargs: Any) -> "MockChatOpenAI":
        """Store tool schemas and return self for LangGraph compatibility.

        create_react_agent calls llm.bind_tools(tools) to produce a model
        that 'knows' the available tools. Since our mock pre-scripts tool_calls
        by protocol, we just store names for logging and return self.
        """
        names = []
        for t in tools:
            if hasattr(t, "name"):
                names.append(t.name)
            elif isinstance(t, dict) and "name" in t:
                names.append(t["name"])
        logger.simulation(
            f"MockChatOpenAI.bind_tools: {names}",
            section_ref="§Simulation Mode",
        )
        return self

    # --- Core generation ---

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Produce the next AIMessage in the active protocol sequence.

        1. Detect protocol from HumanMessage keywords.
        2. Count ToolMessages to determine current step.
        3. Return AIMessage with tool_calls (if more steps remain)
           or plain text (terminal message).
        """
        protocol_key = self._detect_protocol(messages)
        steps, terminal = _PROTOCOLS[protocol_key]

        # Failure-scenario overrides
        if self.scenario != "default" and protocol_key in ("mission_supervisor", "constraint_assembler"):
            steps, terminal = self._get_failure_protocol(protocol_key)

        step_index = self._count_tool_results(messages)

        if step_index < len(steps):
            tool_call = steps[step_index]
            call_id = f"call_{protocol_key}_{step_index}_{uuid.uuid4().hex[:8]}"
            ai_msg = AIMessage(
                content="",
                tool_calls=[{
                    "name": tool_call["name"],
                    "args": tool_call["args"],
                    "id": call_id,
                    "type": "tool_call",
                }],
            )
        else:
            ai_msg = AIMessage(content=terminal)

        return ChatResult(generations=[ChatGeneration(message=ai_msg)])

    # --- Protocol detection ---

    def _detect_protocol(self, messages: List[BaseMessage]) -> str:
        """Identify the agent protocol from HumanMessage content."""
        for msg in messages:
            if isinstance(msg, (HumanMessage, dict)):
                content = msg.content if hasattr(msg, "content") else str(msg)
                content_lower = content.lower()
                # Order matters: more specific patterns first
                if "query_flight_state" in content_lower or "protocol:" in content_lower:
                    return "mission_supervisor"
                if "constraint domain" in content_lower or "four constraint" in content_lower:
                    return "constraint_assembler"
                if "knowledge graph" in content_lower or "cross-domain" in content_lower:
                    return "graph_builder"
                if "package" in content_lower or "shelf" in content_lower or "warehouse" in content_lower:
                    return "embodied"
        return "embodied"  # Default fallback

    def _count_tool_results(self, messages: List[BaseMessage]) -> int:
        """Count ToolMessage objects to determine the current step index."""
        return sum(1 for m in messages if isinstance(m, ToolMessage))

    # --- Failure scenario protocols ---

    def _get_failure_protocol(self, protocol_key: str) -> tuple:
        """Return modified protocol steps for failure demonstrations."""
        if self.scenario == "wind_red":
            # Mission supervisor: query state → safety check returns RED → NO dispatch
            return (
                _MISSION_SUPERVISOR_STEPS[:2],  # Only query + check, no dispatch
                "FLIGHT ABORTED. Unified Constraint Envelope: RED. "
                "Wind domain failed: 32.0 km/h exceeds 25 km/h operational ceiling "
                "(§Constraint formalization, p. 29). Drone will not arm.",
            )
        elif self.scenario == "battery_red":
            return (
                _MISSION_SUPERVISOR_STEPS[:2],
                "FLIGHT ABORTED. Unified Constraint Envelope: RED. "
                "Battery domain failed: SoC 22% below 30% departure floor "
                "(§Constraint formalization, p. 29). Drone will not arm.",
            )
        elif self.scenario == "notam_active":
            if protocol_key == "constraint_assembler":
                return (
                    _CONSTRAINT_ASSEMBLER_STEPS[:4],  # All queries, no register
                    json.dumps({
                        "unified_envelope_green": False,
                        "domain_status": {
                            "weather": True,
                            "airspace": False,
                            "battery": True,
                            "parks": True,
                            "mission_geometry": True,
                        },
                        "blocking_notam": "NOTAM-CYOW-2025-0099: TFR active in corridor",
                    }),
                )
            return (
                _MISSION_SUPERVISOR_STEPS[:1],
                "FLIGHT ABORTED. Constraint assembler reports airspace domain RED. "
                "Active NOTAM TFR in CENTERPOINTE_OTTAWARIVER corridor. "
                "Drone will not arm until NOTAM is lifted.",
            )
        # Default: return normal protocol
        return _PROTOCOLS[protocol_key]


# ---------------------------------------------------------------------------
# MockGraph — for propagate_influence() (Listing 16.5, pp. 25–26)
# ---------------------------------------------------------------------------

Edge = namedtuple("Edge", ["target_id", "weight"])
"""Typed edge in the domain knowledge graph G = (V, E).
Ref: §Structural topology: The domain knowledge graph (p. 21)"""


class MockGraph:
    """In-memory graph supporting outgoing_edges() for influence propagation.

    Ref: §Structural topology (p. 21) — G = (V, E) with typed entities
    across domains and typed, weighted, directional relations.
    """

    def __init__(self) -> None:
        self._edges: Dict[str, List[Edge]] = {}
        self._nodes: Dict[str, Dict[str, Any]] = {}

    def add_edge(self, source_id: str, target_id: str,
                 relation: str = "", weight: float = 1.0) -> dict:
        """Add a weighted directed edge from source to target."""
        edge = Edge(target_id=target_id, weight=weight)
        self._edges.setdefault(source_id, []).append(edge)
        return {"source": source_id, "target": target_id,
                "relation": relation, "weight": weight, "status": "registered"}

    def add_constraint_node(self, domain: str, node_id: str,
                            status: str = "GREEN", weight: float = 1.0) -> dict:
        """Register a typed constraint node (used by Listing 16.7)."""
        self._nodes[node_id] = {
            "domain": domain, "status": status, "weight": weight
        }
        return {"node_id": node_id, "domain": domain,
                "status": status, "registered": True}

    def outgoing_edges(self, node_id: str) -> List[Edge]:
        """Return all outgoing edges from a node.
        Ref: Listing 16.5 — propagate_influence calls graph.outgoing_edges()"""
        return self._edges.get(node_id, [])

    def get_node(self, node_id: str) -> Optional[dict]:
        """Retrieve node metadata."""
        return self._nodes.get(node_id)


def build_city_storm_graph() -> MockGraph:
    """Construct the city/storm scenario graph from the chapter narrative.

    Ref: §Structural topology (p. 21) and §Influence propagation (pp. 25–26)
    Substation-7 → TrafficController-12 → 14 downstream intersections.
    Also models emergency service dependency.
    """
    g = MockGraph()

    # Energy → Transportation: Substation-7 powers TrafficController-12
    # Ref: p. 21 — "Substation-7 (energy domain) connects via a 'powers'
    # edge to TrafficController-12 (transportation domain)"
    g.add_edge("Substation-7", "TrafficController-12",
               relation="powers", weight=0.85)

    # TrafficController-12 governs downstream intersections
    # Ref: p. 21 — "which connects via 'governs' edges to the
    # intersections it controls"
    for i in range(1, 15):  # 14 intersections (p. 21)
        g.add_edge(f"TrafficController-12", f"Intersection-{i}",
                   relation="governs", weight=0.7)

    # Intersections affect emergency response routes
    # Ref: p. 26 — "emergency response routes that depend on those intersections"
    for i in [3, 7, 11]:  # Key intersections on ambulance routes
        g.add_edge(f"Intersection-{i}", "EmergencyRoute-Central",
                   relation="affects", weight=0.6)

    # Weather affects energy (lightning → substation)
    g.add_edge("WeatherSystem-Storm", "Substation-7",
               relation="disrupts", weight=0.9)

    return g


# ---------------------------------------------------------------------------
# Failure Scenario Mock Data
# ---------------------------------------------------------------------------
# These dicts override tool return values in notebook failure demo cells.
# Each dict documents which chapter threshold it violates.
# Ref: §Constraint formalization (p. 29) for all thresholds.

MOCK_WIND_RED: Dict[str, Any] = {
    # Wind exceeds 25 km/h ceiling (p. 29: "wind speed below 25 km/hr")
    "position_lat": 45.3490,
    "position_lon": -75.7544,
    "altitude_m": 0.0,
    "battery_soc": 0.82,
    "wind_speed_kmh": 32.0,       # VIOLATION: > 25 km/h
    "temperature_c": -6.2,
    "precipitation_active": False,
    "constraint_envelope_green": False,
}

MOCK_BATTERY_RED: Dict[str, Any] = {
    # Battery SoC below 30% departure floor (p. 29: "SoC at or above 30%")
    "position_lat": 45.3490,
    "position_lon": -75.7544,
    "altitude_m": 0.0,
    "battery_soc": 0.22,          # VIOLATION: < 0.30
    "wind_speed_kmh": 18.5,
    "temperature_c": -6.2,
    "precipitation_active": False,
    "constraint_envelope_green": False,
}

MOCK_NOTAM_ACTIVE: Dict[str, Any] = {
    # Active NOTAM TFR in corridor (p. 29: "NOTAM restriction immediately
    # invalidates the corresponding flight segment")
    "notams": [
        {
            "alert_id": "NOTAM-CYOW-2025-0099",
            "corridor": "CENTERPOINTE_OTTAWARIVER",
            "restriction_type": "TFR",    # Temporary Flight Restriction
            "valid_from": "2025-01-15T06:00:00Z",
            "valid_until": "2025-01-15T22:00:00Z",
            "authority": "Transport Canada",
        }
    ],
    "airspace_constraint_met": False,     # RED
}

MOCK_API_TIMEOUT: Dict[str, Any] = {
    # Simulates API timeout — used with fail_gracefully decorator demo
    # Ref: Listing 16.3 (pp. 17–18) — TimeoutError handling pattern
    "trigger": "timeout",
    "timeout_seconds": 5.0,
    "error_message": "Weather API did not respond within 5.0s",
}

MOCK_STALE_DATA: Dict[str, Any] = {
    # Stale weather reading — timestamp exceeds staleness threshold
    # Ref: Prose after Listing 16.7 (p. 38): "A domain whose data timestamp
    # exceeds a staleness threshold is flagged as STALE rather than GREEN"
    "temperature_c": -6.2,
    "wind_speed_kmh": 18.5,
    "precipitation_active": False,
    "temperature_constraint_met": True,
    "wind_constraint_met": True,
    "precip_constraint_met": True,
    "data_timestamp": "2025-01-15T06:00:00Z",  # 12+ hours stale
    "staleness_flag": "STALE",                  # Treated as RED by fusion
}


# ---------------------------------------------------------------------------
# get_llm() — LLM factory function
# ---------------------------------------------------------------------------

def get_llm(simulation_mode: bool = True):
    """Return MockChatOpenAI (simulation) or ChatOpenAI (live).

    Ref: §Technical requirements (p. 2) — OpenAI API key with gpt-4o access.
    The factory implements the cascading fallback:
        .env → getpass → Simulation Mode (MockChatOpenAI)

    Args:
        simulation_mode: If True, return MockChatOpenAI. If False, attempt
            to instantiate ChatOpenAI with the loaded API key.

    Returns:
        A BaseChatModel instance usable with create_react_agent.
    """
    if simulation_mode:
        logger.simulation(
            "Simulation Mode active — using MockChatOpenAI with "
            "chapter-accurate mock data. No API key required.",
            section_ref="§Technical requirements",
        )
        return MockChatOpenAI()
    else:
        try:
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model="gpt-4o", temperature=0.0)
            logger.info(
                "Live Mode active — using ChatOpenAI(gpt-4o).",
                section_ref="§Technical requirements",
            )
            return llm
        except Exception as exc:
            logger.error(
                f"Failed to initialize ChatOpenAI: {exc}. "
                f"Falling back to Simulation Mode.",
                section_ref="§Technical requirements",
            )
            return MockChatOpenAI()
