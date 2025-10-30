# Layer 4 Envelope v1.0 — Transport-Agnostic Message Wrapper

> **Status:** Normative — this document defines the canonical envelope structure for all Layer 4 protocol messages.

---

## 1. Overview

The Layer 4 Envelope is a **transport-agnostic**, **versioned** wrapper that encapsulates Layer 3–validated payloads and encodes:
- **PN safety boundaries** (Hot/Cold, player-safe flags)
- **TU traceability** (trace unit linkage, snapshot context)
- **Message routing** (sender/receiver roles, intent verbs)
- **Correlation** (reply chains, upstream references)

### Purpose

The envelope provides:
1. **Protocol versioning** — semver-based evolution with forward compatibility
2. **Safety enforcement** — PN receives only Cold + player-safe content
3. **Traceability** — every change carries TU and snapshot context
4. **Intent clarity** — explicit message verbs and lifecycle states
5. **Transport independence** — same contract over HTTP, files, or events

### Design Principles

- **Minimal and explicit** — no implicit defaults that vary by transport
- **Canon-first** — payloads MUST validate against Layer 3 schemas
- **Player-safe boundaries** — safety flags are non-negotiable
- **Forward-compatible** — unknown fields are ignored, not errors

---

## 2. Fields

All envelope messages are JSON objects with the following top-level structure:

### 2.1 Protocol Metadata

#### `protocol` (object, REQUIRED)

Identifies the protocol name and version.

**Fields:**
- `name` (string, REQUIRED): MUST be `"qf-protocol"`
- `version` (string, REQUIRED): Protocol version in semver format (e.g., `"1.0.0"`)

**Example:**
```json
"protocol": {
  "name": "qf-protocol",
  "version": "1.0.0"
}
```

**Rules:**
- Unknown protocol names MUST be rejected
- Version compatibility follows semver: minor/patch changes are backward-compatible, major changes may break

---

### 2.2 Message Identity

#### `id` (string, REQUIRED)

Globally unique message identifier.

**Format:** URN or UUID  
**Example:** `"urn:uuid:550e8400-e29b-41d4-a716-446655440000"` or `"MSG-20251030-SR01-001"`

**Rules:**
- MUST be unique across all messages
- SHOULD use UUID v4 or timestamp-based URN for traceability
- MUST be immutable once assigned

#### `time` (string, REQUIRED)

Message creation timestamp.

**Format:** RFC3339 (ISO 8601 with timezone)  
**Example:** `"2025-10-30T12:19:29Z"`

**Rules:**
- MUST include timezone (UTC recommended)
- Receivers MAY use this for ordering, expiry, or audit trails

---

### 2.3 Routing

#### `sender` (object, REQUIRED)

Identifies the message sender.

**Fields:**
- `role` (string, REQUIRED): Role abbreviation from `02-dictionary/role_abbreviations.md` (e.g., `"SR"`, `"GK"`, `"LW"`)
- `agent` (string, OPTIONAL): Human or agent identifier (e.g., `"human:alice"`, `"bot:gk-v2.1"`)

**Example:**
```json
"sender": {
  "role": "SR",
  "agent": "human:alice"
}
```

#### `receiver` (object, REQUIRED)

Identifies the intended recipient.

**Fields:**
- `role` (string, REQUIRED): Role abbreviation from `02-dictionary/role_abbreviations.md`
- `agent` (string, OPTIONAL): Specific agent identifier (for direct routing)

**Example:**
```json
"receiver": {
  "role": "LW"
}
```

**Rules:**
- Messages MAY be broadcast (receiver role = `"*"`)
- Role abbreviations MUST match `02-dictionary/role_abbreviations.md`

---

### 2.4 Intent

#### `intent` (string, REQUIRED)

The message action or verb, namespaced by domain.

**Format:** `<namespace>.<verb>[.<subverb>]`

**Examples:**
- `"hook.create"` — create a new hook
- `"tu.open"` — open a new trace unit
- `"gate.report.submit"` — submit a gatecheck report
- `"merge.request"` — request merge to Cold
- `"ack"` — acknowledge receipt
- `"error.validation"` — validation error
- `"error.business_rule"` — business rule violation

**Rules:**
- Intent MUST match a defined verb in `04-protocol/INTENTS.md` (future deliverable)
- Unknown intents SHOULD be rejected unless explicitly forward-compatible

---

### 2.5 Context

#### `context` (object, REQUIRED)

Encodes Hot/Cold state, TU linkage, snapshot, and loop context.

