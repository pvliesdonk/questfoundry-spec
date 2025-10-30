# Architecture Decision Record (ADR) — Layer Boundary Clarification

```
ADR-20251029-01-layer-boundary-clarification
```

---

## Status

```
Accepted
```

---

## Context

> What forced this decision? Tie to **Quality Bars** and the triggering work.

- Trigger: Post-PR #1 architectural review — comprehensive Layer 0 and Layer 1 content analysis
- Bars pressed: **Integrity** (structural consistency), **Presentation** (clarity of layer boundaries)
- Symptoms (player-safe):
  - Data structure definitions split across Layer 0 (TERMINOLOGY.md) and Layer 1 (templates/)
  - Unclear separation between policy (Layer 0), roles (Layer 1), and data structures (Layer 2)
  - Layer 2 empty despite being the natural home for "common language" and artifact definitions
- Prior attempts: None; first architectural review after Layer 0 and Layer 1 completion

---

## Decision

> The policy, stated crisply. Prefer MUST/SHOULD/MAY language.

- **We DECIDE:** Clarify and enforce strict layer boundaries as follows:

  - **Layer 0 (North Star)**: Policy, principles, vision, operating model — the WHY
  - **Layer 1 (Roles)**: Role definitions, responsibilities, interactions — the WHO
  - **Layer 2 (Common Language)**: Data dictionary, terminology, artifact structures — the WHAT
  - **Layer 3 (Codification)**: JSON schemas — HOW TO VALIDATE
  - **Layer 4 (Protocol)**: Interaction rules, messages — HOW TO COMMUNICATE

- **Immediate migrations:**

  - Move `00-north-star/TERMINOLOGY.md` → `02-dictionary/glossary.md`
  - Move `01-roles/templates/*.md` (17 files) → `02-dictionary/artifacts/`

- Scope: This repository (QuestFoundry)
- Owner(s): Showrunner (architectural coherence), Gatekeeper (structural integrity)

---

## Rationale

> Why this option beats the alternatives—short and specific.

1. **Separation of concerns**: Data structure definitions (WHAT things ARE) are fundamentally different from policy (WHY we do things) and role responsibilities (WHO does what). Mixing them creates confusion and makes each layer harder to reason about independently.

2. **Layer 2 exists for this purpose**: The seven-layer model explicitly designates Layer 2 as "Common Language" for human-readable data definitions. Having Layer 2 empty while data definitions live elsewhere violates the architectural intent.

3. **Scalability**: As the system grows, clear boundaries prevent:

   - Cross-layer duplication (same structure defined in multiple places)
   - Inconsistent definitions (template in Layer 1 differs from schema in Layer 3)
   - Unclear normative source ("which definition is authoritative?")

4. **Schema generation path**: Layer 2 human-readable definitions naturally inform Layer 3 JSON schemas. With structures scattered across Layer 0 and Layer 1, there's no clear source for schema generation.

5. **Role charters should reference, not duplicate**: Layer 1 charters/briefs should say "Lore Weaver produces canon_pack" and point to Layer 2 for structure, not embed the structure definition itself.

---

## Consequences

> What gets easier/harder. Include migration or adoption notes.

**Positive**

- Clear single source of truth for each artifact structure (Layer 2)
- Layer 0 becomes purer policy/principles (easier to understand system philosophy)
- Layer 1 becomes cleaner role definitions (who does what, not structure details)
- Obvious path to Layer 3 schema generation (one-to-one from Layer 2 artifacts)
- Better maintainability (change artifact structure in one place)

**Negative**

- Cross-references must be updated throughout Layer 0 and Layer 1 (mitigation: systematic grep and update)
- Temporarily creates "parked" content in Layer 2 pending proper draft (mitigation: clear marking with status badges)

**Migration**

- Effective date/snapshot: 2025-10-29
- Who updates what:
  - Showrunner: Create Layer 2 structure, move files, create READMEs with PARKED status
  - Gatekeeper: Verify cross-references updated, structural integrity maintained
- Cutover plan:
  1. ✅ Create `02-dictionary/` structure with README
  2. ✅ Move TERMINOLOGY.md → glossary.md (with PARKED status header)
  3. ✅ Move all 17 templates → artifacts/ (create artifacts/README.md)
  4. 🚧 Update cross-references in Layer 0 and Layer 1 files
  5. 🚧 Verify all links resolve correctly
  6. 🚧 Commit with descriptive message referencing this ADR

