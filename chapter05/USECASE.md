# Use Case: ConnectWave Telecom — Building an Autonomous Customer Service Brain

**Chapter 5: Foundational Cognitive Architectures**
**Book: "30 Agents Every AI Engineer Must Build" by Imran Ahmad (Packt, 2026)**

---

## The Company

**ConnectWave Telecom** is a regional internet and business communications provider based in Ottawa, serving 180,000 residential and 22,000 commercial subscribers across Eastern Ontario and Western Quebec. Annual revenue: CAD $95M. Their support operation handles 14,000 tickets per month through a 45-person contact center running Zendesk, with a small technical team of 6 developers and 2 ML engineers maintaining internal tools.

## The People

- **Ravi Patel, VP of Customer Experience** — Sponsor. Customer satisfaction scores dropped from 82% to 71% over the past year. The board gave him a mandate: fix first-contact resolution without adding headcount. He has a $400K innovation budget for 2026.
- **Lena Dubois, Senior ML Engineer** — Technical lead. She built a proof-of-concept chatbot using LangChain and GPT-4 that can answer simple FAQ-style questions. It handles "What are your plans?" and "How do I reset my router?" well enough. But real support tickets — outages, billing disputes, service upgrades — require judgment the bot cannot make.
- **Tom Akinola, Contact Center Manager** — Oversees 45 agents across three shifts. His top performers resolve 80% of tickets on first contact, but newer agents average 52%. The gap isn't knowledge — it's decision-making. Senior agents instinctively know when to troubleshoot, when to escalate, when to offer a credit, and when to dispatch a technician. That intuition is what Lena needs to encode.
- **Suki Chen, Director of Network Operations** — Owns the monitoring stack (Datadog, PagerDuty). She's seen too many AI demos that ignore the real-time operational context. "Your chatbot doesn't know we have a fiber cut in Kanata right now. It's telling customers to reboot their router when the entire neighborhood is down."

## The Problem

ConnectWave's support experience is falling apart at the seams, and Lena's FAQ chatbot can't save it. The real problems are architectural:

1. **The bot is blind.** When a premium business customer writes "My internet has been intermittent for two days, and I have a critical presentation tomorrow," the chatbot sees text. It doesn't know this is a $2,400/year enterprise account. It doesn't know there are 47 active outage tickets in the same postal code. It doesn't know the customer called twice last week about the same issue and was promised a callback that never came. Without perception of the full operational environment, the bot gives generic advice that makes things worse.

2. **The bot can't think.** Simple tickets (password reset, plan inquiry) follow a script. But 60% of ConnectWave's tickets are complex — they require the agent to weigh multiple factors: Is this a network-wide issue or a customer-specific one? Should I troubleshoot or dispatch immediately? Is this customer at risk of churning? Should I proactively offer a service credit? Lena's chatbot has no reasoning architecture — it pattern-matches from training data and hopes for the best.

3. **The bot can't plan.** When a business customer reports intermittent service before a critical presentation, the resolution isn't a single action — it's a coordinated sequence: check service area status, identify intermittent issues in monitoring data, schedule a priority technician, upgrade the service tier temporarily, provide a mobile hotspot backup, set up proactive monitoring, and schedule a follow-up call. Each step depends on the outcome of the previous one. The chatbot can only do one thing at a time with no ability to orchestrate.

4. **The bot has no memory.** Every conversation starts from zero. The customer who called three times about the same issue has to explain everything again. The agent who resolved a tricky BGP routing problem for a similar customer last month can't transfer that knowledge. There's no learning, no personalization, no institutional memory. ConnectWave's best human agents carry years of pattern recognition in their heads — when they leave, it walks out the door with them.

5. **The bot can't learn.** When a resolution fails and the customer calls back frustrated, there's no feedback loop. When a new type of issue emerges (a firmware bug affecting a specific router model), the bot doesn't adapt. It keeps recommending the same ineffective steps until a human notices and manually updates the knowledge base, weeks later.

## The Attempted Solutions

| Attempt | What happened |
|---|---|
| "Rule-based routing" | Tom's team built a decision tree with 200+ rules mapping keywords to actions. It worked for a month, then edge cases overwhelmed it. Maintaining the rules became a full-time job. A single misclassification during an ice storm routed 400 outage tickets to the billing team. |
| "Fine-tune on ticket history" | Lena fine-tuned GPT-3.5 on 50,000 resolved tickets. The model learned to mimic agent responses but couldn't adapt to novel situations. It confidently told a customer to "check your Ethernet cable" when the issue was a regional DNS failure. Hallucination rate: 18%. |
| "Escalate everything complex" | Ravi added a rule: if the bot's confidence is below 70%, escalate to a human. But 60% of tickets triggered escalation. The human queue grew to 6-hour wait times. Customer satisfaction dropped to 68%. |

