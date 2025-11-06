# Post-Mortem — Executable Loop Playbook

**Category:** Export **Abbreviation:** PM **Schema:**
<https://questfoundry.liesdonk.nl/schemas/tu_brief.schema.json>

> **Note:** Full specification pending in Layer 0. This playbook provides a skeletal structure based
> on taxonomy and canonical naming conventions.

## Purpose

Conduct a retrospective analysis after a major milestone, release, or significant TU cluster
completes. Capture lessons learned, process improvements, quality bar trends, and team insights to
inform future loops and reduce recurring issues. Outcome: A post-mortem report documenting what went
well, what went poorly, action items for process improvement, and updated best practices.

## Activation Criteria (Showrunner)

- After major milestone completion (chapter release, act completion, full book export)
- After a significant TU cluster or multi-loop pass completes
- When recurring quality bar issues suggest process review needed
- Periodic retrospectives (e.g., quarterly, per major release)

Showrunner opens a Trace Unit (TU): `tu-post-mortem-<milestone>` and invites all participating
roles.

## RACI Matrix

| Role       | Assignment | Responsibilities                                                            |
| ---------- | ---------- | --------------------------------------------------------------------------- |
| Showrunner | R/A        | Facilitates retrospective session; documents findings; creates action items |
| All Roles  | C          | Participate in retrospective; provide candid feedback on process            |
| Gatekeeper | C          | Summarize quality bar trends and recurring issues from gatechecks           |

## Inputs

- Completed TUs from the milestone/period under review
- Gatecheck reports and bar status trends
- Narration Dry-Run findings and PN feedback
- Hook Harvest triage patterns
- Timeline metrics (cycle time, gate pass rates, rework frequency)
- Team observations and anecdotes

## Procedure (Message Sequences)

> **Note:** Detailed message sequences pending in Layer 4 protocol specification.

### Step 1: Gather Data

Collect metrics and artifacts from completed TUs:

- Gate pass/conditional pass/block rates per loop
- Most common bar failures (yellow/red)
- Rework cycles per artifact type
- Time from TU open to merge
- Hook acceptance/deferral/rejection patterns

### Step 2: Retrospective Session

Facilitate discussion with all roles covering:

- What went well (celebrate successes)
- What went poorly (identify pain points)
- Surprising discoveries
- Process improvements to try next

### Step 3: Identify Action Items

For each improvement area:

- Specific action to take
- Owner responsible for implementation
- Target completion date or milestone
- Success criteria

### Step 4: Update Best Practices

Document new patterns or guidance:

- Style patterns that reduced drift
- Pre-gate techniques that caught issues early
- Hook formulation patterns that triaged cleanly
- Deferral strategies that worked well

### Step 5: Package Report

Create Post-Mortem Report summarizing findings and action items.

## Deliverables

- **Post-Mortem Report:**
  - Milestone/period under review
  - Metrics summary (gate rates, rework cycles, etc.)
  - What went well (successes, wins, effective practices)
  - What went poorly (pain points, blockers, inefficiencies)
  - Surprising discoveries (unexpected insights)
  - Action items (specific, owned, dated)
  - Updated best practices or process guidance
  - Participants and date

## Success Criteria

- All participating roles contribute to retrospective
- Action items are specific, owned, and dated
- Best practices updated based on lessons learned
- Report archived and accessible for future reference
- Action items tracked in subsequent TUs

## Failure Modes & Remedies

- **Blame culture emerges** → Focus on systems and process, not individuals; frame as learning
  opportunity
- **Vague action items** → Ensure each action has clear owner, description, and success criteria
- **No follow-through** → Assign action item tracking to Showrunner; review in next Post-Mortem
- **Missing participation** → Schedule retrospective when all key roles available; asynchronous
  input acceptable

## Quality Bars Pressed

**Primary:** Integrity (process improvement traceability)

**Secondary:** All bars indirectly (retrospective aims to improve all quality outcomes)

## Handoffs

- **To Showrunner:** Action items for implementation in upcoming TUs
- **To All Roles:** Updated best practices and process guidance
- **To Archive:** Post-Mortem Report for historical reference and pattern analysis
