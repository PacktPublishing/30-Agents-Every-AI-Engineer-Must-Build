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
| **Claude Sonnet 4** | LIVE (ChatAnthropic) | LIVE (HuggingFace all-MiniLM-L6-v2) | SIMULATION (mock papers) | Real LLM for RAG |
| **Gemini Flash 2.5** | LIVE (ChatGoogleGenerativeAI) | LIVE (gemini-embedding-001) | SIMULATION (mock papers) | Real LLM for RAG |
| **OpenAI GPT-4o** | SIMULATION (MockRetrievalQAResult) | LIVE (text-embedding-3-large) | LIVE (real arXiv API) | MockLLM for RAG |
| **DeepSeek V2 16B** | LIVE (Ollama deepseek-v2:16b) | LIVE (Ollama llama3.1:8b) | SIMULATION (mock papers) | Real LLM for RAG |

**Key finding:** Only Claude, Gemini, and DeepSeek produced actual LLM-generated RAG answers. OpenAI's RAG queries went through MockRetrievalQAResult (simulation), though it retrieved real arXiv papers for the scientific research task.

---

## Task 1: RAG Query -- "What are the main limitations of RAG?"

### Claude Sonnet 4

**Actual output:**
- Structured with `## Operational Limitations` and `## Retrieval Failures` sections
- Identified three operational limitations: Index Freshness, Latency, Security
- Separately categorized retrieval failure modes (low semantic similarity, vocabulary mismatch)
- Added a `## Mitigation Strategies Mentioned` section synthesizing corrective actions
- Concluded with: "the provided context appears to be incomplete" -- an epistemic caveat

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | All claims traceable to source documents; no hallucinations |
| Completeness | 9 | Covered operational, retrieval, and mitigation aspects; noted incompleteness |
| Structure & Organization | 10 | Hierarchical headings, bold labels, logical sections |
| Conciseness | 7 | Thorough but verbose -- every sentence adds value but could be tighter |
| Source Grounding | 9 | Closely tied to retrieved chunks; acknowledged when context was insufficient |
| Bloom's Level | **5 -- Evaluate** | Categorized limitations by type, assessed impact, judged context completeness |
| Nuance & Caveats | 10 | Explicitly flagged incomplete context -- rare self-awareness |
| Practical Utility | 9 | Directly usable as a diagnostic checklist |

---

### Gemini Flash 2.5

**Actual output:**
- Bullet-point list with five limitations, each with bold header and 1-2 sentence explanation
- Detailed sub-breakdown of chunking misconfiguration (overly large, overly small, insufficient overlap)
- Covered: quality dependency, chunking misconfiguration, ongoing maintenance, vocabulary mismatch
- No meta-commentary on coverage gaps

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 9 | All points directly from retrieved context; accurate claims |
| Completeness | 7 | Strong on chunking details but missed security, latency, and index freshness |
| Structure & Organization | 8 | Clean bullets with bold headers; flat hierarchy (no sections) |
| Conciseness | 9 | Tight, no wasted words -- excellent information density |
| Source Grounding | 8 | Closely tied to chunks but no meta-commentary on coverage |
| Bloom's Level | **3 -- Apply** | Extracted and organized information but did not analyze across categories |
| Nuance & Caveats | 5 | No acknowledgment of missing context or answer limitations |
| Practical Utility | 7 | Useful but narrowly focused on chunking; misses broader operational concerns |

---

### OpenAI GPT-4o

**Execution note:** RAG queries ran through MockRetrievalQAResult (simulation mode), not the actual GPT-4o model. The response is a pre-authored single-paragraph mock.

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 7 | MockLLM response is correct but generic |
| Completeness | 5 | Single paragraph covering basic points only |
| Structure & Organization | 4 | No formatting structure -- flat paragraph |
| Conciseness | 7 | Brief but at cost of completeness |
| Source Grounding | 6 | Generic mock response loosely tied to source |
| Bloom's Level | **2 -- Understand** | Paraphrases source content without analysis |
| Nuance & Caveats | 3 | No qualifications or gap acknowledgment |
| Practical Utility | 4 | Too thin to be actionable |

> *Output is from MockRetrievalQAResult, not the actual GPT-4o model.*

---

### DeepSeek V2 16B (Local)

**Execution note:** RAG pipeline ran with real Ollama DeepSeek V2 16B model and llama3.1:8b embeddings. However, only 16 cells have output (vs 23 for cloud providers), limiting scoring evidence.

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Claims are correct but thin |
| Completeness | 5 | Abbreviated coverage; fewer details than cloud providers |
| Structure & Organization | 4 | Minimal formatting; single paragraph style |
| Conciseness | 8 | Very compact, though at cost of completeness |
| Source Grounding | 7 | Draws from context but lacks elaboration |
| Bloom's Level | **2 -- Understand** | Summarizes accurately but does not analyze or evaluate |
| Nuance & Caveats | 3 | No qualifications or edge case acknowledgment |
| Practical Utility | 5 | Too brief for practitioner use |

---

## Task 2: Diagnostic Query -- "What is our refund policy for subscriptions?"

### Claude Sonnet 4

