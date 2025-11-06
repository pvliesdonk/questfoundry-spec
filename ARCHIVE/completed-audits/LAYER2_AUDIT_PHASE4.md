# Layer 2 Audit - Phase 4 Quality Review

**Date:** 2025-10-30 **Scope:** Comprehensive scan of Layer 2 for misplaced content,
inconsistencies, and merge opportunities **Status:** Draft for review

---

## Executive Summary

**Files Audited:** 5 core files + 34 artifact templates (17 original + 17 enriched)

**Key Findings:**

- ✅ **No major layer boundary violations** - Layer 2 content is appropriately placed
- ⚠️ **3 internal inconsistencies** found (glossary.md outdated)
- ⚠️ **Status markers outdated** (still say "PARKED" after Phase 3 completion)
- ⚠️ **Role definitions misplaced** in glossary.md (belong in Layer 1)
- ✅ **No true duplicates requiring merge** - overlaps are intentional (prose vs structured)

---

## Part 1: Layer Boundary Analysis

### 1.1 Content That Might Belong in Other Layers

#### Issue #1: Role Definitions in glossary.md

**Location:** `02-dictionary/glossary.md` Section D (lines ~50-76) **Current:** Lists all 15 role
canon names with one-line definitions **Analysis:**

- Role definitions = WHO does work → Layer 1 responsibility
- glossary.md is meant for general system terminology, not role charters
- Layer 1 already has `/01-roles/briefs/*.md` for detailed role info

**Recommendation:** **MOVE**

- Create `01-roles/ROLE_INDEX.md` with canonical role names and brief descriptions
- Remove Section D from glossary.md
- Update cross-references
- Alternatively: Keep very brief mentions in glossary, full details in Layer 1

**Priority:** Medium (organizational clarity, not blocking)

---

#### Issue #2: Loop Information Split Across Layers

**Locations:**

- Layer 0: `00-north-star/LOOPS/*.md` (13 loop guides with detailed instructions)
- Layer 2: `taxonomies.md` §3 (TU Types & Loop Alignment)
- Layer 2: `taxonomies.md` §10 (Loop Classifications)

**Analysis:** This is **acceptable separation**:

- Layer 0 = HOW to execute loops (process/policy)
- Layer 2 = WHAT loop types exist (taxonomy/classification)
- No duplication of content, just references

**Recommendation:** **KEEP AS IS** **Action:** Ensure cross-references remain accurate

---

#### Issue #3: Quality Bars Split Across Layers

**Locations:**

- Layer 0: `00-north-star/QUALITY_BARS.md` (8 bars with criteria/examples)
- Layer 2: `taxonomies.md` §5 (Quality Bar Categories - enumeration only)

**Analysis:** This is **acceptable separation**:

- Layer 0 = Bar definitions, criteria, evaluation guidance (policy)
- Layer 2 = Bar names and categorization (taxonomy)
- taxonomies.md §5 just lists the 8 bar names, doesn't redefine them

**Recommendation:** **KEEP AS IS** **Action:** Verify count consistency (currently 8 bars in both)

---

### 1.2 Layer Boundary Summary

**Verdict:** Layer 2 boundaries are generally well-maintained. Only minor issue is role definitions
in glossary.md, which could optionally be moved to Layer 1.

---

## Part 2: Internal Layer 2 Inconsistencies

### 2.1 Hook Types: glossary.md Outdated

**Issue:** Hook types listed in two places with different values

**Location A:** `glossary.md` Section E **Content:** Lists 4 hook types:
`narrative | scene | factual | taxonomy` **Status:** ❌ OUTDATED (missing 9 types)

**Location B:** `taxonomies.md` §1 **Content:** Lists 13 hook types (complete as of Phase 3):

- narrative, scene, factual, taxonomy, structure, canon, **research**,
- style/pn, translation, art, audio, binder/nav, accessibility

**Root Cause:** glossary.md was created before full taxonomy was developed

**Recommendation:** **UPDATE glossary.md**

- Option A: Update Section E to list all 13 types (brief one-liners)
- Option B: Remove type enumeration from glossary, point to taxonomies.md §1
- Option C: Keep 4 "primary" types in glossary as examples, note "see taxonomies.md for full list"

**Preferred:** Option B or C (avoid duplication)

---

### 2.2 Hook Status: glossary.md Outdated

