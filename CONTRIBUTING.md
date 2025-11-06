# Contributing to QuestFoundry

Thanks for jumping in. QuestFoundry is a **layered spec** for building nonlinear gamebooks with
clear roles, tight feedback loops, and player-safe surfaces. This guide explains how to propose
changes **today** while we’re focusing on **Layer 0 (North Star)** and **Layer 1 (Roles)**.

> Short version: open a small PR anchored by a **Trace Unit (TU)**; keep spoilers in Hot; the
> **Gatekeeper** enforces Quality Bars before anything hits **Cold**.

---

## 1) Ground rules

- **Code of Conduct**: Be kind, specific, and assume good intent. See
  [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md).
- **License**: Contributions are under MIT. See [`LICENSE`](./LICENSE).
- **Current scope**: We’re authoring **Layer 0 & 1**. Don’t add schemas, protocol messages, or code
  yet—leave stubs in Layers 3–7.

---

## 2) The layered repo (what goes where)

- **Layer 0 — North Star**: human docs (SoT, PN principles, loops, quality bars, accessibility,
  spoiler hygiene, traceability).
- **Layer 1 — Roles**: human-level role charters/briefs and RACIs.
- **Layer 2 — Dictionary**: human terms (non-technical).
- **Layers 3–7**: first-class directories, but **no new technical content** until 0/1 stabilize.

When in doubt: if it’s **how we think/work**, it’s Layer 0/1. If it’s **data or execution**, it
belongs to later layers (leave a stub or open an ADR to discuss).

---

## 3) Workflow in practice

### 3.1 Create a Trace Unit (TU)

Every meaningful PR should reference a **TU** (see `00-north-star/TRACEABILITY.md`):

```text
TU-ID: tu-<topic>-<date>
Title: <human headline>
Type: <topology | prose | style | canon | codex | policy | docs>
Rationale: <why this helps creators/players>
Upstream refs: <files/sections/loops this builds on>
Downstream impacts: <roles/surfaces likely affected>
Quality bars touched: <Integrity | Reachability | Nonlinearity | Gateways | Style | Determinism | Presentation>
Status: hot-proposed
Notes: <spoiler flags if any>
```

Place a brief TU note at the top of your PR description.

### 3.2 Keep Hot vs Cold straight

- **Hot**: draft changes, spoilers, internal reasoning, proposed loops.
- **Cold**: curated player-safe surfaces, ready for exports; _no spoilers_. Edits to player-facing
  text must pass **Gatekeeper** checks in `QUALITY_BARS.md`.

### 3.3 Use small, targeted loops

Prefer **micro-PRs** that align with a loop:

- Story Spark / Hook Harvest / Lore Deepening / Codex Expansion
- Style Tune-up / Art Touch-up / Audio Pass / Translation Pass
- Binding Run / Narration Dry-Run (usually coordination docs)

Each PR should say which loop it’s supporting.

---

## 4) Submitting a PR

1. **Fork & Branch**

   - Branch naming: `tu/<slug>` (e.g., `tu/story-spark-hubs-v1`).

2. **Make focused changes**

   - Update exactly the docs you claim. Avoid drive-by edits.
   - If you reference later layers, add TODO stubs—not implementations.

3. **Update indices**

   - If you add a new doc, link it from `00-north-star/README.md` and any relevant `LOOPS/README.md`
     or `PLAYBOOKS/README.md`.

4. **PR description template**

   - TU summary (copy the TU block)
   - “Loop alignment”: which loop and why
   - “Player-surface impact”: none / codex / PN / binder … (and spoiler stance)
   - “Quality bars touched”: list which and how you satisfied them
   - “Follow-ups”: next loop(s) or ADR needed

5. **Self-check (tick before opening)**
   - [ ] Player-safe surfaces contain **no spoilers** or internal labels
   - [ ] Links resolve; anchors match filenames and headings
   - [ ] Style matches register (see Style Lead guardrails)
   - [ ] Accessibility basics: headings meaningful; alt-text where applicable
   - [ ] Traceability: TU referenced in touched files (Lineage line when relevant)
   - [ ] Scope is minimal and testable by a reviewer in <10 minutes

---

## 5) Commit message conventions

We use **Conventional Commits** to make the git history readable and to enable automated tooling.

### Format

