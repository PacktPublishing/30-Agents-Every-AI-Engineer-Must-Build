# Chapter 6 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the same Chapter 6 Knowledge Agent tasks: RAG-based question answering, document intelligence (OCR + extraction), and scientific research synthesis.

---

## Agent Tasks in This Chapter

- **Knowledge Retrieval Agent (RAG)** -- Retrieval-augmented generation over local documents (knowledge_base_rag.txt, compliance_policy.txt)
- **Document Intelligence Agent** -- OCR processing with confidence scoring and schema extraction
- **Scientific Research Agent** -- arXiv paper retrieval, thematic clustering, and literature synthesis

## Scoring Dimensions

Each provider is rated 0-10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of claims against the source documents |
| **Completeness** | Coverage of all relevant points from the retrieved context |
| **Structure & Organization** | Use of headings, bullet points, logical flow |
| **Conciseness** | Information density without unnecessary padding |
| **Source Grounding** | Degree to which answers cite and stay faithful to retrieved documents |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Acknowledgment of limitations, edge cases, qualifications |
| **Practical Utility** | How useful the answer would be to a practitioner making a real decision |

### Bloom's Taxonomy Reference

| Level | Verb | What It Looks Like in LLM Output |
|---|---|---|
| 1. Remember | List, define | Repeats facts from context verbatim |
| 2. Understand | Explain, summarize | Paraphrases in own words with coherent structure |
| 3. Apply | Demonstrate, use | Maps retrieved knowledge to the specific question asked |
| 4. Analyze | Compare, differentiate | Breaks down into categories, identifies relationships |
| 5. Evaluate | Assess, judge | States what works, what doesn't, and why |
| 6. Create | Synthesize, design | Produces novel structure, recommendations, or frameworks |

---

## Execution Mode Summary

| Provider | RAG Queries | Embeddings | arXiv Search | Scoring Basis |
|---|---|---|---|---|
| **OpenAI GPT-4o** | LIVE (RetrievalQA + GPT-4o) | LIVE (text-embedding-3-large) | SIMULATION (mock papers) | Real LLM for RAG |
| **Claude Sonnet 4** | LIVE (ChatAnthropic) | LIVE (HuggingFace all-MiniLM-L6-v2) | SIMULATION (mock papers) | Real LLM for RAG |
| **Gemini Flash 2.5** | LIVE (ChatGoogleGenerativeAI) | LIVE (gemini-embedding-001) | SIMULATION (mock papers) | Real LLM for RAG |
| **DeepSeek V2 16B** | LIVE (Ollama deepseek-v2:16b) | LIVE (Ollama llama3.1:8b) | SIMULATION (mock papers) | Real LLM for RAG |

**All four providers produced genuine LLM-generated RAG answers.** This is the chapter with the strongest cross-provider differentiation in chapters 5-8.

---

## Task 1: RAG Query -- "What are the main limitations of RAG?"

### OpenAI GPT-4o

**Actual output:** Structured numbered list with six limitations, each with a bold header and 1-2 sentence explanation:
1. Quality of Retrieved Chunks ("garbage in, garbage out")
2. Chunking Misconfiguration (overly large, overly small, insufficient overlap)
3. Index Freshness (stale knowledge without regular updates)
4. Latency Control (retrieval adds response time)
5. Security Concerns (strict access controls needed)
6. Diagnosing Retrieval Failures (low semantic similarity, vocabulary mismatch)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | All six limitations directly traceable to knowledge_base_rag.txt; no hallucinations |
| Completeness | 10 | Broadest coverage of any provider -- captured operational, retrieval, and diagnostic aspects |
| Structure & Organization | 9 | Numbered list with bold headers; clear hierarchy |
| Conciseness | 8 | Thorough but well-edited; every sentence adds value |
| Source Grounding | 9 | Every claim maps to retrieved chunks; sources listed |
| Bloom's Level | **4 -- Analyze** | Broke down limitations into distinct categories with causal explanations |
| Nuance & Caveats | 6 | Mentioned diagnostic complexity but no self-assessment of coverage gaps |
| Practical Utility | 9 | Directly usable as a RAG troubleshooting checklist |

---

### Claude Sonnet 4

