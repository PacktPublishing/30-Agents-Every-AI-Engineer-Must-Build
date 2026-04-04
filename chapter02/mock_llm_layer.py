"""
mock_llm_layer.py — Simulation & Resilience Infrastructure
============================================================
Chapter 2: The Agent Engineer's Toolkit
Book: "Agents" by Imran Ahmad (Packt, 2025)

This module provides a complete simulation layer that enables the
companion notebook to run end-to-end without any live API key.
When an API key is detected, the module supports transparent
switching to live mode.

Components:
    - AgentLogger: Color-coded console logging (Blue/Green/Red/Yellow)
    - fail_gracefully: Decorator for defensive tool/LLM invocation
    - detect_mode: Environment detection (dotenv -> getpass -> simulation)
    - MockLLM: Deterministic, chapter-derived response engine
    - MockToolkit: Mock implementations of all chapter tool demos
    - MockMemory: Simulated conversation memory (buffer and summary)

Author: Imran Ahmad
"""

import os
import functools
import json
from typing import Any, Optional, Tuple, List, Dict

__all__ = [
    "AgentLogger",
    "fail_gracefully",
    "detect_mode",
    "MockLLM",
    "MockToolkit",
    "MockMemory",
]


# ---------------------------------------------------------------------------
# 1. Color-Coded Logging
# ---------------------------------------------------------------------------

class AgentLogger:
    """Color-coded logger for agent execution tracing.

    Provides four log levels with distinct ANSI colors for clear
    visual separation in Jupyter notebooks and terminals.

    Author: Imran Ahmad — Chapter 2, The Agent Engineer's Toolkit
    """

    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    @staticmethod
    def info(msg: str) -> None:
        """Log informational messages (Blue). Agent init, step entry."""
        print(f"{AgentLogger.BLUE}[INFO]{AgentLogger.RESET} {msg}")

    @staticmethod
    def success(msg: str) -> None:
        """Log successful completions (Green). Valid tool returns."""
        print(f"{AgentLogger.GREEN}[SUCCESS]{AgentLogger.RESET} {msg}")

    @staticmethod
    def error(msg: str) -> None:
        """Log handled errors (Red). Caught exceptions, fallbacks."""
        print(f"{AgentLogger.RED}[HANDLED ERROR]{AgentLogger.RESET} {msg}")

    @staticmethod
    def simulation(msg: str) -> None:
        """Log simulation mode activity (Yellow). Mock data served."""
        print(f"{AgentLogger.YELLOW}[SIMULATION]{AgentLogger.RESET} {msg}")

    @staticmethod
    def banner(mode: str) -> None:
        """Print a startup banner showing the active mode."""
        if mode == "simulation":
            print(
                f"\n{AgentLogger.BOLD}{AgentLogger.YELLOW}"
                f"{'=' * 60}\n"
                f"  SIMULATION MODE ACTIVE\n"
                f"  No API key detected. All outputs are deterministic mocks\n"
                f"  derived from Chapter 2 content.\n"
                f"  To switch to live mode: cp .env.template .env\n"
                f"{'=' * 60}"
                f"{AgentLogger.RESET}\n"
            )
        else:
            print(
                f"\n{AgentLogger.BOLD}{AgentLogger.GREEN}"
                f"{'=' * 60}\n"
                f"  LIVE MODE ACTIVE\n"
                f"  API key detected. Calls will use real LLM endpoints.\n"
                f"{'=' * 60}"
                f"{AgentLogger.RESET}\n"
            )


# ---------------------------------------------------------------------------
# 2. Fail-Gracefully Decorator
# ---------------------------------------------------------------------------

