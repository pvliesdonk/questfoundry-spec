# Schema Extraction Guide — How to Generate JSON Schemas from Enriched Templates

> **Purpose:** Step-by-step instructions for extracting JSON schemas from Layer 2 enriched artifact templates.

---

## Overview

Each enriched template (`*_ENRICHED.md`) contains **HTML constraint comments** that define field metadata. Your job is to transform these comments into a valid JSON Schema (Draft 2020-12).

---

## Step 1: Identify the Source Template

**Input file pattern:** `02-dictionary/artifacts/{artifact_name}_ENRICHED.md`

**Output file name:** `03-schemas/{artifact_name}.schema.json`

**Example:**
- Input: `02-dictionary/artifacts/hook_card_ENRICHED.md`
- Output: `03-schemas/hook_card.schema.json`

---

## Step 2: Extract Metadata from File Header

Look at the top of the enriched template for:

```markdown
# {Artifact Name} — {Short Description} (Layer 2, Enriched)

> **Use:** {Usage description}
```

**Extract:**
- `title` = Artifact Name (e.g., "Hook Card")
- `description` = Short description + usage (combine both lines)

---

## Step 3: Scan for HTML Constraint Comments

Look for comments in this format:

```html
<!-- Field: {field_name} | Type: {type} | Required: {yes/no} | ... -->
<!-- Allowed values: value1 | value2 | value3 -->
<!-- Validation: {constraint} -->
```

**Pattern Recognition:**

| Comment Fragment | Maps To Schema |
|------------------|----------------|
| `Field: ID` | Property name: `"id"` |
| `Type: string` | `"type": "string"` |
| `Type: enum` | `"type": "string"` + `"enum": [...]` |
| `Type: enum-list` | `"type": "array"` + `"items": {"enum": [...]}` |
| `Type: markdown` | `"type": "string"` |
| `Type: date` | `"type": "string"` + `"format": "date"` |
| `Required: yes` | Add to `"required": []` array |
| `Optional` | Do NOT add to required |
| `Format: YYYY-MM-DD` | `"format": "date"` + `"pattern": "^\\d{4}-\\d{2}-\\d{2}$"` |
| `Format: HK-YYYYMMDD-seq` | `"pattern": "^HK-\\d{8}-\\d{2,3}$"` |
| `Allowed values: a \| b \| c` | `"enum": ["a", "b", "c"]` |
| `Taxonomy: Hook Types` | Add reference comment to description |
| `Length: 1-3 lines` | `"minLength": 1` (estimate ~80 chars/line) |
| `Min: 1 criterion` | `"minItems": 1` |

---

## Step 4: Group Fields by Section

Enriched templates have sections marked by `##` headers:

```markdown
## Header
<!-- constraints here -->

## 1) Classification
<!-- constraints here -->

## 2) Player-Safe Summary
<!-- constraints here -->
```

**Schema Structure Options:**

**Option A: Flat (all fields at root level)**
```json
{
  "properties": {
    "id": {...},
    "status": {...},
    "type_primary": {...},
    "player_safe_summary": {...}
  }
}
```

**Option B: Nested (group by section)** ⭐ Recommended
```json
{
  "properties": {
    "header": {
      "type": "object",
      "properties": {
        "id": {...},
        "status": {...}
      }
    },
    "classification": {
      "type": "object",
      "properties": {
        "type_primary": {...},
        "bars_affected": {...}
      }
    }
  }
}
```

Use **Option B** for complex artifacts with multiple sections.
Use **Option A** for simple artifacts with fewer than 10 fields.

---

## Step 5: Build the Schema Structure

