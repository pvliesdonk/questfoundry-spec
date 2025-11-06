# Protocol Changelog

All notable changes to QuestFoundry protocol specifications will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Status

Layer 4 (Protocol) is currently at **95% completion** and has not yet been formally versioned.
Protocol specifications are evolving as a living document.

When Layer 4 stabilizes, the first formal release will be tagged as `protocol-v1.0.0`.

### Current Components (Unversioned)

**Core Protocol:**

- `ENVELOPE.md` — Message envelope structure (transport-agnostic, versioned wrapper)
- `envelope.schema.json` — JSON Schema for envelope validation
- `CONFORMANCE.md` — Protocol conformance requirements

**Intent Specifications:**

- `INTENTS.md` — Intent taxonomy and routing rules
- Intent examples in `EXAMPLES/intents/`

**Lifecycle Definitions:**

- `LIFECYCLES/hooks.md` — Hook lifecycle states and transitions
- `LIFECYCLES/tu.md` — Trace Unit (TU) lifecycle
- `LIFECYCLES/gate.md` — Gatecheck workflow
- `LIFECYCLES/view.md` — View export workflow

**Flow Specifications:**

- `FLOWS/hook_harvest_lore.md` — Hook Harvest + Lore Deepening flow
- `FLOWS/codex_gate_merge.md` — Codex Expansion + Gatecheck + Merge flow
- `FLOWS/binding_pn.md` — Binding Run + Narration Dry-Run flow
- Additional loop flows

**Examples:**

- `EXAMPLES/envelopes/` — Complete envelope examples
- `EXAMPLES/intents/` — Intent payload examples
- `EXAMPLES/flows/` — Multi-message flow sequences

### Planned for v1.0.0

When protocol stabilizes, the first release will include:

**Added:**

- Complete envelope specification with all required fields
- Intent taxonomy covering all 13 loops
- Lifecycle state machines for all artifact types
- Flow specifications for all workflow patterns
- Conformance test suite

**Changed:**

- TBD based on stabilization feedback

**Deprecated:**

- TBD based on stabilization feedback

**Removed:**

- TBD based on stabilization feedback

**Fixed:**

- TBD based on stabilization feedback

**Security:**

- TBD based on stabilization feedback

---

## Version Numbering Strategy

Protocol versions will follow **Semantic Versioning**:

- **Major (X.0.0)**: Breaking changes to envelope structure, intent taxonomy, or required fields
- **Minor (1.X.0)**: New intents, new lifecycle states, backward-compatible additions
- **Patch (1.0.X)**: Clarifications, documentation fixes, example updates

### Breaking Change Policy

Breaking changes require:

1. Major version bump
2. Migration guide in release notes
3. Deprecation notice in previous minor version (when possible)
4. Support window for old version (TBD by maintainers)

### Backward Compatibility

- Envelope `protocol.version` field enables version negotiation
- New intents are backward-compatible (ignored by old implementations)
- New optional fields are backward-compatible
- Required field additions are breaking changes

---

## Release Process

When cutting a protocol release:

1. Update this CHANGELOG.md with complete release notes
2. Update `04-protocol/README.md` with new version status
3. Commit: `protocol: bump to vX.Y.Z`
4. Tag: `git tag -a protocol-vX.Y.Z -m "Release protocol vX.Y.Z: description"`
5. Push: `git push origin protocol-vX.Y.Z`
6. Create GitHub release with changelog excerpt
7. Update dependent documentation (Layer 5 prompts if needed)

---

## Relationship to Schema Versions

- **Protocol versions** (Layer 4) are independent of **schema versions** (Layer 3)
- Protocol specifies message structure (envelope, intents, flows)
- Schemas specify artifact payload structure (hook cards, TU briefs, etc.)
- A protocol version may reference specific schema versions in documentation
- Breaking schema changes do not automatically require protocol version bump

Example:

- `protocol-v1.0.0` may work with `schemas-v0.2.0` through `schemas-v0.5.0`
- If envelope structure changes, bump protocol version
- If artifact payload structure changes, bump schema version

---

## Notes

- Protocol specifications are currently evolving as Layer 4 approaches 100%
- First formal release expected when Layer 4 stabilizes
- See `03-schemas/CHANGELOG.md` for artifact schema version history
- See root `README.md` for overall layer completion status

---

**Changelog created:** 2025-11-06 **First protocol version:** TBD (expected: protocol-v1.0.0 when
Layer 4 reaches 100%)

[Unreleased]: https://github.com/pvliesdonk/questfoundry-spec/tree/main/04-protocol
