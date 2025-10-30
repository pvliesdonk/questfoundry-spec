# Research Memo — Question → Answer → Posture → Neutral Phrasing (Layer 1, Human-Level)

> **Use:** Answer the **smallest useful question** with a short, sourced summary. Label **posture**, provide **player-safe neutral phrasing**, and name **creative implications**. Hot can hold citations; outward text stays spoiler-free.

---

## Normative references

- Bars & hygiene: `../../00-north-star/QUALITY_BARS.md` · `../../00-north-star/SPOILER_HYGIENE.md`
- Sources & trace: `../../00-north-star/SOURCES_OF_TRUTH.md` · `../../00-north-star/TRACEABILITY.md`
- Interfaces & lanes: `../interfaces/pair_guides.md` · `../interfaces/escalation_rules.md`
- Role brief: `../briefs/researcher.md`

---

## Header

```

Research Memo — <topic / question short name>
TU: <id> · Edited: <YYYY-MM-DD> · Owner: Researcher
Slice: <scope, e.g., “Act I — Dock 7 inspections”>
Stakeholders: @plot @lore @style @curator @translator @gatekeeper

```

---

## 1) Question (as used)

> One line, framed in the language of the surface where it appears.

```

Q: <e.g., “Can dock badges be cloned with off-the-shelf gear?”>
Where it appears: </manuscript/...#anchor or codex entry or caption>
Why it matters: <gate fairness | safety | terminology | tone>

```

---

## 2) Short Answer (2–5 lines, plain language)

> Decision-ready summary; no jargon; no spoilers.

```

<Concise answer in prose.>
```

---

## 3) Evidence (Hot)

> Cite 2–5 credible sources. Put URLs/DOIs in Hot; summarize relevance briefly.

```
- <Source 1> — <1 line on relevance>
- <Source 2> — <1 line on relevance>
- <Source 3> — <1 line on relevance>
```

---

## 4) Posture

> Label certainty; use the strict set. If not **corroborated**, offer **neutral phrasing** (next section).

```
Posture: <corroborated | plausible | disputed | uncorroborated:low | uncorroborated:medium | uncorroborated:high>
Caveats: <bullets on gaps, contention, edge cases>
```

---

## 5) Neutral Phrasing (player-safe surface lines)

> 1–3 lines owners can drop into **Cold** without spoilers or internals.

```
- "<safe line 1>"
- "<safe line 2>"
- "<safe line 3>"  (optional)
```

*Rules:* no technique (seeds/models/DAW), no codewords/logic, keep register per Style.

---

## 6) Risks & Mitigations

> Safety, sensitivity, cultural, legal. Plain language.

```
Risks: <bullets>
Mitigations: <bullets—tone, wording, placement, alt/caption guidance>
```

---

## 7) Creative Implications (for owners)

> What this unlocks or forbids. Keep it short and actionable.

```
Plotwright: <affordance/constraint>  
Lore: <canon constraint or invariant suggestion>  
Style/PN: <phrasing or cadence implications>  
Curator/Translator: <term clarity, glossary or anchor concerns>  
Gatekeeper: <bar to watch—Presentation/Accessibility/Integrity>
```

---

## 8) Hooks (follow-ups, if any)

> Things you didn’t chase now.

```
- hook://research/<topic> — <one-line question> — reason: <defer rationale>
- hook://curator/<term> — glossary/entry need
- hook://lore/<cause> — canon choice required
```

---

## 9) Done checklist

- [ ] **Short Answer** (2–5 lines) in plain language
- [ ] **2–5 sources** listed in Hot; relevance summarized
- [ ] **Posture** labeled; **neutral phrasing** supplied if not corroborated
- [ ] **Risks & mitigations** named (safety/culture/legal)
- [ ] **Creative implications** tagged to owners
- [ ] Hooks filed (if scope deferred); trace updated

---

## Mini example (safe)

```
Research Memo — Dock badge cloning
TU: TU-2025-10-28-RS01 · Edited: 2025-10-28 · Owner: Researcher
Slice: Act I — Foreman Gate
Stakeholders: @plot @lore @style @curator @translator @gatekeeper

1) Question
Q: Can a dock badge be cloned with off-the-shelf gear?
Where it appears: /manuscript/act1/foreman-gate#inspection
Why it matters: gate fairness and loop-with-difference route

2) Short Answer
Cloning is **plausible with insider access**; commodity readers resist trivial duplication. Visual checks by staff commonly prevent simple spoofing.

3) Evidence (Hot)
- Trade whitepaper on RFID dock passes — common anti-clone features
- Security conf talk — attack requires firmware access
- Industry forum summary — visual verification policy norms

4) Posture
Posture: plausible
Caveats: variations across docks; outdated readers exist but not typical

5) Neutral Phrasing
- "The scanner hesitates. The foreman studies your lapel."
- "The reader blinks, then waits for the guard's nod."

6) Risks & Mitigations
Risks: implying illegal methods; glamorizing tampering
Mitigations: avoid how-to details; keep lines observational

7) Creative Implications
Plotwright: allow insider route as loop-with-difference; otherwise enforce visual check
Lore: invariant — tokens must be visually verifiable under dock lighting
Style/PN: adopt diegetic refusal pattern; keep sentences short near choices
Curator/Translator: add **Union Token** entry; ensure label localizes cleanly
Gatekeeper: watch for meta language like "option locked"

8) Hooks
hook://research/reader-firmware — prevalence of vulnerable models (defer)
```

---

```