---

## Policy & Examples (player-safe)

> Tiny, reusable examples that **don't** reveal canon or internals.

- **Rule:** Data structure definitions (what fields an artifact has) live in Layer 2

  - _Example:_ "hook_card.md defines: ID, Status, Type, Summary, Hot Details, Exit Criteria"
  - _Counterexample:_ Don't embed the full hook structure in `00-north-star/HOOKS.md` (policy) or `01-roles/charters/plotwright.md` (role definition)

- **Rule:** Policy about WHY we use an artifact stays in Layer 0

  - _Example:_ "HOOKS.md explains prioritization heuristics, lifecycle philosophy"
  - _Counterexample:_ Don't move Hook Harvest loop guidance to Layer 2

- **Rule:** Role charters say WHO creates WHAT, Layer 2 says what WHAT contains
  - _Example:_ Layer 1: "Lore Weaver produces canon_pack (see 02-dictionary/artifacts/canon_pack.md)"
  - _Counterexample:_ Don't duplicate canon_pack structure in lore_weaver charter

---

## Interactions & Ownership

- Affected roles: All (everyone references artifacts and terminology)
- Handshakes to update: `01-roles/interfaces/*.md` (update paths to artifacts)
- Templates to update: All role charters/briefs that reference `../templates/` → update to `../../02-dictionary/artifacts/`
- Binder/Translator anchor policy: No change (they still reference artifact structures, just from Layer 2 now)

---

## Alternatives Considered

- **Option A: Keep everything as-is** — rejected because:

  - Violates stated layer model (Layer 2 for common language)
  - Creates confusion about where to look for artifact structures
  - Makes schema generation path unclear

- **Option B: Move templates to Layer 0** — rejected because:

  - Layer 0 is for policy, not data structures
  - Would make Layer 0 even more bloated
  - Still leaves Layer 2 empty despite being designed for this

- **Option C: Keep templates in Layer 1, move only TERMINOLOGY** — rejected because:

  - Doesn't solve the fundamental issue (data structures misplaced)
  - Templates are about WHAT artifacts are, not WHO creates them
  - Partial solution creates inconsistency

- **Do nothing:** Risk of continued confusion, duplication, and unclear boundaries between layers leading to maintenance burden and inconsistencies

---

## Verification

> How we'll know the ADR is working.

- Gatekeeper checks:

  - **Integrity Bar**: All cross-references resolve correctly
  - **Presentation Bar**: Clear status markings on parked content
  - Quick test: Can trace from role charter → artifact reference → Layer 2 definition → (future) Layer 3 schema

- PN dry-run signals: N/A (internal architectural change, no player-facing impact)

- Binding:
  - Artifact structures clearly sourced from Layer 2
  - No duplicate or conflicting definitions across layers
  - Clean path from human template (Layer 2) to schema (Layer 3, future)

---

## References & Lineage

- TUs: Post-PR #1 architectural review (2025-10-29)
- Gatecheck reports: N/A (preventive architecture work)
- View Logs: N/A (internal structure)
- Canon Packs / Style Addenda / Language Packs touched: None (structural only)
- Related ADRs: None (first ADR for QuestFoundry)

---

## Changelog

```
2025-10-29 — Proposed by Claude Code (architectural analysis post-PR #1)
2025-10-29 — Accepted by Showrunner (implementation in progress)
```

---

## Implementation Checklist

- [x] Create `02-dictionary/` structure
- [x] Create `02-dictionary/README.md` with PARKED status and Layer 2 overview
- [x] Move `00-north-star/TERMINOLOGY.md` → `02-dictionary/glossary.md` (mark as PARKED)
- [x] Move `01-roles/templates/*.md` → `02-dictionary/artifacts/`
- [x] Create `02-dictionary/artifacts/README.md` with artifact index
- [x] Remove empty `01-roles/templates/` directory
- [x] Update cross-references in Layer 0 files
- [x] Update cross-references in Layer 1 files (charters, briefs, interfaces)
- [x] Verify all links resolve
- [x] Commit with message referencing this ADR
- [x] Push to branch
