# Implementation Plan: Schema Validation Enforcement

**Date:** 2025-11-06
**Status:** Implementation Blueprint
**Linked From:** [Schema Enforcement Post-Mortem](./2025-11-06_schema_enforcement_and_validation_contracts.md)
**Owner:** Specification Team

---

## Critical Insight: Document Creation ≠ Agent Compliance

**Problem:** Creating `VALIDATION_CONTRACT.md` doesn't force agents to read it.

**Solution:** Validation contracts must be **embedded in uploaded files** in the **correct order**, not just referenced.

---

## Upload Kit File Ordering Analysis

### Current Order (Correct Foundation)

```
1. 05-prompts/_shared/context_management.md        ← Shared patterns FIRST
2. 05-prompts/_shared/safety_protocol.md
3. 05-prompts/_shared/escalation_rules.md
4. 05-prompts/_shared/human_interaction.md
5. 05-prompts/showrunner/system_prompt.md          ← Role-specific content
6. [Role prompts or loop playbooks]
7. [Role adapters if orchestration mode]
```

**Why this matters:**
- LLMs read files in upload order
- Early files set context for later files
- Instructions in file #1 are "rules" for processing files #2-N
- Instructions in file #N may be "too late"

### Problem: Validation Instructions Come Too Late

**Current state:**
- Shared patterns loaded first ✅
- BUT: No validation contract in shared patterns ❌
- Role prompts loaded later
- By the time agent reads role prompts, may have already formed output structure

**Result:** Agent may produce output before seeing validation requirements

---

## Solution: Three-Layer Validation Embedding

### Layer 1: Validation Contract in _shared/ (FIRST FILE)

**Create:** `05-prompts/_shared/validation_contract.md`

**Upload Position:** **File #1** (before all other shared patterns)

**Content:**

```markdown
# Shared Pattern — Validation Contract

**CRITICAL: This contract applies to ALL roles and ALL artifacts.**

## Non-Negotiable Requirements

Every JSON artifact you produce MUST:

1. **Validate against canonical schema** before emission
2. **Include `"$schema"` field** pointing to schema $id
3. **Produce `validation_report.json`** alongside artifact
4. **STOP and report errors** if validation fails

## Discovery Protocol

Schemas are indexed in `/SCHEMA_INDEX.json` (uploaded with this kit).

For each artifact type, look up:
- `$id`: Canonical schema URL
- `path`: Local file path (if schema included)
- `draft`: JSON Schema draft version
- `sha256`: Integrity hash

## Preflight Protocol (MANDATORY)

Before producing ANY artifact:

1. **Locate schema** via SCHEMA_INDEX.json
2. **Echo back:**
   ```json
   {
     "$id": "...",
     "draft": "2020-12",
     "path": "...",
     "sha256": "..."
   }
   ```
3. **Show minimal valid instance** (1-2 required fields)
4. **Show one invalid example** + why it fails
5. **Only then proceed** with actual artifact

## Output Requirements

For every artifact `X.json`:

```
/out/X.json                    ← Artifact with "$schema" field
/out/X_validation_report.json  ← Validation evidence
```

### validation_report.json format

```json
{
  "artifact": "hook_card.json",
  "schema": {
    "$id": "https://questfoundry.liesdonk.nl/schemas/hook_card.schema.json",
    "draft": "2020-12",
    "sha256": "abc123..."
  },
  "validator": "jsonschema 4.17.3",
  "timestamp": "2025-11-06T12:00:00Z",
  "valid": true,
  "errors": []
}
```

If `valid: false`, errors array contains validation failures.

## Hard Gate Enforcement

**IF validation fails:**
1. STOP immediately
2. Return validation_report.json with errors
3. DO NOT produce the artifact
4. DO NOT continue the loop
5. ASK human for guidance

**DO NOT:**
- Produce "close enough" artifacts
- Skip validation "just this once"
- Assume structure without validating
- Continue after validation failure

## Validation Tools

Use one of:
- **Python:** `jsonschema` library
- **JavaScript:** `ajv` library
- **CLI:** `qfspec-check-instance <schema> <artifact>`

## This Contract Supersedes

If any role prompt or playbook contradicts this contract, **this contract wins**.
Validation is non-negotiable across all roles and all workflows.

---

**Loaded:** First shared pattern (file #1)
**Applies to:** All subsequent files and all roles
**Enforcement:** Hard stops on validation failure
```

**Manifest Update:**

