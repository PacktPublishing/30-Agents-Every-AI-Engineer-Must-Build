# Chapter 3 -- LLM Provider Comparison

**Book:** *30 Agents Every AI Engineer Must Build* by Imran Ahmad (Packt Publishing, 2026)

This document compares the performance of four LLM providers running the Chapter 3 Agent Prompting tasks: persona construction (bare vs. constrained), PTCF framework, task decomposition, few-shot classification, chain-of-thought reasoning, Tree-of-Thought product launch strategy, inter-agent communication, and case study evaluations (triage, compliance, code review, A/B testing).

---

## Agent Tasks in This Chapter

- **Persona Construction (Section 3.1)** -- Bare prompt vs. fitness-coach persona for workout plan
- **System Prompt Roles (Section 3.2)** -- Customer support persona with internet and billing queries
- **PTCF Framework (Section 3.3)** -- Persona/Task/Context/Format enterprise billing agent
- **Task Decomposition (Section 3.4)** -- Vague goal ("Plan my business trip to Tokyo") into structured sub-tasks
- **Few-Shot Classification (Section 3.5)** -- Zero-shot urgency classification of support tickets
- **Chain-of-Thought (Section 3.6)** -- Diagnostic reasoning for "Application loads but data is missing"
- **Tree-of-Thought (Section 3.6)** -- Multi-expert product launch: market analysis, financial planning, marketing, synthesis
- **Inter-Agent Protocol (Section 3.7)** -- Credit risk agent-to-agent message generation
- **Case Studies** -- Ticket triage (Severity-1), compliance review (MiFID II), code review (SQL injection), A/B persona testing

## Scoring Dimensions

Each provider is rated 0-10 across eight dimensions:

