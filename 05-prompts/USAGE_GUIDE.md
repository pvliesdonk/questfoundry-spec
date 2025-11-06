# Using Layer 5 Prompts To Produce Your First Manuscript — A Practical Guide

Audience: humans using ChatGPT, Claude, or Gemini to run QuestFoundry Layer 5 prompts.

## Quick Start

- Choose a chatbot (ChatGPT, Claude, or Gemini).
- Upload the Minimal Upload Kit (files listed below) or paste the core prompts in order.
- Tell the bot to act as Showrunner and open a TU for your manuscript.
- Wake Plotwright, Scene Smith, and Style Lead; iterate outline → scenes → style.
- Pre-gate with Gatekeeper, bind with Book Binder, and do a PN dry-run.
- Close the TU when satisfied.

## Working with Loop Playbooks

Loop playbooks are the **primary way to execute QuestFoundry workflows**. Each playbook contains
complete procedures for one of the 13 canonical loops.

**Location:** `loops/*.playbook.md`

### Running a Loop (Multi-Role Orchestration)

1. **Showrunner loads playbook**: `loops/lore_deepening.playbook.md`
2. **Playbook specifies procedure**: 9 steps with message sequences
3. **Roles respond to intents**: Lore Weaver drafts canon, Gatekeeper pre-gates, etc.
4. **Showrunner coordinates**: Routes messages per RACI matrix in playbook

**Example workflow:**

```
loops/lore_deepening.playbook.md        # Load procedure
  → Step 1: tu.open (SR → LW)           # Showrunner opens TU
  → Step 2: Frame questions (LW)        # Lore Weaver drafts
  → Step 3: Draft answers (LW)          # Lore Weaver creates canon
  → Step 8: Pre-gate (LW → GK)          # Gatekeeper validates
  → Step 9: Handoff (LW → CC)           # Codex Curator receives summaries
```

### Choosing Format: Full Prompt vs Adapter

**For standalone work:** Upload full role prompt

- Example: "I need Lore Weaver help canonizing backstory"
- Upload: `lore_weaver/system_prompt.md`

**For orchestrated workflow:** Use adapters + loop playbook

- Example: "Run Lore Deepening loop for character hooks"
- Load: `loops/lore_deepening.playbook.md` + `role_adapters/lore_weaver.adapter.md`

## Supported Chatbots And File Uploads

- ChatGPT
  - Limit: up to 10 files per upload action. You can upload more overall by repeating uploads, or by
    using a zip.
  - Recommendation: use the Minimal Upload Kit (10 files). Upload Player‑Narrator later as an addon,
    or use the provided zip.
  - Keep filenames descriptive (the UI shows them for quick reference).
- Claude
  - Handles multiple attachments well; individual files preferred for transparency and grounding.
  - Zips are accepted; still prefer individual files unless you hit limits.
- Gemini
  - Zip limit: up to 10 files per zip. Use two zips (core + optional) when loading the full set.
  - Recommendation: upload the core zip first (shared + SR + PW + SS + ST + GK + BB), then the
    optional zip when needed.

Tip: If your platform drops attachments between threads, reattach the Minimal Upload Kit at the
start of each new session.

## Upload Kits (Minimal vs. Full)

**Note on Dual Formats:**

- **Full prompts** (`[role]/system_prompt.md`) — Use for standalone work or learning
- **Role adapters** (`role_adapters/[role].adapter.md`) — Use for multi-role orchestration with loop
  playbooks (more efficient)

The kits below use full prompts for simplicity. For orchestrated workflows with loop playbooks,
consider using role adapters instead.

Minimal Upload Kit (10 files — ChatGPT‑friendly, Full Prompts)

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

Orchestrated Loop Kit (Alternative — Loop Playbooks + Adapters)

For running specific loops with multi-role coordination:

- Upload target loop playbook: `loops/[loop_name].playbook.md`
- Upload role adapters: `role_adapters/[role].adapter.md` (only needed roles)
- Example: Lore Deepening loop → upload `loops/lore_deepening.playbook.md` + adapters for
  Showrunner, Lore Weaver, Gatekeeper, Codex Curator

Addon (upload later when binding/PN is needed)

- 05-prompts/player_narrator/system_prompt.md

Layer 3 Schema Reference (No Upload Required)

**All Cold SoT schemas are available at canonical URLs**:
`https://questfoundry.liesdonk.nl/schemas/`

Book Binder and Gatekeeper prompts reference these schemas for validation:

- cold_manifest.schema.json — Top-level file index with SHA-256 hashes
- cold_book.schema.json — Story structure, section order, metadata
- cold_art_manifest.schema.json — Asset mappings with provenance tracking
- hot_manifest.schema.json — Hot discovery space index
- project_metadata.schema.json — Project configuration

