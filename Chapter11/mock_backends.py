# mock_backends.py
# Chapter 11: Multi-Modal Perception Agents
# Book: 30 Agents Every AI Engineer Must Build
# Author: Imran Ahmad | Publisher: Packt Publishing
#
# Simulation Mode backends for all three agent domains.
# Each mock class mirrors the real API surface used in the chapter code
# and returns chapter-accurate responses keyed by scenario.
#
# Ref: Technical Requirements (p.2), all three domain sections

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple


# ──────────────────────────────────────────────────────────────────────
# SHARED UTILITIES
# ──────────────────────────────────────────────────────────────────────

@dataclass
class SensorReading:
    """
    A single sensor measurement with temporal metadata.
    Used by MockSensorStream and consumed by SmartBuildingAgent's
    sensor fusion logic.

    Ref: Smart Building Management Architecture, Sensor Fusion (p.23-24)
    """
    timestamp: datetime
    sensor_type: str  # "temperature", "co2", "occupancy"
    value: float
    zone_id: str


class MockInputs(dict):
    """
    Dict subclass that supports .to(device) chaining, mimicking
    the transformers BatchEncoding interface.

    Ref: Building a Vision Question-Answering Agent (p.5-6)
    """

    def __init__(self, prompt_text: str = "", **kwargs):
        super().__init__(**kwargs)
        self._prompt_text = prompt_text

    def to(self, device: Any) -> "MockInputs":
        """No-op device transfer for Simulation Mode."""
        return self

    @property
    def prompt_text(self) -> str:
        return self._prompt_text


# ──────────────────────────────────────────────────────────────────────
# DOMAIN 1: VISION-LANGUAGE
# ──────────────────────────────────────────────────────────────────────

class MockProcessor:
    """
    Simulates transformers.AutoProcessor for Vision-Language models.

    Provides __call__ (tokenization + image preprocessing) and decode
    (detokenization) methods that the VisionQuestionAnsweringAgent
    expects.

    Ref: Building a Vision Question-Answering Agent (p.5-6)
    """

    def __init__(self, model_id: str = "mock-vlm"):
        self.model_id = model_id
        self._last_prompt = ""

    @classmethod
    def from_pretrained(cls, model_id: str) -> "MockProcessor":
        """Factory method matching AutoProcessor.from_pretrained()."""
        return cls(model_id=model_id)

    def __call__(
        self,
        text: str = "",
        images: Any = None,
        audio: Any = None,
        return_tensors: str = "pt",
        **kwargs,
    ) -> MockInputs:
        """
        Mimics processor(text=..., images=..., return_tensors='pt').
        Stores the prompt text for downstream scenario detection.
        """
        self._last_prompt = text
        return MockInputs(
            prompt_text=text,
            input_ids=[[1, 2, 3]],
            attention_mask=[[1, 1, 1]],
        )

    def decode(self, token_ids: Any, skip_special_tokens: bool = True) -> str:
        """
        Returns a pre-built response string based on the last prompt.
        The response includes 'ASSISTANT:' prefix so the VQA agent's
        split logic works correctly.
        """
        return self._last_prompt_response()

    def _last_prompt_response(self) -> str:
        """Select scenario response based on keywords in stored prompt.
        Priority: more specific matches (spatial, count) checked before
        general matches (describe) to avoid false positives."""
        prompt = self._last_prompt.lower()

        # Check specific queries first (spatial/count may co-occur with "describe")
        if "spatial" in prompt or "relationship" in prompt or "where" in prompt:
            return (
                "ASSISTANT: Reasoning: Analyzing spatial layout — the laptop "
                "is centered on the desk. The coffee cup is to the right, "
                "approximately 15cm from the laptop edge. Papers are stacked "
                "beneath the cup. The desk lamp is positioned at the upper "
                "left corner of the desk.\n"
                "Therefore, the answer is: The laptop occupies the center of "
                "the desk, with the coffee cup to its right resting on a "
                "paper stack, and the desk lamp at the upper-left corner."
            )

        if "count" in prompt or "how many" in prompt:
            return (
                "ASSISTANT: Reasoning: I will scan the image systematically "
                "from left to right. I can see one person seated at the desk "
                "and a second person partially occluded by the bookshelf in "
                "the background. There are no other figures visible.\n"
                "Therefore, the answer is: 2 people are visible in the image."
            )

        if "describe" in prompt:
            return (
                "ASSISTANT: Reasoning: The image shows an indoor workspace. "
                "I can identify a desk with a laptop, scattered papers, a "
                "coffee cup positioned near the edge, and an adjustable desk "
                "lamp. The lighting suggests daytime with natural light from "
                "a window on the left side.\n"
                "Therefore, the answer is: This is a cluttered workspace "
                "containing a laptop, papers, a coffee cup precariously "
                "balanced on a stack of documents, and a desk lamp. Natural "
                "light enters from the left."
            )

        # Default fallback
        return (
            "ASSISTANT: Reasoning: I observe a general scene in the image.\n"
            "Therefore, the answer is: The image shows an indoor environment "
            "with standard office furnishings."
        )


