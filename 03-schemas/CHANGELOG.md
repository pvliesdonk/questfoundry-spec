# Schema Changelog

All notable changes to QuestFoundry schemas will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/pvliesdonk/questfoundry-spec/compare/schemas-v0.1.0...HEAD
[0.1.0]: https://github.com/pvliesdonk/questfoundry-spec/releases/tag/schemas-v0.1.0