**No upload needed**: Agents reference schemas by canonical URL. The schemas define the Cold SoT
format that prevents protocol violations (e.g., Adventure Bay Binder Breakdown).

Full Upload Kit (split for Gemini)

- Core zip (≤10 files): Minimal kit files above
- Optional zip (≤10 files):
  - 05-prompts/player_narrator/system_prompt.md
  - 05-prompts/lore_weaver/system_prompt.md
  - 05-prompts/codex_curator/system_prompt.md
  - 05-prompts/researcher/system_prompt.md
  - 05-prompts/art_director/system_prompt.md
  - 05-prompts/illustrator/system_prompt.md
  - 05-prompts/audio_director/system_prompt.md
  - 05-prompts/audio_producer/system_prompt.md
  - 05-prompts/translator/system_prompt.md

See also: 05-prompts/upload_kits/ for manifests and build scripts that generate link folders and
zips.

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

5. Run a pre‑gate check (we’ll do PN after expansion in Stage 2):

```
Gatekeeper: run a pre‑gate on the manuscript. Evaluate Presentation, Integrity, and Style with
player‑safe evidence. Produce a brief gatecheck report and any smallest viable fixes.
```

6. Address gate feedback, then ask Book Binder to bind a player‑safe view:

```
Book Binder: produce a Markdown view for the current Cold snapshot. Include an anchor map summary.
Return a view.export.result envelope with export_artifacts.
```

7. Close the TU when satisfied (or keep it open and continue into Stage 2 for full production):

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
  - Evaluate bars (Presentation, Integrity, Style, Determinism, etc.) with player‑safe evidence.
  - **Runs Cold SoT validation** before allowing Binder (8 preflight checks: manifest validation,
    file existence, SHA-256 verification, asset approval metadata). Schemas at
    <https://questfoundry.liesdonk.nl/schemas/>
  - Useful prompt: "Pre‑gate manuscript; list smallest fixes per bar; don't leak spoilers."
- Book Binder (BB)
  - Bind views (Markdown/HTML) from Cold manifest, summarize anchors, return export artifacts.
  - **All inputs MUST come from `cold/manifest.json`** (no directory scanning/heuristics). Validates
    against schemas at <https://questfoundry.liesdonk.nl/schemas/>
  - Useful prompt: "Bind to Markdown for PN; include anchor_map summary; return paths."
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

- PN Safety: Never route Hot content to PN. If PN is receiver, enforce Cold + `player_safe=true` +
  `snapshot`.
- Context Pressure: Summarize older turns as state notes; keep raw quotes only when needed.
- Traceability: Maintain `correlation_id` and use `refs` to link artifacts.
- Escalation: Use `human.question` when blocked; propose options and a default.

## Production Run — Stage 1 (Minimal Kit Only)

Goal: produce a small, player‑safe manuscript using only the Minimal Upload Kit roles (SR, PW, SS,
ST, GK, BB).

1. Open TU and plan

```
Showrunner: open TU for a 3–5 scene manuscript (loop "Story Spark"). Propose plan and wake PW/SS/ST.
```

2. Outline

```
Plotwright: propose a compact outline with any gateways and their consequences. Keep hubs modest.
```

3. Scene drafting

```
Scene Smith: write Scene 1 per the outline, in the agreed register. Aim for 3+ paragraphs unless this is a micro‑beat transit; if shorter, auto‑extend with a movement/vector paragraph. Emit tu.checkpoint with a 1–2 line summary.
```

4. Style audit

```
Style Lead: audit Scene 1 for register drift; propose minimal rewrites. Keep rationale short.
```

5. Iterate

- Repeat steps 3–4 for Scene 2…N.
- Encourage checkpoints after each scene to keep context tight.

6. Pre‑gate and remediation

```
Gatekeeper: run pre‑gate (Presentation, Integrity, Style). Provide smallest viable fixes and owners.
```

7. Bind a view

```
Book Binder: produce a Markdown view for the current Cold snapshot with anchor_map summary; return export_artifacts.
```

8. Close or proceed

- If satisfied and bars are green, close TU now.
- Or proceed to Stage 2 to enrich with canon/codex, art, audio, PN, and localization.

## Production Run — Stage 2 (Full Kit Expansion)

Attach the Optional zip (or upload the additional role prompts) and continue in the same TU
(preferred) or a follow‑on TU.

1. Canon continuity (Lore Weaver)

```
Lore Weaver: review the manuscript and provide player‑safe summaries and continuity checks (timeline, invariants, refs).
If any changes are needed, propose smallest viable edits without leaking spoilers.
```

2. Codex entries (Codex Curator)

```
Codex Curator: generate/update codex entries for new terms introduced by the manuscript. Ensure entries are player‑safe and
validated against codex_entry.schema.json. Provide crosslinks and coverage notes.
```

