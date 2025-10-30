## Summary

> One or two sentences. What does this PR do in Layer 0/1 terms?

- TU-ID(s): `tu-<topic>-<date>` (link if public)
- Loop alignment: `story_spark | hook_harvest | lore_deepening | codex_expansion | style_tune_up | art_touch_up | audio_pass | translation_pass | binding_run | narration_dry_run | docs/policy`
- Scope: `Layer-0 | Layer-1` (avoid editing Layers 3–7 here)

---

## Motivation / Rationale

Why is this change valuable to creators/players? Cite friction found in loops, PN dry-runs, or Gatekeeper checks. Keep spoilers out of the PR body; link to Hot notes if needed.

---

## Changes

- [ ] Docs added/updated:
  - [ ] `00-north-star/...`
  - [ ] `01-roles/...`
  - [ ] Index pages updated (LOOPS/README, PLAYBOOKS/README, Layer-0 README)
- [ ] No schemas/protocol/prompts/libraries/UI added (Layers 3–7 untouched)

---

## Player-surface impact

- [ ] None (policy/structure only)
- [ ] Manuscript wording
- [ ] PN phrasing patterns
- [ ] Codex entries
- [ ] Captions/alt text
- [ ] Audio text-equivalents
- [ ] Translations

> If any box is checked, ensure Presentation & Accessibility bars below are met.

---

## Quality Bars — Self-check

**Integrity**

- [ ] All links/anchors resolve across docs (and exports, if applicable)

**Reachability / Nonlinearity / Gateways** _(only if touching topology or PN phrasing)_

- [ ] No accidental dead-ends; hubs/loops meaningful
- [ ] Gate phrasing is **diegetic** (no codeword names or logic on surfaces)

**Style**

- [ ] Voice/register/motifs align with Style Guide & addenda

**Determinism** _(assets only; plan-only may skip)_

- [ ] Reproducibility/seed/DAW notes are in logs, **not** on surfaces

**Presentation (Spoiler & Accessibility Hygiene)**

- [ ] No spoilers or internal labels on player surfaces
- [ ] Alt text / text equivalents present & spoiler-safe
- [ ] Descriptive link text; print-friendly assumptions hold

Reference: `00-north-star/QUALITY_BARS.md`, `SPOILER_HYGIENE.md`, `ACCESSIBILITY_AND_CONTENT_NOTES.md`.

---

## Traceability

- [ ] TU(s) updated with inputs/outputs and bar pressure
- [ ] If this PR implements an ADR, reference: `DECISIONS/ADR-YYYYMMDD-<slug>.md`

---

## Screenshots / Before–After (optional, no spoilers)

<drop images of structure diffs or snippet comparisons if helpful>

---

## Follow-ups

- [ ] Create/Update TU(s): <ids> for downstream loops
- [ ] Wake dormant roles in next sprint: `Researcher | Art | Audio | Translator` (if needed)
- [ ] Binder/PN to schedule next **Binding Run / Dry-Run** (if surfaces changed)

---

## Checklist for Maintainers

- [ ] Scope fits Layer 0/1
- [ ] Indices updated
- [ ] Gatekeeper bars green
- [ ] Merge to **Cold** (if applicable) and consider snapshot tagging
