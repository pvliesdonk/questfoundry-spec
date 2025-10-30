# Layer 3 Schema Generation — Handoff to Cheap LLM

> **For the human operator:** Instructions for delegating schema generation to a cheaper coding LLM (e.g., GPT-4o-mini, Claude 3.5 Haiku, Llama 3.1 70B).

---

## What's Been Prepared

✅ **Complete template system:**
- `SCHEMA_TEMPLATE.json` — Copy-paste starting point
- `EXTRACTION_GUIDE.md` — Detailed how-to guide
- `LLM_GENERATION_PROMPT.md` — Step-by-step LLM instructions
- `hook_card.schema.json` — Complete reference example

✅ **Source material:**
- 17 enriched templates in `../02-dictionary/artifacts/*_ENRICHED.md`
- Each template has machine-parseable HTML constraint comments

✅ **What you need:**
- 16 more schema files (hook_card already done as example)

---

## How to Delegate This Work

### Option 1: One-Shot Prompt (Recommended)

**Copy-paste this to your cheap LLM:**

```
You are generating JSON Schema files for QuestFoundry artifacts.

CONTEXT:
- Location: 03-schemas/ directory in QuestFoundry repo
- Input files: ../02-dictionary/artifacts/*_ENRICHED.md (17 markdown templates)
- Output: {artifact_name}.schema.json (JSON Schema Draft 2020-12)

COMPLETED ALREADY:
- hook_card.schema.json ✅ (use as reference example)

YOUR TASK:
Generate the remaining 16 schema files by extracting metadata from enriched templates.

INSTRUCTIONS:
1. Read LLM_GENERATION_PROMPT.md for detailed step-by-step process
2. Read EXTRACTION_GUIDE.md for pattern reference
3. Study hook_card.schema.json to understand output format
4. For each of the 16 artifacts, generate a complete JSON Schema

START WITH TIER 1 (simplest):
1. front_matter.schema.json
2. edit_notes.schema.json
3. shotlist.schema.json
4. cuelist.schema.json

RULES:
- Extract ALL fields with <!-- Field: comments from templates
- Match enum values EXACTLY (spelling, capitalization)
- Include the definitions section in every schema (copy from hook_card)
- Validate JSON syntax before marking complete
- File naming: {artifact_name}.schema.json (lowercase, underscores)

VALIDATION CHECKLIST for each schema:
✓ Valid JSON (no syntax errors)
✓ Has $schema, $id, title, description
✓ All required fields in "required" array
✓ All enums have complete value lists
✓ Definitions section included

Output each schema as a separate artifact in a code block with filename.
```

### Option 2: Iterative (Tier by Tier)

Generate in batches, validating each batch before proceeding:

**Batch 1 - Simple (4 files):**
```
Generate these 4 schemas using the instructions in LLM_GENERATION_PROMPT.md:
1. front_matter.schema.json (from front_matter_ENRICHED.md)
2. edit_notes.schema.json (from edit_notes_ENRICHED.md)
3. shotlist.schema.json (from shotlist_ENRICHED.md)
4. cuelist.schema.json (from cuelist_ENRICHED.md)

Provide complete JSON for each file.
```

**Batch 2 - Medium (5 files):**
```
Generate these 5 schemas:
1. tu_brief.schema.json
2. research_memo.schema.json
3. style_addendum.schema.json
4. codex_entry.schema.json
5. pn_playtest_notes.schema.json
```

**Batch 3 - Complex (7 files):**
```
Generate these final 7 schemas:
1. gatecheck_report.schema.json
2. view_log.schema.json
3. register_map.schema.json
4. audio_plan.schema.json
5. language_pack.schema.json
6. canon_pack.schema.json
7. art_plan.schema.json
```

### Option 3: One File at a Time

For maximum control, request each schema individually:

```
Generate {artifact_name}.schema.json from ../02-dictionary/artifacts/{artifact_name}_ENRICHED.md

Follow the instructions in LLM_GENERATION_PROMPT.md.
Use hook_card.schema.json as the reference pattern.

Provide the complete JSON Schema.
```

---

## Validation After LLM Output

For each generated schema file:

### 1. Syntax Check
```bash
# Validate JSON syntax
jq . {artifact_name}.schema.json

# If error, fix and re-run
```

