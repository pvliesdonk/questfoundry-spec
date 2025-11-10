# Canon Workflows — Alternative Flows for Canon Management

**Document Version:** 1.0 (2025-11-10)
**Status:** NEW — Extends core loop architecture with canon-centric workflows

---

## Overview

QuestFoundry's standard workflow is **story-driven**: Story Spark generates hooks, Hook Harvest triages them, and Lore Deepening canonizes them. This works well for discovery-led authoring.

However, two additional **canon-centric workflows** are valuable:

1. **Canon Transfer (Shared Stories)** — Export canon from one project to seed the next
2. **World Genesis (Canon-First)** — Build extensive worldbuilding before plot design

This document specifies both workflows and their integration with the existing 7-layer architecture.

---

## 1) Canon Transfer — Shared Story Universes

### Use Case

**Scenario:** You've completed "The Lighthouse Keeper" (Project A) and want to write "The Harbor Master" (Project B) in the same universe. Project B should inherit Project A's established canon (geography, factions, metaphysics, timeline) while allowing new story beats.

**Goal:** Export Project A's canon at end-of-project; import it as seed canon for Project B.

---

### Workflow

#### 1.1 Export Phase (End of Project A)

**Trigger (Showrunner):**
After final Binding Run and before project archival.

**Loop:** Canon Transfer — Export
**Required roles:** Lore Weaver (R), Codex Curator (C), Gatekeeper (C), Showrunner (A)

**Procedure:**

1. **Canon Snapshot (Lore Weaver)**
   - Identify all Cold canon packs from Project A
   - Tag canon as:
     - **Invariant** — Must remain true in Project B (e.g., "Wormhole 3 collapsed in Y-18")
     - **Mutable** — Can evolve in Project B (e.g., "Toll Syndicate has 5 known members")
     - **Local** — Project A only; exclude from transfer (e.g., "Kestrel's personal backstory")

2. **Codex Export (Codex Curator)**
   - Bundle player-safe codex entries that apply universe-wide
   - Mark entries as **inherited** (from Project A) vs **new** (to be created in Project B)

3. **Timeline Anchors**
   - Export Project A timeline with T0/T1/T2 markers
   - Project B will extend timeline as T3/T4/...

4. **Gatekeeper Validation**
   - Check exported canon for:
     - No Project A spoilers leaking into invariant canon
     - No broken references (all entities/places defined)
     - Presentation hygiene (player-safe codex clean)

5. **Package Export**
   - Create **Canon Transfer Package** artifact:
     - Invariant canon (must honor)
     - Mutable canon (can extend)
     - Codex baseline (inherited entries)
     - Timeline anchors (past events)
     - Metadata (source project, export date, snapshot ID)

**Deliverable:**
`canon_transfer_package_<project-a-slug>.json` (Layer 3 schema)

---

#### 1.2 Import Phase (Start of Project B)

**Trigger (Showrunner):**
During Project B initialization, before first Story Spark.

**Loop:** Canon Transfer — Import
**Required roles:** Lore Weaver (R), Codex Curator (C), Gatekeeper (C), Showrunner (A)

**Procedure:**

1. **Load Transfer Package (Lore Weaver)**
   - Import `canon_transfer_package_<project-a-slug>.json`
   - Parse invariant/mutable canon
   - Load timeline anchors as T0 (Project A baseline)

2. **Seed Project B Hot**
   - Invariant canon → merge to **Cold** immediately (no changes allowed)
   - Mutable canon → place in **Hot** as accepted canon (can be extended)
   - Timeline → T0/T1/T2 from Project A; T3+ available for Project B

3. **Codex Import (Codex Curator)**
   - Mark inherited codex entries as `source: <project-a>`
   - Flag gaps where Project B needs new entries

4. **Gatekeeper Validation**
   - Verify invariant canon doesn't conflict with Project B seed ideas
   - If conflict detected, escalate to Showrunner (reject import or revise Project B concept)