```text
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

- **feat**: New feature or content addition
- **fix**: Bug fix or correction
- **docs**: Documentation-only changes
- **chore**: Maintenance tasks (formatting, typos, cleanup)
- **schema**: Schema changes (Layer 3)
- **protocol**: Protocol specification changes (Layer 4)
- **milestone**: Major completion milestones
- **refactor**: Code/content restructuring without behavior change
- **test**: Adding or updating tests
- **style**: Formatting changes (whitespace, prettier)

### Scopes

Use layer names or artifact types:

- **Layers**: `layer0`, `layer1`, `layer2`, `layer3`, `layer4`, `layer5`
- **Artifacts**: `hook-card`, `tu-brief`, `canon-pack`, `gatecheck-report`
- **Cross-cutting**: `architecture`, `all-layers`, `repo`

### Examples

```text
feat(layer2): add choice integrity conventions

Added conventions/choice_integrity.md documenting the diegetic choice
pattern and intent-forward labeling requirements.
```

```text
fix(schema): correct hook_card status enum values

Updated status field to include all 7 lifecycle states from taxonomies.md.
Missing "canonized" and "deferred" values caused validation failures.
```

```text
docs(layer0): update quality bars to 8 total

Split Presentation bar into Presentation and Accessibility as separate
mandatory checks. Updated all layer documentation and cross-references.
```

```text
milestone: complete Layer 2 to 100%

All 20 artifact templates enriched with constraints, taxonomies complete,
cross-references updated.
```

```text
chore(repo): archive completed audit documents

Moved LAYER2_AUDIT_PHASE4.md and protocol issue drafts to ARCHIVE/
directory to keep working tree clean.
```

### Breaking changes

If a commit introduces breaking changes, add `BREAKING CHANGE:` in the footer:

```text
feat(schema): redesign hook lifecycle states

BREAKING CHANGE: Hook status values changed from 5 to 7 states.
Projects using old status values must migrate.
```

### Multi-scope commits

For changes spanning multiple scopes, choose the primary scope or use `all-layers`:

```text
docs(all-layers): update status to reflect completion milestones
```

### Guidelines

- **Keep commits atomic**: One logical change per commit
- **Use imperative mood**: "add feature" not "added feature" or "adds feature"
- **Capitalize description**: Start with capital letter, no period at end
- **Body is optional**: Use for complex changes requiring explanation
- **Reference issues**: Add `Closes #123` or `Refs #456` in footer when applicable

---

## 6) Reviews & roles

- **Maintainers** act as **Showrunner** (triage/scope) and **Gatekeeper** (quality bars).
- **Subject reviews**:
  - **Style** changes → ping Style Lead
  - **Codex** pages → ping Codex Curator + Lore Weaver
  - **PN** principles or surfaces → ping PN reviewer
  - **Accessibility/Spoiler hygiene** → ping Gatekeeper

Expect friendly pushback on scope and spoiler hygiene. We value **clarity and testability** over
cleverness.

---

## 7) ADRs vs TUs

- Use a **TU** for changes _within_ the current rules (docs, loops, guardrails).
- Use an **ADR** (`/DECISIONS/ADR-YYYYMMDD-<slug>.md`) for **changing the rules** (e.g.,
  adding/removing a role, redefining Hot/Cold boundaries, altering loop taxonomy).

PRs that mix ADR and routine edits will be asked to split.

---

## 8) Style & formatting

- Markdown, sentence-case headings, 80–100 char soft wrap preferred.
- Use short sections with clear leads; favor examples over abstractions.
- Keep player-facing phrasing **diegetic** (no “codeword ASH”, no schema talk).
- No purple prose; no lorem ipsum.

---

## 9) Common pitfalls (avoid)

- Sneaking spoilers into codex/captions/PN examples.
- Bundling unrelated edits into one PR.
- Editing later layers (schemas/protocol/prompts) while Layer 0/1 are unsettled.
- Writing taxonomy pages that quietly invent **canon** (route that to Lore Deepening).

---

## 10) After merge

- Maintainers will tag a **Cold snapshot** periodically and note which **TU-IDs** landed since the
  previous snapshot in `00-north-star/TRACELOG.md`.
- The **Book Binder** may cut a new export view; the PN may schedule a **Narration Dry-Run**.

---

## 11) Questions?

Open a Discussion or a draft PR with the TU header and “Questions” section. Small, concrete examples
beat long hypotheticals.

**Welcome aboard.** Keep changes small, keep surfaces safe, and let the book get better in
deliberate steps.
