# Schema Changelog

All notable changes to QuestFoundry schemas will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-11-05

### Added

- **Cold Source of Truth (Cold SoT) Schemas:**
  - `cold_manifest.schema.json` - Top-level file index with SHA-256 hashes for deterministic builds
  - `cold_book.schema.json` - Story structure, section order, and bibliographic metadata
  - `cold_art_manifest.schema.json` - Asset mappings with SHA-256 hashes and provenance tracking
  - `cold_fonts.schema.json` - Optional font file mappings for consistent typography
  - `cold_build_lock.schema.json` - Optional tool version pinning for reproducible builds
- **Hot Discovery Space Schema:**
  - `hot_manifest.schema.json` - Master index for Hot discovery space (TUs, hooks, proposals,
    drafts)

### Changed

- **Storage-Agnostic Architecture**: Added notes to `cold_manifest` and `hot_manifest` schemas
  clarifying that Layer 3 defines logical structure only; Layer 6 implementations may use JSON
  files, SQLite, Redis, or other backends
- Updated all Cold SoT-aware schemas to reference canonical URLs:
  `https://questfoundry.liesdonk.nl/schemas/`

### Documentation

- Updated Layer 5 system prompts (Book Binder, Gatekeeper, Art Director, Illustrator, Showrunner)
  with Cold SoT format sections and schema URLs
- Updated `05-prompts/USAGE_GUIDE.md` to reference schemas by canonical URL (no upload required)
- Updated `05-prompts/upload_kits/README.md` to clarify schemas are accessed via URL, not uploaded

### Context

This release adds the complete Cold Source of Truth format specification, enabling deterministic
builds and preventing protocol violations (e.g., Adventure Bay Binder Breakdown incident). The 6 new
schemas define manifest-driven builds with SHA-256 validation, eliminating heuristics and "newest
file wins" logic.

## [0.1.0] - 2025-11-05

### Added

- Initial release of all 18 artifact schemas
- **Core Artifacts:**
  - `hook_card.schema.json` - Hook tracking and routing
  - `tu_brief.schema.json` - Trace Unit (work unit) tracking
  - `canon_pack.schema.json` - Canonical story facts
  - `gatecheck_report.schema.json` - Quality validation reports
- **Content Artifacts:**
  - `codex_entry.schema.json` - Player-facing encyclopedia entries
  - `style_addendum.schema.json` - Style and voice guidelines
  - `style_manifest.schema.json` - Comprehensive style guide
  - `register_map.schema.json` - Language register specifications
  - `edit_notes.schema.json` - Editorial feedback and revisions
  - `research_memo.schema.json` - Factual research documentation
- **Asset Artifacts:**
  - `art_plan.schema.json` - Illustration planning
  - `art_manifest.schema.json` - Complete art asset inventory
  - `shotlist.schema.json` - Individual illustration specifications
  - `audio_plan.schema.json` - Audio production planning
  - `cuelist.schema.json` - Audio cue specifications
- **Export Artifacts:**
  - `view_log.schema.json` - Export metadata and traceability
  - `front_matter.schema.json` - Book front matter (title, credits, etc.)
  - `language_pack.schema.json` - Localization translations
  - `pn_playtest_notes.schema.json` - Player-Narrator playtest feedback
- **Project Metadata:**
  - `project_metadata.schema.json` - Project configuration

### Schema Details

- All schemas comply with JSON Schema Draft 2020-12
- Schema IDs use canonical URL pattern: `https://questfoundry.liesdonk.nl/schemas/`
- Comprehensive validation rules for each artifact type
- Detailed descriptions and examples in schema annotations

### Documentation

- Added schema generation documentation in `03-schemas/README.md`
- Linked to Layer 2 source documents (`02-dictionary/artifacts/`)
- Validation tools available in `spec-tools/`

[Unreleased]: https://github.com/pvliesdonk/questfoundry-spec/compare/schemas-v0.2.0...HEAD
[0.2.0]: https://github.com/pvliesdonk/questfoundry-spec/compare/schemas-v0.1.0...schemas-v0.2.0
[0.1.0]: https://github.com/pvliesdonk/questfoundry-spec/releases/tag/schemas-v0.1.0
