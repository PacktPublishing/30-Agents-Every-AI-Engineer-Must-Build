# Use Case: ShieldPoint Insurance — Automating Claims with Tool Orchestration Agents

**Chapter 7: Tool Manipulation and Orchestration Agents**
**Book: "30 Agents Every AI Engineer Must Build" by Imran Ahmad (Packt, 2026)**

---

## The Company

**ShieldPoint Insurance** is a regional property and casualty insurer headquartered in Chicago, covering residential and small commercial policies across 12 Midwestern states. They process 18,000 claims per month — water damage, fire, theft, and storm-related events. Annual premium revenue: USD $480M. Their claims department has 42 adjusters, a 6-person fraud investigation unit, and a legacy claims management system built on Oracle Forms in 2011.

## The People

- **Karen Novak, SVP of Claims** — She reports to the CEO and owns the P&L for claims operations. Average claim cycle time is 12 days. The board wants it under 5 days by Q4 2026 to match InsurTech competitors. She has budget for technology but not for 20 more adjusters.
- **Raj Patel, Senior Data Scientist** — Built a proof-of-concept claims triage model in a Jupyter notebook. It classifies claims by severity and estimates payout ranges. Accuracy is strong but it's a standalone script — no workflow integration, no human checkpoints, no audit trail.
- **Lisa Dominguez, Fraud Unit Lead** — Her team manually reviews ~2,200 flagged claims per month. She needs automated risk scoring to focus her team on truly suspicious cases instead of reviewing every claim over $10,000.
- **Tom Bradley, Chief Compliance Officer** — State regulators require ShieldPoint to demonstrate consistent, auditable decision-making. The current process has no centralized log of why a claim was approved, escalated, or denied. Tom failed a regulatory spot-check last quarter because adjusters documented decisions inconsistently.

## The Problem

ShieldPoint's claims process is a patchwork of manual steps:

1. **Intake** — A claimant calls or files online. A clerk manually enters the claim into Oracle Forms, often re-typing information from photos and PDFs. Error rate: 8%.
2. **Validation** — An adjuster checks policy status by looking up the account in a separate system. Expired policies sometimes slip through — ShieldPoint paid $340K on invalid claims last year.
3. **Risk assessment** — No systematic risk scoring. Every claim over $10,000 goes to the fraud unit, regardless of actual risk indicators. This floods Lisa's team with low-risk, high-value claims (kitchen renovations, roof replacements) while genuinely suspicious claims with address mismatches or new-customer + high-value patterns get the same treatment.
4. **Payout** — Approved claims wait in a payment queue. Average time from approval to payment: 4 days. Claimants call to ask "Where's my check?" — these calls cost $12 each in call center time.
5. **Audit** — Tom's compliance team reconstructs decision history from adjuster notes, emails, and Oracle Forms timestamps. It takes 3 weeks to prepare for a regulatory review.

**The bottom line:** 12-day average cycle time, $340K/year in invalid claim payouts, a fraud unit drowning in false positives, and a failed compliance audit.

## The Attempted Solutions

| Attempt | What happened |
|---|---|
| RPA (Robotic Process Automation) | Automated data entry from forms into Oracle. Reduced intake errors to 3% but did nothing for risk assessment, escalation, or audit trails. Still no intelligence in the process. |
| Rules engine for fraud flagging | IT built 47 if/then rules. Too rigid — legitimate large claims triggered false positives constantly. Lisa's team workload actually increased because now they had to review rule-flagged claims AND their own investigations. |
| Outsourced AI vendor | A vendor offered a "black box" claims AI. Tom rejected it — no explainability, no audit trail, and the vendor couldn't demonstrate how decisions were made. Regulators would never accept it. |

## How Chapter 7's Code Solves This

Chapter 7 builds three progressively complex agent patterns. ShieldPoint uses all three:

### Pattern 1: Tool-Using Agent — Campaign Analytics (Section 7.1–7.3)

Before touching claims, Raj uses the Tool-Using Agent pattern to prove the architecture works on a lower-risk problem: marketing campaign analytics.

The **data visualization agent** demonstrates the Think/Plan/Act cycle:
- **Think:** Parse a natural language query ("Show me spend by campaign") into structured intent (metric=spend, dimension=campaign_name, chart_type=bar)
- **Plan:** Construct a tool sequence — `load_csv` → `group_by_and_aggregate` → `plot_bar_chart`
- **Act:** Execute tools in order, passing data state between them

The **Tool Registry** provides a centralized catalog of available functions with input/output schemas and status flags. This registry pattern becomes the foundation for the claims system — every capability (validate policy, score risk, process payment) is registered as a discoverable tool.

The **deliberate failure demos** show that when a file doesn't exist or a column is wrong, the `@graceful_fallback` decorator catches the error, logs it, and returns a safe default — no crash, no unhandled exception. Karen sees this and says: "That's what I need for claims. It can't crash during a storm event when we're processing 3× normal volume."

### Pattern 2: Chain-of-Agents — Market Intelligence (Section 7.4–7.6)

The **ManagerAgent** orchestrates three specialist agents (NewsAgent, FinancialAgent, SentimentAgent) using a cooperation protocol. Each agent:
- Declares its role and output format
- Executes independently
- Reports status back to the manager

The **episodic memory** logs every agent interaction with timestamps — this becomes the blueprint for ShieldPoint's claims audit trail.

