# LLM Prompt for Schema Generation

> **Instructions for cheap coding LLM:** Use this prompt to generate the remaining 16 JSON schemas from enriched Layer 2 templates.

---

## Your Task

Generate JSON Schema (Draft 2020-12) files for each QuestFoundry artifact template.

**Input:** Enriched markdown templates in `../02-dictionary/artifacts/*_ENRICHED.md`

**Output:** JSON Schema files in `03-schemas/{artifact_name}.schema.json`

**Reference:** `hook_card.schema.json` is a complete example — study it first!

---

## Files to Generate (16 remaining)

```
1. tu_brief.schema.json              (from tu_brief_ENRICHED.md)
2. canon_pack.schema.json            (from canon_pack_ENRICHED.md)
3. codex_entry.schema.json           (from codex_entry_ENRICHED.md)
4. style_addendum.schema.json        (from style_addendum_ENRICHED.md)
5. edit_notes.schema.json            (from edit_notes_ENRICHED.md)
6. research_memo.schema.json         (from research_memo_ENRICHED.md)
7. shotlist.schema.json              (from shotlist_ENRICHED.md)
8. cuelist.schema.json               (from cuelist_ENRICHED.md)
9. art_plan.schema.json              (from art_plan_ENRICHED.md)
10. audio_plan.schema.json           (from audio_plan_ENRICHED.md)
11. language_pack.schema.json        (from language_pack_ENRICHED.md)
12. register_map.schema.json         (from register_map_ENRICHED.md)
13. gatecheck_report.schema.json     (from gatecheck_report_ENRICHED.md)
14. view_log.schema.json             (from view_log_ENRICHED.md)
15. front_matter.schema.json         (from front_matter_ENRICHED.md)
16. pn_playtest_notes.schema.json    (from pn_playtest_notes_ENRICHED.md)
```

---

## Step-by-Step Process

### Step 1: Read the Source Template

Open `../02-dictionary/artifacts/{artifact_name}_ENRICHED.md`

Extract title and description from the header:
```markdown
# {Artifact Name} — {Description} (Layer 2, Enriched)

> **Use:** {Usage description}
```

### Step 2: Scan for HTML Constraint Comments

Find all comments that start with `<!-- Field:`

Example:
```html
<!-- Field: Status | Type: enum | Required: yes | Taxonomy: Hook Status Lifecycle -->
<!-- Allowed values: proposed | accepted | in-progress | resolved | canonized | deferred | rejected -->
```

### Step 3: Convert Each Field to JSON Schema Property

Use this mapping table:

| Template Metadata | JSON Schema |
|-------------------|-------------|
| `Field: Status` | `"status": {...}` |
| `Type: string` | `"type": "string"` |
| `Type: enum` | `"type": "string"` + `"enum": [...]` |
| `Type: enum-list` | `"type": "array"` + `"items": {"enum": [...]}` |
| `Type: markdown` | `"type": "string"` |
| `Type: date` | `"type": "string"` + `"format": "date"` |
| `Required: yes` | Add to `"required": []` |
| `Optional` | Do NOT add to required |
| `Format: YYYY-MM-DD` | `"pattern": "^\\d{4}-\\d{2}-\\d{2}$"` |
| `Allowed values: a \| b \| c` | `"enum": ["a", "b", "c"]` |

### Step 4: Build the Schema File

