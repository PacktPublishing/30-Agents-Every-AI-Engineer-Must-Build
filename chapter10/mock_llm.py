"""
mock_llm.py — Simulation Layer for Chapter 10

Book: 30 Agents Every AI Engineer Must Build
Author: Imran Ahmad
Chapter: 10 — Conversational and Content Creation Agents

This module provides drop-in replacements for LangChain's ChatOpenAI and
OpenAIEmbeddings classes. When no OPENAI_API_KEY is detected, the notebook
imports MockChatOpenAI and MockOpenAIEmbeddings from this file, enabling
full execution in SIMULATION MODE with zero external dependencies.

Design constraints:
    - No external API calls of any kind
    - Deterministic output — same input always produces same output
    - All mock text derived from chapter examples
    - Implements LangChain interfaces exactly (invoke, Embeddings)
"""

import hashlib
from typing import Any, Dict, List, Optional

import numpy as np
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult

# =========================================================================
# MOCK_RESPONSES — Context-aware synthetic response registry
# Ref: Strategy §10, Chapter 10 Sections 10.1 and 10.2
# =========================================================================

MOCK_RESPONSES: Dict[str, Any] = {

    # --- Section 10.1: The Conversational Agent (Mental Health) ---

    "mental_health": {
        "default": (
            "I appreciate you sharing that with me. It takes courage to talk "
            "about how you're feeling. Can you tell me a bit more about what's "
            "been on your mind? I'm here to listen without judgment, and we "
            "can work through this together at whatever pace feels right."
        ),
        "exam_anxiety": (
            "It sounds like the pressure of exams is really weighing on you "
            "right now. That's a very common experience, and it makes sense "
            "to feel anxious when something important is coming up. What "
            "aspect of the exam feels most overwhelming — is it the material "
            "itself, the time pressure, or something else?"
        ),
        "follow_up_memory": (
            "I remember you mentioned feeling anxious about your exams "
            "earlier. How have things been going since then? Sometimes just "
            "checking back in can help us see how far we've come. Have you "
            "found any strategies that have been working for you?"
        ),
        "crisis": (
            "I'm hearing that you're in a lot of pain. I am an AI and cannot "
            "provide emergency help. Please call 988 immediately."
        ),
    },

    # --- Section 10.2: The Content Creation Agent (Marketing) ---

    "email_specialist": (
        "Subject: Unlock Enterprise-Grade Data Governance with DataVault Pro\n\n"
        "Dear Data Leader,\n\n"
        "Managing data at scale demands more than spreadsheets and good intentions. "
        "DataVault Pro gives your team a unified governance platform built for the "
        "realities of modern data engineering — automated lineage tracking, "
        "role-based access controls, and real-time compliance monitoring.\n\n"
        "Here is what teams like yours are achieving:\n"
        "- 60% reduction in audit preparation time\n"
        "- Automated PII detection across 50+ data sources\n"
        "- One-click compliance reports for SOC 2, GDPR, and HIPAA\n\n"
        "Ready to see it in action? Schedule a personalized demo with our "
        "solutions team.\n\n"
        "Warm regards,\n"
        "The DataVault Pro Team"
    ),

    "seo_writer": (
        "# Why Enterprise Data Governance Is No Longer Optional\n\n"
        "For CTOs and data engineering leads at mid-market companies, the "
        "question is no longer whether to invest in data governance — it is "
        "how to do it without slowing down the teams that depend on fast, "
        "reliable data access.\n\n"
        "## The Cost of Ungoverned Data\n\n"
        "Organizations that delay governance investment face compounding risks: "
        "regulatory penalties, duplicated data pipelines, and eroding trust in "
        "analytical outputs. A 2024 industry survey found that 72% of data "
        "engineering teams spend more than 15 hours per week on manual data "
        "quality checks — time that could be reclaimed with automated policy "
        "enforcement.\n\n"
        "## How DataVault Pro Addresses the Gap\n\n"
        "DataVault Pro approaches governance as an enabler rather than a "
        "bottleneck. Its architecture integrates directly with existing data "
        "stacks — Snowflake, Databricks, BigQuery — and applies governance "
        "rules at the metadata layer without disrupting query performance.\n\n"
        "Key capabilities include:\n"
        "- Automated data lineage from ingestion to dashboard\n"
        "- Policy-as-code frameworks for access control\n"
        "- Continuous compliance monitoring with alerting\n\n"
        "## Taking the Next Step\n\n"
        "Data governance is a strategic investment. The organizations that "
        "treat it as such gain not only compliance confidence but also faster "
        "decision-making and stronger cross-functional trust in their data "
        "assets."
    ),

    "ad_creative": (
        "DataVault Pro — Govern your data, accelerate your decisions.\n\n"
        "Trusted by data teams at 200+ mid-market companies.\n"
        "Automated lineage. Real-time compliance. Zero friction.\n\n"
        "Start your free evaluation today."
    ),

    "editor_revision": (
        "DataVault Pro offers a modern approach to enterprise data governance, "
        "designed for teams that need robust compliance without sacrificing "
        "speed. Our platform integrates seamlessly with your existing data "
        "stack to deliver automated lineage tracking, granular access controls, "
        "and continuous monitoring — all through an intuitive interface that "
        "data engineers and compliance officers both appreciate."
    ),

    "summarizer": (
        "The user discussed feelings of anxiety related to upcoming exams, "
        "particularly in mathematics. They expressed concern about time "
        "pressure and preparation adequacy. The conversation explored coping "
        "strategies and validation of their experience."
    ),
}


