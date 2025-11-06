# Changelog — Layer 5 Prompts

All notable changes to Layer 5 prompts will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-06

### Added

#### Loop-Focused Architecture (commits a300224, 428140c)

Complete transformation of Layer 5 from role-focused to loop-focused architecture, making loop playbooks the primary executable units.

**13 Loop Playbooks** (`loops/*.playbook.md`)

Each playbook contains complete procedures with:
- Purpose and activation criteria
- RACI matrix (from Layer 1)
- Complete procedure with message sequences (Layer 0 + Layer 4)
- Deliverables and success criteria
- Failure modes and remedies
- Schema references to Layer 3
- Validation examples with complete message flows

**Playbooks by category:**
- **Discovery:** Story Spark, Hook Harvest, Lore Deepening
- **Refinement:** Codex Expansion, Style Tune-up
- **Asset Production:** Art Touch-up, Audio Pass, Translation Pass
- **Quality & Export:** Binding Run, Narration Dry-Run, Gatecheck, Post-Mortem, Archive Snapshot

**15 Role Adapters** (`role_adapters/*.adapter.md`)

Thin interface specs (50-100 lines each) optimized for multi-role orchestration:
- Core expertise summary
- Protocol intents handled (receives/sends)
- Loop participation references
- Efficient context usage

**Roles:** Showrunner, Plotwright, Scene Smith, Style Lead, Gatekeeper, Book Binder, Player Narrator, Lore Weaver, Codex Curator, Researcher, Art Director, Illustrator, Audio Director, Audio Producer, Translator

**Modular Showrunner** (5 focused modules)

Split 213-line monolith into focused modules with single responsibility:
- `system_prompt.md` (110 lines) - Index and navigation
- `loop_orchestration.md` (100 lines) - Execute playbooks
- `manifest_management.md` (102 lines) - Hot/Cold operations
- `initialization.md` (223 lines) - 7-step project setup
- `protocol_handlers.md` (230 lines) - Message validation

Benefits: Clear navigation, cross-references, maintainability

**Enhanced Role Prompts**

All 15 full role prompts (200-300 lines each) enhanced with:
- "Loop Participation" section
- References to loop playbooks with relative paths
- Preserved all existing domain expertise content
- Use case: Standalone work, learning, ChatGPT sessions

**Documentation**

- `README.md` - Architecture overview, dual-format strategy
- `USAGE_GUIDE.md` - Loop playbook workflows, format selection
- `ARCHITECTURE.md` (NEW) - Comprehensive design rationale (60+ sections)
  - Problem statement, solution principles
  - Component descriptions, workflow scenarios
  - Benefits analysis, migration path
  - Future enhancements

#### Upload Kits and Distribution (commit 426f2b9)

**14 Upload Kits** for ChatGPT, Claude, and Gemini

**Orchestration Mode** ⭐ (NEW - recommended for production)
- `orchestration-complete.zip` (36 files)
  - 4 shared patterns
  - 4 showrunner modules
  - 13 loop playbooks
  - 15 role adapters

**Gemini Orchestration Splits** (10-file limit compliant)
- `gemini-orchestration-1-foundation.zip` (9 files) - Shared + showrunner + SR adapter
- `gemini-orchestration-2-playbooks.zip` (10 files) - Core loop playbooks
- `gemini-orchestration-3-playbooks-extra.zip` (3 files) - Additional loops
- `gemini-orchestration-4-adapters-core.zip` (10 files) - Core role adapters
- `gemini-orchestration-5-adapters-extra.zip` (4 files) - Optional role adapters

**Standalone Mode** (traditional)
- `minimal-standalone.zip` (10 files) - Quick start with core roles
- `optional-standalone.zip` (9 files) - Additional roles (PN, LW, CC, etc.)
- `full-standalone.zip` (23 files) - All role prompts + showrunner modules

**Gemini Standalone Splits** (10-file limit compliant)
- `gemini-minimal-standalone.zip` (10 files)
- `gemini-optional-standalone.zip` (9 files)
- `gemini-full-standalone-1.zip` (10 files) - Shared + showrunner + 1 role
- `gemini-full-standalone-2.zip` (10 files) - 10 role prompts
- `gemini-full-standalone-3.zip` (3 files) - 3 role prompts

