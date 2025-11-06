# QuestFoundry Architecture

This document provides a comprehensive overview of the QuestFoundry specification architecture,
design principles, and component relationships.

---

## Table of Contents

1. [Design Philosophy](#design-philosophy)
2. [The 7-Layer Architecture](#the-7-layer-architecture)
3. [Core Components](#core-components)
4. [Data Flow](#data-flow)
5. [State Machines](#state-machines)
6. [Hot vs. Cold Architecture](#hot-vs-cold-architecture)
7. [Quality Enforcement](#quality-enforcement)
8. [Protocol Design](#protocol-design)
9. [Extensibility](#extensibility)
10. [Design Decisions](#design-decisions)

---

## Design Philosophy

QuestFoundry is built on several key principles:

### 1. **Separation of Concerns**

The 7-layer architecture ensures each concern is isolated:

- **What we do** (Layers 0-1): Vision, roles, workflows
- **What we say** (Layers 2-3): Data structures, schemas
- **How we communicate** (Layer 4): Protocol, state machines
- **How we implement** (Layers 5-7): Prompts, code, interfaces

This separation allows:

- **Human understanding** without code
- **Machine validation** without ambiguity
- **Tool replaceability** without breaking canon
- **Independent evolution** of each layer

### 2. **Clarity Over Cleverness**

Every design choice prioritizes **explainability**:

- Human-readable markdown for vision/roles
- Self-documenting JSON schemas
- Explicit state transitions
- Traceable changes via Trace Units

### 3. **Replaceability**

No component is irreplaceable:

- Swap AI models (Claude → ChatGPT → custom)
- Change validation tools (Python → TypeScript)
- Replace UI frameworks
- **Without** changing canon, roles, or protocol

### 4. **Traceability**

Every change is tracked:

- **Trace Units (TUs)** for all modifications
- **Hot/Cold snapshots** for reproducibility
- **Git-based versioning** for history
- **Gatekeeper approval** for quality

### 5. **Safety First**

Player-facing content is protected:

- **Player-Narrator (PN)** sees only Cold
- **Spoiler hygiene** enforced at protocol level
- **Quality bars** prevent broken experiences
- **Accessibility** built into requirements

---

## The 7-Layer Architecture

### Visual Overview

```text
┌─────────────────────────────────────────────────────────────┐
│ Layer 7: UI (CLI, GUI, Player-Narrator)                    │ 📋 Planned
│ ├─ Command-line tools for authors                          │
│ ├─ Web-based authoring interface                           │
│ └─ Player-facing narrative engine                          │
├─────────────────────────────────────────────────────────────┤
│ Layer 6: Libraries (Python SDK, TypeScript SDK)            │ 📋 Planned
│ ├─ Validation libraries                                    │
│ ├─ Protocol clients                                        │
│ └─ Export engines                                          │
├─────────────────────────────────────────────────────────────┤
│ Layer 5: Prompts (AI Agent Implementations)                │ ✅ 100% (loop-focused architecture)
│ ├─ 13 loop playbooks (executable procedures)               │
│ ├─ 15 role adapters (thin interfaces)                      │
│ ├─ 15 full system prompts (standalone work)                │
│ ├─ 31 intent handlers                                      │
│ └─ Example conversations                                   │
├─────────────────────────────────────────────────────────────┤
│ Layer 4: Protocol (Communication Rules)                    │ 🚧 85% (envelopes, intents done)
│ ├─ Message envelopes (protocol versioning)                 │
│ ├─ Intent catalog (30+ intents)                            │
│ ├─ State machines (hook, TU lifecycles)                    │
│ └─ Message flows (sequence diagrams)                       │
├─────────────────────────────────────────────────────────────┤
│ Layer 3: Schemas (JSON Schema Draft 2020-12)               │ ✅ 100% (21 schemas)
│ ├─ Artifact schemas (hook_card, tu_brief, etc.)            │
│ ├─ Envelope schema (protocol structure)                    │
│ └─ Validation metadata ($id, $schema, examples)            │
├─────────────────────────────────────────────────────────────┤
│ Layer 2: Common Language (Data Dictionary)                 │ ✅ 100% complete
│ ├─ 20 artifact templates enriched (markdown + constraints) │
│ ├─ Glossary and taxonomies (8 sections)                    │
│ └─ Field registry and cross-references                     │
├─────────────────────────────────────────────────────────────┤
│ Layer 1: Roles (Who Does What)                             │ ✅ 100% complete
│ ├─ 15 role charters (mission, scope, authorities)          │
│ ├─ 15 agent briefs (practical heuristics)                  │
│ └─ Interfaces (role interactions)                          │
├─────────────────────────────────────────────────────────────┤
│ Layer 0: North Star (Vision & Principles)                  │ ✅ 100% complete
│ ├─ Working model (Hot/Cold, loops, merges)                 │
│ ├─ Quality bars (8 mandatory validation checks)            │
│ ├─ PN principles (player safety)                           │
│ ├─ 13 workflow loops (full guides)                         │
│ └─ 13 playbook one-pagers (quick reference)                │
└─────────────────────────────────────────────────────────────┘

                    ↓ Dependencies flow downward ↓
```

### Layer Dependencies

- **Layer 5** (Prompts) depends on **Layer 4** (Protocol) + **Layer 1** (Roles)
- **Layer 4** (Protocol) depends on **Layer 3** (Schemas)
- **Layer 3** (Schemas) depends on **Layer 2** (Dictionary)
- **Layer 2** (Dictionary) depends on **Layer 0** (North Star)

**No upward dependencies** — upper layers can change without affecting lower layers.

---

## Core Components

### 1. Roles (15 Total)

**Always Active:**

- **Showrunner (SR)** — Orchestrator, scopes work, wakes dormant roles
- **Gatekeeper (GK)** — Quality enforcer, validates against Quality Bars

**Default Active:**

- **Plotwright (PW)** — Topology design (hubs, loops, gateways)
- **Scene Smith (SS)** — Prose writing to topology & style
- **Style Lead (ST)** — Voice, register, motifs
- **Lore Weaver (LW)** — Hooks → spoiler-level canon
- **Codex Curator (CC)** — Player-safe encyclopedia entries

**Optional/Dormant:**

- **Researcher (RS)** — Fact verification
- **Art Director (AD)** / **Illustrator (IL)** — Visual planning/creation
- **Audio Director (AuD)** / **Audio Producer (AuP)** — Sound planning/creation
- **Translator (TR)** — Localization

**Downstream:**

- **Book Binder (BB)** — Export views from Cold
- **Player-Narrator (PN)** — Performs book in-world

### 2. Artifacts (17 Types)

**Core Workflow:**

- `hook_card` — Traceable follow-ups
- `tu_brief` — Work order for changes

**Content:**

- `canon_pack`, `codex_entry`, `style_addendum`, `edit_notes`

**Planning:**

- `research_memo`, `shotlist`, `cuelist`, `art_plan`, `audio_plan`

**Quality:**

- `gatecheck_report`, `view_log`, `front_matter`, `pn_playtest_notes`

**Localization:**

- `language_pack`, `register_map`

**Project:**

- `project_metadata`, `art_manifest`, `style_manifest`

### 3. Workflow Loops (11 Total)

**Discovery:** Story Spark → Hook Harvest → Lore Deepening → Codex Expansion

**Refinement:** Style Tune-up

**Assets:** Art Touch-up, Audio Pass

**Localization:** Translation Pass

**Export:** Binding Run → Narration Dry-Run

**Full Cycle:** Full Production Run

---

## Data Flow

### Hot → Cold Pipeline

```text
┌──────────────────────────────────────────────────────────────┐
│                        HOT (Discovery)                       │
│  - Draft content                                             │
│  - Hook cards                                                │
│  - Spoilers                                                  │
│  - Internal reasoning                                        │
│  - Unstable topology                                         │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ Trace Unit (TU)
                     │ hot-proposed → stabilizing
                     ↓
┌──────────────────────────────────────────────────────────────┐
│                    GATEKEEPER REVIEW                         │
│  - Integrity check (no dead references)                      │
│  - Reachability check (keystones accessible)                 │
│  - Nonlinearity check (hubs/loops meaningful)                │
│  - Gateway check (diegetic coherence)                        │
│  - Style check (voice consistency)                           │
│  - Determinism check (assets promised)                       │
│  - Presentation check (no spoilers, accessibility)           │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ TU: gatecheck → cold-merged
                     ↓
┌──────────────────────────────────────────────────────────────┐
│                        COLD (Canon)                          │
│  - Curated content                                           │
│  - Player-safe surfaces                                      │
│  - Stable topology                                           │
│  - Export-ready                                              │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     │ Snapshot tagging
                     │ Cold @ YYYY-MM-DD
                     ↓
┌──────────────────────────────────────────────────────────────┐
│                       EXPORT VIEWS                           │
│  - EPUB                                                      │
│  - Web (HTML/CSS)                                            │
│  - Plain text                                                │
│  - Audiobook script                                          │
└──────────────────────────────────────────────────────────────┘
```

### Message Flow Example (Hook Harvest)

```text
Showrunner                 Lore Weaver              Gatekeeper
    │                           │                         │
    │ 1. hook.create            │                         │
    ├──────────────────────────>│                         │
    │                           │                         │
    │ 2. ack                    │                         │
    │<──────────────────────────┤                         │
    │                           │                         │
    │                           │ 3. hook.advance         │
    │                           ├────────────────────────>│
    │                           │                         │
    │                           │ 4. gate.report.submit   │
    │                           │<────────────────────────┤
    │                           │                         │
    │ 5. hook.canonize          │                         │
    │<──────────────────────────┤                         │
    │                           │                         │
    │ 6. ack                    │                         │
    ├──────────────────────────>│                         │
```

---

## State Machines

### Hook Lifecycle (7 States)

```text
      proposed
         │
         ├──────> deferred
         │
         ├──────> rejected
         │
         ↓
    investigating
         │
         ↓
     researched
         │
         ↓
    drafting-canon
         │
         ↓
    awaiting-gate
         │
         ↓
     canonized
```

**Allowed Transitions:**

- `proposed → investigating` (Lore Weaver starts work)
- `proposed → deferred` (Showrunner deprioritizes)
- `proposed → rejected` (Showrunner declines)
- `investigating → researched` (Researcher completes fact-check)
- `researched → drafting-canon` (Lore Weaver drafts canon pack)
- `drafting-canon → awaiting-gate` (Lore Weaver submits for review)
- `awaiting-gate → canonized` (Gatekeeper approves)

### Trace Unit (TU) Lifecycle (6 States)

```text
  hot-proposed
       │
       ↓
   stabilizing
       │
       ↓
   gatecheck
       │
       ├──────> hot-revision (if failed gate)
       │
       ↓
   cold-merged
       │
       ↓
   snapshotted
       │
       ↓
   exported
```

**Key Transition Rules:**

- Only **Gatekeeper** can advance `gatecheck → cold-merged`
- Only **Showrunner** can trigger `snapshotted`
- Only **Book Binder** can trigger `exported`

---

## Hot vs. Cold Architecture

### Hot (Discovery Space)

**Purpose:** Experimentation, brainstorming, spoiler content

**Contains:**

- Draft topology (unstable)
- Hook cards (unresolved ideas)
- Canon packs (spoiler-level lore)
- Internal notes & reasoning
- Failed experiments

**Access:** All roles except Player-Narrator (PN)

**Mutation:** Freely mutable, no quality gates

**Git Branch:** Typically `main` or feature branches

### Cold (Canon/Production)

**Purpose:** Curated, player-safe, export-ready content

**Contains:**

- Stable topology (validated reachability)
- Codex entries (no spoilers)
- Player-facing prose
- Asset references
- Front matter

**Access:** All roles, including Player-Narrator (PN)

**Mutation:** Only via Gatekeeper-approved TUs

**Git Tags:** Snapshots tagged as `cold-YYYY-MM-DD`

### Why Two Sources?

1. **Safety:** PN never sees spoilers in Hot
2. **Quality:** Cold is always gate-checked
3. **Reproducibility:** Cold snapshots are immutable
4. **Freedom:** Hot allows experimentation without breaking canon

---

## Quality Enforcement

### The 7 Quality Bars

#### 1. Integrity

**Definition:** No broken references, valid IDs, consistent structure

**Checks:**

- All section IDs exist
- All gateway references valid
- All asset IDs in manifests

#### 2. Reachability

**Definition:** All keystone sections reachable from start

**Checks:**

- Graph traversal from `start_section_id`
- All mandatory gates accessible
- No orphaned subgraphs

#### 3. Nonlinearity

**Definition:** Hubs, loops, gateways are meaningful (not fake branching)

**Checks:**

- At least N% hubs (sections with 3+ choices)
- At least M loops (paths that revisit sections)
- Gateways have actual consequences

#### 4. Gateways

**Definition:** Diegetic checks are coherent and fair

**Checks:**

- Gateway logic is in-world explainable
- Gateway failures have narrative justification
- Gateway successes feel earned

#### 5. Style

**Definition:** Voice, register, motifs consistent

**Checks:**

- Tense consistency (present/past)
- POV consistency (2nd/1st person)
- Motif references valid
- Register appropriate to genre

#### 6. Determinism

**Definition:** Assets promised are present or scheduled

**Checks:**

- All referenced art IDs in `art_manifest`
- All audio cues in `cuelist`
- All translation keys in `language_pack`

#### 7. Presentation

**Definition:** No spoilers on player surfaces, accessibility baseline met

**Checks:**

- Codex entries contain no spoilers
- Front matter contains no plot reveals
- Alt text for images
- Screen reader compatibility

### Enforcement Process

1. **Author** submits TU from Hot
2. **Gatekeeper** runs automated checks
3. **Gatekeeper** performs manual review
4. **Gatekeeper** issues `gatecheck_report`:
   - ✅ Pass → TU advances to `cold-merged`
   - ❌ Fail → TU returns to `hot-revision` with feedback
5. **Showrunner** merges passed TUs to Cold

---

## Protocol Design

### Envelope Structure

All messages use a **transport-agnostic envelope**:

```json
{
  "protocol": "questfoundry/1.0.0",
  "id": "msg-20251105-143052-abc123",
  "time": "2025-11-05T14:30:52Z",
  "sender": "lore_weaver",
  "receiver": "gatekeeper",
  "intent": "gate.report.request",
  "context": {
    "tu_id": "TU-20251105-LW01",
    "source": "hot",
    "quality_bars": ["integrity", "presentation"]
  },
  "safety": {
    "player_safe": true,
    "sot": "cold"
  },
  "payload": {
    "type": "codex_entry",
    "data": { ... }
  }
}
```

### Key Fields

- **protocol**: Semantic version for forward compatibility
- **intent**: Dotted action (e.g., `hook.create`, `tu.advance`, `gate.report.submit`)
- **context**: Traceability metadata (TU IDs, sources, bars)
- **safety**: PN protection (must be `player_safe=true` and `sot=cold` for PN)
- **payload**: Artifact data validated against Layer 3 schemas

### Two-Pass Validation

1. **Pass 1:** Validate envelope structure (Layer 4 schema)
2. **Pass 2:** Validate `payload.data` against `payload.type` schema (Layer 3)

Example:

```bash
qfspec-check-envelope message.json
# → Validates envelope structure
# → Validates payload.data against codex_entry.schema.json
```

### Intent Domains

- **hook**: Hook lifecycle (`hook.create`, `hook.advance`, `hook.canonize`)
- **tu**: TU lifecycle (`tu.start`, `tu.advance`, `tu.merge`)
- **gate**: Quality checks (`gate.report.request`, `gate.report.submit`)
- **view**: Exports (`view.export.request`, `view.export.complete`)
- **role**: Role management (`role.wake`, `role.sleep`)
- **human**: Escalation (`human.clarify`, `human.approve`)
- **error**: Failures (`error.validation`, `error.conflict`)
- **ack**: Confirmations (`ack`)

---

## Extensibility

### Adding New Roles

1. Create charter in `01-roles/charters/{role_name}.md`
2. Create brief in `01-roles/briefs/{role_name}.md`
3. Add to `00-north-star/ROLE_INDEX.md`
4. Create system prompt in `05-prompts/{role_name}/system_prompt.md`
5. Update RACI matrix in `01-roles/raci/by_loop.md`

### Adding New Artifacts

1. Create template in `02-dictionary/artifacts/{artifact_name}.md`
2. Generate schema: `qfspec-generate-schema {artifact_name}`
3. Add to `03-schemas/{artifact_name}.schema.json`
4. Register in schema index
5. Update protocol examples

### Adding New Intents

1. Document intent in `04-protocol/INTENTS.md`
2. Define payload schema
3. Add example in `04-protocol/EXAMPLES/{intent_name}.json`
4. Update state machines if needed
5. Validate with `qfspec-check-envelope`

### Adding New Quality Bars

1. Document in `00-north-star/QUALITY_BARS.md`
2. Update Gatekeeper charter
3. Add validation logic to `spec-tools`
4. Update `gatecheck_report` schema

---

## Design Decisions

QuestFoundry's design is documented in **Architectural Decision Records (ADRs)** in the
[`DECISIONS/`](../DECISIONS/) directory.

### Key ADRs

- **ADR-20251029-01:** Layer Boundary Clarification (Layer 0/1/2 separation)
- _(More ADRs to be added as architectural decisions are made)_

### Decision-Making Process

1. **Identify architectural question**
2. **Copy ADR template** from `DECISIONS/ADR_TEMPLATE.md`
3. **Document context, decision, consequences**
4. **Submit PR for review**
5. **Merge when approved**

---

## Implementation Status

| Component            | Status      | Completion |
| -------------------- | ----------- | ---------- |
| Layer 0 (North Star) | ✅ Complete | 100%       |
| Layer 1 (Roles)      | ✅ Complete | 100%       |
| Layer 2 (Dictionary) | ✅ Complete | 100%       |
| Layer 3 (Schemas)    | ✅ Complete | 100%       |
| Layer 4 (Protocol)   | ✅ Complete | 95%        |
| Layer 5 (Prompts)    | ✅ Complete | 100%       |
| Layer 6 (Libraries)  | 📋 Planned  | 0%         |
| Layer 7 (UI)         | 📋 Planned  | 0%         |
| Validation Tools     | ✅ Complete | 100%       |

---

## Further Reading

- [Getting Started Guide](getting-started.md)
- [Implementation Roadmap](../IMPLEMENTATION_ROADMAP.md)
- [Protocol Specification](../04-protocol/ENVELOPE.md)
- [Quality Bars](../00-north-star/QUALITY_BARS.md)
- [ADRs](../DECISIONS/)

---

**Last Updated:** 2025-11-05
