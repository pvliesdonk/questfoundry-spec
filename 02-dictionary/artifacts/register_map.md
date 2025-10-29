# Register Map — Localization Register & Patterns (Layer 1, Human-Level)

> **Use:** Translator’s one-pager that pins **pronouns, formality, tense/aspect, punctuation, numerals, idioms, PN patterns,** and any typography/directionality notes for a **target locale**. It travels with the slice or book. Keep it **player-safe**.

---

## Normative references

- Bars & hygiene: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md` · `../../00-north-star/ACCESSIBILITY_AND_CONTENT_NOTES.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md`
- Interfaces & lanes: `../interfaces/pair_guides.md` (Style ↔ Translator; Binder ↔ Translator) · `../interfaces/escalation_rules.md`
- Role briefs: `../briefs/translator.md` · `../briefs/style_lead.md` · `../briefs/book_binder.md`

---

## Header

```

Register Map — <locale code>  (e.g., NL, EN-GB, DE)
Edited: <YYYY-MM-DD> · Owner: Translator
Scope: <book | slice> · Snapshot: Cold @ <YYYY-MM-DD> · TU: <id>
Neighbors: @style @binder @pn @gatekeeper

```

---

## 1) Voice & Address

- **Second person:** <tu/vous/du/usted/je/jij/u> — default for narrative  
- **Formality switch rules:** <when officials/elders/authority appear>  
- **Titles & honorifics:** <localized forms; gender/number behavior>  
- **Directness level:** <plain/indirect; prefer short clauses near choices>

---

## 2) Tense / Aspect / Mood

- **Narrative tense:** <present simple / preterite / …>  
- **Progressive/perfect usage:** <allowed/avoid; examples>  
- **Imperatives in choices:** <allowed/discouraged; sample>  
- **Modal verbs:** <should/must/can equivalents; tone guidance>

---

## 3) PN Patterns (localized)

- **Gate refusal:**  
  Pattern: “\<world cue\>. ‘\<short in-world check/refusal\>’”  
  Example: “\<localized example\>”

- **Choice labels:**  
  Pattern: “\<verb\> \<object/place\>” vs “\<verb\> \<person\>” (contrast)  
  Examples: “\<A\> / \<B\>”

- **Micro-recap (≤2 lines):**  
  Pattern: “\<state change\>. \<current stakes\>.”  
  Example: “\<localized example\>”

> Keep examples **player-safe** and portable.

---

## 4) Punctuation & Numerals

- **Quotation style:** <„…“ | « … » | “ … ” | ‘ … ’>  
- **Decimal/Thousands:** <comma/dot rules>  
- **Dash/Ellipsis:** <en/em rules; spacing>  
- **Time/Date:** <24-hour? day-month order?>  
- **List & choice markers:** <hyphen/bullet; casing conventions>

---

## 5) Orthography & Typography

- **Casing for headings/anchors:** <Sentence case / Title Case>  
- **Diacritics in anchors:** <allowed | normalize to ASCII> (coordinate with Binder)  
- **Hyphenation policy:** <soft hyphens? never in anchors>  
- **RTL/LTR:** <directionality; mirrored punctuation rules if RTL>

---

## 6) Idiom & Lexicon Policy

- **Domesticating vs foreignizing:** <preference and limits>  
- **Banned idioms:** <list that doesn’t travel or jars tone>  
- **Preferred turns:** <portable equivalents>  
- **Loanwords:** <ok/avoid; transliteration if any>

---

## 7) Accessibility & Readability

- **Sentence length near choices:** <target range>  
- **Numbers & units read-aloud:** <spell out under N; SI units behavior>  
- **Proper names:** <pronunciation hints if needed; PN guidance>  
- **Alt/Caption register:** <neutral/formal; no technique terms>

---

## 8) Labels, Anchors, & TOC

- **Slug policy:** <kebab-case ASCII | locale diacritics>  
- **Stop-word removal:** <rules>  
- **Collision handling:** <normalize/rename procedure with Binder>  
- **UI label casing:** <e.g., sentence case>

---

## 9) Examples (Before → After, player-safe)

| Context | Source (safe) | Target (localized) | Note |
|---|---|---|---|
| Gate refusal | “The scanner blinks red. ‘Union badge?’” | “\<localized\>” | Diegetic; one beat |
| Choice labels | “Slip through maintenance / Face the foreman.” | “\<localized\> / \<localized\>” | Contrast of approach |
| Caption | “[A short alarm chirps twice, distant.]” | “[\<localized\>]” | No technique |

---

## 10) Risks & Mitigations

- **Anchors with diacritics** → policy: <normalize/allow>; Binder check  
- **Polysemy on core terms** → Curator glossary entries with usage notes  
- **Register clashes (youth vs officials)** → Style patterns per scene

---

## 11) Hooks

- `hook://translator/<term>` — needs variant policy  
- `hook://curator/<term>` — glossary/entry impact  
- `hook://binder/anchors-<locale>` — slug normalization decision (if needed)

---

## 12) Done checklist

- [ ] PN patterns localized (gate, choice, micro-recap)  
- [ ] Pronouns/formality rules explicit; examples included  
- [ ] Tense/aspect/mood pinned; imperatives policy set  
- [ ] Punctuation/numerals/anchors policies defined (Binder aligned)  
- [ ] Accessibility guidance added (read-aloud, alt/caption register)  
- [ ] Examples are **player-safe**; no spoilers/internals  
- [ ] Hooks filed; trace updated (TU, snapshot)

---

## Mini example (NL, safe)

```

Register Map — NL
Edited: 2025-10-29 · Owner: Translator
Scope: Act I slice · Snapshot: Cold @ 2025-10-28 · TU: TU-2025-10-29-TR01
Neighbors: @style @binder @pn @gatekeeper

1. Voice & Address
   Second person: jij/je (default); u for officials (foreman).
   Titles: “voorman”, “inspecteur”. Direct, short clauses near choices.

2. Tense / Aspect / Mood
   Narrative: onvoltooid tegenwoordige tijd (tegenwoordige tijd).
   Progressief: vermijden; gebruik korte zinnen.
   Imperatief in keuzes toegestaan: “Neem de onderhoudsgang / Spreek de voorman aan.”

3. PN Patterns
   Gate refusal: “De scanner knippert rood. ‘Union-badge?’”
   Choice labels: “Door de onderhoudsgang / De voorman te woord staan.”
   Micro-recap: “Je houdt de badge in je zak. De rij schuift onrustig op.”

4. Punctuation & Numerals
   Quotes: “…”; Decimal: komma; Duizend: punt; Tijd: 24-uurs.

5. Orthography & Typography
   Anchors: kebab-case ASCII (Binder policy). Geen diacritics in slugs.

6. Idiom & Lexicon
   Banned: “groenlicht krijgen”. Prefer: “goedgekeurd”.
   Loanwords: vermijden tenzij gangbaar.

7. Accessibility
   ≤ 16 woorden per zin nabij keuzelijsten. Alt/caption neutraal, concreet.

8. Labels & Anchors
   Slug policy: kebab-case ASCII. Collisions: Binder normaliseert; Translator bevestigt.

9. Examples
   Gate refusal — EN “The scanner blinks red. ‘Union badge?’” → NL “De scanner knippert rood. ‘Union-badge?’”
   Caption — “[A short alarm chirps twice, distant.]” → “[Een korte alarmtoon klinkt tweemaal, in de verte.]”

Risks & Mitigations
Diacritics in loanwords → verwijderen in anchors; toelichting in glossary.

Hooks
hook://curator/union-token (synoniemen)
hook://binder/anchors-nl (confirm ASCII policy)

```
