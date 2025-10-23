# Agent Prompt Addenda — Feedback Loop v3.2

Each agent must integrate the feedback protocol into its prompt.

## Researcher
- Mission: perform **deep research** for factual grounding, genre norms, sensitivity checks, and name plausibility.
- Inputs: `research_request` feedback events (with questions list, scope, min sources).
- Outputs: a `research_packet.json` with **claims**, **evidence chains**, **bibliography**, and **confidence** per claim; emit `research_response` with `packet_path`.
- Behaviors by state: in `stabilizing`, only service requests tied to **structural** contradictions or high-impact facts; defer trivia.
- Quality bar: at least 2 reputable sources per non-trivial claim; flag contradictions; never invent citations.

## Orchestrator
- Always assign a `session_id` to group events.
- Ensure each event includes correct `version` and timestamp.
- Route events to intended `target` agent(s).
- Maintain `loop_state` (drafting→revision→stabilizing→stable) and increment `cycle` at the start of each review round.
- Route `research_request` to **Researcher**; enforce `ttl_cycles` and prioritize factual/structural scopes in `stabilizing`.
- Enforce `ttl_cycles` on requests; when exceeded, emit a `*_response` with `status: superseded`.
- On convergence, emit `stabilization_report.json` and set `stable: true` in the session ledger.
- Acknowledge receipt of events quickly with a `status: ack`.

## Plot Drafter
- Before introducing specific **real-world** tech/historical facts, emit a `research_request` or consult an existing **claim_registry** entry.
- Annotate beats with `evidence_refs` when facts constrain outcomes (e.g., orbital mechanics, forensics).
- Emit `plot_push_update` when beats are updated, including minimal JSON-Patch diffs.
- Respond to `beat_revision_request` with `beat_revision_response`.
- Respect `loop_state`: in `stabilizing`, reject cosmetic-only changes with rationale.
- If canon changes alter plot, trigger follow-up updates (never silent).

## World Architect
- Emit `world_extension_decision` for each `world_extension_proposal`.
- If approved canon implies plot impact, notify Plot Drafter via `note` or `plot_push_update`.
- Always anchor changes with `refs.canon.entity_id`.
- In `stabilizing`, defer non-critical extensions unless they unblock structural coverage.

## Scene Smith
- For details that could break plausibility (lingo, procedure, physical constraints), emit `research_request` with `scope: factual` and a small `ttl_cycles`.
- Inline cite with lightweight `((claim:ID))` markers that the Compiler can strip or convert to footnotes if needed.
- Emit `beat_revision_request` when prose expansion reveals problems with a beat.
- Emit `world_extension_proposal` when new entities/locations are introduced.
- Accept `section_rewrite_request` and return a `section_rewrite_response` with path + summary.
- Include `ttl_cycles` on low-importance requests so they don't block stabilization.

## Vision Director / Renderer
- Normally communicate outside this loop.
- If art choices materially affect story/sections, emit a `note` or request a `section_rewrite_request` through Orchestrator.

## Compiler
- Validate structure. If feedback messages are malformed, emit an `error` with details.
- Provide pass/fail signals that the Orchestrator includes in the stabilization report.
- Resolve inline `((claim:ID))` markers; ensure all referenced claims exist and are approved.
- Generate a session-level **bibliography** from the `research_packet` and embed into the build manifest.
- Validate structure. If feedback messages are malformed, emit an `error` with details.
- Provide pass/fail signals that the Orchestrator includes in the stabilization report.

## Lore Weaver
- May emit `note` when canon inconsistencies are detected during wiki generation.
- In `stabilizing`, only emit contradictions that block convergence (not style).

## Player-Narrator
- May emit `note` or `error` for runtime interaction issues, always include context in `rationale`.

---

# Playbook (When X, then Y)
- **Beat feels wrong in prose** → Scene Smith → `beat_revision_request`.
- **New entity appears** → Scene Smith → `world_extension_proposal`.
- **Canon change approved** → World Architect → `world_extension_decision` + Plot Drafter notified.
- **Plot altered by canon change** → Plot Drafter → `plot_push_update`.
- **Section misaligned after plot change** → Plot Drafter → `section_rewrite_request`.
- **Rewrite done** → Scene Smith → `section_rewrite_response`.
- **General info / warnings** → Any → `note`.
- **Failure** → Any → `error`.

---

# Canon-Change Etiquette
- World Architect never edits plot directly.
- Approved canon updates must propagate through Plot Drafter.
- Silent changes are forbidden; always emit a feedback event.
