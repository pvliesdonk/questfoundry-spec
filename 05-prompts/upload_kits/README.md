# Upload Kits — Quick File Lists And Zip Commands

This folder provides quick copy-pasta file lists and example commands for creating zip archives of
the Layer 5 prompts you'll typically upload to a chatbot (ChatGPT, Claude, Gemini).

Platform limits to keep in mind:

- ChatGPT: max 10 files per upload action (you can repeat uploads). Zips can carry more than 10
  files.
- Gemini: zips can contain at most 10 files; use multiple zips for larger sets.

---

## Architecture Overview: Loop-Focused vs Role-Focused

Layer 5 now uses a **loop-focused architecture** with three usage modes:

### 1. Orchestrated Mode (Recommended — Most Efficient)

**Who loads what:**

- **Showrunner**: Loads loop playbook + role adapters for needed roles
- **Other roles**: Not needed (Showrunner coordinates via playbook)

**Context efficiency:** ~500 lines (1 playbook + 3-4 adapters @ 50-100 lines each)

**Files needed:**

```text
05-prompts/loops/[loop_name].playbook.md           # e.g., lore_deepening.playbook.md
05-prompts/role_adapters/showrunner.adapter.md
05-prompts/role_adapters/lore_weaver.adapter.md    # roles mentioned in playbook
05-prompts/role_adapters/gatekeeper.adapter.md
05-prompts/role_adapters/codex_curator.adapter.md
```

**Best for:** Multi-agent orchestration, production workflows, context-limited models

### 2. Standalone Mode (Current Upload Kits)

**Who loads what:**

- **Single role**: Loads full system prompt for one role
- Includes domain expertise + loop participation guidance

**Context efficiency:** ~200-300 lines per role

**Files needed:**

```text
05-prompts/_shared/*.md                       # 4 shared patterns
05-prompts/[role]/system_prompt.md           # Full prompt with Loop Participation section
```

**Best for:** Single-role tasks, learning/exploration, human-in-the-loop workflows

### 3. Hybrid Mode (Advanced)

Mix loop playbooks with full role prompts when you need both orchestration and deep expertise.

---

## Kit A: Minimal Standalone (10 files — ChatGPT-friendly)

**Purpose:** Core roles with full system prompts for standalone work

**Files (relative to repo root):**

```text
05-prompts/_shared/context_management.md
05-prompts/_shared/safety_protocol.md
05-prompts/_shared/escalation_rules.md
05-prompts/_shared/human_interaction.md
05-prompts/showrunner/system_prompt.md
05-prompts/plotwright/system_prompt.md
05-prompts/scene_smith/system_prompt.md
05-prompts/style_lead/system_prompt.md
05-prompts/gatekeeper/system_prompt.md
05-prompts/book_binder/system_prompt.md
```

**PowerShell (Windows):**

```powershell
Compress-Archive -Path @(
  '05-prompts/_shared/context_management.md',
  '05-prompts/_shared/safety_protocol.md',
  '05-prompts/_shared/escalation_rules.md',
  '05-prompts/_shared/human_interaction.md',
  '05-prompts/showrunner/system_prompt.md',
  '05-prompts/plotwright/system_prompt.md',
  '05-prompts/scene_smith/system_prompt.md',
  '05-prompts/style_lead/system_prompt.md',
  '05-prompts/gatekeeper/system_prompt.md',
  '05-prompts/book_binder/system_prompt.md'
) -DestinationPath kit-a-minimal-standalone.zip -Force
```

**Bash (macOS/Linux):**

```bash
zip -r kit-a-minimal-standalone.zip \
  05-prompts/_shared/context_management.md \
  05-prompts/_shared/safety_protocol.md \
  05-prompts/_shared/escalation_rules.md \
  05-prompts/_shared/human_interaction.md \
  05-prompts/showrunner/system_prompt.md \
  05-prompts/plotwright/system_prompt.md \
  05-prompts/scene_smith/system_prompt.md \
  05-prompts/style_lead/system_prompt.md \
  05-prompts/gatekeeper/system_prompt.md \
  05-prompts/book_binder/system_prompt.md
```

---

## Kit B: Full Standalone (all 15 roles)

**Purpose:** All role system prompts for comprehensive standalone work

**Additional roles beyond Kit A:**

```text
05-prompts/lore_weaver/system_prompt.md
05-prompts/codex_curator/system_prompt.md
05-prompts/player_narrator/system_prompt.md
05-prompts/researcher/system_prompt.md
05-prompts/art_director/system_prompt.md
05-prompts/illustrator/system_prompt.md
05-prompts/audio_director/system_prompt.md
05-prompts/audio_producer/system_prompt.md
05-prompts/translator/system_prompt.md
```

**Total:** 19 files (4 shared + 15 role prompts)

**PowerShell (Windows):**

