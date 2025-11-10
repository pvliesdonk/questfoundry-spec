# Canon Transfer (Export) — Package Canon for Shared Universes

**Purpose** Export stabilized canon from a completed project as a **Canon Transfer Package**,
enabling shared story universes, sequels, and franchise continuity. Invariant canon rules are
preserved; mutable canon allows extension.

**Outcome** A validated **Canon Transfer Package** artifact ready for import into a new project,
containing tagged canon (invariant/mutable), codex baseline, timeline anchors, and entity registry.

**See also:** `../WORKING_MODEL.md` §12 for workflow pattern comparison.

---

## 1) Triggers (Showrunner)

- After final **Binding Run** and before project archival.
- User explicitly requests canon export for sequel/shared universe.
- Preparing franchise foundation for multiple projects.

**Activation** Showrunner opens a **Trace Unit (TU)** for the export and confirms which canon
elements should be:

- **Invariant** (must remain true in downstream projects)
- **Mutable** (can be extended in downstream projects)
- **Local** (project-specific; exclude from transfer)

---

## 2) Inputs

- Current **Cold** snapshot (final canon packs, codex entries, style guardrails).
- Project metadata (title, slug, snapshot ID).
- Lore Weaver's understanding of which canon is foundational vs. story-specific.
- Codex Curator's player-safe codex baseline.

---

## 3) Roles & Responsibilities

- **Lore Weaver (R)**
  - Identify all canon packs from Cold.
  - Tag each canon pack element as **invariant**, **mutable**, or **local**.
  - Extract timeline anchors (T0/T1/T2) for downstream projects.
  - Create entity registry (characters, places, factions defined in this project).
- **Codex Curator (C)**
  - Identify player-safe codex entries suitable for universe-wide transfer.
  - Mark entries as **inherited** (from this project) for downstream reference.
  - Ensure codex baseline is spoiler-free.
- **Gatekeeper (C)**
  - Validate export package for:
    - **Integrity** — All entity references in invariant canon resolve.
    - **Presentation** — No source project spoilers leak into invariant canon.
    - **Consistency** — Timeline anchors are chronologically ordered.
- **Showrunner (A)**
  - Approves export scope (which canon elements to include).
  - Confirms invariant vs. mutable tagging.
  - Triggers final export after gatecheck.

---

## 4) Procedure

1. **Canon Inventory (Lore Weaver)**
   - List all canon packs from Cold.
   - For each canon pack, identify elements by scope:
     - **Invariant** — Must remain true (e.g., "Wormhole 3 collapsed in Y-18").
     - **Mutable** — Can evolve (e.g., "Toll Syndicate has 5 known members").
     - **Local** — Story-specific (e.g., "Kestrel's personal arc resolution").
   - Create summary table:

     | Canon Pack ID | Theme       | Invariant Elements | Mutable Elements | Local Elements |
     | ------------- | ----------- | ------------------ | ---------------- | -------------- |
     | CP-001        | Geography   | 5                  | 2                | 0              |
     | CP-002        | Factions    | 3                  | 4                | 2              |
     | CP-003        | Metaphysics | 8                  | 1                | 0              |

2. **Tag Canon Elements**
   - For each canon pack:
     - Mark invariant elements with `immutable: true`.
     - Mark mutable elements with `immutable: false`.
     - Exclude local elements from export.
   - Rationale: Downstream projects must honor invariants; can extend mutables.

3. **Extract Timeline Anchors**
   - From canon packs, extract timeline (T0/T1/T2):
     - T0 = past anchor (e.g., "Y-18: Wormhole 3 collapse")
     - T1 = recent (e.g., "Y-5: Union reforms")
     - T2 = story "now" (e.g., "Y+0: Current state")
   - Downstream projects will extend as T3/T4/...

4. **Build Entity Registry**
   - List all entities defined in canon:
     - Characters: Name, role, status (alive/dead/unknown)
     - Places: Name, type (hub/gate/landmark), geography
     - Factions: Name, structure, influence
     - Items/Tech: Name, function, availability
   - Ensure all entity references in invariant canon resolve to registry.

5. **Codex Baseline (Codex Curator)**
   - Identify codex entries for universe-wide transfer:
     - Player-safe entries that apply to downstream stories.
     - Mark as `inherited: true` with `source: <project-slug>`.
   - Exclude story-specific codex entries (e.g., "Kestrel's final decision").
   - Ensure codex baseline is spoiler-free.

6. **Package Assembly (Lore Weaver)**
   - Create **Canon Transfer Package** artifact:
     - **Metadata**
       - `source_project`: Project slug
       - `export_date`: YYYY-MM-DD
       - `snapshot_id`: Cold snapshot tag
     - **Invariant Canon** (array of canon pack elements with `immutable: true`)
     - **Mutable Canon** (array of canon pack elements with `immutable: false`)
     - **Codex Baseline** (array of codex entries with `inherited: true`)
     - **Timeline Anchors** (T0/T1/T2 from this project)
     - **Entity Registry** (characters, places, factions, items)