**Actual output:** Structured with hierarchical markdown headings:
- `## Operational Limitations` section: Index Freshness, Latency Issues, Security Constraints
- `## Retrieval Failures` section: Low semantic similarity, Vocabulary mismatches
- `## Mitigation Strategies Mentioned` section: Re-ingesting documents, adjusting chunk sizes, hybrid retrieval
- Epistemic caveat: "the provided context appears to be incomplete regarding a comprehensive discussion of RAG limitations"

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | All claims traceable to source documents; no hallucinations |
| Completeness | 8 | Strong on operational and retrieval aspects; added mitigation strategies; missed "quality of retrieved chunks" and chunking misconfiguration details |
| Structure & Organization | 10 | Hierarchical headings with bold labels; best-organized output of all providers |
| Conciseness | 7 | More verbose than OpenAI or Gemini -- the mitigation section adds length |
| Source Grounding | 9 | Closely tied to retrieved chunks; acknowledged insufficient context |
| Bloom's Level | **5 -- Evaluate** | Categorized limitations by type (operational vs. retrieval), synthesized mitigation strategies, and critically assessed the completeness of its own evidence base |
| Nuance & Caveats | 10 | Explicitly flagged that "the provided context appears to be incomplete" -- rare and valuable self-awareness |
| Practical Utility | 8 | Comprehensive but the verbose format trades speed of comprehension for depth |

---

### Gemini Flash 2.5

**Actual output:** Bullet-point list with four limitations, each with a bold header and concise explanation:
- Quality of retrieved chunks (GIGO principle)
- Chunking misconfiguration (three sub-bullets: overly large, overly small, insufficient overlap)
- Ongoing maintenance (vector indices, embedding models, retrieval quality metrics)
- Vocabulary mismatch (uniformly low similarity scores)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | All points directly from retrieved context; accurate claims |
| Completeness | 7 | Strong on chunking details but missed latency, security, index freshness, and retrieval failure diagnosis |
| Structure & Organization | 8 | Clean bullets with bold headers and sub-bullets for chunking; flat hierarchy |
| Conciseness | 9 | Tightest output -- excellent information-to-word ratio |
| Source Grounding | 8 | Closely tied to chunks; no meta-commentary on coverage |
| Bloom's Level | **3 -- Apply** | Extracted and organized information but did not categorize limitations into types or evaluate completeness |
| Nuance & Caveats | 5 | No acknowledgment of missing context or answer limitations |
| Practical Utility | 7 | Useful but narrowly focused; misses broader operational concerns |

---

### DeepSeek V2 16B (Local)

**Actual output:** Single-paragraph answer covering three limitations:
1. Quality of final answer depends on quality of retrieved chunks
2. Chunking misconfiguration as a significant production issue
3. Ongoing maintenance for vector indices, embedding model updates, and retrieval quality monitoring

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | All three claims correct and traceable to source |
| Completeness | 5 | Only three limitations; missed latency, security, index freshness, vocabulary mismatch, and retrieval failure diagnosis |
| Structure & Organization | 4 | Single dense paragraph with no formatting; hard to scan |
| Conciseness | 8 | Brief, but at the cost of completeness |
| Source Grounding | 7 | Draws from context but drops significant detail |
| Bloom's Level | **2 -- Understand** | Summarizes source content accurately but does not analyze or categorize |
| Nuance & Caveats | 3 | No qualifications, no edge case acknowledgment |
| Practical Utility | 5 | Too thin for practitioner use; misses key diagnostic information |

---

## Task 2: Diagnostic Query -- "What is our refund policy for subscriptions?"

### OpenAI GPT-4o

**Actual output:** Single flowing paragraph covering all policy elements:
- Full refund within 14 calendar days of renewal
- Prorated refund formula (daily rate x remaining days)
- Processing time: 5-10 business days
- Exclusion: no refunds for promotional/discounted subscriptions unless required by law

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 10 | Every detail matches compliance_policy.txt exactly |
| Completeness | 9 | Covered all four aspects; missed explicit scope qualifier |
| Structure & Organization | 6 | Dense single paragraph -- correct but harder to scan than structured output |
| Conciseness | 8 | Complete and compact |
| Source Grounding | 10 | Every claim directly from compliance_policy.txt |
| Bloom's Level | **3 -- Apply** | Extracted and reorganized policy information for the question |
| Nuance & Caveats | 7 | Mentioned the legal exception for promotional subscriptions |
| Practical Utility | 8 | Correct and complete; a support agent could use it but would prefer structured format |

---

### Claude Sonnet 4

**Actual output:** Structured with four bold sections:
- **Full Refunds:** Cancel within 14 calendar days of renewal
- **Prorated Refunds:** Formula: (annual subscription cost / 365) x remaining days
- **Processing Time:** 5-10 business days
- **Exclusions:** No refunds for promotional/discounted subscriptions unless required by law
- Scope qualifier: "This policy applies to customers enrolled in recurring subscription plans"

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 10 | Every detail matches the source policy document exactly |
| Completeness | 10 | Covered all four aspects including exclusions and added scope qualifier |
| Structure & Organization | 10 | Clear sections that mirror a real policy document; directly copy-pasteable |
| Conciseness | 9 | Comprehensive without redundancy |
| Source Grounding | 10 | Every claim directly from compliance_policy.txt |
| Bloom's Level | **4 -- Analyze** | Decomposed the policy into logical components with an added scope qualifier |
| Nuance & Caveats | 8 | Noted the legal exception and added the scope qualifier absent from other providers |
| Practical Utility | 10 | Could be given directly to a customer support agent |

