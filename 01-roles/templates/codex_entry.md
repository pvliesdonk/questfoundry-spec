# Codex Entry — Player-Safe Knowledge (Layer 1, Human-Level)

> **Use:** Write **player-safe** background pieces that clarify terms, places, procedures, or objects without revealing canon or internal mechanics. Keep entries concise, linkable, and portable across locales. This is a **human template**; no schemas here.

---

## Normative references

- Bars & hygiene: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md`
- Interfaces & lanes: `../interfaces/pair_guides.md` (Lore ↔ Curator; Translator ↔ Binder) · `../interfaces/escalation_rules.md`
- Role briefs: `../briefs/codex_curator.md` · neighbors in `../briefs/*.md`

---

## Header

```

Codex Entry — <Entry Title>
Slug: <kebab-case-anchor>          Locale: <EN|NL|…>
Owner: Codex Curator               Edited: <YYYY-MM-DD>
Snapshot: Cold @ <YYYY-MM-DD>      TU: <id>
Lineage: Canon Pack(s) <ids> · Research Memos <ids> (posture noted)
Register: <neutral | formal | colloquial> (per Style)

```

---

## 1) Overview (2–5 lines, player-safe)

> What a reader needs to **recognize** and **use** the concept in choices—no causes, no twists.

```

<Concise, spoiler-safe description. Avoid internal logic, codewords, or technique.>

```

---

## 2) Usage (how it appears in the book)

- **Where to link:** <section themes/anchors; e.g., “first mention in inspection scenes”>  
- **When not to link:** <avoid overlinking; spoiler contexts>  
- **PN cue (1 line, optional):** “<in-voice nudge the PN may use>”

---

## 3) Context (2–6 lines)

> Surface-level background: practical norms, common misunderstandings, visible traits. Keep diegetic.

```

<Short paragraph(s) that expand clarity without hinting at hidden causes.>

```

---

## 4) Variants & Synonyms (player-safe)

| Variant | Register/Region | Notes for Translator |
|---|---|---|
| <term> | <neutral/formal/colloquial> | <polysemy risks; idiom policy> |
| <term> | <…> | <…> |

---

## 5) Relations (See also)

- **Related entries:** `<slug-a>` ↔ `<slug-b>` ↔ `<slug-c>`  
- **Up/Down taxonomy:** `<parent>` → `<this>` → `<children>`  
- **Cross-media:** images/captions **if present** (link by slug; no technique)

---

## 6) Accessibility & Presentation

- **Reading level:** <plain / needs glossary link>  
- **Alt guidance (if illustrated):** *subject + relation + location*, one sentence.  
- **Caption guideline:** one line, atmospheric/clarifying; **no technique**.  
- **Link text:** avoid “click here”; prefer descriptive anchors.

---

## 7) Labels & Anchors (for Binder)

```

Anchor slug: /codex/<kebab-case-anchor>
Collision risks: <diacritics/punctuation to avoid>
Binder note: ensure TOC/grouping under <category> (ASCII slugs if policy)

```

---

## 8) Notes (what to avoid)

- **Don’t** reveal hidden allegiances, causes, or puzzle solutions.  
- **Don’t** use internal terms (flags, codewords, seed/model, DAW/plugins).  
- **Don’t** set policy—use an ADR if this entry would change global taxonomy.

---

## 9) Lineage & Trace

```

From Canon: <summary of player-safe fact intake>
Research posture touched: <corroborated | plausible | disputed | uncorroborated:<low|med|high>>
Hooks filed: hook://translator/<term> (if tricky), hook://curator/<child-term> (if new children needed)

```

---

## 10) Done checklist

- [ ] Overview is **player-safe**, concise, in register  
- [ ] Usage notes explain **where to link** and when not to  
- [ ] Context adds clarity **without causes/twists**  
- [ ] Variants table filled for translation portability  
- [ ] Relations list crosslinks; slugs stable; no orphans  
- [ ] Accessibility notes present (alt/caption guidance if illustrated)  
- [ ] Binder anchor confirmed; collision risks noted  
- [ ] Trace written (TU, Canon/Research lineage, hooks if any)

---

## Mini example (safe)

```

Codex Entry — Union Token
Slug: union-token                      Locale: EN
Owner: Codex Curator                   Edited: 2025-10-28
Snapshot: Cold @ 2025-10-28            TU: TU-2025-10-28-CC03
Lineage: Canon Pack CP-FT-01 · Research Memo RS-FT-02 (posture: plausible)
Register: neutral

1. Overview
   A small badge or card recognized at dock checkpoints to confirm union membership. Inspectors may glance or scan it during routine checks.

2. Usage
   Link on first mention in inspection scenes and at gates where access depends on labor status.
   When not to link: interior scenes after inspection is resolved.
   PN cue: “The foreman’s eyes flick to your lapel.”

3. Context
   Tokens vary by dock but share a clear emblem and member ID. Visual verification is common; readers should assume inspectors know the emblem by sight in well-lit areas.

4. Variants & Synonyms
   | Variant        | Register/Region | Notes for Translator |
   | union badge    | neutral         | Preferred US/EN; avoid brand-like capitalization |
   | labor token    | neutral         | Works in generic sci-fi; check local idiom       |
   | membership tag | colloquial      | Use sparingly; may read informal                 |

5. Relations (See also)
   Related: inspection-logs ↔ dock-checkpoints
   Taxonomy: credentials → union-token → (none)

6. Accessibility & Presentation
   Reading level: plain
   Alt guidance (if illustrated): "A badge scanner glows as a lapel emblem is held near it at a dock checkpoint."
   Caption guideline: “Sodium lamps smear along wet steel; the scanner’s eye waits.”
   Link text: “union token requirements” (not “click here”).

7. Labels & Anchors (for Binder)
   Anchor slug: /codex/union-token
   Collision risks: none; ASCII kebab-case
   Binder note: group under /codex/credentials

8. Notes
   Avoid implying forgery methods or backstory causes.

9. Lineage & Trace
   From Canon: player-safe summary of inspection strictness (no causes stated).
   Research posture touched: plausible (visual verification norms)
   Hooks filed: hook://translator/union-token (regional variants); hook://curator/inspection-logs (new entry)

```
