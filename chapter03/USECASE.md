# Use Case: Meridian SaaS — Engineering the Cognitive Constitution of a Billing Support Agent

**Chapter 3: The Art of Agent Prompting**
**Book: "30 Agents Every AI Engineer Must Build" by Imran Ahmad (Packt, 2026)**

---

## The Company

**Meridian SaaS** is a B2B billing and subscription management platform based in Toronto, serving 1,800 enterprise customers across North America. Their platform processes $2.1B in annual recurring revenue for clients ranging from 50-seat startups to 10,000-seat enterprises. Support team: 24 agents handling 6,200 tickets per month. Engineering: 35 developers, 4 ML engineers.

## The People

- **Nadia Volkov, VP of Customer Success** — Sponsor. Enterprise churn is at 4.8%/year, and exit interviews reveal that 62% of churning customers cite "frustrating support experience" as a factor. She has budget to build an AI support agent but her last attempt — a generic chatbot — was decommissioned after it told a Fortune 500 CFO to "just Google your invoice."
- **Jason Park, Principal ML Engineer** — Technical lead. He built a working prototype agent using GPT-4 with a basic system prompt: "You are a helpful billing assistant." It answers questions, but its behavior is erratic. Sometimes it's overly casual with enterprise executives. Sometimes it attempts to resolve issues it should escalate. It occasionally provides financial advice ("You could save money by downgrading your plan"), which the legal team flagged as unauthorized.
- **Amara Osei, Head of Support Operations** — Manages the 24-person support team. Her best agents resolve 85% of billing tickets on first contact. Her newest agents average 54%. The gap isn't product knowledge — everyone has the same training materials. The gap is judgment: knowing the right tone, the right level of detail, when to troubleshoot versus escalate, and how to structure a response that actually resolves the issue.
- **David Chen, General Counsel** — Meridian operates in financial services adjacent space. Agents cannot provide financial advice, cannot disclose other customers' data, and must comply with SOC 2 Type II requirements for data handling. Every automated customer interaction is a potential compliance event.

## The Problem

Jason's prototype agent has the knowledge but no constitution. It can answer billing questions, but it doesn't know *who it is*, *what it should do*, *where its boundaries are*, or *how it should communicate*. The result is an agent that's intermittently brilliant and intermittently dangerous.

**Five specific failures that map to Chapter 3 concepts:**

1. **Identity collapse (page 70 — Weak Persona anti-pattern).** The agent's prompt says "You are a helpful assistant." When an enterprise VP asks "Can you help me understand the tax implications of our billing structure?", the agent obliges — wandering into tax advice territory that violates Meridian's compliance rules. It has no identity to defend, no scope to enforce, no persona to anchor its behavior.

2. **Misaligned PTCF components (page 69 — Conflicting components anti-pattern).** Jason added instructions piecemeal: "Be creative and find solutions" (Persona), "Follow the escalation policy strictly" (Task), "Always respond in numbered lists" (Format). The creative persona conflicts with strict policy adherence. The agent oscillates between improvising solutions and robotically following scripts, depending on which instruction it weighs more heavily on a given turn.

3. **Missing context boundaries (page 71 — Scope Ambiguity anti-pattern).** The agent knows Meridian's product but doesn't know its operational constraints. It doesn't know it operates under SOC 2, that it must never reference other customers' data, or that it has a 4-hour SLA for Severity-1 issues. Without context, it handles a payment system outage affecting 200 enterprise customers with the same urgency as a formatting question about an invoice PDF.

4. **No few-shot calibration.** When the agent encounters a billing dispute — "We were charged $47,000 but our contract says $38,000" — it has no examples to guide its classification. Is this urgent or routine? Should it investigate or escalate? Without embedded examples showing how similar tickets were handled, every edge case triggers the same generic response.

5. **Opaque reasoning.** When the agent decides to issue a $5,000 credit, there's no reasoning trail. Amara's team can't audit why the agent made that decision, David can't prove to auditors that the decision followed policy, and Jason can't debug what went wrong when the agent makes a bad call.

## The Attempted Solutions

| Attempt | What happened | Chapter 3 diagnosis |
|---|---|---|
| "Long instruction prompt" | Jason wrote a 3,000-token system prompt with every rule he could think of. The agent followed some rules, ignored others, and contradicted itself. | No PTCF structure — rules were unorganized, priorities unclear |
| "Temperature = 0" | Set temperature to 0 to eliminate creativity. The agent became robotic and couldn't handle any question not in its training data. | Behavioral control is a prompt architecture problem, not a parameter problem |
| "Add more rules when problems occur" | Every customer complaint triggered a new rule in the prompt. After 60 rules, the prompt was 5,000 tokens and the agent spent half its context window on instructions. | Reactive rule-stacking instead of principled PTCF design |
| "Human review for everything" | Added mandatory human review for all agent responses. Resolution time went from 4 minutes to 45 minutes. | Defeated the purpose — needed targeted escalation criteria, not blanket review |