Use this exact structure:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://questfoundry.example.com/schemas/{artifact}.schema.json",
  "title": "{Artifact Display Name}",
  "description": "Generated from 02-dictionary/artifacts/{artifact}_ENRICHED.md. {Usage description}",
  "type": "object",

  "properties": {
    // Add all fields here, grouped by section
  },

  "required": [
    // List all required field names
  ],

  "definitions": {
    // Copy from hook_card.schema.json:
    // - role_name
    // - date_string
    // - quality_bar
    // - loop_name
    // - deferral_tag
  }
}
```

### Step 5: Group Properties by Section

**For artifacts with many sections** (10+ fields), use nested structure:

```json
"properties": {
  "header": {
    "type": "object",
    "properties": {
      "id": {...},
      "status": {...}
    },
    "required": ["id", "status"]
  },
  "section_2": {
    "type": "object",
    "properties": {...}
  }
}
```

**For simple artifacts** (< 10 fields), use flat structure:

```json
"properties": {
  "id": {...},
  "status": {...},
  "summary": {...}
}
```

### Step 6: Copy Reusable Definitions

**Always include** the `definitions` section from `hook_card.schema.json`:

```json
"definitions": {
  "role_name": {
    "type": "string",
    "enum": ["SR", "GK", "PW", "SS", "ST", "LW", "CC", "AD", "IL", "AuD", "AuP", "TR", "BB", "PN", "RS"]
  },
  "date_string": {
    "type": "string",
    "format": "date",
    "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
  },
  "quality_bar": {
    "type": "string",
    "enum": ["Integrity", "Reachability", "Nonlinearity", "Gateways", "Style", "Determinism", "Presentation", "Accessibility"]
  },
  "loop_name": {
    "type": "string",
    "enum": ["Story Spark", "Hook Harvest", "Lore Deepening", "Codex Expansion", "Style Tune-up", "Art Touch-up", "Audio Pass", "Translation Pass", "Binding Run", "Narration Dry-Run", "Gatecheck", "Post-Mortem", "Archive Snapshot"]
  },
  "deferral_tag": {
    "type": "string",
    "enum": ["deferred:art", "deferred:audio", "deferred:translation", "deferred:research"]
  }
}
```

### Step 7: Validate JSON Syntax

Before saving, check:
- [ ] Valid JSON (no trailing commas, proper quotes)
- [ ] All brackets/braces matched
- [ ] All enum arrays properly formatted
- [ ] No typos in enum values (match template exactly)

---

## Common Patterns Quick Reference

### Pattern 1: Enum Field

**Template:**
```html
<!-- Field: Status | Type: enum | Required: yes -->
<!-- Allowed values: draft | review | published -->
```

**Schema:**
```json
"status": {
  "type": "string",
  "description": "Current artifact status",
  "enum": ["draft", "review", "published"]
}
```

### Pattern 2: Space-Separated List

**Template:**
```html
<!-- Field: Tags | Type: enum-list | Optional -->
<!-- Format: Space-separated -->
<!-- Allowed values: tag1 | tag2 | tag3 -->
```

**Schema:**
```json
"tags": {
  "type": "array",
  "description": "Space-separated tags",
  "items": {
    "type": "string",
    "enum": ["tag1", "tag2", "tag3"]
  },
  "uniqueItems": true
}
```

### Pattern 3: Date Field

**Template:**
```html
<!-- Field: Edited | Type: date | Format: YYYY-MM-DD -->
```

**Schema:**
```json
"edited": {
  "$ref": "#/definitions/date_string"
}
```

### Pattern 4: ID with Pattern

**Template:**
```html
<!-- Field: ID | Format: TU-YYYY-MM-DD-XX99 -->
```

**Schema:**
```json
"id": {
  "type": "string",
  "description": "TU Brief unique identifier",
  "pattern": "^TU-\\d{4}-\\d{2}-\\d{2}-[A-Z]{2,4}\\d{2}$"
}
```

### Pattern 5: Role Field

**Template:**
```html
<!-- Field: Owner | Type: role-name | Required: yes -->
```

**Schema:**
```json
"owner": {
  "$ref": "#/definitions/role_name",
  "description": "Responsible role"
}
```

### Pattern 6: Quality Bars

**Template:**
```html
<!-- Field: Bars | Type: enum-list | Taxonomy: Quality Bar Categories -->
```

**Schema:**
```json
"bars": {
  "type": "array",
  "items": {
    "$ref": "#/definitions/quality_bar"
  },
  "minItems": 1
}
```

### Pattern 7: Markdown Text

**Template:**
```html
<!-- Field: Summary | Type: markdown | Length: 1-3 lines -->
```

**Schema:**
```json
"summary": {
  "type": "string",
  "description": "Brief summary (1-3 lines)",
  "minLength": 10,
  "maxLength": 240
}
```

---

## What to Include

✅ **DO include:**
- All fields with `<!-- Field:` comments
- All enum values listed in templates
- Required vs optional status
- Format patterns for IDs/dates
- Descriptions from template prose
- Validation constraints (min/max)

❌ **DO NOT include:**
- Example values in `<angle brackets>`
- Section headers as properties
- Human validation notes
- Comments meant for reviewers

---

## Quality Checklist

Before considering a schema complete:

- [ ] Valid JSON (passes `jq .` test)
- [ ] Has all required header fields: `$schema`, `$id`, `title`, `description`
- [ ] All required fields listed in `required` array
- [ ] All enum fields have complete value lists from template
- [ ] Pattern constraints match template formats exactly
- [ ] Definitions section included
- [ ] No typos in enum values (compare to template carefully)
- [ ] File saved with correct name: `{artifact_name}.schema.json`

---

## Example Workflow

```bash
# 1. Read the enriched template
cat ../02-dictionary/artifacts/tu_brief_ENRICHED.md

# 2. Extract constraint comments (look for <!-- Field: patterns)
grep -A 2 "<!-- Field:" ../02-dictionary/artifacts/tu_brief_ENRICHED.md

# 3. Create schema file starting from SCHEMA_TEMPLATE.json
cp SCHEMA_TEMPLATE.json tu_brief.schema.json

# 4. Fill in properties from constraint comments

# 5. Validate JSON syntax
jq . tu_brief.schema.json

# 6. Compare to hook_card.schema.json for structure consistency
```

---

## Priority Order (Start Here)

Generate schemas in this order for efficiency:

**Tier 1 (Simple, good learning):**
1. `front_matter.schema.json` — Only 9 fields
2. `edit_notes.schema.json` — ~15 fields, straightforward
3. `shotlist.schema.json` — ~15 fields, table structure
4. `cuelist.schema.json` — ~15 fields, similar to shotlist

**Tier 2 (Medium complexity):**
5. `tu_brief.schema.json` — Core workflow artifact
6. `research_memo.schema.json` — ~20 fields
7. `style_addendum.schema.json` — ~23 fields
8. `codex_entry.schema.json` — ~29 fields
9. `pn_playtest_notes.schema.json` — ~18 fields

**Tier 3 (Complex):**
10. `gatecheck_report.schema.json` — Table structure
11. `view_log.schema.json` — Multiple sections
12. `register_map.schema.json` — ~30 fields
13. `audio_plan.schema.json` — ~28 fields
14. `language_pack.schema.json` — ~25 fields
15. `canon_pack.schema.json` — 34 fields, Hot/Cold split
16. `art_plan.schema.json` — 36 fields, most complex

---

## Getting Help

- **Stuck on a pattern?** Check `EXTRACTION_GUIDE.md` for detailed examples
- **Need structure guidance?** Look at `hook_card.schema.json` (complete reference)
- **JSON syntax errors?** Use `jq .` to find and fix issues
- **Unsure about enum values?** Copy EXACTLY from template comments (including spelling/capitalization)

---

## Success Criteria

You've successfully completed the task when:

1. All 16 schema files created in `03-schemas/`
2. Each file is valid JSON
3. Each file follows the structure pattern from `hook_card.schema.json`
4. All enum values match templates exactly
5. All required fields marked in `required` array
6. Definitions section included in each file

---

**Ready to start?** Begin with `front_matter.schema.json` (simplest) and work through the tiers!
