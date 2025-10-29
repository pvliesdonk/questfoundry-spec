# Edit Notes — Small, Surgical Changes (Layer 1, Human-Level)

> **Use:** Propose **line-level** fixes without changing structure or canon. Keep examples **player-safe**; no spoilers, no internals. Owners apply the edits in their lanes.

---

## Normative references

- Bars & hygiene: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md` · `../../00-north-star/ACCESSIBILITY_AND_CONTENT_NOTES.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md`
- Handshakes & lanes: `../interfaces/pair_guides.md` · `../interfaces/escalation_rules.md`
- Role briefs (who applies fixes): `../briefs/*.md`

---

## Header

```

Edit Notes — <slice name>
TU: <id> · Opened: <YYYY-MM-DD> · Snapshot: Cold @ <YYYY-MM-DD>
Author: <role, e.g., Style Lead> · Owners to apply: <roles, e.g., Scene Smith / Curator / Translator>
Bars pressed: <Style | Presentation | Accessibility | …>

```

---

## 1) Summary (2–4 bullets)

- <why these edits exist; smallest viable fix per bar>  
- <what not to change (structure/canon/anchors)>  
- <who applies which group of edits>  
- <any dormancy tags left intact, e.g., deferred:art>

---

## 2) Before → After (player-safe exemplars)

> Provide **surgical** replacements. Do not reveal canon or internal logic. One or two lines per item.

| Location (path#anchor) | Issue tag | Before | After | Owner | Rationale |
|---|---|---|---|---|---|
| `/manuscript/act1/foreman-gate#entry` | `choice-ambiguity` | “Go / Proceed.” | “Slip through maintenance / Face the foreman.” | Scene | Make options contrastive. |
| `/manuscript/act1/foreman-gate#scanner` | `meta-gate` | “Option locked: missing CODEWORD.” | “The scanner blinks red. ‘Union badge?’” | Scene | Diegetic refusal; PN-safe. |
| `/codex/union-token` | `register` | “Badge credential is mandated.” | “Dock inspections often require a union token.” | Curator | Plain, portable phrasing. |

> **Issue tags (suggested):** `choice-ambiguity`, `meta-gate`, `tone-wobble`, `caption-technique`, `alt-vague`, `label-collision`, `accessibility`.

---

## 3) PN patterns (optional)

> If helpful, add **pattern** lines PN can reuse (not mandatory rewrites).

- **Gate refusal pattern:** “<World cue>. ‘<Short in-world question/statement>’”  
- **Micro-recap (≤2 lines):** “<State delta>. <Current stakes>.”

---

## 4) Banned / Preferred (delta to Style Addendum)

- **Ban:** “Option locked”, “You must select…”  
- **Prefer:** “The guard waves you back.”, “The console stays dark.”

> If this list becomes reusable across slices, copy to `Style Addendum`.

---

## 5) Translator & Curator notes (player-safe)

- **Translator:** anchors/labels changed? **No**. Idioms: avoid “greenlighted”; use “approved”.  
- **Curator:** add codex entry *Union Token* if missing; neutral description only.

---

## 6) Accessibility sweep (what changed)

- Choice lists isolated; short sentences near junctions.  
- Captions 1 line; **no technique**.  
- Alt text rewritten to **subject + relation + location** (one sentence).

---

## 7) Hooks (file separately if needed)

- `hook://codex/union-token` — glossary anchor + crosslinks  
- `hook://pn/patterns/gates` — add refusal exemplar to PN kit

---

## 8) Done checklist (tick before handoff)

- [ ] Examples are **player-safe** (no spoilers/internals)  
- [ ] Edits do **not** change structure, canon, or anchors  
- [ ] Owners identified per line; effort fits a **single sitting**  
- [ ] Bars targeted named; smallest viable fix shown  
- [ ] Translator/Curator impacts noted; Accessibility improved or unchanged  
- [ ] TU & Trace updated; Gatekeeper pre-gate pinged if needed

---

## 9) Handoffs

```

To apply:

* @scene — locations 1–2
* @curator — location 3 + codex anchor hook
* @translator — sanity check captions/labels (no anchor renames)

Pre-gate sample for @gatekeeper:

* /manuscript/act1/foreman-gate#entry
* /codex/union-token

```

---
