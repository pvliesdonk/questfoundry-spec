# Shotlist — Art Plan Index for a Slice (Layer 1, Human-Level)

> **Use:** Art Director’s compact index of **all illustration slots** in a slice. Each row points to a full **Art Plan**. Keep **player surfaces** clean here too (captions/alt are safe); all technique/repro details stay **off-surface** inside the Art Plan or producer logs.

---

## Normative references

- Bars & hygiene: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md` · `../../00-north-star/ACCESSIBILITY_AND_CONTENT_NOTES.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md`
- Interfaces & lanes: `../interfaces/pair_guides.md` (Art Director ↔ Illustrator; Style ↔ Translator) · `../interfaces/escalation_rules.md` · `../interfaces/dormancy_signals.md`
- Role briefs: `../briefs/art_director.md` · `../briefs/illustrator.md`
- Template: `./art_plan.md`

---

## Header

```

Shotlist — <slice name>
Edited: <YYYY-MM-DD> · Owner: Art Director
Scope: <e.g., “Act I — Dock 7 checkpoint (3 sections)”>
Dormancy: <active | plan-only (deferred:art) | dormant>
Snapshot: Cold @ <YYYY-MM-DD> · TU: <id>
Neighbors: @illustrator @style @translator @binder @gatekeeper

```

---

## 1) Summary (player-safe)

- **Purpose mix:** <count> clarify · <count> recall · <count> mood · <count> signpost  
- **Inclusion policy:** <1–2 lines; where these images appear>  
- **Accessibility:** all slots have **caption (1 line)** and **alt (1 sentence)**

---

## 2) Table (one row per slot)

> Keep it short. Link **Slot ID** to the full `Art Plan`. Captions/alt are **player-safe** excerpts.

| Slot ID → Plan | Purpose | Subject (short) | Focal affordance | Caption (1 line, safe) | Alt (1 sentence, safe) | Anchor target | Status |
|---|---|---|---|---|---|---|---|
| `foreman-gate-signpost` | signpost | badge vs scanner | badge region | “Sodium lamps smear along wet steel; the scanner’s eye waits.” | “A foreman’s shadow falls across a badge scanner at a dock checkpoint.” | `/manuscript/act1/foreman-gate#inspection` | planned |
| `<slot-2>` | mood | <…> | <…> | “<…>” | “<…>” | `/manuscript/...#...` | planned/producing/done |

*Statuses:* `planned` · `producing` · `done` · `deferred`.

---

## 3) Inclusion/Exclusion rules (per slot, optional)

> Only when a slot has non-obvious placement rules.

```

foreman-gate-signpost — include on first gate appearance; exclude on interior scenes.

```

---

## 4) Localization & Style notes (slice-level)

- Captions use **slice register** (see Style Addendum).  
- Translator confirms **portability**; avoid idioms; anchors stay kebab-case ASCII (if policy).  
- Curator aligns terms with codex entries (no spoiler wording).

---

## 5) Accessibility checklist (slice-level)

- [ ] Each slot has **caption (1 line)** and **alt (1 sentence)**  
- [ ] Focal affordance legible at **target sizes** (thumbnail → print)  
- [ ] No caption hints at **twists**; no **technique** on surfaces  
- [ ] Contrast/silhouette readable; no flashing/strobe content

---

## 6) Binder & Gatekeeper notes

- Binder: verify **anchors** and figure placements in **dry bind**; list any normalized slugs in View Log.  
- Gatekeeper: **Presentation/Accessibility** spot-check one representative slot before unlocking production.

---

## 7) Hooks (if any)

```

hook://style/caption-register — confirm slice register for captions
hook://translator/anchor-policy — confirm diacritics/ASCII policy for slugs
hook://curator/term-variants — align badge/scanner terms

```

---

## 8) Done checklist (before handing to Illustrator)

- [ ] Shotlist table complete; each slot links to an **Art Plan**  
- [ ] Purpose mix sensible; **signpost** shots placed near hesitation points  
- [ ] Captions/alt present and **player-safe**  
- [ ] Inclusion/exclusion rules clear where needed  
- [ ] Translator/Style notes added; Binder/Gatekeeper informed  
- [ ] Dormancy state recorded (`deferred:art` if plan-only)  
- [ ] Trace updated (TU, snapshot)

---

## Mini example (safe)

```

Shotlist — Act I Dock 7
Edited: 2025-10-29 · Owner: AD-01
Scope: Act I — checkpoint scenes (3 sections)
Dormancy: plan-only (deferred:art)
Snapshot: Cold @ 2025-10-28 · TU: TU-2025-10-29-AD01
Neighbors: @illustrator @style @translator @binder @gatekeeper

Summary

* Purpose mix: 1 signpost, 1 mood
* Inclusion: first appearance of gate; mood plate only on exterior wide
* Accessibility: captions/alt present

Table
| Slot ID → Plan             | Purpose | Subject         | Focal | Caption                                               | Alt                                                              | Anchor                                   | Status   |
| foreman-gate-signpost → ./art_plan-foreman-gate-signpost.md | signpost | badge vs scanner | badge | "Sodium lamps smear along wet steel; the scanner’s eye waits." | "A foreman’s shadow falls across a badge scanner at a dock checkpoint." | /manuscript/act1/foreman-gate#inspection | planned  |
| dock-exterior-plate → ./art_plan-dock-exterior-plate.md     | mood     | wet steel quay   | signage | "Rain needles the quay; cargo lights pace the water."         | "A rainy cargo dock with distant lights reflecting on wet steel."       | /manuscript/act1/dock-overview#arrival   | planned  |

Notes

* Localization: captions avoid idioms; anchors ASCII kebab-case
* Binder: run dry bind after signpost selection; update View Log if slugs normalize
* Gatekeeper: pre-gate Presentation/Accessibility on signpost

Hooks

* hook://style/caption-register
* hook://translator/anchor-policy

```
