# Using Layer 5 Prompts To Produce Your First Manuscript — A Practical Guide

Audience: humans using ChatGPT, Claude, or Gemini to run QuestFoundry Layer 5 prompts.

## Quick Start

- Choose a chatbot (ChatGPT, Claude, or Gemini).
- Upload the Minimal Upload Kit (files listed below) or paste the core prompts in order.
- Tell the bot to act as Showrunner and open a TU for your manuscript.
- Wake Plotwright, Scene Smith, and Style Lead; iterate outline → scenes → style.
- Pre-gate with Gatekeeper, bind with Book Binder, and do a PN dry-run.
- Close the TU when satisfied.

## Supported Chatbots And File Uploads

- ChatGPT
  - Supports attaching multiple files per conversation. Prefer uploading individual `.md` files.
  - Zips may work but are inconsistently previewed; prefer individual files for transparency.
  - Keep filenames descriptive (they are visible in the UI for quick reference).
- Claude
  - Handles multiple attachments well and summarizes them; large contexts are supported.
  - Zips are often accepted, but individual files provide better inline citation and grounding.
- Gemini
  - Supports attachments; behavior varies by interface. Prefer individual files; if using zips,
    keep them small and clearly named.

Tip: If your platform drops attachments between threads, reattach the Minimal Upload Kit at the start
of each new session.

## Upload Kits (Minimal vs. Full)

Minimal Upload Kit (recommended to start)

- 05-prompts/\_shared/context_management.md
- 05-prompts/\_shared/safety_protocol.md
- 05-prompts/\_shared/escalation_rules.md
- 05-prompts/\_shared/human_interaction.md
- 05-prompts/showrunner/system_prompt.md
- 05-prompts/plotwright/system_prompt.md
- 05-prompts/scene_smith/system_prompt.md
- 05-prompts/style_lead/system_prompt.md
- 05-prompts/gatekeeper/system_prompt.md
- 05-prompts/book_binder/system_prompt.md
- 05-prompts/player_narrator/system_prompt.md

Full Upload Kit (add later as needed)

- All Minimal kit files, plus additional role prompts:
  - 05-prompts/lore_weaver/system_prompt.md
  - 05-prompts/codex_curator/system_prompt.md
  - 05-prompts/researcher/system_prompt.md
  - 05-prompts/art_director/system_prompt.md
  - 05-prompts/illustrator/system_prompt.md
  - 05-prompts/audio_director/system_prompt.md
  - 05-prompts/audio_producer/system_prompt.md
  - 05-prompts/translator/system_prompt.md

See also: 05-prompts/upload_kits/ for copy‑pasta file lists and zip commands.

## Boot Sequence (Paste Or Upload, Then Prompt)

1. Upload Minimal Upload Kit (or paste in order): shared patterns → Showrunner → other roles.
2. Send this message to initialize Showrunner as orchestrator:

```
You are the Showrunner. Load and follow the uploaded shared patterns and your system prompt.
Open a new TU for a short manuscript (3–5 scenes). Use tu.open and produce a tu_brief payload
with loop "Story Spark". Target Cold snapshot "Cold @ YYYY-MM-DD" (pick today). After opening,
reply with a gate-safe summary and a plan to wake core roles (Plotwright, Scene Smith, Style Lead).
```

3. Approve the TU plan. Then send:

```
Wake Plotwright, Scene Smith, and Style Lead for this TU. Plotwright: propose a compact outline
(3–5 scenes) with any gateways. Scene Smith: draft the first scene from that outline in the agreed
register. Style Lead: be ready to audit/register‑tune the draft.
```

4. Iterate outline → scene → style. Keep messages short and actionable. Encourage Scene Smith to
   emit `tu.checkpoint` summaries after each scene.

5. Run a pre‑gate check:

```
Gatekeeper: run a pre‑gate on the manuscript. Evaluate Presentation, Integrity, and Style with
player‑safe evidence. Produce a brief gatecheck report and any smallest viable fixes.
```

6. Address gate feedback, then ask Book Binder to bind a player‑safe view:

```
Book Binder: produce a Markdown view for the current Cold snapshot. Include an anchor map summary.
Return a view.export.result envelope with export_artifacts.
```

7. PN dry‑run (Cold + player‑safe only):