### 5.1 Schema Header

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://questfoundry.example.com/schemas/{artifact}.schema.json",
  "title": "{Artifact Display Name}",
  "description": "Generated from 02-dictionary/artifacts/{artifact}_ENRICHED.md. {Usage description}",
  "type": "object"
}
```

### 5.2 Add Properties

For each field found in HTML comments:

```json
"properties": {
  "{field_name}": {
    "type": "{json_type}",
    "description": "{human_description}",
    // Add constraints based on comment metadata
  }
}
```

### 5.3 Add Required Array

List all fields marked `Required: yes`:

```json
"required": ["id", "status", "type_primary", "bars_affected"]
```

### 5.4 Add Definitions

For reusable types (used across multiple artifacts):

```json
"definitions": {
  "role_name": {
    "type": "string",
    "enum": ["SR", "GK", "PW", "SS", "ST", "LW", "CC", "AD", "IL", "AuD", "AuP", "TR", "BB", "PN", "RS"]
  },
  "quality_bar": {
    "type": "string",
    "enum": ["Integrity", "Reachability", "Nonlinearity", "Gateways", "Style", "Determinism", "Presentation", "Accessibility"]
  },
  "loop_name": {
    "type": "string",
    "enum": ["Story Spark", "Hook Harvest", "Lore Deepening", "Codex Expansion", "Style Tune-up", "Art Touch-up", "Audio Pass", "Translation Pass", "Binding Run", "Narration Dry-Run", "Gatecheck", "Post-Mortem", "Archive Snapshot"]
  }
}
```

---

## Step 6: Handle Special Cases

### Enum Fields

**Template comment:**
```html
<!-- Field: Status | Type: enum | Required: yes -->
<!-- Allowed values: proposed | accepted | in-progress -->
```

**Schema:**
```json
"status": {
  "type": "string",
  "description": "Current hook status",
  "enum": ["proposed", "accepted", "in-progress"]
}
```

### Enum Lists (Space-Separated)

**Template comment:**
```html
<!-- Field: Deferral tags | Type: deferral-list | Optional -->
<!-- Format: Space-separated list -->
<!-- Allowed values: deferred:art | deferred:audio | deferred:translation | deferred:research -->
```

**Schema:**
```json
"deferral_tags": {
  "type": "array",
  "description": "Space-separated deferral tags",
  "items": {
    "type": "string",
    "enum": ["deferred:art", "deferred:audio", "deferred:translation", "deferred:research"]
  },
  "uniqueItems": true
}
```

### Pattern Constraints

**Template comment:**
```html
<!-- Field: ID | Type: string | Format: HK-YYYYMMDD-seq (seq = 01-999) -->
```

**Schema:**
```json
"id": {
  "type": "string",
  "description": "Hook card unique identifier",
  "pattern": "^HK-\\d{8}-(0[1-9]|[1-9]\\d{1,2})$"
}
```

### Date Fields

**Template comment:**
```html
<!-- Field: Edited | Type: date | Format: YYYY-MM-DD -->
```

**Schema:**
```json
"edited": {
  "type": "string",
  "description": "Last edited date",
  "format": "date",
  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
}
```

### Markdown Fields

**Template comment:**
```html
<!-- Field: Player-Safe Summary | Type: markdown | Required: yes | Length: 1-3 lines -->
<!-- Constraints: No spoilers, no codewords -->
```

**Schema:**
```json
"player_safe_summary": {
  "type": "string",
  "description": "Brief player-facing description (1-3 lines, no spoilers)",
  "minLength": 10,
  "maxLength": 240
}
```

### Optional Fields with Conditions

**Template comment:**
```html
<!-- Field: Fallback | Type: markdown | Required if deferrals set -->
```

**Schema approach:**
Use `dependencies` or custom validation. For simplicity, mark as optional and note in description:

```json
"fallback": {
  "type": "string",
  "description": "Required if deferral_tags are set. Describes what happens without deferred work."
}
```

---

## Step 7: Validate the Schema

Before saving, validate:

1. **Valid JSON** — Use `jq` or `jsonlint`
2. **Valid JSON Schema** — Check against meta-schema
3. **Complete** — All required fields from template included
4. **Accurate** — Enum values match template comments exactly

**CLI validation:**
```bash
# Check valid JSON
jq . hook_card.schema.json

# Validate against JSON Schema meta-schema (if validator available)
ajv validate -s meta-schema.json -d hook_card.schema.json
```

---

## Step 8: Add Cross-References

In the description field, reference:
- Source template path
- Taxonomy sections (e.g., "See taxonomies.md §1 for Hook Types")
- Related schemas (e.g., "References tu_brief.schema.json for TU field")

---

## Common Patterns Quick Reference

| Template Type | JSON Schema Type | Notes |
|---------------|------------------|-------|
| `string` | `"type": "string"` | Plain text |
| `enum` | `"type": "string"` + `"enum"` | Single choice |
| `enum-list` | `"type": "array"` + `"items": {"enum"}` | Multiple choices |
| `markdown` | `"type": "string"` | Rich text (stays as string) |
| `date` | `"type": "string"` + `"format": "date"` | YYYY-MM-DD |
| `role-name` | `"$ref": "#/definitions/role_name"` | Use shared definition |
| `markdown-list` | `"type": "array"` + `"items": {"type": "string"}` | List of items |
| `boolean` | `"type": "boolean"` | true/false |
| `integer` | `"type": "integer"` | Whole numbers |

---

## Example Walkthrough

See `hook_card.schema.json` for a complete reference implementation showing all these patterns in practice.

---

## Tips for Efficiency

1. **Start with SCHEMA_TEMPLATE.json** — Copy and modify
2. **Extract all field names first** — Scan for `<!-- Field:` comments
3. **Build properties incrementally** — One section at a time
4. **Validate often** — Check JSON syntax after each section
5. **Reuse definitions** — Don't duplicate role_name, quality_bar, etc.
6. **Keep descriptions concise** — 1-2 sentences max

---

## What to Skip

**Do NOT extract:**
- `<!-- VALIDATION: -->` comments (these are for human validators, not schema)
- Example values in `<angle brackets>`
- Prose explanations (except for description field)
- Section headers (these are for human readability)

**DO extract:**
- Field names
- Types
- Required/optional status
- Enum values
- Format patterns
- Validation constraints (min/max length, etc.)

---

## Output Checklist

Before marking a schema complete:

- [ ] Valid JSON (no syntax errors)
- [ ] Has `$schema`, `$id`, `title`, `description`
- [ ] All required fields in `required` array
- [ ] All enum fields have complete value lists
- [ ] Pattern constraints match template formats
- [ ] Definitions section included (if reusing types)
- [ ] Description references source template path
- [ ] No typos in enum values (match template exactly)

---

**Ready to generate schemas?** See the LLM prompt file: `LLM_GENERATION_PROMPT.md`
