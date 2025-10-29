# Art Plan — Slot Specification (Layer 1, Human-Level)

> **Use:** Specify an illustration slot so an Illustrator can execute without guessing. Keep **player surfaces** clean: captions/alt are **in-world**; all technique/repro stays **off-surface**.

---

## Normative references

- Bars & hygiene: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md` · `../../00-north-star/ACCESSIBILITY_AND_CONTENT_NOTES.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md`
- Interfaces & lanes: `../interfaces/pair_guides.md` (Art Director ↔ Illustrator) · `../interfaces/escalation_rules.md`
- Role briefs: `../briefs/art_director.md` · `../briefs/illustrator.md`

---

## Header

```

Art Plan — <slot id / short name>
TU: <id> · Edited: <YYYY-MM-DD> · Owner: Art Director
Slice: <scope, e.g., “Act I — Foreman Gate (3 sections)”>
Status: planned | rendering | deferred

```

---

## 1) Purpose (pick one; add rationale)

```

Purpose: <clarify | recall | mood | signpost>
Rationale: <1–2 lines on why this image helps the reader here>

```

> *Clarify* = make a described object/space legible.  
> *Recall* = help memory of a prior scene/concept.  
> *Mood* = set atmosphere that prose can’t carry alone.  
> *Signpost* = reduce hesitation at hubs/gates.

---

## 2) Subject & Focal Affordance

```

Subject (what the image shows): <concrete nouns>
Focal affordance (what must be readable): <e.g., lapel badge vs scanner>

```

---

## 3) Composition Intent (no technique terms)

```

Framing: <tight/medium/wide> · Angle: <eye/low/high/oblique> · Distance: <close/room/establishing>
Hierarchy: <what leads the eye first/second>
Spatial cues: <lines/occlusion/overlap used to guide reading>
Legibility at size: <target sizes; what must survive thumbnail/print>

```

---

## 4) Iconography & Motifs

```

Motifs to include: <materials/lights/icons reused across acts>
Motifs to avoid: <list>

```

---

## 5) Light / Palette / Texture (descriptive, not technical)

```

Light: <e.g., sodium lamp glow; soft shadow under gantry>
Palette: <e.g., muted steel, oily greens, amber highlights>
Texture: <e.g., wet metal, worn fabric>

```

---

## 6) Environment & Props (player-safe)

```

Location tells: <environment details that anchor place/time without spoilers>
Props: <only those needed for clarity/signpost>

```

---

## 7) Characters & Poses (player-safe)

```

Who is visible: <roles/titles, not secret identities>
Pose & silhouette: <gesture that reads at a glance>
Face visibility: <yes/no; if no, say why (mood/ambiguity)>

```

---

## 8) Inclusion Criteria (where this slot appears)

```

Include when: <conditions: section themes/anchors/gates>
Exclude when: <avoid duplication or spoiler contexts>

```

---

## 9) Caption (player-safe, one line) & Alt Guidance (one sentence)

```

Caption (atmospheric/clarifying; no technique):
"<one-line caption>"

Alt (subject + relation + location; spoiler-safe):
"<one-sentence concrete description>"

```

---

## 10) Variants / Crops (if allowed)

```

Variants: <none | list variant intents (e.g., tighter crop for mobile)>
Selection rule: <when to choose which variant>

```

---

## 11) Placement & Anchors (for Binder)

```

Anchor targets: </manuscript/...#slug, /codex/...>
Placement note: <before/after choice block | at section start | figure callout>
Anchor stability risks: <diacritics/renames to coordinate with Translator/Binder>

```

---

## 12) Accessibility & Localization Notes

```

Accessibility: <any risks (busy textures, ambiguous silhouettes) + mitigation>
Localization: <caption idioms to avoid; register; terms checked with Curator>

```

---

## 13) Determinism (off-surface; do not expose to players)

```

Repro expectation: <none | log-only>
Producer log fields (off-surface): <seed/model OR capture session, chain summary, target size/aspect, hash>

```

---

## 14) Handoffs

```

To Illustrator: this plan + target sizes + deadline
To Style: caption review (register); banned phrases check
To Translator: caption/alt portability; slug impacts
To Gatekeeper: Presentation/Accessibility spot-check (pre-gate)
To Binder: anchor list for dry bind

```

---

## 15) Done checklist (tick before handing to Illustrator)

- [ ] Purpose chosen (**clarify/recall/mood/signpost**) with rationale  
- [ ] Subject & **focal affordance** unambiguous at target sizes  
- [ ] Composition intent stated with **no technique terms**  
- [ ] Caption (one line) **player-safe**; Alt (one sentence) concrete  
- [ ] Inclusion criteria clear; anchors listed; Binder informed  
- [ ] Accessibility/localization notes added; Style/Translator consulted if needed  
- [ ] Determinism handled **off-surface** (if promised)  
- [ ] Gatekeeper pre-gate check passed on Presentation/Accessibility

---

## Mini example (safe)

```

Art Plan — foreman-gate-signpost
TU: TU-2025-10-28-AD02 · Edited: 2025-10-28 · Owner: Art Director
Slice: Act I — Dock 7 checkpoint
Status: planned

1. Purpose: signpost
   Rationale: Readers hesitate at the gate; show what matters (badge vs scanner).

2. Subject & Focal
   Subject: lapel area and dock badge scanner
   Focal affordance: badge region vs scanner “eye”

3. Composition Intent
   Framing: tight · Angle: slight low · Distance: close
   Hierarchy: badge area → scanner light → foreman silhouette
   Legibility at size: badge region must read at thumbnail

4. Iconography & Motifs
   Include: wet steel, sodium lamp smear
   Avoid: syndicate symbols (spoiler risk)

5. Light / Palette / Texture
   Light: sodium lamp glow; scanner LED
   Palette: muted steel, amber highlights
   Texture: wet metal; worn jacket fabric

6. Environment & Props
   Location tells: dock railing; industrial signage shapes (no readable text)

7. Characters & Poses
   Visible: foreman silhouette shoulder/hand
   Pose: hand near scanner; face not shown (keeps neutrality)

8. Inclusion Criteria
   Include when: sections invoking inspection/access control at Dock 7
   Exclude when: post-inspection interiors

9. Caption & Alt
   Caption: "Sodium lamps smear along wet steel; the scanner’s eye waits."
   Alt: "A foreman’s shadow falls across a badge scanner at a dock checkpoint."

10. Variants / Crops
    Variants: tighter crop for mobile if badge area shrinks below legibility
    Selection rule: choose tight variant when width < 480 px

11. Placement & Anchors
    Anchors: /manuscript/act1/foreman-gate#inspection
    Placement: directly above choice list the first time the gate appears
    Risks: none; slug confirmed kebab-case ASCII

12. Accessibility & Localization
    Accessibility: high contrast at focal; avoid glare; clear silhouette
    Localization: caption portable; no idioms; Curator terms align (“badge scanner”)

13. Determinism (off-surface)
    Repro expectation: log-only
    Producer fields: session id, model/seed OR capture settings, export hash

14. Handoffs
    Illustrator by: 2025-10-30; Style/Translator review of caption tomorrow; Binder dry bind after render

15. Checklist
    [✔] purpose  [✔] focal  [✔] caption/alt  [✔] anchors  [✔] accessibility  [✔] off-surface repro

```
