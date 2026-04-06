# Use Case: Meridian Facilities — AI-Powered Smart Building Operations

**Chapter 11: Multi-Modal Perception Agents**
**Book: "30 Agents Every AI Engineer Must Build" by Imran Ahmad (Packt, 2026)**

---

## The Company

**Meridian Facilities** is a commercial property management firm in Denver, Colorado, operating 22 Class A and Class B office buildings totaling 4.8 million square feet. Their tenants include law firms, tech companies, a regional hospital's administrative offices, and two data center colocation facilities. Annual revenue: $62M from tenant leases and managed services. Operations team: 34 building engineers, 12 security staff, and a 6-person central operations center that monitors all 22 properties remotely.

## The People

- **Gloria Vasquez, COO** — Oversees all building operations. She's under pressure from the CFO to cut energy costs by 15% ($1.4M/year) without impacting tenant comfort scores, which are already at the industry minimum (3.6/5.0) for their lease class. Two enterprise tenants have cited "temperature complaints" in their lease renewal negotiations.
- **Mike Tanaka, Director of Engineering** — Manages the building engineers. His team handles 380+ HVAC service tickets per month across 22 buildings. 40% are "too hot" or "too cold" complaints that turn out to be within normal range — but by the time an engineer drives to the site, inspects the zone, and closes the ticket, 2 hours have passed. Mike estimates his team wastes 600 hours/month on false-alarm comfort tickets.
- **Aisha Obi, Head of Security** — Runs the security operations center. Her team monitors camera feeds across all 22 properties — roughly 480 cameras. Realistically, operators can actively watch 20–30 feeds at a time. After-hours intrusion detection relies on motion-triggered alerts that fire 200+ times per night across the portfolio (mostly cleaning crews, HVAC cycling, and rodents). The actual security incidents: 3 per year.
- **Dr. Nathan Cho, Tenant Relations (Regional Hospital Admin)** — The hospital's administrative offices occupy 3 floors of Meridian's flagship building. Dr. Cho has filed formal complaints about CO2 levels in the 4th-floor conference center — his staff reported headaches and difficulty concentrating during long meetings. Meridian's engineers tested the HVAC and said it was "within spec," but they only took a single point-in-time reading.
- **Priya Reddy, Data Center Operations Manager** — Manages the two colocation facilities. Her SLA guarantees 99.99% uptime with ambient temperature between 64–72°F. Last quarter, a cooling unit failed silently on a Saturday night. By the time the on-call engineer was alerted (via a tenant's own monitoring), server inlet temperatures had reached 94°F. Three tenants filed SLA breach claims totaling $180K.

## The Problem

Meridian manages buildings the way most property firms do — reactively. Problems are discovered by tenants, not by Meridian. The operations center exists but mostly processes alarms after the fact.

### Problem 1: HVAC Is Blind

Meridian's building management system (BMS) collects temperature readings from zone sensors every 15 minutes. But:

- **No fusion.** Each sensor reports independently. A zone with 4 temperature sensors might show 71°F, 74°F, 69°F, and 73°F. The BMS averages to 71.75°F and declares "in range." But sensor 2 is near a sun-facing window and sensor 3 is near the server closet — the average masks real discomfort.
- **No CO2 monitoring.** The BMS tracks temperature and humidity but not CO2. Dr. Cho's conference room complaint is invisible to Meridian's systems. CO2 above 1,000 ppm causes measurable cognitive impairment; above 1,500 ppm causes headaches. The conference center regularly hits 1,300+ ppm during back-to-back meetings — but nobody measures it.
- **No occupancy awareness.** The HVAC runs on a fixed schedule (7 AM – 7 PM). If a floor is empty at 2 PM (everyone at an offsite), it's still heating/cooling at full capacity. If a team works until 10 PM, they're in the dark and uncomfortable because the system shut off at 7.
- **Short-cycling.** Engineers have noticed that the HVAC in Building 7 cycles on and off every 3–4 minutes — the compressor is being destroyed by rapid switching. The BMS has no deadband logic; it reacts to every 0.5°F fluctuation.

### Problem 2: Security Drowns in False Alarms

Aisha's team gets 200+ motion alerts per night. The signal-to-noise ratio is 3 real incidents per year out of ~73,000 annual alerts — a 0.004% hit rate. Operators have developed "alert fatigue" and started ignoring most notifications. The real risk: a genuine after-hours intrusion will be missed because it looks like every other alert.

What Aisha actually needs is not motion detection — it's *contextual occupancy analysis*. A cleaning crew at 9 PM is normal. A single person in the server room at 2 AM on a Sunday is not.

### Problem 3: The Data Center Has No Early Warning

Priya's $180K SLA breach happened because the cooling failure was silent — no alarm fired until a tenant noticed. The BMS polls temperature every 15 minutes. A cooling unit that fails at minute 1 isn't detected until minute 15. In a server room, temperatures can rise 4–5°F per minute without cooling. By minute 15, servers are throttling or shutting down.

Priya needs continuous monitoring with proportional response — not a binary alarm at a critical threshold.

## The Attempted Solutions

| Attempt | What happened |
|---|---|
| Upgraded BMS to latest version | New dashboard, same 15-minute polling. No sensor fusion, no CO2, no occupancy. Cost: $280K. Tenant satisfaction unchanged. |
| Added more cameras + motion sensors | Increased alert volume from 150/night to 200/night. Aisha's team now ignores more alerts, not fewer. |
| Hired 2 more building engineers | Helped with ticket volume for 3 months, then two existing engineers quit (burnout from false-alarm site visits). Net staffing unchanged. |
| CO2 spot checks per Dr. Cho's complaint | Engineer brought a handheld CO2 meter, measured 680 ppm at 8 AM (empty room), declared "within spec." Conference room hits 1,300 ppm at 2 PM with 20 people — but nobody was there to measure it. |
| Data center temperature alerts at 85°F | Alert fires at 85°F — but at that point the cooling has been failed for 4+ minutes and the damage trajectory is already critical. Too late for proportional response. |

## How Chapter 11's Code Solves This

Chapter 11 builds three multimodal perception agents. Meridian deploys all three across different building types.

### Agent 1: Vision-Language Agent — Workspace Safety & Occupancy (Section 11.2)

Meridian connects the Vision-Language agent to existing security cameras — not for surveillance, but for contextual scene understanding.

**The Chain-of-Thought Approach:**

Unlike traditional motion detection (binary: motion/no-motion), the VL agent *reasons* about what it sees:

1. **Identify** relevant objects and people in the frame
2. **Examine** specific contextual details (uniforms, equipment, time of day)
3. **Conclude** based on visual evidence

**Scenario: After-Hours Occupancy Analysis**

Camera captures motion in the server room at 2 AM Sunday. Traditional system: fires alert #47 of the night. VL agent analysis:

```
Reasoning: I observe one individual in the server room at 02:14.
The person is not wearing a Meridian uniform or badge lanyard.
They are carrying a backpack, not a tool kit.
Cleaning crew typically operates in pairs with carts.
Therefore: This is an UNAUTHORIZED presence — escalate to security.
```

**Scenario: Workspace Occupancy Counting**

The agent counts people on each floor every 15 minutes during business hours. This feeds the HVAC occupancy signal:
- Floor 4 conference center: 22 people detected → high occupancy → increase ventilation
- Floor 7: 3 people detected (should be 40) → low occupancy → reduce HVAC output

**Impact:** Aisha's false alarm rate drops from 200/night to ~8/night (contextual filtering). The 3 real incidents per year are *more* likely to be caught because operators aren't fatigued.

### Agent 2: Audio Processing Agent — Tenant Call Analysis (Section 11.3)

Meridian's tenant support line handles 1,200 calls per month — maintenance requests, complaints, lease inquiries. The Audio Processing Agent adds two capabilities:

**Transcription with Mode Awareness:**

Every call is transcribed in CLEAN mode (disfluencies removed) for the ticket system, and archived in VERBATIM mode for lease dispute records.

```
CLEAN:  "I've been waiting for three weeks and nobody has called 
         me back. This is unacceptable."
VERBATIM: "Yes um I've been waiting for um three weeks now and uh 
           nobody has called me back. This is um unacceptable..."
```

**Voice Sentiment Analysis (VAD):**

The prosodic analysis detects caller emotion from pitch and speaking rate — before a human agent picks up:

| Caller Profile | Pitch (Hz) | Rate (syl/s) | Detected Emotion | Routing |
|---|---|---|---|---|
| Normal inquiry | 130 | 4.0 | Neutral (0.95) | Standard queue |
| Frustrated tenant | 260 | 6.2 | Angry (0.975) | Priority → senior agent |
| Dr. Cho (concerned) | 180 | 3.5 | Sad/worried (0.88) | Priority → tenant relations |

**Impact:** Frustrated callers are routed to senior agents immediately instead of waiting in queue and escalating further. Tenant satisfaction on complaint calls improves from 2.1/5.0 to 3.8/5.0 because the right person answers the first time.

### Agent 3: Physical World Sensing Agent — Smart Building Control (Section 11.4)

This is the core of Meridian's operational transformation. The SmartBuildingAgent implements a full Sense-Model-Plan-Act control loop for every zone in every building.

**Sensor Fusion (5-Minute Temporal Window):**

Instead of single point-in-time readings, the agent fuses all sensor data from the past 5 minutes:

```
Zone 4F-CONF (Dr. Cho's conference center):
  Temperature sensors (4): [72.1, 74.3, 71.8, 73.2] → fused: 72.85°F
  CO2 sensors (2): [1,280, 1,420] → fused: 1,350 ppm
  Occupancy (PIR + camera): probability 0.92
  Time: 14:30 (within occupied hours)
```

The 5-minute window smooths transient noise (someone walks past a sensor, door opens briefly) while remaining responsive to real trends.

**Event Detection via Pattern Matching:**

Three built-in patterns run against every zone every cycle:

| Pattern | Condition | Severity | Action |
|---|---|---|---|
| Critical Temperature | > 95°F or < 50°F | CRITICAL | Immediate alert + max cooling/heating |
| Unexpected Occupancy | > 70% occupancy outside business hours | WARNING | Security alert |
| High CO2 | > zone max (1,000 ppm for offices) | WARNING | Increase ventilation |

**Proportional Control with Deadband Hysteresis:**

This solves Building 7's short-cycling problem. The control algorithm:

```
target = 72°F (midpoint of 68–76°F range)
error = current_temp - target

if |error| ≤ 1.0°F:     → DEADBAND: no action (prevents short-cycling)
if error > 1.0°F:       → COOLING at intensity = min(100%, error × 20%)
if error < -1.0°F:      → HEATING at intensity = min(100%, |error| × 20%)
```

The 1.0°F deadband means the system tolerates small fluctuations without reacting. The HVAC compressor in Building 7 stops cycling every 3 minutes and instead runs in smooth, proportional bursts.

For CO2 ventilation:
```
if CO2 > 1,000 ppm:
  excess = CO2 - 1,000
  ventilation = min(100%, 50% + excess/10)
```

Dr. Cho's conference center at 1,350 ppm → ventilation at 85% intensity. CO2 drops below 1,000 within 12 minutes.

**The Four Demo Scenarios Map to Meridian's Buildings:**

| Scenario | Zone | What happens | Result |
|---|---|---|---|
| Normal office | Standard tenant floor | 72°F, 650 ppm CO2, 80% occupancy during hours | 0 alerts, 0 commands — comfort maintained efficiently |
| Server room overheat | Priya's colocation facility | 96.5°F detected (cooling failure) | CRITICAL alert + 100% emergency cooling — detected in seconds, not 15 minutes |
| After-hours intrusion | Building lobby at 11 PM | 90% occupancy probability outside hours | WARNING alert → security dispatched |
| High CO2 in occupied space | Dr. Cho's conference center | 1,350 ppm during meeting | WARNING alert + 85% ventilation command |

## The Revenue Impact

| Metric | Before | After | Change |
|---|---|---|---|
| Energy cost (HVAC) | $9.4M/year | $7.8M/year | -17% ($1.6M saved) |
| False-alarm comfort tickets | 380/month | 95/month | -75% |
| Engineer hours on false alarms | 600 hrs/month | 150 hrs/month | -75% |
| Security false alerts | 200/night | 8/night | -96% |
| Data center SLA breaches | $180K/quarter | $0 (early detection) | -100% |
| Tenant satisfaction score | 3.6/5.0 | 4.3/5.0 | +19% |
| HVAC compressor replacements | 4/year ($35K each) | 1/year | -75% ($105K saved) |
| CO2-related complaints | 12/year | 0 | -100% |

**Projected annual impact:** $2.1M in energy savings, avoided SLA penalties, reduced maintenance, and retained tenants. Two enterprise tenants that were negotiating lease exits (combined rent: $3.2M/year) renewed after seeing the improved comfort scores and CO2 monitoring.

Gloria's 15% energy reduction target: achieved at 17%.

## What This Code Covers vs. Next Steps

### What Chapter 11's code solves:
- Vision-Language agent with Chain-of-Thought reasoning for contextual scene understanding
- Audio transcription in VERBATIM and CLEAN modes for different compliance needs
- Voice sentiment analysis using prosodic features (pitch + rate → emotion detection)
- Sensor fusion with 5-minute temporal windowing across heterogeneous sensor types
- Event detection via pattern matching (critical temperature, unexpected occupancy, high CO2)
- Proportional control with deadband hysteresis to prevent short-cycling
- Full Sense-Model-Plan-Act architecture for physical world agents
- Simulation mode with mock backends for development without hardware

### Next steps Meridian would need:
- **Predictive maintenance** — Use historical sensor patterns to predict cooling unit failures *before* they happen, not just detect them (see Chapter 8 for data analysis and reasoning agents)
- **Tenant-facing chatbot** — Let tenants report issues and check maintenance status via conversational AI instead of phone calls (see Chapter 10)
- **Multi-building orchestration** — Coordinate energy management across all 22 buildings — shift cooling load to buildings with solar generation during peak hours (see Chapter 7 for tool orchestration and Chapter 16 for multi-agent coordination)
- **Compliance auditing** — Generate automated reports for ASHRAE 55 (thermal comfort) and WELL Building Standard certification (see Chapter 12 for explainable decisions)
- **Cost-aware model routing** — Route simple occupancy counts through lightweight models, complex scene analysis through full VL models (see Chapter 4)
- **Knowledge base** — RAG pipeline over equipment manuals, maintenance histories, and building codes for engineer decision support (see Chapter 6)

---

*This use case is fictional and created for educational purposes. It demonstrates how the code patterns in Chapter 11 apply to a realistic commercial property management scenario.*
