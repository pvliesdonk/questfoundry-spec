# Front Matter — Player-Safe View Header (Layer 1, Human-Level)

> **Use:** Book Binder’s player-facing header that tops any bound **View** (PDF/HTML/EPUB/bundle). Declares **what this View is**, **which Cold snapshot it reflects**, and **what options/coverage** are included (art/audio/locales/accessibility). No spoilers, no Hot content, no internal technique.

---

## Normative references

- Bars & hygiene: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md` · `../../00-north-star/ACCESSIBILITY_AND_CONTENT_NOTES.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md`
- Binder/View logging: `./view_log.md`
- Interfaces & lanes: `../interfaces/escalation_rules.md` · `../interfaces/dormancy_signals.md`
- Role brief: `../briefs/book_binder.md`

---

## 1) Required fields (player-safe)

```

Title: <book or slice title>
Version: <semver or YYYY.MM.DD>
Snapshot: Cold @ <YYYY-MM-DD>
Options: art=<none|plans|renders>, audio=<none|plans|cues>, locales=<EN[, NL(74%) …]>
Accessibility: alt=<present|na>, captions=<present|na>, reading-order=<ok>, contrast=<ok|na>
Notes: <1–2 short lines max; no spoilers or internals>

```

**Rules:**

- **Title** matches cover/TOC; avoid internal code names.  
- **Version** may be date-based; avoid commit hashes in player surfaces.  
- **Snapshot** is a Cold date, never a Hot ref.  
- **Options** mirror reality; if a track is plan-only, reflect it.  
- **Accessibility** declares what’s present now (not promises).  
- **Notes** must be neutral; do not hint at twists or behind-the-scenes methods.

---

## 2) Optional fields (use sparingly)

```

Edition: <Standard | Annotated | Classroom | …>
Audience note: <content/reading guidance in one line>
Changelog (short): <bullet of what changed since last public version; 1–3 items, no spoilers>

```

> If you need more than one screen of front matter, you’re writing a blog post. Keep it tight.

---

## 3) Example blocks (safe)

**A) Prose-only, single-locale**

```

Title: Dock Seven — Act I
Version: 2025.10.29
Snapshot: Cold @ 2025-10-28
Options: art=none, audio=none, locales=EN
Accessibility: alt=na, captions=na, reading-order=ok
Notes: Interactive paths with hubs and loops; choices are contrastive.

```

**B) Plans-only art, partial translation**

```

Title: Dock Seven — Checkpoint Cut
Version: 2025.11.03
Snapshot: Cold @ 2025-11-02
Options: art=plans, audio=none, locales=EN, NL(76%)
Accessibility: alt=present, captions=na, reading-order=ok
Notes: Illustrations are planned but not yet included; Dutch translation is in progress.

```

**C) Renders + cues, multilingual**

```

Title: Dock Seven — Release 1
Version: 1.2.0
Snapshot: Cold @ 2025-11-07
Options: art=renders, audio=cues, locales=EN, NL
Accessibility: alt=present, captions=present, reading-order=ok, contrast=ok
Notes: Audio cues fade before choice lists. Captions are in-world, one line each.

```

---

## 4) Binder checklist (before publish)

- [ ] Text is **player-safe**; no spoilers, no technique (seeds/models/DAW).  
- [ ] **Snapshot** date matches the View’s Cold source.  
- [ ] **Options** match the actual contents; deferrals reflected (`deferred:*` in `View Log`).  
- [ ] **Accessibility** fields filled truthfully (present/na/ok).  
- [ ] Localization coverage stated clearly (percentages only in View Log).  
- [ ] Front matter **copied verbatim** into `View Log` §5.  
- [ ] Links/anchors within front matter (if any) resolve (Integrity green).

---

## 5) Escalation triggers (if you can’t keep it safe)

- Any need to mention **process, models, seeds, or tools** → **remove**; if policy tension exists, escalate to **Showrunner** (ADR likely unnecessary—usually Presentation hygiene).  
- Pressure to hint at **future plot** or **hidden logic** → route to **Style** for neutral rephrasing.  
- Locale anchor policy disagreement → **Translator ↔ Binder** (see Register Map & Language Pack); record in `View Log`.

---
