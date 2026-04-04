"""
Agent Utilities — Chapter 6: Information Retrieval and Knowledge Agents
Author: Imran Ahmad
Book: AI Agents (Packt, 2026)

Provides: ColorLogger, resilience decorator, API key management,
and simulation-mode mocks for all three agent types in Chapter 6.
"""

import os
import sys
import functools
import hashlib
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv


# ─────────────────────────────────────────────
# 1. COLOR-CODED LOGGER
# ─────────────────────────────────────────────

class ColorLogger:
    """
    Visual logging with color-coded output for agent operations.

    Schema:
      [INFO]    (Blue)   — Pipeline steps, tool initialization
      [SUCCESS] (Green)  — Step completed, valid output returned
      [ERROR]   (Red)    — Handled failure, fallback activated
    """
    BLUE   = "\033[94m"
    GREEN  = "\033[92m"
    RED    = "\033[91m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"

    def info(self, msg: str) -> None:
        print(f"{self.BLUE}{self.BOLD}[INFO]{self.RESET}    {msg}")

    def success(self, msg: str) -> None:
        print(f"{self.GREEN}{self.BOLD}[SUCCESS]{self.RESET} {msg}")

    def error(self, msg: str) -> None:
        print(f"{self.RED}{self.BOLD}[ERROR]{self.RESET}   {msg}")


log = ColorLogger()


# ─────────────────────────────────────────────
# 2. RESILIENCE DECORATOR
# ─────────────────────────────────────────────