## How Chapter 5's Code Solves This

### 1. The Autonomous Decision-Making Agent — Perception, Cognition, Action (Section 5.1)

Chapter 5's core architecture replaces ConnectWave's blind chatbot with a three-stage cognitive loop that mirrors how Tom's best human agents actually think:

**Perception: From raw input to structured intelligence**

The `enhanced_perception()` function transforms a customer message from raw text into a rich situational picture:

```
Input:  "My business internet has been intermittent for two days..."
Output: {
    "message": "My business internet has been intermittent...",
    "sentiment": "frustrated",
    "user_id": "premium_business_123",
    "user_tier": "enterprise",
    "current_load": 847 active sessions,
    "time_of_day": 14 (afternoon — business hours),
    "recent_issues": ["OUTAGE-KAN-2026-0341", "OUTAGE-KAN-2026-0339"],
    "agent_availability": false (all senior agents busy)
}
```

The perception layer doesn't just read the message — it reads the situation. It pulls the customer's account tier from the CRM, checks active system alerts from Suki's Datadog feed, notes that it's business hours (higher urgency), and sees that no senior human agents are available. This is exactly what Tom's best agents do unconsciously — they scan the full context before deciding.

**Impact:** The bot now knows this is a high-value business customer affected by a known regional issue, during business hours, with no human backup available. That context changes every decision downstream.

**Cognition: Strategic reasoning for autonomous operation**

The `autonomous_reasoning()` function scores four candidate strategies and picks the best one:

- **Full autonomous resolution** — scored on autonomy level, escalation risk, and complexity
- **Immediate escalation** — scored on urgency, agent availability, and escalation threshold
- **Guided autonomous resolution** — the hybrid fallback, with human checkpoints

For the intermittent business internet case, the scoring produces: high autonomy level (well-understood issue type) + low escalation threshold (premium customer) + no agent availability = **full autonomous resolution approved**, because the alternative (waiting 2+ hours for a human) is worse for the customer.

**Impact:** The agent makes the same judgment call Tom's senior agents make — "I can handle this myself, and waiting for a human would hurt the customer more than acting now."

**Action: Autonomous execution and adaptation**

The `autonomous_action_execution()` function creates and executes a dependency-aware task DAG:

```
T1: check_service_area_status → (no dependencies)
T2: identify_intermittent_issues → (depends on T1)
T3: schedule_priority_technician → (depends on T1)
T4: upgrade_service_tier_temporarily → (depends on T2, T3)
T5: provide_mobile_hotspot_backup → (depends on T1)
T6: set_proactive_monitoring → (depends on T2)
T7: schedule_followup_call → (depends on T4, T5)
```

Each task runs only after its dependencies complete. If T1 reveals the issue is network-wide (not customer-specific), the DAG adapts — skipping individual troubleshooting and jumping to proactive notification and temporary service upgrades.

**Impact:** The customer's intermittent internet before a critical presentation triggers a coordinated 7-step response in under 90 seconds — the same workflow that takes a human agent 25 minutes to coordinate across three internal systems.

### 2. The Planning Agent — Orchestrating Complex Workflows (Section 5.2)

For ConnectWave's most complex scenarios — commercial service installations, multi-site outage coordination, infrastructure migration projects — the Planning agent provides what the Autonomous Decision-Making agent cannot: **strategic decomposition over extended time horizons**.

The architecture decomposes high-level goals into hierarchical task trees:

```
Goal: "Migrate ConnectWave's Kanata business park from copper to fiber"

Phase 1: Pre-migration assessment
  ├── Survey all 340 business accounts in the zone
  ├── Identify critical SLA accounts requiring zero-downtime migration
  ├── Schedule capacity planning with network engineering
  └── Generate customer notification timeline

Phase 2: Staged migration execution
  ├── Wave 1: Non-critical accounts (weekday evenings)
  ├── Wave 2: Standard SLA accounts (weekend maintenance window)
  └── Wave 3: Critical SLA accounts (scheduled 1:1 with dedicated tech)

Phase 3: Post-migration monitoring
  ├── Monitor error rates for 72 hours per wave
  ├── Run automated speed/latency tests per account
  └── Generate migration completion report for each customer
```