## How Chapter 3's Code Solves This

### 1. The PTCF Blueprint — From Chaos to Constitution (Section 3.2)

Chapter 3's PTCF framework (Figure 3.1) replaces Jason's ad-hoc rules with a structured cognitive contract. Each component reinforces the others:

**Persona — Who the agent is:**
```
You are a methodical enterprise billing specialist with five years
of experience in SaaS financial operations. Your communication is
professional, clear, and solution-oriented. You approach problems
with diagnostic precision and never speculate about financial
implications outside your domain.
```

This solves the identity collapse. When the VP asks about tax implications, the agent now has an identity to defend: "I'm a billing specialist, not a tax advisor. Let me connect you with our finance team for tax-specific guidance." The persona gives the agent grounds to decline — something Jason's "helpful assistant" could never do.

**Task — What the agent does:**
```
Your primary mission is to resolve enterprise billing inquiries by:
- Diagnosing billing discrepancies and system errors
- Providing step-by-step resolution guidance
- Escalating complex cases to appropriate specialists
You must not provide financial, tax, or legal advice.
```

This prevents feature creep. The agent has a defined mission with explicit boundaries. It knows its three jobs and knows what's outside its scope.

**Context — Where the agent operates:**
```
You operate within a GDPR-compliant, SOC 2 Type II-certified
environment serving enterprise clients in financial services.
You must never store, repeat, or reference personally identifiable
information in your responses. When uncertain whether an action is
compliant, default to refusal and escalate to a human reviewer.
You operate under a 4-hour SLA for Severity-1 issues.
```

This solves David's compliance concerns. The agent doesn't just know the product — it knows the rules of engagement. SOC 2 constraints, data handling restrictions, and SLA commitments are baked into its operational law.

**Format — How the agent responds:**
```
Structure all interactions as follows:
1. Acknowledge the customer's concern with empathy
2. Provide solutions in numbered, actionable steps
3. Include relevant case numbers and documentation references
4. Offer clear escalation pathways
5. End with a commitment to follow-up when appropriate
```

This ensures every response has a consistent, professional structure that Amara's team and David's compliance auditors can verify at a glance.

### 2. The Two-Layer Prompt Architecture — Constitution + Stimulus (Section 3.1)

The system prompt (PTCF above) is the agent's **constitution** — loaded once and persistent throughout every session. It defines who the agent is.

The user prompt is the **stimulus** — each incoming ticket. The key insight from page 65: the system prompt defines *how* the agent behaves; the user prompt defines *what* it should do. A billing dispute from a Fortune 500 CFO and a formatting question from a startup founder both get processed through the same constitutional framework — but with different responses appropriate to each.

In multi-agent handoffs (page 65 — the "diplomatic brief" analogy), when the billing agent escalates to a specialist agent, it passes the PTCF context along — ensuring the receiving agent inherits the same compliance constraints and communication standards.

### 3. Few-Shot Learning — Teaching by Example (Section 3.4)

Chapter 3's ticket routing case study (page 78-79) directly solves Meridian's classification problem. Jason embeds four calibration examples in the system prompt's Context component:

**Example 1 — Low urgency, routine:**
```
Input: "I am so happy with this service! Just wanted to say thanks."
Analysis: Positive sentiment, no action needed
Classification: {"Urgency": "Low", "Category": "Feedback", "Action": "None"}
```

**Example 2 — Medium urgency, billing:**
```
Input: "My bill might be incorrect, can someone look at it?"
Analysis: Polite query about billing; non-urgent
Classification: {"Urgency": "Medium", "Category": "Billing", "Action": "Route to Billing Dept."}
```

**Example 3 — High urgency, access:**
```
Input: "I can't log in, and I have a deadline in an hour!"
Analysis: Account lockout with high urgency
Classification: {"Urgency": "High", "Category": "Account Access", "Action": "Initiate Password Reset Protocol"}
```

**Example 4 — Critical, escalate:**
```
Input: "My entire system is down and I'm losing money every minute!"
Analysis: Total outage with financial impact
Classification: {"Urgency": "Critical", "Category": "Outage", "Action": "Escalate to Tier-2 Engineering"}
```

These four examples transform the agent from guessing to reasoning by analogy. When the $47,000 billing dispute arrives, the agent recognizes the pattern — financial impact claim + discrepancy + enterprise context — and classifies it correctly as High urgency / Billing / Investigate + Escalate. The examples don't just instruct; they shape cognition (page 79 — "from template to cognitive transfer").

### 4. Chain-of-Thought — Making Reasoning Visible (Section 3.5)

For complex billing disputes, the agent uses the CoT pattern from page 81-82 to reason transparently:

```
Agent thinking: "Let me first check the customer's billing history
for the last 3 months. Then, I'll compare the invoiced amount against
their contract terms. Finally, I'll determine whether the discrepancy
is a system error, a legitimate rate change, or a contract
misunderstanding."
```

This step-by-step reasoning produces an audit trail that David can show to SOC 2 auditors. Every decision has a visible logic chain — not just a conclusion, but the path that led to it.

