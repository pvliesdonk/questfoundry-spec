# Hook Card — Small, Traceable Follow-Up (Layer 1, Human-Level)

> **Use:** Capture a **new need or uncertainty** without derailing the current TU. Hooks are small, classified, and routed to the right lane. Keep the **player-safe summary** clean; any spoilers live under **Hot Details**.

---

## Normative references

- Bars & hygiene: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md` · `../../00-north-star/ACCESSIBILITY_AND_CONTENT_NOTES.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md` · `../../00-north-star/HOOKS.md`
- Lanes & handshakes: `../interfaces/pair_guides.md` · `../interfaces/escalation_rules.md` · `../interfaces/dormancy_signals.md`
- RACI by loop: `../raci/by_loop.md`

---

## Header

```

Hook Card — <short name>
ID: HK-<YYYYMMDD>-<seq>         Status: open | accepted | in-progress | resolved | dropped
Raised by: <role>               TU: <origin tu-id>        Edited: <YYYY-MM-DD>
Slice: <scope, e.g., “Act I — Foreman Gate (3 sections)”>
Snapshot context: Cold @ <YYYY-MM-DD> (Hot details allowed in §3)

```

---

## 1) Classification

> Choose **one primary** and optional **secondary** types.

- **Type (primary):** <structure | canon | terminology | research | style/pn | translation | art | audio | binder/nav | accessibility>
- **Secondary (optional):** <…>
- **Bars affected:** <Integrity | Reachability | Nonlinearity | Gateways | Style | Presentation | Accessibility>
- **Blocking?:** <no | yes (explain why)>

---

## 2) Player-Safe Summary (1–3 lines)

> What is the smallest player-facing need? **No spoilers, no internals.**

```

<e.g., “Choice labels read as synonyms at the checkpoint; need intent-forward wording.”>

```

---

## 3) Hot Details (optional; spoilers allowed)

> Only if needed to route correctly. Keep brief.

```

<e.g., “Gate fairness hinges on foreman’s prior incident; world reason needed (Lore).”>

```

---

## 4) Proposed Next Step

> Suggest the **smallest** loop and **owner** that can resolve it.

```

Loop: <Story Spark | Style Tune-up | Lore Deepening | Codex Expansion | Art Touch-up | Audio Pass | Translation Pass | Binding Run | Narration Dry-Run>
Owner (R): <role>     Accountable (A): Showrunner
Consult: <roles>      Dormancy: <keep art/audio/translation/research dormant?> (see §6)

```

---

## 5) Acceptance Criteria (exit to green)

> What must be true to close this hook?

- <criterion 1 tied to a Bar>
- <criterion 2 (e.g., “labels contrastive; diegetic gate line present”)>
- <criterion 3 (e.g., “anchors verified in dry bind; 0 collisions”)>

---

## 6) Dormancy & Deferrals (optional)

> If a track can wait safely, declare the fallback.

```

Deferral tags to set now: <deferred:art | deferred:audio | deferred:translation | deferred:research>
Fallback: <neutral phrasing | register map only | plan-only | research posture label>
Revisit: <loop or milestone name/date>

```

---

## 7) Locations & Links

> Pin where this matters and connect related work.

```

Locations (player-safe): </manuscript/...#anchor, /codex/...>
Related hooks: HK-<id>, HK-<id>
Lineage: Canon Packs <ids> · Research Memos <ids> · Style Addendum <id> · ADR <id if policy>

```

---

## 8) Resolution (to be filled on close)

```

Decision: <one sentence>
Work performed: <TU ids>  · View impact: <none | rebind needed>
Gatekeeper result: <bars green summary>
Status → resolved on <YYYY-MM-DD>  · Owner: <role>

```

---

## 9) Done checklist (before handing to Showrunner)

- [ ] Player-safe summary written; classification chosen  
- [ ] Bars named; blocking flag set correctly  
- [ ] Smallest viable next step + owner suggested  
- [ ] Acceptance criteria tied to Bars  
- [ ] Dormancy decision recorded (if applicable)  
- [ ] Locations & lineage linked; trace updated

---

## Mini examples (safe)

**A) Style/PN — choice clarity**

```

Hook Card — “Foreman Gate labels”
ID: HK-20251029-01 · Status: open
Raised by: PN · TU: TU-2025-10-29-PN01 · Edited: 2025-10-29
Slice: Act I — Checkpoint
Snapshot: Cold @ 2025-10-28

1. Classification
   Type: style/pn     Bars: Presentation, Style     Blocking?: yes (confuses players)

2. Player-Safe Summary
   “Choice labels read as near-synonyms; need intent-forward wording.”

3. Proposed Next Step
   Loop: Style Tune-up
   Owner: Style Lead (R) · A: Showrunner · Consult: Scene, Gatekeeper

4. Acceptance Criteria

* Choices read as different intents (Style green)
* Diegetic gate line present (Presentation green)
* PN dry-run confirms cadence

7. Locations & Links
   /manuscript/act1/foreman-gate#entry
   Related: HK-20251028-03 (gate phrasing)

```

**B) Canon → player-safe summary (Curator needed)**

```

Hook Card — “Inspection Logs entry”
ID: HK-20251029-02 · Status: open
Raised by: Style · TU: TU-2025-10-29-ST02 · Edited: 2025-10-29
Slice: Act I — Checkpoint

1. Classification
   Type: terminology     Bars: Integrity, Presentation     Blocking?: no

2. Player-Safe Summary
   “Add a codex entry for ‘Inspection Logs’ to clarify references in gate scenes.”

3. Hot Details
   “Underlying causes exist; Lore already answered in CP-FT-01.”

4. Proposed Next Step
   Loop: Codex Expansion
   Owner: Codex Curator · Consult: Lore (player-safe summary), Translator (variants)

5. Acceptance Criteria

* Entry with Overview/Usage/Context/See-also/Lineage
* Anchors resolve; no orphans in dry bind

```