**Actual output:** Structured with four bold sections:
- **Full Refunds:** Cancel within 14 calendar days of renewal
- **Prorated Refunds:** Formula: (annual subscription cost / 365) x remaining days
- **Processing Time:** 5-10 business days
- **Exclusions:** No refunds for promotional/discounted subscriptions unless required by law
- Added scope qualifier: "This policy applies to customers enrolled in recurring subscription plans"

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 10 | Every detail matches the source policy document exactly |
| Completeness | 10 | Covered all four aspects including exclusions and scope |
| Structure & Organization | 10 | Clear sections that mirror a real policy document |
| Conciseness | 9 | Comprehensive without redundancy |
| Source Grounding | 10 | Every claim directly from compliance_policy.txt |
| Bloom's Level | **4 -- Analyze** | Decomposed the policy into logical components |
| Nuance & Caveats | 8 | Noted the legal exception for promotional subscriptions |
| Practical Utility | 10 | Could be given directly to a customer support agent |

---

### Gemini Flash 2.5

**Actual output:** Flowing paragraph covering:
- Full refund within 14 calendar days
- Prorated refund formula (daily rate x remaining days)
- Processing time: 5-10 business days
- Promotional exclusion with legal caveat

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 10 | All details correct and complete |
| Completeness | 9 | Covered full refunds, proration, processing time, exclusions |
| Structure & Organization | 6 | Dense paragraph -- harder to scan than structured output |
| Conciseness | 8 | Complete but could benefit from visual structure |
| Source Grounding | 10 | Faithfully reproduces source policy |
| Bloom's Level | **3 -- Apply** | Extracted and reorganized information for the question |
| Nuance & Caveats | 7 | Mentioned the legal exception |
| Practical Utility | 7 | Correct but a support agent would prefer bulleted format |

---

### OpenAI GPT-4o

**Execution note:** MockRetrievalQAResult returned: "[SIMULATION MODE] The subscription refund policy allows full refunds within 14 days of renewal. After 14 days, refunds are prorated based on remaining subscription period."

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Core facts correct but simplified |
| Completeness | 5 | Missed exclusions, processing time, and the proration formula |
| Structure & Organization | 4 | Single sentence, no formatting |
| Conciseness | 7 | Brief but incomplete |
| Source Grounding | 6 | Generic summary of policy |
| Bloom's Level | **2 -- Understand** | Summarizes without decomposition |
| Nuance & Caveats | 2 | No mention of exclusions or edge cases |
| Practical Utility | 4 | Missing details a customer would ask about |

> *Output is from MockRetrievalQAResult.*

---

### DeepSeek V2 16B (Local)

| Dimension | Score | Rationale |
|---|---|---|
| Factual Accuracy | 8 | Core facts correct |
| Completeness | 6 | Covered basics but missed exclusions and formula details |
| Structure & Organization | 5 | Single paragraph format |
| Conciseness | 8 | Brief but incomplete |
| Source Grounding | 7 | Draws from source but drops details |
| Bloom's Level | **2 -- Understand** | Summarizes but does not decompose |
| Nuance & Caveats | 3 | No mention of exclusions |
| Practical Utility | 5 | Missing details for practical use |

---

## Task 3: Scientific Research Synthesis

### Execution Modes

- **OpenAI:** Retrieved LIVE arXiv papers (real 2025 papers including "Investigating Retrieval-Augmented Generation in Quranic Studies" and "FAIR-RAG: Faithful Adaptive Iterative Refinement"). Clustered using real embeddings with TF-IDF labels.
- **Claude, Gemini, DeepSeek:** All used SIMULATION MODE for arXiv retrieval (12 mock papers from agent_utils.py). Clustering used SentenceTransformer embeddings but on identical mock data.

Since 3 of 4 providers used mock data for this task, cross-provider comparison of synthesis quality is limited. The clustering and labeling outputs are largely driven by the embedding model and KMeans algorithm, not the LLM itself.

---

## Overall Scorecard

Averaged across Tasks 1 and 2 (the RAG queries where LLM differentiation is most meaningful):

| Dimension | Claude Sonnet 4 | Gemini Flash 2.5 | OpenAI GPT-4o | DeepSeek V2 (Local) |
|---|---|---|---|---|
| Factual Accuracy | **9.5** | **9.5** | **7.5*** | **8.0** |
| Completeness | **9.5** | **8.0** | **5.0*** | **5.5** |
| Structure & Organization | **10.0** | **7.0** | **4.0*** | **4.5** |
| Conciseness | **8.0** | **8.5** | **7.0*** | **8.0** |
| Source Grounding | **9.5** | **9.0** | **6.0*** | **7.0** |
| Bloom's Taxonomy Level | **4.5 (Analyze-Evaluate)** | **3.0 (Apply)** | **2.0 (Understand)*** | **2.0 (Understand)** |
| Nuance & Caveats | **9.0** | **6.0** | **2.5*** | **3.0** |
| Practical Utility | **9.5** | **7.0** | **4.0*** | **5.0** |
| **WEIGHTED AVERAGE** | **8.7** | **7.3** | **4.8*** | **5.4** |