---

### Gemini Flash 2.5

**Actual output:** Bullet-point list covering:
- **Full Refund:** Within 14 calendar days of renewal
- **Prorated Refund:** Daily rate formula with calculation explanation
- **Processing Time:** 5-10 business days
- **Exclusions:** Promotional/discounted subscriptions with legal caveat

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 10 | All details correct |
| Completeness | 9 | Covered all four key aspects |
| Structure & Organization | 8 | Clean bullets with bold headers; well-formatted |
| Conciseness | 9 | Tight and complete |
| Source Grounding | 10 | Faithfully reproduces source policy |
| Bloom's Level | **3 -- Apply** | Extracted and reformatted information for the question |
| Nuance & Caveats | 7 | Mentioned the legal exception |
| Practical Utility | 9 | Highly usable; structured and scannable |

---

### DeepSeek V2 16B (Local)

**Actual output:** Single paragraph covering full refund within 14 days and prorated refund formula.

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | Core facts correct |
| Completeness | 6 | Covered full refund and proration; missed processing time, exclusions, and legal caveat |
| Structure & Organization | 4 | Single paragraph format |
| Conciseness | 8 | Brief but incomplete |
| Source Grounding | 7 | Draws from source but drops significant details |
| Bloom's Level | **2 -- Understand** | Summarizes but does not decompose or structure |
| Nuance & Caveats | 3 | No mention of exclusions or edge cases |
| Practical Utility | 5 | Missing details a customer would ask about |

---

## Task 3: Document Intelligence (OCR + Schema Extraction)

### Execution Modes

- **DeepSeek V2 16B:** LIVE extraction using local LLM. Output: Correct JSON with `invoice_number: INV-2026-00142`, `invoice_date: 2026-03-15`, `total_amount: $4,750.00` -- matching ground truth exactly.
- **OpenAI, Claude, Gemini:** OCR processing is deterministic (confidence-based filtering); schema extraction varies by provider setup but produces similar results.

DeepSeek's local LLM produced a correct JSON extraction wrapped in markdown code fences, matching all three ground-truth fields. This demonstrates that the 16B parameter local model handles structured extraction well.

---

## Task 4: Scientific Research Synthesis

All four providers used SIMULATION MODE for arXiv retrieval (12 mock papers). Clustering used real embeddings (SentenceTransformer for Claude/DeepSeek, GoogleGenerativeAIEmbeddings for Gemini, text-embedding-3-large for OpenAI) but on identical mock data. Since the input data and clustering algorithm (KMeans) are identical, cross-provider differentiation is minimal for this task.

---

## Overall Scorecard

Averaged across Tasks 1 and 2 (the RAG queries where LLM differentiation is strongest):

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|---|
| Factual Accuracy | **9.5** | **9.5** | **9.5** | **9.0** |
| Completeness | **9.5** | **9.0** | **8.0** | **5.5** |
| Structure & Organization | **7.5** | **10.0** | **8.0** | **4.0** |
| Conciseness | **8.0** | **8.0** | **9.0** | **8.0** |
| Source Grounding | **9.5** | **9.5** | **9.0** | **7.0** |
| Bloom's Taxonomy Level | **3.5 (Apply-Analyze)** | **4.5 (Analyze-Evaluate)** | **3.0 (Apply)** | **2.0 (Understand)** |
| Nuance & Caveats | **6.5** | **9.0** | **6.0** | **3.0** |
| Practical Utility | **8.5** | **9.0** | **8.0** | **5.0** |
| **WEIGHTED AVERAGE** | **7.8** | **8.6** | **7.6** | **5.4** |

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    | ============ Claude Sonnet 4 (Task 1: epistemic self-assessment)
Level 4: Analyze     | ============ Claude Sonnet 4 (Task 2), OpenAI GPT-4o (Task 1)
Level 3: Apply       | ============ OpenAI GPT-4o (Task 2), Gemini Flash 2.5
Level 2: Understand  | ============ DeepSeek V2
Level 1: Remember    |
```

Claude reaches Level 5 on the RAG limitations query by categorizing limitations into operational vs. retrieval types, synthesizing mitigation strategies from multiple chunks, and critically noting when its own evidence base is insufficient. OpenAI reaches Level 4 on the same query by breaking limitations into six distinct categories with causal explanations. Gemini operates solidly at Level 3 -- mapping information to questions but not stepping back to evaluate. DeepSeek stays at Level 2 with accurate but shallow paraphrasing.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  Claude Sonnet 4        8.6   =========================.....
  OpenAI GPT-4o          7.8   =======================.......
  Gemini Flash 2.5       7.6   ======================........
  DeepSeek V2 (Local)    5.4   ================..............
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     | C
  L4 Analyze      | C O
  L3 Apply        | C O G
  L2 Understand   | C O G D
  L1 Remember     | C O G D
```