5. **Announce Constraints**
   - Document for Plotwright/Scene Smith:
     - **Invariants**: "Wormhole 3 collapsed in Y-18 (cannot change)"
     - **Mutables**: "Toll Syndicate has 5 known members (can add more)"
     - **Timeline**: "Project B starts at Y+2 (two years after Project A)"

**Deliverable:**
- Cold canon (invariants merged)
- Hot canon (mutables seeded)
- Constraint notes for creative roles
- TU documenting the import (`TU-<date>-LW-CanonTransfer`)

---

#### 1.3 Project B Story Development

**Standard Flow (with canon constraints):**

1. **Story Spark** — Plotwright designs topology honoring invariant canon
2. **Hook Harvest** — New hooks from Project B story
3. **Lore Deepening** — Extends mutable canon; respects invariants
4. **Codex Expansion** — Creates new entries; cross-refs inherited entries

**Safeguard:**
Gatekeeper blocks any changes that violate invariant canon. Lore Weaver may propose **canon extension** (adding detail to mutables) but not **canon contradiction** (breaking invariants).

---

### New Artifacts

#### Canon Transfer Package

**Schema:** `canon_transfer_package.schema.json` (Layer 3)

**Contents:**
- **Metadata**
  - `source_project`: Project A ID
  - `export_date`: YYYY-MM-DD
  - `snapshot_id`: Cold snapshot tag
- **Invariant Canon** (array of canon packs marked `immutable: true`)
- **Mutable Canon** (array of canon packs marked `immutable: false`)
- **Codex Baseline** (array of codex entries marked `inherited: true`)
- **Timeline Anchors** (T0/T1/T2 from Project A)
- **Entity Registry** (characters/places/factions defined in Project A)

**Validation:**
- All referenced entities must be defined
- No spoiler leaks in invariant canon
- Timeline anchors must be chronologically ordered

---

### Success Criteria

**Export:**
- Canon package contains all invariant rules from Project A
- No Project A spoilers leak into invariant canon
- Codex baseline is player-safe
- Package validates against schema

**Import:**
- Invariant canon merges to Cold without conflicts
- Mutable canon seeds Hot without contradictions
- Plotwright/Scene Smith understand constraints
- Gatekeeper can enforce invariants during Project B development

---

### RACI

| Task                  | R           | A          | C          | I       |
| --------------------- | ----------- | ---------- | ---------- | ------- |
| Canon export tagging  | Lore Weaver | Showrunner | Curator    | Plot    |
| Codex baseline export | Curator     | Lore       | Gatekeeper | —       |
| Package validation    | Gatekeeper  | Showrunner | Lore       | All     |
| Canon import to Cold  | Lore Weaver | Showrunner | Gatekeeper | Plot/SS |
| Constraint docs       | Lore Weaver | Showrunner | Plot/SS    | All     |

---

## 2) World Genesis — Canon-First Development

### Use Case

**Scenario:** You're writing an epic fantasy series. Before designing the plot, you want to build:
- Detailed magic system with rules and constraints
- Geography with 12 kingdoms, trade routes, historical conflicts
- Timeline spanning 500 years with 3 major wars
- Metaphysics (gods, afterlife, prophecy mechanics)
- Faction hierarchy (political houses, guilds, temples)

**Goal:** Lore Weaver proactively builds deep canon **before** Plotwright starts designing story structure. Story then unfolds within this rich, pre-built world.

---

### Workflow

#### 2.1 World Genesis Loop

**Trigger (Showrunner):**
At project start, **before** Story Spark. User explicitly requests canon-first approach.

**Loop:** World Genesis
**Required roles:** Lore Weaver (R), Codex Curator (C), Researcher (C, optional), Style Lead (C), Gatekeeper (C), Showrunner (A)

**Procedure:**