**Fields:**
- `hot_cold` (string, REQUIRED): Content temperature  
  - Values: `"hot"` (work-in-progress, spoilers allowed) or `"cold"` (stable, player-safe)
- `tu` (string, OPTIONAL): Trace Unit ID (format: `TU-YYYY-MM-DD-RRnn`)
- `snapshot` (string, OPTIONAL): Cold snapshot reference (format: `"Cold @ YYYY-MM-DD"`)
- `loop` (string, REQUIRED): Loop name from `02-dictionary/loop_names.md` (display name format)

**Example:**
```json
"context": {
  "hot_cold": "cold",
  "tu": "TU-2025-10-30-SR01",
  "snapshot": "Cold @ 2025-10-28",
  "loop": "Lore Deepening"
}
```

**Rules:**
- `tu` is REQUIRED for messages targeting Cold (merges, gatechecks)
- `snapshot` is REQUIRED when referencing Cold content for reproducibility
- `loop` MUST match a display name from `02-dictionary/loop_names.md`

---

### 2.6 Safety

#### `safety` (object, REQUIRED)

Encodes player safety and spoiler policy.

**Fields:**
- `player_safe` (boolean, REQUIRED): Whether content is safe for PN/players
- `spoilers` (string, REQUIRED): Spoiler policy  
  - Values: `"allowed"` (Hot content, internal) or `"forbidden"` (Cold/PN surfaces)

**Example:**
```json
"safety": {
  "player_safe": true,
  "spoilers": "forbidden"
}
```

**Rules (non-negotiable):**
- **PN MUST only receive messages where:**
  - `context.hot_cold = "cold"` AND
  - `safety.player_safe = true` AND
  - `safety.spoilers = "forbidden"`
- Gatekeeper MUST verify safety flags before approving Cold merges
- Violation of PN safety boundaries is a critical error

---

### 2.7 Payload

#### `payload` (object, REQUIRED)

The message content, validated against a Layer 3 schema.

**Fields:**
- `type` (string, REQUIRED): Payload type name (matches schema filename without `.schema.json`)
- `$schema` (string, REQUIRED): Relative or absolute path to the JSON Schema in `03-schemas/`
- `data` (object, REQUIRED): The actual payload data

**Example:**
```json
"payload": {
  "type": "hook_card",
  "$schema": "../03-schemas/hook_card.schema.json",
  "data": {
    "header": {
      "short_name": "Shadow Toll at Wormhole 3",
      "id": "HK-20251030-01",
      "status": "proposed",
      "raised_by": "SR",
      "tu": "TU-2025-10-30-SR01",
      "edited": "2025-10-30",
      "slice": "Add recurring resource pressure at hub",
      "snapshot_context": "Cold @ 2025-10-28"
    },
    "classification": {
      "type_primary": "narrative",
      "bars_affected": ["Integrity", "Nonlinearity"],
      "blocking": "no"
    },
    "player_safe_summary": "New faction mechanic at major hub",
    "proposed_next_step": {
      "loop": "Lore Deepening",
      "owner_r": "LW",
      "accountable_a": "SR"
    },
    "acceptance_criteria": [
      "Canon entry for toll mechanism completed",
      "Integration points identified"
    ],
    "locations_links": {
      "locations": ["manuscript/sections/wormhole3.md"],
      "related_hooks": [],
      "lineage": "TU-2025-10-30-SR01"
    }
  }
}
```

**Rules:**
- `payload.data` MUST validate against the schema referenced by `payload.$schema`
- Schema path MAY be relative (from envelope location) or absolute URL
- Unknown payload types SHOULD be rejected
- Empty payloads are allowed for acks/errors (see Error Envelopes)

---

### 2.8 References

#### `refs` (array of strings, OPTIONAL)

Array of upstream IDs this message depends on or relates to.

**Allowed reference types:**
- Hook IDs (e.g., `"HK-20251024-03"`)
- TU IDs (e.g., `"TU-2025-10-28-LW02"`)
- ADR IDs (e.g., `"ADR-001-player-safety"`)
- Section IDs (e.g., `"manuscript/section-17.md"`)
- Message IDs (for reply chains)

**Example:**
```json
"refs": [
  "HK-20251024-03",
  "TU-2025-10-28-LW02",
  "manuscript/section-17.md"
]
```

**Rules:**
- References are informational; receivers MAY use for traceability
- Empty array `[]` or absent field both mean "no references"

---

### 2.9 Correlation

#### `correlation_id` (string, OPTIONAL)

Groups related messages in a conversation or workflow.

**Example:** `"corr-hook-harvest-2025-10-30"`