**Impact:** When the agent issues a $5,000 credit, the reasoning trail shows: (1) pulled billing history, (2) found rate discrepancy between contract and system, (3) confirmed system error via internal lookup, (4) calculated correct amount, (5) applied credit within autonomous authority threshold. Amara can review the chain. David can prove compliance. Jason can debug the logic.

### 5. Tree-of-Thought — Parallel Reasoning for Complex Cases (Section 3.5)

For Meridian's most complex scenarios — a multi-entity enterprise with consolidated billing across 3 subsidiaries disputing charges on 7 different line items — CoT's linear reasoning isn't enough. The Tree-of-Thought pattern (Figure 3.4) explores multiple resolution paths simultaneously:

- **Path A:** Investigate as a system billing error (check each line item against contract)
- **Path B:** Investigate as a contract interpretation issue (compare master agreement vs. subsidiary addenda)
- **Path C:** Investigate as a rate change notification failure (check if price increases were communicated per contract terms)

Each path produces evidence. The agent synthesizes across all three paths to produce a comprehensive analysis: "Line items 1-3 are correct per the Q2 rate adjustment (Path C confirms notification was sent). Line items 4-5 show a system error (Path A confirms contract mismatch). Line items 6-7 require contract review by Legal (Path B identifies ambiguous subsidiary terms)."

### 6. Capability Alignment — Matching Prompt Complexity to Agent Maturity (Section 3.3)

Chapter 3's agent capability spectrum (page 73-74) guides Meridian's phased deployment:

| Level | Agent capability | Prompt pattern | Meridian deployment |
|---|---|---|---|
| **Level 1: Reactive** | Simple trigger-response | Direct commands | FAQ bot: "What's my invoice?" → instant lookup |
| **Level 2: Tool-Using** | External API access | Tool usage guidance | Billing agent: pull account data, generate statements |
| **Level 3: Planning** | Multi-step task decomposition | Structured decomposition | Dispute resolver: investigate → compare → calculate → resolve |
| **Level 4: Learning** | Feedback incorporation | Metacognitive prompts | Self-improving agent: learns from Amara's team corrections |

Jason starts at Level 2 (current prototype + PTCF fix), graduates to Level 3 (dispute resolution with CoT/ToT), and plans Level 4 (learning from human overrides) for Q3.

## The Revenue Impact

| Metric | Before (ad-hoc prompt) | After (PTCF + few-shot + CoT) | Change |
|---|---|---|---|
| First-contact resolution | 54% (new agents) / 85% (senior) | 82% (AI agent, all tickets) | +52% (vs. new agent baseline) |
| Compliance violations | 3-4/month (unauthorized advice) | 0 | -100% |
| Average response time | 12 minutes (human) / 4 min (old bot) | 90 seconds | -63% vs. old bot |
| Escalation accuracy | 61% (many false escalations) | 94% (few-shot calibrated) | +54% |
| Customer satisfaction (CSAT) | 6.8/10 | 8.6/10 | +26% |
| Enterprise churn rate | 4.8%/year | 2.9%/year | -40% |
| Audit prep time (SOC 2) | 2 weeks/quarter | 2 days (CoT audit trails) | -86% |

**Projected annual impact:** 1.9% churn reduction on $2.1B platform = $39.9M in preserved client revenue. Even attributing 10% of the retention improvement to the support agent, that's $3.99M in preserved revenue from a prompt engineering investment.

## What This Code Covers vs. Next Steps

### What Chapter 3's code demonstrates (this notebook):
- The PTCF framework (Persona, Task, Context, Format) as a structured prompt design system
- Two-layer prompt architecture (system prompt constitution + user prompt stimulus)
- Few-shot learning with embedded classification examples
- Chain-of-thought prompting for transparent, auditable reasoning
- Tree-of-thought for parallel exploration of complex problems
- Task decomposition from vague goals to structured action plans
- Capability alignment matching prompt sophistication to agent maturity
- PTCF prompt template (page 72) for rapid construction of new agent prompts

### Next steps Meridian would need:
- **Production deployment** — Cost-aware model routing and circuit breakers for the support agent (see Chapter 4)
- **Cognitive architecture** — Full perception → cognition → action loop for autonomous billing resolution (see Chapter 5)
- **Knowledge retrieval** — RAG pipeline over Meridian's product documentation and billing policies (see Chapter 6)
- **Tool integration** — Connect the agent to billing APIs, CRM, and ticketing systems (see Chapter 7)
- **Conversational memory** — Multi-turn dialog management with personality persistence (see Chapter 10)
- **Self-improvement** — Learning from Amara's team corrections to refine escalation thresholds (see Chapter 9)

---

*This use case is fictional and created for educational purposes. It demonstrates how the prompt engineering concepts in Chapter 3 — PTCF framework, few-shot learning, chain-of-thought, tree-of-thought, and capability alignment — apply to a realistic enterprise SaaS billing support scenario.*