1. **Frame the World (Lore Weaver + Showrunner)**
   - Define canon scope:
     - **Geography** — How many regions/kingdoms/biomes?
     - **History** — How far back does the timeline go?
     - **Metaphysics** — Magic, gods, afterlife, prophecy?
     - **Factions** — How many major powers?
     - **Technology/Culture** — What's the baseline?
   - Set **worldbuilding budget**: How much canon to build before story starts?

2. **Proactive Canon Creation (Lore Weaver)**
   - Unlike standard Lore Deepening (which responds to hooks), World Genesis is **proactive**:
     - Lore Weaver drafts canon packs directly
     - No hooks required; this IS the discovery phase
   - For each theme (geography, magic, history, factions):
     - Write canon answers (spoiler-level detail allowed)
     - Define invariants & constraints
     - Build timeline anchors (T0 = ancient past, T1 = recent history, T2 = story "now")
     - Create knowledge ledger (who knows what)

3. **Factual Grounding (Researcher, if active)**
   - For real-world inspirations (e.g., medieval trade routes, siege tactics):
     - Research corroborates claims
     - Citations added to canon
     - If dormant: mark `uncorroborated:<risk>`

4. **Codex Baseline (Codex Curator)**
   - Create player-safe codex entries for world elements:
     - **Geography** — "The Ironwood Forest spans 200 leagues..."
     - **Factions** — "The Guild of Chandlers controls candle trade..."
     - **Metaphysics** — "Mages draw power from ley lines..."
   - Build taxonomy (category structure for codex)
   - Cross-link entries

5. **Style Anchors (Style Lead)**
   - Define voice/register for this world:
     - **Narrative voice** — Formal? Colloquial? Archaic?
     - **Dialogue patterns** — How do nobles speak vs. commoners?
     - **Motifs** — Recurring imagery (fire/ice, light/shadow)
   - Create style addendum for Scene Smith to use later

6. **Gatekeeper Preview**
   - Early review:
     - **Integrity** — All entity references resolve
     - **Style** — Voice is consistent
     - **Presentation** — Codex is player-safe
   - Note: Reachability/Nonlinearity don't apply yet (no plot)

7. **Stabilization**
   - Loop iterates until:
     - All canon themes covered
     - No internal contradictions
     - Codex baseline complete
     - Gatekeeper approves

**Deliverables (Hot → Cold after gatecheck):**
- **Canon Packs** (one per theme: geography, magic, history, factions)
- **Codex Baseline** (player-safe entries for world elements)
- **Style Addendum** (voice/register for this world)
- **Timeline Foundation** (T0/T1/T2 anchors)
- **Constraint Manifest** (rules for Plotwright: "Magic cannot resurrect the dead", "Trade routes frozen in winter")

---

#### 2.2 Story Development (Post-Genesis)

**Standard Flow (with canon foundation):**

1. **Story Spark** — Plotwright designs topology **within canon constraints**:
   - Geography canon defines where hubs/gateways can exist
   - Magic canon defines what powers are plausible gates
   - Faction canon defines political tensions for loops
   - Timeline canon defines when story occurs (T2 or later)

2. **Hook Harvest** — New hooks from Story Spark:
   - **Narrative/Scene hooks** — Plot-specific questions
   - **Lore hooks** — Extensions to existing canon (not contradictions)

