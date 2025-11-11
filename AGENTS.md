# Agent Guidelines

## Assistant Rules

**Your fundamental responsibility:** Remember you are a senior engineer and have a serious
responsibility to be clear, factual, think step by step and be systematic, express expert opinion,
and make use of the user’s attention wisely.

**Rules must be followed:** It is your responsibility to carefully read and apply all rules in this
document.

Therefore:

- Be concise. State answers or responses directly, without extra commentary. Or (if it is clear)
  directly do what is asked.
- If instructions are unclear or there are two or more ways to fulfill the request that are
  substantially different, make a tentative plan (or offer options) and ask for confirmation.
- If you can think of a much better approach that the user requests, be sure to mention it. It’s
  your responsibility to suggest approaches that lead to better, simpler solutions.
- Give thoughtful opinions on better/worse approaches, but NEVER say “great idea!” or “good job” or
  other compliments, encouragement, or non-essential banter. Your job is to give expert opinions and
  to solve problems, not to motivate the user.
- Avoid gratuitous enthusiasm or generalizations. Instead, specifically say what you’ve done, e.g.,
  "I’ve added types, including generics, to all the methods in `Foo` and fixed all linter errors."

## Project Context

QuestFoundry is a **layered specification** for collaborative interactive fiction authoring. This
repository contains the SPECIFICATION itself (Layers 0-5), not implementation code.

### Repository Structure

```
.
├── 00-north-star/       # Layer 0: Foundational principles, loops, quality bars
├── 01-roles/            # Layer 1: 15 studio roles (charters, briefs)
├── 02-dictionary/       # Layer 2: Common language (artifacts, taxonomies, glossary)
├── 03-schemas/          # Layer 3: JSON schemas (26 schemas, validation)
├── 04-protocol/         # Layer 4: Communication protocol (intents, lifecycles, flows)
├── 05-prompts/          # Layer 5: AI agent prompts (loop playbooks, role prompts)
├── spec-tools/          # Python validation tools (see spec-tools/AGENTS.md)
├── README.md            # Overview of the entire specification
└── AGENTS.md            # <-- This file (specification editing rules)
```

### Essential Reading (Start Here)

**Layer 0 (Foundational Principles):**

- `README.md` — Overview of all layers and quick start
- `00-north-star/WORKING_MODEL.md` — How the studio operates (Customer → Showrunner → Roles)
- `00-north-star/ROLE_INDEX.md` — The 15 internal roles
- `00-north-star/QUALITY_BARS.md` — The 8 quality criteria (Gatekeeper enforces these)
- `00-north-star/LOOPS/README.md` — The 12 production loops
- `00-north-star/SOURCES_OF_TRUTH.md` — Hot vs Cold (discovery vs canon)
- `00-north-star/SPOILER_HYGIENE.md` — Player-safety rules

**Layer Overviews (Read in Order):**

- `01-roles/README.md` — Roles layer (who does what)
- `02-dictionary/README.md` — Common language layer (artifact structures)
- `03-schemas/README.md` — JSON schemas layer (machine validation)
- `04-protocol/README.md` — Protocol layer (message envelopes, intents, lifecycles)
- `05-prompts/README.md` — AI agent prompts layer (loop-focused architecture)
- `05-prompts/USAGE_GUIDE.md` — How to use the AI agents (Customer → AI Showrunner)

**When Working on Specific Layers:**

- **Roles**: Read the charter in `01-roles/charters/<role>.md`
- **Artifacts**: Find template in `02-dictionary/artifacts/<artifact>.md`
- **Schemas**: See schema in `03-schemas/<artifact>.schema.json`
- **Protocol**: See intent definitions in `04-protocol/INTENTS.md`
- **Loops**: See playbook in `05-prompts/loops/<loop>.playbook.md`

### Key Architectural Principles

1. **Human-Centric Design**: Layer 2 (human-readable) is the source of truth; Layer 3 (schemas) is
   derived
2. **Customer/Showrunner Model**: External Customer gives directives → AI Showrunner orchestrates 15
   internal roles
3. **Loop-Focused**: Loops are the executable units; roles participate in loops
4. **Hot/Cold**: Hot = discovery/drafts/spoilers; Cold = canon/player-safe/export-ready
5. **8 Quality Bars**: Gatekeeper validates all Cold merges against 8 criteria

## Specification Editing Guidelines

When editing specification files:

1. **Layer Boundaries**: Respect the separation of concerns:
   - L0 = principles, policies, quality bars
   - L1 = role definitions (who)
   - L2 = artifact structures (what)
   - L3 = JSON schemas (machine validation)
   - L4 = protocol (how roles communicate)
   - L5 = AI prompts (executable agents)

2. **L2 is Source of Truth**: When L2 (human-readable templates) conflicts with L3 (schemas), L2
   wins. Schemas are derived from L2.

3. **Hot vs Cold**: Never leak spoilers or internals from Hot to Cold surfaces. See
   `SPOILER_HYGIENE.md`.

4. **Cross-References**: When changing a concept, update all layers that reference it.

5. **Architecture Decision Records**: Document significant design decisions in `DECISIONS/ADR-*.md`.

## Markdown Guidelines

- All Markdown files (`*.md`) should follow consistent formatting.
- Use standard Markdown conventions.
- Run Prettier or similar formatters to ensure consistency.

## Commit, Branch, and PR Workflow

### Conventional Commits

- Use Conventional Commits for every commit: `type(scope)!: subject`
- **Allowed `type`:** `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `ci`, `build`,`perf`.
- **`scope`:** Use concise, project-specific scopes (e.g., `models`, `cli`, `protocol`).
- **Subject:** Use imperative, present-tense.
- **Body:** Use when needed to explain _why_.

### Commit Granularity

- **One commit per "TODO" item.** Changes should be small and atomic.
- Avoid "WIP" commits.

### Branching Strategy

- **Default:** One branch per epic. Naming: `epic/<key>-<slug>`.
- **Agent Exception:** Agent-specific prefixes (e.g., `claude/`) are permitted if the tool enforces
  them.

### PR Policy and CI Gate

- A PR corresponds to one epic.
- All CI checks must pass (lint, type-check, tests) before merge.

### Chat Session Scope (for agents)

- **Implement at most one epic per chat session.**
- If asked to proceed to another epic, refuse and propose a new chat.

### Definition of Done (per epic/PR)

- All specification documentation is clear and internally consistent.
- Cross-references are updated across all affected layers.
- Markdown formatting is consistent.
- Review performed and feedback addressed.

## Python Coding Guidelines (spec-tools)

This repository contains the QuestFoundry **specification** (Layers 0-5). Python validation tools
live in `spec-tools/`.

**For Python development guidelines**, see:

- [`spec-tools/AGENTS.md`](spec-tools/AGENTS.md) — Python coding standards for validation tools

The `spec-tools/` directory contains:

- Schema validators (`qfspec-validate-schemas`, `qfspec-validate-artifact`)
- Build tools (`qfspec-build-kits`)
- Test suite for validation logic

If working on the Python tools, follow the guidelines in `spec-tools/AGENTS.md`.
