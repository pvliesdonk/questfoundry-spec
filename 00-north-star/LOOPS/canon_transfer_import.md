# Canon Transfer (Import) — Seed New Project with Shared Canon

**Purpose**
Import a **Canon Transfer Package** from a prior project to seed a new project with established canon, enabling sequels, shared universes, and franchise continuity. Invariant canon merges to Cold immediately; mutable canon seeds Hot for extension.

**Outcome**
New project's Hot/Cold is initialized with imported canon, timeline anchors, and codex baseline. Plotwright and Scene Smith receive clear constraint documentation. Gatekeeper ensures no conflicts between imported canon and project seed ideas.

**See also:** `../WORKING_MODEL.md` §12 for workflow pattern comparison.

---

## 1) Triggers (Showrunner)

- During new project initialization, before first **Story Spark**.
- User provides `canon_transfer_package_<source-project>.json` for import.
- Building a sequel or shared universe story.

**Activation**
Showrunner opens a **Trace Unit (TU)** for the import: `TU-<date>-LW-CanonTransferImport` and confirms import scope.

---

## 2) Inputs

- **Canon Transfer Package** (`canon_transfer_package_<source-project>.json`)
  - Invariant canon (immutable rules)
  - Mutable canon (extensible rules)
  - Codex baseline (inherited entries)
  - Timeline anchors (T0/T1/T2 from source project)
  - Entity registry (characters, places, factions, items)
