# Layer 4 — Protocol (Interaction Rules)

> Status: Planned — this layer defines how roles communicate using validated, structured messages on top of Layer 3 schemas.

---

## Purpose

Layer 4 specifies HOW roles, tools, and agents exchange information: message envelopes, intents, lifecycles, and handshakes. It builds on:
- Layer 0 policies (PN, Hot/Cold, Quality Bars, Traceability)
- Layer 1 roles and pair interfaces (who talks to whom, why)
- Layer 2 common language (artifact types, taxonomies)
- Layer 3 JSON Schemas (payload shapes)

Layer 4 remains transport-agnostic. Concrete mappings (HTTP, files, events) are non-normative appendices.

---

## Design Pillars

- Canon-first: payloads MUST validate against Layer 3 schemas.
- Player-safe boundaries: PN only receives Cold + player-safe content.
- Traceable: every message carries TU and snapshot context where relevant.
- Minimal, explicit state machines: hooks, TUs, gates, and views.
- Replaceable transports: same contract over HTTP, files, or events.
- Versioned envelopes: semver, forward-compatible defaulting.

---

## Deliverables (Spec, not code)

- Envelope contract (fields, versioning, correlation, safety flags)
- Message intents and catalogs (e.g., hook.create, tu.open, gate.report.submit)
- Lifecycle/state machines (hooks, TU, gate, merge, view/export)
- Pairwise handshakes for key role interactions (Showrunner↔All, GK↔Owners, Binder↔PN)
- Validation rules tying envelope + payload to Layer 3 schemas
- Non-normative transport mappings (HTTP endpoints, file layout, event topics)
- Conformance suite outline and examples

---

## Directory Layout

```
04-protocol/
  README.md                  # Overview and pointers (this file)
  ENVELOPE.md                # ✅ Normative envelope spec (fields, versioning, safety)
  INTENTS.md                 # Message catalog (verbs, required payloads) [planned]
  LIFECYCLES/                # State machines (hooks, TU, gate, view)
    hooks.md                 # ✅ Hook lifecycle with state transitions
    tu.md                    # ✅ TU lifecycle with state transitions
    gate.md                  # [planned]
    view.md                  # [planned]
  FLOWS/                     # End-to-end handshakes per loop [planned]
    hook_harvest.md
    lore_deepening.md
    codex_expansion.md
    gatecheck.md
    binding_run.md
    narration_dry_run.md
  APPENDIX/                  # Non-normative mappings [planned]
    transport-http.md
    transport-files.md
    transport-events.md
  EXAMPLES/                  # Player-safe example messages and sequences [planned]
```

---

## Envelope Sketch (illustrative)

This is an illustrative example only (the normative spec will live in ENVELOPE.md):

```json
{
  "protocol": { "name": "qf-protocol", "version": "1.0.0" },
  "id": "urn:uuid:...",
  "time": "2025-10-30T12:00:00Z",
  "sender": { "role": "SR", "agent": "human:alice" },
  "receiver": { "role": "LW" },
  "intent": "hook.create",
  "context": {
    "hot_cold": "hot",
    "tu": "TU-2025-10-30-SR01",
    "snapshot": null,
    "loop": "Hook Harvest"
  },
  "safety": { "player_safe": false, "spoilers": "allowed" },
  "payload": {
    "type": "hook_card",
    "$schema": "../03-schemas/hook_card.schema.json",
    "data": { "header": { "short_name": "...", "id": "HK-20251030-01", "status": "proposed", "raised_by": "SR", "tu": "TU-2025-10-30-SR01", "edited": "2025-10-30", "slice": "...", "snapshot_context": "Cold @ 2025-10-25" }, "classification": { "type_primary": "narrative", "bars_affected": ["Integrity"], "blocking": "no" }, "player_safe_summary": "...", "proposed_next_step": { "loop": "Lore Deepening", "owner_r": "LW", "accountable_a": "SR" }, "acceptance_criteria": ["..."] }
  },
  "refs": ["HK-20251024-03"],
  "correlation_id": "...",
  "reply_to": "..."
}
```

---

## Cross-Layer Norms (must-haves)

- Envelopes MUST NOT leak Hot content to PN. PN receives only `hot_cold: "cold"` and `safety.player_safe: true` payloads.
- Gatekeeper decisions MUST cite Quality Bars and smallest viable fixes (see `03-schemas/gatecheck_report.schema.json`).
- Merge to Cold MUST carry snapshot ID (`Cold @ YYYY-MM-DD`) for Binder/PN reproducibility.
- TU linkage is REQUIRED for artifacts headed to Cold (see `00-north-star/TRACEABILITY.md`).

---

## Specifications

### Layer 4 Envelope v1.0

**Location:** [`ENVELOPE.md`](./ENVELOPE.md)

The normative specification for the transport-agnostic message envelope. Defines:
- Protocol metadata and versioning (semver)
- Message identity, routing, and intent
- Hot/Cold context and snapshot tracking
- PN safety boundaries (non-negotiable)
- TU traceability requirements
- Payload structure and schema validation
- Error handling and correlation
- Forward compatibility rules

**Status:** ✅ **Complete** — v1.0.0 specification with examples

See `ENVELOPE.md` for full details, field definitions, MUST/SHOULD rules, and JSON examples.

---

### Hook Lifecycle v1.0

**Location:** [`LIFECYCLES/hooks.md`](./LIFECYCLES/hooks.md)

The normative specification for Hook Card state transitions and protocol rules. Defines:
- 7-state lifecycle: proposed → accepted → in-progress → resolved → canonized (with deferred/rejected branches)
- Complete transition matrix with allowed sender roles
- Required message intents for each transition (hook.accept, hook.start, hook.resolve, etc.)
- Payload schemas and required fields per transition
- Error cases and validation rules
- Quality bar integration and blocking hook enforcement
- Envelope context requirements and examples

**Status:** ✅ **Complete** — v1.0.0 specification with transition matrix and examples

See `LIFECYCLES/hooks.md` for state machine, authorization rules, and JSON message examples.

---

### TU Lifecycle v1.0

**Location:** [`LIFECYCLES/tu.md`](./LIFECYCLES/tu.md)

The normative specification for Trace Unit (TU) state transitions and protocol rules. Defines:
- 6-state lifecycle: hot-proposed → stabilizing → gatecheck → cold-merged (with deferred/rejected branches)
- Complete transition matrix with allowed sender roles
- Required message intents for each transition (tu.start, tu.submit_gate, tu.merge, etc.)
- Payload schemas and required fields per transition
- Error cases and validation rules
- Quality bar integration and gatecheck enforcement
- Cold-bound requirement (any artifact for Cold MUST have a TU)
- Dormancy/deferral integration with wake rubric
- Envelope context requirements and examples

**Status:** ✅ **Complete** — v1.0.0 specification with transition matrix and examples

See `LIFECYCLES/tu.md` for state machine, authorization rules, quality gates, and JSON message examples.

---

## Status & Next Steps

**Completed:**
- ✅ Phase 1: Envelope v1.0 specification
- ✅ Phase 2 (Partial): Lifecycles & state machines
  - ✅ `LIFECYCLES/hooks.md` — Hook Card lifecycle with all state transitions
  - ✅ `LIFECYCLES/tu.md` — Trace Unit lifecycle with all state transitions

**Next:**
- Phase 2 (Remaining): Gate and View lifecycles
- Phase 3: Message intents & catalogs
- Phase 4: End-to-end flows per loop

See `LAYER4_PLAN.md` at repository root for the full phased implementation plan, success criteria, and rollout timeline.