def fail_gracefully(fallback_return=None, section_ref=""):
    """
    Wraps any agent tool call in defensive logic.
    On exception: logs RED error with chapter section reference,
    returns fallback value, never terminates execution.

    Args:
        fallback_return: Value returned on failure.
        section_ref: Chapter section (e.g., '6.1') for traceability.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                log.info(f"Executing: {func.__name__} [Ref: §{section_ref}]")
                result = func(*args, **kwargs)
                log.success(f"{func.__name__} completed. [Ref: §{section_ref}]")
                return result
            except Exception as e:
                log.error(
                    f"{func.__name__} failed: {type(e).__name__}: {e}. "
                    f"Falling back to mock result. [Ref: §{section_ref}]"
                )
                if callable(fallback_return):
                    return fallback_return()
                return fallback_return
        return wrapper
    return decorator


# ─────────────────────────────────────────────
# 3. API KEY MANAGEMENT (Zero-Hardcode Policy)
# ─────────────────────────────────────────────

def get_api_key(env_var: str = "OPENAI_API_KEY") -> Optional[str]:
    """
    Retrieve API key with cascading fallback:
      1. .env file (python-dotenv)
      2. OS environment variable
      3. Interactive getpass prompt
      4. None → activates SIMULATION MODE

    Returns:
        The API key string, or None if unavailable.
    """
    import getpass as _getpass

    load_dotenv()
    key = os.getenv(env_var)
    if key and key.strip() not in ("", "your_key_here"):
        log.success(f"API key loaded from environment ({env_var}).")
        return key.strip()

    log.info(f"No valid {env_var} found in .env or environment.")

    # Guard: only prompt if stdin is interactive (avoids blocking in
    # non-interactive Jupyter kernels or CI pipelines)
    try:
        if sys.stdin and sys.stdin.isatty():
            key = _getpass.getpass(
                f"Enter {env_var} (or press Enter for Simulation Mode): "
            )
            if key.strip():
                log.success("API key provided interactively.")
                return key.strip()
    except Exception:
        # Broad catch: handles EOFError, KeyboardInterrupt,
        # StdinNotImplementedError, and any other stdin issues
        pass

    log.error(
        f"No API key available for {env_var}. "
        f"SIMULATION MODE activated — all outputs are chapter-derived mocks."
    )
    return None


# ─────────────────────────────────────────────
# 4. MOCK LLM (§6.1 Knowledge Retrieval Agent)
# ─────────────────────────────────────────────

class MockLLM:
    """
    Simulates LLM responses using content derived from Chapter 6.
    Drop-in replacement when SIMULATION_MODE is True.

    Designed to teach the same concepts as live API output.
    Ref: §6.1, RAG pipeline (pp. 6–7)
    """

    RESPONSES = {
        "rag_limitations": (
            "[SIMULATION MODE] Based on the retrieved documents, the main "
            "limitations of retrieval-augmented generation include: "
            "(1) Noise in retrieved chunks can degrade answer quality — "
            "irrelevant context dilutes the LLM's focus (§6.1, Noise "
            "reduction). (2) Index freshness — if the vector store is not "
            "regularly updated, answers reflect stale information (§6.1, "
            "Index freshness). (3) Latency overhead — the retrieval step "
            "adds response time compared to direct generation (§6.1, "
            "Latency control). (4) Chunking sensitivity — poor chunk_size "
            "or overlap parameters can split key facts across boundaries, "
            "causing incomplete answers (§6.1, Chunking strategies).\n\n"
            "Sources: docs/knowledge_base_rag.txt (simulated)"
        ),
        "compliance_query": (
            "[SIMULATION MODE] The latest compliance regulation requires "
            "data retention for a minimum of 7 years for financial records "
            "and 3 years for general correspondence. Automated deletion "
            "policies must be documented and auditable.\n\n"
            "Sources: docs/compliance_policy.txt (simulated)"
        ),
        "refund_policy": (
            "[SIMULATION MODE] The subscription refund policy allows "
            "full refunds within 14 days of renewal. After 14 days, "
            "refunds are prorated based on remaining subscription period.\n\n"
            "Sources: docs/compliance_policy.txt (simulated)"
        ),
    }

    def __call__(self, prompt: str, **kwargs) -> str:
        return self.invoke(prompt)

    def invoke(self, prompt: str, **kwargs) -> str:
        prompt_lower = prompt.lower() if isinstance(prompt, str) else ""
        # Priority: most specific keywords first
        if any(kw in prompt_lower for kw in ["refund", "subscription"]):
            return self.RESPONSES["refund_policy"]
        if any(kw in prompt_lower for kw in ["compliance", "regulation", "retention"]):
            return self.RESPONSES["compliance_query"]
        if any(kw in prompt_lower for kw in ["limitation", "challenge", "rag"]):
            return self.RESPONSES["rag_limitations"]
        return self.RESPONSES["rag_limitations"]


class MockRetrievalQAResult:
    """
    Simulates RetrievalQA chain output structure.
    Ref: §6.1, RetrievalQA.from_chain_type (p. 7)
    """

    def __init__(self, query: str):
        self.llm = MockLLM()
        self.query = query

    def run(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "result": self.llm.invoke(self.query),
            "source_documents": [
                {"metadata": {"source": "docs/knowledge_base_rag.txt"}, "page_content": "Simulated chunk 1"},
                {"metadata": {"source": "docs/compliance_policy.txt"}, "page_content": "Simulated chunk 2"},
                {"metadata": {"source": "docs/knowledge_base_rag.txt"}, "page_content": "Simulated chunk 3"},
            ],
        }


# ─────────────────────────────────────────────
# 5. MOCK EMBEDDINGS (§6.1)
# ─────────────────────────────────────────────

class MockEmbeddings:
    """
    Deterministic pseudo-embeddings for FAISS indexing without an API key.
    Uses a seeded hash of each text for reproducibility.
    Ref: §6.1, OpenAIEmbeddings / text-embedding-3-large (p. 6)
    """
    DIMENSION = 256

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._embed(text)

    def _embed(self, text: str) -> List[float]:
        seed = int(hashlib.md5(text.encode()).hexdigest()[:8], 16) % (2**31)
        rng = np.random.RandomState(seed)
        vec = rng.randn(self.DIMENSION).astype(float)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist() if norm > 0 else vec.tolist()


# ─────────────────────────────────────────────
# 6. MOCK OCR (§6.2 Document Intelligence Agent)
# ─────────────────────────────────────────────

@dataclass
class MockOcrToken:
    """Single OCR token with position, confidence, and line grouping."""
    text: str
    x: int
    y: int
    w: int
    h: int
    conf: float
    line_id: int


# Synthetic invoice tokens — matches the SCHEMA on p. 13 of Chapter 6
MOCK_INVOICE_TOKENS = [
    # Line 1: header
    MockOcrToken("INVOICE", 50, 50, 120, 20, 98.0, 1),
    # Line 2: invoice number
    MockOcrToken("Invoice", 50, 100, 60, 16, 95.0, 2),
    MockOcrToken("No:", 115, 100, 25, 16, 93.0, 2),
    MockOcrToken("INV-2026-00142", 150, 100, 120, 16, 97.0, 2),
    # Line 3: date
    MockOcrToken("Date:", 50, 130, 40, 16, 96.0, 3),
    MockOcrToken("2026-03-15", 100, 130, 90, 16, 94.0, 3),
    # Line 4: total
    MockOcrToken("Total", 50, 300, 45, 16, 92.0, 6),
    MockOcrToken("Due:", 100, 300, 35, 16, 90.0, 6),
    MockOcrToken("$4,750.00", 145, 300, 80, 16, 96.0, 6),
    # Line 5: low-confidence token (demonstrates CONFIDENCE_THRESHOLD filtering)
    MockOcrToken("Smudged", 50, 350, 60, 16, 35.0, 7),
]

MOCK_EXTRACTED_FIELDS = {
    "invoice_number": "INV-2026-00142",
    "invoice_date": "2026-03-15",
    "total_amount": "$4,750.00",
}


def mock_pytesseract_output() -> Dict[str, list]:
    """
    Returns a dict matching pytesseract.image_to_data(output_type=DICT) format.
    Includes both high- and low-confidence tokens to demonstrate
    the CONFIDENCE_THRESHOLD=60 filter from §6.2 (p. 12).
    """
    data = {
        "text": [], "conf": [], "left": [], "top": [],
        "width": [], "height": [],
        "block_num": [], "par_num": [], "line_num": [],
    }
    for t in MOCK_INVOICE_TOKENS:
        data["text"].append(t.text)
        data["conf"].append(str(int(t.conf)))
        data["left"].append(t.x)
        data["top"].append(t.y)
        data["width"].append(t.w)
        data["height"].append(t.h)
        data["block_num"].append(1)
        data["par_num"].append(1)
        data["line_num"].append(t.line_id)
    return data


# ─────────────────────────────────────────────
# 7. MOCK ARXIV SEARCH (§6.3 Scientific Research Agent)
# ─────────────────────────────────────────────

MOCK_ARXIV_PAPERS = pd.DataFrame([
    {
        "title": "Evaluating Retrieval-Augmented Generation: A Comprehensive Survey",
        "summary": (
            "This survey examines evaluation methodologies for RAG systems, "
            "covering faithfulness metrics, hallucination detection benchmarks, "
            "and retrieval quality assessment. We identify key gaps in current "
            "evaluation frameworks and propose standardized benchmarks."
        ),
        "authors": "Chen, W., Park, S., Liu, R.",
        "published": "2025-11-15",
        "url": "https://arxiv.org/abs/2511.00001",
    },
    {
        "title": "Benchmarking Faithfulness in RAG Pipelines",
        "summary": (
            "We introduce FaithBench, a dataset of 5,000 annotated QA pairs for "
            "measuring faithfulness in retrieval-augmented generation. Experiments "
            "show that chunk size and overlap parameters significantly affect "
            "hallucination rates. Larger chunks reduce hallucinations but increase latency."
        ),
        "authors": "Patel, A., Kim, J.",
        "published": "2025-09-22",
        "url": "https://arxiv.org/abs/2509.00002",
    },
    {
        "title": "Hybrid Retrieval Strategies for Enterprise Knowledge Bases",
        "summary": (
            "This paper compares lexical, semantic, and hybrid retrieval strategies "
            "in enterprise settings. Hybrid retrieval combining BM25 with dense "
            "passage retrieval achieves the best recall across mixed-content corpora, "
            "validating the approach described in recent architectural surveys."
        ),
        "authors": "Fernandez, M., Zhao, L.",
        "published": "2025-08-10",
        "url": "https://arxiv.org/abs/2508.00003",
    },
    {
        "title": "BioRAG: Domain-Adapted Retrieval for Clinical Question Answering",
        "summary": (
            "We present BioRAG, a domain-adapted RAG system for biomedical literature. "
            "Fine-tuned embeddings on PubMed abstracts improve retrieval precision by "
            "23% compared to general-purpose models. The system supports multi-hop "
            "reasoning across clinical evidence."
        ),
        "authors": "Singh, R., Tanaka, H., Morris, E.",
        "published": "2025-10-05",
        "url": "https://arxiv.org/abs/2510.00004",
    },
    {
        "title": "Knowledge Graphs Meet RAG in Drug Discovery Pipelines",
        "summary": (
            "This work integrates knowledge graph traversal with retrieval-augmented "
            "generation for pharmaceutical research. Entity linking unifies compound "
            "references across PubMed, ChEMBL, and patent databases. Results demonstrate "
            "40% faster identification of candidate compounds."
        ),
        "authors": "O'Brien, K., Vasquez, D.",
        "published": "2025-07-18",
        "url": "https://arxiv.org/abs/2507.00005",
    },
    {
        "title": "Chunking Strategies and Their Impact on RAG Quality",
        "summary": (
            "We systematically evaluate fixed-size, recursive, and semantic chunking "
            "across six domains. Recursive chunking with 1000-character chunks and "
            "200-character overlap provides the best balance of precision and recall "
            "for mixed-content corpora. Semantic chunking excels for narrative text "
            "but carries higher computational cost."
        ),
        "authors": "Nakamura, T., Ellis, B.",
        "published": "2025-06-30",
        "url": "https://arxiv.org/abs/2506.00006",
    },
    {
        "title": "Latency-Aware RAG: Optimizing Retrieval for Real-Time Applications",
        "summary": (
            "This paper addresses latency challenges in production RAG systems. "
            "We propose a tiered caching strategy that reduces median response time "
            "by 60% for frequently asked queries while maintaining answer freshness "
            "for dynamic corpora."
        ),
        "authors": "Gupta, S., Almeida, P.",
        "published": "2025-12-01",
        "url": "https://arxiv.org/abs/2512.00007",
    },
    {
        "title": "Multi-Vector Retrieval for Scientific Literature Synthesis",
        "summary": (
            "We introduce a multi-vector representation scheme that captures methodology, "
            "findings, and implications separately for each research paper. This approach "
            "enables more nuanced retrieval when synthesizing evidence across large "
            "scientific corpora."
        ),
        "authors": "Zhang, Y., Thompson, L., Khatri, N.",
        "published": "2025-05-20",
        "url": "https://arxiv.org/abs/2505.00008",
    },
    {
        "title": "Citation Graph Traversal for Research Discovery Agents",
        "summary": (
            "This work formalizes citation graph traversal as a tool for automated "
            "research agents. Starting from seed papers, the agent follows forward "
            "and backward citations to discover clusters of related work, identify "
            "influential studies, and detect emerging research fronts."
        ),
        "authors": "Lee, C., Hoffmann, M.",
        "published": "2025-04-12",
        "url": "https://arxiv.org/abs/2504.00009",
    },
    {
        "title": "Provenance Tracking in Multi-Source RAG Systems",
        "summary": (
            "We propose a provenance framework that maintains metadata, citations, "
            "and confidence metrics throughout the RAG pipeline. The framework ensures "
            "every factual claim in the generated answer is traceable to its source "
            "document, chunk, and retrieval score."
        ),
        "authors": "Williams, A., Johansson, E.",
        "published": "2025-03-08",
        "url": "https://arxiv.org/abs/2503.00010",
    },
    {
        "title": "Document Intelligence Agents for Financial Services",
        "summary": (
            "We deploy a five-stage document intelligence pipeline for automating "
            "invoice and contract processing in financial services. OCR with confidence "
            "scoring, layout parsing, and schema-driven extraction achieve 96.2% accuracy "
            "on critical fields, keeping human review under 5%."
        ),
        "authors": "Marchetti, R., Okonkwo, C.",
        "published": "2025-08-25",
        "url": "https://arxiv.org/abs/2508.00011",
    },
    {
        "title": "Self-Improving Document Extraction with Human-in-the-Loop Feedback",
        "summary": (
            "This paper presents an agent that learns from human corrections to improve "
            "extraction accuracy over time. The feedback loop reduces the human review "
            "rate from 15% to under 4% within three months of deployment, demonstrating "
            "the ADL lifecycle in practice."
        ),
        "authors": "Costa, F., Yamamoto, S.",
        "published": "2025-11-02",
        "url": "https://arxiv.org/abs/2511.00012",
    },
])


def mock_search_arxiv(query: str = "", max_results: int = 12) -> pd.DataFrame:
    """
    Returns synthetic arXiv results for §6.3 Scientific Research Agent demo.
    Ref: §6.3, Broad literature scanning (pp. 22–23)
    """
    log.info(f"[SIMULATION MODE] Returning {min(max_results, len(MOCK_ARXIV_PAPERS))} mock arXiv papers.")
    return MOCK_ARXIV_PAPERS.head(max_results).copy()
