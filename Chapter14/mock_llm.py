# mock_llm.py
# Chapter 14: Financial and Legal Domain Agents
# Book: 30 Agents Every AI Engineer Must Build — Imran Ahmad (Packt Publishing)
# Author: Imran Ahmad
#
# Provides the resilience layer, color-coded logging, service configuration,
# and mock implementations that enable Simulation Mode without API keys.
# Ref: Technical Requirements (p.2), Sections 14.1–14.2

import os
import sys
import time
import hashlib
import functools
import math
from datetime import datetime
from typing import Any, Callable, Optional


# ═══════════════════════════════════════════════════════════════════════════════
# B1: ColorLogger — Color-coded visual logging
# Ref: Used across all sections for agent activity tracing
# ═══════════════════════════════════════════════════════════════════════════════

class ColorLogger:
    """Color-coded logger for agent activity tracing.

    Provides visual distinction between information (BLUE), success (GREEN),
    error (RED), and warning (YELLOW) messages with ISO timestamps.

    Author: Imran Ahmad
    Ref: Chapter 14, all sections
    """

    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    def __init__(self, name: str = "Chapter14"):
        self.name = name

    def _timestamp(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def _log(self, color: str, level: str, message: str):
        ts = self._timestamp()
        prefix = f"{color}{self.BOLD}[{ts}] [{self.name}] {level}{self.RESET}"
        print(f"{prefix} {color}{message}{self.RESET}")

    def info(self, message: str):
        """Log informational message in BLUE."""
        self._log(self.BLUE, "INFO", message)

    def success(self, message: str):
        """Log success message in GREEN."""
        self._log(self.GREEN, "SUCCESS", message)

    def error(self, message: str):
        """Log handled error in RED."""
        self._log(self.RED, "ERROR", message)

    def warning(self, message: str):
        """Log warning in YELLOW."""
        self._log(self.YELLOW, "WARNING", message)


# Module-level logger instance
logger = ColorLogger("Chapter14")


# ═══════════════════════════════════════════════════════════════════════════════
# B2: ServiceConfig — Per-service API key detection with dashboard
# Ref: Technical Requirements (p.2)
# ═══════════════════════════════════════════════════════════════════════════════

class ServiceConfig:
    """Detects per-service API availability and prints a status dashboard.

    For each service (OpenAI, Finnhub, Tavily), checks os.getenv first,
    then falls back to getpass if running interactively. Empty inputs
    activate Simulation Mode for that service.

    Author: Imran Ahmad
    Ref: Chapter 14, Technical Requirements (p.2)
    """

    SERVICES = {
        "OPENAI_API_KEY": "OpenAI (LLM)",
        "FINNHUB_API_KEY": "Finnhub (Financial Data)",
        "TAVILY_API_KEY": "Tavily (News Search)",
    }

    def __init__(self):
        self.status = {}
        self.keys = {}
        self._detect_all()
        self._print_dashboard()

    def _detect_all(self):
        for env_var, label in self.SERVICES.items():
            key = os.getenv(env_var, "")
            if not key:
                key = self._try_getpass(env_var, label)
            is_live = bool(key and key.strip())
            self.status[env_var] = is_live
            self.keys[env_var] = key if is_live else ""

    @staticmethod
    def _try_getpass(env_var: str, label: str) -> str:
        """Prompt for key via getpass; return empty if non-interactive."""
        try:
            if not sys.stdin.isatty():
                return ""
            import getpass
            key = getpass.getpass(
                f"  Enter {label} key (or press Enter for Simulation): "
            )
            return key
        except (EOFError, OSError, KeyboardInterrupt):
            return ""

    def _print_dashboard(self):
        border = "═" * 54
        print(f"\n{border}")
        print("  CHAPTER 14 — SERVICE STATUS DASHBOARD")
        print("  Book: 30 Agents Every AI Engineer Must Build")
        print("  Author: Imran Ahmad")
        print(border)
        for env_var, label in self.SERVICES.items():
            is_live = self.status[env_var]
            dot = "●" if is_live else "○"
            mode = "LIVE" if is_live else "SIMULATED"
            color = ColorLogger.GREEN if is_live else ColorLogger.YELLOW
            reset = ColorLogger.RESET
            print(f"  {label:<35} {color}{dot} {mode}{reset}")
        print(f"{border}\n")

    def is_live(self, env_var: str) -> bool:
        """Check if a specific service has a live API key."""
        return self.status.get(env_var, False)

    def get_key(self, env_var: str) -> str:
        """Retrieve the API key for a service (empty if simulated)."""
        return self.keys.get(env_var, "")


# ═══════════════════════════════════════════════════════════════════════════════
# B3: @graceful_fallback — Resilience decorator
# Ref: Sections 14.1.1–14.2.4 (wraps every agent tool)
# ═══════════════════════════════════════════════════════════════════════════════

def graceful_fallback(
    fallback_value: Any = None,
    section_ref: str = "Chapter 14",
    max_retries: int = 2,
    base_delay: float = 0.5,
):
    """Decorator that catches all exceptions, logs them in RED, and returns
    a structured fallback value. Supports exponential backoff for transient
    failures.

    Args:
        fallback_value: Value returned when all retries are exhausted.
        section_ref: Chapter section reference for log tracing.
        max_retries: Number of retry attempts before falling back.
        base_delay: Base delay in seconds for exponential backoff.

    Author: Imran Ahmad
    Ref: Chapter 14, Sections 14.1.1–14.2.4
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    if attempt < max_retries:
                        delay = base_delay * (2 ** attempt)
                        logger.warning(
                            f"[{section_ref}] {func.__name__} attempt "
                            f"{attempt + 1}/{max_retries + 1} failed: "
                            f"{type(exc).__name__}: {exc} — "
                            f"retrying in {delay:.1f}s"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"[{section_ref}] {func.__name__} failed after "
                            f"{max_retries + 1} attempts: "
                            f"{type(exc).__name__}: {exc} — "
                            f"returning fallback"
                        )
                        return fallback_value
        return wrapper
    return decorator


# ═══════════════════════════════════════════════════════════════════════════════
# B4: MockChatOpenAI — Keyword-based mock LLM (BaseChatModel subclass)
# Ref: Section 14.1 (supervisor routing, agent responses)
# ═══════════════════════════════════════════════════════════════════════════════

from typing import List, Optional as Opt

try:
    from langchain_core.language_models.chat_models import BaseChatModel
    from langchain_core.messages import AIMessage, BaseMessage as _BM
    from langchain_core.outputs import ChatResult, ChatGeneration
    _HAS_LANGCHAIN = True
except ImportError:
    _HAS_LANGCHAIN = False


def _classify_and_respond(query: str) -> str:
    """Classify query by keyword and return chapter-faithful response.

    Author: Imran Ahmad
    Ref: Chapter 14, Sections 14.1–14.2
    """
    q = query.lower()

    # Financial market data responses (Sec 14.1.1)
    if any(kw in q for kw in ["market data", "price", "stock", "aapl",
                                "msft", "googl", "ticker"]):
        return (
            "Market Data for AAPL: Price: $178.72, "
            "Market Cap: $2800000000000, P/E Ratio: 28.5, "
            "Day Range: $176.50-$179.80, Volume: 52340000. "
            "The stock shows stable trading within a narrow range."
        )

    # Risk assessment responses (Sec 14.1.2)
    if any(kw in q for kw in ["risk", "volatility", "var", "drawdown"]):
        return (
            "Risk Assessment: Composite risk score 4.85 (MODERATE). "
            "Annualized volatility: 0.2340, Max drawdown: -0.0812, "
            "VaR (95%): -0.0198. Position is within acceptable "
            "risk parameters for a moderate-tolerance client."
        )

    # Financial analysis responses (Sec 14.1.1)
    if any(kw in q for kw in ["analysis", "financials", "portfolio",
                                "metric", "ratio"]):
        return (
            "Portfolio Analysis for AAPL: P/E Ratio: 28.5, "
            "Revenue Growth: 7.8%, 52W High: $199.62, "
            "52W Low: $143.90. Fundamentals indicate stable growth "
            "with strong earnings momentum."
        )

    # News responses (Sec 14.1.1)
    if any(kw in q for kw in ["news", "sentiment", "headline",
                                "market outlook"]):
        return (
            "Financial News Summary: (1) Federal Reserve signals "
            "cautious approach to rate adjustments amid stable "
            "inflation data. (2) Technology sector continues strong "
            "Q4 earnings momentum. (3) Global markets respond "
            "positively to improved trade outlook."
        )

    # Legal issue extraction (Sec 14.2.2)
    if any(kw in q for kw in ["legal issue", "extract issue",
                                "decompose", "legal matter"]):
        return (
            "Identified Issues: 1) Standard of care in data "
            "protection (Regulatory Compliance, Priority 1). "
            "2) Elements of negligence in security breach "
            "(Tort Law, Priority 1). 3) Applicable statutory "
            "obligations under GDPR/CCPA (Privacy Law, Priority 2)."
        )

    # Legal analysis (Sec 14.2.1–14.2.4)
    if any(kw in q for kw in ["legal", "contract", "clause",
                                "precedent", "citation", "court",
                                "jurisdiction"]):
        return (
            "Legal Analysis: The matter involves established principles "
            "of contractual interpretation under common law. Key "
            "authorities include relevant Supreme Court holdings on "
            "duty of care and statutory obligations. Recommend "
            "focusing on binding precedent within the applicable "
            "jurisdiction before expanding to persuasive authority."
        )

    # Compliance / advisory (Sec 14.1.3)
    if any(kw in q for kw in ["compliance", "suitability",
                                "recommend", "invest", "allocat"]):
        return (
            "Advisory Recommendation: For a moderate-risk client "
            "with a 10-year horizon and $50,000 initial investment, "
            "the recommended allocation is: US Equities 45%, "
            "International Equities 20%, Fixed Income 25%, "
            "Alternatives 10%. This allocation has been validated "
            "against suitability and concentration limits."
        )

    # Default response
    return (
        f"[Simulation Mode] Processed query: '{query[:80]}...' — "
        f"Response generated using chapter-derived mock logic."
    )


if _HAS_LANGCHAIN:
    class MockChatOpenAI(BaseChatModel):
        """Mock LLM that returns chapter-faithful responses based on
        keyword classification of the input query.

        Extends BaseChatModel so it is fully compatible with LangGraph's
        create_react_agent, the pipe operator (|), bind_tools(), and
        with_structured_output().

        Author: Imran Ahmad
        Ref: Chapter 14, Section 14.1
        """

        model_name: str = "gpt-4o-mini-2024-07-18"

        class Config:
            arbitrary_types_allowed = True

        def __init__(self, model: str = "gpt-4o-mini-2024-07-18",
                     temperature: float = 0, **kwargs):
            super().__init__(model_name=model, **kwargs)
            # Use object.__setattr__ to bypass pydantic v1 field validation
            object.__setattr__(self, "_mock_call_count", 0)
            object.__setattr__(self, "_mock_bound_tools", [])
            logger.info(
                f"[Simulation Mode] MockChatOpenAI initialized "
                f"(model={model})"
            )

        @property
        def _llm_type(self) -> str:
            return "mock-chat-openai"

        def _generate(self, messages: List[_BM],
                      stop: Opt[List[str]] = None,
                      **kwargs) -> ChatResult:
            """Core generation method required by BaseChatModel."""
            query = ""
            if messages:
                query = messages[-1].content if hasattr(
                    messages[-1], "content"
                ) else str(messages[-1])

            self_count = getattr(self, "_mock_call_count", 0) + 1
            object.__setattr__(self, "_mock_call_count", self_count)

            # If tools are bound and odd call, emit a tool_call
            bound_tools = getattr(self, "_mock_bound_tools", [])
            if bound_tools and self_count % 2 == 1:
                tool = bound_tools[0]
                tool_name = getattr(tool, "name",
                                    getattr(tool, "__name__", "tool"))
                msg = AIMessage(
                    content="",
                    tool_calls=[{
                        "id": f"mock_call_{self_count}",
                        "name": tool_name,
                        "args": {"query": query},
                    }],
                )
            else:
                content = _classify_and_respond(query)
                msg = AIMessage(content=content)

            return ChatResult(generations=[ChatGeneration(message=msg)])

        def bind_tools(self, tools, **kwargs):
            """Bind tools to enable tool_calls in responses.
            Returns a new instance with tools bound.
            """
            clone = MockChatOpenAI(model=self.model_name)
            object.__setattr__(clone, "_mock_bound_tools",
                               list(tools) if tools else [])
            object.__setattr__(clone, "_mock_call_count", 0)
            return clone

        def with_structured_output(self, schema, **kwargs):
            """Return a Runnable that produces structured routing decisions.
            Ref: Section 14.1, supervisor_agent() on p.5
            """
            from langchain_core.runnables import RunnableLambda
            chain = MockStructuredChain(schema)
            return RunnableLambda(chain.invoke)

        def generate_text(self, prompt: str, **kwargs) -> str:
            """Simple text generation for non-agent use cases.
            Used by PrecedentFinder._extract_issues() (Sec 14.2.2).
            """
            return _classify_and_respond(prompt)

else:
    # Fallback if langchain is not installed
    class MockChatOpenAI:
        """Minimal mock LLM for environments without langchain.

        Author: Imran Ahmad
        Ref: Chapter 14, Section 14.1
        """

        def __init__(self, model: str = "gpt-4o-mini-2024-07-18",
                     temperature: float = 0, **kwargs):
            self.model_name = model
            self._mock_bound_tools = []
            self._mock_call_count = 0
            logger.info(
                f"[Simulation Mode] MockChatOpenAI initialized "
                f"(model={model})"
            )

        def invoke(self, input_data, **kwargs):
            query = str(input_data)
            return type("Msg", (), {
                "content": _classify_and_respond(query)
            })()

        def bind_tools(self, tools, **kwargs):
            return self

        def with_structured_output(self, schema, **kwargs):
            return MockStructuredChain(schema)

        def generate_text(self, prompt: str, **kwargs) -> str:
            return _classify_and_respond(prompt)


# ═══════════════════════════════════════════════════════════════════════════════
# B5: MockStructuredChain — Deterministic supervisor routing
# Ref: Section 14.1, supervisor routing (p.4-5)
# ═══════════════════════════════════════════════════════════════════════════════

class MockStructuredChain:
    """Deterministic routing chain for the supervisor agent.

    Cycles through the specialist agent sequence defined in the chapter:
    Market_Data_Agent → Financial_Analysis_Agent → News_Agent → FINISH.

    Uses a class-level step counter so routing progresses even when
    new instances are created by with_structured_output() calls.

    Author: Imran Ahmad
    Ref: Chapter 14, Section 14.1 (p.4-5)
    """

    ROUTING_SEQUENCE = [
        "Market_Data_Agent",
        "Financial_Analysis_Agent",
        "News_Agent",
        "FINISH",
    ]

    _global_step = 0

    def __init__(self, schema=None):
        self.schema = schema

    def invoke(self, input_data, **kwargs):
        """Return the next routing target in the deterministic sequence."""
        target = self.ROUTING_SEQUENCE[
            MockStructuredChain._global_step % len(self.ROUTING_SEQUENCE)
        ]
        MockStructuredChain._global_step += 1
        logger.info(f"[Supervisor] Routing to: {target}")

        # Return an instance of the schema if provided
        if self.schema is not None:
            try:
                return self.schema(next=target)
            except Exception:
                pass

        # Fallback: return a simple object with .next attribute
        return type("RouteResult", (), {"next": target})()

    @classmethod
    def reset(cls):
        """Reset the routing counter (useful for repeated demos)."""
        cls._global_step = 0


# ═══════════════════════════════════════════════════════════════════════════════
# B6: MockEmbeddingModel — Hash-based pseudo-embeddings
# Ref: Section 14.2.1 (legal knowledge base, p.20-22)
# ═══════════════════════════════════════════════════════════════════════════════

class MockEmbeddingModel:
    """Generates deterministic pseudo-embeddings using text hashing.

    Produces consistent embeddings for the same input text, enabling
    reproducible similarity comparisons without a real embedding model.

    Author: Imran Ahmad
    Ref: Chapter 14, Section 14.2.1 (p.20-22)
    """

    def __init__(self, dimension: int = 128):
        self.dimension = dimension

    def encode(self, text: str) -> list:
        """Generate a deterministic pseudo-embedding from text content."""
        text_bytes = text.encode("utf-8")
        hash_digest = hashlib.sha512(text_bytes).hexdigest()

        # Extend hash to cover the full dimension
        extended = hash_digest
        while len(extended) < self.dimension * 2:
            extended += hashlib.sha512(
                extended.encode("utf-8")
            ).hexdigest()

        # Convert hex pairs to floats in [-1, 1]
        embedding = []
        for i in range(self.dimension):
            hex_pair = extended[i * 2: i * 2 + 2]
            value = (int(hex_pair, 16) / 255.0) * 2 - 1
            embedding.append(round(value, 6))

        # Normalize to unit length
        norm = math.sqrt(sum(v * v for v in embedding))
        if norm > 0:
            embedding = [round(v / norm, 6) for v in embedding]

        return embedding


# ═══════════════════════════════════════════════════════════════════════════════
# B7: MockVectorStore — In-memory vector store with cosine similarity
# Ref: Section 14.2.1 (legal knowledge base, p.20-22)
# ═══════════════════════════════════════════════════════════════════════════════

class MockSearchResult:
    """Container for vector search results with metadata.

    Author: Imran Ahmad
    Ref: Chapter 14, Section 14.2.1
    """

    def __init__(self, id: str, embedding: list, metadata: dict,
                 similarity_score: float = 0.0):
        self.id = id
        self.embedding = embedding
        self.metadata = metadata
        self.similarity_score = similarity_score
        self.final_score = similarity_score


class MockVectorStore:
    """In-memory vector store with cosine similarity search and
    metadata filtering.

    Supports upsert(), query(), and verify_citation() operations
    needed by LegalKnowledgeBase and the citation verification gate.

    Author: Imran Ahmad
    Ref: Chapter 14, Section 14.2.1 (p.20-22)
    """

    def __init__(self):
        self._store = {}

    def upsert(self, id: str, embedding: list, metadata: dict):
        """Insert or update a document in the store."""
        self._store[id] = {
            "id": id,
            "embedding": embedding,
            "metadata": metadata,
        }
        logger.info(
            f"[VectorStore] Upserted document: {id} "
            f"({len(embedding)}-dim embedding)"
        )

    def query(self, embedding: list, filter: dict = None,
              top_k: int = 10) -> list:
        """Retrieve top-k results by cosine similarity with optional
        metadata filtering.

        Args:
            embedding: Query embedding vector.
            filter: Metadata filter dict. Supports exact match and
                    $gte operator for numeric fields.
            top_k: Maximum number of results to return.

        Returns:
            List of MockSearchResult objects sorted by similarity.
        """
        results = []
        for doc_id, doc in self._store.items():
            # Apply metadata filters
            if filter and not self._matches_filter(doc["metadata"], filter):
                continue

            score = self._cosine_similarity(embedding, doc["embedding"])
            results.append(MockSearchResult(
                id=doc_id,
                embedding=doc["embedding"],
                metadata=doc["metadata"],
                similarity_score=score,
            ))

        results.sort(key=lambda r: r.similarity_score, reverse=True)
        return results[:top_k]

    def verify_citation(self, citation_text: str,
                        jurisdiction: str = None,
                        check_precedential: bool = True,
                        check_good_law: bool = True) -> bool:
        """Verify a citation exists in the store and is valid.

        Used by the citation verification gate (Sec 14.2.4, p.31-32).

        Returns:
            True if the citation exists, is good law, and meets
            jurisdiction/precedential requirements.
        """
        for doc_id, doc in self._store.items():
            meta = doc["metadata"]
            citation = meta.get("citation", "")
            case_name = meta.get("case_name", "")

            # Match by citation string or case name substring
            if (citation_text in citation or
                    citation_text in case_name or
                    citation in citation_text):

                # Check precedential status
                if check_good_law and meta.get("status") != "good_law":
                    return False

                # Check jurisdiction match
                if jurisdiction and meta.get("jurisdiction") != jurisdiction:
                    continue

                # Check minimum authority
                if check_precedential and meta.get("authority_level", 0) < 1:
                    return False

                return True

        return False

    @staticmethod
    def _cosine_similarity(vec_a: list, vec_b: list) -> float:
        """Compute cosine similarity between two vectors."""
        if len(vec_a) != len(vec_b):
            return 0.0
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    @staticmethod
    def _matches_filter(metadata: dict, filter_dict: dict) -> bool:
        """Check if document metadata matches all filter criteria."""
        for key, condition in filter_dict.items():
            value = metadata.get(key)
            if isinstance(condition, dict):
                if "$gte" in condition:
                    if value is None or value < condition["$gte"]:
                        return False
            else:
                if value != condition:
                    return False
        return True

    def count(self) -> int:
        """Return the number of documents in the store."""
        return len(self._store)