class MockVLM:
    """
    Simulates LlavaForConditionalGeneration for Simulation Mode.

    Provides .device attribute and .generate() method matching the
    transformers model interface used by the VQA agent.

    Ref: Building a Vision Question-Answering Agent (p.5-6)
    """

    def __init__(self, model_id: str = "mock-vlm"):
        self.model_id = model_id
        self.device = "cpu"

    @classmethod
    def from_pretrained(
        cls,
        model_id: str,
        torch_dtype: Any = None,
        low_cpu_mem_usage: bool = True,
        device_map: str = "auto",
    ) -> "MockVLM":
        """Factory method matching LlavaForConditionalGeneration.from_pretrained()."""
        return cls(model_id=model_id)

    def generate(self, **kwargs) -> list:
        """
        Returns a mock tensor (list) that MockProcessor.decode() will
        convert to a scenario-appropriate response string.
        """
        # Return a placeholder; actual response is driven by MockProcessor.decode()
        return [[0]]


# ──────────────────────────────────────────────────────────────────────
# DOMAIN 2: AUDIO PROCESSING
# ──────────────────────────────────────────────────────────────────────

# Scenario registry: raw transcript segments with fillers for testing
# CLEAN vs VERBATIM modes.
# Ref: Building a Speech Recognition Agent (p.13-15)
_AUDIO_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "customer_complaint": {
        "full_text": (
            "Yes um I've been waiting for um three weeks now and uh "
            "nobody has called me back. This is um unacceptable and "
            "I want to speak with a manager right now."
        ),
        "segments": [
            {
                "text": "Yes um I've been waiting for um three weeks now",
                "start": 0.0,
                "end": 3.2,
                "confidence": 0.94,
            },
            {
                "text": "and uh nobody has called me back.",
                "start": 3.2,
                "end": 5.5,
                "confidence": 0.91,
            },
            {
                "text": "This is um unacceptable",
                "start": 5.8,
                "end": 7.6,
                "confidence": 0.96,
            },
            {
                "text": "and I want to speak with a manager right now.",
                "start": 7.6,
                "end": 10.1,
                "confidence": 0.98,
            },
        ],
        "language": "en",
    },
    "meeting_notes": {
        "full_text": (
            "So um the Q3 results are in and uh we exceeded targets "
            "by twelve percent. Um the marketing team um deserves "
            "credit for the campaign push."
        ),
        "segments": [
            {
                "text": "So um the Q3 results are in",
                "start": 0.0,
                "end": 2.1,
                "confidence": 0.93,
            },
            {
                "text": "and uh we exceeded targets by twelve percent.",
                "start": 2.1,
                "end": 5.0,
                "confidence": 0.95,
            },
            {
                "text": "Um the marketing team um deserves credit for the campaign push.",
                "start": 5.3,
                "end": 9.2,
                "confidence": 0.90,
            },
        ],
        "language": "en",
    },
}


class MockWhisperBackend:
    """
    Simulates a Whisper-compatible ASR backend for Simulation Mode.

    The transcribe() method returns (full_text, segments, language),
    matching the interface expected by SpeechRecognitionAgent.

    Scenario selection is based on the scenario_key set at construction
    or overridden per-call.

    Ref: Building a Speech Recognition Agent (p.13-15)
    """

    def __init__(self, scenario_key: str = "customer_complaint"):
        self.scenario_key = scenario_key

    def transcribe(
        self, audio: Any, scenario_key: Optional[str] = None
    ) -> Tuple[str, List[Dict[str, Any]], str]:
        """
        Simulate ASR transcription.

        Args:
            audio: NumPy array (ignored in Simulation Mode).
            scenario_key: Override the default scenario for this call.

        Returns:
            Tuple of (full_text, segment_dicts, language_code).
        """
        key = scenario_key or self.scenario_key
        scenario = _AUDIO_SCENARIOS.get(key, _AUDIO_SCENARIOS["customer_complaint"])
        return (
            scenario["full_text"],
            scenario["segments"],
            scenario["language"],
        )