3. **Lore Deepening** — Extends genesis canon (doesn't replace):
   - Answers plot-specific hooks
   - Adds detail to mutable canon
   - Respects invariants set in World Genesis

4. **Codex Expansion** — Extends baseline:
   - Adds plot-specific entries
   - Cross-refs genesis entries

**Safeguard:**
Gatekeeper blocks plot changes that violate genesis canon invariants. Lore Weaver may extend (add detail) but not contradict.

---

### Loop Iteration

World Genesis supports **multi-iteration stabilization** (per Epic 7/8 architecture):

**Example:**

```
World Genesis Loop:

Iteration 1:
  ✓ Step 1: Frame the World (scope: magic, geography, factions)
  ✓ Step 2: Draft Magic Canon (Lore Weaver)
  ✓ Step 3: Draft Geography Canon (Lore Weaver)
  ✓ Step 4: Draft Faction Canon (Lore Weaver)
  ✓ Step 5: Codex Baseline (Codex Curator)
  ✓ Step 6: Style Anchors (Style Lead)
  ❌ Step 7: Gatekeeper Preview (BLOCKED)
      Issues: Magic canon contradicts geography canon (ley lines don't align)

Showrunner decision: Revise magic canon (back to Step 2)

Iteration 2:
  ✓ Step 2: Revise Magic Canon (align ley lines with geography)
  ✓ Step 3: Geography Canon (no changes needed)
  ✓ Step 4: Faction Canon (no changes needed)
  ✓ Step 5: Update Codex (revised magic entries)
  ✓ Step 6: Style check (passed)
  ✓ Step 7: Gatekeeper Preview (PASSED)
  ✓ Step 8: Merge to Cold

✅ Loop Stabilized
```

---

### Scoping Guidance

**How much worldbuilding is enough?**

Showrunner and Lore Weaver collaborate on **worldbuilding budget**:

**Minimal Genesis** (1-2 hours):
- 1 canon pack for magic/metaphysics
- 1 canon pack for geography
- 5-10 codex entries
- 1 style addendum

**Standard Genesis** (4-8 hours):
- 3-5 canon packs (magic, geography, factions, history, metaphysics)
- 20-30 codex entries
- 1 style addendum
- Timeline with 5-10 anchors

**Epic Genesis** (20+ hours):
- 10+ canon packs (detailed magic, 12 kingdoms, 500-year timeline, 8 factions, metaphysics, technology, culture)
- 100+ codex entries
- Multiple style addenda (per region/faction voice)
- Extensive timeline (50+ anchors)

**Heuristic:** Stop when you can answer Plotwright's likely questions. Over-building risks unused canon.

---

### Success Criteria

**World Genesis Complete:**
- All scoped canon themes have canon packs
- No internal contradictions in genesis canon
- Codex baseline covers world fundamentals
- Style addendum sets voice/register
- Gatekeeper approves (Integrity + Style + Presentation)

**Story Spark Integration:**
- Plotwright can design topology using genesis canon
- Canon constraints are clear and actionable
- Hooks from Story Spark **extend** genesis (don't contradict)

---

### RACI

| Task                | R           | A          | C                 | I    |
| ------------------- | ----------- | ---------- | ----------------- | ---- |
| Frame world scope   | Lore Weaver | Showrunner | Style             | Plot |
| Draft genesis canon | Lore Weaver | Showrunner | Researcher, Style | —    |
| Codex baseline      | Curator     | Lore       | Style             | —    |
| Style anchors       | Style Lead  | Showrunner | Lore              | SS   |
| Gatekeeper preview  | Gatekeeper  | Showrunner | Lore              | All  |
| Merge to Cold       | Lore Weaver | Showrunner | Gatekeeper        | All  |

---

## 3) Comparison of Canon Workflows

| Aspect              | Standard (Story-Driven)     | Canon Transfer (Shared)        | World Genesis (Canon-First) |
| ------------------- | --------------------------- | ------------------------------ | --------------------------- |
| **Starting point**  | Story Spark → hooks         | Import from prior project      | Proactive canon building    |
| **Lore Weaver**     | Reactive (answers hooks)    | Curator (exports/imports)      | Proactive (builds canon)    |
| **When**            | After Story Spark           | Between projects               | Before Story Spark          |
| **Canon source**    | Hooks from plot/scenes      | Prior project's Cold canon     | Direct worldbuilding        |
| **Plot dependency** | Plot drives canon discovery | Plot inherits canon baseline   | Canon constrains plot       |
| **Best for**        | Discovery-led authoring     | Shared universes, sequels      | Epic fantasy, deep worlds   |

---

## 4) Integration with Existing Loops

### Loop Sequencing

**Standard Flow:**
```
Story Spark → Hook Harvest → Lore Deepening → Codex Expansion → Gatecheck → Cold
```

**Canon Transfer Flow (Project B):**
```
Canon Transfer (Import) → Story Spark → Hook Harvest → Lore Deepening → Codex Expansion → Gatecheck → Cold
```

**World Genesis Flow:**
```
World Genesis → Story Spark → Hook Harvest → Lore Deepening → Codex Expansion → Gatecheck → Cold
```

### Showrunner Orchestration

Per Epic 7/8 revised architecture:
- **Showrunner decides** which loop runs next from loop registry
- For Canon Transfer: User requests import at project init
- For World Genesis: User requests canon-first at project init
- Showrunner adapts: if genesis canon exists, Story Spark works within constraints

---

## 5) New Artifacts Required

### Canon Transfer Package

**Schema:** `03-schemas/canon_transfer_package.schema.json`

**Template:** `02-dictionary/artifacts/canon_transfer_package.md`

**Fields:**
- Metadata (source project, export date, snapshot ID)
- Invariant canon (immutable rules)
- Mutable canon (extensible rules)
- Codex baseline (inherited entries)
- Timeline anchors
- Entity registry

### World Genesis Manifest

**Schema:** `03-schemas/world_genesis_manifest.schema.json`

**Template:** `02-dictionary/artifacts/world_genesis_manifest.md`

**Fields:**
- Worldbuilding scope (themes covered)
- Canon pack IDs (generated during genesis)
- Codex baseline IDs
- Style addendum ID
- Timeline foundation
- Constraint manifest (rules for Plotwright)

---

## 6) Layer Impacts

### Layer 0 (North Star)

**New documents:**
- `00-north-star/LOOPS/canon_transfer_export.md`
- `00-north-star/LOOPS/canon_transfer_import.md`
- `00-north-star/LOOPS/world_genesis.md`

### Layer 1 (Roles)

**Updated briefs:**
- **Lore Weaver**: Add proactive worldbuilding mode (World Genesis)
- **Showrunner**: Add canon transfer orchestration

### Layer 2 (Dictionary)

**New artifact templates:**
- `02-dictionary/artifacts/canon_transfer_package.md`
- `02-dictionary/artifacts/world_genesis_manifest.md`

### Layer 3 (Schemas)

**New schemas:**
- `03-schemas/canon_transfer_package.schema.json`
- `03-schemas/world_genesis_manifest.schema.json`

### Layer 4 (Protocol)

**New intents:**
- `canon.transfer.export`
- `canon.transfer.import`
- `world_genesis.create`

**New flows:**
- `04-protocol/FLOWS/canon_transfer.md`
- `04-protocol/FLOWS/world_genesis.md`

### Layer 5 (Prompts)

**Updated prompts:**
- **Lore Weaver**: Add World Genesis mode
- **Showrunner**: Add canon transfer/genesis orchestration

**New playbooks:**
- `05-prompts/playbooks/playbook_canon_transfer_export.md`
- `05-prompts/playbooks/playbook_canon_transfer_import.md`
- `05-prompts/playbooks/playbook_world_genesis.md`

### Layer 6 (Libraries)

**New modules:**
- Canon transfer export/import logic
- World Genesis loop implementation

### Layer 7 (UI/CLI)

**New commands:**
```bash
qf canon export <project-slug>         # Export canon transfer package
qf canon import <package-path>         # Import canon into new project
qf run world-genesis                   # Run World Genesis loop
qf run canon-transfer --mode=export    # Export mode
qf run canon-transfer --mode=import    # Import mode
```

---

## 7) Migration Path

For existing projects:

**To use Canon Transfer:**
1. Run `qf canon export <project-slug>` at end of Project A
2. Initialize Project B
3. Run `qf canon import <package-path>` at Project B start
4. Proceed with Story Spark (respecting invariants)

**To use World Genesis:**
1. Initialize new project with `qf init --canon-first`
2. Run `qf run world-genesis` before first Story Spark
3. Review genesis canon in Cold
4. Run `qf run story-spark` (Plotwright works within constraints)

---

## 8) Quality Bar Implications

### Canon Transfer

**Export:**
- **Integrity** — All exported entity references resolve
- **Presentation** — No spoilers in invariant canon or codex baseline

**Import:**
- **Integrity** — Imported canon doesn't conflict with Project B seed
- **Gateways** — Ensure imported rules don't break Project B topology

### World Genesis

**Genesis Loop:**
- **Integrity** — All entity references resolve within genesis canon
- **Style** — Voice/register consistent across genesis
- **Presentation** — Codex baseline is player-safe

**Story Spark (post-genesis):**
- **Integrity** — Plot honors genesis invariants
- **Reachability/Nonlinearity** — Topology uses geography/faction canon
- **Gateways** — Gates use metaphysics/magic canon

---

## 9) Example Scenarios

### Scenario 1: Sequel Series (Canon Transfer)

**Project A: "The Lighthouse Keeper"**
- Ends with Wormhole 3 collapsed, Toll Syndicate exposed
- Canon transfer package exports:
  - Invariants: Wormhole 3 status, Toll Syndicate structure
  - Mutables: Character fates (can evolve), dock politics
  - Codex: Union tokens, dock inspections, wormhole physics

**Project B: "The Harbor Master" (2 years later)**
- Imports transfer package
- Story Spark: New protagonist (harbor master), new conflict (wormhole repair efforts)
- Lore Deepening: Extends Toll Syndicate (adds new members), updates dock politics
- Respects invariants: Wormhole 3 still collapsed, Toll structure unchanged

### Scenario 2: Epic Fantasy (World Genesis)

**Project: "The Broken Crown" (12-book series)**

**World Genesis Phase (20 hours):**
- Magic canon: 5 schools of magic, ley line network, divine vs. arcane
- Geography canon: 12 kingdoms, 3 continents, trade routes, capitals
- History canon: 500-year timeline, 3 major wars, dynasties
- Faction canon: 8 great houses, 3 temples, 2 guilds
- Metaphysics canon: Gods, afterlife, prophecy mechanics, soul magic
- Codex baseline: 100+ entries (kingdoms, magic schools, gods, wars)

**Story Spark (Book 1: "The Heir's Gambit"):**
- Plotwright: Designs topology using kingdom geography (hubs = capitals)
- Gateways: Use magic/faction access (e.g., "Need House Vaelen's seal")
- Loops: Political intrigue between houses (from faction canon)
- Story unfolds within pre-built world constraints

**Book 2+:**
- Lore Deepening extends genesis canon (new wars, new houses)
- Codex Expansion adds book-specific entries
- Genesis invariants remain (magic rules, geography, core history)

---

## 10) Conclusion

These two canon-centric workflows extend QuestFoundry's flexibility:

**Canon Transfer** enables shared story universes, sequels, and franchise continuity.

**World Genesis** enables epic worldbuilding for deep fantasy/sci-fi before plot design.

Both integrate cleanly with the existing 7-layer architecture, Hot/Cold model, and iterative loop stabilization (Epic 7/8).

**Recommendation:**
- Implement Canon Transfer first (simpler, high-value for sequels)
- Implement World Genesis second (requires more complex Lore Weaver proactive mode)
- Both are **optional workflows** — standard story-driven flow remains default

---

**Next Steps:**
1. Create loop specs for Canon Transfer (Export/Import) and World Genesis
2. Design schemas for Canon Transfer Package and World Genesis Manifest
3. Update Lore Weaver charter/brief for proactive worldbuilding
4. Create playbooks for Showrunner orchestration
5. Implement Layer 6/7 support for new commands