```powershell
Compress-Archive -Path @(
  '05-prompts/_shared/context_management.md',
  '05-prompts/_shared/safety_protocol.md',
  '05-prompts/_shared/escalation_rules.md',
  '05-prompts/_shared/human_interaction.md',
  '05-prompts/showrunner/system_prompt.md',
  '05-prompts/plotwright/system_prompt.md',
  '05-prompts/scene_smith/system_prompt.md',
  '05-prompts/style_lead/system_prompt.md',
  '05-prompts/gatekeeper/system_prompt.md',
  '05-prompts/book_binder/system_prompt.md',
  '05-prompts/lore_weaver/system_prompt.md',
  '05-prompts/codex_curator/system_prompt.md',
  '05-prompts/player_narrator/system_prompt.md',
  '05-prompts/researcher/system_prompt.md',
  '05-prompts/art_director/system_prompt.md',
  '05-prompts/illustrator/system_prompt.md',
  '05-prompts/audio_director/system_prompt.md',
  '05-prompts/audio_producer/system_prompt.md',
  '05-prompts/translator/system_prompt.md'
) -DestinationPath kit-b-full-standalone.zip -Force
```

**Bash (macOS/Linux):**

```bash
zip -r kit-b-full-standalone.zip \
  05-prompts/_shared/*.md \
  05-prompts/*/system_prompt.md
```

---

## Kit C: Loop Orchestration (Showrunner + Playbooks + Adapters)

**Purpose:** Efficient multi-role orchestration via loop playbooks

**Recommended split for Gemini (10-file limit per zip):**

### Kit C1: Core Orchestration (10 files)

```text
05-prompts/showrunner/system_prompt.md
05-prompts/showrunner/loop_orchestration.md
05-prompts/showrunner/manifest_management.md
05-prompts/loops/hook_harvest.playbook.md
05-prompts/loops/lore_deepening.playbook.md
05-prompts/loops/story_spark.playbook.md
05-prompts/role_adapters/showrunner.adapter.md
05-prompts/role_adapters/plotwright.adapter.md
05-prompts/role_adapters/lore_weaver.adapter.md
05-prompts/role_adapters/gatekeeper.adapter.md
```

### Kit C2: Additional Playbooks (10 files)

```text
05-prompts/loops/codex_expansion.playbook.md
05-prompts/loops/style_tune_up.playbook.md
05-prompts/loops/art_touch_up.playbook.md
05-prompts/loops/audio_pass.playbook.md
05-prompts/loops/translation_pass.playbook.md
05-prompts/loops/binding_run.playbook.md
05-prompts/loops/narration_dry_run.playbook.md
05-prompts/loops/gatecheck.playbook.md
05-prompts/loops/post_mortem.playbook.md
05-prompts/loops/archive_snapshot.playbook.md
```

### Kit C3: Role Adapters (10 files)

```text
05-prompts/role_adapters/scene_smith.adapter.md
05-prompts/role_adapters/style_lead.adapter.md
05-prompts/role_adapters/codex_curator.adapter.md
05-prompts/role_adapters/book_binder.adapter.md
05-prompts/role_adapters/player_narrator.adapter.md
05-prompts/role_adapters/researcher.adapter.md
05-prompts/role_adapters/art_director.adapter.md
05-prompts/role_adapters/illustrator.adapter.md
05-prompts/role_adapters/audio_director.adapter.md
05-prompts/role_adapters/audio_producer.adapter.md
```

**PowerShell (Kit C1):**

```powershell
Compress-Archive -Path @(
  '05-prompts/showrunner/system_prompt.md',
  '05-prompts/showrunner/loop_orchestration.md',
  '05-prompts/showrunner/manifest_management.md',
  '05-prompts/loops/hook_harvest.playbook.md',
  '05-prompts/loops/lore_deepening.playbook.md',
  '05-prompts/loops/story_spark.playbook.md',
  '05-prompts/role_adapters/showrunner.adapter.md',
  '05-prompts/role_adapters/plotwright.adapter.md',
  '05-prompts/role_adapters/lore_weaver.adapter.md',
  '05-prompts/role_adapters/gatekeeper.adapter.md'
) -DestinationPath kit-c1-orchestration-core.zip -Force
```

**Bash (Kit C1):**

```bash
zip -r kit-c1-orchestration-core.zip \
  05-prompts/showrunner/system_prompt.md \
  05-prompts/showrunner/loop_orchestration.md \
  05-prompts/showrunner/manifest_management.md \
  05-prompts/loops/hook_harvest.playbook.md \
  05-prompts/loops/lore_deepening.playbook.md \
  05-prompts/loops/story_spark.playbook.md \
  05-prompts/role_adapters/showrunner.adapter.md \
  05-prompts/role_adapters/plotwright.adapter.md \
  05-prompts/role_adapters/lore_weaver.adapter.md \
  05-prompts/role_adapters/gatekeeper.adapter.md
```

---

## Kit D: On-Demand Loop Execution

**Purpose:** Load just what you need for a specific loop

**Example: Lore Deepening loop**

