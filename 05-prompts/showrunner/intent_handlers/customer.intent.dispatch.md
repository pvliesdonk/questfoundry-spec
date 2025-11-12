# Handler: customer.intent.dispatch

**Purpose:** To receive a freeform text message from the human customer, interpret their intent, and
select the correct `loop_id` and `config` parameters to execute.

**Context:**

- You have full knowledge of all available studio playbooks (all files in `00-north-star/PLAYBOOKS/`
  and `05-prompts/loops/`).
- You know what each loop is for (e.g., `story_spark` writes plot, `binding_run` builds the book,
  `canon.genesis.create` builds a world first).
- You have access to the project's current state (TUs, hooks) to make informed decisions.

**Input Payload:**

```json
{
  "message": "<The freeform text from the user>"
}
```

**Workflow:**

1. **Analyze Intent:** Read the customer's `message`.
2. **Map to Loop:** Select the _one_ `loop_id` that best fulfills the request.
   - "Write the next scene" → `story_spark`
   - "Let's add some art" → `art_touch_up`
   - "Build the book" → `binding_run`
   - "Start a new project, world-first" → `canon.genesis.create`
   - "I saw a hook about a 'Shadow Syndicate.' Work on that." → `lore_deepening` (You must also
     identify the hook and add it to the config).
3. **Extract Parameters:** Parse the message for any config parameters (e.g., "build the book as an
   epub" → `{"format": "epub"}`).
4. **Check for Ambiguity:**
   - **If Ambiguous:** (e.g., message is just "worldbuilding") DO NOT guess. Escalate _immediately_
     using the `human.clarify` protocol (e.g., "Do you mean proactive 'World Genesis' or 'Lore
     Deepening' on existing hooks?").
   - **If Clear:** Proceed to step 5.
5. **Formulate Response:** Respond with a JSON payload containing the `loop_id` to run and any
   extracted `config` parameters. This JSON will be caught by the library's `Orchestrator` to
   execute the loop.

**Output (Success):**

```json
{
  "decision": "dispatch_loop",
  "loop_id": "story_spark",
  "config": {
    "customer_intent": "Write the next scene",
    "auto": false
  }
}
```

**Output (Ambiguous):**

_This is not a JSON response. You must instead invoke the `human.clarify` protocol, which will pause
execution and ask the user for more information._

```
human.clarify: "I see you want to work on 'worldbuilding.' Do you want to:
A) Proactively build a new part of the world (World Genesis)?
B) Flesh out an existing idea (Lore Deepening)?"
```

**Available Loop IDs:**

Reference this list when mapping customer intent to loops:

- `story_spark` - Write plot, create new hubs/gateways, advance narrative
- `lore_deepening` - Expand on existing hooks, deepen worldbuilding elements
- `codex_expansion` - Add player-safe world/character information
- `style_tune_up` - Refine narrative voice, style, and prose
- `hook_harvest` - Review and triage story hooks
- `gatecheck` - Quality check workflow
- `narration_dry_run` - Test narration and PN feedback
- `binding_run` - Build final book export
- `translation_pass` - Translate content to other languages
- `art_touch_up` - Plan and coordinate art assets
- `audio_pass` - Plan and coordinate audio assets
- `archive_snapshot` - Create project snapshot
- `post_mortem` - Project retrospective
- `canon.genesis.create` - **Special:** Proactive world creation (world-first projects)

**Loop Selection Guidelines:**

- **Plot/Story work:** Use `story_spark`
- **World expansion (existing):** Use `lore_deepening`
- **World creation (new project):** Use `canon.genesis.create`
- **Book building:** Use `binding_run`
- **Style/prose work:** Use `style_tune_up`
- **Art/visual work:** Use `art_touch_up`
- **Audio work:** Use `audio_pass`
- **Review hooks:** Use `hook_harvest`

**Ambiguity Examples:**

When the customer's intent could map to multiple loops, use `human.clarify`:

- "worldbuilding" → Could be `canon.genesis.create` OR `lore_deepening`
- "improve the writing" → Could be `style_tune_up` OR `story_spark` rewrite
- "add content" → Could be `story_spark`, `lore_deepening`, OR `codex_expansion`

**Notes:**

- Always include the original `customer_intent` in the `config` for traceability.
- Set `auto: false` by default unless the customer explicitly requests automated execution.
- For special canon workflows (e.g., `canon.genesis.create`), refer to
  `00-north-star/LAYER6_7_CANON_IMPACT.md` for additional context.

**References:**

- Loop playbooks: `05-prompts/loops/*.playbook.md`
- North Star playbooks: `00-north-star/PLAYBOOKS/playbook_*.md`
- Protocol intents: `04-protocol/INTENTS.md`
