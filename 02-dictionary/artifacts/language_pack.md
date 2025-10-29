# Language Pack — Localized Slice/Book Bundle (Layer 1, Human-Level)

> **Use:** Translator’s deliverable that ships a **portable bundle** for a locale: localized surfaces (manuscript/codex/captions), **Register Map**, **Glossary Slice**, **anchor/label diffs**, and a **Coverage Report**—all **player-safe**. No spoilers, no internals.

---

## Normative references

- Bars & hygiene: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md` · `../../00-north-star/ACCESSIBILITY_AND_CONTENT_NOTES.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md`
- Interfaces & lanes: `../interfaces/pair_guides.md` (Style ↔ Translator; Binder ↔ Translator) · `../interfaces/escalation_rules.md`
- Role briefs: `../briefs/translator.md` · `../briefs/book_binder.md` · `../briefs/style_lead.md`
- Templates: `./register_map.md`

---

## Header

```

Language Pack — <locale code>  (e.g., EN-GB, NL, DE)
Edited: <YYYY-MM-DD> · Owner: Translator
Scope: <book | slice name> · Snapshot: Cold @ <YYYY-MM-DD> · TU: <id>
Neighbors: @style @binder @pn @gatekeeper @curator

```

---

## 1) Coverage Report (player-safe)

> Declare what’s localized **now** and what’s deferred. Percentages are by characters or sections—state which.

```

Granularity: <characters | sections>
Manuscript: <XX%>    (notes: <what is included/excluded>)
Codex: <YY%>         (notes: <which entries>)
Captions/Alt: <ZZ%>  (notes: art/audio presence)
UI Labels/Front-matter: <done | partial>
Deferrals: [deferred:translation?](deferred:translation?) (if partial)

```

---

## 2) Register Map (pointer + delta)

> Point to the Register Map; include any **delta** for this pack.

```

Register Map: ./register_map-<locale>.md
Delta (this pack): <pronoun/formality tweaks, PN patterns added, punctuation policy changes>

```

---

## 3) Localized PN Patterns (player-safe)

> Short, reusable lines that PN can use.

```

Gate refusal (pattern + example): <one line each>
Choice labels (pattern + 2 examples): <…>
Micro-recap (pattern + example): <…>

```

---

## 4) Glossary Slice (bilingual, player-safe)

> Terms likely to appear in the slice; keep definitions neutral.

| Source term | Target term | Notes for usage/ambiguity |
|---|---|---|
| <union token> | <…> | avoid brand-like capitalization |
| <inspection logs> | <…> | neutral bureaucratic phrasing |
| <foreman> | <…> | register: formal |

---

## 5) Anchor & Label Policy (Binder-facing)

> Ensure anchors survive binding; list any changes.

```

Slug policy: <kebab-case ASCII | locale diacritics> (coordinate with Binder)
Anchor diffs:

* /manuscript/act1/<old> → /manuscript/act1/<new>
* /codex/<old> → /codex/<new>
  Collision risks: <list>  · Resolution: <normalize/rename policy>
  UI Labels: <heading casing, TOC terms>

```

---

## 6) Localized Surfaces (paths)

> Paths or file globs for the localized text. Do **not** include Hot.

```

Manuscript: /locales/<locale>/manuscript/**/*.md
Codex: /locales/<locale>/codex/**/*.md
Captions & Alt: /locales/<locale>/assets_text/**/*.md
Front-matter labels: /locales/<locale>/meta/front_matter.md

```

---

## 7) Examples (Before → After, player-safe)

> A few representative lines to sanity-check tone and anchors.

| Context | Source (safe) | Target (localized) | Anchor |
|---|---|---|---|
| Gate line | “The scanner blinks red. ‘Union badge?’” | “\<localized\>” | `/manuscript/…#scanner` |
| Choice pair | “Slip through maintenance / Face the foreman.” | “\<localized\> / \<localized\>” | `/manuscript/…#entry` |
| Codex label | “Union Token” | “\<localized\>” | `/codex/union-token` |