def fail_gracefully(
    section_ref: str = "Unknown Section",
    fallback_value: Any = None,
):
    """Decorator that wraps any function in defensive error handling.

    On success: logs in green and returns the real result.
    On failure: logs the error in red and returns a graceful fallback,
    ensuring the notebook never terminates from an uncaught exception.

    Args:
        section_ref: Chapter section reference (e.g., "LangChain Agent, p.4-5")
        fallback_value: Value to return on failure. If None, returns a
                        formatted simulation fallback string.

    Author: Imran Ahmad
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            AgentLogger.info(f"Executing: {func.__name__} ({section_ref})")
            try:
                result = func(*args, **kwargs)
                AgentLogger.success(f"{func.__name__} completed successfully.")
                return result
            except Exception as e:
                AgentLogger.error(
                    f"{func.__name__} failed: {type(e).__name__}: {e}. "
                    f"Falling back to mock for {section_ref}."
                )
                if fallback_value is not None:
                    return fallback_value
                return (
                    f"[SIMULATION] Graceful fallback for {section_ref}. "
                    f"In live mode, this would return real data."
                )
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# 3. Environment Detection
# ---------------------------------------------------------------------------

def detect_mode() -> Tuple[str, Optional[str]]:
    """Detect whether to run in live or simulation mode.

    Resolution order:
        1. Load .env file via python-dotenv
        2. Check os.getenv("OPENAI_API_KEY")
        3. Prompt via getpass (Enter to skip → simulation)

    Returns:
        Tuple of (mode, api_key) where mode is "live" or "simulation"
        and api_key is the key string or None.

    Author: Imran Ahmad
    """
    # Step 1: Try dotenv
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        AgentLogger.info(
            "python-dotenv not installed. Skipping .env file loading. "
            "Install with: pip install python-dotenv"
        )

    # Step 2: Check environment
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key.strip():
        AgentLogger.info("API key found in environment.")
        return "live", api_key.strip()

    # Step 3: Interactive fallback
    try:
        import getpass
        key = getpass.getpass(
            "Enter OpenAI API key (or press Enter for Simulation Mode): "
        )
        if key.strip():
            os.environ["OPENAI_API_KEY"] = key.strip()
            AgentLogger.info("API key provided via interactive prompt.")
            return "live", key.strip()
    except (EOFError, KeyboardInterrupt, Exception):
        # Catches EOFError, KeyboardInterrupt, and Jupyter's
        # StdinNotImplementedError in non-interactive environments.
        pass

    # Default: Simulation
    AgentLogger.simulation("No API key detected. Entering Simulation Mode.")
    return "simulation", None


# ---------------------------------------------------------------------------
# 4. MockLLM — Deterministic Response Engine
# ---------------------------------------------------------------------------

class MockLLM:
    """Deterministic mock LLM that returns chapter-derived responses.

    Matches input queries against a keyword registry to return
    contextually appropriate mock data from Chapter 2 of "Agents"
    by Imran Ahmad.

    Usage:
        llm = MockLLM()
        result = llm.invoke("What is the square root of 144?")

    Author: Imran Ahmad — Chapter 2, The Agent Engineer's Toolkit
    """

    def __init__(self):
        self._registry = self._build_registry()

    def _build_registry(self) -> Dict[str, Dict[str, Any]]:
        """Build the keyword-to-response mapping from chapter content."""
        return {

            # --- LangChain Agent Demo (p.4-5) ---
            "square root": {
                "section": "LangChain, p.4-5",
                "thought_process": [
                    {
                        "step": "Thought",
                        "content": (
                            "I need to calculate the square root of 144 "
                            "and then search for recent news about that number."
                        ),
                    },
                    {
                        "step": "Action",
                        "tool": "Calculator",
                        "input": "sqrt(144)",
                        "output": "12",
                    },
                    {
                        "step": "Action",
                        "tool": "WebSearch",
                        "input": "recent news about number 12",
                        "output": (
                            "The number 12 holds significance across many domains: "
                            "there are 12 months in a year, 12 zodiac signs, and "
                            "jersey number 12 is retired by several major sports teams."
                        ),
                    },
                    {
                        "step": "Final Answer",
                        "content": (
                            "The square root of 144 is 12. In recent news, "
                            "the number 12 appears across sports (retired jerseys), "
                            "astronomy (zodiac signs), and timekeeping (months)."
                        ),
                    },
                ],
                "final_answer": (
                    "The square root of 144 is 12. In recent news, "
                    "the number 12 appears across sports (retired jerseys), "
                    "astronomy (zodiac signs), and timekeeping (months)."
                ),
            },

            # --- LangGraph Workflow (p.7-8) ---
            "quantum computing": {
                "section": "LangGraph, p.7-8",
                "nodes": {
                    "research": (
                        "Recent breakthroughs in quantum computing include "
                        "advances in error correction codes, development of "
                        "processors exceeding 1,000 qubits, and early "
                        "demonstrations of quantum advantage in materials "
                        "simulation and cryptographic applications."
                    ),
                    "analyze": (
                        "Analysis of the research data reveals three primary "
                        "trajectories: (1) Error correction is maturing from "
                        "theoretical to practical implementations, (2) Qubit "
                        "counts are scaling rapidly, and (3) Real-world "
                        "applications in drug discovery and optimization "
                        "problems are emerging."
                    ),
                    "decide": "sufficient",
                    "respond": (
                        "Based on research and analysis: Quantum computing "
                        "is advancing rapidly. Error correction, qubit scaling, "
                        "and practical applications in drug discovery and "
                        "cryptography are the three leading fronts of progress."
                    ),
                },
            },

            # --- Hybrid Model Routing — Factual (p.15) ---
            "factual": {
                "section": "Hybrid model architecture, p.15",
                "model_used": "Mistral-7B (fast, cost-effective)",
                "response": (
                    "[SIMULATION][Mistral-7B] The capital of France is Paris. "
                    "It has served as the nation's capital since the late 10th "
                    "century under King Hugh Capet. Paris is also the seat of "
                    "the French government and the country's economic center."
                ),
            },

            # --- Hybrid Model Routing — Creative (p.15) ---
            "creative": {
                "section": "Hybrid model architecture, p.15",
                "model_used": "Claude (superior creative capabilities)",
                "response": (
                    "[SIMULATION][Claude] In the garden of silicon dreams, "
                    "where circuits bloom like luminous flowers and data "
                    "streams cascade through corridors of light, the agents "
                    "awaken — each one a spark of purpose in an infinite "
                    "lattice of possibility."
                ),
            },

            # --- Hybrid Model Routing — Analytical (p.15) ---
            "analytical": {
                "section": "Hybrid model architecture, p.15",
                "model_used": "GPT-4o (strong reasoning)",
                "response": (
                    "[SIMULATION][GPT-4o] Market analysis indicates a 23% "
                    "year-over-year revenue increase, driven by three primary "
                    "factors: (1) geographic market expansion into APAC (+31%), "
                    "(2) operational efficiency gains from automated workflows "
                    "(-15% cost), and (3) strategic acquisitions adding $12M "
                    "in recurring revenue."
                ),
            },

            # --- Tool Integration: Stock Price (p.22) ---
            "stock": {
                "section": "Tool integration — LangChain Tool, p.22",
                "tool_name": "StockPriceTool",
                "ticker": "AAPL",
                "price": "$187.42",
                "response": (
                    "[SIMULATION] The price of AAPL is $187.42. "
                    "This is a mock response from the StockPriceTool "
                    "demonstrating the LangChain Tool abstraction pattern."
                ),
            },

            # --- Tool Integration: Weather / Function Calling (p.23) ---
            "weather": {
                "section": "Tool integration — OpenAI Function Calling, p.23",
                "function_call": {
                    "name": "get_weather",
                    "arguments": json.dumps({"city": "Toronto"}),
                },
                "function_result": {
                    "temperature": "18°C",
                    "condition": "Partly cloudy",
                    "humidity": "62%",
                    "wind": "12 km/h NW",
                },
                "response": (
                    "[SIMULATION] Weather for Toronto: 18°C, Partly cloudy, "
                    "62% humidity, wind 12 km/h NW."
                ),
            },

            # --- RAG Pipeline (p.16-21) ---
            "rag": {
                "section": "Vector DB & RAG, p.16-21",
                "chunks_retrieved": 3,
                "chunks": [
                    {
                        "text": (
                            "Vector databases represent meaning as direction "
                            "in space. When you search a vector database, your "
                            "question becomes a vector pointing in a specific "
                            "direction in high-dimensional space."
                        ),
                        "similarity_score": 0.92,
                        "source": "Chapter 2, p.17",
                    },
                    {
                        "text": (
                            "Approximate nearest neighbor algorithms such as "
                            "HNSW and IVF make searching billions of high-"
                            "dimensional vectors possible in milliseconds."
                        ),
                        "similarity_score": 0.87,
                        "source": "Chapter 2, p.17",
                    },
                    {
                        "text": (
                            "A simple but powerful RAG pipeline: chunk your "
                            "knowledge, embed everything, store with metadata, "
                            "retrieve on demand, inject into prompts."
                        ),
                        "similarity_score": 0.81,
                        "source": "Chapter 2, p.19",
                    },
                ],
                "synthesized_answer": (
                    "[SIMULATION] Vector databases enable semantic search by "
                    "representing meaning as direction in high-dimensional "
                    "space. Using ANN algorithms like HNSW, they search "
                    "billions of vectors in milliseconds. The RAG pipeline "
                    "chains chunking, embedding, storage, retrieval, and "
                    "prompt injection to give LLMs dynamic knowledge access."
                ),
            },

            # --- Vector / embedding queries ---
            "vector": {
                "section": "Vector DB & RAG, p.16-21",
                "response": (
                    "[SIMULATION] Vector search activated. Returning top-3 "
                    "semantically similar chunks from the knowledge base."
                ),
            },

            # --- Memory demo (p.5-6) ---
            "memory": {
                "section": "LangChain Memory, p.5-6",
                "buffer_history": [
                    {"human": "What are the main agent frameworks?",
                     "ai": "The main frameworks include LangChain, LangGraph, "
                           "LlamaIndex, AutoGPT, CrewAI, and AutoGen."},
                    {"human": "Which one is best for RAG?",
                     "ai": "LlamaIndex excels at RAG with its advanced semantic "
                           "indexing and context compression capabilities."},
                    {"human": "Can I combine them?",
                     "ai": "Yes, a common pattern is LangChain for orchestration "
                           "combined with LlamaIndex for document retrieval."},
                ],
                "summary": (
                    "[SIMULATION] Summary of 3 exchanges: The user asked about "
                    "agent frameworks and their strengths. Key topics covered: "
                    "LangChain for orchestration, LlamaIndex for RAG, and the "
                    "compose-over-build philosophy of combining frameworks."
                ),
            },

            # --- Framework comparison (p.2-12) ---
            "framework": {
                "section": "Agent development frameworks, p.2-12",
                "response": (
                    "[SIMULATION] Framework comparison: LangChain excels at "
                    "modular orchestration (70K+ stars), LlamaIndex at knowledge "
                    "retrieval (41K stars), AutoGPT at autonomous goal planning "
                    "(150K stars), CrewAI at role-based collaboration (30K stars), "
                    "and AutoGen at conversational multi-agent workflows."
                ),
            },
        }

    def invoke(self, query: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Match query keywords to registry, return mock response.

        Args:
            query: The input query string.
            context: Optional additional context (unused in simulation).

        Returns:
            A dictionary containing the mock response data.
        """
        query_lower = query.lower() if isinstance(query, str) else ""
        for keyword, response in self._registry.items():
            if keyword in query_lower:
                AgentLogger.simulation(
                    f"MockLLM matched keyword '{keyword}' "
                    f"-> {response.get('section', 'N/A')}"
                )
                return response

        # Default fallback for unmatched queries
        AgentLogger.simulation(
            "MockLLM: No keyword match. Returning generic response."
        )
        return {
            "section": "Generic fallback",
            "response": (
                f"[SIMULATION] The agent processed your query: '{query[:80]}...' "
                f"In live mode, this would call the configured LLM endpoint. "
                f"The mock layer did not find a chapter-specific match."
            ),
        }

    def __repr__(self) -> str:
        return (
            f"MockLLM(registry_size={len(self._registry)}, "
            f"mode='simulation')"
        )