```
Player‑Narrator: perform a brief dry‑run of the bound Markdown. Enforce gateways diegetically,
never leak internals. Submit pn.playtest.submit with issues and smallest fixes.
```

8. Close the TU when satisfied:

```
Showrunner: if all bars are green, close the TU. Summarize outcomes, link artifacts, and record
remaining debt if any.
```

## Role Cheat Sheets (What To Ask)

- Showrunner (SR)
  - Open TU, wake/dormant roles, plan loops, run checkpoints.
  - Useful prompt: “Open TU, propose plan, and wake PW/SS/ST for a 3–5 scene manuscript.”
- Plotwright (PW)
  - Propose outline, hubs/gateways, and nonlinearity constraints.
  - Useful prompt: “Draft a compact outline (3–5 scenes), note any gateways and consequences.”
- Scene Smith (SS)
  - Draft scenes, keep register and continuity; emit checkpoints.
  - Useful prompt: “Write Scene 1 per the outline; add a tu.checkpoint with a 1–2 line summary.”
- Style Lead (ST)
  - Audit tone/register; propose targeted rewrites, update register hints.
  - Useful prompt: “Audit Scene 1 for register drift; propose minimal rewrites.”
- Gatekeeper (GK)
  - Evaluate bars (Presentation, Integrity, Style, etc.) with player‑safe evidence.
  - Useful prompt: “Pre‑gate manuscript; list smallest fixes per bar; don’t leak spoilers.”
- Book Binder (BB)
  - Bind views (Markdown/HTML), summarize anchors, return export artifacts.
  - Useful prompt: “Bind to Markdown for PN; include anchor_map summary; return paths.”
- Player‑Narrator (PN)
  - Perform in‑world; enforce gateways diegetically; report issues.
  - Useful prompt: “Dry‑run performance; never leak internals; send pn.playtest.submit with issues.”
- Lore Weaver (LW) [optional early]
  - If working from canon, provide player‑safe summaries and continuity checks.
- Codex Curator (CC) [optional]
  - Produce codex entries for terms; can run in parallel after draft.
- Art Director / Illustrator (AD/IL) [optional]
  - Shotlists and art prompts after manuscript stabilizes.
- Audio Director / Producer (AuD/AuP) [optional]
  - Cuelist and renders after structure stabilizes.
- Translator (TR) [optional]
  - Localize after English pass; keep style/register consistent.

## Safety, Context, And Memory Tips

- PN Safety: Never route Hot content to PN. If PN is receiver, enforce Cold + `player_safe=true` + `snapshot`.
- Context Pressure: Summarize older turns as state notes; keep raw quotes only when needed.
- Traceability: Maintain `correlation_id` and use `refs` to link artifacts.
- Escalation: Use `human.question` when blocked; propose options and a default.

## Appendix — Uploading Files And Zipping Kits

Upload individually (preferred): Drag the listed `.md` files into your chat. Keep filenames intact.

Zip (if supported by your chatbot):

- PowerShell
  - `Compress-Archive -Path @(
  '05-prompts/_shared/context_management.md',
  '05-prompts/_shared/safety_protocol.md',
  '05-prompts/_shared/escalation_rules.md',
  '05-prompts/_shared/human_interaction.md',
  '05-prompts/showrunner/system_prompt.md',
  '05-prompts/plotwright/system_prompt.md',
  '05-prompts/scene_smith/system_prompt.md',
  '05-prompts/style_lead/system_prompt.md',
  '05-prompts/gatekeeper/system_prompt.md',
  '05-prompts/book_binder/system_prompt.md',
  '05-prompts/player_narrator/system_prompt.md'
) -DestinationPath minimal-upload-kit.zip -Force`
- Bash
  - `zip -r minimal-upload-kit.zip \
  05-prompts/_shared/context_management.md \
  05-prompts/_shared/safety_protocol.md \
  05-prompts/_shared/escalation_rules.md \
  05-prompts/_shared/human_interaction.md \
  05-prompts/showrunner/system_prompt.md \
  05-prompts/plotwright/system_prompt.md \
  05-prompts/scene_smith/system_prompt.md \
  05-prompts/style_lead/system_prompt.md \
  05-prompts/gatekeeper/system_prompt.md \
  05-prompts/book_binder/system_prompt.md \
  05-prompts/player_narrator/system_prompt.md`

For full kits and platform notes, see 05-prompts/upload_kits/README.md.
