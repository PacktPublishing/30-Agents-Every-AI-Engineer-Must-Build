# Use Case: Quandri-Inspired Insurance Processing — From Manual Paperwork to Autonomous Agent Networks

**Chapter 1: Foundations of Agent Engineering**
**Book: "30 Agents Every AI Engineer Must Build" by Imran Ahmad (Packt, 2026)**

---

## The Company

**PeakShield Insurance Group** is a mid-size property and casualty brokerage in Vancouver, processing 3,200 policy renewals, endorsements, and claims per week across 14 carrier partners. Annual premium volume: CAD $180M. Operations team: 38 staff handling policy administration, a 5-person IT team, and no ML engineers. Their tech stack is a 12-year-old Applied Epic policy management system connected to carrier portals via manual data entry and email.

## The People

- **Janet Kowalski, COO** — Sponsor. She's watching Quandri (referenced on page 34 of the book) process thousands of policies daily with 99.9% accuracy while her team struggles to keep up with renewal season. The board wants a 40% efficiency gain without proportional headcount growth.
- **Derek Fong, Director of Policy Operations** — Manages the team that processes renewals. His staff spend 70% of their time on data entry — copying information between carrier portals, Applied Epic, and Excel spreadsheets. During renewal season (Q4), overtime costs spike $120K/month and error rates double.
- **Anika Sharma, IT Manager** — Responsible for Applied Epic, carrier API integrations, and a patchwork of RPA bots built over the years. She's skeptical of AI after a 2024 chatbot project that hallucinated policy terms and had to be killed in week two.
- **Mike Tremblay, VP of Client Services** — Owns the broker-client relationship. His team discovers processing errors when clients call about incorrect coverage. Last quarter, 6 clients churned after renewal errors — $340K in lost annual premium.

## The Problem

PeakShield's policy processing is stuck in 2012. Every renewal follows the same soul-crushing workflow:

1. **Carrier sends renewal notice** (PDF or email) with updated terms, pricing, and coverage changes
2. **Operations staff manually reads** the document, identifies changes from the prior year
3. **Staff re-enters data** into Applied Epic, comparing 40+ fields across the old and new policy
4. **Broker reviews** the renewal, drafts a summary for the client
5. **Client confirms**, staff processes the binding, and documents are filed

This workflow has five structural failures that map directly to the Chapter 1 concepts:

**No perception (Section 1.1 — The Cognitive Loop).** The system has no ability to sense its environment. Renewal documents arrive in 14 different carrier formats — some as structured PDFs, some as scanned images, some as email body text. There is no automated way to extract, normalize, or interpret this information. Every document requires a human to read it, understand it, and translate it into data entry actions.

**No reasoning (Section 1.1).** When a carrier changes a deductible from $1,000 to $2,500, a human must recognize this is a material change, assess whether it affects the client's coverage adequacy, decide whether the broker needs to be alerted, and determine the urgency. This judgment happens entirely in Derek's team's heads — there's no system that reasons about what changes mean.

**No planning (Section 1.1).** A complex commercial renewal might involve 6 coverage lines, 3 sub-limits, endorsement changes, and a premium increase that triggers a client review threshold. The sequence of actions — update each line, flag the premium change, draft the client communication, schedule the broker review — is coordinated by sticky notes and tribal knowledge.

**No learning (Section 1.1).** When Carrier A changes their renewal PDF format (which happens 2-3 times per year), the entire team stumbles for a week until someone figures out where the fields moved. The same data-entry mistakes recur because there's no mechanism to learn from past errors. Knowledge walks out the door when experienced staff leave.

**No interoperability (Section 1.3 — MCP/A2A).** Applied Epic, carrier portals, email, and Excel don't talk to each other. Each system is an island. There's no universal interface for discovering what data is available, no protocol for exchanging structured messages between systems, and no way to coordinate actions across platforms.

## The Attempted Solutions

| Attempt | What happened | Chapter 1 concept it violated |
|---|---|---|
| "RPA bots for data entry" | Anika built UiPath bots that click through carrier portals. They break every time a carrier updates their UI (monthly). Maintenance cost: $8K/month. | Level 1 (Reactive) — no adaptability, no learning |
| "OCR + templates" | Bought an OCR tool to extract text from PDFs. It extracted text but couldn't understand meaning — "Deductible: $2,500" was just a string, not a material coverage change. | Missing the cognition layer — perception without reasoning |
| "Offshore processing team" | Added 12 offshore staff for data entry during renewal season. Error rate increased to 4.2%. Cost: $15K/month. | Level 0 (Manual Operations) — scaling humans, not intelligence |
| "Carrier API integrations" | Anika spent 8 months building direct API integrations with 3 carriers. Two carriers changed their APIs; one sunset theirs entirely. | No interoperability protocol — brittle point-to-point connections |

