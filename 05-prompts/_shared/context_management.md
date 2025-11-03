# Shared Pattern — Context Management

STATUS: SCAFFOLD TODO: Flesh out full guidance, examples, and acceptance criteria.

Target: GPT-5 (primary)

Scope

- Maintain TU and loop awareness
- Track Hot/Cold, snapshot, and recent artifacts
- Manage conversation history within session limits

References

- 04-protocol/ENVELOPE.md
- 04-protocol/INTENTS.md
- 00-north-star/TRACEABILITY.md
- 04-protocol/LIFECYCLES/tu.md

Guidelines

- Always populate `context.hot_cold`; include `context.loop` during active loops.
- When referencing Cold content, ensure `context.snapshot` is present.
- Keep a rolling conversation buffer; summarize older turns when approaching context limits.
- Link upstream artifacts by ID in `refs` when relevant (hooks, TUs, canon entries).
- For checkpoints, emit `tu.checkpoint` with a concise `summary`.

Session Life Cycle

- Session begins when SR opens a TU (`tu.open`).
- Agents stay active for the loop duration; SR may send `role.wake` / `role.dormant`.
- Archive conversation history at TU close.

Examples

- See 04-protocol/EXAMPLES/tu.checkpoint.json