```text
05-prompts/loops/lore_deepening.playbook.md
05-prompts/role_adapters/showrunner.adapter.md
05-prompts/role_adapters/lore_weaver.adapter.md
05-prompts/role_adapters/gatekeeper.adapter.md
05-prompts/role_adapters/codex_curator.adapter.md
05-prompts/role_adapters/plotwright.adapter.md     # consulted
05-prompts/role_adapters/scene_smith.adapter.md    # consulted
```

**Total:** 7 files (~500-600 lines) — highly efficient!

**Bash:**

```bash
zip -r kit-d-lore-deepening.zip \
  05-prompts/loops/lore_deepening.playbook.md \
  05-prompts/role_adapters/showrunner.adapter.md \
  05-prompts/role_adapters/lore_weaver.adapter.md \
  05-prompts/role_adapters/gatekeeper.adapter.md \
  05-prompts/role_adapters/codex_curator.adapter.md \
  05-prompts/role_adapters/plotwright.adapter.md \
  05-prompts/role_adapters/scene_smith.adapter.md
```

---

## Layer 3 Schema Reference (No Upload Required)

**All Cold SoT schemas are available at canonical URLs**:
`https://questfoundry.liesdonk.nl/schemas/`

Book Binder and Gatekeeper system prompts reference these schemas by canonical URL for validation:

- cold_manifest.schema.json — Top-level file index with SHA-256 hashes
- cold_book.schema.json — Story structure, section order, metadata
- cold_art_manifest.schema.json — Asset mappings with provenance tracking
- hot_manifest.schema.json — Hot discovery space index
- project_metadata.schema.json — Project configuration

**No upload needed**: Agents reference schemas by URL. The schemas define the Cold SoT format that
prevents protocol violations (e.g., Adventure Bay Binder Breakdown).

---

## Build Link Folders And Zips (Recommended)

Generate `dist/upload_kits/*` with flattened filenames and ready-made zips (no platform subfolders):

- Using uv (recommended): `uv run qfspec-build-kits`
- Bash (macOS/Linux/WSL): `spec-tools/scripts/build_upload_kits.sh`
- PowerShell (Windows): `spec-tools/scripts/build_upload_kits.ps1`

You'll get (top-level):

- `kit-a-minimal-standalone/` and `kit-a-minimal-standalone.zip`
- `kit-b-full-standalone/` and `kit-b-full-standalone.zip`
- `kit-c1-orchestration-core/` and `kit-c1-orchestration-core.zip`
- `kit-c2-playbooks/` and `kit-c2-playbooks.zip`
- `kit-c3-adapters/` and `kit-c3-adapters.zip`

Filenames are simplified (e.g., `showrunner.md`, `book_binder.md`; shared docs keep their names) to
avoid collisions when attaching.

**Note**: Layer 3 schemas are not included in upload kits as they are available at canonical URLs
(`https://questfoundry.liesdonk.nl/schemas/`) and referenced directly by prompts.

---

## Platform Notes (General)

- **Prefer individual files over zips when possible**: better grounding and inline citation.
- **Keep filenames stable and descriptive** — most UIs show them prominently.
- **Reattach your kit when starting a fresh thread**; some UIs drop context.
- **If attachments are capped**, load shared patterns + Showrunner first, then add role prompts or
  playbooks as needed.
- **For orchestration**, use Kit C (playbooks + adapters) instead of Kit B (full prompts) to save
  context.

---

## Which Kit Should I Use?

| Use Case                           | Recommended Kit                                              | Files | Context |
| ---------------------------------- | ------------------------------------------------------------ | ----- | ------- |
| Learning QuestFoundry              | Kit A (Minimal Standalone)                                   | 10    | ~2K     |
| Single-role task (e.g., drafting)  | Specific role's system_prompt.md + shared                    | 5     | ~500    |
| Full project (human orchestrates)  | Kit B (Full Standalone)                                      | 19    | ~5K     |
| Multi-role loop (AI orchestrates)  | Kit D (On-Demand Loop) — 1 playbook + needed adapters       | 7     | ~600    |
| Complete orchestration environment | Kit C (all 3 parts)                                          | 30    | ~3K     |
| Production workflow                | Kit C1 (core) + specific playbooks from C2 as needed        | 10-15 | ~1-2K   |
| Context-constrained models         | Kit D (On-Demand Loop) — load only what's needed for 1 loop | 5-10  | ~500    |

**Context estimates:** Lines of markdown loaded into model context window

---

## Migration Note: Old Upload Kits → New Architecture

If you're upgrading from pre-loop-focused architecture:

- **Old "minimal kit"** → Now **Kit A** (no change)
- **Old "full kit"** → Now **Kit B** (no change)
- **NEW: Kit C** → Loop-focused orchestration (most efficient)
- **NEW: Kit D** → On-demand single-loop execution

The old upload kits (system prompts only) still work perfectly for standalone mode. The new kits
(playbooks + adapters) enable efficient multi-role orchestration.
