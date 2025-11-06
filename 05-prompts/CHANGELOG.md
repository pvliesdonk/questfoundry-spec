# Changelog — Layer 5 Prompts

All notable changes to Layer 5 prompts will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-06

### Added

**Loop-Focused Architecture (commit 428140c)**

- 13 loop playbooks (`loops/*.playbook.md`) - Complete procedures for all canonical loops
- 15 role adapters (`role_adapters/*.adapter.md`) - Thin interface specs (50-100 lines each)
- Modular Showrunner (5 focused modules): system_prompt, loop_orchestration, manifest_management, initialization, protocol_handlers
- Enhanced all 15 role prompts with "Loop Participation" sections

**Upload Kits**

- `orchestration-complete.zip` (36 files) - Complete loop-focused environment for production workflows
- `full-standalone.zip` (23 files) - All role prompts + showrunner modules
- `minimal-standalone.zip` (10 files) - Core roles for quick start
- `optional-standalone.zip` (9 files) - Additional roles (PN, LW, CC, etc.)
- Gemini splits for orchestration mode (5 zips, 10-file limit compliant)
- Gemini splits for full standalone mode (3 zips)

**Documentation**

- `upload_kits/README.md` - Complete kit descriptions with platform guidance
- `USAGE_GUIDE.md` - Updated to emphasize orchestration mode as recommended
- Loop playbook workflow examples
- Clear guidance on mode selection (standalone vs. orchestration)

**Build Tools**

- `spec-tools/src/questfoundry_spec_tools/upload_kits.py` - Preserves directory structure in zips
- Prevents filename collisions (multiple `system_prompt.md` files)
- Automated kit building: `uv run qfspec-build-kits`

### Features

**Orchestration Mode Benefits:**

- 70% context reduction vs. standalone mode (adapters: 50-100 lines vs. full prompts: 200-300 lines)
- Single-source-of-truth loop procedures (1 playbook vs 7 role prompts)
- Role interchangeability (swap implementations without changing playbooks)
- Clear RACI matrix and coordination

**Platform Support:**

- ChatGPT: Single upload with `orchestration-complete.zip`
- Claude: Individual files or complete zip
- Gemini: 5-zip orchestration splits respecting 10-file limit

### Technical Details

**15 Roles:**
- Core: Showrunner, Plotwright, Scene Smith, Style Lead, Gatekeeper, Book Binder
- Expansion: Lore Weaver, Codex Curator, Player Narrator, Researcher
- Production: Art Director, Illustrator, Audio Director, Audio Producer, Translator

**13 Loop Playbooks:**
- Hook Harvest, Story Spark, Lore Deepening, Codex Expansion, Style Tune-up
- Gatecheck, Binding Run, Narration Dry-Run
- Art Touch-up, Audio Pass, Translation Pass
- Post-Mortem, Archive Snapshot

**Architecture:**
- Loop-focused (commit 428140c) - AI-coordinated multi-role workflows
- Dual-format strategy: Full prompts for standalone, adapters for orchestration
- Protocol-compliant messaging (Layer 4 envelope v0.2.1)
- Cold SoT validation (Layer 3 schemas v0.2.0)

### Version Alignment

**Prompts Version:** v0.1.0
**Compatible with:**
- schemas-v0.2.0 (Layer 3)
- protocol-v0.2.1 (Layer 4)

---

## Release Notes

This is the first versioned release of Layer 5 prompts, introducing the loop-focused architecture
for efficient multi-role AI coordination. For production workflows, **orchestration mode is
recommended** due to significant context savings and clear coordination benefits.

**Quick Start:**

1. Download `orchestration-complete.zip` from release assets
2. Upload to ChatGPT/Claude/Gemini
3. Prompt: "Load the Story Spark playbook and execute it for a 3-scene mystery."
4. Showrunner coordinates all roles via loop playbook

See `05-prompts/USAGE_GUIDE.md` for complete usage instructions.
