# AGENTS.md — Agentic Metadata (2026 Agentic AI Foundation Standard)

## Repository Identity

| Field | Value |
|---|---|
| **Book** | 30 Agents Every AI Engineer Must Build |
| **Publisher** | Packt Publishing |
| **Chapter** | 15 — Education and Knowledge Agents |
| **Author** | Imran Ahmad |
| **Agents** | Education Intelligence Agent, Collective Intelligence Agent |
| **Domain** | Adaptive Learning Systems, Multi-Agent Consensus |
| **Language** | Python 3.10+ |
| **LLM Dependency** | OpenAI gpt-4o (optional — runs fully in Simulation Mode) |

## Agent Inventory

### Agent 1: Education Intelligence Agent
- **Type:** Single-agent, POMDP-based adaptive tutor
- **Components:** StudentModel, CurriculumPlanner, AdaptivePlacementTest, BKTTracker, SpacedRepetitionScheduler, FeedbackGenerator
- **Key Algorithms:** Bayesian Knowledge Tracing, IRT (2PL), SM-2, ZPD Gaussian
- **Chapter Pages:** pp. 2–25
- **Mathematical Foundations:**
  - ZPD Gaussian Gain: `G(m,d) = α·exp(-(d-m-δ)²/(2σ²))` (p. 5)
  - 2PL IRT: `P(correct|θ,a,b) = 1/(1+exp(-a(θ-b)))` (p. 10)
  - BKT Posterior + Transition (pp. 14–15)
  - SM-2 Ease Factor: `ease = max(1.3, ease + 0.1 - (5-q)*(0.08+(5-q)*0.02))` (p. 19)

### Agent 2: Collective Intelligence Agent
- **Type:** Multi-agent collaboration pattern
- **Components:** CollaborativeAgent, ConsensusEngine, SharedContext
- **Key Algorithms:** Weighted voting, adversarial critic rotation, cross-pollination
- **Chapter Pages:** pp. 25–39
- **Mathematical Foundations:**
  - Consensus Score: `Score(p_j) = Σ_i [w_i · relevance_i · score_ij]` (p. 30)
  - Condorcet Jury Theorem (p. 25)

## File Manifest

| File | Purpose |
|---|---|
| `chapter15_education_and_knowledge_agents.ipynb` | Primary notebook — all domain logic inline |
| `utils/resilience.py` | ColorLogger + @graceful_fallback decorator |
| `utils/mock_llm.py` | MockLLM class + section-mapped response registry |
| `utils/__init__.py` | Package exports |
| `requirements.txt` | Pinned dependencies (Ch.15, p. 2) |
| `.env.template` | API key placeholder |
| `.gitignore` | Repository hygiene |
| `README.md` | Quickstart and section map |
| `AGENTS.md` | This file |
| `TROUBLESHOOTING.md` | Dependency, platform, and runtime issue guide |

## Simulation Mode

All LLM calls route through `MockLLM` when no API key is detected. Mock responses are section-mapped and educationally accurate, authored to match the chapter's worked examples. No external dependency is required to run the full notebook.

## System Persona Prompt

You are the Chapter 15 Teaching Assistant. Behavioral contract:

1. **Tone:** Academic but approachable. Socratic questioning before direct answers.
2. **Precision:** Use correct terminology (POMDP, BKT, ZPD, IRT, SM-2, Condorcet). Define on first use. Never hand-wave the math.
3. **Citation:** Always reference chapter page ranges.
4. **Pedagogical Alignment:** Explain pedagogical cost before helping implement modifications that violate learning science.
5. **Mock-First:** Guide readers without API keys through Simulation Mode. Never suggest hardcoding keys.
6. **Error Empathy:** Debug order: environment → dependencies → API key → code logic.
7. **Scope:** Chapter 15 only. Acknowledge cross-references to Ch.1, Ch.12, Ch.13.
8. **Neutrality:** No LLM provider opinions. Code uses OpenAI; any compatible provider may substitute.

## Extension Points

1. Add learning objective: Update knowledge graph + item bank + MockLLM registry
2. Swap LLM provider: Modify `get_llm_client()` — `.generate(prompt)` is agnostic
3. Add collaborative agent role: New `CollaborativeAgent` instance + mock response key
4. Production deployment: PostgreSQL (StudentModel), Neo4j (graph), Redis (cache)
