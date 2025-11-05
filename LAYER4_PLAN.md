# Layer 4 Implementation Plan — Protocol (Interaction Rules)

> Goal: Specify a transport-agnostic, versioned protocol so roles and tools exchange validated,
> player-safe messages grounded in Layer 3 schemas and Layer 0–2 policy.

---

## Scope

- Define message envelope, intents, and role handshakes
- Define lifecycles/state machines for hooks, TUs, gatechecks, merges, and views
- Bind payloads to Layer 3 JSON Schemas
- Keep Player-Narrator isolated to Cold, player-safe content
- Provide non-normative transport mappings and conformance examples

Out of scope: Implementing prompts (L5), libraries/SDKs (L6), or UI (L7).

---

## Inputs & Constraints

- Policies: `00-north-star/PN_PRINCIPLES.md`, `QUALITY_BARS.md`, `SOURCES_OF_TRUTH.md`,
  `TRACEABILITY.md`
- Roles & interfaces: `01-roles/` (charters, briefs, pair guides)
- Common language: `02-dictionary/` (taxonomies, field registry, artifacts)
- Schemas: `03-schemas/*.schema.json` (canonical payload shapes)
- Tools: `spec-tools/` (schema/instance validators; extend to Layer 4 later)

Constraints:

- No spoilers on player-facing/PN surfaces
- TU linkage required for changes targeting Cold
- Gatekeeper decisions tied to Quality Bars

---

## Phases (high level)

1. Envelope v1.0
2. Lifecycles & state machines
3. Message intents & catalogs
4. End-to-end flows per loop
5. Validation & conformance
6. Transport mappings (appendix)
7. Governance & versioning
8. Rollout & repo/tooling integration

---

## Phase 1 — Envelope v1.0

Deliverables:

- `04-protocol/ENVELOPE.md`: normative fields and semantics
  - protocol.name/version (semver), id, time (RFC3339)
  - sender/receiver (role abbreviation + optional agent id)
  - intent (verb.namespace), correlation_id, reply_to
  - context: hot_cold, tu, snapshot (Cold @ YYYY-MM-DD), loop
  - safety: player_safe (bool), spoilers (allowed/forbidden)
  - payload: { type, $schema, data }
  - refs: upstream IDs (hooks, TUs, ADRs, sections)

Success criteria:

- Fields are minimal, unambiguous, and cover PN/GK/SR needs
- Default behaviors defined for unknown fields (forward-compat)
- Example envelopes provided for create/update/submit/ack/error

---

## Phase 2 — Lifecycles & State Machines

Deliverables (in `04-protocol/LIFECYCLES/`):

- `hooks.md` — aligns with `02-dictionary/taxonomies.md` Hook Status Lifecycle
- `tu.md` — TU states: hot-proposed → stabilizing → gatecheck → cold-merged | deferred | rejected
- `gate.md` — pre-gate → gatecheck decisions (pass | conditional pass | block) + remediation
- `view.md` — snapshot selected → export → PN dry-run → feedback

Success criteria:

- Allowed transitions defined, with who can trigger and required payloads
- Invalid transitions and error semantics documented
- Gatekeeper integration points highlighted

---

## Phase 3 — Message Intents & Catalogs

Deliverables:

- `04-protocol/INTENTS.md` — catalog of intents with required payload schemas:
  - hook.create, hook.update_status
  - tu.open, tu.update, tu.close
  - gate.report.submit, gate.decision
  - merge.request, merge.approve, merge.reject
  - view.export.request, view.export.result
  - pn.playtest.submit
  - error.report, ack

For each intent specify: purpose, sender→receiver, required envelope fields, payload `$schema`,
expected replies, and errors.

Success criteria:

- Every Layer 1 handoff has at least one corresponding intent
- Every Layer 3 schema that’s exchanged has a mapped intent
- Examples accompany each intent (EXAMPLES/)

---

## Phase 4 — End-to-End Flows (per loop)

Deliverables (in `04-protocol/FLOWS/`):

- Hook Harvest: SR triages hook.create → hook.update_status(accepted|deferred|rejected)
- Lore Deepening: SR→LW tu.open → canon_pack submit → GK pre-gate → merge.request
- Codex Expansion: LW→CC summaries → codex_entry submit → GK checks → merge
- Gatecheck: owners submit to GK → gate.report.submit → gate.decision + handoffs
- Binding Run: SR selects snapshot → BB view.export.request → PN dry-run → pn.playtest.submit

Success criteria:

- Each flow lists message sequence, roles, lifecycles touched
- PN only appears in Cold, player-safe legs
- Small, testable subflows identified for conformance

---

## Phase 5 — Validation & Conformance

Deliverables:

- Conformance examples in `04-protocol/EXAMPLES/` (player-safe)
- Tools updates (tracked; implemented in Layer 6):
  - Extend `tools` validators to check Layer 4 envelopes + payload `$schema`
  - Add pre-commit entry for future `04-protocol/*.schema.json` if/when we formalize envelope in
    JSON Schema

Success criteria:

- Example envelopes validate payloads against Layer 3
- Conformance doc lists MUST/SHOULD and a minimal test matrix

---

## Phase 6 — Transport Mappings (Appendix)

Deliverables:

- `APPENDIX/transport-http.md`: endpoints, verbs, status codes, idempotency
- `APPENDIX/transport-files.md`: file layout, naming, ack/error files
- `APPENDIX/transport-events.md`: topics, ordering, replay, retries

Success criteria:

- Clear, minimal mappings without changing normative contract
- Safety/visibility flags enforceable at mapping layer (e.g., PN routing)

---

## Phase 7 — Governance & Versioning

Deliverables:

- Versioning and deprecation policy (semver, feature flags, grace windows)
- Error taxonomy: validation_error, business_rule_violation, not_authorized, not_found, conflict

Success criteria:

- Back/forward-compat guidance documented
- Error handling consistent across intents

---

## Phase 8 — Rollout & Integration

Deliverables:

- `04-protocol/README.md` (overview) — done
- Populate ENVELOPE/INTENTS/LIFECYCLES/FLOWS/APPENDIX/EXAMPLES incrementally
- Update `spec-tools/README.md` "Adding New Layers" checklists (already present)
- Prepare PR checklist additions (no Hot→PN leaks; envelope completeness)

Success criteria:

- Repo contains Layer 4 spec docs with examples and traceable references
- Pre-commit comment placeholder extended to include L4 when schemas exist

---

## Timeline (estimate)

- Phase 1: 1 iteration (envelope)
- Phase 2: 1–2 iterations (lifecycles)
- Phase 3: 2 iterations (intents)
- Phase 4: 2 iterations (flows)
- Phase 5: 1 iteration (examples + conformance outline)
- Phase 6: 1 iteration (transport appendices)
- Phase 7: 0.5 iteration (governance)
- Phase 8: 0.5 iteration (rollout wiring)

Total: ~8–10 iterations depending on review density.

---

## Risks & Mitigations

- Scope creep into prompts/tools/UI → Keep Layer 4 transport-agnostic; defer concrete clients to
  Layer 6.
- Player-safety regressions → Mandatory safety flags and PN isolation in envelopes; GK checks in
  flows.
- Divergence from Layer 3 schemas → Pre-commit and conformance examples tied to 03-schemas.

---

## Next Actions

1. Draft `04-protocol/ENVELOPE.md` per Phase 1
2. Write `LIFECYCLES/hooks.md`, then `tu.md` and `gate.md`
3. Produce initial `INTENTS.md` covering hook/tu/gate
4. Add 3–5 EXAMPLES to validate envelope + payload wiring
5. Review with Showrunner + Gatekeeper for policy alignment
