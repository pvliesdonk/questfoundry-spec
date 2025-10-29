# Artifact Structures (Layer 2)

> **Status:** 🚧 **PARKED — Pending Layer 2 proper draft**
>
> These 17 artifact templates were moved from `01-roles/templates/` during architectural cleanup (2025-10-29). They define the structure of work products created during loops, but as **data structure definitions** they belong in Layer 2 (what artifacts ARE) rather than Layer 1 (who creates them).
>
> Content is unchanged pending full Layer 2 review and refinement.

---

## What This Is

Each file here defines the **structure and purpose** of a work artifact used in QuestFoundry studio operations:
- What fields/sections it contains
- What each field means (human-readable)
- When and why you'd create one
- Filled examples (player-safe)

These are **human-readable templates** that:
- Bridge Layer 0 concepts with Layer 1 role responsibilities
- Inform Layer 3 JSON schemas (when drafted)
- Serve as working references during loops

---

## Artifact Index

### Core Workflow
- **hook_card.md** — Small follow-up ideas/uncertainties captured during work
- **tu_brief.md** — Timeboxed task unit (scope, roles, bars, deliverables)

### Creation & Content
- **canon_pack.md** — Spoiler-level lore and causality (Lore Weaver)
- **codex_entry.md** — Player-safe terminology and summaries (Codex Curator)
- **style_addendum.md** — Voice/register patterns and exemplars (Style Lead)
- **edit_notes.md** — Prose revision guidance (Style Lead → Scene Smith)

### Research & Planning
- **research_memo.md** — Factual verification and uncertainty notes (Researcher)
- **shotlist.md** — Illustration planning and intent (Art Director)
- **cuelist.md** — Audio cue planning and intent (Audio Director)
- **art_plan.md** — Detailed illustration slot specifications (Art Director)
- **audio_plan.md** — Detailed audio cue specifications (Audio Director)

### Localization
- **language_pack.md** — Translation glossary, register map, coverage % (Translator)
- **register_map.md** — Voice/tone equivalence across languages (Style Lead + Translator)

### Quality & Export
- **gatecheck_report.md** — Quality Bar validation results (Gatekeeper)
- **view_log.md** — Export metadata and coverage notes (Book Binder)
- **front_matter.md** — Player-facing export intro/credits/notes (Showrunner + Binder)
- **pn_playtest_notes.md** — UX feedback and friction tags (Player-Narrator)

---

## How to Use These (During Transition)

### For Role Work (Layer 1)
Each role charter/brief in `01-roles/` references which artifacts that role produces. Look here for the structure, but remember:
- WHO creates it = Layer 1 charter/brief
- WHAT it contains = here (Layer 2)

### For Future Schemas (Layer 3)
When drafting Layer 3, each artifact here should inform a corresponding JSON schema:
- `hook_card.md` → `hook-card.schema.json`
- `tu_brief.md` → `tu-brief.schema.json`
- etc.

### For Protocol Design (Layer 4)
Layer 4 will define how these artifacts flow between roles:
- Submission endpoints
- Validation rules
- State transitions
- Merge protocols

---

## Migration Notes

**From:** `01-roles/templates/`
**To:** `02-dictionary/artifacts/`
**Reason:** These define data structures (WHAT), not role responsibilities (WHO)

**Cross-reference updates needed:**
- Layer 0 files referencing templates
- Layer 1 charters/briefs referencing templates
- See ADR-20251029-01 for full rationale

---

## Future Layer 2 Work

When properly drafting Layer 2:
1. Review each artifact for completeness and consistency
2. Ensure terminology aligns with `../glossary.md`
3. Add clear field descriptions and constraints
4. Provide more filled examples (player-safe)
5. Note which fields are Hot-only vs Cold-safe
6. Create artifact lifecycle diagrams
7. Define relationships between artifacts

---

## Normative References (Layer 0)

All artifacts must respect:
- `../../00-north-star/QUALITY_BARS.md` — Quality standards
- `../../00-north-star/SPOILER_HYGIENE.md` — Player-safety rules
- `../../00-north-star/SOURCES_OF_TRUTH.md` — Hot/Cold policy
- `../../00-north-star/PN_PRINCIPLES.md` — Presentation boundaries
- `../../00-north-star/ACCESSIBILITY_AND_CONTENT_NOTES.md` — Accessibility baseline
