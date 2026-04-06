# Use Case: LearnPath — AI-Powered Adaptive Learning for Computer Science Education

**Chapter 15: Education and Knowledge Agents**
**Book: "30 Agents Every AI Engineer Must Build" by Imran Ahmad (Packt, 2026)**

---

## The Company

**LearnPath** is an EdTech startup in Seattle, offering an online Python programming course for university students and career changers. Their platform serves 12,000 active learners across 28 university partnerships and a direct-to-consumer channel. The course covers Python fundamentals through intermediate topics (variables, control flow, data structures, functions) in a self-paced format with auto-graded exercises. Annual revenue: $4.8M from university site licenses ($25K–$80K each) and individual subscriptions ($29/month). Team: 8 engineers, 4 curriculum designers, 3 learning scientists, and 6 in sales/ops.

## The People

- **Dr. Mei Lin, CEO & Co-Founder** — Former CS professor at the University of Washington. She left academia because she saw the same pattern every semester: 30% of students fell behind by week 4, couldn't catch up, and either failed or dropped. The one-size-fits-all lecture format couldn't adapt to individual learners. She founded LearnPath to build the adaptive tutor she wished she'd had as a professor.
- **Carlos Rivera, Head of Curriculum** — Manages the course content: 10 learning modules, 85 exercises, and 15 auto-graded assessments. His problem: the curriculum follows a fixed sequence (variables → conditionals → loops → functions). A student who already knows variables and conditionals still has to work through those modules before reaching loops. Meanwhile, a student struggling with boolean logic gets pushed into for-loops before they're ready.
- **Dr. Aisha Okafor, Learning Scientist** — Holds a PhD in educational measurement. She's been analyzing LearnPath's learner data and has alarming findings: 40% of students who fail a for-loops exercise have the *same misconception* — they place the `break` statement after the accumulation step instead of before it. The platform treats every wrong answer identically ("Try again!") regardless of the underlying error.
- **Jake Thompson, Student** — 26-year-old career changer, former barista, enrolled in LearnPath through a community college partnership. He completed the variables and conditionals modules easily but has been stuck on for-loops for 2 weeks. He's attempted the "sum even numbers with early termination" exercise 7 times. Each attempt gets the same generic feedback. He's considering dropping the course.
- **Professor Diana Reeves, University of Oregon** — Uses LearnPath in her intro CS course (180 students/semester). Her frustration: all 180 students start at module 1 regardless of prior experience. CS majors who took AP Computer Science in high school are bored for 3 weeks. First-generation students with no coding experience are overwhelmed by week 3. She wants adaptive placement and pacing, not a one-speed conveyor belt.

## The Problem

LearnPath has a completion problem that threatens the business:

1. **Course completion rate: 52%.** Nearly half of enrolled learners don't finish. University partners measure LearnPath by completion rate — if it drops below 60%, two contracts ($110K combined) are at risk of non-renewal. The direct-to-consumer channel has 71% monthly churn for learners who've been enrolled more than 60 days without completing.

