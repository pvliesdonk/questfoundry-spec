# Layer 3 — JSON Schemas (Generated from Layer 2)

> **Purpose:** Machine-readable schemas derived from enriched Layer 2 artifact templates.

---

## Status

🚧 **IN PROGRESS** — Schema generation from enriched templates

- **Source:** 17 enriched artifact templates in `02-dictionary/artifacts/*_ENRICHED.md`
- **Target:** 17 JSON Schema files (Draft 2020-12)
- **Method:** Extract constraints from HTML comments in enriched templates

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

## Schema Index (17 Total)

### Core Workflow (2)

- [ ] `hook_card.schema.json` — ✅ REFERENCE EXAMPLE
- [ ] `tu_brief.schema.json`

### Creation & Content (4)

- [ ] `canon_pack.schema.json`
- [ ] `codex_entry.schema.json`
- [ ] `style_addendum.schema.json`
- [ ] `edit_notes.schema.json`

### Research & Planning (5)

- [ ] `research_memo.schema.json`
- [ ] `shotlist.schema.json`
- [ ] `cuelist.schema.json`
- [ ] `art_plan.schema.json`
- [ ] `audio_plan.schema.json`

### Localization (2)

- [ ] `language_pack.schema.json`
- [ ] `register_map.schema.json`

### Quality & Export (4)

- [ ] `gatecheck_report.schema.json`
- [ ] `view_log.schema.json`
- [ ] `front_matter.schema.json`
- [ ] `pn_playtest_notes.schema.json`

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

- **Source templates:** `../02-dictionary/artifacts/*_ENRICHED.md`
- **Taxonomies:** `../02-dictionary/taxonomies.md` (enumerations)
- **Field registry:** `../02-dictionary/field_registry.md` (field catalog)
- **Validation rules:** Embedded in enriched template comments

---

**Created:** 2025-10-30 **Method:** Automated extraction from enriched Layer 2 templates
