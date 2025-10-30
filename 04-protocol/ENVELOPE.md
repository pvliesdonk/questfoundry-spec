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

---

### 2.4 Context

#### `context` (object, REQUIRED)

Provides traceability and safety context.

**Fields:**

- `hot_cold` (string, REQUIRED): MUST be `"hot"` or `"cold"`

- `tu` (string, OPTIONAL): Trace Unit identifier

- `snapshot` (string, OPTIONAL): Snapshot context (e.g., `"Cold @ 2025-10-25"`)

- `loop` (string, OPTIONAL): Loop name

**Rules:**

- `hot_cold` MUST be `"cold"` for PN

- `snapshot` is REQUIRED for PN

---

### 2.5 Safety

#### `safety` (object, REQUIRED)

Enforces player-safe boundaries.

**Fields:**

- `player_safe` (boolean, REQUIRED): MUST be `true` for PN

- `spoilers` (string, REQUIRED): MUST be `"allowed"` or `"forbidden"`

---

### 2.6 Payload

#### `payload` (object, REQUIRED)

Encapsulates the Layer 3–validated data.

**Fields:**

- `type` (string, REQUIRED): Payload type (e.g., `"hook_card"`)

- `data` (object, REQUIRED): Layer 3–validated payload

---

### 2.7 References

#### `refs` (array, OPTIONAL)

Provides upstream references.

**Fields:**

- Items: Unique strings

---

## 3. Examples

### Example 1: Hook Creation

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
    "hot_cold": "cold",
    "snapshot": "Cold @ 2025-10-25"
  },
  "safety": {
    "player_safe": true,
    "spoilers": "forbidden"
  },
  "payload": {
    "type": "hook_card",
    "data": {}
  },
  "refs": []
}
```
