# Layer 2 Implementation Plan

> **Goal:** Create "Common Language" as human-readable data dictionary bridging Layer 0/1 concepts to Layer 3 schemas
>
> **Scope:** Good coverage without redundancy - depends on L0/L1 for context, focuses on data structures and taxonomies
>
> **Approach:** Hybrid (automated extraction → human review → iteration → finalization)

---

## Proposed Phase Order

### **Phase 1: Taxonomies** 🎯 START HERE

**Why first:** Everything else references these classifications
**Effort:** Medium (extract from L0, consolidate, extend)
**Risk:** Low (mostly exists scattered across L0/1)

### **Phase 2: Field Registry**

**Why second:** Needs taxonomies for enum type definitions
**Effort:** High (parse 17 artifacts, deduplicate, classify)
**Risk:** Medium (requires careful deduplication)

### **Phase 3: Artifacts Refinement**

**Why third:** Now we have taxonomies and fields to reference
**Effort:** Medium (enrich existing 17 templates)
**Risk:** Low (incremental improvements to existing)

### **Phase 4: Validation Rules**

**Why fourth:** Needs fields and taxonomies to express rules
**Effort:** Medium (extract from L0/1 policies)
**Risk:** Medium (needs careful policy interpretation)

### **Phase 5: Relationships**

**Why fifth:** Builds on complete understanding of artifacts
**Effort:** Medium (map flows between artifacts)
**Risk:** Low (mostly documentation of existing flows)

### **Phase 6: Glossary Enhancement**

**Why sixth:** Final polish after all structures defined
**Effort:** Low (augment existing glossary.md)
**Risk:** Low (refinement only)

### **Phase 7: Finalization**

**Why last:** Remove PARKED markers, final consistency check
**Effort:** Low (cleanup and documentation)
**Risk:** Low

---

## Phase 1 Detail: Taxonomies

### Deliverables

**File:** `02-dictionary/taxonomies.md`

**Sections to create:**

1. **Hook Types** (extract from `00-north-star/HOOKS.md` + `01-roles/templates/hook_card.md`)
   - `narrative` - Story entities, locations, stakes, topology
   - `scene` - Scene-level details, traits, props, micro-events
   - `factual` - Real-world claims to verify
   - `taxonomy` - Coverage gaps, cross-ref needs
   - `style/pn` - Voice, register, phrasing patterns
   - `translation` - Localization needs
   - `art` - Visual requirements
   - `audio` - Sound requirements
   - `binder/nav` - Export and navigation issues
   - `accessibility` - A11y concerns

2. **Hook Status Lifecycle**
   - `proposed` → `accepted` → `in-progress` → `resolved`
   - `proposed` → `deferred` (with reason)
   - `proposed` → `rejected` (with reason)
   - `resolved` → `canonized` (appears in Cold)

3. **TU Types & Loop Alignment** (extract from `00-north-star/LOOPS/`)
   - Story Spark → topology/structure TUs
   - Hook Harvest → triage TUs
   - Lore Deepening → canon TUs
   - Codex Expansion → taxonomy/terminology TUs
   - Style Tune-up → voice/register TUs
   - Art Touch-up → visual planning TUs
   - Audio Pass → sound planning TUs
   - Translation Pass → localization TUs
   - Binding Run → export TUs
   - Narration Dry-Run → UX testing TUs

4. **Gate Types** (extract from `00-north-star/PN_PRINCIPLES.md`)
   - `token` - Physical object possession
   - `reputation` - Social standing thresholds
   - `knowledge` - Information discovered
   - `physical` - Location, capability, tool access
   - `temporal` - Time-based constraints
   - `composite` - Multiple conditions (AND/OR)

5. **Quality Bar Categories** (extract from `00-north-star/QUALITY_BARS.md`)
   - **Integrity** - Anchors resolve, no orphans, IDs unique
   - **Reachability** - Keystones accessible, no unreachable sections
   - **Nonlinearity** - Hubs/loops matter, choices non-trivial
   - **Gateways** - Fair paths exist, diegetic enforcement
   - **Style** - Voice consistent, register appropriate, motifs tracked
   - **Determinism** - Reproducibility logged when promised
   - **Presentation** - No spoilers/meta on surfaces, accessibility baseline

6. **Artifact Status Types** (extract from artifact templates)
   - `draft` - Initial creation in Hot
   - `review` - Submitted for gatecheck
   - `blocked` - Failed bars, needs remediation
   - `approved` - Passed bars, ready for Cold
   - `merged` - Landed in Cold snapshot
   - `published` - Included in exported view

7. **Deferral Types** (extract from `01-roles/interfaces/dormancy_signals.md`)
   - `deferred:art` - Visual work postponed
   - `deferred:audio` - Sound work postponed
   - `deferred:translation` - Localization postponed
   - `deferred:research` - Fact-checking postponed

8. **Research Posture Levels** (extract from `01-roles/briefs/researcher.md`)
   - `uncorroborated:low` - Minor claim, low player impact
   - `uncorroborated:medium` - Significant claim, moderate impact
   - `uncorroborated:high` - Critical claim, high impact (requires immediate attention)

9. **Role Dormancy States** (extract from `01-roles/interfaces/dormancy_signals.md`)
   - `always-on` - Showrunner, Gatekeeper
   - `default-on` - Plotwright, Scene Smith, Lore Weaver, Codex Curator, Style Lead
   - `optional-dormant` - Researcher, Art Director, Illustrator, Audio Director, Audio Producer, Translator
   - `downstream` - Book Binder, Player-Narrator