**Issue:** Hook status values listed in two places with different counts

**Location A:** `glossary.md` Section E **Content:** Lists 4 statuses:
`proposed | accepted | deferred | rejected` **Status:** ❌ OUTDATED (missing 3 statuses)

**Location B:** `taxonomies.md` §2 **Content:** Lists 7 statuses (complete lifecycle):

- proposed, accepted, **in-progress**, **resolved**, **canonized**, deferred, rejected

**Root Cause:** glossary.md predates full lifecycle definition

**Recommendation:** **UPDATE glossary.md**

- Option A: Update to list all 7 statuses
- Option B: Remove status enumeration, point to taxonomies.md §2
- Option C: List basic flow only, reference taxonomies.md for full lifecycle

**Preferred:** Option B or C (single source of truth in taxonomies.md)

---

### 2.3 Quality Bars: Count Inconsistency Across Layers ⚠️ CRITICAL

**Issue:** Quality Bars count varies across layers

**Layer 0** (`00-north-star/QUALITY_BARS.md`):

```text
7 bars listed:
1. Integrity
2. Reachability
3. Nonlinearity
4. Gateways
5. Style
6. Determinism (when promised)
7. Presentation Safety (includes accessibility as bullet point)
```

**Status:** ❌ OUTDATED

**Layer 2** (`02-dictionary/taxonomies.md` §5):

```text
8 Quality Bar Categories (line 344 explicitly states "8 mandatory checks"):
1. Integrity
2. Reachability
3. Nonlinearity
4. Gateways
5. Style
6. Determinism
7. Presentation
8. Accessibility
```

**Status:** ✅ CURRENT (matches enriched templates)

**Layer 2** (`02-dictionary/glossary.md` Section F):

```text
7 bars mentioned:
Integrity, Reachability, Nonlinearity, Gateways, Style,
Determinism (when promised), Presentation (spoiler & accessibility hygiene)
```

**Status:** ❌ OUTDATED (follows old Layer 0 structure)

**Context from Issue #3:** LAYER1_CORRECTIONS.md Issue #3 documents that templates were missing
Determinism, and the decision was made to standardize on **8 bars** with Presentation and
Accessibility as separate bars.

**All Phase 3 enriched templates use 8 bars** (Presentation and Accessibility separate)

**Recommendation:** **UPDATE Layer 0 and glossary.md to 8-bar structure**

- Update `00-north-star/QUALITY_BARS.md` to split Presentation Safety into:
  - Bar 7: Presentation (spoiler hygiene, meta language, technique leakage)
  - Bar 8: Accessibility (alt text, captions, readability, contrast)
- Update `glossary.md` Section F to list all 8 bars
- This aligns with the documented decision in Issue #3

---

### 2.4 Internal Inconsistency Summary

**Found:** 4 inconsistencies

**Root Causes:**

1. glossary.md was created earlier and hasn't been updated as taxonomies evolved
2. Layer 0 QUALITY_BARS.md hasn't been updated to reflect the 8-bar decision (documented in Issue
   #3)

**Fix Strategy:**

1. Update glossary.md to defer to taxonomies.md for precise enumerations
2. Update Layer 0 QUALITY_BARS.md to split Presentation Safety into Presentation + Accessibility (8
   bars total)

---

## Part 3: Near-Duplicates & Merge Opportunities

### 3.1 glossary.md vs taxonomies.md

**Analysis:**

- **glossary.md (118 lines):** Prose definitions of concepts, organized by domain (A-H sections)
- **taxonomies.md (979 lines):** Structured controlled vocabularies with validation rules, organized
  by taxonomy type (10 sections)

**Overlap:** Both define hook types, hook status, quality bars, roles, loops

**Purpose Difference:**

- glossary.md = **Human-friendly reference** (explain concepts in plain language)
- taxonomies.md = **System-friendly reference** (precise enumerations for validation)

**Recommendation:** **KEEP BOTH** but clarify division of responsibility:

- glossary.md → General definitions, high-level explanations
- taxonomies.md → Precise controlled vocabularies, allowed values, validation rules
- glossary.md should **reference** taxonomies.md for precise details, not duplicate them

**Action:** Refactor glossary.md to be conceptual, not enumerative

---

### 3.2 field_registry.md vs taxonomies.md

**Analysis:**

