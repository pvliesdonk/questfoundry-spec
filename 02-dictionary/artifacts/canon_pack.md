# Canon Pack — Answers in Hot + Player-Safe Summaries (Layer 1, Human-Level)

> **Use:** Lore Weaver’s bundle that turns **accepted hooks** into coherent **canon** (Hot) and exports **player-safe summaries** (Cold) for neighbors. Keep the split explicit: **Hot may contain spoilers; Cold must not.** This is a *human template* (no schemas).

---

## Normative references

- Bars & hygiene: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md`
- Interfaces & lanes: `../interfaces/pair_guides.md` · `../interfaces/escalation_rules.md`
- Role briefs: `../briefs/lore_weaver.md` · neighbors in `../briefs/*.md`

---

## Header

```

Canon Pack — <cluster name>
TU: <id> · Edited: <YYYY-MM-DD> · Owner: Lore Weaver
Slice: <scope, e.g., "Act I — Dock 7 & Foreman Gate">
Hooks answered: <list of hook IDs/short names>
Research posture touched: <corroborated | plausible | disputed | uncorroborated:low | uncorroborated:medium | uncorroborated:high>
Sensitivity: <none | content note refs>

```

---

## 1) Canon Answers (Hot)

> **Spoilers allowed.** Short, decisive answers to each accepted hook.

```

[H-01] <hook short name>
Answer: <2–6 lines; crisp; avoid prose flourish>
Evidence/Reasoning (if relevant): <short; cite Research posture if used>
Consequences: <1–3 bullets; what this enables/constrains>

```

*(Repeat per hook in this cluster.)*

---

## 2) Timeline Anchors (Hot)

> Place events on a simple axis so neighbors can reason about “before/after/ongoing.”

```

T0 <past anchor>: <event> — <who involved> — <where>
T1 <recent>: <event> — <effect on present>
T2 <now>: <state at start of slice>
T3 <near-future invariant>: <what must happen or cannot happen during slice>

```

---

## 3) Invariants & Constraints (Hot)

> Name the **things that must stay true** (physics, politics, metaphysics, procedures).

- **Invariant:** <short statement> — *Owner:* <Lore/Plot/Curator> — *Why:* <1 line>  
- **Constraint:** <cannot/only if> — *Implication:* <gates, routes, risks>

---

## 4) Entity/State Deltas (Hot)

> What changed because of these answers? Track deltas to characters, factions, places, items.

| Entity | Before | After | Visibility (who could know) |
|---|---|---|---|
| <name> | <state> | <state> | <crew / foreman / public / nobody> |

---

## 5) Knowledge Ledger (Hot)

> **Who knows what, when.** Prevent accidental omniscience.

| Actor | Knows at T0 | Gains at T1/T2 | Notes (how they’d express it) |
|---|---|---|---|
| <actor> | <facts> | <new facts> | <speech patterns, euphemisms> |

---

## 6) Player-Safe Summaries (Cold)

> **No spoilers, no internals.** What neighbors may surface to players right now.

- **Summary S-01** *(for Curator/Scene/Style/PN)*  
  Topic: <concept, place, procedure>  
  Player-safe text (2–4 lines):  
  “<neutral description that enables choices without revealing causes or twists>”  
  Notes to Translator: <register hints/idioms to avoid>  
  See-also: <entries/anchors>

*(Repeat per concept needing a surface-safe summary.)*

---

## 7) Downstream Effects (to neighbors)

> Give each neighbor the **actionable** next steps—still **player-safe** in phrasing.

- **Plotwright:**  
  - Gate reason(s): <diegetic checks the world enforces>  
  - Loop-with-difference seeds: <small state deltas that justify meaningful returns>  
  - Keystone resilience: <fallback route or soft-fail suggestion>

- **Scene Smith:**  
  - Phrasing cues: <what the world would *show/say* at the gate>  
  - Micro-context: <one line to clarify choice contrast>

- **Style Lead:**  
  - Pattern nudge: <banned/preferred forms tied to this canon>  
  - Example (player-safe): “<1–2 lines>”

- **Codex Curator:**  
  - New/updated entries: <list of titles>  
  - Crosslink hints: <A ↔ B ↔ C>  
  - Anchor slugs: <kebab-case suggestions>

- **Translator:**  
  - Terminology risks: <polysemy, diacritics, RTL/anchor policy>  
  - Register map nudge: <pronouns/formality if relevant>

- **Gatekeeper:**  
  - Presentation watchouts: <risk of meta leaks; anchor collisions to check>

---

## 8) Open Questions & Hooks (leftovers)

> Keep scope tight: what you **did not** answer now—file as hooks.

- `hook://lore/<topic>` — <one-line question> — *Reason to defer:* <not needed for current slice>  
- `hook://curator/<term>` — <needs entry or taxonomy>  
- `hook://plot/<structure>` — <requires topology decision>  
- `hook://research/<claim>` — <needs corroboration; current posture = <…>>

---

## 9) Checks (tick before handoff)

- [ ] All accepted hooks in this cluster have **Hot answers** or a deferral hook  
- [ ] **Timeline** updated; deltas recorded; invariants explicit  
- [ ] **Knowledge ledger** prevents unwanted omniscience  
- [ ] **Player-safe summaries** written for every exposed concept  
- [ ] **Downstream effects** list is actionable and spoiler-safe  
- [ ] Research posture noted; sensitivities addressed (or flagged)  
- [ ] Trace updated; neighbors tagged; escalation not needed / filed if so

---

## 10) Traceability

```

Lineage: TU <id> · Edited <YYYY-MM-DD> · Lore Weaver: <name or agent>
Neighbors notified: @plot @scene @style @curator @translator @gatekeeper
Snapshot impact: <none | will require Cold update after owners apply>
Related: Research memos <ids> · Prior Canon Packs <ids> · ADRs <ids if policy touched>

```

---

## Mini example (safe)

```

Canon Pack — “Foreman Backstory”
TU: TU-2025-10-28-LW01 · Edited: 2025-10-28 · Owner: Lore Weaver
Hooks answered: H-02 Foreman scar origin; H-03 Why inspections hardened
Posture: plausible (no public records on retrofit)
Sensitivity: workplace injury (see content notes)

1. Canon Answers (Hot)
   [H-02] Scar origin
   Answer: Burn from plasma backflow during unauthorized retrofit; foreman coerced by Toll intermediaries; guilt → stricter inspections.
   Consequences: foreman avoids night-shift socializing; keeps scanner logs tidy.

2. Timeline Anchors (Hot)
   T0: Retrofit accident (year −2)
   T1: Union inquiry fizzles (year −1)
   T2: Now: inspections are by-the-book; rumor persists

3. Invariants & Constraints (Hot)
   Invariant: Union tokens must be visually verifiable under dock lighting.

4. Player-Safe Summary (Cold)
   Topic: Dock inspections
   Text: “Dock inspections are stricter than they used to be; badges are checked by sight, and logs are kept clean.”
   Translator note: keep neutral; avoid implying wrongdoing.

5. Downstream Effects
   Plotwright: Gate reason — visual badge check + foreman recognition plausible; offer insider route as loop-with-difference.
   Scene: Gate line cue — “The scanner blinks red. ‘Union badge?’”
   Curator: Entries — Union Token; Inspection Logs
   Style: Ban “option locked”; prefer diegetic refusals.

6. Hooks
   hook://curator/inspection-logs — entry with overview/usage/context
   hook://research/retrofit-standards — posture corroboration

```

---
