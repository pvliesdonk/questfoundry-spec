# Feedback Loop — v1.0.0 (Protocol 1.0.0)

This release keeps the 1.0.0 feedback protocol but cleans examples and docs. See `schemas/feedback.schema.json` and `examples/contracts/feedback.annotated.json`.

**Lifecycle:** drafting → revision → stabilizing → stable. Orchestrator increments `cycle` and enforces `ttl_cycles`.

**Message classes:** beat_revision_request/response, world_extension_proposal/decision, plot_push_update, section_rewrite_request/response, research_request/response, note, error.

**Anchors:** refs.plot, refs.section, refs.canon.

**Diffs:** minimal JSON-Patch ops (add/remove/replace).