- **field_registry.md (465 lines):** Catalogs 237 fields across 17 artifacts
- **taxonomies.md (979 lines):** Defines 10 classification systems

**Overlap:** Both reference hook types, status, bars in field definitions

**Purpose Difference:**

- field_registry.md = **Field catalog** (what fields exist, where used, constraints)
- taxonomies.md = **Classification systems** (allowed values for enum fields)

**Relationship:** field_registry.md **references** taxonomies.md (many fields link to taxonomy
sections)

**Recommendation:** **KEEP BOTH** - No merge needed, they serve different purposes

- field_registry = horizontal (all fields across artifacts)
- taxonomies = vertical (classification systems depth)

---

### 3.3 Original vs Enriched Artifact Templates

**Current State:** 17 original + 17 enriched = 34 files in `artifacts/`

**Analysis:**

- Original templates: Human-friendly, prose-heavy, examples
- Enriched templates: Same content + HTML constraint comments + validation rules + common errors

**Purpose:**

- Original = Human authoring reference (clean, readable)
- Enriched = Human + machine reference (includes inline schemas for Layer 3)

**Recommendation:** **KEEP BOTH**

- Original templates for human consumption during work
- Enriched templates as source of truth for Layer 3 schema generation
- Could eventually deprecate originals once Layer 3 schemas exist

**Future:** Once Layer 3 has formal schemas, consider:

- Option A: Archive original templates
- Option B: Keep originals as "Quick Reference" versions
- Option C: Merge (replace originals with enriched, accept extra noise)

**Current:** KEEP BOTH (enriched templates were the Phase 3 deliverable)

---

### 3.4 README Files (2)

**Files:**

- `02-dictionary/README.md` (128 lines) - Layer 2 overview
- `02-dictionary/artifacts/README.md` (112 lines) - Artifact index

**Overlap:** Both explain artifact structure and Layer 2 purpose

**Purpose Difference:**

- Layer README = High-level: what Layer 2 is, migration notes, planned structure
- Artifact README = Focused: artifact index, usage guide, cross-references

**Recommendation:** **KEEP BOTH**

- Layer README = Layer 2 entry point for newcomers
- Artifact README = Artifact catalog and index

**Action:** Update both to reflect Phase 3 completion (currently both say "PARKED")

---

### 3.5 Near-Duplicates Summary

**Verdict:** No true duplicates requiring merge. All apparent overlaps serve different purposes.

**Keep:**

- glossary.md AND taxonomies.md (conceptual vs structured)
- field_registry.md AND taxonomies.md (fields vs classifications)
- Original AND enriched templates (human vs human+machine)
- Both README files (layer overview vs artifact index)

**Action:** Clarify relationships and update cross-references

---

## Part 4: Outdated Content

### 4.1 Status Markers Need Updating

**Files with "PARKED" status:**

1. `02-dictionary/README.md` - Line 3: "Status: 🚧 PARKED — Pending proper Layer 2 draft"
2. `02-dictionary/glossary.md` - Line 3: "Status: 🚧 PARKED — Pending Layer 2 proper draft"
3. `02-dictionary/artifacts/README.md` - Line 3: "Status: 🚧 PARKED — Pending Layer 2 proper draft"

**Reality:** Phase 3 just completed:

- ✅ taxonomies.md drafted (Phase 1)
- ✅ field_registry.md created (Phase 2)
- ✅ All 17 artifacts enriched (Phase 3)

**Recommendation:** **UPDATE STATUS**

**New status suggestions:**

- **README.md:** "Status: ✅ ACTIVE — Phase 3 enrichment complete (2025-10-30)"
- **glossary.md:** "Status: ⚠️ REVIEW NEEDED — Outdated enumerations, update to defer to
  taxonomies.md"
- **artifacts/README.md:** "Status: ✅ ENRICHED — All 17 templates enriched with constraints (Phase
  3)"

---

### 4.2 Migration Notes Are Historical

**Location:** All 3 README files mention "migration" from Layer 0/1

**Context:** This was from earlier architectural cleanup (ADR-20251029-01)

**Recommendation:** **KEEP** migration notes as historical context, but:

- Move to "History" or "Background" section
- Add current status prominently at top
- Don't let historical content overshadow current state

---

## Part 5: Recommendations Summary

