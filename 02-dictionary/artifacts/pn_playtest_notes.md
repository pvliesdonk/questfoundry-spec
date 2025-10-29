# PN Playtest Notes — Dry-Run Log (Layer 1, Human-Level)

> **Use:** Log **player-facing friction** while reading a bound **View** aloud (no improvisation). Tag issues, cite the smallest fix, and route to the right owner. Keep all examples **player-safe**; never reveal canon or internals.

---

## Normative references

- Bars & hygiene: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md` · `../../00-north-star/ACCESSIBILITY_AND_CONTENT_NOTES.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md`
- Handshakes & lanes: `../interfaces/pair_guides.md` (Style ↔ PN) · `../interfaces/escalation_rules.md`
- Role brief: `../briefs/player_narrator.md` · Gatekeeping: `../checklists/quality_bars_by_role.md`

---

## Header

```

PN Playtest Notes — <view-name or slice>
Run: <YYYY-MM-DD HH:MM> · PN: <name/agent> · TU: <id>
Snapshot: Cold @ <YYYY-MM-DD> · Targets: <PDF | HTML | EPUB | …>
Mode: dry-run (no improv) · Pace: <normal | slow | fast>

```

---

## Tags (choose at least one per note)

- `choice-ambiguity` — options feel samey; intent unclear  
- `gate-friction` — refusal reads meta or unfair; diegetic wording needed  
- `nav-bug` — link/anchor sends me wrong place or loses context  
- `tone-wobble` — register shifts awkwardly; breaks voice  
- `translation-glitch` — localized phrasing/label collides or jars  
- `accessibility` — hard to read aloud; alt/caption missing/misaligned  
- `pace` — breath units wrong near choices; needs micro-recap or trim  
- `caption-mismatch` — caption/alt doesn’t match what an asset shows/sounds  
- `label-collision` — heading/anchor/slug collides or is unreadable  
- `other` — specify briefly

---

## Log format (table; player-safe)

> Keep snippets short and spoiler-safe. Pin to **section path + anchor**. Suggest the **smallest viable fix** and the **owner**.

| When | Location (path#anchor) | Tag(s) | Severity | Snippet (safe) | Smallest viable fix | Owner | Notes |
|---|---|---|---|---|---|---|---|
| 00:03 | `/manuscript/act1/foreman-gate#entry` | choice-ambiguity | med | “Go / Proceed.” | Sharpen to intent-forward verbs | Style → Scene | Contrast: “Slip through maintenance / Face the foreman.” |
| 00:06 | `/manuscript/act1/foreman-gate#scanner` | gate-friction | high | “Option locked: missing CODEWORD.” | Swap to diegetic refusal line | Style → Scene | “The scanner blinks red. ‘Union badge?’” |
| 00:09 | `/views/…/index.html#union-token` | nav-bug | med | Link jumps to top | Fix anchor or TOC id | Binder | Check kebab-case slug, no diacritics |
| 00:12 | `/codex/inspection-logs` | translation-glitch | low | “greenlighted” | Neutral, portable term | Translator | Prefer “approved” |

**Severity rubric:** *low* (minor polish), *med* (confuses some players), *high* (blocks clarity/fairness/access).

---

## Micro-recaps (optional, ≤2 lines each)

> If a recap would help, write it **in-voice** and **player-safe**. Owners will decide.

```

* "<state change>. <current stakes>."
* "You hold your ground. The queue tightens."

```

---

## Breath units & cadence (quick ticks)

- Near choice lists, lines average **≤ 12–16 words** ✅/❌  
- Sentences avoid stacked prepositional phrases ✅/❌  
- Gate refusals are **one beat** long (short cue + line) ✅/❌

---

## Accessibility sweep (PN-level)

- Captions present and concise? ✅/❌  
- Alt text present and concrete (subject + relation + location)? ✅/❌  
- Numbers, units, and titles pronounce cleanly? ✅/❌ (note collisions)

---

## Handoffs

```

To Style: tags = choice-ambiguity, gate-friction, tone-wobble
To Scene: apply Style’s exemplars on listed locations
To Binder: nav-bug & label-collision
To Translator: translation-glitch with anchor notes
To Gatekeeper: one sample per tag for gatecheck

```

---

## Done checklist (tick before submitting)

- [ ] All notes **player-safe**; no spoilers/internals  
- [ ] Each note has **location, tag, smallest fix, owner**  
- [ ] Severity set using rubric; only **high** blocks are marked as such  
- [ ] Micro-recaps (if any) fit **PN patterns** (see Style Addendum)  
- [ ] Handoffs listed; TU and Trace updated

---

## Mini example (filled, safe)

```

PN Playtest Notes — ActI-ForemanGate-EN
Run: 2025-10-29 20:10 · PN: PN-01 · TU: TU-2025-10-29-PN01
Snapshot: Cold @ 2025-10-28 · Targets: HTML
Mode: dry-run · Pace: normal

Notes:

* 00:03 /manuscript/act1/foreman-gate#entry — choice-ambiguity (med)
  Fix: intent-forward verbs — Owner: Style→Scene
  Example: “Slip through maintenance / Face the foreman.”

* 00:06 /manuscript/act1/foreman-gate#scanner — gate-friction (high)
  Fix: diegetic refusal — Owner: Style→Scene
  Example: “The scanner blinks red. ‘Union badge?’”

* 00:09 /views/ActI-ForemanGate-EN/index.html#union-token — nav-bug (med)
  Fix: check slug; Binder to normalize

Micro-recap candidates:

* “You kept the badge pocketed. The inspection line tightens.”

Accessibility:

* Captions n/a; Alt present on images; numbers read fine.

Handoffs:
@style @scene @binder @gatekeeper

```