7. **Validation (Gatekeeper)**
   - **Integrity** — All entity references in invariant canon resolve to entity registry.
   - **Presentation** — No project-specific spoilers in invariant canon or codex baseline.
   - **Consistency** — Timeline anchors are ordered; no conflicts.
   - **Schema compliance** — Package validates against `canon_transfer_package.schema.json`.

8. **Export Finalization (Showrunner)**
   - Review Gatekeeper report.
   - Approve export scope.
   - Save package: `canon_transfer_package_<project-slug>.json`.
   - Record export in TU: `TU-<date>-LW-CanonTransferExport`.

---

## 5) Deliverables (Cold)

- **Canon Transfer Package** (`canon_transfer_package_<project-slug>.json`)
  - Metadata (source project, export date, snapshot ID)
  - Invariant canon (immutable rules)
  - Mutable canon (extensible rules)
  - Codex baseline (inherited entries)
  - Timeline anchors (T0/T1/T2)
  - Entity registry (characters, places, factions, items)
- **TU** documenting the export (`TU-<date>-LW-CanonTransferExport`)
- **Gatekeeper report** (validation summary)

---

## 6) Merge Path (summary)

Canon Transfer (Export) operates on **Cold** canon only (no Hot changes). Export package is a
read-only artifact derived from finalized project canon.

---

## 7) Success Criteria

- All invariant canon elements are tagged and included in package.
- All mutable canon elements are tagged and included in package.
- Local canon is excluded from package.
- Entity registry is complete; all references resolve.
- Codex baseline is player-safe and spoiler-free.
- Timeline anchors are chronologically ordered.
- Package validates against schema.
- Gatekeeper approves (Integrity + Presentation + Consistency).

---

## 8) Failure Modes & Remedies

- **Invariant tagging unclear** → Lore Weaver consults Showrunner; defer ambiguous elements to
  mutable.
- **Entity reference broken** → Add missing entity to registry or remove reference from invariant
  canon.
- **Codex baseline contains spoilers** → Codex Curator revises to player-safe summary or excludes
  entry.
- **Timeline conflicts** → Lore Weaver reorders anchors or removes conflicting anchor.
- **Schema validation fails** → Fix package structure; re-validate.

---

## 9) RACI (quick)

| Task                  | R           | A          | C          | I    |
| --------------------- | ----------- | ---------- | ---------- | ---- |
| Canon inventory       | Lore Weaver | Showrunner | Curator    | —    |
| Tag canon elements    | Lore Weaver | Showrunner | —          | Plotwright |
| Extract timeline      | Lore Weaver | —          | —          | —    |
| Build entity registry | Lore Weaver | —          | —          | —    |
| Codex baseline        | Curator     | Lore       | Gatekeeper | —    |
| Package assembly      | Lore Weaver | Showrunner | —          | —    |
| Validation            | Gatekeeper  | Showrunner | Lore       | All  |
| Export finalization   | Showrunner  | Showrunner | Gatekeeper | All  |

---

## 10) Hand-offs

- **To downstream project**: Canon Transfer Package (`canon_transfer_package_<project-slug>.json`)
- **To archival**: TU and Gatekeeper report for project records

---

## 11) Example (miniature)

**Project:** "The Lighthouse Keeper" (slug: `lighthouse-keeper`)

**Canon Inventory:**

| Canon Pack         | Invariant                          | Mutable                    | Local                  |
| ------------------ | ---------------------------------- | -------------------------- | ---------------------- |
| CP-001 (Geography) | Wormhole 3 collapsed (Y-18)        | Dock 7 layout (can expand) | —                      |
| CP-002 (Factions)  | Toll Syndicate structure (5 tiers) | Member roster (can add)    | Kestrel's betrayal arc |
| CP-003 (Physics)   | Wormhole mechanics (8 constraints) | Plasma backflow rules      | —                      |

**Timeline Anchors:**

- T0: Y-18 — Wormhole 3 collapse
- T1: Y-5 — Union reforms after accident
- T2: Y+0 — Current story state

**Entity Registry:**

- Characters: Kestrel Var (alive, status: reformed), Ena Roe (alive, status: promoted)
- Places: Dock 7 (hub), Wormhole 3 (gate-defunct), Union Hall (landmark)
- Factions: Toll Syndicate (active), Dock Workers Union (active)
- Items: Union Token (visual badge), Plasma Scanner (inspection tool)

**Codex Baseline:**

- Entry: "Dock Inspections" (inherited, player-safe)
- Entry: "Union Tokens" (inherited, player-safe)
- Entry: "Wormhole Physics" (inherited, player-safe)
- Excluded: "Kestrel's Final Choice" (spoiler, story-specific)

**Package:** `canon_transfer_package_lighthouse-keeper.json`

**Validation:**

- ✅ Integrity: All entity references resolve
- ✅ Presentation: No spoilers in invariant canon
- ✅ Consistency: Timeline ordered correctly
- ✅ Schema: Validates against `canon_transfer_package.schema.json`

**Gatekeeper Approval:** PASS

**Export Complete:** `TU-2025-11-10-LW-CanonTransferExport`

---

**TL;DR** Tag project canon as invariant/mutable/local, extract timeline and entities, bundle with
player-safe codex baseline, validate for integrity and presentation, export as reusable package for
downstream sequels or shared universes.
