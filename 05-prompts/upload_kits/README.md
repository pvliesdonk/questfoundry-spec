# Upload Kits — Layer 5 Prompts for Chat Platforms

This directory provides manifests and build tools for creating upload kits for Layer 5 prompts.
Upload kits are organized collections of prompts optimized for different chat platforms (ChatGPT,
Claude, Gemini) and usage modes (standalone vs. orchestration).

**All zips preserve original directory structure** (e.g., `05-prompts/showrunner/system_prompt.md`)
to avoid filename collisions.

---

## Quick Start

**Build all kits:**

```bash
uv run qfspec-build-kits
# or: python spec-tools/src/questfoundry_spec_tools/upload_kits.py
```

Output: `dist/upload_kits/` with folders and zips for all kits.

---

## What's New in v0.2.0 — Schema Validation Enforcement

**BREAKING CHANGE:** Schema validation is now **mandatory** for all JSON artifacts.

All kits now include **validation enforcement** infrastructure:

1. **validation_contract.md** (file #1) — Non-negotiable validation requirements
   - Preflight protocol before producing artifacts
   - Hard gate enforcement (validation failures STOP workflow)
   - Schema discovery via SCHEMA_INDEX.json

2. **SCHEMA_INDEX.json** (file #2) — Canonical registry of 26 Layer 3 schemas
   - Schema $id, path, draft version, SHA-256 hash
   - Role-to-schema and intent-to-schema mappings

3. **Role prompts** — All 15 roles updated with "Output Validation (Required)" sections
   - Reference to validation_contract.md
   - Preflight/validation protocol
   - Hard gate enforcement

4. **Loop playbooks** — All 13 playbooks updated with validation checkpoints
   - Showrunner verifies validation_report.json at every handoff
   - STOP loop on validation failure

5. **Gatekeeper** — Enhanced with "Schema Validation Quality Bar"
   - Audits ALL artifacts in TU before merge
   - BLOCKS merge if any artifact lacks validation_report.json

**File ordering matters:** LLMs read files sequentially. validation_contract.md is always file #1.

**Impact:**

- Agents will validate all artifacts before handoff
- Invalid artifacts cause workflow STOP (hard gate)
- 0% → 100% validation compliance (expected)

**See:** `CHANGELOG.md` for complete v0.2.0 details and migration notes.

---

## Architecture: Two Usage Modes

Layer 5 supports two primary usage modes introduced in commit 428140c:

### 1. Standalone Mode (Traditional Role-Based)

**Who:** Single user working with individual roles **Context:** ~200-300 lines per role **Best
for:** Learning, single-role tasks, human-led workflows

**Files needed:**

- `_shared/validation_contract.md` — Validation requirements (v0.2.0+)
- `SCHEMA_INDEX.json` — Schema registry (v0.2.0+)
- `_shared/*.md` (4 files) — Cross-role patterns
- `[role]/system_prompt.md` — Full role prompt with domain expertise + loop participation

**Kits:** minimal-standalone, optional-standalone, full-standalone

### 2. Orchestration Mode (Loop-Focused Architecture) ⭐ **RECOMMENDED**

**Who:** Showrunner coordinating multiple roles via loop playbooks **Context:** ~500-1000 lines (1
playbook + 3-5 adapters + showrunner modules) **Best for:** Multi-role workflows, production runs,
efficient orchestration

**Files needed:**

- `_shared/validation_contract.md` — Validation requirements (v0.2.0+)
- `SCHEMA_INDEX.json` — Schema registry (v0.2.0+)
- `_shared/*.md` (4 files) — Cross-role patterns
- `showrunner/system_prompt.md` + modules — Orchestration index and tools
- `loops/[loop_name].playbook.md` — Complete procedure for one loop
- `role_adapters/[role].adapter.md` — Thin role interfaces (50-100 lines each)

**Kits:** orchestration-complete (+ Gemini splits)

---

## Available Kits

### Standalone Kits

**minimal-standalone.zip** (12 files — ChatGPT/Claude friendly)

- validation_contract.md + SCHEMA_INDEX.json (v0.2.0+)
- 4 shared patterns
- 1 showrunner prompt
- 5 core role prompts (Plotwright, Scene Smith, Style Lead, Gatekeeper, Book Binder)

**optional-standalone.zip** (9 files — addon roles)

- Player Narrator, Lore Weaver, Codex Curator, Researcher
- Art Director, Illustrator, Audio Director, Audio Producer, Translator

**full-standalone.zip** (25 files — all roles + showrunner modules)

- validation_contract.md + SCHEMA_INDEX.json (v0.2.0+)
- 4 shared patterns
- 5 showrunner modules (system_prompt, loop_orchestration, manifest_management, initialization,
  protocol_handlers)
- 15 full role prompts

### Orchestration Kits ⭐ **RECOMMENDED**

**orchestration-complete.zip** (38 files — complete loop-focused environment)

- validation_contract.md + SCHEMA_INDEX.json (v0.2.0+)
- 4 shared patterns
- 4 showrunner modules (system_prompt, loop_orchestration, manifest_management, protocol_handlers)
- 13 loop playbooks
- 15 role adapters

### Gemini Splits (10-file limit per zip)

**Standalone Mode:**

1. `gemini-minimal-standalone.zip` (11 files) — validation files + minimal set (removed
   human_interaction.md to fit limit)
2. `gemini-optional-standalone.zip` (9 files) — Same as optional-standalone
3. `gemini-full-standalone-1.zip` (10 files) — Validation + shared + showrunner modules + 1 role
   (removed human_interaction.md + initialization.md to fit limit)
4. `gemini-full-standalone-2.zip` (10 files) — 10 role prompts
5. `gemini-full-standalone-3.zip` (3 files) — 3 role prompts

**Orchestration Mode:** ⭐ **RECOMMENDED**

1. `gemini-orchestration-1-foundation.zip` (10 files) — Validation + shared + showrunner modules +
   SR adapter (removed human_interaction.md to fit limit)
2. `gemini-orchestration-2-playbooks.zip` (10 files) — Core loop playbooks
3. `gemini-orchestration-3-playbooks-extra.zip` (3 files) — Additional loops
4. `gemini-orchestration-4-adapters-core.zip` (10 files) — Core role adapters
5. `gemini-orchestration-5-adapters-extra.zip` (4 files) — Optional role adapters (art, audio,
   translator)

---

## Platform Guidelines

### ChatGPT

- **Limit:** 10 files per upload action (can repeat uploads or use zip)
- **Recommendation:** Use `orchestration-complete.zip` for production workflows (single upload)
- **Learning:** Use `minimal-standalone.zip` for quick start

### Claude

- **Limit:** No strict limit; handles multiple attachments well
- **Recommendation:** Upload `orchestration-complete.zip` or individual files from kit
- **Tip:** Individual files preferred for better grounding

### Gemini

- **Limit:** 10 files max per zip
- **Recommendation:** Upload `gemini-orchestration-1` through `-5` in sequence
- **Order:** Foundation first, then playbooks, then adapters

**General tip:** Prefer individual files over zips when platform allows (better grounding). Keep
filenames stable for UI reference.

---

## Which Kit Should I Use?

| Use Case                            | Recommended Kit(s)                         | Files  | Platform           |
| ----------------------------------- | ------------------------------------------ | ------ | ------------------ |
| Quick start / learning              | minimal-standalone                         | 10     | All                |
| Single-role task                    | minimal-standalone (or specific role only) | 5-10   | All                |
| **Production: Multi-role workflow** | **orchestration-complete** ⭐              | **36** | **ChatGPT/Claude** |
| **Production: Gemini**              | **gemini-orchestration-1 through -5** ⭐   | **36** | **Gemini**         |
| Full project (human orchestrates)   | full-standalone                            | 23     | ChatGPT/Claude     |
| Full project (Gemini, human-led)    | gemini-full-standalone-1/2/3               | 23     | Gemini             |
| Specific loop only                  | Custom selection from orchestration kit    | 7-15   | All                |

**⭐ Orchestration mode is recommended for production workflows** as it provides:

- Single-source-of-truth loop procedures
- Role interchangeability (swap implementations)
- Efficient context usage (~70% reduction vs. full prompts)
- Clear RACI matrix and coordination

---

## Build Process

The `qfspec-build-kits` command reads manifests from `manifests/` and creates:

1. **Folders** with symlinks (or copies on Windows) preserving directory structure
2. **Zips** with original paths (e.g., `05-prompts/showrunner/system_prompt.md`)

**Why preserve paths?** Multiple roles have `system_prompt.md` files. Original paths prevent
collisions when extracting zips.

**Manifest format:** Plain text, one repo-relative path per line (e.g.,
`05-prompts/_shared/context_management.md`).

---

## Example Workflows

### Standalone Mode: Draft First Manuscript

1. Upload `minimal-standalone.zip` to ChatGPT
2. Prompt: "You are Showrunner. Open TU for a 3-5 scene manuscript using Story Spark loop."
3. Iterate with Plotwright → Scene Smith → Style Lead → Gatekeeper → Book Binder
4. Upload `optional-standalone.zip` later for Player Narrator dry-run

### Orchestration Mode: Run Story Spark Loop ⭐ **RECOMMENDED**

1. Upload `orchestration-complete.zip` to Claude
2. Prompt: "Load the Story Spark playbook from loops/ and execute it for a 3-scene mystery."
3. Showrunner coordinates:
   - TU open with scope and role roster
   - Plotwright drafts outline with gateways
   - Scene Smith writes scenes with checkpoints
   - Style Lead audits register and proposes fixes
   - Gatekeeper pre-gates manuscript
   - Book Binder creates player-safe view
4. Result: Gate-approved manuscript with traceability

### Orchestration Mode: Lore Deepening

1. Upload `orchestration-complete.zip` (or just needed files for efficiency)
2. Prompt: "Load Lore Deepening playbook and run it for character backstory questions."
3. Showrunner coordinates per playbook:
   - Lore Weaver frames questions and drafts answers
   - Gatekeeper pre-gates for spoiler hygiene
   - Codex Curator receives summaries for integration
4. Result: Canon-compliant lore with gatecheck approval

### Gemini: Full Orchestration Setup

1. Upload `gemini-orchestration-1-foundation.zip` (shared + showrunner + SR adapter)
2. Upload `gemini-orchestration-2-playbooks.zip` (core loops)
3. Upload `gemini-orchestration-4-adapters-core.zip` (core role adapters)
4. Prompt: "Load Story Spark playbook and coordinate outline → scenes → style."

---

## Layer 3 Schema Reference (No Upload Required)

**All Cold SoT schemas are available at canonical URLs:**
`https://questfoundry.liesdonk.nl/schemas/`

Gatekeeper and Book Binder prompts reference these schemas by URL for validation:

- `cold_manifest.schema.json` — Top-level file index with SHA-256 hashes
- `cold_book.schema.json` — Story structure, section order, metadata
- `cold_art_manifest.schema.json` — Asset mappings with provenance tracking
- `hot_manifest.schema.json` — Hot discovery space index
- `project_metadata.schema.json` — Project configuration

**No upload needed.** Agents reference schemas by canonical URL. The schemas define the Cold SoT
format that prevents protocol violations (e.g., Adventure Bay Binder Breakdown).

---

## Manifest Inventory

Located in `05-prompts/upload_kits/manifests/`:

**Standalone:**

- `chatgpt_minimal.list` → `minimal-standalone.zip`
- `optional.list` → `optional-standalone.zip`
- `full-standalone.list` → `full-standalone.zip`
- `gemini_core_zip.list` → `gemini-minimal-standalone.zip`
- `gemini_optional_zip.list` → `gemini-optional-standalone.zip`
- `gemini-full-standalone-1/2/3.list` → Gemini full splits

**Orchestration:** ⭐

- `orchestration-complete.list` → `orchestration-complete.zip`
- `gemini-orchestration-1/2/3/4/5.list` → Gemini orchestration splits

---

## Build Scripts

Three equivalent ways to build kits:

1. **uv (recommended):** `uv run qfspec-build-kits`
2. **Python:** `python spec-tools/src/questfoundry_spec_tools/upload_kits.py`
3. **Shell scripts:**
   - Bash: `spec-tools/scripts/build_upload_kits.sh`
   - PowerShell: `spec-tools/scripts/build_upload_kits.ps1`

All methods produce identical output in `dist/upload_kits/`.

---

## Migration from Pre-428140c

If you're upgrading from pre-loop-focused architecture:

- **Old "minimal kit"** → Now `minimal-standalone.zip` (unchanged)
- **Old "full kit"** → Now `full-standalone.zip` (added showrunner modules)
- **NEW: `orchestration-complete.zip`** ⭐ — Loop-focused multi-role coordination (**recommended**)

The old standalone kits still work perfectly for human-led workflows. The new orchestration kits
enable efficient AI-coordinated multi-role workflows via loop playbooks (70% context reduction).

---

## Directory Structure in Zips

All zips preserve original paths to avoid filename collisions:

```
minimal-standalone.zip:
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

orchestration-complete.zip:
  05-prompts/_shared/*.md (4 files)
  05-prompts/showrunner/system_prompt.md
  05-prompts/showrunner/loop_orchestration.md
  05-prompts/showrunner/manifest_management.md
  05-prompts/showrunner/protocol_handlers.md
  05-prompts/loops/*.playbook.md (13 files)
  05-prompts/role_adapters/*.adapter.md (15 files)
```

Extract with `unzip` or your platform's zip utility. Original paths are preserved.

---

## Summary

- **Two modes:** Standalone (role-focused) and **Orchestration (loop-focused)** ⭐
- **Original paths preserved** in all zips to avoid collisions
- **Platform-specific splits** for Gemini's 10-file limit
- **Orchestration mode recommended** for production multi-role workflows (70% context savings)
- **Schemas referenced by URL** — no upload needed

For usage guidance and loop playbook instructions, see `05-prompts/USAGE_GUIDE.md`.