### 2. Completeness Check
```bash
# Count properties (should match field count in enriched template)
jq '.properties | length' {artifact_name}.schema.json

# List required fields
jq '.required[]' {artifact_name}.schema.json

# Verify definitions section exists
jq '.definitions | keys' {artifact_name}.schema.json
```

### 3. Enum Accuracy Check

Manually compare enum values in schema vs. template:

```bash
# Extract enum values from schema
jq '.. | .enum? // empty' {artifact_name}.schema.json

# Compare against enriched template
grep "Allowed values:" ../02-dictionary/artifacts/{artifact_name}_ENRICHED.md
```

### 4. Pattern Validation

Check that ID/date patterns match template specifications:

```bash
# Find all patterns in schema
jq '.. | .pattern? // empty' {artifact_name}.schema.json
```

---

## Common LLM Errors to Watch For

🔴 **Typos in enum values**
- Schema: `"canonised"` ❌
- Template: `"canonized"` ✓
- Fix: Compare carefully, match template exactly

🔴 **Missing definitions section**
- Fix: Copy entire definitions block from hook_card.schema.json

🔴 **Wrong JSON Schema draft version**
- Should be: `"$schema": "https://json-schema.org/draft/2020-12/schema"`
- Not: draft-07 or draft-04

🔴 **Incorrect required array**
- Only include fields marked `Required: yes` in template
- Don't include optional fields

🔴 **Trailing commas in JSON**
- Invalid: `{"a": 1, "b": 2,}` ❌
- Valid: `{"a": 1, "b": 2}` ✓

🔴 **Using nested enums for space-separated lists**
- Template says "space-separated" → use array, not nested format

---

## Verification Script

Create a simple validation script:

```bash
#!/bin/bash
# validate_schemas.sh

echo "Validating all schemas in 03-schemas/"

for schema in *.schema.json; do
  echo -n "Checking $schema... "

  if jq empty "$schema" 2>/dev/null; then
    echo "✓ Valid JSON"
  else
    echo "✗ INVALID JSON"
  fi
done

echo ""
echo "Schema count: $(ls -1 *.schema.json | wc -l) / 17"
```

Run after each batch:
```bash
cd 03-schemas
chmod +x validate_schemas.sh
./validate_schemas.sh
```

---

## Expected Timeline

**Using cheap LLM with batching:**
- Batch 1 (4 simple): ~10-15 minutes (including validation)
- Batch 2 (5 medium): ~20-30 minutes
- Batch 3 (7 complex): ~30-45 minutes
- **Total: ~60-90 minutes** (mostly validation time)

**Cost estimate:**
- Input tokens: ~200K (all enriched templates + instructions)
- Output tokens: ~150K (16 complete schemas)
- **Total cost:** $0.50 - $2.00 depending on LLM provider

---

## Success Criteria

✅ All 17 schema files present in `03-schemas/`
✅ Each file is valid JSON (passes `jq .` test)
✅ Each file follows hook_card.schema.json structure pattern
✅ All enum values match templates exactly
✅ All required fields marked in required array
✅ Definitions section included in each file
✅ No TODO or placeholder values

---

## What to Do When Complete

1. Run final validation: `./validate_schemas.sh`
2. Commit all schemas: `git add 03-schemas/*.schema.json`
3. Create PR with title: "feat(layer3): Generate all 17 JSON schemas from enriched templates"
4. Move to next phase: Validation tooling or Layer 4 protocol

---

## Files for LLM Context

**Provide these to the LLM:**
1. `LLM_GENERATION_PROMPT.md` — Primary instructions
2. `EXTRACTION_GUIDE.md` — Pattern reference
3. `hook_card.schema.json` — Complete example
4. `SCHEMA_TEMPLATE.json` — Starting template

**LLM will read from:**
- `../02-dictionary/artifacts/*_ENRICHED.md` (17 files)

**LLM will output:**
- 16 JSON schema files

---

## Quick Start Command

```bash
# Navigate to schemas directory
cd 03-schemas

# Provide context files to your LLM:
cat LLM_GENERATION_PROMPT.md
cat hook_card.schema.json

# Then give the one-shot prompt from Option 1 above
```

---

**Ready to delegate?** Use Option 1 (one-shot) for speed, or Option 2 (batched) for quality control.