**Build Tools**
- `spec-tools/src/questfoundry_spec_tools/upload_kits.py` - Automated kit building
- Preserves original directory structure in zips (prevents filename collisions)
- Command: `uv run qfspec-build-kits`
- Output: `dist/upload_kits/*.zip`

**Documentation**
- `upload_kits/README.md` - Complete kit descriptions, platform guidance, quick starts
- `USAGE_GUIDE.md` - Updated to emphasize orchestration mode as recommended
- Loop playbook workflow examples
- Clear guidance on mode selection

**Manifests** (10 new files in `05-prompts/upload_kits/manifests/`)
- `orchestration-complete.list` (36 files)
- `full-standalone.list` (23 files)
- 8 Gemini split manifests (respecting 10-file limits)

### Features

#### Dual-Format Strategy

**Orchestration Mode** (AI-coordinated) ⭐ **RECOMMENDED**
- Showrunner loads loop playbook + role adapters
- Single-source-of-truth procedures (1 playbook vs 7 role prompts)
- 70% context reduction (adapters: 50-100 lines vs full prompts: 200-300 lines)
- Efficient context usage (~1000 lines vs ~3000 lines)
- Role interchangeability (swap implementations without changing playbooks)
- Clear RACI matrix and coordination

**Standalone Mode** (human-led)
- Full role prompts with complete domain expertise
- Human coordinates workflow via prompts
- Best for learning, exploration, single-role tasks

#### Architecture Benefits

**Single Source of Truth**
- Loop procedures defined once in playbook
- Eliminates duplication across role prompts
- Update loop once, all roles benefit

**Maintainability**
- Clear modular structure
- Single responsibility per component
- Easy to understand and update

**Role Interchangeability**
- Roles implement standard interface from adapters
- Swap implementations without changing playbooks
- Clear separation of concerns

**Clear Orchestration**
- Showrunner loads playbook and coordinates
- Roles respond to protocol intents
- RACI matrix defines responsibilities

**Testability**
- Validation examples for all 13 loops
- Complete message flows included
- Realistic payloads matching Layer 3 schemas

**Efficient Context**
- Adapters: 50-100 lines per role
- Full prompts: 200-300 lines per role
- Load only what's needed for specific loop

#### Platform Support

**ChatGPT**
- Single upload with `orchestration-complete.zip` (36 files)
- Or `minimal-standalone.zip` (10 files) for quick start
- Supports zips and individual files

**Claude**
- Handles multiple attachments well
- Individual files preferred for better grounding
- `orchestration-complete.zip` also supported

**Gemini**
- 10-file limit per zip respected
- 5 orchestration splits or 5 standalone splits
- Upload in sequence: foundation → playbooks → adapters

### Technical Details

#### Protocol Compliance

- Layer 4 envelope v0.2.1 compliant
- All messages follow ENVELOPE.md specification
- Proper context fields (hot_cold, snapshot, TU, loop)
- Traceability via correlation_id and refs

#### Schema Integration

- Cold SoT validation via Layer 3 schemas v0.2.0
- Canonical URLs: `https://questfoundry.liesdonk.nl/schemas/`
- No upload needed (referenced directly)
- Gatekeeper and Book Binder validate against schemas

#### Shared Patterns

4 cross-role patterns included in all kits:
- `context_management.md` - Hot/Cold separation, snapshot references
- `safety_protocol.md` - PN boundaries, content hygiene
- `escalation_rules.md` - When to request human intervention
- `human_interaction.md` - Question batching, timeout handling

### Changed

#### Upload Kit Build Process

**Before:**
- Flattened filenames (e.g., `showrunner.md`)
- Filename collisions (multiple `system_prompt.md` files)
- No orchestration kits
- Manual zip creation

**After:**
- Preserves directory structure (e.g., `05-prompts/showrunner/system_prompt.md`)
- No collisions when extracting zips
- Automated orchestration kit building
- Command: `uv run qfspec-build-kits`

#### Documentation Focus

**Before:**
- Emphasized standalone mode
- Role-focused workflows
- Limited guidance on multi-role coordination

**After:**
- Emphasizes orchestration mode as recommended for production
- Loop-focused workflows with clear procedures
- Comprehensive guidance on mode selection
- Platform-specific instructions (ChatGPT, Claude, Gemini)

### Files Modified/Created

**Total: 51 files changed across 3 commits**

