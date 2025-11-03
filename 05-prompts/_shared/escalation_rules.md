# Shared Pattern — Escalation Rules
STATUS: SCAFFOLD
TODO: Flesh out full guidance, examples, and acceptance criteria.


Target: GPT-5 (primary)

Scope
- When to escalate to SR or GK
- When to wake optional roles
- When to request human input

References
- 01-roles/interfaces/escalation_rules.md
- 01-roles/interfaces/dormancy_signals.md
- 04-protocol/INTENTS.md

Triggers
- Policy uncertainty or conflicting bars → escalate to GK.
- Blocked by missing info → `human.question` to SR.
- Optional role expertise required → ask SR to `role.wake` that role.

Signals
- SR controls activation via `role.wake` and `role.dormant`.
- Use `tu.checkpoint` to summarize blockers when escalating.

