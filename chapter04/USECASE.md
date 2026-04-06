# Use Case: NovaClaim Insurance — Deploying AI Agents at Scale

**Chapter 4: Agent Deployment and Responsible Development**
**Book: "30 Agents Every AI Engineer Must Build" by Imran Ahmad (Packt, 2026)**

---

## The Company

**NovaClaim Insurance** is a mid-market property and casualty insurer based in Toronto, processing 40,000 claims per month across auto, home, and commercial lines. Annual revenue: CAD $320M. Engineering team: 18 developers, 3 ML engineers. They run a hybrid cloud stack (AWS + on-prem) with a Django monolith handling policy administration and a React portal for adjusters.

## The People

- **Priya Mehta, VP of Claims Operations** — Sponsor. She's under board pressure to cut average claim resolution time from 11 days to 5 days without growing headcount. She approved a $1.2M AI modernization budget for 2026.
- **Daniel Okoro, Staff ML Engineer** — Technical lead. Built a proof-of-concept claims triage agent in a Jupyter notebook using GPT-4. It works beautifully in demos but has never handled real traffic.
- **Sarah Chen, Platform Engineering Lead** — Responsible for infrastructure, uptime, and security. She's skeptical — the last "AI initiative" ran up a $38K OpenAI bill in one weekend during a load test and had to be killed.
- **Marcus Williams, Chief Compliance Officer** — Needs audit trails for every automated decision. NovaClaim is regulated by FSRA (Ontario) and must demonstrate fair treatment across demographic groups.

## The Problem

Daniel's prototype agent can read a claim submission (photos, text description, policy number), classify severity, estimate payout range, and route to the right adjuster team. In the notebook it's impressive — 92% routing accuracy on historical claims.

But when Priya asks "When can we go live?", the room goes quiet. The problems:

1. **Cost explosion risk.** Each claim triggers 3–5 LLM calls (classification, extraction, estimation, routing, summary). At GPT-4 pricing, 40,000 claims/month × 5 calls = 200,000 LLM calls. Uncontrolled, this could cost $60K–$80K/month — half the annual budget on API fees alone.

2. **No resilience.** When OpenAI's API had a 47-minute outage last quarter, the prototype crashed with an unhandled exception. In production, a claims portal outage during a major storm event could strand thousands of policyholders.

3. **Security gaps.** The prototype passes raw claim text directly to the LLM. Sarah's security scan flagged prompt injection risks — a malicious claimant could craft a description that makes the agent approve a fraudulent claim or leak policy data.

4. **No audit trail.** Marcus needs to prove to regulators that automated routing decisions don't discriminate by postal code (a proxy for demographics). The prototype logs nothing.

5. **Wrong infrastructure.** Daniel deployed everything as a single Lambda function. The deliberative estimation agent regularly times out at the 15-second Lambda limit. The reactive routing agent wastes resources on a GPU instance.

## The Attempted Solutions

| Attempt | What happened |
|---|---|
| "Just add retries" | Daniel added `tenacity` retries. This helped with transient failures but caused cascading retry storms during extended outages, tripling API costs. |
| "Use GPT-3.5 for everything" | Reduced cost by 10× but routing accuracy dropped to 71%. Adjusters revolted — misrouted claims added 3 days to resolution. |
| "Manual review queue" | Priya added a human review step for all agent decisions. This defeated the purpose — resolution time went *up* to 13 days. |

## How Chapter 4's Code Solves This

### 1. Agent Typology Alignment (Section 4.1)

The `simulate_infrastructure()` function maps each of NovaClaim's agents to the right deployment target:

- **Claim Classifier** → **Reactive agent** → Serverless (AWS Lambda). Stateless, event-driven, <100ms latency, $0.002/call. Handles the high-volume initial triage.
- **Payout Estimator** → **Deliberative agent** → Container-based (ECS/Fargate). Needs 30+ seconds of reasoning, persistent context, and access to policy databases. Runs on reserved capacity.
- **Multi-Claim Coordinator** → **Multi-agent system** → Kubernetes with service mesh. Orchestrates specialist agents for complex commercial claims involving multiple parties.

**Impact:** Right-sizing infrastructure cuts compute costs by 40% and eliminates Lambda timeouts for the estimator.

### 2. Cost-Aware Model Router (Section 4.2)

The `CostTracker` class and routing logic solve the $80K/month API cost problem:

```
Simple claims (severity: low)     → GPT-3.5 Turbo  ($0.002/call)
Standard claims (severity: medium) → GPT-4o-mini    ($0.015/call)
Complex claims (severity: high)    → GPT-4          ($0.06/call)
```

The `CostTracker` enforces a budget ceiling — when monthly spend approaches the limit, the router automatically downgrades models and alerts the team. The 50-query synthetic demo in the notebook demonstrates this tiered routing with real cost accumulation.