10. **Loop Types** (create classification)
    - **Discovery loops** (Hot-primary): Story Spark, Hook Harvest, Lore Deepening
    - **Refinement loops** (Hot→Cold): Style Tune-up, Codex Expansion
    - **Asset loops** (optional): Art Touch-up, Audio Pass, Translation Pass
    - **Export loops** (Cold-only): Binding Run, Narration Dry-Run
    - **Validation loops** (cross-cutting): Gatekeeper checks at all stages

### Extraction Strategy

**Automated extraction (I do):**

```bash
# Extract hook types from HOOKS.md
grep -A5 "hook types" 00-north-star/HOOKS.md

# Extract Quality Bars
grep -A3 "^###" 00-north-star/QUALITY_BARS.md

# Extract loop names
ls 00-north-star/LOOPS/*.md | xargs -n1 basename | sed 's/\.md//'

# Extract status enums from templates
grep -rh "Status:" 02-dictionary/artifacts/ | sort -u

# Extract deferral tags
grep -rh "deferred:" 01-roles/
```

**Manual consolidation (you review):**

- Verify completeness of each taxonomy
- Add missing values I didn't catch
- Clarify decision criteria for choosing values
- Ensure terminology is consistent with L0/L1

### Template Structure (for each taxonomy)

```markdown
## Taxonomy: [Name]

**Purpose:** [Why this classification exists - 1 sentence]

**Defined in Layer 0/1:** [References to source documents]

**Values:**

- `value1` — [Description: when to use, what it means]
- `value2` — [Description: when to use, what it means]
- ...

**Usage:**

- Appears in: [Which artifacts use this taxonomy]
- Used by: [Which roles make these classifications]
- Examples: [Player-safe examples]

**Decision Criteria:** [How to choose between values - if not obvious]

**Validation:**

- Must be one of the listed values
- [Any other constraints]
```

---

## Phase 2-7 Outlines (Brief)

### Phase 2: Field Registry

**File:** `02-dictionary/fields.md`

- Parse all 17 artifacts for field names
- Classify by data type (enum, string, date, reference, markdown)
- Map to taxonomies (enums reference Phase 1)
- Mark Hot vs Cold safety
- Define constraints and formats

### Phase 3: Artifacts Refinement

**Files:** All `02-dictionary/artifacts/*.md`

- Add field type annotations
- Reference taxonomies from Phase 1
- Add more examples
- Clarify Hot vs Cold fields
- Enhance descriptions

### Phase 4: Validation Rules

**File:** `02-dictionary/validation.md`

- Cross-field rules (if X then Y must be set)
- Reference integrity (IDs must exist)
- Spoiler safety checks
- Completeness requirements
- Naming conventions

### Phase 5: Relationships

**File:** `02-dictionary/relationships.md`

- Artifact flow diagrams (TU → Hooks, Canon → Codex)
- Cardinality (one-to-many, many-to-many)
- Required vs optional relationships
- Lifecycle connections (TU → Snapshot → View)

### Phase 6: Glossary Enhancement

**File:** `02-dictionary/glossary.md`

- Add missing terms discovered in Phases 1-5
- Cross-reference to taxonomies
- Ensure consistency with artifacts
- Add usage examples

### Phase 7: Finalization

- Remove all PARKED markers
- Update all READMEs
- Cross-check all internal references
- Update root README to show Layer 2 complete
- Create Layer 2 → Layer 3 mapping guide

---

## Success Criteria (per Phase)

**Phase 1 (Taxonomies):** ✅ When:

- All 10 taxonomy categories documented
- Each taxonomy has clear values and usage
- References to Layer 0/1 provided
- Humans can classify items without guessing
- Layer 3 schema designers have clear enum definitions

**Phase 2 (Fields):** ✅ When:

- All fields from 17 artifacts cataloged
- Data types assigned
- Hot vs Cold marked
- Constraints documented
- Layer 3 can generate schema fields directly

**Phase 3 (Artifacts):** ✅ When:

- All templates enriched with type info
- Examples provided for each
- Hot/Cold boundaries clear
- No ambiguous field meanings

**Phase 4 (Validation):** ✅ When:

- All critical rules documented
- Player-safety checks specified
- Cross-field constraints listed
- Layer 3 can implement validators

**Phase 5 (Relationships):** ✅ When:

- Artifact flows documented
- Cardinality clear
- Lifecycle connections mapped
- Layer 4 can design protocol based on this

**Phase 6 (Glossary):** ✅ When:

- No undefined terms in Layer 2
- Cross-references complete
- Consistent with L0/L1

**Phase 7 (Final):** ✅ When:

- No PARKED markers remain
- All references resolve
- Layer 2 feels "done enough"
- Ready to start Layer 3

---

## Timeline Estimate

- **Phase 1 (Taxonomies):** 2-3 iterations (extract → review → refine)
- **Phase 2 (Fields):** 3-4 iterations (complex extraction)
- **Phase 3 (Artifacts):** 2 iterations (enrichment)
- **Phase 4 (Validation):** 2-3 iterations (rule extraction)
- **Phase 5 (Relationships):** 1-2 iterations (documentation)
- **Phase 6 (Glossary):** 1 iteration (quick polish)
- **Phase 7 (Final):** 1 iteration (cleanup)

**Total:** ~12-18 iterations depending on feedback density

---

## Next Step: Phase 1 Kickoff

**I will:**

1. Extract hook types, statuses from Layer 0/1
2. Extract Quality Bar categories
3. Extract loop types and classifications
4. Create draft `taxonomies.md` with all 10 sections
5. Present for your review

**You will:**

1. Review extracted taxonomies
2. Mark missing values or incorrect classifications
3. Clarify decision criteria where needed
4. Approve or request iteration

**Ready to start Phase 1?** Say the word and I'll begin automated extraction and draft the first version of `taxonomies.md`.