# ---------------------------------------------------------------------------
# 5. MockToolkit — Mock Tool Implementations
# ---------------------------------------------------------------------------

class MockToolkit:
    """Mock implementations of all tools demonstrated in Chapter 2.

    Each method mirrors a tool from the chapter's code examples and
    returns deterministic, chapter-relevant data.

    Author: Imran Ahmad — Chapter 2, The Agent Engineer's Toolkit
    """

    @staticmethod
    @fail_gracefully(
        section_ref="LangChain Calculator Tool, p.4-5",
        fallback_value="[SIMULATION] Calculation error. Fallback: result = 0",
    )
    def calculator(expression: str) -> str:
        """Evaluate a mathematical expression using sympy.

        This is a real computation (not mocked) since sympy is a
        core dependency. Demonstrates the Calculator tool from
        the LangChain agent example on p.4-5.
        """
        from sympy import sympify
        result = sympify(expression)
        return str(result)

    @staticmethod
    @fail_gracefully(
        section_ref="LangChain WebSearch Tool, p.4-5",
        fallback_value="[SIMULATION] Search unavailable. No results.",
    )
    def web_search(query: str) -> str:
        """Mock web search returning chapter-relevant results.

        Demonstrates the DuckDuckGoSearchRun tool from the
        LangChain agent example on p.4-5.
        """
        mock_results = {
            "quantum computing": (
                "Recent advances in quantum computing include processors "
                "exceeding 1,000 qubits, breakthroughs in error correction, "
                "and early demonstrations of quantum advantage."
            ),
            "number 12": (
                "The number 12 is significant in mathematics, culture, "
                "and sports. It represents a dozen, appears in clock faces, "
                "and is a retired jersey number for several sports legends."
            ),
            "stock market": (
                "Markets showed mixed performance today with tech stocks "
                "leading gains while energy sector declined modestly."
            ),
            "agent framework": (
                "LangChain, LangGraph, LlamaIndex, CrewAI, and AutoGen "
                "are the leading agent development frameworks in 2025, "
                "each with distinct strengths and ideal use cases."
            ),
        }
        for key, result in mock_results.items():
            if key in query.lower():
                return f"[SIMULATION] Search result: {result}"
        return (
            f"[SIMULATION] Search result for '{query}': "
            f"General information found. In live mode, this would "
            f"query DuckDuckGo for real-time results."
        )

    @staticmethod
    @fail_gracefully(section_ref="Vector DB & RAG Pipeline, p.16-21")
    def vector_search(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Simulated vector similarity search with scored results.

        Demonstrates the RAG retrieval pipeline from the
        "Building the brain of your AI agent" section on p.19.
        """
        mock_chunks = [
            {
                "text": (
                    "Vector databases represent meaning as direction in "
                    "space. Your question becomes a vector pointing in a "
                    "specific direction in high-dimensional space."
                ),
                "similarity_score": 0.92,
                "source": "Chapter 2, p.17",
            },
            {
                "text": (
                    "ANN algorithms such as HNSW and IVF make searching "
                    "billions of high-dimensional vectors possible in "
                    "milliseconds, enabling real-time semantic retrieval."
                ),
                "similarity_score": 0.87,
                "source": "Chapter 2, p.17",
            },
            {
                "text": (
                    "The RAG pipeline: chunk your knowledge into digestible "
                    "pieces, embed everything into vectors, store with "
                    "metadata, retrieve on demand, inject into prompts."
                ),
                "similarity_score": 0.81,
                "source": "Chapter 2, p.19",
            },
            {
                "text": (
                    "Hierarchical chunking stores the same content at "
                    "multiple granularities and dynamically chooses the "
                    "appropriate level during retrieval."
                ),
                "similarity_score": 0.74,
                "source": "Chapter 2, p.20",
            },
            {
                "text": (
                    "Rerankers examine query-document pairs in detail, "
                    "dramatically improving precision beyond first-stage "
                    "vector retrieval."
                ),
                "similarity_score": 0.69,
                "source": "Chapter 2, p.20",
            },
        ]
        AgentLogger.simulation(
            f"Vector search for '{query}' -> returning top-{top_k} chunks."
        )
        return mock_chunks[:top_k]

    @staticmethod
    @fail_gracefully(
        section_ref="LangChain Tool Abstraction, p.22",
        fallback_value="[SIMULATION] Stock price unavailable.",
    )
    def get_stock_price(ticker: str) -> str:
        """Mock stock price tool from the Tool Integration section.

        Demonstrates the LangChain Tool abstraction pattern on p.22.
        """
        prices = {
            "AAPL": 187.42,
            "GOOGL": 175.30,
            "MSFT": 420.15,
            "AMZN": 195.73,
            "NVDA": 890.25,
        }
        ticker_upper = ticker.upper()
        if not ticker_upper.isalpha():
            raise ValueError(f"Invalid ticker symbol: {ticker}")
        price = prices.get(ticker_upper, 100.00)
        return f"The price of {ticker_upper} is ${price:.2f} (simulated)"

    @staticmethod
    @fail_gracefully(section_ref="OpenAI Function Calling, p.23")
    def get_weather(city: str) -> Dict[str, str]:
        """Mock weather function for the Function Calling demo.

        Demonstrates the OpenAI function calling JSON schema on p.23.
        """
        weather_data = {
            "Toronto": {
                "temperature": "18°C",
                "condition": "Partly cloudy",
                "humidity": "62%",
                "wind": "12 km/h NW",
            },
            "New York": {
                "temperature": "22°C",
                "condition": "Sunny",
                "humidity": "45%",
                "wind": "8 km/h SW",
            },
            "London": {
                "temperature": "14°C",
                "condition": "Overcast",
                "humidity": "78%",
                "wind": "18 km/h W",
            },
        }
        result = weather_data.get(city, {
            "temperature": "20°C",
            "condition": "Clear",
            "humidity": "50%",
            "wind": "10 km/h",
        })
        return result


# ---------------------------------------------------------------------------
# 6. MockMemory — Simulated Conversation Memory
# ---------------------------------------------------------------------------

class MockMemory:
    """Simulated conversation memory for LangChain memory demos.

    Supports two modes matching the chapter's examples on p.5-6:
        - "buffer": ConversationBufferMemory (stores full history)
        - "summary": ConversationSummaryMemory (compressed summary)

    Author: Imran Ahmad — Chapter 2, The Agent Engineer's Toolkit
    """

    def __init__(self, mode: str = "buffer"):
        """Initialize memory in the specified mode.

        Args:
            mode: Either "buffer" (full history) or "summary" (compressed).
        """
        if mode not in ("buffer", "summary"):
            raise ValueError(f"Mode must be 'buffer' or 'summary', got '{mode}'")
        self.mode = mode
        self._history: List[Dict[str, str]] = []

    def add_exchange(self, human: str, ai: str) -> None:
        """Record a human-AI exchange.

        Args:
            human: The human message.
            ai: The AI response.
        """
        self._history.append({"human": human, "ai": ai})
        AgentLogger.info(
            f"MockMemory ({self.mode}): Recorded exchange "
            f"#{len(self._history)}"
        )

    def load_memory(self) -> Any:
        """Retrieve stored memory in the configured mode.

        Returns:
            Full history list (buffer mode) or summary string (summary mode).
        """
        if self.mode == "buffer":
            AgentLogger.simulation(
                f"Buffer memory returning {len(self._history)} exchanges."
            )
            return list(self._history)  # Return a copy

        # Summary mode
        count = len(self._history)
        if count == 0:
            return "[SIMULATION] No conversation history to summarize."

        topics = set()
        for exchange in self._history:
            text = exchange["human"].lower()
            if "framework" in text or "langchain" in text:
                topics.add("agent frameworks")
            if "rag" in text or "retrieval" in text or "vector" in text:
                topics.add("RAG and vector databases")
            if "tool" in text:
                topics.add("tool integration")
            if "model" in text or "llm" in text:
                topics.add("LLM selection")
            if "memory" in text:
                topics.add("memory systems")

        if not topics:
            topics.add("agent engineering concepts")

        topics_str = ", ".join(sorted(topics))
        AgentLogger.simulation(
            f"Summary memory compressing {count} exchanges."
        )
        return (
            f"[SIMULATION] Summary of {count} exchanges: "
            f"The conversation covered {topics_str}. Key insights from "
            f"Chapter 2 were discussed including framework comparisons "
            f"and the compose-over-build philosophy."
        )

    def clear(self) -> None:
        """Reset all stored memory."""
        self._history.clear()
        AgentLogger.info(f"MockMemory ({self.mode}): History cleared.")

    def __repr__(self) -> str:
        return (
            f"MockMemory(mode='{self.mode}', "
            f"exchanges={len(self._history)})"
        )
