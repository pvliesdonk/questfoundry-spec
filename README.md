# CYOA Framework — v1.0.0

This is a cleaned, self-contained snapshot of the v1.x.y workflow system. It’s aimed at new users who want a quick grasp, and power users who want stable contracts.

## What it is
A modular, agent-based pipeline for building choose-your-own-adventure fiction. Agents exchange **structured artifacts** (JSON) and **lightweight feedback events** to converge on a coherent story with art.

## High-level flow
1. Configure a project (`project_config.json`).
2. Draft plot structure (`plot_outline.json` + `plot_map.json`).
3. Curate world canon (`canon.json` + `relations.json`).
4. Expand beats into prose sections (`sections/*/current.json`).
5. Iterate via the **feedback loop** (see `schemas/feedback.schema.json`).
6. Plan and render art (`art_plan.json` → images; `art_manifest.json`).
7. Compile the book/manifest; build a wiki (`manifest.json`, `wiki_index.json`).
8. Stabilize and ship (`stabilization_report.json`, session ledger).

## Key artifacts & where to look
- Schemas: `schemas/*.schema.json` (JSON Schema Draft 2020-12).
- Examples: `examples/contracts/*.annotated.json` (one per schema).
- End-to-end runs: `examples/workflow/` (placeholder while refreshed runs are generated).
- Feedback & research docs: `README_FEEDBACK.md`, `README_RESEARCH.md`.
- **New:** Chat-ops how-to: `README_CHAT.md` (step-by-step guide for using these prompts and files with a chatbot).

## Feedback loop (bite-sized)
Agents send events to request targeted changes: beat revisions, section rewrites, world extensions, plot diffs, and research. Each event is a single JSON object carrying refs to plot/section/canon and a type-specific payload. The Orchestrator enforces loop **state** (drafting → revision → stabilizing → stable) and **iteration budgets** (TTL cycles).

## Versioning
- Protocol stays at **1.0.0** for event compatibility.
- This **v1.0.0** release cleans names, examples, and docs; no breaking changes.

## Start here
- Skim `examples/contracts/` to see each contract in context.
- Check `examples/workflow/` after regeneration for pacing across genres (placeholder today).
- Read `README_CHAT.md` to run the system via chat.
- Copy the schemas you need and validate your artifacts against them.

---
Happy writing, and may your rejoin edges be gentle.
