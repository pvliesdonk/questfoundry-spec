# View Log — Bound, Player-Safe Output Record (Layer 1, Human-Level)

> **Use:** Book Binder’s one-pager for any bound *View* (export). Declares the **Cold** snapshot, **options/coverage**, anchor health, and any `deferred:*` tracks. No spoilers, no Hot content.

---

## Normative references

- Bars & hygiene: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md` · `../../00-north-star/ACCESSIBILITY_AND_CONTENT_NOTES.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md`
- Interfaces & lanes: `../interfaces/escalation_rules.md` · `../interfaces/dormancy_signals.md`
- Role brief: `../briefs/book_binder.md` · Gatekeeping: `../checklists/quality_bars_by_role.md`

---

## Header

```

View Log — <view-name>
Bound: <YYYY-MM-DD> · Binder: <name/agent> · TU: <id>
Cold snapshot: [cold@YYYY-MM-DD](mailto:cold@YYYY-MM-DD)  (no Hot)
Targets: <PDF | HTML | EPUB | Web-bundle | …>

```

---

## 1) Options & Coverage (player-safe)

```

Art: <none | plans-only | renders-included>     Tag: [deferred:art?](deferred:art?)
Audio: <none | plans-only | cues-included>      Tag: [deferred:audio?](deferred:audio?)
Languages: <EN 100% | NL 74% | …>               Tag: [deferred:translation?](deferred:translation?)
Research posture surfaced: <neutral phrasing only | none>  Tag: [deferred:research?](deferred:research?)
Accessibility snapshot: alt <present/na>, captions <present/na>, reading order <ok>, contrast <ok/na>

```

---

## 2) Anchor Map (integrity check)

> Summarize resolution state; details in attached report if large.

```

Manuscript anchors: <N> (resolved: <N>; orphans: <0|N>)
Codex anchors: <N> (resolved: <N>; orphans: <0|N>)
Crosslinks (ms ↔ codex): <N> (broken: <0|N>)
Locale anchors (if multilingual): <policy: ASCII kebab-case | other> (collisions: <0|N>)
Notes: <one line if any renames or slugs normalized>

```

---

## 3) Presentation & Accessibility (gatecheck result)

```

Presentation: <green | yellow | red> — notes: <smallest-viable-fix if yellow/red>
Accessibility: <green | yellow | red> — notes: <alt/caption gaps, reading-order, etc.>
Gatekeeper: <name> · Gatecheck ID: <id>

```

---

## 4) Export Artifacts

| Kind | Path/Name | Hash/ID (optional) | Notes |
|---|---|---|---|
| PDF | /views/<view-name>.pdf | <sha256…> | front-matter present |
| HTML | /views/<view-name>/index.html | <sha256…> | anchors stable |
| EPUB | /views/<view-name>.epub | <sha256…> | nav ok |
| Bundle | /views/<view-name>.zip | <sha256…> | contains View + PN kit |

> Hashes are optional but recommended for reproducibility.

---

## 5) Front-Matter (what the View declares to players)

> Copy the front-matter section that ships **in the View** (player-safe).

```

Title: <title> · Version: <semver or date>
Snapshot: Cold @ <YYYY-MM-DD>
Options: art=<none|plans|renders>, audio=<none|plans|cues>, locales=<EN, NL(74%)>
Accessibility: alt=<present>, captions=<na>, reading-order=<ok>
Notes: <short, player-safe remark if needed>

```

---

## 6) Known Deferrals & Follow-ups

```

Deferrals: <deferred:art | deferred:audio | deferred:translation | deferred:research>
Follow-up TUs:

* TU-<id> — <role> — <slice> — <one-sentence goal> — due <date>

```

---

## 7) Incidents & Fixes (if any)

```

Incident: <anchor collision in NL> — Impact: <codex links> — Fix: <normalized slugs> — Owner: Translator · Record: ADR-XX (if policy)
Incident: <caption idiom opaque> — Fix: neutral variant — Owner: Style/Translator

```

---

## 8) Done checklist (tick before publishing)

- [ ] Bound from **Cold**; no Hot bleed  
- [ ] **Options & coverage** stated (and match reality)  
- [ ] **Anchor Map**: no unresolved red flags (or follow-up TU listed)  
- [ ] **Gatecheck** recorded (Presentation/Accessibility status)  
- [ ] Export artifacts listed; hashes optional but present if policy  
- [ ] Front-matter block copied verbatim into the View  
- [ ] Deferrals tagged; follow-ups scheduled; trace updated

---

## Mini example (safe)

```

View Log — ActI-ForemanGate-EN
Bound: 2025-10-29 · Binder: BB-01 · TU: TU-2025-10-29-BIND01
Cold snapshot: cold@2025-10-28
Targets: HTML, PDF

1. Options & Coverage
   Art: plans-only        Tag: deferred:art
   Audio: none            Tag: deferred:audio
   Languages: EN 100%     Tag: —
   Research posture: neutral phrasing only   Tag: deferred:research
   Accessibility: alt present, captions n/a, reading order ok

2. Anchor Map
   Manuscript anchors: 42 (resolved: 42; orphans: 0)
   Codex anchors: 7 (resolved: 7; orphans: 0)
   Crosslinks: 19 (broken: 0)
   Locale anchors: ASCII kebab-case policy; collisions: 0
   Notes: normalized two internal section slugs to kebab-case

3. Gatecheck
   Presentation: green — no technique on surfaces
   Accessibility: green — alt present; choice lists clean
   Gatekeeper: GK-02 · Gatecheck ID: GC-2025-10-29-07

4. Export Artifacts
   | Kind | Path/Name                          | Hash/ID             | Notes                 |
   | PDF  | /views/ActI-ForemanGate-EN.pdf     | 2ce9…b71            | front-matter present  |
   | HTML | /views/ActI-ForemanGate-EN/index.html | 8b54…90e          | anchors stable        |

5. Front-Matter
   Title: “Dock Seven — Act I”
   Version: 2025.10.29
   Snapshot: Cold @ 2025-10-28
   Options: art=plans, audio=none, locales=EN
   Accessibility: alt=present, captions=na, reading-order=ok
   Notes: —

6. Deferrals & Follow-ups
   Deferrals: deferred:art · deferred:audio · deferred:research
   Follow-ups:

* TU-2025-10-31-AD02 — Art Director — signpost image plan → render candidate — 2025-10-31
* TU-2025-11-02-RS01 — Researcher — dock reader firmware posture — 2025-11-02

7. Incidents & Fixes
   None.

8. Checklist
   [✔] cold-only  [✔] options/coverage  [✔] anchors ok  [✔] gatecheck recorded  [✔] artifacts listed  [✔] front-matter copied  [✔] deferrals & TUs logged

```
