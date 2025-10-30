# Phase 3: Artifacts Refinement Plan

> **Status:** 🚧 **In Progress**
>
> Created: 2025-10-29
>
> Enrich all 17 artifact templates with inline field constraints, validation rules, and reference tables from field_registry.md.

---

## Goal

Transform artifact templates from **human-readable guides** into **machine-checkable specifications** while maintaining readability and usability.

**What "enriched" means:**

- Every field has inline constraints (type, optionality, allowed values)
- Taxonomy references are explicit (links to taxonomies.md sections)
- Validation rules are documented as comments
- Common errors have prevention guidance
- Field tables show quick reference for complex sections

---

## Enrichment Strategy

### 1. Add Field Constraint Comments

For each field in a template section, add inline comments showing:

```markdown
## Section Name

<!-- Field: field_name | Type: string | Required: yes | Format: PREFIX-YYYYMMDD-seq -->
<!-- Taxonomy: Hook Types (taxonomies.md §1) | Values: narrative|scene|factual|... -->
<!-- Validation: Must be unique across all hooks in Hot -->

<field content>
```

### 2. Add Validation Rule Sections

After template sections, add validation guidance:

```markdown
---

## Validation Rules (for Layer 3 schemas)

**Field-level:**

- `ID`: Must match format `HK-YYYYMMDD-\d{2,3}`, unique across all hook cards
- `Type`: Must be one of 13 values from taxonomies.md §1
- `Status`: Must follow lifecycle transitions (taxonomies.md §2)

**Cross-field:**

- If `Blocking? = yes`, then `Bars affected` must include at least one bar
- If `Status = deferred`, then §6 Dormancy section must be filled
- If `Status = rejected`, then §8 Resolution must include rejection reason

**Cross-artifact:**

- `TU` ID must reference an existing TU Brief
- `Related hooks` IDs must reference existing Hook Cards
- `Locations` paths must resolve to valid anchors (checked by Binder)
```

### 3. Add Field Reference Tables

For complex artifacts with many fields, add quick-reference tables:

```markdown
## Field Reference

| Section | Field          | Type   | Required | Taxonomy/Constraint         |
| ------- | -------------- | ------ | -------- | --------------------------- |
| Header  | ID             | string | yes      | Format: HK-YYYYMMDD-seq     |
| Header  | Status         | enum   | yes      | Hook Status Lifecycle (§2)  |
| §1      | Type (primary) | enum   | yes      | Hook Types (§1) - 13 values |
| ...     | ...            | ...    | ...      | ...                         |
```

### 4. Add Common Error Prevention

Document frequent mistakes and how to avoid them:

```markdown
## Common Errors

**❌ Meta phrasing in Player-Safe Summary**

- Wrong: "Option locked: missing reputation flag"
- Right: "The guard eyes you coldly. 'Not today.'"

**❌ Hook type too broad**

- Wrong: `canon` for everything
- Right: Use narrowest type (scene over narrative, taxonomy over canon)

**❌ Missing acceptance criteria**

- Wrong: "Fix the gate"
- Right: "Gate refusal is diegetic (Gateways green); labels contrastive (Style green)"
```

---

## Artifact Priority Order

Enrich in this order (most-used first):

### Tier 1: Core Workflow (High Frequency)

1. **hook_card.md** — Most frequently created, drives all follow-up work
2. **tu_brief.md** — Every work session starts here
3. **gatecheck_report.md** — Every TU ends here

### Tier 2: Content Creation (Medium Frequency)

4. **canon_pack.md** — Complex, high field count (34 fields)
5. **codex_entry.md** — Player-facing, localization-heavy
6. **style_addendum.md** — Patterns reused across slices
7. **research_memo.md** — Evidence-based decision making

### Tier 3: Asset Planning (Optional Tracks)

8. **art_plan.md** — Highest field count (36 fields)
9. **audio_plan.md** — Similar to art_plan
10. **shotlist.md** — Index for art plans
11. **cuelist.md** — Index for audio plans

### Tier 4: Localization & Export (Specialized)

12. **language_pack.md** — Translation deliverable
13. **register_map.md** — Localization reference
14. **view_log.md** — Export record
15. **front_matter.md** — Player-facing header

