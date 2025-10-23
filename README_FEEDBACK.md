# Feedback Loop — v3.3-qa (Protocol 3.2)

This release keeps the 3.2 feedback protocol but cleans examples and docs. See `schemas/feedback.schema.json` and `examples/contracts/feedback.annotated.json`.

**Lifecycle:** drafting → revision → stabilizing → stable. Orchestrator increments `cycle` and enforces `ttl_cycles`.

**Message classes:** beat_revision_request/response, world_extension_proposal/decision, plot_push_update, section_rewrite_request/response, research_request/response, note, error.

**Anchors:** refs.plot, refs.section, refs.canon.

**Diffs:** minimal JSON-Patch ops (add/remove/replace).