# ──────────────────────────────────────────────────────────────────────
# DOMAIN 3: PHYSICAL WORLD SENSING
# ──────────────────────────────────────────────────────────────────────

# Scenario registry: pre-built sensor reading sets for each demo.
# Values are sourced from the chapter's EventPattern thresholds:
#   - critical_temp: >95°F or <50°F  (p.21)
#   - unexpected_occupancy: >0.7 outside occupied_hours (p.21-22)
#   - CO2 ventilation: >max_co2 (default 1000 ppm) (p.22-23)
#   - deadband: abs(error) > 1.0 from target avg (p.22)
#
# Ref: Smart Building Management Architecture (p.18-24)

def _recent(minutes_ago: float = 1.0) -> datetime:
    """Helper: create a timestamp N minutes in the past."""
    return datetime.now() - timedelta(minutes=minutes_ago)


def _build_sensor_scenarios() -> Dict[str, List[SensorReading]]:
    """
    Build scenario-keyed sensor reading lists.

    Each scenario produces readings within the 5-minute fusion window
    used by SmartBuildingAgent.update_zone_state().
    """
    return {
        # Normal office: 72°F is within default target range (68-76),
        # so deadband check (abs(72 - 72) = 0 < 1.0) produces no commands.
        "normal_office": [
            SensorReading(_recent(1), "temperature", 72.0, "zone_a_office"),
            SensorReading(_recent(2), "temperature", 71.8, "zone_a_office"),
            SensorReading(_recent(3), "temperature", 72.2, "zone_a_office"),
            SensorReading(_recent(1), "co2", 650.0, "zone_a_office"),
            SensorReading(_recent(1), "occupancy", 0.8, "zone_a_office"),
        ],
        # Server room overheat: 96.5°F exceeds the critical_temp
        # threshold of 95°F. Ref: EventPattern critical_temp (p.21)
        "server_room_overheat": [
            SensorReading(_recent(1), "temperature", 96.5, "zone_d_server"),
            SensorReading(_recent(2), "temperature", 96.3, "zone_d_server"),
            SensorReading(_recent(3), "temperature", 96.7, "zone_d_server"),
            SensorReading(_recent(1), "co2", 450.0, "zone_d_server"),
            SensorReading(_recent(1), "occupancy", 0.0, "zone_d_server"),
        ],
        # After-hours intrusion: occupancy 0.9 at 23:00, outside
        # default occupied_hours (8-18).
        # Ref: EventPattern unexpected_occupancy (p.21-22)
        "after_hours_intrusion": [
            SensorReading(_recent(1), "temperature", 70.0, "zone_b_meeting"),
            SensorReading(_recent(1), "co2", 500.0, "zone_b_meeting"),
            SensorReading(_recent(1), "occupancy", 0.9, "zone_b_meeting"),
        ],
        # High CO2 in occupied lab: 1350 ppm exceeds max_co2 (1000).
        # Excess = 350 → ventilation intensity = min(100, 50 + 350/10) = 85.
        # Ref: Control Management and Feedback Loops (p.22-23)
        "high_co2_occupied": [
            SensorReading(_recent(1), "temperature", 73.0, "zone_c_lab"),
            SensorReading(_recent(2), "temperature", 72.8, "zone_c_lab"),
            SensorReading(_recent(1), "co2", 1350.0, "zone_c_lab"),
            SensorReading(_recent(1), "occupancy", 0.95, "zone_c_lab"),
        ],
    }


class MockSensorStream:
    """
    Provides pre-built sensor reading sequences for Simulation Mode.

    Each scenario maps to a list of SensorReading objects with recent
    timestamps, ensuring they pass the 5-minute temporal filter in
    SmartBuildingAgent.update_zone_state().

    Usage:
        stream = MockSensorStream("server_room_overheat")
        readings = stream.get_readings()

    Ref: Smart Building Management Architecture (p.18-24)
    """

    def __init__(self, scenario_key: str = "normal_office"):
        self.scenario_key = scenario_key
        self._scenarios = _build_sensor_scenarios()

    def get_readings(
        self, scenario_key: Optional[str] = None
    ) -> List[SensorReading]:
        """
        Return sensor readings for the specified scenario.

        Args:
            scenario_key: Override the default scenario for this call.

        Returns:
            List of SensorReading objects with recent timestamps.
        """
        key = scenario_key or self.scenario_key
        # Rebuild to get fresh timestamps each call
        fresh = _build_sensor_scenarios()
        return fresh.get(key, fresh["normal_office"])

    @property
    def available_scenarios(self) -> List[str]:
        """List all registered scenario keys."""
        return list(self._scenarios.keys())