### Tier 5: Operational (Supporting)

16. **edit_notes.md** — Line-level fixes
17. **pn_playtest_notes.md** — Dry-run feedback

---

## Enrichment Approach Per Artifact

For each artifact:

1. **Read current template** — Understand structure
2. **Cross-reference field_registry.md** — Find all fields used
3. **Add inline constraints** — Type, optionality, format
4. **Link to taxonomies** — Explicit §references
5. **Add validation rules section** — Field-level, cross-field, cross-artifact
6. **Add common errors** — Prevention guidance
7. **Add field reference table** (if >20 fields) — Quick lookup
8. **Check for new inconsistencies** — Log to LAYER1_CORRECTIONS.md

---

## Validation Rule Categories

Document 3 levels of validation:

### Field-Level Validation

- Type checks (string, enum, date, markdown)
- Format constraints (date: YYYY-MM-DD, ID: PREFIX-YYYYMMDD-seq)
- Allowed values (enums from taxonomies)
- Optionality (required vs optional)
- Length limits (e.g., Player-Safe Summary: 1-3 lines)

### Cross-Field Validation

- Conditional requirements (if X then Y must be filled)
- Mutual exclusivity (can't have both X and Y)
- Dependencies (if status=deferred, need deferral reason)
- Consistency checks (bars listed in §1 must match bars in validation table)

### Cross-Artifact Validation

- Reference integrity (TU ID exists, Hook IDs exist)
- Anchor resolution (paths resolve to actual locations)
- Lineage traces (Canon Pack → Hook Card → TU Brief)
- Taxonomy conformance (values match taxonomies.md)

---

## Expected Inconsistencies to Watch For

Based on Phase 2 findings, watch for:

1. **Hook types** — Templates may still reference old 10-type list
2. **Hook status** — Templates may use `open` instead of `proposed`
3. **Quality Bars** — Templates may list 7 instead of 8 bars
4. **Loop names** — Templates may be missing Hook Harvest or export loops
5. **Deferral tags** — Format inconsistencies (comma vs space-separated)
6. **Research posture** — Colon format `uncorroborated:high` may vary
7. **Role abbreviations** — May be used inconsistently
8. **Anchor formats** — kebab-case policy may not be enforced everywhere

Document all findings in LAYER1_CORRECTIONS.md with new section numbers.

---

## Output Format

Each enriched template will have:

**Header:**

- Original template content (unchanged)
- Status note: "Enriched with Layer 2 constraints (Phase 3)"

**Body Sections:**

- Inline field constraint comments (before each field)
- Original template instructions (preserved)

**Footer:**

- Validation Rules section (new)
- Common Errors section (new)
- Field Reference table (new, if >20 fields)

---

## Success Criteria

Phase 3 is complete when:

- [ ] All 17 artifacts have inline field constraints
- [ ] All taxonomy references are explicit (§links)
- [ ] Validation rules documented (field, cross-field, cross-artifact)
- [ ] Common errors documented for top 10 artifacts
- [ ] Field reference tables added for 5 most complex artifacts
- [ ] All new inconsistencies logged to LAYER1_CORRECTIONS.md
- [ ] Templates remain human-readable (not schema dumps)

---

## Approach Notes

**Readability First:**

- Don't turn templates into schema dumps
- Use HTML comments for constraints (won't render in preview)
- Keep natural language instructions
- Add validation as footer sections, not inline clutter

**Incremental Enrichment:**

- Start with Tier 1 artifacts (high-value)
- Get user feedback on enrichment style
- Adjust approach before enriching all 17

**Machine-Checkable Goal:**

- Layer 3 can parse constraint comments
- Layer 3 can generate JSON schemas from enriched templates
- Layer 3 can validate artifact instances against constraints

---

## Tracking

- [✅] Phase 3 plan created
- [⏳] Tier 1 artifacts (3) — In progress
- [⏳] Tier 2 artifacts (4) — Pending
- [⏳] Tier 3 artifacts (4) — Pending
- [⏳] Tier 4 artifacts (4) — Pending
- [⏳] Tier 5 artifacts (2) — Pending
- [⏳] New inconsistencies logged — Ongoing

---