The **conflict resolution** system detects when agents disagree (e.g., positive sentiment but negative stock movement, conflict score > 0.5). For ShieldPoint, this translates to: when the automated risk score says "low risk" but the claim has known fraud indicators, flag the conflict and escalate.

### Pattern 3: Agentic Workflow — Claims Processing (Section 7.7)

This is the core of ShieldPoint's solution. The code implements a **5-agent state machine** with guard conditions and HITL gates:

**Agent 1: Intake Agent**
Digitizes the claim submission and extracts structured fields (claim ID, policy ID, claim type, amount, description). Replaces the manual clerk entry step.

**Agent 2: Validator Agent**
Checks the policy database automatically:
- Is the policy active? (Catches the $340K expired-policy problem)
- Is there a fraud flag on the account?
- Does the policy exist at all?

If validation fails, the claim transitions directly to **Closed: Rejected** — no adjuster time wasted.

**Agent 3: Classifier Agent**
Scores every claim with a confidence score (0.0–1.0) and risk level:

```
Water damage, $8,400  → confidence: 0.91, risk: low   → auto-approve
Fire damage, $47,000  → confidence: 0.79, risk: high  → escalate to human
```

The threshold is 0.85 — claims above it proceed automatically, claims below it go to HITL review. This replaces the crude "$10K = fraud review" rule with actual risk intelligence.

**Agent 4: Escalation Agent (HITL Gate)**
When the classifier's confidence is below threshold, the workflow pauses and routes to a human reviewer. The reviewer sees the claim details, risk score, and reason for escalation, then approves or rejects.

In simulation mode, this auto-approves after a 2-second delay — enabling ShieldPoint to test the entire pipeline headlessly without human interaction.

**Agent 5: Payout Agent**
Processes the settlement payment and records the transaction.

### The State Machine

The workflow is modeled as an explicit state graph with 8 states:

```
Start → Intake → Validating → Assessing Risk → Processing Payout → Closed: Approved
                      ↓              ↓
               Closed: Rejected   Pending Human Review
                                      ↓
                               Processing Payout → Closed: Approved
```

**Guard conditions** gate every transition:
- Validation must pass before risk assessment begins
- Confidence must be ≥ 0.85 to skip human review
- Human must explicitly approve before payout proceeds

**Audit trail** logs every state transition with the reason:
```
Intake → Validating          "All fields populated"
Validating → Assessing Risk  "Policy POL-992317 active, no fraud flag"
Assessing Risk → Payout      "Confidence 0.91 ≥ 0.85 threshold"
Payout → Closed: Approved    "Settlement $8,400 processed"
```

Tom can pull this audit trail for any claim in seconds — no more 3-week reconstruction.

## The Three Test Claims

The code demonstrates three scenarios that mirror ShieldPoint's actual claim mix:

| Claim | Type | Amount | Risk | Path | Outcome |
|---|---|---|---|---|---|
| CLM-4821 | Water damage | $8,400 | Low (0.91) | Auto-approve | Closed: Approved in < 1 minute |
| CLM-5099 | Fire damage | $47,000 | High (0.79) | HITL escalation → human approves | Closed: Approved after review |
| CLM-5100 | Theft | $3,200 | N/A | Rejected at validation (expired policy) | Closed: Rejected in 5 seconds |

## The Revenue Impact

| Metric | Before | After | Change |
|---|---|---|---|
| Average claim cycle time | 12 days | 3.5 days | -71% |
| Invalid claim payouts | $340K/year | ~$20K/year | -94% |
| Claims auto-approved (no human touch) | 0% | 55% | — |
| Fraud unit review volume | 2,200/month | 650/month | -70% |
| Regulatory audit prep time | 3 weeks | Real-time (automated trail) | -95% |
| Claimant "where's my check" calls | 4,800/month | 1,200/month | -75% |
| Call center savings | — | $43K/month | — |

**Projected annual savings:** $1.6M (reduced invalid payouts + call center savings + adjuster productivity + compliance automation). The technology investment pays back in 7 months.

## What This Code Covers vs. Next Steps

### What Chapter 7's code solves:
- Tool registry pattern for discoverable, composable agent capabilities
- Think/Plan/Act cycle for single-agent tool use
- Multi-agent cooperation protocol with episodic memory and conflict detection
- State machine workflow with guard conditions and HITL gates
- Full audit trail for every claim decision
- Resilience patterns — `@graceful_fallback`, `safe_invoke()`, exponential backoff
- Dual-mode operation (Simulation + Live LLM)

### Next steps ShieldPoint would need:
- **Document intelligence** — OCR and NLP for extracting data from claim photos, repair estimates, and police reports (see Chapter 6 for RAG-based document agents)
- **Cost-aware model routing** — Route simple claims through cheaper models, complex claims through GPT-4 (see Chapter 4 for CostTracker and tiered routing)
- **Fraud pattern learning** — A self-improving agent that learns from Lisa's fraud unit decisions over time (see Chapter 9 for self-improving agents)
- **Claimant-facing chatbot** — Conversational agent for status updates and document submission (see Chapter 10 for conversational agents)
- **Multi-party coordination** — For commercial claims involving contractors, adjusters, and reinsurers (see Chapter 16 for multi-agent orchestration)
- **Fairness monitoring** — Ensure claim decisions don't discriminate by geography or demographics (see Chapter 12 for ethical and explainable agents)

---

*This use case is fictional and created for educational purposes. It demonstrates how the code patterns in Chapter 7 apply to a realistic insurance claims automation scenario.*