2. **The fixed curriculum ignores learner state.** Carlos's 10-module sequence assumes every student needs every module in order. In reality:
   - 25% of students already know variables and conditionals (they're bored)
   - 15% of students need *more* time on boolean logic before attempting loops (they're overwhelmed)
   - The ZPD (Zone of Proximal Development) — the sweet spot where content is challenging but achievable — is different for every student, and the platform doesn't detect it

3. **Feedback is generic and unhelpful.** When Jake submits incorrect code, the platform says "Your output doesn't match the expected output. Try again!" It doesn't identify that his break statement is in the wrong position, that this is a known misconception (control flow ordering), or that tracing through the code with a specific input would reveal the bug. Aisha's data shows 40% of for-loop failures share this one misconception — but the platform can't detect or address it.

4. **Mastered skills decay without review.** A student who masters list basics in week 2 hasn't practiced it since. By week 6, when list comprehensions build on list basics, the student has forgotten slicing syntax. There's no spaced repetition — once a module is "complete," it's never revisited.

5. **No adaptive placement.** Professor Reeves's 180 students all start at module 1. The AP students coast through 3 weeks of material they already know, developing bad study habits (not reading carefully, rushing). The first-generation students get no extra scaffolding in the early modules where they need it most.

## The Attempted Solutions

| Attempt | What happened |
|---|---|
| Added "skip module" button | 30% of students skipped modules they actually needed. Completion rate dropped further because they hit walls in later modules without prerequisites. Carlos removed the feature. |
| Wrote better error messages | Carlos and Aisha wrote 200 custom error messages mapped to common wrong answers. This helped for exact-match errors but missed variations. A student who places `break` on line 5 vs. line 6 gets different generic feedback even though the misconception is identical. |
| Weekly review quizzes | Added a quiz at the end of each week covering prior material. Students crammed before the quiz and forgot afterward. No long-term retention benefit. Completion rate unchanged. |
| Office hours chatbot | Built a basic Q&A chatbot using GPT-4 with course content as context. It answered factual questions well but couldn't diagnose specific code errors, track individual student progress, or adapt its explanations to what the student already knew vs. didn't know. |

## How Chapter 15's Code Solves This

### Agent 1: Education Intelligence Agent — POMDP-Based Adaptive Tutor

LearnPath deploys the full adaptive tutoring pipeline from Chapter 15. The student's knowledge state is *hidden* (the platform can't directly observe what a student knows — it can only observe their performance on exercises) and evolves over time. This is a Partially Observable Markov Decision Process.

**Component 1: Knowledge Graph (Curriculum as DAG)**

Carlos's 10 learning modules are restructured as a directed acyclic graph with prerequisite edges:

```
variables → conditionals → for_loops → loop_termination → nested_iteration
                 │                            │
                 → boolean_logic              → list_comprehensions
                                                      │
variables → list_basics → list_slicing ──────→ list_comprehensions → functions_intro
```

Each objective has a calibrated difficulty (0.0–1.0). `variables` is 0.15 (easy). `nested_iteration` is 0.70 (hard). The graph enforces prerequisites: a student can't attempt `for_loops` until `conditionals` and `list_basics` are mastered.

**Component 2: Adaptive Placement Test (IRT 2PL)**

Professor Reeves's 180 students no longer all start at module 1. The `AdaptivePlacementTest` uses a 15-item bank calibrated from 12,000 historical students with Item Response Theory:

```
P(correct | θ, a, b) = 1 / (1 + exp(-a(θ - b)))
```

Each item has a discrimination parameter (a) measuring how sharply it distinguishes ability levels, and a difficulty parameter (b) measuring the ability level at which P(correct) = 0.50.

The test selects items adaptively using Fisher Information — each question is chosen to maximally reduce uncertainty about the student's ability at the current estimate. It converges when standard error drops below 0.30, typically in 8–12 questions.

**Result for Professor Reeves's class:**
- AP students test into for_loops or beyond — skip 3 weeks of review, start challenged immediately
- First-generation students place at variables or conditionals — get the scaffolding they need from day one
- Average placement test: 10 questions, 4 minutes

**Component 3: Bayesian Knowledge Tracing (BKT)**

Every time Jake submits an exercise, his mastery probability is updated using Bayes' rule:

```
If correct:
  P(mastery | correct) = P(correct | mastery) × P(mastery) / P(correct)
  P(mastery_next) = P(mastery | correct) + (1 - P(mastery | correct)) × P(learn)

If incorrect:
  P(mastery | incorrect) = P(slip | mastery) × P(mastery) / P(incorrect)
  P(mastery_next) = P(mastery | incorrect) + (1 - P(mastery | incorrect)) × P(learn)
```

Default parameters: P(learn) = 0.10 per opportunity, P(slip) = 0.05 (correct despite not mastered), P(guess) = 0.20 (correct by luck).

Jake's for_loops trajectory:
- Start: p = 0.10 (low prior)
- Exercise 1 (correct): p → 0.18
- Exercise 2 (incorrect — break placement): p → 0.11 (drops, triggers diagnostic)
- Diagnostic trace exercise (correct): p → 0.22
- Corrected resubmission (correct): p → 0.33
- Spaced review 2 days later (correct): p → 0.44
- Continues until p ≥ 0.85 (mastery threshold)

The platform no longer treats Jake's 7 identical wrong answers identically. After 2 failures, BKT detects declining mastery and triggers the misconception detection pipeline.

**Component 4: ZPD-Based Curriculum Planning**

The `CurriculumPlanner` selects Jake's next exercise using a Gaussian expected-gain formula:

```
G(mastery, difficulty) = α × exp(-(difficulty - mastery - δ)² / (2σ²))
```

Where δ = 0.20 (optimal gap) and σ = 0.25 (ZPD width). Learning gain peaks when the exercise is slightly harder than the student's current mastery — challenging but achievable.

Too easy (difficulty << mastery): minimal learning, student is bored.
Too hard (difficulty >> mastery): cognitive overload, student gives up.

This is why Carlos's fixed sequence fails — it doesn't adjust difficulty to where the student actually is.

**Component 5: Misconception Detection (Two-Stage Pipeline)**

When Jake submits incorrect code, the platform doesn't say "Try again!" It runs Aisha's misconception detection:

**Stage 1: Rule-Based Classifier (~50ms, catches ~70%)**
Pattern matching against 180+ known misconceptions. Jake's code contains `break` after `total += x` → matches `ctrl_flow_break_placement` (confidence: 0.82).

**Stage 2: LLM Diagnostic (invoked if Stage 1 confidence < 0.70)**
For novel errors, the LLM analyzes the submission, exercise description, and student's recent error history.

**Feedback follows a 4-part pedagogical contract:**
1. "Great work on the overall structure! Your for loop iterates correctly and your modulo check for even numbers is right."
2. "However, there's an issue with where your break statement executes relative to the accumulation step."
3. "Trace through your code with `nums = [2, 4, -1, 6]`. Write down `total` after each iteration. At which point does the behavior diverge from what you expect?"
4. "This is a common misconception about control flow ordering — the sequence of conditions and actions inside a loop determines behavior."

Jake doesn't get "wrong answer." He gets a guided discovery experience that addresses his specific misconception.

**Component 6: Spaced Repetition (SM-2 Algorithm)**

Once Jake masters for_loops (p ≥ 0.85), the SM-2 scheduler prevents decay:

```
Rep 0 (first mastery): review in 1 day
Rep 1 (second success): review in 6 days
Rep 2+: interval × ease_factor (growing)
```

If Jake answers correctly with slight hesitation (quality = 4), the ease factor remains stable and the interval grows. If he struggles (quality ≤ 2), the interval resets to 1 day.

The platform schedules 3–5 review exercises per session, prioritized by overdue priority (days_overdue / 7, capped at 1.0). By week 6, when Jake reaches list comprehensions, his list_basics mastery is still fresh from periodic reviews.

### Agent 2: Collective Intelligence Agent — Multi-Agent Rubric Design

Carlos needs to create a grading rubric for a new "merge two sorted lists" assignment. Instead of designing it alone, he deploys three specialized AI agents:

**Pedagogy Specialist** — Proposes process-oriented assessment: 40% strategy / 30% correctness / 30% readability. Values partial credit for good reasoning with bugs.

**Domain Expert** — Proposes technical rigor: 50% correctness / 30% efficiency / 20% style. Rewards O(n+m) two-pointer approach over sort-based O(n log n).

**Assessment Specialist** — Proposes binary reliability: 5 pass/fail criteria × 20% each. Maximizes inter-rater agreement.

The `ConsensusEngine` runs a multi-round critique-and-refine protocol:
- Round 1: Each agent proposes independently, one rotates into adversarial critic role
- Round 2: Agents evaluate each other's proposals with expertise-weighted scoring
- Convergence: Score changes < 0.1 → synthesize

**The emergent result:** A hybrid 5-criterion × 3-point rubric combining the Assessment Specialist's structure, the Domain Expert's edge-case specificity, and the Pedagogy Specialist's process emphasis. Plus a novel "diagnostic trace" criterion that none proposed individually — it emerged from the interaction between the Domain Expert's technical focus and the Pedagogy Specialist's process orientation.

Carlos gets a rubric in 20 minutes that would have taken 3 days of committee meetings.

## The Revenue Impact

| Metric | Before | After | Change |
|---|---|---|---|
| Course completion rate | 52% | 78% | +26pp |
| Time to placement (new students) | 3 weeks (fixed sequence) | 4 minutes (adaptive test) | -99% |
| Students stuck > 2 weeks on one topic | 23% | 6% | -74% |
| Misconception-targeted feedback | 0% (generic "try again") | 70% (rule-based) + 30% (LLM) | 100% coverage |
| Skill retention at 6 weeks | 45% (no review) | 82% (SM-2 spaced repetition) | +37pp |
| Student satisfaction (NPS) | +12 | +47 | +35 points |
| Rubric design time | 3 days (committee) | 20 minutes (multi-agent consensus) | -99% |

**Revenue impact:** Completion rate rising from 52% to 78% saves the two at-risk university contracts ($110K). Student satisfaction improvement drives 6 new university partnerships in the pipeline ($300K combined). Direct-to-consumer churn drops from 71% to 38% at 60-day mark, adding $1.2M in annual subscription retention. Projected ARR: $4.8M → $7.6M.

**Educational outcomes:** 34% improvement in assessment scores across the learner population. Course completion: 52% → 78%. Student-reported confidence in programming: +0.8 points on 5-point scale.

## What This Code Covers vs. Next Steps

### What Chapter 15's code solves:
- Knowledge graph (DAG) with prerequisite edges and calibrated difficulty
- Adaptive placement test using 2PL IRT with Fisher Information item selection
- Bayesian Knowledge Tracing with per-student probabilistic mastery estimates
- ZPD-based curriculum planning (Gaussian expected-gain optimization)
- SM-2 spaced repetition scheduling with ease factor adaptation
- Two-stage misconception detection (rule-based 50ms + LLM diagnostic)
- Four-part pedagogical feedback contract (acknowledge → localize → guide → address)
- Multi-agent consensus engine with adversarial critic rotation and weighted voting
- Emergent rubric criteria from cross-agent interaction

### Next steps LearnPath would need:
- **Conversational tutoring** — Let students like Jake ask follow-up questions in natural language: "I don't understand why my break is wrong" (see Chapter 10)
- **Explainable recommendations** — Show students *why* the platform recommends a specific exercise: "Your mastery of list_basics is 0.72 and this exercise targets the 0.20 gap where you learn fastest" (see Chapter 12)
- **Multimodal input** — Accept screenshots of code errors, voice questions during mobile study sessions (see Chapter 11)
- **Self-improving feedback** — Learn from which feedback messages actually help students correct misconceptions vs. which ones they ignore (see Chapter 9)
- **Ethical monitoring** — Ensure the adaptive algorithm doesn't create disparate outcomes by demographics — students from under-resourced backgrounds shouldn't systematically receive easier content (see Chapter 12)
- **Cost-aware model routing** — Route rule-based misconception detection (70% of cases) to avoid LLM costs; only invoke GPT-4 for novel errors (see Chapter 4)

---

*This use case is fictional and created for educational purposes. It demonstrates how the code patterns in Chapter 15 apply to a realistic adaptive learning platform scenario.*
