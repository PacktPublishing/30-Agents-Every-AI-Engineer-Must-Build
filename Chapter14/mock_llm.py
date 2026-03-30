# ─────────────────────────────────────────────────────────────────────────────
# mock_llm.py — Mocking & Resilience Layer
# Chapter 14: Financial and Legal Domain Agents
# Book: 30 Agents Every AI Engineer Must Build — Imran Ahmad (Packt Publishing)
#
# This module provides:
#   - ColorLogger:          Color-coded terminal logging (Blue/Green/Red/Yellow)
#   - ServiceConfig:        Per-service API key detection with getpass fallback
#   - @graceful_fallback:   Decorator that catches exceptions and returns fallback values
#   - MockChatOpenAI:       LangGraph-compatible mock LLM with keyword routing
#   - MockStructuredChain:  Deterministic supervisor routing sequence
#   - MockEmbeddingModel:   Hash-based pseudo-embeddings for vector store testing
#   - MockVectorStore:      In-memory vector store with cosine similarity search
#
# Author: Imran Ahmad
# ─────────────────────────────────────────────────────────────────────────────

import os
import sys
import hashlib
import functools
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass, field

import numpy as np
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


# ═══════════════════════════════════════════════════════════════════════════════
# B1: ColorLogger — Color-Coded Visual Logging
# Chapter Ref: Used across all sections (14.1.x, 14.2.x)
# ═══════════════════════════════════════════════════════════════════════════════