> *\* OpenAI scores reflect MockRetrievalQAResult output for RAG tasks. With a real RetrievalQA chain, GPT-4o would be expected to score in the 7.5-8.5 range.*

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    | ============ Claude Sonnet 4 (Task 1)
Level 4: Analyze     | ============ Claude Sonnet 4 (Task 2)
Level 3: Apply       | ============ Gemini Flash 2.5
Level 2: Understand  | ============ DeepSeek V2 / OpenAI* (MockLLM)
Level 1: Remember    |
```

Claude reaches Level 5 on the RAG limitations query by categorizing limitations into types (operational vs. retrieval), assessing their impact, and critically noting when its own evidence base is insufficient. Gemini operates solidly at Level 3 -- correctly mapping information to questions but rarely stepping back to evaluate. DeepSeek stays at Level 2 with accurate but shallow paraphrasing.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  Claude Sonnet 4        8.7   ==========================....
  Gemini Flash 2.5       7.3   =====================.........
  DeepSeek V2 (Local)    5.4   ================..............
  OpenAI GPT-4o          4.8*  ==============................
```

> *OpenAI ran in Simulation Mode for RAG queries.*

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     | C
  L4 Analyze      | C
  L3 Apply        | C G
  L2 Understand   | C G D O
  L1 Remember     | C G D O
```

Legend: **C** = Claude Sonnet 4, **G** = Gemini Flash 2.5, **D** = DeepSeek V2, **O** = OpenAI GPT-4o

---

## Winner: Claude Sonnet 4

| | |
|---|---|
| **Chapter 6 Winner** | **Claude Sonnet 4** |
| **Score** | **8.7 / 10** |
| **Bloom's Level** | **Level 5 -- Evaluate** |

**Why Claude Sonnet 4 wins this chapter:**
- Highest weighted average across all 8 scoring dimensions
- Only provider to reach Bloom's Level 5 -- evaluating context completeness and categorizing limitations by type
- Produced structured, section-based output that mirrors professional documentation
- The epistemic caveat ("context appears to be incomplete") demonstrates a level of self-awareness absent from other providers

**Important caveat:** OpenAI GPT-4o was not fairly tested because its RAG queries ran through MockRetrievalQAResult. With a live RetrievalQA chain, GPT-4o would likely score significantly higher (estimated 7.5-8.5 range).

**Runner-up:** Gemini Flash 2.5 (7.3/10) -- excellent conciseness and accuracy, but narrower coverage and flat structure

**Third place:** DeepSeek V2 (5.4/10) -- correct fundamentals but too brief for practical use

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Maximum quality | Claude Sonnet 4 | Highest completeness, structure, and analytical depth |
| Cost-efficient production | Gemini Flash 2.5 | Strong accuracy with excellent conciseness at lower cost |
| Air-gapped / private data | DeepSeek V2 (Local) | Only option with zero cloud dependency |
| Rapid prototyping | DeepSeek V2 (Local) | No API key, instant iteration, zero cost |


## Provider Profiles

### Claude Sonnet 4 -- "The Analyst"
**Strengths:** Highest cognitive sophistication (Bloom's Level 5); exceptional structured output with hierarchical sections; proactively flags evidence gaps; best at decomposing complex questions into sub-components.
**Weaknesses:** More verbose than Gemini -- higher token cost for similar factual content.

### Gemini Flash 2.5 -- "The Efficient Extractor"
**Strengths:** Best information-to-word ratio; tight, accurate responses; fast and cost-effective; strong on specific technical details (e.g., chunking parameters).
**Weaknesses:** Tends to deep-dive on one aspect while missing breadth; flat organizational structure; no self-awareness about coverage gaps.

### OpenAI GPT-4o -- "Not Scored (Simulation for RAG)"
**Note:** RAG queries ran through MockRetrievalQAResult. The model did successfully retrieve real arXiv papers for the scientific research task, demonstrating functional live API integration. With a live RAG chain, GPT-4o would likely be competitive.

### DeepSeek V2 16B -- "The Pragmatic Summarizer"
**Strengths:** Fully local execution; zero cost; correct fundamental facts; viable for prototyping.
**Weaknesses:** Consistently shallow responses (Bloom's Level 2); minimal formatting; no self-awareness about completeness.

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Production RAG system** | Claude Sonnet 4 | Highest completeness, structure, and source grounding |
| **High-volume document processing** | Gemini Flash 2.5 | Best speed/cost ratio with strong accuracy |
| **Offline / air-gapped environments** | DeepSeek V2 (Local) | Only option that runs without cloud access |
| **Research synthesis** | Claude Sonnet 4 | Deepest analytical output with categorical reasoning |
| **Cost-optimized production** | Gemini Flash 2.5 | Lowest per-token cost among cloud providers |
| **Compliance-critical applications** | Claude Sonnet 4 | Best at surfacing caveats and edge cases |

---

*Analysis based on Chapter 6 notebook outputs executed April 2026. Claude and Gemini ran in LIVE mode for RAG queries. OpenAI ran in Simulation Mode for RAG (but live for arXiv). DeepSeek ran with a real local Ollama model. Scores reflect actual notebook evidence.*
