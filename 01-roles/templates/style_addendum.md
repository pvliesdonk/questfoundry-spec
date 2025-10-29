# Style Addendum — Patterns & Examples (Layer 1, Human-Level)

> **Use:** Capture **repeatable patterns** and **tiny examples** the owners can apply without rewrites. This addendum supplements the house style with *slice-specific* guidance (register, banned/preferred forms, PN phrasing, captions/alt). Keep it **player-safe**: no spoilers, no internals.

---

## Normative references

- Bars & hygiene: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md` · `../../00-north-star/ACCESSIBILITY_AND_CONTENT_NOTES.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md`
- Handshakes & lanes: `../interfaces/pair_guides.md` (Style ↔ PN / Translator / Scene) · `../interfaces/escalation_rules.md`
- Role briefs: `../briefs/style_lead.md` · neighbors in `../briefs/*.md`

---

## Header

```

Style Addendum — <slice or theme>
Edited: <YYYY-MM-DD> · Owner: Style Lead
Scope: <e.g., “Act I — Foreman Gate (3 sections)”>
Snapshot: Cold @ <YYYY-MM-DD> · TU: <id>
Neighbors: @scene @pn @translator @gatekeeper

```

---

## 1) Register & Voice (slice-specific)

- **Register:** <neutral | formal | colloquial> (and who uses it)  
- **Cadence:** <short lines near choices | longer in travel beats | …>  
- **Pronouns & address:** <2nd person direct; titles for officials; …>  
- **Tense/aspect:** <present-simple; avoid progressive; …>

> *If this conflicts with global policy, escalate for ADR.*

---

## 2) Banned / Preferred (delta)

> Keep this concise; include only what changed for this slice.

- **Ban:** “Option locked”, “Proceed”, “You must…”, “Click…”  
- **Prefer:** Diegetic refusals; intent-forward choice labels (verb + object)

---

## 3) PN Patterns (player-facing phrasing)

- **Gate refusal (pattern):**  
  “\<world cue\>. ‘\<short in-world check/refusal\>’”  
  *Ex:* “The scanner blinks red. ‘Union badge?’”

- **Choice labels (pattern):**  
  “\<verb\> \<object/place\>” vs “\<verb\> \<person\>” (contrast of *approach*)  
  *Ex:* “Slip through maintenance / Face the foreman.”

- **Micro-recap (≤2 lines):**  
  “\<state change\>. \<current stakes\>.”

---

## 4) Scene-Level Patterns (owners apply)

- **Context line before choices (if needed):** one line that clarifies *why* the options differ.  
- **Show, don’t lecture:** swap exposition for a physical cue when a term is in the **Codex**.  
- **Diegetic time pressure:** concrete sensory tick (“dock klaxon”, “clock sweep”) rather than meta countdowns.

---

## 5) Captions & Alt (art/audio surfaces)

- **Caption rule:** one line, atmospheric/clarifying; **no technique**; same register as prose.  
- **Alt rule:** one sentence — **subject + relation + location**; spoiler-safe.  
- **Examples (portable):**  
  - Caption: “Sodium lamps smear along wet steel; the scanner’s eye waits.”  
  - Alt: “A foreman’s shadow falls across a badge scanner at a dock checkpoint.”

---

## 6) Translator Notes (portability)

- Avoid culture-bound idioms near choices.  
- Keep anchors kebab-case ASCII if policy-bound; coordinate renames with Binder.  
- Provide variants for occupational titles if target locale distinguishes formality sharply.

---

## 7) Tiny Before → After (player-safe)

| Location | Issue | Before | After | Owner |
|---|---|---|---|---|
| `/manuscript/act1/foreman-gate#entry` | `choice-ambiguity` | “Go / Proceed.” | “Slip through maintenance / Face the foreman.” | Scene |
| `/manuscript/act1/foreman-gate#scanner` | `meta-gate` | “Option locked: missing CODEWORD.” | “The scanner blinks red. ‘Union badge?’” | Scene |

---

## 8) Accessibility nudges

- Short sentences within 2 lines of a choice list.  
- Avoid stacked prepositional phrases; prefer concrete subjects.  
- Ensure caption meaning matches audio/image perception (no metaphor-only captions).

---

## 9) Hooks & Hand-offs

- Hooks: `hook://curator/union-token` (glossary anchor); `hook://translator/gate-phrasing` (register variants).  
- Hand-offs: Scene applies line edits; PN adopts patterns; Translator localizes examples; Gatekeeper pre-gates Presentation.

---

## 10) Change Log

```

YYYY-MM-DD — v1.0 — Initial slice patterns (gate refusal, choice labels, captions/alt)
YYYY-MM-DD — v1.1 — Added micro-recap exemplar; banned “Proceed”

```

---

## 11) Done checklist

- [ ] Register/cadence stated without changing global policy  
- [ ] PN patterns include at least **gate + choice + micro-recap**  
- [ ] Caption/Alt rules + 1–2 exemplars provided  
- [ ] Tiny Before→After table added (owner-marked)  
- [ ] Translator/Binder impacts noted (anchors/idioms)  
- [ ] Hooks filed; Gatekeeper pre-gate pinged  
- [ ] Trace updated (TU, snapshot)

---

## Mini example (filled, safe)

```

Style Addendum — Act I Foreman Gate
Edited: 2025-10-28 · Owner: Style Lead
Scope: Act I — 3 sections around the checkpoint
Snapshot: Cold @ 2025-10-27 · TU: TU-2025-10-28-ST02
Neighbors: @scene @pn @translator @gatekeeper

1. Register & Voice
   Register: neutral; officials slightly formal
   Cadence: short lines within 2 sentences of choices
   Pronouns: second person; titles for officials
   Tense: present simple

2. Banned / Preferred
   Ban: “Option locked”, “Proceed”
   Prefer: diegetic refusals; intent-forward labels

3. PN Patterns
   Gate refusal: “The scanner blinks red. ‘Union badge?’”
   Choice labels: “Slip through maintenance / Face the foreman.”
   Micro-recap: “You kept the badge pocketed. The inspection line tightens.”

4. Captions & Alt
   Caption: “Sodium lamps smear along wet steel; the scanner’s eye waits.”
   Alt: “A foreman’s shadow falls across a badge scanner at a dock checkpoint.”

5. Translator Notes
   ASCII slugs; avoid idioms like “greenlighted”. Provide formal variant for foreman title if locale requires.

6. Before → After

* see table in §7

8. Accessibility
   Short sentences near choices; avoid nested clauses.

Hooks & Hand-offs
Hooks: curator/union-token; translator/gate-phrasing
Owners: @scene applies; @pn adopts; @translator localizes; @gatekeeper pre-gate

Change Log
2025-10-28 — v1.0

```