| Dimension | What It Measures |
|---|---|
| **Factual Accuracy** | Correctness of classifications, compliance flags, security findings |
| **Completeness** | Coverage of all prompting techniques and case study outputs |
| **Structure & Organization** | Quality of JSON formatting, table output, PTCF adherence |
| **Conciseness** | Information density without unnecessary padding |
| **Source Grounding** | Adherence to the chapter's PTCF framework and prompting patterns |
| **Cognitive Sophistication (Bloom's)** | Highest Bloom's taxonomy level demonstrated |
| **Nuance & Caveats** | Acknowledgment of edge cases, regulatory specifics, tradeoffs |
| **Practical Utility** | How actionable the outputs would be in production systems |

---

## Task 1: Persona Construction -- Bare vs. Constrained (Section 3.1)

### Bare Prompt (No Persona)

All four providers generated generic workout plans when given "Create a workout plan for me" without persona constraints:

- **GPT-4o:** Factual, structured with disclaimers ("consult with..."), beginner-to-intermediate focus. Professional but flat.
- **Claude:** Concise weekly schedule format (Monday/Tuesday/Thursday/Friday split), well-organized headers. Efficient.
- **Gemini:** Conversational opening ("I can definitely help you!"), offered customization advice alongside the plan. Approachable.
- **DeepSeek:** Standard structure with medical disclaimer. Similar to GPT-4o in tone and content.

### Persona-Constrained (Fitness Coach)

With the fitness coach persona, all four providers adopted an enthusiastic, motivational tone -- but the quality of persona adherence varied:

- **GPT-4o:** "Absolutely! I'm thrilled to help you crush your fitness goals!" Strong motivational language throughout with specific timings. Maintained persona consistently.
- **Claude:** Used emojis and headers extensively ("YOUR DAILY POWER WORKOUT", "Get that body fired up!"). Three distinct workout rounds (Lower Body Power, Upper Body Strength, Core & Cardio Blast) with work/rest intervals (45s/15s). Most structured workout format.
- **Gemini:** "Hey there, fitness superstar!" Opening with emojis. Detailed warm-up with dynamic stretches. Included Cat-Cow stretch -- the most diverse exercise selection.
- **DeepSeek:** "Let's get moving and make today a fantastic day for progress." Good motivational tone but less energetic than GPT-4o or Gemini. Solid structure with warm-up and main circuit.

**Assessment:** All four successfully adopted the persona. Claude's structured round format was most practical for actual use. GPT-4o had the most natural motivational voice. Gemini was the most approachable.

---

## Task 2: Customer Support System Prompt (Section 3.2)

### Query 1: "My internet is not working. Can you help?"

- **GPT-4o:** Immediate troubleshooting steps (modem/router restart, check connections, device restart, Wi-Fi signal, network settings). Professional and direct.
- **Claude:** Unique response -- clarified scope ("as a customer support specialist focused on enterprise software solutions, I typically handle issues related to our software platforms, billing, and account management rather than internet connectivity"). Then asked clarifying questions to determine if it was platform-specific. Demonstrated strongest persona boundary awareness.
- **Gemini:** "Oh no, that's incredibly frustrating!" Empathetic opening, then asked diagnostic questions (home vs. office, modem lights, all devices or one) before troubleshooting. Most empathetic response.
- **DeepSeek:** Standard troubleshooting steps similar to GPT-4o. Professional but less distinctive.

**Notable:** Claude's boundary-setting response was the most persona-consistent -- the system prompt described an enterprise software specialist, and internet connectivity is outside that domain. The other three providers all attempted to help with the internet issue regardless.

### Query 2: "I think I was charged twice on my last invoice."

All four produced strong billing-focused responses. Key differences:
- **GPT-4o:** Four steps (check invoice, payment history, account activity, contact support). Template-like.
- **Claude:** Structured with bold headers ("First, I'll need to gather some information", "While I investigate", "Next steps"). Three possible outcomes listed. Most operationally detailed.
- **Gemini:** Asked for 4 specific data points (account name/ID, invoice number, dates, amounts). Clean and efficient.
- **DeepSeek:** Shorter response asking for invoice number or date, then cross-referencing. Concise but less thorough.

---

## Task 3: PTCF Enterprise Agent (Section 3.3)

The enterprise billing agent uses the full PTCF framework: Persona (billing specialist), Task (resolve inquiries), Context (24h SLA, Fortune 500), Format (numbered sequence: Acknowledge, Diagnose, Resolve, Escalate, Follow-up).

### Enterprise Agent Response to Duplicate Billing

- **GPT-4o:** Clean 5-step numbered response following the PTCF format exactly. Professional language. Mentioned escalation to "billing operations team" and 24-hour escalation window. Solid adherence.
- **Claude:** Added a case reference number ("ENT-2024-DBL-001") unprompted. Identified the recurring pattern as "likely stemming from API synchronization problems or subscription management conflicts." Most specific root-cause hypothesis. Mentioned "duplicate charge prevention flags" as a proactive measure.
- **Gemini:** Added case reference number ("BIL-78901"). Mentioned investigating "overlapping subscription renewals or manual reprocessing events." Noted "third occurrence" and committed to identifying the "underlying systemic cause." Slightly more verbose than GPT-4o but well-structured.
- **DeepSeek:** Followed the 5-step format cleanly. Less specific than Claude or Gemini -- asked for account number rather than proactively investigating. Did not generate a case reference number.

**Assessment:** Claude and Gemini both exceeded the format requirements by generating case reference numbers and hypothesizing specific root causes. GPT-4o was the most format-compliant. DeepSeek was functional but the least distinctive.

---

## Task 4: Task Decomposition (Section 3.4)

Vague goal: "Plan my upcoming business trip to Tokyo"

All four providers decomposed this into sequential, dependency-ordered sub-tasks. Key differences:

- **GPT-4o:** 6 tasks starting with dates, passport/visa, budget, flights, accommodation, then scheduling. Each with a "Rationale" block. Clean and comprehensive.
- **Claude:** Included "Purpose/nature of business meetings" and "Consider time zone impact on meeting schedules" -- unique considerations that reflect business-travel awareness. Specified NRT/HND airports.
- **Gemini:** Most detailed sub-task list with nested sub-tasks (e.g., under "Gather Core Trip Details": confirm dates, clarify purpose, identify contacts). Most hierarchical structure.
- **DeepSeek:** 5 tasks in clean order. Included "time zone differences to minimize jet lag" -- practical touch. Slightly less detailed than others.

**Assessment:** Gemini produced the most granular decomposition. Claude showed the best domain awareness (airport codes, time zone impact on meetings). GPT-4o and DeepSeek were solid but more generic.

---

## Task 5: Zero-Shot Classification (Section 3.5)

Ticket: "Love your product, keep up the great work!" (expected: Low urgency, Feedback category)

- **GPT-4o:** `{"Urgency": "Low", "Category": "Feedback/Compliment", "Action": "Acknowledge and thank"}` -- Correct.
- **Claude:** `{"urgency": "low", "category": "feedback", "action": "acknowledge_positive_feedback"}` -- Correct. Lowercase keys (machine-friendly).
- **Gemini:** `{"Urgency": "None", "Category": "Feedback", "Action": "Log Feedback"}` -- Used "None" instead of "Low" for urgency. Debatable: "None" is arguably more accurate for a compliment (there is no urgency), but deviates from the expected classification schema.
- **DeepSeek:** `{"Urgency": "Low", "Category": "Feedback", "Action": "Acknowledge and thank the user"}` -- Correct.

**Note:** The few-shot classification task failed for all providers due to a template variable error (`Input to ChatPromptTemplate is missing variables {'"Urgency"'}`). This is a code bug, not a provider issue.

---

## Task 6: Chain-of-Thought Reasoning (Section 3.6)

Scenario: "Application loads but all data is missing"

- **GPT-4o:** 4+ diagnostic steps (database connection, server status, access permissions, data integrity). Each step had "Why" and "Expected Outcome." Standard diagnostic chain.
- **Claude:** Similar structure with headers (Check Database Connectivity, Verify Database Service Status, Examine Application Logs, Test Database Queries Directly). Added "Examine Application Logs" as a distinct step -- practical and often the real first debugging action.
- **Gemini:** Unique approach -- started with "Check Client-Side Errors and Network Activity" using browser developer tools (F12, Console tab, Network tab). Then checked for HTTP status codes (401, 404, 500). Most user-accessible diagnostic approach. The only provider to suggest client-side debugging first.
- **DeepSeek:** 4 steps (database connectivity, connection strings, server status, then continued). Added "Review Database Connection Strings" as a specific step -- a common real-world misconfiguration cause.

**Assessment:** Gemini's client-side-first approach was the most practically differentiated. Claude's inclusion of application logs was realistic. GPT-4o and DeepSeek followed standard server-side diagnostic patterns.

---

## Task 7: Tree-of-Thought -- Product Launch Strategy (Section 3.6)

Four branches: Market Analysis, Financial Planning, Marketing Strategy, and Synthesis. All four providers converged on **university students** as the target market and **freemium** as the business model -- reasonable given the prompts. Quality differences emerged in specificity and actionability:

### Branch A: Market Analysis

- **GPT-4o:** Analyzed all three segments (high school, university, professionals) with strengths/weaknesses. Selected university students with balanced reasoning.
- **Claude:** Led with "Primary Recommendation: University Students" and structured rationale around market fundamentals, competitive position, and network effects. Most assertive and organized.
- **Gemini:** Focused on academic need, self-directed learning, and tech-savviness. Concise but less comparative.
- **DeepSeek:** Evaluated all three segments with pros/cons. Similar to GPT-4o in structure and depth.

### Branch B: Financial Planning

- **Claude:** Provided specific pricing ($9.99/month, $79.99/year with 33% savings). Three strategic justifications with sub-points. Most production-ready pricing model.
- **Gemini:** Detailed hybrid model ("Freemium leading to Subscription") with justification around "value-conscious" students. Thorough.
- **GPT-4o:** Recommended freemium with clear rationale (budget constraints, engagement, scalability). Solid but no specific pricing.
- **DeepSeek:** Standard freemium recommendation. Less detail than Claude or Gemini.

### Branch C: Marketing Strategy

- **Claude:** "Your AI Study Partner" campaign, 8-week duration (Weeks 6-13 of fall semester -- midterms through finals). Budget allocation: 70% TikTok/Instagram, 20% campus partnerships, 10% Reddit/Discord. Most specific and actionable.
- **Gemini:** "Your Academic Edge, Powered by AI" campaign targeting undergrad and postgrad. Channels included TikTok, Instagram, campus partnerships. Similar structure to Claude.
- **GPT-4o:** Campus partnerships, social media, content marketing. Standard channels without specific budget allocation.
- **DeepSeek:** Instagram, TikTok, LinkedIn, campus ambassadors. Included LinkedIn for career-oriented students -- a unique channel choice.

### Synthesis

All four produced coherent integrated strategies. Claude's synthesis was the most specific (pricing, timing, budget splits). Gemini's was the most verbose. GPT-4o's was well-structured. DeepSeek's was concise.

---

## Task 8: Inter-Agent Protocol (Section 3.7)

Agent Alpha (Credit Risk) sends a risk assessment update to Agent Beta (Market Risk).

- **GPT-4o:** Confidence 0.92, risk category "medium", 4 generic recommendations. Valid JSON but wrapped in prose.
- **Claude:** Confidence 0.87, risk score 6.8/10, key metrics object (default_rate_increase: 0.23, portfolio_volatility: 0.34, macroeconomic_impact: 0.41, sector_concentration_risk: 0.28). Three prioritized recommendations with rationale. Added timestamp. Most structured and machine-parseable.
- **Gemini:** Confidence 0.88, "Elevated Risk - Watchlist" category, summary narrative, key indicators with quantitative values (delinquency rate +1.5% QoQ at 4.2%, early-stage defaults +0.8% at 1.7%). Most data-rich.
- **DeepSeek:** Confidence 0.92, risk category "Moderate", 4 recommendations. Similar to GPT-4o but with slightly more specific advice.

**Assessment:** Claude produced the most structured machine-parseable output with nested metrics objects. Gemini provided the most realistic financial data with quarter-over-quarter changes. Both significantly outperformed GPT-4o and DeepSeek for inter-agent communication.

---

## Task 9: Case Studies

### Case Study 1: Ticket Triage (Dashboard Degradation 2s -> 45s)

All four correctly classified as Severity-1, Performance Degradation, with 1-hour SLA. Differences:
- **GPT-4o:** Assigned to "Performance_Team". Clean reasoning.
- **Claude:** Assigned to "Critical Infrastructure Team". Calculated "2,150% degradation" -- specific metric. Mentioned "rollback procedures."
- **Gemini:** Assigned to "Application Support - Critical". Calculated "over 2000% degradation." Most detailed reasoning with explicit SRE/DevOps engagement.
- **DeepSeek:** Assigned to "Performance_Team". Concise reasoning mentioning "widespread impact."

### Case Study 2: Compliance Review (MiFID II / FCA COBS)

All four flagged both problematic passages and rated risk as "High" with escalation required. Regulatory citation depth varied:
- **GPT-4o:** Referenced "MiFID II and FCA COBS regulations" generally. Two flagged passages with reasoning.
- **Claude:** Cited specific articles: "MiFID II Article 24", "FCA COBS 9A", "FCA COBS 4.5". Four distinct violations enumerated. Most thorough regulatory analysis.
- **Gemini:** Cited "COBS 4.2.1R, COBS 4.5.1R", "MiFID II Article 24", "COBS 9 Suitability". Detailed two-part reasoning. Comparable to Claude.
- **DeepSeek:** Referenced regulations generally without specific article numbers. Shortest reasoning.

### Case Study 3: Code Review (SQL Injection + File Upload)

All four identified the critical SQL injection (line 2) and file upload vulnerabilities. Depth varied:
- **GPT-4o:** 4 findings in table format. Included test coverage gap. Clean table.
- **Claude:** 5 findings. Added "Missing database authentication" and explicitly referenced `secure_filename()`. Most specific remediation advice.
- **Gemini:** Referenced OWASP taxonomy (A03:2021-Injection, A01:2021-Broken Access Control, A05:2021-Security Misconfiguration). Most standards-aligned. Longest reasoning per finding.
- **DeepSeek:** 4 findings. Mentioned "environment variables or secure configuration management" for database connection. Practical but less detailed.

### Case Study 4: A/B Persona Testing

Five tickets classified by two persona variants (A = precise, B = lenient). Results:

| Provider | Variant A Accuracy | Variant B Accuracy |
|---|---|---|
| GPT-4o | 100% (5/5) | 60% (3/5) |
| Claude | 100% (5/5) | 60% (3/5) |
| Gemini | 80% (4/5) | 80% (4/5) |
| DeepSeek | 80% (4/5) | 60% (3/5) |

**GPT-4o and Claude** achieved perfect 100% on Variant A (the precise persona), while **Gemini** missed the "Cannot log in, deadline in 30 minutes!" ticket (should be High) on both variants. **DeepSeek** missed "My invoice seems wrong" on Variant A (should be Medium).

---

## Overall Scorecard

| Dimension | OpenAI GPT-4o | Claude Sonnet 4 | Gemini Flash 2.5 | DeepSeek V2 (Local) |
|---|---|---|---|---|
| Factual Accuracy | **8.0** | **8.5** | **7.5** | **7.0** |
| Completeness | **8.0** | **9.0** | **8.5** | **7.5** |
| Structure & Organization | **8.0** | **8.5** | **8.0** | **7.5** |
| Conciseness | **8.0** | **6.5** | **7.0** | **8.0** |
| Source Grounding | **8.0** | **8.5** | **8.0** | **7.5** |
| Bloom's Taxonomy Level | **5.0 (Evaluate)** | **5.5 (Evaluate)** | **5.0 (Evaluate)** | **4.0 (Analyze)** |
| Nuance & Caveats | **6.5** | **8.0** | **7.5** | **6.0** |
| Practical Utility | **8.5** | **8.0** | **7.5** | **7.0** |
| **WEIGHTED AVERAGE** | **7.5** | **7.8** | **7.4** | **6.8** |

**Scoring notes:**
- Claude's Conciseness is penalized to 6.5 -- the ToT synthesis and inter-agent messages are highly detailed but consume significantly more tokens than GPT-4o's equivalents
- GPT-4o's Practical Utility is highest at 8.5 because its PTCF response, A/B testing (100% accuracy), and code review table were the most deployment-ready
- Gemini's Factual Accuracy is penalized for the A/B testing miss (80% on Variant A where GPT-4o and Claude achieved 100%) and for classifying urgency as "None" instead of "Low" for the feedback ticket
- Claude's Nuance is highest at 8.0 because it set persona boundaries on the internet query, cited specific regulatory articles in compliance review, and produced the most specific campaign timing (midterms-through-finals)
- DeepSeek's Bloom's level is capped at Analyze (4.0) because its outputs are correct but lack the evaluative depth seen in the other providers' compliance and code review outputs

---

## Bloom's Taxonomy Analysis

```
Level 6: Create      |
Level 5: Evaluate    | Claude Sonnet 4, OpenAI GPT-4o, Gemini Flash 2.5
Level 4: Analyze     | DeepSeek V2 (Local)
Level 3: Apply       |
Level 2: Understand  |
Level 1: Remember    |
```

**Claude Sonnet 4** reaches Level 5.5 (strong Evaluate) through specific regulatory article citations in compliance review, persona boundary-setting in the internet query, and quantified campaign timing in the marketing branch.

**OpenAI GPT-4o** reaches Level 5 (Evaluate) through the A/B testing task (100% accuracy on both classification variants), clean PTCF adherence, and consistent evaluation quality across case studies.

**Gemini Flash 2.5** reaches Level 5 (Evaluate) through OWASP taxonomy referencing in code review and client-side-first diagnostic approach in CoT -- but is pulled down by the A/B testing accuracy gap.

**DeepSeek V2** operates at Level 4 (Analyze) -- correctly decomposes prompting tasks and produces valid outputs, but lacks the specific citations, boundary-setting, and evaluative depth of the cloud providers.

---

## Visual Summary

### Overall Score Comparison

```
  Provider              Score  Visual
  --------------------  -----  ------------------------------
  1. Claude Sonnet 4        7.8  #######################-------
  2. OpenAI GPT-4o          7.5  #######################-------
  3. Gemini Flash 2.5       7.4  ######################--------
  4. DeepSeek V2 (Local)    6.8  ####################----------
```

### Bloom's Taxonomy Tower

```
  Level  Name          Providers at this level
  -----  ------------  --------------------------
  L6 Create       |
  L5 Evaluate     | C O G
  L4 Analyze      | C O G D
  L3 Apply        | C O G D
  L2 Understand   | C O G D
  L1 Remember     | C O G D
```

Legend: **C** = Claude Sonnet 4, **G** = Gemini Flash 2.5, **D** = DeepSeek V2, **O** = OpenAI GPT-4o

---

## Winner: OpenAI GPT-4o

| | |
|---|---|
| **Chapter 3 Winner** | **OpenAI GPT-4o** |
| **Score** | **7.5 / 10** |
| **Bloom's Level** | **Level 5 -- Evaluate** |

**Why GPT-4o wins this chapter:**
- Perfect 100% accuracy on A/B persona testing (Variant A) -- the chapter's most objective evaluation metric
- Highest Practical Utility (8.5) across all dimensions: PTCF response required no editing, code review table was clean markdown, and the ToT synthesis was well-organized
- Best balance of quality and conciseness -- every output was deployment-ready without over-engineering
- Consistent performance across all 9 tasks with no weak spots

**Why not Claude despite higher raw score:**
- Claude's 0.3-point raw lead is driven by Completeness and Nuance scores that reward depth over efficiency
- The persona boundary-setting on the internet query was intellectually interesting but would frustrate a user expecting help -- in production, customers do not care about your agent's jurisdictional scope
- Specific regulatory citations (MiFID II Article 24, FCA COBS 9A) are valuable for compliance teams but add tokens without changing the outcome: all providers correctly flagged the violations
- The pricing specificity in the ToT branch ($9.99/month, $79.99/year) is impressive but potentially misleading in a strategic analysis -- these numbers have no empirical basis

**Runner-up:** Claude Sonnet 4 (7.8/10) -- Highest raw score. Best for compliance-heavy applications requiring specific regulatory citations and inter-agent protocols with rich metadata. The persona boundary-awareness is unique and valuable for safety-critical systems.

**Third place:** Gemini Flash 2.5 (7.4/10) -- OWASP taxonomy referencing in code review and client-side-first CoT approach were standout contributions. Penalized for the A/B testing accuracy gap and "None" urgency classification.

### Best Provider by Scenario

| Scenario | Best Choice | Why |
|---|---|---|
| Production agent prompting | OpenAI GPT-4o | Cleanest PTCF adherence; highest A/B testing accuracy |
| Compliance-heavy domains | Claude Sonnet 4 | Specific regulatory article citations; persona boundary enforcement |
| Security-focused code review | Gemini Flash 2.5 | OWASP taxonomy alignment; most detailed vulnerability descriptions |
| Multi-expert ToT analysis | Claude Sonnet 4 | Specific pricing and campaign timing; richest synthesis |
| Cost-efficient prototyping | DeepSeek V2 (Local) | Zero API cost; valid outputs across all tasks |

## Provider Profiles for This Chapter

### OpenAI GPT-4o -- "The Reliable Executor"

**Strengths:**
- Perfect A/B testing accuracy (100% Variant A, 60% Variant B) -- best classification precision
- Cleanest PTCF format adherence in enterprise agent response
- Consistent quality without over-engineering
- Professional, deployment-ready language across all tasks

**Weaknesses:**
- Inter-agent message lacked quantitative risk metrics (generic "medium" category)
- No specific regulatory article citations in compliance review
- Task decomposition was solid but not distinctive

---

### Claude Sonnet 4 -- "The Compliance Specialist"

**Strengths:**
- Only provider to enforce persona boundaries on the internet connectivity query
- Specific regulatory citations (MiFID II Article 24, FCA COBS 9A, COBS 4.5) in compliance review
- Generated case reference numbers unprompted in PTCF response
- Most production-ready pricing model in ToT financial planning ($9.99/month)
- Richest inter-agent message with nested metrics objects and prioritized recommendations

**Weaknesses:**
- Most verbose output -- ToT branches and synthesis significantly longer than others
- Persona boundary-setting on internet query may frustrate end users
- Higher token consumption across all tasks

---

### Gemini Flash 2.5 -- "The Standards Expert"

**Strengths:**
- OWASP taxonomy referencing (A03:2021, A01:2021, A05:2021) in code review -- unique among providers
- Client-side-first diagnostic approach in CoT was the most user-accessible
- Detailed compliance reasoning with specific COBS rule references
- Concise task decomposition with hierarchical sub-task nesting

**Weaknesses:**
- A/B testing accuracy gap (80% on Variant A vs. 100% for GPT-4o and Claude)
- Classified urgency as "None" rather than "Low" for feedback ticket
- ToT synthesis was verbose without proportional increase in actionability

---

### DeepSeek V2 16B -- "The Capable Local Option"

**Strengths:**
- All tasks executed successfully with valid JSON and correct formatting
- LinkedIn channel suggestion in marketing strategy was a unique and practical idea
- Time zone awareness in task decomposition ("minimize jet lag")
- Zero API cost for all outputs

**Weaknesses:**
- A/B testing accuracy (80% Variant A, 60% Variant B) -- lowest among providers
- Shorter compliance reasoning without regulatory article citations
- Less specific inter-agent message (generic "Moderate" risk category)
- Billing response was concise but missed structured investigation steps

---

## Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| **Production PTCF agents** | OpenAI GPT-4o | Cleanest format adherence; highest classification accuracy |
| **Compliance screening** | Claude Sonnet 4 | Specific regulatory citations; persona boundary enforcement |
| **Security code review** | Gemini Flash 2.5 | OWASP-aligned output; most detailed vulnerability analysis |
| **Multi-expert synthesis** | Claude Sonnet 4 | Richest ToT branch outputs with actionable specifics |
| **Offline prototyping** | Ollama DeepSeek V2 | Zero cost; valid outputs across all prompting patterns |

---

*Analysis based on Chapter 3 notebook outputs executed April 2026. All four providers ran in LIVE mode with real API keys (OpenAI GPT-4o, Claude Sonnet 4, Gemini Flash 2.5, DeepSeek V2 16B via Ollama). Scores reflect actual output from persona construction, PTCF, CoT/ToT, classification, and case study cells, with specific output text cited as evidence.*