## How Chapter 1's Concepts Solve This

### 1. The Cognitive Loop — Building a Policy Processing Brain (Section 1.1)

Chapter 1's five-phase cognitive loop transforms PeakShield's manual workflow into an autonomous system:

**Perception:** The agent receives a renewal document (PDF, email, or API payload) and transforms it into structured intelligence — extracting carrier name, policy number, effective dates, coverage lines, limits, deductibles, premiums, and endorsements. This isn't OCR; it's semantic understanding. The agent recognizes that "Per Occurrence Limit" and "Each Occurrence" mean the same thing across different carriers.

**Reasoning:** The agent compares the new renewal against the existing policy in Applied Epic. It identifies every change — premium increases, coverage modifications, new exclusions — and classifies each by materiality. A $50 premium increase on a $5,000 policy is routine. A deductible change from $1,000 to $5,000 on a restaurant's liability policy is a red flag that requires broker attention.

**Planning:** For each renewal, the agent creates an action plan: update 12 fields in Applied Epic, flag the deductible change for broker review, draft a client summary highlighting the 3 material changes, and schedule a follow-up if the client hasn't responded in 5 business days. The plan adapts — if the premium increase exceeds the client's historical threshold, it adds an automatic market comparison step.

**Action:** The agent executes the plan — updating Applied Epic via API, generating the broker summary, sending the client communication through the CRM, and filing documents in the management system. Each action produces results that feed back into perception.

**Learning:** When a broker overrides the agent's materiality classification ("That deductible change is fine for this client — they self-insure small losses"), the agent updates its reasoning model. Over time, it learns client-specific preferences, broker styles, and carrier patterns.

**Impact:** The renewal that took Derek's team 45 minutes of manual work is processed in 3 minutes with 99.2% accuracy — approaching the 99.9% Quandri benchmark cited on page 34.

### 2. Agent Architecture — Communication Between Components (Section 1.2)

The book's six-layer communication architecture (Figure 1.3) maps directly to PeakShield's agent:

| Layer | PeakShield implementation |
|---|---|
| **Profile/Persona** | "You are an experienced insurance operations specialist. You process renewals with precision, flag material changes conservatively, and never guess at coverage terms." |
| **Tool Use/Action** | Applied Epic API, carrier portal scrapers, email composer, PDF generator |
| **Planning/Feedback** | Renewal action plan with dependency tracking — don't send client summary until all fields are updated |
| **Knowledge/Memory** | Client history (past renewals, preferences, claim patterns), carrier format patterns, broker-specific review thresholds |
| **Reasoning/Evaluation** | Materiality classifier, coverage adequacy checker, premium trend analyzer |
| **Cognition Core** | Central coordinator that routes each renewal through the right processing path based on complexity |

### 3. Agent Brain Patterns — Choosing the Right Architecture (Section 1.2)

Different parts of PeakShield's workflow demand different agent brain patterns from the chapter:

**Reactive agents** for high-volume, low-complexity tasks: When a carrier sends a standard renewal with no changes, the agent follows a direct stimulus-response pattern — extract, verify, update, file. No deliberation needed. This handles 40% of renewals in under 60 seconds.

**Deliberative agents** for complex renewals: When a commercial policy has coverage changes, premium increases, and new endorsements, the agent follows the Sense-Model-Plan-Act (SMPA) paradigm from Figure 1.4. It builds an internal model of the policy state, plans the update sequence considering dependencies, and executes strategically.

**Hybrid agents** for the full workflow: The layered architecture from Figure 1.5 combines both patterns. Simple renewals flow through the reactive layer. Complex renewals escalate to the deliberative layer. The reactive layer handles the data entry while the deliberative layer reasons about materiality and client impact — operating in parallel, just like the warehouse robot example in the book.

### 4. Interoperability Protocols — MCP and A2A (Section 1.3)

PeakShield's biggest technical debt is the lack of interoperability. Chapter 1's protocols solve this:

