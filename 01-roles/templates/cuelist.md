# Cuelist — Audio Plan Index for a Slice (Layer 1, Human-Level)

> **Use:** Audio Director’s compact index of **all cues** in a slice. Each row points to a full **Audio Plan**. Keep **player surfaces** clean (captions/text equivalents are safe). All technique/repro lives **off-surface** inside the Audio Plan or producer logs.

---

## Normative references

- Bars & hygiene: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md` · `../../00-north-star/ACCESSIBILITY_AND_CONTENT_NOTES.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md`
- Interfaces & lanes: `../interfaces/pair_guides.md` (Audio Director ↔ Audio Producer; Style ↔ Translator) · `../interfaces/escalation_rules.md` · `../interfaces/dormancy_signals.md`
- Role briefs: `../briefs/audio_director.md` · `../briefs/audio_producer.md`
- Template: `./audio_plan.md`

---

## Header

```

Cuelist — <slice name>
Edited: <YYYY-MM-DD> · Owner: Audio Director
Scope: <e.g., “Act I — Dock 7 checkpoint (3 sections)”>
Dormancy: <active | plan-only (deferred:audio) | dormant>
Snapshot: Cold @ <YYYY-MM-DD> · TU: <id>
Neighbors: @audioproducer @style @translator @pn @gatekeeper @binder

```

---

## 1) Summary (player-safe)

- **Purpose mix:** <count> clarify · <count> recall · <count> mood · <count> signpost · <count> pace  
- **Placement policy:** <1–2 lines; where cues enter/exit relative to prose/choices>  
- **Accessibility:** each cue has a **one-line caption**; onsets are **gradual** (no startle)

---

## 2) Table (one row per cue)

> Keep it short. Link **Cue ID** to the full `Audio Plan`. Captions are **player-safe**.

| Cue ID → Plan | Purpose | Placement (short) | Description (plain) | Caption (1 line, safe) | Anchor target | Status |
|---|---|---|---|---|---|---|
| `foreman-gate-hum` | pace | under last 2 lines; end before choices | low engine hum rises, then settles | “[A low engine hum rises, then settles.]” | `/manuscript/act1/foreman-gate#scanner` | planned |
| `<cue-2>` | mood | <…> | <…> | “[<…>]” | `/manuscript/...#...` | planned/producing/done |

*Statuses:* `planned` · `producing` · `done` · `deferred`.

---

## 3) Inclusion/Exclusion rules (per cue, optional)

> Only when a cue has non-obvious placement or risks masking speech.

```

foreman-gate-hum — include on exterior inspection lines; exclude during dialogue-heavy interiors.

```

---

## 4) Safety & Localization notes (slice-level)

- **Safety:** gradual onset; conservative intensity; no piercing transients; content notes referenced when applicable.  
- **Localization:** captions use slice register; avoid culture-bound onomatopoeia; Translator confirms portability.  
- **PN coordination:** PN confirms cues don’t fight cadence or mask lines.

---

## 5) Accessibility checklist (slice-level)

- [ ] Each cue has **caption (1 line)**; matches what is heard  
- [ ] No startle; onsets/offsets gentle; duration short near choices  
- [ ] Captions contain **no technique** (no DAW/seed/FX jargon)  
- [ ] Readable on laptop/phone speakers (intent communicated in plan)

---

## 6) Binder & Gatekeeper notes

- Binder: list whether cues **ship in the View** or are plan-only; reflect in `View Log` options/coverage.  
- Gatekeeper: **Presentation/Accessibility** spot-check one representative cue before production unlock.

---

## 7) Hooks (if any)

```

hook://style/caption-register — confirm caption register for this slice
hook://translator/caption-onomatopoeia — portability decision
hook://pn/cadence — verify cue timing vs breath units

```

---

## 8) Done checklist (before handing to Producer)

- [ ] Cuelist table complete; each cue links to an **Audio Plan**  
- [ ] Purpose mix sensible; **pace/signpost** cues near hesitation points  
- [ ] Captions present and **player-safe**; PN cadence considered  
- [ ] Inclusion/exclusion rules clear where needed  
- [ ] Translator/Style notes added; Binder/Gatekeeper informed  
- [ ] Dormancy state recorded (`deferred:audio` if plan-only)  
- [ ] Trace updated (TU, snapshot)

---

## Mini example (safe)

```

Cuelist — Act I Dock 7
Edited: 2025-10-29 · Owner: AuD-01
Scope: Act I — checkpoint scenes (3 sections)
Dormancy: plan-only (deferred:audio)
Snapshot: Cold @ 2025-10-28 · TU: TU-2025-10-29-AUD01
Neighbors: @audioproducer @style @translator @pn @gatekeeper @binder

Summary

* Purpose mix: 1 pace, 1 mood
* Placement: cues never under choice lists; fade before options
* Accessibility: captions present; onsets gradual

Table
| Cue ID → Plan               | Purpose | Placement                       | Description                     | Caption                                   | Anchor                                   | Status   |
| foreman-gate-hum → ./audio_plan-foreman-gate-hum.md | pace    | under last 2 lines; end pre-choices | low hum rises, then settles     | "[A low engine hum rises, then settles.]" | /manuscript/act1/foreman-gate#scanner    | planned  |
| dock-rain-plate → ./audio_plan-dock-rain-plate.md   | mood    | before exterior wide paragraph      | soft rain with distant beacons  | "[Rain needles the quay; distant beacons.]" | /manuscript/act1/dock-overview#arrival | planned  |

Notes

* Localization: captions neutral; Translator confirms portability (EN↔NL)
* Binder: plan-only for this View; reflect in `View Log` options
* Gatekeeper: pre-gate Presentation/Accessibility on first cue

Hooks

* hook://style/caption-register
* hook://translator/caption-onomatopoeia
* hook://pn/cadence

```
