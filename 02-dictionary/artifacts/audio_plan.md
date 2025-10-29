# Audio Plan — Cue Specification (Layer 1, Human-Level)

> **Use:** Specify a cue so an Audio Producer can realize it **without guessing**. Keep player surfaces clean: captions/text equivalents are **in-world**; all technique/repro stays **off-surface**.

---

## Normative references

- Bars & hygiene: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md` · `../../00-north-star/ACCESSIBILITY_AND_CONTENT_NOTES.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md`
- Interfaces & lanes: `../briefs/audio_director.md` · `../briefs/audio_producer.md` · `../interfaces/pair_guides.md` (Audio Director ↔ Audio Producer)
- Dormancy: `../interfaces/dormancy_signals.md` (plan-only allowed: `deferred:audio`)

---

## Header

```

Audio Plan — <cue id / short name>
TU: <id> · Edited: <YYYY-MM-DD> · Owner: Audio Director
Slice: <scope, e.g., “Act I — Dock 7 checkpoint”>
Status: planned | producing | deferred

```

---

## 1) Purpose (pick one; add rationale)

```

Purpose: <clarify | recall | mood | signpost | pace>
Rationale: <1–2 lines on how this cue helps reading/performance>

```

> *Clarify* = make an implied action/surroundings legible.  
> *Recall* = help memory of a prior scene/concept.  
> *Mood* = set atmosphere that prose alone can’t carry.  
> *Signpost* = reduce hesitation at hubs/gates.  
> *Pace* = manage tension/energy around choices.

---

## 2) Placement & Envelope

```

Placement: <before line | under lines X–Y | after line | between paragraph and choice list>
Timing note: <enter/exit moments in words, not SMPTE>
Duration target: <e.g., 2–4 s>
Duck policy (if under speech): <soft | moderate | strong>

```

---

## 3) Description (no technique terms)

```

What is heard (plain language): <e.g., low engine hum swells, then settles>
Salient qualities (descriptive): <steady | distant | short | mechanical | airy>
Readability: <intended to be audible on laptop/phone speakers>

```

---

## 4) Caption / Text Equivalent (player-safe, one line)

```

Caption: "[<one line, in-world, portable>]"

```

> Do not include plugin/DAW/settings/“seed”/mix jargon. Keep it diegetic.

---

## 5) Safety Notes

```

Onset: <soft | gradual> (avoid startle)
Intensity: <conservative | moderate> (player comfort)
Transients: <none | gentle> (avoid piercing highs)
Content notes: <if applicable; reference Layer-0 content notes>

```

---

## 6) Inclusion Criteria (where this cue appears)

```

Include when: <conditions: section themes/anchors/gates>
Exclude when: <avoid masking prose or duplicating other cues>

```

---

## 7) Localization & Style

```

Register: <neutral / formal / colloquial> (for caption phrasing)
Idioms to avoid: <list if any>
Translator note: <portable wording hints; onomatopoeia policy>

```

---

## 8) Determinism (off-surface; not for players)

```

Repro expectation: <none | log-only>
Producer log fields (off-surface): <session/project id, chain summary, target LUFS, export hash>

```

---

## 9) Handoffs

```

To Producer: this plan + file specs (format/rate) + loudness target
To Style: caption review (register)
To Translator: caption portability check; variants if needed
To PN: confirm placement won’t fight delivery
To Gatekeeper: Presentation/Accessibility spot-check (caption parity)
To Binder: naming/placement conventions if assets ship in View

```

---

## 10) Done checklist (tick before handing to Producer)

- [ ] Purpose chosen (**clarify/recall/mood/signpost/pace**) with rationale  
- [ ] Placement clear; **duration** & **duck policy** stated  
- [ ] Description uses **no technique terms**  
- [ ] **Caption** is one line, in-world, portable  
- [ ] **Safety notes** set (onset/intensity/transients/content)  
- [ ] Inclusion/exclusion criteria written  
- [ ] Localization & Style reviewed as needed  
- [ ] Determinism handled **off-surface** (if promised)  
- [ ] Gatekeeper pre-gate on Presentation/Accessibility **green**

---

## Mini example (safe)

```

Audio Plan — foreman-gate-hum
TU: TU-2025-10-28-AUD03 · Edited: 2025-10-28 · Owner: Audio Director
Slice: Act I — Dock 7 checkpoint
Status: planned

1. Purpose: pace
   Rationale: Lift tension across the inspection lines, then clear before choices.

2. Placement & Envelope
   Placement: under the last two narrative lines; end before the choice list
   Timing note: enter on “scanner blinks,” fade by the next sentence’s period
   Duration target: 3–4 s
   Duck policy: soft (voice remains primary)

3. Description (no technique)
   What is heard: a low engine hum gently swells, then eases back to the ambient floor
   Salient qualities: steady, distant, short, mechanical
   Readability: must read on laptop/phone speakers

4. Caption / Text Equivalent
   Caption: "[A low engine hum rises, then settles.]"

5. Safety Notes
   Onset: gradual
   Intensity: conservative
   Transients: none
   Content notes: none

6. Inclusion Criteria
   Include when: section mentions dock machinery/inspection at the gate
   Exclude when: interior dialogue after inspection; high-density speech

7. Localization & Style
   Register: neutral
   Idioms to avoid: none
   Translator note: keep concrete and short; avoid culture-specific onomatopoeia

8. Determinism (off-surface)
   Repro expectation: log-only
   Producer fields: session id, chain summary, LUFS target, export hash

9. Handoffs
   Producer: render 1 cue at −16 LUFS integrated; gentle 300 ms fade-in/out
   Style: confirm caption register
   Translator: verify portability (NL/EN)
   PN: confirm no masking of delivery
   Gatekeeper: Presentation/Accessibility spot-check before marking “producing”
   Binder: no asset in View for this pass (plan-only allowed)

10. Checklist
    [✔] purpose  [✔] placement  [✔] caption  [✔] safety  [✔] localization  [✔] off-surface repro

```
