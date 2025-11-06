# Layer 3 — JSON Schemas (Generated from Layer 2)

> **Purpose:** Machine-readable schemas derived from enriched Layer 2 artifact templates.

---

## Status

✅ **COMPLETE** — All schemas generated and validated

- **Current version:** `schemas-v0.2.0` (2025-11-05)
- **Total schemas:** 26 JSON Schema files (Draft 2020-12)
  - 20 artifact schemas (from Layer 2 templates)
  - 6 system schemas (Cold SoT manifests, Hot manifest, envelope)
- **Source:** Layer 2 artifact templates in `02-dictionary/artifacts/*.md`
- **Validation:** All schemas pass JSON Schema Draft 2020-12 meta-validation
- **Published:** Canonical URLs at `https://questfoundry.liesdonk.nl/schemas/`

See [CHANGELOG.md](./CHANGELOG.md) for version history.

---

## Schema Generation Process

### 1. Source Material

Each enriched template contains **HTML constraint comments** with field metadata:

```html
<!-- Field: Status | Type: enum | Required: yes | Taxonomy: Hook Status Lifecycle (taxonomies.md §2) -->
<!-- Allowed values: proposed | accepted | in-progress | resolved | canonized | deferred | rejected -->
```

### 2. Extraction Pattern

For each field, extract:

- **Field name** — Property name in schema
- **Type** — JSON Schema type (string, enum, array, object, etc.)
- **Required** — Boolean (yes/no)
- **Format** — Pattern, date format, or reference format
- **Enum values** — For controlled vocabularies
- **Validation rules** — Length, pattern, cross-field constraints
- **Description** — Human-readable explanation from prose

### 3. Output Format

JSON Schema Draft 2020-12 with:

- `$schema`, `$id`, `title`, `description`
- `type: "object"`
- `properties: {}` — All fields
- `required: []` — Required field names
- `definitions: {}` — Reusable types (role names, dates, IDs)

---

## Schema Template

See `SCHEMA_TEMPLATE.json` for the standard pattern.

See `EXTRACTION_GUIDE.md` for step-by-step extraction instructions.

See `hook_card.schema.json` for a complete reference example.

---

## File Naming Convention

**Pattern:** `{artifact_name}.schema.json`

**Examples:**

- `hook_card.schema.json`
- `tu_brief.schema.json`
- `gatecheck_report.schema.json`
- `canon_pack.schema.json`
- etc.

---

## Schema Index (26 Total)

### Artifact Schemas (20)

**Core Workflow:**

- ✅ `hook_card.schema.json` — Hook tracking and routing
- ✅ `tu_brief.schema.json` — Trace Unit (work unit) tracking

**Creation & Content:**

- ✅ `canon_pack.schema.json` — Canonical story facts
- ✅ `codex_entry.schema.json` — Player-facing encyclopedia
- ✅ `style_addendum.schema.json` — Style and voice guidelines
- ✅ `edit_notes.schema.json` — Editorial feedback

**Research & Planning:**

- ✅ `research_memo.schema.json` — Factual research documentation
- ✅ `shotlist.schema.json` — Individual illustration specs
- ✅ `cuelist.schema.json` — Audio cue specifications
- ✅ `art_plan.schema.json` — Illustration planning
- ✅ `audio_plan.schema.json` — Audio production planning

**Localization:**

- ✅ `language_pack.schema.json` — Localization translations
- ✅ `register_map.schema.json` — Language register specs

**Quality & Export:**

- ✅ `gatecheck_report.schema.json` — Quality validation reports
- ✅ `view_log.schema.json` — Export metadata
- ✅ `front_matter.schema.json` — Book front matter
- ✅ `pn_playtest_notes.schema.json` — Player-Narrator feedback

**Project Metadata:**

- ✅ `project_metadata.schema.json` — Project configuration
- ✅ `art_manifest.schema.json` — Complete art asset inventory
- ✅ `style_manifest.schema.json` — Typography and style settings

### System Schemas (6)

**Cold Source of Truth:**

- ✅ `cold_manifest.schema.json` — Top-level file index with SHA-256 hashes
- ✅ `cold_book.schema.json` — Story structure and bibliographic metadata
- ✅ `cold_art_manifest.schema.json` — Asset mappings with provenance
- ✅ `cold_fonts.schema.json` — Font file mappings
- ✅ `cold_build_lock.schema.json` — Tool version pinning

**Hot Discovery Space:**

- ✅ `hot_manifest.schema.json` — Master index for Hot discovery space

**Protocol:**

- ✅ `envelope.schema.json` — Message envelope structure (Layer 4)

---

## Validation

Each schema should:

- ✅ Pass JSON Schema meta-validation
- ✅ Reference taxonomies from Layer 2
- ✅ Include all required fields from enriched template
- ✅ Include all enum values from constraint comments
- ✅ Include format patterns (dates, IDs)
- ✅ Include descriptions from template prose

---

## Usage

Schemas will be used for:

- **Validation tooling** — CLI validators for artifacts
- **API design** — REST/GraphQL endpoint definitions
- **UI generation** — Form builders from schemas
- **Documentation** — Auto-generated field reference

---

## Cross-References

- **Source templates:** `../02-dictionary/artifacts/*.md` (enriched with HTML constraint comments)
- **Taxonomies:** `../02-dictionary/taxonomies.md` (enumerations)
- **Field registry:** `../02-dictionary/field_registry.md` (field catalog)
- **Validation rules:** Embedded in Layer 2 artifact template comments
- **Changelog:** `./CHANGELOG.md` (version history)

---

**Created:** 2025-10-30 **Method:** Automated extraction from enriched Layer 2 templates
