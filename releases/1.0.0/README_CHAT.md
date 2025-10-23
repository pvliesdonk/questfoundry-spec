# Using CYOA v1.x.y with a Chatbot

This guide explains how to run the CYOA v1.x.y workflow entirely by chat, with copy/paste and files.

## Folder map
- prompts/ — agent role prompts to paste into chat.
- prompts/snippets/ — feedback event templates.
- schemas/ — JSON Schemas for all artifacts.
- examples/contracts/ — valid annotated examples for each schema.

## Agent flow (recommended)
1. Orchestrator: validate or create project_config.json.
2. Plot Drafter: create plot_outline.json and plot_map.json.
3. World Architect: curate canon.json.
4. Scene Smith: write sections/S-###/current.json.
5. Vision Director → Renderer: plan art (`art_plan.json`, artlist) and produce art_manifest.
6. Compiler: produce build/book.md and build/manifest.json.

Feedback events can be sent at any time to request changes.

## Chat discipline
- Paste the correct role prompt first (from prompts/).
- Ask the model to output a single JSON object only (no commentary).
- Use stable ids: B-###, S-###, IMG-###, LOC-…, SHIP-….
- Validate outputs against schemas and examples before proceeding.
- Append all feedback events to events/feedback.jsonl (one JSON per line).
- Feedback protocol version is 1.0.0.

## Kickoff (Orchestrator)
1) Paste prompts/00_orchestrator_conductor.txt.
2) Paste and adapt examples/contracts/project_config.annotated.json.
3) Save as project_config.json.

## Outline (Plot Drafter)
1) Paste prompts/15_plot_drafter.txt.
2) Provide project_config.json and optionally canon.json.
3) Request plot_outline.json then plot_map.json. Save both.

Quality checks: plot_outline threads and beats match schema; plot_map nodes and edges have valid kinds.

## World canon (World Architect)
Paste prompts/10_world_architect.txt. Provide current canon.json. Ask for append-only additions based on proposals.

## Draft sections (Scene Smith)
Paste prompts/20_scene_smith.txt. Provide plot_outline.json, canon.json, and a beat id. Request a section object matching schemas/section.schema.json. Save to sections/S-###/current.json.

## Art planning and rendering
Vision Director: produce art_plan.json (and optionally artlist rows) from sections.
Renderer: take art_plan.json + artlist rows and produce art_manifest entries that reference art/images/*.

## Feedback loop (core of iteration)
- Use prompts/snippets/feedback_envelope_template.json + feedback_type_templates.json to build events.
- Required fields include: id, version (1.0.0), timestamp, session_id, actor, target, type, refs, payload.
- Keep the log at events/feedback.jsonl.

Example: section rewrite request (fields abbreviated):
{
  "id": "EVT-0001", "version": "1.0.0", "session_id": "run-demo",
  "actor": "plot_drafter", "target": "scene_smith", "type": "section_rewrite_request",
  "refs": {"section": {"section_id": "S-089", "path": "sections/S-089/current.json"}},
  "payload": {"instructions": "tighten approach"}
}

Response example: section rewrite response
{
  "id": "EVT-0002", "version": "1.0.0", "correlation_id": "EVT-0001",
  "actor": "scene_smith", "target": "plot_drafter", "type": "section_rewrite_response",
  "status": "applied", "payload": {"result_path": "sections/S-089/current.json"}
}

## Validation
Manual: compare to examples/contracts/*.annotated.json.
Automated: use any JSON Schema validator (AJV, jsonschema, fastjsonschema) against the schemas/ files.

## Compile (Compiler)
Paste prompts/60_compiler.txt. Provide outline, canon, sections, and optional art. Request build/book.md and build/manifest.json.

## Research integration
Issue research_request events and collect answers in research_packet.json. Maintain claim_registry.json for compiler checks.

## Stabilization
Generate stabilization_report.json and ensure checks are green (open_requests, plot_invariants, world_integrity, section_coverage, continuity, compiler, pacing, research_pass).

## Troubleshooting
- If the model adds commentary, instruct it to return a single JSON object only.
- If ids drift, keep a small ids.md and normalize.
- If invented fields appear, point to the schema and ask to remove fields not defined.
- Always include session_id and use correlation_id for responses.

## Minimal end-to-end script
1) Orchestrator: create project_config.json.
2) Plot Drafter: create plot_outline.json and plot_map.json.
3) Scene Smith: create one section.
4) Emit a rewrite request and response via the feedback log.
5) Compiler: build book and manifest.

This is the quickest way to exercise CYOA v1.x.y with any competent chatbot.