**Rules:**
- All messages in a logical workflow SHOULD share the same `correlation_id`
- Replies SHOULD preserve the original message's `correlation_id`

#### `reply_to` (string, OPTIONAL)

The `id` of the message this is replying to.

**Example:** `"urn:uuid:550e8400-e29b-41d4-a716-446655440000"`

**Rules:**
- MUST reference a valid message `id`
- Used for acks, errors, and status updates

---

## 3. Semantics

### 3.1 Message Lifecycle

1. **Creation** — sender assigns `id`, `time`, fills required fields
2. **Validation** — envelope structure validated, then payload against `$schema`
3. **Safety check** — if receiver is PN, enforce safety rules
4. **Routing** — transport layer delivers to `receiver.role`
5. **Processing** — receiver handles based on `intent`
6. **Reply** (optional) — receiver sends ack/error with `reply_to` set

### 3.2 Hot/Cold Boundary

- **Hot messages** (`context.hot_cold = "hot"`):
  - Used during active development/stabilization
  - May contain spoilers and internal notes
  - NOT safe for PN or player-facing tools
  
- **Cold messages** (`context.hot_cold = "cold"`):
  - Stable, merged content
  - Linked to a `snapshot` for reproducibility
  - MAY be player-safe (check `safety.player_safe`)

### 3.3 PN Safety Invariant

**The Player-Narrator (PN) MUST only receive messages that satisfy ALL of:**
1. `context.hot_cold = "cold"`
2. `safety.player_safe = true`
3. `safety.spoilers = "forbidden"`

**Enforcement points:**
- Gatekeeper pre-merge validation
- Transport routing layer (reject Hot→PN)
- PN ingestion validation (double-check)

### 3.4 TU Linkage

Changes targeting Cold (merges, gatechecks) MUST include:
- `context.tu` — the trace unit driving the change
- `context.snapshot` — the Cold snapshot being modified or validated

This enables traceability per `00-north-star/TRACEABILITY.md`.

---

## 4. Defaults and Forward Compatibility

### 4.1 Unknown Fields

Receivers MUST ignore unknown top-level or nested fields. This allows:
- Adding optional fields in minor versions
- Transport-specific metadata (e.g., HTTP headers as `_transport.http`)

### 4.2 Missing Optional Fields

- `sender.agent`, `receiver.agent` — default to role-level routing
- `context.tu`, `context.snapshot` — absent if not applicable (Hot work, acks)
- `refs` — empty array `[]` if absent
- `correlation_id`, `reply_to` — null if absent

### 4.3 Version Negotiation

- Receivers SHOULD support current major version
- Minor/patch version differences are compatible within a major version
- Receivers MAY reject older major versions (e.g., `protocol.version = "0.x.y"`)

---

## 5. Error Envelopes

Errors use the same envelope structure with:
- `intent` set to `"error.validation"`, `"error.business_rule"`, `"error.not_authorized"`, etc.
- `reply_to` referencing the failed message `id`
- `payload.data` describing the error

### 5.1 Error Payload Schema

Error payloads follow a simple structure (no Layer 3 schema required):

```json
{
  "code": "VALIDATION_FAILED",
  "message": "Payload data does not validate against schema",
  "details": {
    "schema_path": "../03-schemas/hook_card.schema.json",
    "validation_errors": [
      "header.id: does not match pattern ^HK-\\d{8}-...",
      "classification.bars_affected: must have at least 1 item"
    ]
  }
}
```

**Common error codes:**
- `VALIDATION_FAILED` — schema validation error
- `BUSINESS_RULE_VIOLATION` — policy violation (e.g., Hot→PN)
- `NOT_AUTHORIZED` — sender lacks permission
- `NOT_FOUND` — referenced entity missing
- `CONFLICT` — state conflict (e.g., TU already merged)

---

## 6. Examples

### 6.1 Example: Ack (Acknowledgment)

```json
{
  "protocol": {
    "name": "qf-protocol",
    "version": "1.0.0"
  },
  "id": "urn:uuid:a1b2c3d4-e5f6-4789-a012-3456789abcde",
  "time": "2025-10-30T12:20:00Z",
  "sender": {
    "role": "LW",
    "agent": "bot:lw-v1.5"
  },
  "receiver": {
    "role": "SR"
  },
  "intent": "ack",
  "context": {
    "hot_cold": "hot",
    "loop": "Lore Deepening"
  },
  "safety": {
    "player_safe": false,
    "spoilers": "allowed"
  },
  "payload": {
    "type": "ack",
    "$schema": null,
    "data": {
      "message": "Hook HK-20251030-01 received and queued"
    }
  },
  "refs": [],
  "correlation_id": "corr-hook-harvest-2025-10-30",
  "reply_to": "urn:uuid:550e8400-e29b-41d4-a716-446655440000"
}
```

