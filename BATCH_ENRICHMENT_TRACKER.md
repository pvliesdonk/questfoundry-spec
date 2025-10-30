# Batch Enrichment Tracker (Tiers 2-5)

## New Inconsistencies Found

### Issue #14: Research Posture Format in canon_pack.md
**Location:** canon_pack.md line 24
**Current:** `uncorroborated:<low|med|high>`
**Should be:** `uncorroborated:low | uncorroborated:medium | uncorroborated:high`
**Why:** Taxonomy uses "medium" not "med"; separate values not nested format

---

## Enrichment Progress

### Tier 1: Core Workflow (3 artifacts) - ✅ COMPLETED (previous session)
- [x] hook_card.md - 28 fields
- [x] tu_brief.md - 27 fields
- [x] gatecheck_report.md - 28 fields

### Tier 2: Content Creation (4 artifacts) - ✅ COMPLETED
- [x] canon_pack.md - 34 fields (Hot/Cold split complex) - Issue #14 fixed
- [x] codex_entry.md - 29 fields - Player-safe only, localization heavy - Issue #14 fixed
- [x] style_addendum.md - 23 fields - Patterns, examples
- [x] research_memo.md - 20 fields - Evidence, posture - Issue #14 fixed

### Tier 3: Asset Planning (4 artifacts) - ✅ COMPLETED
- [x] art_plan.md - 36 fields (largest artifact)
- [x] audio_plan.md - 28 fields
- [x] shotlist.md - ~15 fields (index table)
- [x] cuelist.md - ~15 fields (index table)

### Tier 4: Localization & Export (4 artifacts)
- [ ] language_pack.md - Coverage, glossary
- [ ] register_map.md - Voice, punctuation
- [ ] view_log.md - Anchor map
- [ ] front_matter.md - Player-facing header

### Tier 5: Operational (2 artifacts)
- [ ] edit_notes.md - Before/after table
- [ ] pn_playtest_notes.md - Dry-run log

---

## Pattern Applied to All

Each enriched template includes:
1. HTML constraint comments (type, required, format, taxonomy §refs)
2. All Phase 2+3 corrections (13 types, 7 status, 8 bars, 13 loops, space deferrals)
3. Validation rules (field, cross-field, cross-artifact)
4. Common errors section (4-10 examples)
5. Field reference table
6. Layer 2 references

---

## Issues Found During Tier 2-5 Enrichment

### Issue #14: Research Posture Format (Expanded)
**Templates affected:** canon_pack.md, codex_entry.md, research_memo.md
**Problems:**
- Uses "med" instead of "medium" (abbreviation not allowed)
- Uses nested format `uncorroborated:<low|med|high>` instead of flat format
**Resolution:** Use flat format with full word: `uncorroborated:low | uncorroborated:medium | uncorroborated:high`
**Status:** Fixed in all 3 enriched templates; documented in LAYER1_CORRECTIONS.md

### Tiers 1-3: No additional issues found
All 11 enriched templates (Tiers 1-3) completed with no new inconsistencies discovered beyond Issue #14.

