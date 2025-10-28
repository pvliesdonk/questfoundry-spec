# QuestFoundry — A Layered Studio for Nonlinear Gamebooks

QuestFoundry is a **multi-agent, compositional studio** for making interactive, branching gamebooks. It separates *what we do* (roles, loops, quality bars) from *how machines speak* (schemas, protocol) and *how tools run* (prompts, libraries, UI). Humans and AI can both play the roles—as long as they communicate via structured, validated data (lower layers).

This repository is deliberately layered so that each concern is **clear, testable, and traceable**.

---

## What’s in this repo (at a glance)

- **Layer 0 — North Star** (human): vision, operating model, SoT (Hot/Cold), PN principles, quality bars, loops & playbooks, traceability, spoiler hygiene, accessibility.  
  Start here ➜ `00-north-star/README.md` (Navigator)
- **Layer 1 — Roles** (human): role charters, responsibilities, dormancy policy, RACI patterns.  
  Entry ➜ `01-roles/README.md`
- **Layer 2 — Common Language** (human): data dictionary & controlled terms used by roles (non-technical).  
  Entry ➜ `02-dictionary/README.md`
- **Layer 3 — Codification** (technical): JSON Schemas for the common language. *(Do not implement here yet.)*
- **Layer 4 — Protocol** (technical): interaction rules between roles (Hot ↔ Cold, messages, lifecycles). *(Do not implement here yet.)*
- **Layer 5 — Role Prompts** (technical): AI prompt kits that implement Layer-1 roles using Layer-4 protocol and Layer-3 schemas. *(Future)*
- **Layer 6 — Libraries** (technical): software wrappers, clients, validators, packagers. *(Future)*
- **Layer 7 — UI** (technical): CLI/GUI/PN surfaces for authors and players. *(Future)*

> Today’s focus: **Layer 0 & 1**. Layers 2–7 are first-class directories but intentionally empty or stubs until we define them.

---

## Why layers?

- **Clarity** — People can understand the studio without reading code.  
- **Replaceability** — You can swap AI models/tools without changing canon or roles.  
- **Traceability** — Every change has a **Trace Unit (TU)** and a **Cold snapshot** you can export and play.  
- **Safety** — The **Player-Narrator (PN)** sees only player-safe surfaces; spoilers live in Hot/Canon.

---

## The studio in one breath

- **Showrunner** coordinates **targeted loops** (micro-runs), wakes dormant roles, and merges **Hot → Cold**.  
- **Plotwright** shapes topology (hubs/loops/gateways). **Scene Smith** writes prose.  
- **Lore Weaver** turns **hooks** into canon; **Codex Curator** publishes player-safe pages.  
- **Style Lead** keeps the voice tight.  
- **Art/Audio Directors** plan visuals/sound; **Illustrator/Producer** create assets (optional/dormant).  
- **Translator** maintains language slices.  
- **Gatekeeper** enforces **Quality Bars** before anything touches **Cold**.  
- **Book Binder** exports **views** on Cold; **PN** narrates them diegetically.

See: `00-north-star/WORKING_MODEL.md`, `00-north-star/QUALITY_BARS.md`, `00-north-star/PN_PRINCIPLES.md`.

---

## Micro-loops you’ll run a lot

- **Story Spark** → **Hook Harvest** → **Lore Deepening** → **Codex Expansion**  
- **Style Tune-up** (as needed)  
- **Art Touch-up** / **Audio Pass** (plan-only or plan+assets; optional)  
- **Binding Run** (export a view on Cold) → **Narration Dry-Run** (PN playtest)  
- **Translation Pass** (target-language slice)

Pick loops via: `00-north-star/LOOPS/README.md` and `00-north-star/PLAYBOOKS/README.md`.

---

## Sources of Truth (SoT)

- **Hot**: where discovery, drafts, and **hooks** live.  
- **Cold**: curated canon and player-safe surfaces; exports are cut from **Cold snapshots**.  
- Change is tracked with **Trace Units (TUs)**; merges require **Gatekeeper** pass.  
Details: `00-north-star/SOURCES_OF_TRUTH.md`, `00-north-star/TRACEABILITY.md`, `00-north-star/EVERGREEN_MANUSCRIPT.md`.

---

## Repository layout

```

00-north-star/
README.md                # Navigator for Layer 0
WORKING_MODEL.md         # Studio operating model (Hot/Cold, loops, merges)
ROLE_INDEX.md            # Canonical role names & dormancy
PN_PRINCIPLES.md         # Player-Narrator boundaries
SOURCES_OF_TRUTH.md      # Hot vs Cold SoT
QUALITY_BARS.md          # Gatekeeper checks
TRACEABILITY.md          # Trace Units & snapshots
EVERGREEN_MANUSCRIPT.md  # Export views policy
SPOILER_HYGIENE.md       # Player-surface rules
ACCESSIBILITY_AND_CONTENT_NOTES.md
LOOPS/                   # Loop guides (full_production_run, story_spark, …)
PLAYBOOKS/               # Quick “use-when/outcome” playbooks
01-roles/
README.md                # Role charters & briefs (human-level)
02-dictionary/
README.md                # Non-technical terminology (human-level)
03-codification/           # JSON Schemas (reserved; not authored yet)
04-protocol/               # Interaction protocol (reserved; not authored yet)
05-prompts/                # Role prompt kits (reserved; not authored yet)
06-libraries/              # Software wrappers/validators (reserved)
07-ui/                     # CLI/GUI/PN surfaces (reserved)
DECISIONS/
README.md                # ADR policy & records

```

*(Empty/stub folders for Layers 2–7 exist to keep the layered map navigable now.)*

---

## Contributing

- Read `00-north-star/README.md` and `WORKING_MODEL.md` to understand the studio.  
- Propose changes via **Trace Units (TUs)** in Hot; **Gatekeeper** must pass before Cold merges.  
- See `/CONTRIBUTING.md` and `/CODE_OF_CONDUCT.md` (root) for etiquette and review flow.  
- Architectural rule changes use **ADRs** (`/DECISIONS`), not TUs.

---

## Licensing

This repository is licensed under **MIT**. See `LICENSE`.

---

## Status

Layer-0 is **actively authored**. Layer-1 is in progress. Layers 2–7 are reserved and will be filled once Layer-0/1 stabilize.

---

## Quick start for evaluators

1. Read `00-north-star/README.md` (5 minutes).  
2. Skim `QUALITY_BARS.md` and `PN_PRINCIPLES.md`.  
3. Pick a loop from `PLAYBOOKS/README.md` and run a **Story Spark** micro-loop on a tiny slice.  
4. Export a **Binding Run** view and do a **Narration Dry-Run**.  
5. File **TUs** for any findings and march them through Gatekeeper.

> The book is never “done.” We export **views** on Cold—safe, traceable snapshots you can ship or play today.