class ColorLogger:
    """Color-coded logger for agent execution tracing.

    Provides visual differentiation of log levels:
        - BLUE:   Informational messages (agent starts, data loading)
        - GREEN:  Success messages (tool completion, validation pass)
        - RED:    Handled errors (caught by @graceful_fallback)
        - YELLOW: Warnings (fallback activated, simulated mode)

    No external dependencies — uses ANSI escape codes only.

    Author: Imran Ahmad
    """

    # ANSI color codes
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    def __init__(self, name: str = "Chapter14"):
        self.name = name
        # Enable ANSI on Windows cmd if applicable
        if sys.platform == "win32":
            os.system("")

    def _timestamp(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def _log(self, color: str, level: str, message: str) -> None:
        ts = self._timestamp()
        prefix = f"{color}{self.BOLD}[{ts}] [{self.name}] {level}{self.RESET}"
        print(f"{prefix} {color}{message}{self.RESET}")

    def info(self, message: str) -> None:
        """Blue — informational messages."""
        self._log(self.BLUE, "INFO", message)

    def success(self, message: str) -> None:
        """Green — success and completion messages."""
        self._log(self.GREEN, "SUCCESS", message)

    def error(self, message: str) -> None:
        """Red — handled errors (caught exceptions)."""
        self._log(self.RED, "ERROR", message)

    def warning(self, message: str) -> None:
        """Yellow — warnings and fallback activations."""
        self._log(self.YELLOW, "WARNING", message)


# Module-level logger instance
logger = ColorLogger("Chapter14")


# ═══════════════════════════════════════════════════════════════════════════════
# B2: ServiceConfig — Per-Service API Key Detection
# Chapter Ref: Technical Requirements (p.2), Simulation Mode Decision Flow
# ═══════════════════════════════════════════════════════════════════════════════

class ServiceConfig:
    """Detects API key availability per service and prints a status dashboard.

    For each service (OpenAI, Finnhub, Tavily):
      1. Check os.getenv() for the key
      2. If not found, prompt via getpass (user can press Enter to skip)
      3. Record status as LIVE or SIMULATED

    The dashboard is printed once at instantiation time.

    Author: Imran Ahmad
    Chapter Ref: Technical Requirements (p.2)
    """

    SERVICES = {
        "OPENAI_API_KEY":  "OpenAI (LLM)",
        "FINNHUB_API_KEY": "Finnhub (Financial Data)",
        "TAVILY_API_KEY":  "Tavily (News Search)",
    }

    def __init__(self, interactive: bool = True):
        """Initialize service configuration.

        Args:
            interactive: If True, prompt for missing keys via getpass.
                         If False (e.g., CI/CD), skip prompts and default to SIMULATED.
        """
        self.status: Dict[str, str] = {}
        self.keys: Dict[str, Optional[str]] = {}

        for env_var, display_name in self.SERVICES.items():
            key = os.getenv(env_var, "")

            if key:
                self.status[env_var] = "LIVE"
                self.keys[env_var] = key
            elif interactive and self._is_interactive():
                key = self._safe_getpass(env_var, display_name)
                if key:
                    os.environ[env_var] = key
                    self.status[env_var] = "LIVE"
                    self.keys[env_var] = key
                else:
                    self.status[env_var] = "SIMULATED"
                    self.keys[env_var] = None
            else:
                self.status[env_var] = "SIMULATED"
                self.keys[env_var] = None

        self._print_dashboard()

    def _is_interactive(self) -> bool:
        """Check if running in an interactive environment."""
        try:
            return sys.stdin.isatty() or "ipykernel" in sys.modules
        except Exception:
            return False

    def _safe_getpass(self, env_var: str, display_name: str) -> str:
        """Prompt for a key, handling both terminal and Jupyter contexts."""
        try:
            import getpass
            key = getpass.getpass(
                f"  Enter {display_name} key (or press Enter for Simulation Mode): "
            )
            return key.strip()
        except Exception:
            return ""

    def _print_dashboard(self) -> None:
        """Print the color-coded service status dashboard."""
        line = "═" * 56
        print(f"\n{ColorLogger.BOLD}{line}")
        print("  CHAPTER 14 — SERVICE STATUS DASHBOARD")
        print("  Book: 30 Agents Every AI Engineer Must Build")
        print("  Author: Imran Ahmad")
        print(f"{line}{ColorLogger.RESET}")

        for env_var, display_name in self.SERVICES.items():
            status = self.status[env_var]
            if status == "LIVE":
                color = ColorLogger.GREEN
                symbol = "●"
            else:
                color = ColorLogger.YELLOW
                symbol = "○"
            padding = " " * (32 - len(display_name))
            print(f"  {display_name}{padding}{color}{symbol} {status}{ColorLogger.RESET}")

        print(f"{ColorLogger.BOLD}{line}{ColorLogger.RESET}\n")

    def is_live(self, env_var: str) -> bool:
        """Check if a specific service is in LIVE mode."""
        return self.status.get(env_var) == "LIVE"

    def get_key(self, env_var: str) -> Optional[str]:
        """Retrieve the API key for a service, or None if SIMULATED."""
        return self.keys.get(env_var)


# ═══════════════════════════════════════════════════════════════════════════════
# B3: @graceful_fallback — Defensive Execution Decorator
# Chapter Ref: Sections 14.1.1 through 14.2.4
# ═══════════════════════════════════════════════════════════════════════════════

def graceful_fallback(
    fallback_value: Any = None,
    section_ref: str = "",
    log_traceback: bool = False,
):
    """Decorator that wraps a callable with exception handling.

    When the decorated function raises any exception:
      1. The exception is caught (notebook never crashes)
      2. A RED log message is printed with the section reference
      3. The fallback_value is returned instead

    Args:
        fallback_value: Value to return on failure. Can be any type.
        section_ref:    Chapter section reference (e.g., "Sec 14.1.1") for traceability.
        log_traceback:  If True, print the full traceback (useful for debugging).

    Usage:
        @graceful_fallback(fallback_value={}, section_ref="Sec 14.1.1")
        def get_market_data(symbol):
            ...

    Author: Imran Ahmad
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                ref = f" [{section_ref}]" if section_ref else ""
                logger.error(
                    f"@graceful_fallback caught exception in "
                    f"{func.__name__}(){ref}: {type(e).__name__}: {e}"
                )
                if log_traceback:
                    logger.error(traceback.format_exc())
                logger.warning(
                    f"Returning fallback value for {func.__name__}(){ref}"
                )
                return fallback_value
        return wrapper
    return decorator


# ═══════════════════════════════════════════════════════════════════════════════
# B4: MockChatOpenAI — LangGraph-Compatible Mock LLM
# Chapter Ref: Section 14.1 (supervisor routing), 14.2.x (legal analysis)
# ═══════════════════════════════════════════════════════════════════════════════

class MockChatOpenAI:
    """Mock LLM that returns chapter-faithful responses via keyword classification.

    Designed to be a drop-in replacement for ChatOpenAI in LangGraph pipelines.
    Returns AIMessage objects with properly formatted tool_calls when tools are
    bound, making it compatible with create_react_agent.

    Keyword routing logic:
        - "market" / "stock" / "price"  → financial market data response
        - "risk" / "var" / "volatility" → risk assessment response
        - "legal" / "case" / "court"    → legal research response
        - "contract" / "clause"         → contract analysis response
        - "compliance" / "validate"     → compliance check response
        - "news" / "headline"           → financial news response
        - default                       → generic analytical response

    Supports:
        - .invoke(messages) → AIMessage
        - .bind_tools(tools) → self (for create_react_agent compatibility)
        - .with_structured_output(schema) → MockStructuredChain
        - .generate(messages_list) → LLMResult-like

    Author: Imran Ahmad
    Chapter Ref: Section 14.1 (supervisor routing)
    """

    def __init__(self, model: str = "mock-gpt-4o-mini", temperature: float = 0, **kwargs):
        self.model = model
        self.temperature = temperature
        self.bound_tools: List[Any] = []
        self._call_count = 0

    def bind_tools(self, tools: List[Any]) -> "MockChatOpenAI":
        """Bind tools for create_react_agent compatibility."""
        self.bound_tools = tools
        return self

    def invoke(self, messages: Union[List, str, Any], **kwargs) -> AIMessage:
        """Generate a mock response based on keyword classification.

        If tools are bound and the query matches a tool, returns an AIMessage
        with tool_calls. Otherwise returns a plain text AIMessage.
        """
        self._call_count += 1
        query = self._extract_query(messages)
        query_lower = query.lower()

        # If tools are bound, check if we should invoke one
        if self.bound_tools and self._call_count <= len(self.bound_tools):
            tool = self._match_tool(query_lower)
            if tool:
                return AIMessage(
                    content="",
                    tool_calls=[{
                        "id": f"call_mock_{self._call_count}",
                        "name": tool.name if hasattr(tool, "name") else str(tool),
                        "args": self._generate_tool_args(tool, query_lower),
                    }],
                )

        # Text-only response via keyword routing
        response_text = self._route_response(query_lower)
        return AIMessage(content=response_text)

    def with_structured_output(self, schema: Any, **kwargs) -> "MockStructuredChain":
        """Return a MockStructuredChain for structured output routing."""
        return MockStructuredChain(schema=schema)

    def generate(self, messages_list: List[List], **kwargs) -> Any:
        """Batch generation — returns a simple result structure."""
        results = []
        for messages in messages_list:
            msg = self.invoke(messages)
            results.append(msg)
        return _MockLLMResult(generations=[[_MockGeneration(text=r.content)] for r in results])

    def _extract_query(self, messages: Any) -> str:
        """Extract the text query from various message formats."""
        if isinstance(messages, str):
            return messages
        if isinstance(messages, list):
            for msg in reversed(messages):
                if isinstance(msg, HumanMessage):
                    return msg.content
                if isinstance(msg, dict) and msg.get("role") == "user":
                    return msg.get("content", "")
                if isinstance(msg, (SystemMessage, AIMessage)):
                    continue
            # Fallback: concatenate all string-like content
            parts = []
            for msg in messages:
                if isinstance(msg, str):
                    parts.append(msg)
                elif hasattr(msg, "content"):
                    parts.append(msg.content)
            return " ".join(parts)
        if hasattr(messages, "content"):
            return messages.content
        return str(messages)

    def _match_tool(self, query_lower: str) -> Optional[Any]:
        """Match query keywords to a bound tool."""
        for tool in self.bound_tools:
            tool_name = tool.name if hasattr(tool, "name") else str(tool)
            tool_name_lower = tool_name.lower()
            # Match tool name keywords against query
            if any(kw in query_lower for kw in tool_name_lower.split("_")):
                return tool
        # Default: return first tool if available
        return self.bound_tools[0] if self.bound_tools else None

    def _generate_tool_args(self, tool: Any, query_lower: str) -> Dict:
        """Generate plausible tool arguments based on tool schema."""
        if hasattr(tool, "args_schema") and tool.args_schema:
            schema_fields = tool.args_schema.model_fields if hasattr(
                tool.args_schema, "model_fields"
            ) else {}
            args = {}
            for field_name, field_info in schema_fields.items():
                if "symbol" in field_name.lower():
                    args[field_name] = "AAPL"
                elif "query" in field_name.lower():
                    args[field_name] = query_lower[:100]
                else:
                    args[field_name] = ""
            return args
        return {"query": query_lower[:100]}

    def _route_response(self, query_lower: str) -> str:
        """Route to chapter-faithful mock responses based on keywords."""

        if any(kw in query_lower for kw in ["market", "stock", "price", "ticker"]):
            return (
                "Based on current market analysis (Sec 14.1.1): "
                "AAPL is trading at $178.72 with a P/E ratio of 28.5 and market cap "
                "of $2.8T. MSFT is at $338.11 with P/E of 32.1 and market cap of $2.5T. "
                "Both show stable fundamentals with moderate growth indicators. "
                "The technology sector continues to demonstrate resilience despite "
                "broader market volatility. Volume patterns suggest institutional "
                "accumulation in large-cap tech names."
            )

        if any(kw in query_lower for kw in ["risk", "var", "volatility", "cvar"]):
            return (
                "Risk Assessment Summary (Sec 14.1.2): "
                "Portfolio VaR (95%): -2.34% daily. CVaR (95%): -3.12% daily. "
                "Annualized volatility: 18.7%. Maximum drawdown over 90 days: -8.2%. "
                "The portfolio risk score is 5.8/10 (Moderate). "
                "Recommendation: Current allocation is within acceptable risk bounds "
                "for a moderate-growth investor profile. Consider rebalancing if "
                "volatility exceeds 25% annualized."
            )

        if any(kw in query_lower for kw in ["legal", "case", "court", "precedent", "jurisdiction"]):
            return (
                "Legal Research Summary (Sec 14.2.1-14.2.2): "
                "Found 4 relevant precedents in the knowledge base. "
                "Highest authority: Supreme Court ruling in SEC v. Capital Growth "
                "(authority level 10). Supporting circuit court decisions provide "
                "consistent interpretation of fiduciary duty standards. "
                "Note: All citations verified against the knowledge base. "
                "One potential hallucinated citation (Varghese v. Tech Corp) was "
                "flagged and excluded per verification protocol."
            )

        if any(kw in query_lower for kw in ["contract", "clause", "indemnif", "liability"]):
            return (
                "Contract Analysis Summary (Sec 14.2.3): "
                "Analyzed 8 contract clauses. Risk findings: "
                "HIGH — Indemnification clause (Section 4) contains unlimited liability exposure. "
                "HIGH — Liability cap (Section 5) is set below industry standard thresholds. "
                "CRITICAL — No GDPR data processing addendum found. "
                "MEDIUM — Termination clause lacks mutual termination rights. "
                "Recommendation: Negotiate liability cap increase and add GDPR addendum "
                "before execution."
            )

        if any(kw in query_lower for kw in ["compliance", "validate", "compliant"]):
            return (
                "Compliance Validation (Sec 14.1.3): "
                "Checking advisory plan against regulatory requirements... "
                "Suitability check: PASS — Risk level matches client tolerance. "
                "Concentration check: PASS — No single position exceeds 40%. "
                "Disclosure check: PASS — All required disclaimers present. "
                "Overall compliance status: APPROVED. "
                "Plan may proceed to client delivery."
            )

        if any(kw in query_lower for kw in ["news", "headline", "sentiment"]):
            return (
                "Financial News Summary (Sec 14.1.1): "
                "Top 5 relevant headlines: "
                "1. Federal Reserve signals steady rates through Q2 (Reuters). "
                "2. Tech earnings season shows mixed results with AI spending focus (Bloomberg). "
                "3. S&P 500 reaches new highs amid strong employment data (CNBC). "
                "4. Global supply chain improvements reduce inflation concerns (WSJ). "
                "5. Semiconductor sector rallies on increased data center demand (FT). "
                "Overall sentiment: Moderately bullish with cautious optimism."
            )

        if any(kw in query_lower for kw in ["allocat", "portfolio", "invest", "plan"]):
            return (
                "Investment Plan (Sec 14.1.3-14.1.4): "
                "Recommended allocation for moderate growth, 10-year horizon: "
                "US Equities: 45% — Diversified large-cap growth and value mix. "
                "International Equities: 20% — Developed markets with emerging market tilt. "
                "Fixed Income: 25% — Investment-grade corporate and government bonds. "
                "Alternatives: 10% — REITs and commodity exposure for inflation hedge. "
                "Expected annual return: 7.2%. Expected volatility: 12.4%."
            )

        # Default analytical response
        return (
            "Analysis complete (Chapter 14 — Financial and Legal Domain Agents). "
            "The multi-agent system has processed the request through the supervisor "
            "architecture. All agent nodes executed successfully with results aggregated "
            "at the supervisor level. For detailed methodology, refer to the relevant "
            "chapter section in '30 Agents Every AI Engineer Must Build' by Imran Ahmad."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# B5: MockStructuredChain — Deterministic Supervisor Routing
# Chapter Ref: Section 14.1, Fig 14.1 (supervisor pattern)
# ═══════════════════════════════════════════════════════════════════════════════

class MockStructuredChain:
    """Deterministic routing for the supervisor agent.

    Returns a fixed sequence of routing decisions:
        Call 1: "market_data_agent"
        Call 2: "analysis_agent"
        Call 3: "news_agent"
        Call 4+: "FINISH"

    This mirrors the supervisor architecture in Fig 14.1 where the supervisor
    orchestrates agents in a logical sequence.

    Author: Imran Ahmad
    Chapter Ref: Section 14.1, Fig 14.1
    """

    ROUTE_SEQUENCE = ["market_data_agent", "analysis_agent", "news_agent", "FINISH"]

    def __init__(self, schema: Any = None):
        self.schema = schema
        self._call_index = 0

    def invoke(self, messages: Any, **kwargs) -> Any:
        """Return the next routing decision in the sequence."""
        route = self.ROUTE_SEQUENCE[
            min(self._call_index, len(self.ROUTE_SEQUENCE) - 1)
        ]
        self._call_index += 1

        # If schema is provided, try to instantiate it with the route
        if self.schema:
            try:
                return self.schema(next=route)
            except Exception:
                pass

        return _MockRouteResponse(next=route)

    def reset(self) -> None:
        """Reset the routing sequence (useful for re-running demos)."""
        self._call_index = 0


@dataclass
class _MockRouteResponse:
    """Fallback route response when no Pydantic schema is provided."""
    next: str = "FINISH"


# ═══════════════════════════════════════════════════════════════════════════════
# B6: MockEmbeddingModel — Deterministic Hash-Based Embeddings
# Chapter Ref: Section 14.2.1 (legal knowledge base)
# ═══════════════════════════════════════════════════════════════════════════════

class MockEmbeddingModel:
    """Produces deterministic pseudo-embeddings from text via hashing.

    Uses SHA-256 to generate reproducible float vectors from input text.
    Same input always produces the same embedding, enabling consistent
    similarity search results across runs.

    Author: Imran Ahmad
    Chapter Ref: Section 14.2.1
    """

    def __init__(self, dimension: int = 384):
        """Initialize with embedding dimension.

        Args:
            dimension: Output vector dimension (default 384 for MiniLM compatibility).
        """
        self.dimension = dimension

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        return [self._hash_embed(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string."""
        return self._hash_embed(text)

    def _hash_embed(self, text: str) -> List[float]:
        """Generate a deterministic embedding from text using SHA-256 expansion.

        Process:
          1. Hash the input text with SHA-256
          2. Use the hash as a seed for numpy random
          3. Generate a unit-normalized float vector of the configured dimension
        """
        hash_bytes = hashlib.sha256(text.encode("utf-8")).digest()
        seed = int.from_bytes(hash_bytes[:4], "big")
        rng = np.random.RandomState(seed)
        vector = rng.randn(self.dimension).astype(float)
        # L2 normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector.tolist()


# ═══════════════════════════════════════════════════════════════════════════════
# B7: MockVectorStore — In-Memory Vector Store with Cosine Similarity
# Chapter Ref: Section 14.2.1 (legal knowledge base, hybrid retrieval)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class MockSearchResult:
    """A single search result from MockVectorStore.

    Attributes:
        id:       Document identifier
        text:     Original document text
        metadata: Associated metadata (court, jurisdiction, authority_level, etc.)
        score:    Cosine similarity score (0 to 1)
    """
    id: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    score: float = 0.0


class MockVectorStore:
    """In-memory vector store with cosine similarity search and metadata filtering.

    Provides the core operations needed for the legal knowledge base:
      - upsert(): Add or update documents with embeddings and metadata
      - query():  Find similar documents with optional metadata filters
      - delete(): Remove documents by ID
      - count():  Return the number of stored documents

    Uses MockEmbeddingModel for automatic text-to-vector conversion.

    Author: Imran Ahmad
    Chapter Ref: Section 14.2.1
    """

    def __init__(self, embedding_model: Optional[MockEmbeddingModel] = None):
        self.embedding_model = embedding_model or MockEmbeddingModel()
        self._store: Dict[str, Dict[str, Any]] = {}

    def upsert(
        self,
        doc_id: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ) -> None:
        """Add or update a document in the store.

        Args:
            doc_id:    Unique document identifier
            text:      Document text
            metadata:  Optional metadata dictionary
            embedding: Pre-computed embedding (if None, auto-computed from text)
        """
        if embedding is None:
            embedding = self.embedding_model.embed_query(text)

        self._store[doc_id] = {
            "text": text,
            "metadata": metadata or {},
            "embedding": embedding,
        }
        logger.info(f"MockVectorStore: Upserted document '{doc_id}'")

    def query(
        self,
        query_text: str,
        top_k: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[MockSearchResult]:
        """Search for similar documents using cosine similarity.

        Args:
            query_text:      Search query text
            top_k:           Maximum number of results to return
            metadata_filter: Optional dict of metadata key-value pairs to filter by

        Returns:
            List of MockSearchResult ordered by descending similarity score.
        """
        if not self._store:
            return []

        query_embedding = np.array(self.embedding_model.embed_query(query_text))
        results = []

        for doc_id, doc in self._store.items():
            # Apply metadata filter
            if metadata_filter:
                skip = False
                for key, value in metadata_filter.items():
                    if doc["metadata"].get(key) != value:
                        skip = True
                        break
                if skip:
                    continue

            # Compute cosine similarity
            doc_embedding = np.array(doc["embedding"])
            dot_product = np.dot(query_embedding, doc_embedding)
            norm_product = np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)

            if norm_product > 0:
                score = float(dot_product / norm_product)
            else:
                score = 0.0

            results.append(MockSearchResult(
                id=doc_id,
                text=doc["text"],
                metadata=doc["metadata"],
                score=score,
            ))

        # Sort by score descending and return top_k
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]

    def delete(self, doc_id: str) -> bool:
        """Remove a document by ID. Returns True if found and deleted."""
        if doc_id in self._store:
            del self._store[doc_id]
            return True
        return False

    def count(self) -> int:
        """Return the number of documents in the store."""
        return len(self._store)

    def list_ids(self) -> List[str]:
        """Return all document IDs in the store."""
        return list(self._store.keys())


# ═══════════════════════════════════════════════════════════════════════════════
# Internal Helper Classes
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class _MockGeneration:
    """Mimics LangChain's Generation object for .generate() compatibility."""
    text: str = ""


@dataclass
class _MockLLMResult:
    """Mimics LangChain's LLMResult object for .generate() compatibility."""
    generations: List[List[_MockGeneration]] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════════
# Module Exports
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "ColorLogger",
    "ServiceConfig",
    "graceful_fallback",
    "MockChatOpenAI",
    "MockStructuredChain",
    "MockEmbeddingModel",
    "MockVectorStore",
    "MockSearchResult",
    "logger",
]