### 6.2 Example: Validation Error

```json
{
  "protocol": {
    "name": "qf-protocol",
    "version": "1.0.0"
  },
  "id": "urn:uuid:f1e2d3c4-b5a6-4987-8765-43210fedcba0",
  "time": "2025-10-30T12:25:00Z",
  "sender": {
    "role": "GK",
    "agent": "bot:gk-validator"
  },
  "receiver": {
    "role": "SS"
  },
  "intent": "error.validation",
  "context": {
    "hot_cold": "hot",
    "loop": "Gatecheck"
  },
  "safety": {
    "player_safe": false,
    "spoilers": "allowed"
  },
  "payload": {
    "type": "error",
    "$schema": null,
    "data": {
      "code": "VALIDATION_FAILED",
      "message": "Payload data does not validate against schema",
      "details": {
        "schema_path": "../03-schemas/hook_card.schema.json",
        "validation_errors": [
          "header.id: does not match pattern ^HK-\\d{8}-(0[1-9]|[1-9]\\d{1,2})$",
          "classification.bars_affected: must have at least 1 item"
        ]
      }
    }
  },
  "refs": [],
  "correlation_id": "corr-gatecheck-2025-10-30",
  "reply_to": "urn:uuid:123e4567-e89b-12d3-a456-426614174000"
}
```

### 6.3 Example: Business Rule Error (PN Safety Violation)

```json
{
  "protocol": {
    "name": "qf-protocol",
    "version": "1.0.0"
  },
  "id": "urn:uuid:deadbeef-cafe-4444-8888-000011112222",
  "time": "2025-10-30T12:30:00Z",
  "sender": {
    "role": "BB",
    "agent": "bot:binder-v2"
  },
  "receiver": {
    "role": "SR"
  },
  "intent": "error.business_rule",
  "context": {
    "hot_cold": "hot",
    "loop": "Binding Run"
  },
  "safety": {
    "player_safe": false,
    "spoilers": "allowed"
  },
  "payload": {
    "type": "error",
    "$schema": null,
    "data": {
      "code": "BUSINESS_RULE_VIOLATION",
      "message": "Attempted to route Hot content to PN",
      "details": {
        "rule": "PN_SAFETY_INVARIANT",
        "violation": "context.hot_cold='hot' but receiver.role='PN'",
        "reference": "00-north-star/PN_PRINCIPLES.md",
        "remedy": "Ensure content is merged to Cold and marked player_safe=true before PN ingestion"
      }
    }
  },
  "refs": [
    "00-north-star/PN_PRINCIPLES.md"
  ],
  "correlation_id": "corr-binding-2025-10-30",
  "reply_to": "urn:uuid:badc0ffe-1234-5678-9abc-def012345678"
}
```

### 6.4 Example: Hook Creation (Full Payload)

```json
{
  "protocol": {
    "name": "qf-protocol",
    "version": "1.0.0"
  },
  "id": "urn:uuid:550e8400-e29b-41d4-a716-446655440000",
  "time": "2025-10-30T12:19:29Z",
  "sender": {
    "role": "SR",
    "agent": "human:alice"
  },
  "receiver": {
    "role": "LW"
  },
  "intent": "hook.create",
  "context": {
    "hot_cold": "hot",
    "tu": "TU-2025-10-30-SR01",
    "snapshot": null,
    "loop": "Hook Harvest"
  },
  "safety": {
    "player_safe": false,
    "spoilers": "allowed"
  },
  "payload": {
    "type": "hook_card",
    "$schema": "../03-schemas/hook_card.schema.json",
    "data": {
      "header": {
        "short_name": "Shadow Toll at Wormhole 3",
        "id": "HK-20251030-01",
        "status": "proposed",
        "raised_by": "SR",
        "tu": "TU-2025-10-30-SR01",
        "edited": "2025-10-30",
        "slice": "Add recurring resource pressure at major hub",
        "snapshot_context": "Cold @ 2025-10-28"
      },
      "classification": {
        "type_primary": "narrative",
        "bars_affected": ["Integrity", "Nonlinearity"],
        "blocking": "no"
      },
      "player_safe_summary": "New faction mechanic at major hub",
      "proposed_next_step": {
        "loop": "Lore Deepening",
        "owner_r": "LW",
        "accountable_a": "SR"
      },
      "acceptance_criteria": [
        "Canon entry for toll mechanism completed",
        "Integration points with existing factions identified"
      ],
      "locations_links": {
        "locations": ["manuscript/sections/wormhole3.md"],
        "related_hooks": [],
        "lineage": "TU-2025-10-30-SR01"
      }
    }
  },
  "refs": [
    "HK-20251024-03",
    "TU-2025-10-28-LW02"
  ],
  "correlation_id": "corr-hook-harvest-2025-10-30",
  "reply_to": null
}
```