The Planning agent monitors execution feedback at each phase. When Wave 1 reveals that a specific router model requires a firmware update before fiber handoff, it automatically revises Wave 2 and Wave 3 plans to include the firmware step — without human intervention.

**Impact:** A fiber migration that previously took Suki's team 6 weeks of manual coordination is planned and monitored by the agent in real time, with human oversight only at phase gates.

### 3. The Memory-Augmented Agent — Personalized Long-Term Support (Section 5.3)

ConnectWave's most loyal customers interact with support dozens of times over years. The Memory-Augmented architecture gives the agent what Tom's senior staff carry in their heads — institutional memory.

**Working memory (short-term context):**
Within a single support session, the agent tracks the conversation flow, actions taken, and intermediate results. When the customer says "That didn't work either," the agent knows exactly which two troubleshooting steps were tried and what to try next — without asking the customer to repeat anything.

**Long-term memory (knowledge base):**
Across sessions, the agent builds a profile: this customer's router model, their typical usage patterns, past issues and resolutions, their communication preferences, their churn risk score. When the same customer calls back two weeks later, the agent opens with: "I see we upgraded your service tier temporarily on March 15th for your presentation. How has the connection been since the fiber cut in your area was repaired on March 18th?"

**Episodic memory (pattern learning):**
When a new firmware bug affects a batch of Netgear Orbi routers, the first resolution takes 45 minutes of troubleshooting. The agent stores the resolution pattern. The second customer with the same router model and symptoms gets resolved in 3 minutes — the agent recognizes the pattern and applies the known fix.

**Impact:** First-contact resolution rises from 52% (new agents) to 84% (matching senior agent performance), because every interaction benefits from the accumulated knowledge of every previous interaction.

## The Revenue Impact

| Metric | Before | After | Change |
|---|---|---|---|
| First-contact resolution | 62% (blended) | 84% | +35% |
| Average resolution time (complex tickets) | 25 minutes | 4 minutes | -84% |
| Customer satisfaction (CSAT) | 71% | 88% | +24% |
| Tickets requiring human escalation | 60% | 18% | -70% |
| Enterprise customer churn rate | 8.2%/year | 3.1%/year | -62% |
| Knowledge retention when agents leave | 0% (walks out the door) | 100% (in memory store) | — |
| Time to onboard new support agent | 6 weeks | 2 weeks (agent shadows the AI) | -67% |

**Projected annual savings:** $1.4M (reduced escalations, lower churn, faster onboarding). The $400K innovation budget pays back in 4 months. Enterprise retention improvement alone is worth $680K/year in preserved revenue.

## What This Code Covers vs. Next Steps

### What Chapter 5's code solves (this notebook):
- The perception → cognition → action cognitive loop with environmental awareness
- Autonomous strategy scoring and decision-making with escalation thresholds
- Dependency-aware task DAG execution for complex multi-step resolutions
- Planning agent architecture with hierarchical decomposition and adaptive replanning
- Memory-Augmented agent with working, long-term, and episodic memory systems
- Safety checks and guardrails for autonomous financial decisions (credit limits, data access)
- LLM integration for perception (intent classification), cognition (reasoning), and action (tool use)

### Next steps ConnectWave would need:
- **Knowledge base integration** — Build a RAG pipeline over ConnectWave's technical documentation and past ticket resolutions (see Chapter 6)
- **Tool orchestration** — Connect the action layer to Zendesk, Datadog, CRM, and dispatch systems via function calling (see Chapter 7)
- **Multi-agent coordination** — For major outage events, coordinate between customer-facing, network ops, and dispatch agents (see Chapter 7's chain-of-agents orchestrator)
- **Voice and multi-modal support** — Extend perception to handle phone calls and customer-uploaded photos of equipment (see Chapter 11)
- **Self-improving feedback loop** — Close the loop between resolution outcomes and strategy refinement (see Chapter 9's Self-Improving agent)
- **Compliance and audit trails** — Log all autonomous decisions for regulatory review, especially for automated service credits (see Chapter 4)

---

*This use case is fictional and created for educational purposes. It demonstrates how the three foundational cognitive architectures in Chapter 5 — Autonomous Decision-Making, Planning, and Memory-Augmented agents — apply to a realistic telecom customer service scenario.*