### Priority 1: Update Status Markers (Quick Wins)

1. Update `02-dictionary/README.md` status to ACTIVE/COMPLETE
2. Update `02-dictionary/artifacts/README.md` status to reflect Phase 3
3. Update `glossary.md` status with caveat about needed updates

**Effort:** Low (edit 3 files) **Impact:** High (accurate documentation)

---

### Priority 2: Fix Layer 0 Quality Bars (CRITICAL)

1. Update `00-north-star/QUALITY_BARS.md` to 8-bar structure
2. Split current "Presentation Safety" (bar 7) into:
   - Bar 7: Presentation (spoiler hygiene, meta, technique)
   - Bar 8: Accessibility (alt, captions, readability, contrast)
3. Update Gatekeeper's Checklist to reflect 8 bars
4. Aligns with Issue #3 resolution and all Phase 3 enriched templates

**Effort:** Medium (refactor Layer 0 file) **Impact:** CRITICAL (cross-layer consistency, basis for
all validation)

---

### Priority 3: Fix glossary.md Inconsistencies

1. Update Quality Bars count to 8 (defer to taxonomies.md §5)
2. Remove or update hook type enumeration (defer to taxonomies.md §1)
3. Remove or update hook status enumeration (defer to taxonomies.md §2)
4. Clarify that glossary = concepts, taxonomies = precise enumerations

**Effort:** Medium (refactor glossary.md sections E-F) **Impact:** High (consistency, single source
of truth)

---

### Priority 4: Consider Moving Role Definitions

1. Evaluate if role definitions belong in glossary.md or Layer 1
2. If moved: Create `01-roles/ROLE_INDEX.md` with canonical names
3. Update cross-references

**Effort:** Medium (move content, update refs) **Impact:** Low-Medium (organizational clarity, not
blocking)

---

### Priority 5: Clarify Documentation Relationships

1. Add cross-reference notes to each file explaining its relationship to others
2. Update README files with current structure map
3. Document that glossary = prose, taxonomies = structured, field_registry = catalog

**Effort:** Low (add clarifying notes) **Impact:** Medium (helps future contributors)

---

## Part 6: No Action Needed

### Items Reviewed and Found Acceptable

✅ **Layer boundary separation** - Layer 2 appropriately scoped ✅ **Loop information split** -
Layer 0 (how) vs Layer 2 (what) is correct ✅ **Quality Bars split** - Layer 0 (criteria) vs Layer 2
(taxonomy) is correct ✅ **Multiple README files** - Serve different purposes ✅ **Original +
Enriched templates** - Both have value ✅ **glossary + taxonomies separation** - Different
audiences/purposes ✅ **field_registry + taxonomies separation** - Different dimensions

---

## Conclusion

**Overall Assessment:** Layer 2 is in **good shape** with only **minor housekeeping** needed.

**Major Issues:** 1 (Quality Bars count mismatch across layers - Layer 0 outdated) **Minor Issues:**
3 (glossary.md outdated enumerations) **Documentation Updates:** 3 files need status refresh

**No merges or major restructuring needed.** The apparent duplications are intentional and serve
different purposes (prose vs structured, human vs machine, overview vs detail).

**Recommended Phase 4 Focus:** Clean up identified inconsistencies (Priority 1-2 items) before
proceeding to Layer 3 or applying Layer 1 corrections.

---

## Next Steps

**Option A: Quick Cleanup (2-3 hours)**

- Update 3 status markers
- **Fix Layer 0 QUALITY_BARS.md to 8-bar structure** (CRITICAL)
- Fix glossary.md enumerations (defer to taxonomies.md)
- Commit as "fix: Update Quality Bars to 8-bar structure across layers"

**Option B: Comprehensive Cleanup (4-5 hours)**

- All of Option A
- Move role definitions to Layer 1
- Add cross-reference documentation
- Update README structure maps
- Commit as "refactor: Layer 2 documentation consistency pass"

**Option C: Proceed to Other Work**

- Accept minor inconsistencies as tech debt
- Focus on higher priority work (Layer 1 corrections, Layer 3 schemas, etc.)
- Circle back to cleanup later

**Recommendation:** **Option A** (quick cleanup with Priority 1-2-3) - Medium effort, CRITICAL
value, resolves the cross-layer Quality Bars inconsistency that affects all validation going
forward.

---