3. Art pass (Art Director → Illustrator)

```
Art Director: produce a shotlist for key scenes (subjects, composition, mood).
Illustrator: draft image prompts per the shotlist; align with style guardrails. Do not leak spoilers.
```

4. Audio pass (Audio Director → Audio Producer)

```
Audio Director: propose a cuelist (music/SFX) with motifs and transitions.
Audio Producer: render one or two cues; log parameters. Keep outputs player‑safe.
```

5. Localization (Translator)

```
Translator: produce a language_pack for one locale (e.g., en‑GB → nl‑NL). Keep register consistent; list terms of art.
```

6. PN dry‑run (now that PN prompt is uploaded)

```
Player‑Narrator: perform a dry‑run on the bound Markdown (Cold + player_safe=true + snapshot). Enforce gateways diegetically;
report issues via pn.playtest.submit with smallest fixes and evidence.
```

7. Final gatecheck and binding

```
Gatekeeper: run a full gatecheck (all relevant bars). If green, approve.
Book Binder: produce final exports (Markdown + HTML; add locale exports if available); update anchor_map and coverage.
```

8. Close TU and summarize

```
Showrunner: close TU; summarize outcomes, link artifacts (view exports, cues, images), and list any deferred items.
```

## Calling Explicit Loops (Copy/Paste Prompts)

Use these when you want to explicitly start or switch loops mid‑thread. Send to Showrunner unless
otherwise noted.

- Story Spark (outline → first scenes)

```
Showrunner: open a TU for Story Spark (3–5 scenes). Wake Plotwright, Scene Smith, Style Lead. Propose plan and checkpoints.
```

- Hook Harvest (turn sparks into discrete hooks)

```
Showrunner: start Hook Harvest. Ask Plotwright to extract 3–5 actionable hooks from current notes and file them.
```

- Lore Deepening (lore pass; LW)

```
Showrunner: start Lore Deepening. Wake Lore Weaver. LW: provide player‑safe summaries + continuity checks for the active slice.
```

- Codex Expansion (codex pass; CC)

```
Showrunner: start Codex Expansion. Wake Codex Curator. CC: draft/update codex entries for new terms; validate against schema; provide crosslinks.
```

- Style Tune‑up (register/voice tightening; ST)

```
Showrunner: start Style Tune‑up. Wake Style Lead. ST: audit the current scenes for register drift and propose minimal rewrites.
```

- Binding Run (export views; BB)

```
Showrunner: start Binding Run. Wake Book Binder. BB: bind a Markdown view for the current Cold snapshot; return export_artifacts + anchor_map.
```

- Narration Dry‑Run (player narrates; PN — Cold only)

```
Showrunner: start Narration Dry‑Run. Wake PN. PN: perform a brief dry‑run on the bound Markdown (Cold + player_safe=true + snapshot). Report issues via pn.playtest.submit.
```

- Gatecheck (pre‑gate or full)

```
Showrunner: run pre‑gate. GK: evaluate Presentation, Integrity, Style; provide smallest fixes. If green, proceed to full gatecheck for all relevant bars.
```

- Translation Pass (localization; TR)

```
Showrunner: start Translation Pass. Wake Translator. TR: produce a language_pack for <locale>; keep register; list terms of art.
```

- Art Touch‑up (AD/IL)

```
Showrunner: start Art Touch‑up. Wake Art Director + Illustrator. AD: shotlist key scenes. IL: prompts for each shot (player‑safe).
```

- Audio Pass (AuD/AuP)

```
Showrunner: start Audio Pass. Wake Audio Director + Producer. AuD: cuelist with motifs. AuP: render 1–2 cues and log parameters.
```

- Post‑Mortem (optional health check)

```
Showrunner: run a quick Post‑Mortem. Summarize what worked, what didn’t, and next loop candidates. Emit tu.checkpoint.
```

## Appendix — Uploading Files, Zipping, And Link Folders

Upload individually (preferred): Drag the Minimal kit (10 files) into your chat. Upload PN later as
an addon.

Zips (when hitting attachment limits):

- ChatGPT: Use the Minimal kit zip (all 10 files) or the Full core/optional zips.
- Gemini: Upload the core zip first (≤10 files), then the optional zip (≤10 files).

Auto‑build link folders and zips:

- Preferred: `uv run qfspec-build-kits` (writes to `dist/upload_kits/*`). You’ll get top‑level
  `minimal/` (10 files) + `minimal.zip`, `optional/` + `optional.zip`, and `full/` + `full.zip`.
- Alternatively, scripts:
  - Bash: `spec-tools/scripts/build_upload_kits.sh`
  - PowerShell: `spec-tools/scripts/build_upload_kits.ps1`

See 05-prompts/upload_kits/ for manifests and details.