```diff
  # orchestration-complete.list
+ 05-prompts/_shared/validation_contract.md          ← NEW, FIRST
  05-prompts/_shared/context_management.md
  05-prompts/_shared/safety_protocol.md
  05-prompts/_shared/escalation_rules.md
  05-prompts/_shared/human_interaction.md
  ...
```

### Layer 2: SCHEMA_INDEX.json in Kit Root

**Create:** `05-prompts/SCHEMA_INDEX.json`

**Upload Position:** **File #2** (immediately after validation_contract.md)

**Content:**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://questfoundry.liesdonk.nl/SCHEMA_INDEX.json",
  "title": "QuestFoundry Schema Index",
  "description": "Canonical registry of all schemas for validation",
  "version": "1.0.0",
  "generated": "2025-11-06T12:00:00Z",
  "schemas": {
    "hook_card": {
      "$id": "https://questfoundry.liesdonk.nl/schemas/hook_card.schema.json",
      "path": "03-schemas/hook_card.schema.json",
      "draft": "2020-12",
      "sha256": "a1b2c3d4...",
      "intent": ["hook.propose", "hook.classify"],
      "roles": ["plotwright", "scene_smith", "lore_weaver"]
    },
    "tu_brief": {
      "$id": "https://questfoundry.liesdonk.nl/schemas/tu_brief.schema.json",
      "path": "03-schemas/tu_brief.schema.json",
      "draft": "2020-12",
      "sha256": "e5f6g7h8...",
      "intent": ["tu.open"],
      "roles": ["showrunner"]
    },
    "canon_pack": {
      "$id": "https://questfoundry.liesdonk.nl/schemas/canon_pack.schema.json",
      "path": "03-schemas/canon_pack.schema.json",
      "draft": "2020-12",
      "sha256": "i9j0k1l2...",
      "intent": ["canon.propose", "canon.approve"],
      "roles": ["lore_weaver", "codex_curator", "gatekeeper"]
    }
    // ... all 18 schemas
  }
}
```

**Why in kit root:**
- Loaded immediately after validation contract
- Available before any role prompts
- Single source of truth for all schemas
- Agents can reference `/SCHEMA_INDEX.json` in all subsequent files

**Manifest Update:**

```diff
  # orchestration-complete.list
  05-prompts/_shared/validation_contract.md
+ 05-prompts/SCHEMA_INDEX.json                       ← NEW, SECOND
  05-prompts/_shared/context_management.md
  05-prompts/_shared/safety_protocol.md
  ...
```

### Layer 3: Reinforcement in Role Prompts and Playbooks

**Update ALL role prompts** with validation section:

```markdown
## Output Validation (Required)

**Refer to:** `/05-prompts/_shared/validation_contract.md` (loaded first)

For every artifact you produce:
1. Look up schema in `/SCHEMA_INDEX.json`
2. Run preflight (echo schema + show valid/invalid examples)
3. Validate artifact before emission
4. Produce validation_report.json
5. STOP if validation fails

This role produces these artifact types:
- [List artifact types this role creates]

Refer to SCHEMA_INDEX.json for each schema's $id, draft, and hash.
```

**Update ALL loop playbooks** with validation checkpoints:

```markdown
## Step N: [Role] produces [Artifact]

**Validation Checkpoint:**

1. [Role] looks up [artifact_type] schema in SCHEMA_INDEX.json
2. [Role] runs preflight (echo schema metadata)
3. [Role] produces artifact with "$schema" field
4. [Role] validates and produces validation_report.json
5. If validation fails: STOP loop, escalate to Showrunner
6. Showrunner verifies validation_report.json exists and valid: true
7. Only then proceed to Step N+1