- New project seed ideas (user's initial concept for this project).
- Project metadata (title, slug).

---

## 3) Roles & Responsibilities

- **Lore Weaver (R)**
  - Load transfer package.
  - Parse invariant/mutable canon.
  - Merge invariant canon to **Cold** (immutable).
  - Seed mutable canon to **Hot** (extensible).
  - Import timeline anchors; extend as T3/T4/... for new project.
  - Create entity registry baseline for new project.
- **Codex Curator (C)**
  - Import inherited codex entries.
  - Mark entries with `source: <source-project>`.
  - Identify gaps where new project needs additional entries.
- **Gatekeeper (C)**
  - Validate import for:
    - **Integrity** — Imported canon is internally consistent.
    - **Conflict detection** — No contradiction between imported invariants and new project seed.
    - **Presentation** — Codex baseline remains player-safe.
- **Plotwright (C)**
  - Review imported canon constraints.
  - Confirm new story can work within invariant canon rules.
  - If conflict detected, escalate to Showrunner.
- **Showrunner (A)**
  - Approves import scope.
  - Resolves conflicts (reject import, revise project seed, or downgrade invariant to mutable).
  - Confirms downstream roles understand constraints.

---

## 4) Procedure

1. **Load Transfer Package (Lore Weaver)**
   - Open `canon_transfer_package_<source-project>.json`.
   - Parse package structure:
     - Metadata (source project, export date, snapshot ID)
     - Invariant canon (immutable rules)
     - Mutable canon (extensible rules)
     - Codex baseline (inherited entries)
     - Timeline anchors (T0/T1/T2)
     - Entity registry (characters, places, factions, items)
   - Validate package against schema (`canon_transfer_package.schema.json`).

2. **Conflict Detection (Lore Weaver + Gatekeeper)**
   - Compare imported invariant canon against new project seed ideas.
   - Identify conflicts:
     - Example conflict: Invariant says "Wormhole 3 collapsed in Y-18"; project seed wants to repair it.
   - If conflict detected:
     - **Option A**: Reject import (wrong canon baseline for this story).
     - **Option B**: Revise project seed (honor invariant; story cannot repair Wormhole 3).
     - **Option C**: Downgrade invariant to mutable (allow repair; coordinate with source project owner).
   - Escalate to Showrunner for resolution.

3. **Merge Invariant Canon to Cold**
   - Invariant canon elements are **immutable** in new project.
   - Create canon packs in Cold:
     - Title: "<Source Project> — <Theme> (Invariant Canon)"
     - Mark as `source: <source-project>`, `immutable: true`.
     - Status: `cold-merged` (cannot be changed).
   - Example:
     - "The Lighthouse Keeper — Geography (Invariant Canon)"
     - Canon: "Wormhole 3 collapsed in Y-18; irreparable with current technology."

4. **Seed Mutable Canon to Hot**
   - Mutable canon elements are **extensible** in new project.
   - Create canon packs in Hot:
     - Title: "<Source Project> — <Theme> (Mutable Canon)"
     - Mark as `source: <source-project>`, `immutable: false`.
     - Status: `hot-accepted` (can be extended via Lore Deepening).
   - Example:
     - "The Lighthouse Keeper — Factions (Mutable Canon)"
     - Canon: "Toll Syndicate has 5 known tiers; member roster incomplete."

5. **Import Timeline Anchors**
   - Source project timeline becomes baseline:
     - T0 = past anchor from source (e.g., "Y-18: Wormhole 3 collapse")
     - T1 = recent from source (e.g., "Y-5: Union reforms")
     - T2 = "now" from source (e.g., "Y+0: Source project end state")
   - New project extends timeline:
     - T3 = new project "now" (e.g., "Y+2: Two years after source project")
     - T4+ = new project future events
   - Document timeline offsets for creative roles.

6. **Import Entity Registry**
   - Copy entity registry from transfer package:
     - Characters: Preserve status (alive/dead/unknown).
     - Places: Preserve geography and type.
     - Factions: Preserve structure and influence.
     - Items/Tech: Preserve function and availability.
   - Mark entities as `source: <source-project>`.
   - Allow new project to add entities; cannot remove or contradict source entities.

7. **Codex Import (Codex Curator)**
   - Import inherited codex entries:
     - Mark as `inherited: true`, `source: <source-project>`.
     - Status: `cold-merged` (player-safe baseline).
   - Identify gaps:
     - New project may need entries for new characters/places/concepts.
     - Flag for **Codex Expansion** loop after Story Spark.
   - Ensure codex baseline remains spoiler-free.

8. **Create Constraint Documentation (Lore Weaver)**
   - Document for Plotwright and Scene Smith:
     - **Invariants** (cannot change):
       - "Wormhole 3 collapsed in Y-18 (irreparable)."
       - "Toll Syndicate has 5-tier hierarchy (structure fixed)."
     - **Mutables** (can extend):
       - "Toll Syndicate member roster incomplete (can add members)."
       - "Dock 7 layout partially documented (can expand)."
     - **Timeline** (extend from T3+):
       - "Source project ends at Y+0; new project starts at Y+2."
     - **Entities** (baseline registry):
       - "Kestrel Var (alive, reformed); Ena Roe (alive, promoted)."
   - Include examples:
     - "You CAN: Add new Toll Syndicate members, expand Dock 7, introduce new characters."
     - "You CANNOT: Repair Wormhole 3, change Toll hierarchy, contradict source character fates."

9. **Gatekeeper Validation**
   - **Integrity** — All entity references in imported canon resolve.
   - **Conflict resolution** — No unresolved contradictions with project seed.
   - **Presentation** — Codex baseline is player-safe.
   - **Schema compliance** — Imported canon conforms to QuestFoundry schemas.

10. **Showrunner Approval**
    - Review Gatekeeper report.
    - Confirm import scope and constraint documentation.
    - Approve merge: invariants to Cold, mutables to Hot.
    - Update TU: `TU-<date>-LW-CanonTransferImport`.

11. **Announce to Creative Roles**
    - Notify Plotwright, Scene Smith, Style Lead:
      - "Canon baseline imported from <source-project>."
      - "See constraint docs for invariants and mutables."
      - "Timeline extends from Y+2."
      - "Entity registry baseline available."
    - Ready for **Story Spark** (new plot within imported canon constraints).

---

## 5) Deliverables (Hot/Cold)

- **Cold Canon Packs** (invariant canon, immutable)
  - Title: "<Source Project> — <Theme> (Invariant Canon)"
  - Status: `cold-merged`
- **Hot Canon Packs** (mutable canon, extensible)
  - Title: "<Source Project> — <Theme> (Mutable Canon)"
  - Status: `hot-accepted`
- **Codex Entries** (inherited baseline, player-safe)
  - Status: `cold-merged`
- **Entity Registry** (baseline for new project)
- **Timeline Foundation** (T0/T1/T2 from source; T3+ for new project)
- **Constraint Documentation** (for Plotwright/Scene Smith)
- **TU** (`TU-<date>-LW-CanonTransferImport`)
- **Gatekeeper Report** (validation summary)

---

## 6) Merge Path (summary)

- **Invariant canon** → merges to **Cold** immediately (immutable).
- **Mutable canon** → seeds **Hot** (can be extended via Lore Deepening).
- **Codex baseline** → merges to **Cold** (player-safe surface).

---

## 7) Success Criteria

- Transfer package loads and validates successfully.
- No unresolved conflicts between imported canon and project seed.
- Invariant canon merged to Cold (immutable).
- Mutable canon seeded to Hot (extensible).
- Codex baseline imported (player-safe).
- Timeline anchors imported; new project timeline extends from T3+.
- Entity registry imported and available.
- Constraint documentation clear and actionable.
- Gatekeeper approves (Integrity + Conflict resolution + Presentation).
- Creative roles understand invariants vs. mutables.

---

## 8) Failure Modes & Remedies

- **Schema validation fails** → Fix package format; re-import.
- **Conflict with project seed** → Escalate to Showrunner; choose Option A/B/C (reject, revise, downgrade).
- **Entity reference broken** → Add missing entity to registry or flag for Lore Deepening.
- **Timeline confusion** → Document timeline offsets clearly; provide examples.
- **Codex spoilers** → Codex Curator revises to player-safe or excludes entry.
- **Creative role confusion** → Lore Weaver clarifies constraint docs; provide use-case examples.

---

## 9) RACI (quick)

| Task                      | R           | A          | C          | I          |
| ------------------------- | ----------- | ---------- | ---------- | ---------- |
| Load transfer package     | Lore Weaver | Showrunner | —          | —          |
| Conflict detection        | Lore Weaver | Showrunner | Gatekeeper | Plot       |
| Merge invariant to Cold   | Lore Weaver | Showrunner | Gatekeeper | All        |
| Seed mutable to Hot       | Lore Weaver | Showrunner | —          | All        |
| Import timeline           | Lore Weaver | —          | —          | Plot/SS    |
| Import entity registry    | Lore Weaver | —          | —          | Plot/SS    |
| Codex import              | Curator     | Lore       | Gatekeeper | —          |
| Constraint documentation  | Lore Weaver | Showrunner | Plot/SS    | All        |
| Gatekeeper validation     | Gatekeeper  | Showrunner | Lore       | All        |
| Showrunner approval       | Showrunner  | Showrunner | Gatekeeper | All        |

---

## 10) Hand-offs

- **To Story Spark**: Constraint documentation (invariants/mutables), timeline foundation, entity registry.
- **To Lore Deepening**: Mutable canon (can extend via hooks).
- **To Codex Expansion**: Gap list (where new entries needed).

---

## 11) Example (miniature)

**Source Project:** "The Lighthouse Keeper" (slug: `lighthouse-keeper`)
**New Project:** "The Harbor Master" (slug: `harbor-master`)

**Import Package:** `canon_transfer_package_lighthouse-keeper.json`

**1. Load Package:**
- Metadata: source = "lighthouse-keeper", export_date = "2025-11-10", snapshot_id = "v1.0"
- Invariant canon: Geography (Wormhole 3 collapsed), Factions (Toll structure)
- Mutable canon: Dock 7 layout, Toll member roster
- Codex baseline: 3 entries (Dock Inspections, Union Tokens, Wormhole Physics)
- Timeline: T0 = Y-18, T1 = Y-5, T2 = Y+0
- Entity registry: Kestrel (alive), Ena (alive), Dock 7 (hub), Toll Syndicate (faction)

**2. Conflict Detection:**
- New project seed: "Harbor master investigates wormhole repair efforts."
- Conflict: Invariant says "Wormhole 3 irreparable"; seed wants repair.
- **Resolution (Option B)**: Revise project seed: "Harbor master investigates FAILED wormhole repair attempts (honors invariant)."

**3. Merge Invariant to Cold:**
- Canon Pack: "The Lighthouse Keeper — Geography (Invariant Canon)"
  - Canon: "Wormhole 3 collapsed in Y-18; irreparable with current technology."
  - Status: `cold-merged`, `immutable: true`

**4. Seed Mutable to Hot:**
- Canon Pack: "The Lighthouse Keeper — Factions (Mutable Canon)"
  - Canon: "Toll Syndicate has 5 tiers; member roster incomplete."
  - Status: `hot-accepted`, `immutable: false`

**5. Import Timeline:**
- T0 = Y-18 (Wormhole 3 collapse)
- T1 = Y-5 (Union reforms)
- T2 = Y+0 (Lighthouse Keeper ends)
- **T3 = Y+2** (Harbor Master begins, 2 years later)

**6. Import Entity Registry:**
- Kestrel Var (alive, reformed, source: lighthouse-keeper)
- Ena Roe (alive, promoted, source: lighthouse-keeper)
- Dock 7 (hub, source: lighthouse-keeper)
- Toll Syndicate (faction, 5 tiers, source: lighthouse-keeper)

**7. Codex Import:**
- Entry: "Dock Inspections" (inherited, source: lighthouse-keeper)
- Entry: "Union Tokens" (inherited, source: lighthouse-keeper)
- Entry: "Wormhole Physics" (inherited, source: lighthouse-keeper)
- **Gap**: Need new entry for "Harbor Master role" (flag for Codex Expansion).

**8. Constraint Documentation:**
**Invariants (cannot change):**
- Wormhole 3 collapsed in Y-18 (irreparable)
- Toll Syndicate has 5-tier hierarchy

**Mutables (can extend):**
- Toll member roster (can add new members)
- Dock 7 layout (can expand)

**Timeline (extend from T3+):**
- Source project ends at Y+0
- New project starts at Y+2

**Entities (baseline):**
- Kestrel Var (alive, reformed)
- Ena Roe (alive, promoted)

**You CAN:**
- Add new Toll members
- Expand Dock 7 geography
- Introduce new characters
- Explore failed repair attempts (honoring irreparability)

**You CANNOT:**
- Repair Wormhole 3 (violates invariant)
- Change Toll hierarchy structure (violates invariant)
- Contradict Kestrel/Ena fates (violates entity registry)

**9. Gatekeeper Validation:**
- ✅ Integrity: All entity references resolve
- ✅ Conflict resolution: Seed revised to honor invariant
- ✅ Presentation: Codex baseline is player-safe
- ✅ Schema: Imported canon conforms to QF schemas

**10. Showrunner Approval:** APPROVED

**11. TU:** `TU-2025-11-10-LW-CanonTransferImport`

**12. Announce:** "Canon baseline imported from The Lighthouse Keeper. See constraint docs. Ready for Story Spark."

---

**TL;DR**
Load transfer package, detect conflicts with project seed, merge invariant canon to Cold (immutable), seed mutable canon to Hot (extensible), import timeline/entities/codex, document constraints for creative roles, validate, and hand off to Story Spark for plot development within canon rules.
