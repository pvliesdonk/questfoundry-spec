# TU Brief — Small, Focused Loop (Layer 1, Human-Level)

> **Use this to open a timeboxed task unit (TU).** Keep it one sitting, wake only needed roles, cite the bars you’ll press, and define what “done” means. Views are cut from **Cold**; never ship Hot.

---

## Normative references

- Bars & safety: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md` · `../../00-north-star/ACCESSIBILITY_AND_CONTENT_NOTES.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md`
- Handshakes & policy: `../interfaces/pair_guides.md` · `../interfaces/dormancy_signals.md` · `../interfaces/escalation_rules.md`
- Roles & ownership: `../raci/by_loop.md` · `../checklists/role_readiness.md`

---

## Fill-this template (copy/paste)

```

# TU: <loop> — <slice name>

ID: <tu-id> · Opened: <YYYY-MM-DD> · Owner (A): <showrunner> · Responsible (R): <roles>

## Scope

Loop: <Story Spark | Style Tune-up | Hook Harvest | Lore Deepening | Codex Expansion | Art Touch-up | Audio Pass | Translation Pass | Binding Run | Narration Dry-Run>
Slice: <short description, e.g., “Act I: Foreman Gate (3 sections)”>
Snapshot context: align to Cold @ [cold@YYYY-MM-DD](mailto:cold@YYYY-MM-DD) (no Hot in Views)

## Roles

Awake: <PW, SS, ST, LW, CC, AD, IL, AuD, AuP, TR, BB, PN, GK>
Dormant: <list> · Deferral tags: <deferred:art | deferred:audio | deferred:translation | deferred:research>

## Bars (press/monitor)

Press: <Integrity | Reachability | Nonlinearity | Gateways | Style | Presentation | Accessibility>
Monitor: <others>
Pre-gate risks: <bullets; smallest likely failures>

## Inputs (must exist before start)

* <briefs/notes/canon summaries/codex anchors/register map/etc.>
* Pairing plan: <which pair guides will be used>

## Deliverables (exit artifacts)

* <clear, small list; e.g., “3 section briefs + gateway map excerpt”>
* <hooks, addenda updates, packs, shotlist/cuelist deltas, view log entry>

## Exit (bars green + artifacts)

* Bars green: <which bars must be green for this TU>
* Merge/View: <merge to Cold? cut a View?> (Binder involved? yes/no)

## Timebox & cadence

Timebox: <45–90 min> · Checkpoint: [HH:MM](HH:MM) · Handoffs: <who, when>

## Gatekeeper

Pre-gate: @gatekeeper (sample: <files/anchors>)
Gatecheck: @gatekeeper (pass/fail by bar; smallest viable fixes)

## Escalation (if blocked)

Trigger: <one-sentence decision>
Lane: <owner per escalation_rules.md> · Record: <TU note | Addendum | Pack | View Log | ADR>

## Trace

Tracelog: <path or note> · Linkage: hooks filed @ <paths> · Snapshot/View impact: <notes>

```

---

## One-page example (filled, safe)

```

# TU: Style Tune-up — Foreman Gate phrasing

ID: TU-2025-10-28-FT01 · Opened: 2025-10-28 · Owner (A): SR · Responsible (R): ST

## Scope

Loop: Style Tune-up
Slice: Act I — 3 sections around “Foreman Gate”
Snapshot context: Cold @ 2025-10-27

## Roles

Awake: ST, GK, SS
Dormant: AD, IL, AuD, AuP, TR, LW, CC, BB, PN
Deferral tags: deferred:art · deferred:audio · deferred:translation

## Bars (press/monitor)

Press: Style, Presentation
Monitor: Gateways
Pre-gate risks: meta gate wording; near-synonym choices

## Inputs

* Plot briefs for the 3 sections
* Latest Style Addendum; PN gate patterns
* Pairing: Style ↔ PN (pattern review) if needed

## Deliverables

* Updated Style Addendum: 3 exemplar gate lines; banned phrases list
* Edit notes to Scene for 3 sections
* Hooks for Curator (anchor “Union Token” wording)

## Exit

Bars green: Style, Presentation (for these 3 sections)
Merge/View: Merge to Cold; no View this TU

## Timebox & cadence

Timebox: 60 min · Checkpoint: 30 min · Handoffs: edit notes to SS at end

## Gatekeeper

Pre-gate: @gatekeeper (sample lines before rollout)
Gatecheck: @gatekeeper (confirm diegetic phrasing; no meta)

## Escalation

Trigger: if gate fairness questioned → Plot lane decision
Lane: Plotwright (owner) · Record: TU note

## Trace

Tracelog: /logs/tu/TU-2025-10-28-FT01.md
Linkage: hooks @ /hot/hooks/union-token-anchor.md
Snapshot/View impact: none (text-only small pass)

```

---

## Reminders

- **Small slice or it’s not a TU.** If scope balloons, split and chain.  
- **Bars beat vibes.** Name which bars you’ll flip to green.  
- **Dormancy is explicit.** Use `deferred:*` tags and front-matter notes (Binder).  
- **Never ship from Hot.** Cold-only for Views; Binder states options & coverage.  
- **Record decisions.** If you set precedent, write an ADR (`../../DECISIONS/`).

---