**Impact:** Projected monthly API cost drops from $80K to $12K — an 85% reduction — while maintaining 90%+ accuracy on the complex claims that matter most.

### 3. Circuit Breaker & Resilience (Section 4.3)

The `CircuitBreaker` class implements a three-state machine (CLOSED → OPEN → HALF_OPEN) that prevents the retry storm problem:

- After 3 consecutive API failures, the breaker **opens** and stops sending requests for a cooldown period.
- During an outage, claims are queued (not dropped) and processed when the breaker transitions to **half-open** and confirms the API is back.
- The `@fail_gracefully` decorator wraps every agent call — on failure, it returns a safe fallback (e.g., "route to senior adjuster for manual review") instead of crashing.

**Impact:** During the next API outage, the claims portal stays up. Policyholders see "Your claim is being processed" instead of a 500 error. No retry storms. No cost spikes.

### 4. Microservice Pipeline (Section 4.4)

The pipeline simulation decomposes Daniel's monolithic notebook into 5 microservices:

| Service | Responsibility |
|---|---|
| Planner | Translates claim intent into action steps |
| Executor | Runs each step (classify, extract, estimate) |
| Memory Store | Persists claim context across steps |
| Tool Registry | Manages connections to policy DB, photo analysis, geocoding |
| Monitor | Tracks latency, cost, and error rates per service |

Each service communicates via structured messages, enabling independent scaling — the Executor can autoscale during storm season while the Planner stays at baseline.

### 5. Zero-Trust Security (Section 4.5)

The `InputValidator` class addresses Sarah's prompt injection concerns with three defense layers:

- **Pattern detection** — Scans claim text for known injection patterns ("ignore previous instructions", "system prompt:", encoded payloads).
- **Length limits** — Caps input at safe token thresholds to prevent context overflow attacks.
- **Output sanitization** — Validates that agent responses don't leak policy data or contain hallucinated approval codes.

The threat taxonomy covers all four attack surfaces: input layer, model layer, tool/API layer, and output layer.

**Impact:** The claims portal passes Sarah's penetration test. Prompt injection attempts are logged and blocked before reaching the LLM.

### 6. Fairness & Bias Audit (Section 4.6)

The bias auditing code generates synthetic claim decisions across demographic groups and measures disparate impact:

- **Metric:** Approval rate ratio across groups. FSRA requires the ratio to stay above 0.80 (the "four-fifths rule").
- **Monitoring:** The audit runs nightly on the previous day's decisions. If any group's approval rate drops below the threshold, an alert fires and the model is flagged for review.
- **Audit trail:** Every decision is logged with the input features, model version, confidence score, and routing outcome — satisfying Marcus's regulatory requirement.

**Impact:** NovaClaim can demonstrate fair treatment to FSRA auditors with automated reports instead of manual sampling.

## The Revenue Impact

| Metric | Before | After | Change |
|---|---|---|---|
| Average claim resolution | 11 days | 4.5 days | -59% |
| Monthly LLM API cost | $80K (projected) | $12K | -85% |
| Portal uptime during outages | 0% (crashes) | 99.9% (graceful fallback) | — |
| Routing accuracy | 92% (GPT-4 only) | 90% (tiered, cost-optimized) | -2% (acceptable) |
| Regulatory audit prep time | 3 weeks/quarter | Automated nightly | -95% |
| Adjuster productivity | 18 claims/day | 28 claims/day | +56% |

**Projected annual savings:** $1.8M (faster resolution reduces reserves, lower API costs, fewer compliance penalties). The $1.2M AI budget pays back in 8 months.

## What This Code Covers vs. Next Steps

### What Chapter 4's code solves (this notebook):
- Infrastructure selection framework for each agent type
- Cost-aware model routing with budget enforcement
- Circuit breaker and resilience patterns
- Microservice pipeline architecture
- Input validation and threat detection
- Fairness auditing and bias monitoring

### Next steps NovaClaim would need:
- **Integration with claims management system** — Connect the microservice pipeline to the existing Django backend via REST APIs
- **Photo/document processing** — Add a multimodal agent for damage photo analysis (see Chapter 11)
- **Knowledge base for policy lookup** — Build a RAG pipeline over NovaClaim's policy documents (see Chapter 6)
- **Adjuster feedback loop** — Implement a self-improving agent that learns from adjuster corrections (see Chapter 9)
- **Multi-party claim coordination** — For complex commercial claims involving multiple insurers (see Chapter 16 for multi-agent orchestration)

---

*This use case is fictional and created for educational purposes. It demonstrates how the code patterns in Chapter 4 apply to a realistic insurance deployment scenario.*