# =========================================================================
# MockChatOpenAI — Drop-in replacement for langchain ChatOpenAI
# Ref: Strategy §7.2, Chapter 10 Sections 10.1 and 10.2
# =========================================================================

class MockChatOpenAI(BaseChatModel):
    """
    Simulation-mode replacement for langchain_openai.ChatOpenAI.

    Inspects system prompts and user messages to determine which case study
    is active (Mental Health Agent or Marketing Content Assistant), then
    returns appropriate pre-written responses from MOCK_RESPONSES.

    Extends BaseChatModel for full LangChain pipeline compatibility,
    including ConversationSummaryBufferMemory integration.
    """

    model_name: str = "gpt-4o-mock"
    temperature: float = 0.7

    @property
    def _llm_type(self) -> str:
        return "mock-chat-openai"

    def get_num_tokens(self, text: str) -> int:
        """Approximate token count using word splitting (avoids transformers dependency)."""
        return max(1, len(text.split()) * 4 // 3)

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate a mock chat response from the message list."""
        system_text = ""
        user_text = ""

        for msg in messages:
            content = msg.content if hasattr(msg, "content") else str(msg)
            role = getattr(msg, "type", "unknown")

            if role == "system":
                system_text += " " + content
            elif role == "human":
                user_text += " " + content

        system_text = system_text.lower().strip()
        user_text = user_text.lower().strip()

        response_text = self._dispatch(system_text, user_text)
        ai_message = AIMessage(content=response_text)
        return ChatResult(generations=[ChatGeneration(message=ai_message)])

    def _dispatch(self, system_text: str, user_text: str) -> str:
        """
        Context-aware dispatch logic.

        Routes to the correct mock response based on system prompt keywords
        and user message content. Follows the dispatch tree specified in
        Strategy §7.2.
        """
        # --- Mental Health case study ---
        mental_health_signals = ["supportive peer", "reflective", "empathy"]
        if any(signal in system_text for signal in mental_health_signals):
            mh = MOCK_RESPONSES["mental_health"]

            # Crisis keywords take absolute priority
            crisis_keywords = ["hurt myself", "suicide", "end my life", "harm"]
            if any(kw in user_text for kw in crisis_keywords):
                return mh["crisis"]

            # Exam anxiety
            if any(kw in user_text for kw in ["exam", "study", "test"]):
                return mh["exam_anxiety"]

            # Memory recall / follow-up
            if any(kw in user_text for kw in ["remember", "earlier", "last time"]):
                return mh["follow_up_memory"]

            return mh["default"]

        # --- Content Creation case study ---

        if "email specialist" in system_text:
            return MOCK_RESPONSES["email_specialist"]

        if "seo" in system_text:
            return MOCK_RESPONSES["seo_writer"]

        if "ad creative" in system_text or "display ad" in system_text:
            return MOCK_RESPONSES["ad_creative"]

        if "revise" in system_text or "remove" in system_text:
            return MOCK_RESPONSES["editor_revision"]

        if "summarize" in system_text:
            return MOCK_RESPONSES["summarizer"]

        # --- Fallback ---
        return (
            "Thank you for your message. I have processed your request "
            "and am ready to assist further. [Simulation Mode]"
        )


# =========================================================================
# MockOpenAIEmbeddings — Drop-in replacement for langchain OpenAIEmbeddings
# Ref: Strategy §7.3
# =========================================================================

class MockOpenAIEmbeddings(Embeddings):
    """
    Simulation-mode replacement for langchain_openai.OpenAIEmbeddings.

    Produces deterministic 256-dimensional unit vectors using MD5 hashing.
    Identical input always produces identical output, ensuring reproducible
    FAISS behavior in Simulation Mode.
    """

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of texts into deterministic vectors."""
        return [self._hash_embed(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query text into a deterministic vector."""
        return self._hash_embed(text)

    @staticmethod
    def _hash_embed(text: str) -> List[float]:
        """
        Generate a deterministic 256-dimensional unit vector from text.

        Uses MD5 hash of the input as a seed for numpy RandomState,
        then normalizes to a unit vector for cosine-similarity compatibility.
        """
        md5_hash = hashlib.md5(text.encode("utf-8")).hexdigest()
        seed = int(md5_hash[:8], 16)
        rng = np.random.RandomState(seed)
        raw = rng.randn(256)
        norm = np.linalg.norm(raw)
        if norm == 0:
            return raw.tolist()
        return (raw / norm).tolist()
