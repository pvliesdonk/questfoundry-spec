# Glossary — Common Language (Layer 2)

> **Status:** 🚧 **PARKED — Pending Layer 2 proper draft**
>
> This file was moved from `00-north-star/TERMINOLOGY.md` during architectural cleanup (2025-10-29). It contains core system terminology but belongs in Layer 2 (data dictionary) rather than Layer 0 (policy). Content is unchanged pending full Layer 2 review.

Clear words prevent weird bugs. This glossary defines how we use key terms across roles. These are **human** definitions for Layer 2; technical codification (schemas/protocol) comes in Layers 3–4.

---

## A. Narrative topology

**Section** — A unit of prose that ends in one or more **choices**.

**Choice** — A player-facing action at the end of a section that links to another section.

**Hub** — A section (or cluster) with meaningful fan-out to multiple distinct routes.

**Loop** — A design that returns the reader to a prior location **with difference** (new context, options, or consequences).

**Gateway** — A diegetic condition controlling access (e.g., a token, reputation, knowledge, or tool). PN enforces gates **in-world**; internal labels never surface.

**Codeword** — A hidden state flag used by the system to alter future outcomes. **Names of codewords never appear on player surfaces.** Surfaces speak in-world (“the foreman spots your union token”).

---

## B. Sources of Truth (SoT)

**Hot** — Discovery space: drafts, hooks, canon work-in-progress, plan-only art/audio/translation. Spoilers allowed.

**Cold** — Curated canon and **player-safe surfaces** (codex summaries, captions, localized text). No spoilers, no internal labels.

**Snapshot** — An immutable tag of **Cold** (e.g., `cold@2025-10-28`). Exports are cut from snapshots.

**View** — A player-safe export bundle (MD/HTML/EPUB/PDF) built from a snapshot via **Binding Run**.

---

## C. Traceability

**Trace Unit (TU)** — A small, scoped change record (who/why/what/risks/hand-offs). Lives in Hot; referenced by PRs and merge notes.

**Merge Train** — The sequence: Loop in Hot → Gatecheck → Merge to Cold → Snapshot → View.

**View Log** — A record inside the export noting snapshot ID, included options (art/audio/translations), and notable TUs since last view.

---

## D. Roles (canon names)

**Showrunner** — Coordinates loops, wakes dormant roles, approves merges and exports.

**Gatekeeper** — Enforces **Quality Bars** before Cold merges and in exports.

**Plotwright** — Designs topology: hubs/loops/gateways; drafts section briefs.

**Scene Smith** — Writes/rewrites section prose to briefs and style.

**Lore Weaver** — Turns accepted hooks into spoiler-level **canon** (backstory, timeline, causality).

**Codex Curator** — Publishes **player-safe** entries and cross-refs; never invents deep lore.

**Style Lead** — Maintains voice/register/motifs and phrasing patterns.

**Researcher** *(optional/dormant)* — Verifies factual claims; assigns uncertainty levels.

**Art Director / Illustrator** *(optional/dormant)* — Plan and/or render illustrations.

**Audio Director / Audio Producer** *(optional/dormant)* — Plan and/or produce sound.

**Translator** *(optional/dormant)* — Builds language packs and localized surfaces.

**Book Binder** — Assembles exports (views) from Cold.

**Player-Narrator (PN)** — Performs the book in-world; enforces gates diegetically; reports UX issues.

---

## E. Work units

**Hook** — A compact proposal (idea/uncertainty/tell) small enough to triage. Types: `narrative | scene | factual | taxonomy`. Status: `proposed | accepted | deferred | rejected`.

**Canon** — Spoiler-level truth authored by Lore Weaver (causal, time-anchored). Player-safe summaries live in the **codex**, not here.

**Plan-only** — A merged plan without assets (e.g., art captions/intent, audio cue sheets, glossary). Marked **deferred** until assets land.

---

## F. Safety & Quality

**Player-safe surface** — Text a player can see: manuscript, codex, captions, PN lines. No spoilers, no internal labels, no technique talk.

**Quality Bars** — Merge/expor­t criteria: **Integrity**, **Reachability**, **Nonlinearity**, **Gateways**, **Style**, **Determinism** (when promised), **Presentation** (spoiler & accessibility hygiene).

**Determinism (assets)** — If promised, renders/cues carry reproducibility notes (seed/model or DAW/session). Never surface technique to players.

---

## G. Localization

**Language Pack** — Glossary, register map, motif equivalence, idiom strategy, localized surfaces, coverage %, open issues.

**Coverage %** — Portion of sections/codex entries localized in a slice; exports label slices `complete` / `incomplete`.

---

## H. Naming & references

**Player-safe ref** — A human ref that avoids internal IDs (e.g., “Dock 7 — Foreman’s Gate” rather than `s41` or `CODEWORD: ASH`).

**Lineage** — A one-line pointer in a doc noting the TU/snapshot that produced it, without spoilers.

---

### Notes

- These are **definitions**, not schema fields. Technical codification lives later (Layers 3–4).
- When a term risks spoiler leakage, prefer **player-safe phrasing** on surfaces and keep labels in Hot.
