# Gatecheck Report — Bars Status & Smallest Fixes (Layer 1, Human-Level)

> **Use:** Gatekeeper’s formal pass on a TU or a bound View. Name each **Bar** status (**green/yellow/red**), cite the **smallest viable fix**, and route to the correct owner. Keep examples **player-safe**; never paste Hot.

---

## Normative references

- Bars & hygiene: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md` · `../../00-north-star/ACCESSIBILITY_AND_CONTENT_NOTES.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md`
- Dormancy & loops: `../interfaces/dormancy_signals.md` · `../raci/by_loop.md`
- Escalation lanes: `../interfaces/escalation_rules.md`
- Binder/View logging (if export): `./view_log.md`

---

## Header

```

Gatecheck Report — <TU id | View name>
Checked: <YYYY-MM-DD> · Gatekeeper: <name/agent>
Scope: <slice or export target> · Mode: <pre-gate | gatecheck>
Cold snapshot: [cold@YYYY-MM-DD](mailto:cold@YYYY-MM-DD) (no Hot examined beyond samples)
Artifacts/Samples: <paths or short list>
Dormancy state: <deferred:art? deferred:audio? deferred:translation? deferred:research?>

```

---

## 1) Summary (one screen)

```

Decision: <pass | conditional pass | block>
Why: <one or two lines tied to Bars>
Next actions: <smallest viable fixes + owners>

```

---

## 2) Bars Table (status per bar)

> Mark **green/yellow/red**. For **yellow/red**, give the **smallest fix** and owner.

| Bar | Status | Evidence (player-safe) | Smallest viable fix | Owner (R) | Notes |
|---|---|---|---|---|---|
| Integrity | green/yellow/red | <anchor map, sample paths> | <e.g., normalize 2 slugs> | Binder/Translator/Curator | <brief> |
| Reachability | green/yellow/red | <choice clarity test> | <sharpen labels on 2 nodes> | Style → Scene | <brief> |
| Nonlinearity | green/yellow/red | <loop-with-difference sample> | <add state delta line> | Plotwright/Scene | <brief> |
| Gateways | green/yellow/red | <diegetic check lines> | <swap meta to diegetic> | Style → Scene | <brief> |
| Style | green/yellow/red | <register/cadence issues> | <apply pattern; 3 lines> | Style | <brief> |
| Presentation | green/yellow/red | <spoiler/technique leaks?> | <remove technique; revise caption> | Style/AD/AuD | <brief> |
| Accessibility | green/yellow/red | <alt/caption/readability> | <write alt; shorten lines> | AD/IL/AuD/Style | <brief> |

**Rubric:**  

- **green** = no blocking defects in this slice/export.  
- **yellow** = minor, mergeable with *named* follow-up TU.  
- **red** = blocks merge/view until fixed.

---

## 3) Incidents (optional, concise)

```

* <type> — <location> — Impact: <bar> — Fix: <smallest> — Owner: <role>

```

---

## 4) Deferrals & Coverage (if export/View)

> Player-safe; mirror what will go into the `View Log`.

```

Art: <none | plans-only | renders-included>   Tag: [deferred:art?](deferred:art?)
Audio: <none | plans-only | cues-included>    Tag: [deferred:audio?](deferred:audio?)
Locales: <EN 100% | NL 74% | …>               Tag: [deferred:translation?](deferred:translation?)
Accessibility snapshot: <alt present/na; captions present/na; reading-order ok>

```

---

## 5) Handoffs (smallest next steps)

```

* <Bar> — <fix> — Owner: <role> — TU: <new-id or “SR to open”> — Due: <date>

```

---

## 6) Escalation (only if needed)

```

Topic: <one-sentence decision> · Lane: <owner> · Level: <L1 micro | L2 cross-domain | L3 policy/ADR>
Bundle attached: <yes/no> (see escalation_rules.md §5)

```

---

## 7) Done checklist

- [ ] Decision stated (**pass/conditional pass/block**) tied to **Bars**  
- [ ] Each **yellow/red** has a **smallest viable fix** + **owner**  
- [ ] Player-safe examples only; no Hot canon or internals copied  
- [ ] Dormancy tags noted; export coverage reflected if relevant  
- [ ] Handoffs created (TU ids or “SR to open”)  
- [ ] Trace updated (path/id) · If export: `View Log` created/updated

---

## Mini example (safe)

```

Gatecheck Report — TU-2025-10-29-ST02 (Style Tune-up: Foreman Gate)
Checked: 2025-10-29 · Gatekeeper: GK-02
Scope: Act I — 3 sections around checkpoint · Mode: gatecheck
Cold snapshot: cold@2025-10-28
Artifacts/Samples: /manuscript/act1/foreman-gate#entry, #scanner
Dormancy: deferred:art · deferred:audio · deferred:translation

1. Summary
   Decision: conditional pass
   Why: Presentation green; Style green; Gateways yellow (two meta refusals remain).
   Next actions: swap two meta lines to diegetic; sharpen one choice pair.

2. Bars Table
   | Bar          | Status | Evidence                               | Smallest fix                                | Owner         | Notes |
   |--------------|--------|----------------------------------------|----------------------------------------------|---------------|-------|
   | Integrity    | green  | anchors resolve in sample               | —                                            | Binder        | —     |
   | Reachability | green  | contrastive labels in two nodes         | —                                            | Style→Scene   | —     |
   | Nonlinearity | green  | loop-with-difference observed           | —                                            | Plotwright    | —     |
   | Gateways     | yellow | “Option locked” at #scanner             | swap to diegetic refusal line                | Style→Scene   | use pattern from Style Addendum |
   | Style        | green  | cadence ok near choices                 | —                                            | Style         | —     |
   | Presentation | green  | no spoilers/technique on surfaces       | —                                            | —             | —     |
   | Accessibility| green  | alt present; short sentences near lists | —                                            | AD/Scene      | —     |

3. Incidents

* label-collision — /views/...#UnionToken — Impact: Integrity — Fix: normalize slug to /codex/union-token — Owner: Binder

4. Deferrals & Coverage (N/A for TU)

5. Handoffs

* Gateways — diegetic refusal lines (2) — Owner: Style→Scene — TU: SR to open — Due: 2025-10-30

6. Escalation
   None.

7. Checklist
   [✔] decision  [✔] fixes+owners  [✔] player-safe  [✔] dormancy noted  [✔] handoffs  [✔] trace

```