**Commit a300224 (Loop playbooks):**
- 13 loop playbooks created
- 13 validation example flows created
- 26 files added

**Commit 428140c (Dual formats):**
- 15 role adapters created
- 15 role prompts enhanced (Loop Participation sections)
- 5 showrunner modules (4 new, 1 rewritten)
- 3 documentation files (README.md, USAGE_GUIDE.md, ARCHITECTURE.md)
- 38 files modified/created

**Commit 426f2b9 (Upload kits):**
- `upload_kits.py` rewritten (preserve directory structure)
- `upload_kits/README.md` complete rewrite
- `USAGE_GUIDE.md` updated (emphasize orchestration)
- 10 new manifest files created
- 13 files modified/created

### Version Alignment

**Prompts Version:** v0.1.0
**Compatible with:**
- schemas-v0.2.0 (Layer 3)
- protocol-v0.2.1 (Layer 4)

**Dependencies:**
- Schemas: All validation via canonical URLs
- Protocol: Envelope v0.2.1 for all messages
- Layer 1: RACI matrices for all loops
- Layer 0: Workflows and sequences

---

## Migration Notes

### From Pre-Loop Architecture

**If you were using role prompts before commit a300224:**

1. **Keep using standalone mode** - Full role prompts still available and fully supported
2. **Try orchestration mode** - 70% context savings, clearer coordination
3. **Update Showrunner** - Now modular (5 files instead of 1)
4. **Use loop playbooks** - Single-source-of-truth procedures

**Breaking changes:** None - all previous workflows still supported via standalone mode

### Upload Kit Changes

**If you were using old upload kits:**

1. **Zips now preserve paths** - Extract with `unzip` to see directory structure
2. **New orchestration kits available** - Recommended for production
3. **Build locally** - `uv run qfspec-build-kits` for fresh kits
4. **Gemini splits provided** - 10-file limit respected

**Breaking changes:** Zip internal structure changed (but content identical)

---

## Release Notes

This is the **first versioned release** of Layer 5 prompts, representing the completion of the loop-focused architecture transformation across three major commits:

1. **a300224** - Added 13 loop playbooks as primary executable units
2. **428140c** - Added dual-format strategy (full prompts + role adapters)
3. **426f2b9** - Aligned upload kits with new architecture

### Key Achievements

✅ **Loop-focused architecture** - Single-source-of-truth procedures
✅ **Dual-format strategy** - Full prompts for standalone, adapters for orchestration
✅ **70% context reduction** - Efficient multi-role coordination
✅ **14 upload kits** - Optimized for ChatGPT, Claude, Gemini
✅ **Complete documentation** - Usage guides, architecture docs, examples
✅ **Protocol compliance** - Layer 4 envelope v0.2.1
✅ **Schema validation** - Layer 3 schemas v0.2.0

### Recommended Usage

**For production workflows:** Use **orchestration mode** with `orchestration-complete.zip`
- 70% context savings
- Clear coordination via loop playbooks
- Role interchangeability

**For learning/exploration:** Use **standalone mode** with `minimal-standalone.zip`
- Complete role prompts
- Human-led workflows
- Easier to understand

### Quick Start

**ChatGPT/Claude:**
```bash
# Download orchestration kit
wget https://github.com/pvliesdonk/questfoundry-spec/releases/download/prompts-v0.1.0/orchestration-complete.zip

# Upload to platform and prompt:
"Load the Story Spark playbook from loops/ and execute it for a 3-scene mystery."
```

**Gemini:**
```bash
# Download all 5 orchestration splits
wget https://github.com/pvliesdonk/questfoundry-spec/releases/download/prompts-v0.1.0/gemini-orchestration-{1..5}-*.zip

# Upload in sequence: foundation → playbooks → adapters
# Then prompt: "Load Story Spark playbook and execute it."
```

See `05-prompts/USAGE_GUIDE.md` for complete instructions.

---

## Future Versions

Future releases will follow semantic versioning:

- **PATCH** (0.1.X) - Bug fixes, documentation updates
- **MINOR** (0.X.0) - New loops, new roles, enhanced features (backward compatible)
- **MAJOR** (X.0.0) - Breaking changes to architecture or protocol alignment

Track development in the [main repository](https://github.com/pvliesdonk/questfoundry-spec).