**MCP (Model Context Protocol)** provides a universal interface layer between the agent and PeakShield's tools. Instead of hardcoding integrations with each carrier portal and Applied Epic, the agent discovers available tools through capability descriptions, queries them through a standard interface, and invokes them without tool-specific logic. When Carrier A changes their API, only the MCP adapter updates — the agent's core logic doesn't change.

**A2A (Agent-to-Agent) protocols** enable the specialist agents to collaborate. The document extraction agent passes structured renewal data to the comparison agent, which passes materiality flags to the communication agent. Each agent shares state, role, and status through standardized message packets (Figure 1.7) — enabling fault tolerance and parallel processing.

### 5. The Agentic AI Progression Framework — PeakShield's Roadmap (Section 1.5)

Chapter 1's five-level progression framework (Figure 1.14) gives Janet a concrete maturity roadmap:

| Level | PeakShield today | PeakShield target |
|---|---|---|
| **Level 0: Manual** | 60% of workflow (data entry, comparison) | 5% (exception handling only) |
| **Level 1: Reactive** | RPA bots (brittle, no learning) | Standard renewal auto-processing |
| **Level 2: Tool-Using** | None | Document extraction + Applied Epic updates |
| **Level 3: Planning** | None | Complex renewal orchestration with broker coordination |
| **Level 4: Learning** | None | Continuous improvement from broker feedback and error patterns |

### 6. The Agent Development Lifecycle — Building It Right (Section 1.4)

Chapter 1's ADL (Figure 1.8) provides the development methodology:

1. **Conceptualization:** Map the cognitive workload — what decisions does Derek's team actually make? What information do they need? What constitutes "good judgment" in renewal processing?
2. **Architecture:** Choose the hybrid reactive/deliberative pattern. Design MCP adapters for each carrier. Define memory schema for client and policy history.
3. **Implementation:** Build with LangChain for tool orchestration, carrier-specific document parsers, and Applied Epic API integration.
4. **Evaluation:** Measure against the book's KPIs — task completion rate, accuracy, escalation rate, processing time, broker satisfaction.
5. **Governance:** Audit trails for every automated decision (required by provincial insurance regulators). Human-in-the-loop for materiality classifications above threshold.
6. **Iteration:** Continuous refinement from broker overrides, carrier format changes, and client feedback.

## The Revenue Impact

| Metric | Before | After | Change |
|---|---|---|---|
| Renewals processed per day | 85 (manual) | 640 (autonomous) | +653% |
| Processing accuracy | 96.8% | 99.2% | +2.4 points |
| Average processing time | 45 min | 3 min | -93% |
| Overtime cost (renewal season) | $120K/month | $15K/month | -88% |
| Client churn from processing errors | 6 clients/quarter ($340K premium) | 0 | -100% |
| Staff redeployed to client advisory | 0 | 22 (from 38) | 58% of team |
| Carrier format change recovery time | 5-7 days | <4 hours | -97% |

**Projected annual savings:** $1.6M (overtime elimination + error reduction + churn prevention). The operations team shifts from data entry to client advisory — increasing per-client revenue by 18% through proactive coverage reviews that the team never had time for before.

## What This Code Covers vs. Next Steps

### What Chapter 1's code illustrates (this notebook):
- The five-phase cognitive loop (perceive_input, reason_about_intent, create_action_plan, execute_action, learn_from_outcome)
- Reactive, deliberative, and hybrid agent brain patterns
- Communication architecture between agent components
- MCP capability description and discovery patterns
- A2A message exchange with state, role, and status packets
- The Agentic AI Progression Framework for maturity assessment

### Next steps PeakShield would need:
- **Prompt engineering for carrier-specific extraction** — Design PTCF-compliant prompts for each carrier's document format (see Chapter 3)
- **Production deployment** — Scale the agent with cost-aware routing and circuit breakers (see Chapter 4)
- **Cognitive architecture** — Build the full autonomous decision-making loop with planning and memory (see Chapter 5)
- **Document intelligence** — Advanced multi-format document parsing with OCR fallback (see Chapter 6)
- **Tool orchestration** — Connect to Applied Epic, carrier APIs, and email via function calling (see Chapter 7)
- **Multi-agent coordination** — Specialist agents for extraction, comparison, communication, and filing (see Chapter 7's chain-of-agents pattern)

---

*This use case is fictional and inspired by the Quandri case study referenced on page 34 of the book. It demonstrates how the foundational concepts in Chapter 1 — the cognitive loop, agent architecture, brain patterns, interoperability protocols, and the progression framework — apply to a realistic insurance brokerage scenario.*