**Artifacts:**
- `/out/[artifact].json`
- `/out/[artifact]_validation_report.json`
```

---

## Upload Kit Structure Updates

### Orchestration Kit (Complete)

**New file order:**

```
1. 05-prompts/_shared/validation_contract.md          ← ADDED
2. 05-prompts/SCHEMA_INDEX.json                       ← ADDED
3. 05-prompts/_shared/context_management.md
4. 05-prompts/_shared/safety_protocol.md
5. 05-prompts/_shared/escalation_rules.md
6. 05-prompts/_shared/human_interaction.md
7. 05-prompts/showrunner/system_prompt.md
8. 05-prompts/showrunner/loop_orchestration.md
9. 05-prompts/showrunner/manifest_management.md
10. 05-prompts/showrunner/protocol_handlers.md
11-23. 05-prompts/loops/*.playbook.md
24-38. 05-prompts/role_adapters/*.adapter.md
```

**Files added:** 2
**Total files:** 38 (was 36)

**Gemini splits need redistribution:**

Current split 1: 9 files → **10 files now** (add validation_contract + SCHEMA_INDEX)

```
gemini-orchestration-1-foundation.list:
1. validation_contract.md                             ← ADDED
2. SCHEMA_INDEX.json                                  ← ADDED
3. context_management.md
4. safety_protocol.md
5. escalation_rules.md
6. human_interaction.md
7. system_prompt.md
8. loop_orchestration.md
9. manifest_management.md
10. protocol_handlers.md
```

**Exactly 10 files** - still within Gemini limit ✅

### Standalone Kit (Minimal/Full)

**New file order:**

```
1. 05-prompts/_shared/validation_contract.md          ← ADDED
2. 05-prompts/SCHEMA_INDEX.json                       ← ADDED
3. 05-prompts/_shared/context_management.md
4. 05-prompts/_shared/safety_protocol.md
5. 05-prompts/_shared/escalation_rules.md
6. 05-prompts/_shared/human_interaction.md
7. 05-prompts/showrunner/system_prompt.md
8-12. [Role system prompts]
```

**Minimal kit impact:**
- Was: 10 files
- Now: 12 files (add validation_contract + SCHEMA_INDEX)
- **Exceeds ChatGPT 10-file limit by 2** ⚠️

**Solution:** Merge validation_contract into one of the shared patterns, OR split into minimal-1 (10 files) + minimal-2 (2 files)

**Recommendation:** Merge `validation_contract.md` content into `context_management.md` for minimal kits. Keep separate for orchestration kits.

---

## Manifest Updates Required

### New Manifests to Create

1. `05-prompts/upload_kits/manifests/orchestration-complete-v2.list` (38 files, adds validation files)
2. `05-prompts/upload_kits/manifests/gemini-orchestration-1-foundation-v2.list` (10 files, adds validation files)
3. Update all other manifests similarly

### Build Script Update

**Update:** `spec-tools/src/questfoundry_spec_tools/upload_kits.py`

**Changes:**
1. Generate SCHEMA_INDEX.json from 03-schemas/*.json before building kits
2. Compute SHA-256 for each schema
3. Place validation_contract.md and SCHEMA_INDEX.json at top of manifest order
4. Verify file count constraints (Gemini: ≤10)

---

## Implementation Steps

### Phase 1: Create Core Files (Week 1)

- [ ] **Day 1:** Create `05-prompts/_shared/validation_contract.md`
- [ ] **Day 1:** Create SCHEMA_INDEX.json generator script
- [ ] **Day 2:** Generate `05-prompts/SCHEMA_INDEX.json` with SHA-256s
- [ ] **Day 2:** Test validation_contract.md with ChatGPT (manual upload)
- [ ] **Day 3:** Verify preflight protocol works (agent echoes schema)
- [ ] **Day 3:** Verify hard gate works (agent stops on invalid artifact)

### Phase 2: Update Manifests (Week 1)

- [ ] **Day 4:** Update `orchestration-complete.list` (add 2 files, now 38 total)
- [ ] **Day 4:** Update `gemini-orchestration-1-foundation.list` (10 files with validation)
- [ ] **Day 5:** Update `minimal-standalone.list` (merge validation into context_management)
- [ ] **Day 5:** Update all Gemini split manifests

### Phase 3: Update Role Prompts and Playbooks (Week 2)

- [ ] **Day 6-7:** Add validation section to all 15 role prompts
- [ ] **Day 8-9:** Add validation checkpoints to all 13 loop playbooks
- [ ] **Day 10:** Update Gatekeeper prompt with schema validation quality bar

### Phase 4: Build and Test (Week 2)

- [ ] **Day 11:** Update upload_kits.py to generate SCHEMA_INDEX.json
- [ ] **Day 11:** Build all kits with new structure
- [ ] **Day 12:** Test orchestration-complete.zip with ChatGPT
- [ ] **Day 12:** Test gemini-orchestration splits with Gemini
- [ ] **Day 13:** Verify validation reports are produced
- [ ] **Day 13:** Verify hard gates work (stop on validation failure)

### Phase 5: Documentation (Week 3)

- [ ] **Day 14:** Update upload_kits/README.md with validation requirements
- [ ] **Day 15:** Update USAGE_GUIDE.md with validation workflow
- [ ] **Day 16:** Add validation examples to 04-protocol/EXAMPLES/
- [ ] **Day 17:** Document SCHEMA_INDEX.json format in 03-schemas/README.md

### Phase 6: spec-tools Integration (Week 4)

- [ ] **Day 18-19:** Add `qfspec-generate-schema-index` command
- [ ] **Day 20-21:** Add `qfspec-validate-artifact` command
- [ ] **Day 22:** Update `qfspec-check-instance` output format to validation_report.json
- [ ] **Day 23:** Add validation report verification to CI

### Phase 7: Release (Week 5)

- [ ] **Day 24:** Bump prompts version to v0.2.0
- [ ] **Day 25:** Update CHANGELOG.md with validation enforcement
- [ ] **Day 26:** Build all kits
- [ ] **Day 27:** Create prompts-v0.2.0 tag and release
- [ ] **Day 28:** Update documentation website

---

## Critical File Ordering Rules

### Rule 1: Validation Contract MUST Be File #1

**Why:** Sets non-negotiable rules before any role-specific content is processed.

**Enforcement:** First line in every manifest file.

### Rule 2: SCHEMA_INDEX.json MUST Be File #2

**Why:** Provides discovery mechanism immediately after contract rules.

**Enforcement:** Second line in every manifest file.

### Rule 3: Shared Patterns Before Role Content

**Why:** Establishes cross-role patterns (context, safety, escalation, human interaction).

**Enforcement:** Lines 3-6 in manifest (after validation files).

### Rule 4: Showrunner Before Other Roles

**Why:** Showrunner orchestrates; must see orchestration rules before role-specific content.

**Enforcement:** Showrunner modules after shared patterns, before loop playbooks or role adapters.

### Rule 5: Loop Playbooks Before Role Adapters

**Why:** Playbooks define procedures; adapters are called BY playbooks.

**Enforcement:** In orchestration kits, loops/*.playbook.md before role_adapters/*.adapter.md

---

## Validation Contract Propagation

### Where Validation Contract Appears

1. **Primary:** `05-prompts/_shared/validation_contract.md` (file #1 in all kits)
2. **Reference:** Every role prompt has "See validation_contract.md" section
3. **Checkpoints:** Every loop playbook has validation checkpoints
4. **Enforcement:** Gatekeeper prompt explicitly checks for validation reports
5. **Tools:** spec-tools produces validation_report.json format

### Why This Works

**Layered reinforcement:**
1. **Upload order** puts contract first (can't miss it)
2. **Role prompts** reference contract (reminder)
3. **Loop playbooks** have checkpoints (workflow integration)
4. **Gatekeeper** enforces (quality gate)
5. **Tools** support format (technical enablement)

**Failure modes addressed:**
- ❌ "Didn't see the contract" → Contract is file #1, impossible to miss
- ❌ "Forgot about validation" → Every loop has checkpoint reminders
- ❌ "Validation is optional" → Hard gates with STOP enforcement
- ❌ "Don't know how to validate" → Preflight protocol with examples
- ❌ "Can't find schema" → SCHEMA_INDEX.json is file #2

---

## Success Metrics

### Pre-Implementation (Baseline)

- Files in orchestration-complete.zip: 36
- Validation contract present: No
- SCHEMA_INDEX.json present: No
- Validation checkpoints in playbooks: 0/13
- Role prompts with validation section: 0/15
- Artifacts with "$schema" field: ~0%
- Validation reports produced: 0

### Post-Implementation (Target)

- Files in orchestration-complete.zip: 38 (+2)
- Validation contract present: Yes (file #1)
- SCHEMA_INDEX.json present: Yes (file #2)
- Validation checkpoints in playbooks: 13/13 (100%)
- Role prompts with validation section: 15/15 (100%)
- Artifacts with "$schema" field: 100%
- Validation reports produced: 1 per artifact (100%)

### Measurable Outcomes (Week 5)

- [ ] Agent echo-back of schema during preflight: 100%
- [ ] Artifacts include "$schema" field: 100%
- [ ] Validation reports alongside artifacts: 100%
- [ ] Hard stops on validation failure: 100%
- [ ] Zero schema violations in TU artifacts

---

## Risk Mitigation

### Risk 1: File count exceeds platform limits

**Impact:** Gemini limit is 10 files per zip; minimal kit was 10, now 12

**Mitigation:**
- Orchestration kits: Redistribute gemini-orchestration-1 to stay at 10 (done ✅)
- Minimal kits: Merge validation_contract into context_management.md
- Alternative: Split minimal kit into minimal-1 (10 files) + minimal-2 (2 files)

### Risk 2: Agents still skip validation

**Impact:** Despite contract being file #1, agents proceed without validation

**Mitigation:**
- Add "CRITICAL:" prefix to validation_contract.md title
- Use ALL CAPS for non-negotiable requirements
- Add visual separators (===) around critical sections
- Test with multiple LLMs (ChatGPT, Claude, Gemini)
- Iterate contract wording based on test results

### Risk 3: SCHEMA_INDEX.json becomes stale

**Impact:** SHA-256 hashes don't match actual schemas

**Mitigation:**
- Generate SCHEMA_INDEX.json automatically in build script
- Compute SHA-256s at build time (not manually)
- Add CI check: verify SCHEMA_INDEX.json hashes match schema files
- Fail build if hashes mismatch

### Risk 4: Validation reports not produced

**Impact:** Agents skip validation_report.json output

**Mitigation:**
- Validation contract explicitly requires BOTH artifact + report
- Gatekeeper checks for presence of validation reports
- spec-tools validates report format
- Showrunner refuses to continue loop without validation evidence

---

## Rollout Strategy

### Phase A: Silent Launch (Week 1-2)

- Create files, update manifests, build kits
- **Don't release yet**
- Internal testing with ChatGPT/Claude/Gemini
- Iterate validation_contract.md wording based on agent behavior

### Phase B: Alpha Release (Week 3)

- Release kits with validation (mark as "alpha")
- Document known issues
- Gather feedback on validation enforcement
- Measure: % of artifacts with validation reports

### Phase C: Beta Release (Week 4)

- Update based on alpha feedback
- Enhance error messages
- Add validation examples to documentation
- Measure: % of validation reports showing valid: true

### Phase D: Stable Release (Week 5)

- prompts-v0.2.0 release
- All kits include validation
- Documentation complete
- Metrics: 100% validation compliance

---

## Open Questions

### Q1: Should schemas themselves be included in upload kits?

**Pros:**
- Offline validation possible
- No network dependency
- Agents can read schema directly

**Cons:**
- Adds 18 files to kit (exceeds platform limits)
- Redundant if canonical URLs work
- Increases kit size significantly

**Recommendation:**
- **No** - Don't include schemas in kits
- SCHEMA_INDEX.json references canonical URLs
- Agents fetch from questfoundry.liesdonk.nl/schemas/
- Fallback: If URL unreachable, agent stops and asks human

### Q2: What if agent can't run jsonschema validation?

**Scenario:** Agent has no access to Python jsonschema or JavaScript ajv

**Mitigation:**
1. Agent should ASK human to validate
2. Agent produces artifact + note: "Validation pending, requires jsonschema"
3. Gatekeeper rejects TU until validation confirmed
4. Alternative: Agent uses $schema structure to do "best-effort" field checking

**Recommendation:**
- Contract says "IF you can validate, you MUST"
- Contract says "IF you cannot validate, STOP and ASK human"
- Never proceed without validation evidence

### Q3: How to handle schema evolution?

**Scenario:** Schema v0.3.0 released, but kits have SCHEMA_INDEX pointing to v0.2.0

**Mitigation:**
- SCHEMA_INDEX.json includes version field for each schema
- Agents use version specified in SCHEMA_INDEX (stable)
- To upgrade: rebuild kits with updated SCHEMA_INDEX
- Prompts reference "schemas-v0.2.0" explicitly (pin version)

**Recommendation:**
- Kits are versioned snapshots
- prompts-v0.2.0 uses schemas-v0.2.0
- prompts-v0.3.0 can use schemas-v0.3.0
- No automatic upgrades; intentional version alignment

---

## Conclusion

The key insight: **Validation contract must be loaded FIRST, not just exist somewhere**.

Upload kit file ordering is critical:
1. `validation_contract.md` - file #1 (non-negotiable rules)
2. `SCHEMA_INDEX.json` - file #2 (discovery mechanism)
3. Shared patterns - files #3-6 (cross-role standards)
4. Role-specific content - files #7+ (builds on foundation)

This ensures agents see validation requirements BEFORE producing any outputs.

**Next Action:** Create `validation_contract.md` and test with ChatGPT to verify agents read and follow it.

---

**Document Version:** 1.0
**Last Updated:** 2025-11-06
**Status:** Ready for Implementation