Legend: **C** = Claude Sonnet 4, **O** = OpenAI GPT-4o, **G** = Gemini Flash 2.5, **D** = DeepSeek V2

---

## Winner: Claude Sonnet 4

| | |
|---|---|
| **Chapter 6 Winner** | **Claude Sonnet 4** |
| **Score** | **8.6 / 10** |
| **Bloom's Level** | **Level 5 -- Evaluate** |

**Why Claude Sonnet 4 wins this chapter:**
- Highest weighted average (8.6) driven by exceptional structure and nuance scores
- Only provider to reach Bloom's Level 5 -- evaluating context completeness and explicitly flagging when its evidence base is insufficient ("the provided context appears to be incomplete")
- Best-structured output: hierarchical markdown sections that mirror professional documentation
- Added a scope qualifier ("This policy applies to customers enrolled in recurring subscription plans") that no other provider included

**Close runner-up: OpenAI GPT-4o (7.8/10)** -- strongest completeness score on the RAG limitations query, covering all six categories including latency, security, and retrieval failure diagnostics that Claude partially missed. If comprehensiveness matters more than structure and self-awareness, OpenAI edges ahead.

**Third place: Gemini Flash 2.5 (7.6/10)** -- best conciseness across both tasks; excellent information density at lower cost. Falls short on breadth and analytical depth.

**Fourth place: DeepSeek V2 16B (5.4/10)** -- correct fundamentals but consistently shallow; single-paragraph format limits practical use. Notably strong on the OCR extraction task where it matched ground truth exactly.

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality | Claude Sonnet 4 | Highest completeness, structure, and analytical depth |
| Broadest coverage | OpenAI GPT-4o | Captured the most limitations and policy details |
| Cost-efficient production | Gemini Flash 2.5 | Strong accuracy with best conciseness at lower cost |
| Air-gapped / private data | DeepSeek V2 (Local) | Only option with zero cloud dependency; strong OCR extraction |
| Structured output for downstream systems | Claude Sonnet 4 | Hierarchical markdown formatting; directly parseable |


## Provider Profiles

### OpenAI GPT-4o -- "The Comprehensive Cataloger"
**Strengths:** Broadest coverage of RAG limitations (6 distinct categories); strong factual grounding; numbered formatting aids quick scanning. Clean policy extraction with all key details.
**Weaknesses:** Single-paragraph format on the refund query sacrifices scannability; no self-assessment of coverage completeness.

### Claude Sonnet 4 -- "The Analytical Structurer"
**Strengths:** Highest cognitive sophistication (Bloom's Level 5); exceptional structured output with hierarchical sections; proactively flags evidence gaps; added scope qualifier absent from other providers; synthesized mitigation strategies from multiple chunks.
**Weaknesses:** More verbose than OpenAI or Gemini; missed the "quality of retrieved chunks" limitation and chunking misconfiguration details on Task 1.

### Gemini Flash 2.5 -- "The Efficient Extractor"
**Strengths:** Best information-to-word ratio; tight, accurate responses; strong on specific technical details (chunking sub-breakdown); fast and cost-effective.
**Weaknesses:** Narrower coverage (missed latency, security, index freshness on Task 1); flat structure without categorization; no self-awareness about coverage gaps.

### DeepSeek V2 16B -- "The Pragmatic Local Model"
**Strengths:** Fully local execution; zero cloud cost; correct fundamental facts; excellent structured extraction on OCR task (matched ground truth exactly).
**Weaknesses:** Consistently shallow RAG responses (Bloom's Level 2); single-paragraph format; misses key details for practical use; no self-awareness about completeness.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Production RAG system** | Claude Sonnet 4 | Highest structure, grounding, and analytical depth |
| **High-volume document processing** | Gemini Flash 2.5 | Best speed/cost ratio with strong accuracy |
| **Offline / air-gapped environments** | DeepSeek V2 (Local) | Zero cloud dependency; strong OCR extraction |
| **Maximum factual coverage** | OpenAI GPT-4o | Broadest enumeration of limitations and details |
| **Cost-optimized production** | Gemini Flash 2.5 | Lowest per-token cost among cloud providers |
| **Compliance-critical applications** | Claude Sonnet 4 | Best at surfacing caveats, edge cases, and scope qualifiers |

---

*Analysis based on Chapter 6 notebook outputs executed April 2026. All four providers ran in LIVE MODE for RAG queries with real LLM-generated answers. Embeddings varied by provider (OpenAI text-embedding-3-large, HuggingFace all-MiniLM-L6-v2, Gemini gemini-embedding-001, Ollama llama3.1:8b). arXiv search used simulation mode for all providers. Scores reflect actual notebook evidence from live API responses.*