### 6.5 Example: Cold Content for PN (Player-Safe)

```json
{
  "protocol": {
    "name": "qf-protocol",
    "version": "1.0.0"
  },
  "id": "urn:uuid:c0ffeeee-1111-2222-3333-444455556666",
  "time": "2025-10-30T14:00:00Z",
  "sender": {
    "role": "BB",
    "agent": "bot:binder-v2"
  },
  "receiver": {
    "role": "PN"
  },
  "intent": "view.export.result",
  "context": {
    "hot_cold": "cold",
    "tu": "TU-2025-10-28-BB01",
    "snapshot": "Cold @ 2025-10-28",
    "loop": "Binding Run"
  },
  "safety": {
    "player_safe": true,
    "spoilers": "forbidden"
  },
  "payload": {
    "type": "view_log",
    "$schema": "../03-schemas/view_log.schema.json",
    "data": {
      "view_name": "main-export-v1",
      "snapshot": "Cold @ 2025-10-28",
      "export_options": {
        "include_art_plans": false,
        "include_codex": true
      },
      "manifest": [
        "manuscript/section-01.md",
        "manuscript/section-02.md",
        "codex/factions.md"
      ]
    }
  },
  "refs": [
    "TU-2025-10-28-BB01"
  ],
  "correlation_id": "corr-binding-2025-10-28",
  "reply_to": "urn:uuid:aabbccdd-0011-2233-4455-667788990011"
}
```

---

## 7. Normative Rules Summary

### MUST Requirements

1. **Envelope Structure:**
   - All messages MUST include: `protocol`, `id`, `time`, `sender`, `receiver`, `intent`, `context`, `safety`, `payload`
   - `protocol.name` MUST be `"qf-protocol"`
   - `protocol.version` MUST be valid semver

2. **PN Safety (non-negotiable):**
   - PN MUST only receive messages where:
     - `context.hot_cold = "cold"` AND
     - `safety.player_safe = true` AND
     - `safety.spoilers = "forbidden"`
   - Violation is a critical error

3. **Payload Validation:**
   - `payload.data` MUST validate against the schema at `payload.$schema`
   - Unknown payload types MUST be rejected

4. **TU Linkage:**
   - Messages targeting Cold (merges, gatechecks) MUST include `context.tu`
   - Cold content MUST include `context.snapshot` for reproducibility

5. **Traceability:**
   - Changes affecting Cold MUST reference upstream TU/hooks via `refs` or `context.tu`

### SHOULD Requirements

1. **Message Identity:**
   - `id` SHOULD use UUID v4 or timestamp-based URN
   - `time` SHOULD use UTC timezone

2. **Correlation:**
   - Related messages SHOULD share `correlation_id`
   - Replies SHOULD set `reply_to` to the original message `id`

3. **References:**
   - Messages SHOULD include `refs` for traceability when applicable

4. **Forward Compatibility:**
   - Receivers SHOULD ignore unknown fields
   - Receivers SHOULD support at least current major version

---

## 8. Cross-References

- **Policy:** `00-north-star/PN_PRINCIPLES.md`, `00-north-star/TRACEABILITY.md`
- **Roles:** `02-dictionary/role_abbreviations.md`
- **Loops:** `02-dictionary/loop_names.md`
- **Schemas:** `03-schemas/*.schema.json`
- **Intents:** `04-protocol/INTENTS.md` (future)
- **Lifecycles:** `04-protocol/LIFECYCLES/*.md` (future)
- **Transports:** `04-protocol/APPENDIX/transport-*.md` (future, non-normative)

---

## 9. Appendix: Transport Mappings (Non-Normative)

Transport-specific mappings (HTTP, files, events) are **non-normative** and documented separately in `04-protocol/APPENDIX/`. The envelope contract above is transport-independent.

**Key principle:** Any transport MUST preserve all envelope fields and enforce safety rules. Transport metadata (headers, filenames, topics) is supplementary.

---

**Version:** 1.0.0  
**Last Updated:** 2025-10-30  
**Authors:** QuestFoundry Layer 4 Working Group
