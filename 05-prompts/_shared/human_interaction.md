# Shared Pattern — Human Interaction

STATUS: SCAFFOLD TODO: Flesh out full guidance, examples, and acceptance criteria.

Target: GPT-5 (primary)

Scope

- Ask clear, actionable questions when needed
- Provide just enough context and options
- Interpret free-form answers reliably

References

- 04-protocol/INTENTS.md (human.question / human.response)
- 04-protocol/EXAMPLES/human.question.json
- 04-protocol/EXAMPLES/human.response.json

When to Ask

- Ambiguity that blocks progress (tone, stakes, constraints).
- Choice among design options that change scope or style.
- Missing facts best provided by the author.

How to Ask

- One specific question per message.
- Include short context and 2–4 suggestions when possible.
- Avoid chatty follow-ups; batch where reasonable.

Interpreting Answers

- Treat `choice` as authoritative when present; otherwise use `answer` text.
- Acknowledge via `ack` only when needed; proceed with updated plan.


