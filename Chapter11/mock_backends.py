"""
mock_backends.py — High-Fidelity Mock Backends for Simulation Mode
===================================================================
Book:    30 Agents Every AI Engineer Must Build
Author:  Imran Ahmad
Chapter: 11 — Multi-Modal Perception Agents
Ref:     Technical Requirements + all three domain sections

Provides mock implementations so the entire notebook runs without
GPU hardware, Hugging Face tokens, or microphone access.

Classes:
    MockVLM             — Simulates LLaVA 1.5 vision-language model
    MockProcessor       — Simulates AutoProcessor for image+text inputs
    MockWhisperBackend  — Simulates Whisper speech recognition + sentiment
    MockSensorStream    — Simulates IoT sensor data for building management

Every mock returns realistic, chapter-sourced data keyed to scenario names
from the Mock Data ↔ Chapter Section Mapping table.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


# ============================================================
# Vision-Language Mocks
# Ref: Architecture of Vision-Language Agents, Building a Vision QA Agent
# ============================================================

class MockProcessor:
    """Simulates transformers.AutoProcessor for LLaVA 1.5.

    Ref: Architecture of Vision-Language Agents — alignment mechanism.
    Author: Imran Ahmad

    In Live Mode, AutoProcessor tokenizes text and preprocesses images.
    This mock simply packages the inputs into a dict that MockVLM expects.
    """

    def __init__(self, model_id: str = "mock-llava") -> None:
        self.model_id = model_id

    def __call__(
        self,
        text: str | list[str] = "",
        images: Any = None,
        return_tensors: str = "pt",
        padding: bool = True,
    ) -> Dict[str, Any]:
        """Package text + image into a mock input dict.

        Args:
            text:           The prompt or question string.
            images:         A PIL Image or None.
            return_tensors: Ignored in mock (always 'pt' in live).
            padding:        Ignored in mock.

        Returns:
            dict with 'input_ids' (placeholder) and '_mock_text' / '_mock_image'.
        """
        if images is None:
            raise ValueError(
                "MockProcessor received None as image input. "
                "Provide a valid PIL Image. [Ref: Building a Vision QA Agent]"
            )
        return {
            "input_ids": [0],  # placeholder tensor-like
            "_mock_text": text if isinstance(text, str) else text[0],
            "_mock_image": images,
        }


class MockVLM:
    """Simulates LLaVA 1.5 (7B) vision-language model inference.

    Ref: Building a Vision QA Agent — the model generates natural-language
    answers conditioned on the image and a text question.
    Author: Imran Ahmad

    Scenario routing (keyword-based):
        "describe" → detailed workspace description
        "count"    → object/person counting response
        "spatial"  → spatial relationship analysis
        (default)  → generic visual observation
    """

    # Chapter-sourced mock responses keyed by scenario
    _RESPONSES: Dict[str, str] = {
        "describe": (
            "The image shows a modern workspace with a dual-monitor setup, "
            "an ergonomic keyboard, and a desk lamp providing warm lighting. "
            "Several sticky notes are arranged on the left monitor's bezel. "
            "A coffee mug sits to the right of the keyboard. "
            "Chain-of-thought: I identified the primary objects (monitors, "
            "keyboard, lamp, sticky notes, mug) and described their spatial "
            "arrangement from left to right."
        ),
        "count": (
            "I can see 2 people in the image. One person is seated at the "
            "desk facing the monitors, and another is standing near the "
            "whiteboard in the background. "
            "Chain-of-thought: I scanned the image for human figures, "
            "identified two distinct individuals by pose and location."
        ),
        "spatial": (
            "The monitors are positioned centrally on the desk. The keyboard "
            "is directly in front of the monitors. The desk lamp is to the "
            "upper-left, and the coffee mug is to the lower-right of the "
            "keyboard. The whiteboard is mounted on the wall behind the desk. "
            "Chain-of-thought: I established a reference frame (desk center) "
            "and described each object's relative position."
        ),
    }

    _DEFAULT_RESPONSE: str = (
        "The image contains several objects arranged in an indoor setting. "
        "Chain-of-thought: I performed a general visual scan and summarized "
        "the most salient elements."
    )

    def __init__(self, model_id: str = "mock-llava-1.5-7b") -> None:
        self.model_id = model_id

    def generate(self, **kwargs: Any) -> list[list[int]]:
        """Simulate model.generate() — returns placeholder token IDs.

        The notebook's decode step will call MockVLM.decode() instead of
        a real tokenizer, so this just stores the scenario key.
        """
        mock_text = kwargs.get("_mock_text", "")
        # Stash for decode
        self._last_text = mock_text
        return [[0]]  # placeholder token IDs

    def decode(self, token_ids: list[int], skip_special_tokens: bool = True) -> str:
        """Return the scenario-matched mock response string.

        Args:
            token_ids:          Ignored (placeholder from generate).
            skip_special_tokens: Ignored in mock.

        Returns:
            A chapter-sourced natural-language answer.
        """
        text = getattr(self, "_last_text", "").lower()
        for key, response in self._RESPONSES.items():
            if key in text:
                return response
        return self._DEFAULT_RESPONSE


# ============================================================
# Audio Processing Mocks
# Ref: Architecture of Audio Processing Agents,
#      Building a Speech Recognition Agent,
#      Voice Sentiment Analysis
# ============================================================

@dataclass
class MockTranscriptionSegment:
    """A single timestamped segment of transcribed speech.

    Ref: Building a Speech Recognition Agent.
    Author: Imran Ahmad
    """
    start: float
    end: float
    text: str
    confidence: float = 0.95


class MockWhisperBackend:
    """Simulates Whisper-based speech recognition and voice sentiment.

    Ref: Building a Speech Recognition Agent, Voice Sentiment Analysis.
    Author: Imran Ahmad

    Scenario keys:
        "customer_complaint" — Clean mode: fillers ('um', 'uh') removed
        "meeting_notes"      — Verbatim mode: fillers preserved
    """

    _SCENARIOS: Dict[str, Dict[str, Any]] = {
        "customer_complaint": {
            "raw_segments": [
                MockTranscriptionSegment(0.0, 2.1, "I've been waiting for three weeks"),
                MockTranscriptionSegment(2.1, 4.3, "um and nobody has called me back"),
                MockTranscriptionSegment(4.3, 6.8, "uh this is completely unacceptable"),
                MockTranscriptionSegment(6.8, 9.0, "I want to speak to a manager"),
            ],
            "clean_segments": [
                MockTranscriptionSegment(0.0, 2.1, "I've been waiting for three weeks"),
                MockTranscriptionSegment(2.1, 4.3, "and nobody has called me back"),
                MockTranscriptionSegment(4.3, 6.8, "this is completely unacceptable"),
                MockTranscriptionSegment(6.8, 9.0, "I want to speak to a manager"),
            ],
        },
        "meeting_notes": {
            "raw_segments": [
                MockTranscriptionSegment(0.0, 3.2, "So um the quarterly numbers look good"),
                MockTranscriptionSegment(3.2, 5.9, "uh we exceeded target by twelve percent"),
                MockTranscriptionSegment(5.9, 8.4, "um the main driver was the new product line"),
            ],
            "clean_segments": [
                MockTranscriptionSegment(0.0, 3.2, "So the quarterly numbers look good"),
                MockTranscriptionSegment(3.2, 5.9, "we exceeded target by twelve percent"),
                MockTranscriptionSegment(5.9, 8.4, "the main driver was the new product line"),
            ],
        },
    }

    # Prosodic features for sentiment analysis
    # Ref: Voice Sentiment Analysis — VAD (Valence-Arousal-Dominance) model
    _PROSODIC: Dict[str, Dict[str, float]] = {
        "angry": {"pitch_hz": 210.0, "speech_rate_sps": 5.8, "energy_db": -12.0},
        "calm":  {"pitch_hz": 140.0, "speech_rate_sps": 3.2, "energy_db": -28.0},
    }

    def __init__(self, model_id: str = "mock-whisper-large-v3") -> None:
        self.model_id = model_id

    def transcribe(
        self,
        audio: Any,
        scenario: str = "customer_complaint",
        clean: bool = True,
    ) -> List[MockTranscriptionSegment]:
        """Simulate Whisper transcription.

        Args:
            audio:    Audio array (ignored in mock — scenario key drives output).
            scenario: One of 'customer_complaint' or 'meeting_notes'.
            clean:    If True, return filler-removed segments; else verbatim.

        Returns:
            List of MockTranscriptionSegment objects.
        """
        data = self._SCENARIOS.get(scenario, self._SCENARIOS["customer_complaint"])
        key = "clean_segments" if clean else "raw_segments"
        return data[key]

    def get_prosodic_features(
        self, audio: Any, emotion: str = "angry"
    ) -> Dict[str, float]:
        """Return mock prosodic features for sentiment analysis.

        Ref: Voice Sentiment Analysis — prosodic feature extraction.
        Author: Imran Ahmad

        Args:
            audio:   Audio array (ignored in mock).
            emotion: Scenario key — 'angry' or 'calm'.

        Returns:
            Dict with pitch_hz, speech_rate_sps, energy_db.
        """
        return self._PROSODIC.get(emotion, self._PROSODIC["angry"]).copy()


# ============================================================
# Physical World Sensing Mocks
# Ref: Smart Building Management Architecture,
#      Event Detection Through Pattern Matching,
#      Control Management and Feedback Loops,
#      Sensor Fusion Through Data Aggregation
# ============================================================

@dataclass
class MockSensorReading:
    """A single sensor reading from a building zone.

    Ref: Smart Building Management Architecture.
    Author: Imran Ahmad
    """
    zone_id: str
    timestamp: datetime
    temperature_f: float
    humidity_pct: float
    co2_ppm: float
    occupancy_fraction: float
    light_lux: float


class MockSensorStream:
    """Simulates IoT sensor data streams for smart building management.

    Ref: Smart Building Management Architecture, Event Detection,
         Control Management, Sensor Fusion.
    Author: Imran Ahmad

    Scenario keys (zone_id → scenario):
        "zone_a_office"  / "normal_office"         — 72°F, normal
        "zone_d_server"  / "server_room_overheat"   — 96.5°F, critical
        "zone_b_meeting" / "after_hours_intrusion"   — occupancy at 23:00
        "zone_c_lab"     / "high_co2_occupied"       — CO2 1350 ppm
    """

    _SCENARIOS: Dict[str, Dict[str, Any]] = {
        "normal_office": {
            "zone_id": "zone_a_office",
            "temperature_f": 72.0,
            "humidity_pct": 45.0,
            "co2_ppm": 620.0,
            "occupancy_fraction": 0.4,
            "light_lux": 350.0,
            "hour": 10,
        },
        "server_room_overheat": {
            "zone_id": "zone_d_server",
            "temperature_f": 96.5,
            "humidity_pct": 30.0,
            "co2_ppm": 410.0,
            "occupancy_fraction": 0.0,
            "light_lux": 50.0,
            "hour": 14,
        },
        "after_hours_intrusion": {
            "zone_id": "zone_b_meeting",
            "temperature_f": 68.0,
            "humidity_pct": 42.0,
            "co2_ppm": 500.0,
            "occupancy_fraction": 0.9,
            "light_lux": 20.0,
            "hour": 23,
        },
        "high_co2_occupied": {
            "zone_id": "zone_c_lab",
            "temperature_f": 74.0,
            "humidity_pct": 55.0,
            "co2_ppm": 1350.0,
            "occupancy_fraction": 0.7,
            "light_lux": 500.0,
            "hour": 11,
        },
    }

    # Reverse map: zone_id → scenario key
    _ZONE_MAP: Dict[str, str] = {
        v["zone_id"]: k for k, v in _SCENARIOS.items()
    }

    def __init__(self) -> None:
        self._history: Dict[str, List[MockSensorReading]] = {}

    def get_reading(self, zone_id: str) -> MockSensorReading:
        """Return a single mock sensor reading for the given zone.

        Routes by zone_id or falls back to treating zone_id as a scenario key.

        Args:
            zone_id: Either a zone identifier ('zone_a_office') or
                     a scenario key ('normal_office').

        Returns:
            MockSensorReading with chapter-sourced values.
        """
        # Resolve scenario key
        scenario_key = self._ZONE_MAP.get(zone_id, zone_id)
        data = self._SCENARIOS.get(scenario_key)
        if data is None:
            # Fallback to normal_office if unknown zone
            data = self._SCENARIOS["normal_office"]
            scenario_key = "normal_office"

        reading = MockSensorReading(
            zone_id=data["zone_id"],
            timestamp=datetime.now().replace(hour=data["hour"], minute=0, second=0),
            temperature_f=data["temperature_f"],
            humidity_pct=data["humidity_pct"],
            co2_ppm=data["co2_ppm"],
            occupancy_fraction=data["occupancy_fraction"],
            light_lux=data["light_lux"],
        )

        # Store in history for sensor fusion (temporal averaging)
        self._history.setdefault(data["zone_id"], []).append(reading)
        return reading

    def get_history(
        self, zone_id: str, window_size: int = 5
    ) -> List[MockSensorReading]:
        """Return recent readings for temporal averaging (sensor fusion).

        Ref: Sensor Fusion Through Data Aggregation.
        Author: Imran Ahmad

        If fewer readings exist than window_size, duplicates the last
        reading to fill the window (simulates steady-state).

        Args:
            zone_id:     The zone identifier.
            window_size: Number of readings to return.

        Returns:
            List of MockSensorReading (most recent last).
        """
        resolved = self._ZONE_MAP.get(zone_id, zone_id)
        actual_zone = self._SCENARIOS.get(resolved, {}).get("zone_id", zone_id)

        history = self._history.get(actual_zone, [])
        if not history:
            # Generate one reading to seed history
            self.get_reading(zone_id)
            history = self._history.get(actual_zone, [])

        # Pad to window_size by repeating last reading
        while len(history) < window_size:
            history.append(history[-1])

        return history[-window_size:]