---

## 8) Accessibility & Read-aloud Notes

```

Sentence length near choices: <target range>
Numbers & units: <spell/format rules>
Alt/Caption: keep neutral; avoid culture-bound idioms
Pronunciation notes (PN): <only if necessary; 1–2 items>

```

---

## 9) Risks & Mitigations

- **Anchor collisions** due to diacritics → policy = <normalize/allow>; Binder to verify in dry bind.  
- **Polysemy** on <term> → Curator to add usage note; Style to prefer <phrase>.  
- **Register clashes** (official vs casual) → PN patterns doubled; see §3.

---

## 10) Hooks

```

hook://translator/<term> — needs variant guidance
hook://curator/<entry> — new glossary entry in target locale
hook://binder/anchors-<locale> — confirm slug normalization policy

```

---

## 11) Done checklist

- [ ] Coverage stated (percent + granularity); deferrals tagged if any  
- [ ] Register Map referenced; localized PN patterns included  
- [ ] Glossary slice provided; ambiguity notes added  
- [ ] Anchor/label policy aligned with Binder; diffs listed  
- [ ] Paths to localized surfaces provided; Hot excluded  
- [ ] Examples are **player-safe**; anchors resolve in dry bind  
- [ ] Accessibility/read-aloud notes included  
- [ ] Hooks filed; trace updated (TU, snapshot)

---

## Mini example (NL, safe)

```

Language Pack — NL
Edited: 2025-10-29 · Owner: Translator
Scope: Act I — Dock 7 checkpoint · Snapshot: Cold @ 2025-10-28 · TU: TU-2025-10-29-TR02
Neighbors: @style @binder @pn @gatekeeper @curator

1. Coverage Report
   Granularity: sections
   Manuscript: 76% (Act I scenes localized; epigraphs pending)
   Codex: 60% (core entries done; “inspection-logs” pending)
   Captions/Alt: 100% (all caption/alt lines localized)
   UI Labels/Front-matter: done
   Deferrals: deferred:translation (book-wide; this slice OK)

2. Register Map
   Register Map: ./register_map-NL.md
   Delta: added formal variant for “foreman” = “voorman”; kept jij/je default

3. Localized PN Patterns
   Gate refusal: “De scanner knippert rood. ‘Union-badge?’”
   Choice labels: “Door de onderhoudsgang / De voorman te woord staan.”
   Micro-recap: “Je houdt de badge in je zak. De rij schuift onrustig op.”

4. Glossary Slice
   | Source term     | Target term      | Notes                          |
   | union token     | union-badge      | neutral; avoid brand feel      |
   | inspection logs | inspectielogboeken | bureaucratic; not “verslagen” |

5. Anchor & Label Policy
   Slug policy: kebab-case ASCII
   Anchor diffs: none
   Collision risks: none observed in dry bind
   UI Labels: sentence case headings

6. Localized Surfaces
   Manuscript: /locales/NL/manuscript/**/*.md
   Codex: /locales/NL/codex/**/*.md
   Captions & Alt: /locales/NL/assets_text/**/*.md
   Front-matter: /locales/NL/meta/front_matter.md

7. Examples
   Gate line — EN → NL as above (anchor `/manuscript/act1/foreman-gate#scanner`)
   Choice pair — EN → NL as above (anchor `/manuscript/act1/foreman-gate#entry`)
   Codex label — “Union Token” → “Union-badge” (`/codex/union-token`)

8. Accessibility & Read-aloud
   ≤ 16 words near choices; numbers as “24:00”, comma decimals; alt neutral and concrete.

9. Risks & Mitigations
   Polysemy on “logboek/log” → prefer “inspectielogboek”; Curator note added.

Hooks
hook://curator/inspection-logs (entry in NL)
hook://binder/anchors-nl (confirm ASCII policy stands)

```
