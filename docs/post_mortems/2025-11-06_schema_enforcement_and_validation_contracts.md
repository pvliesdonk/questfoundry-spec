# Post-Mortem: Schema Enforcement and Validation Contract Failures

**Date:** 2025-11-06 **Scope:** Schema validation enforcement across all AI agent interactions
**Status:** Root cause identified; systemic fixes proposed **Severity:** High - Schema
non-compliance, validation bypass, structural drift **Incident Owner:** All roles (systemic issue),
particularly Gatekeeper and protocol handlers

---

## Executive Summary

AI agents (including Claude) failed to consistently validate outputs against canonical JSON schemas
despite schemas being present in the repository. Agents would either (a) not discover schemas, (b)
use inferred structures instead of canonical ones, or (c) proceed without validation even when
schemas were available.

**Key Finding:** The presence of schemas is **necessary but insufficient**. Without explicit
binding, gating, and enforcement instructions, agents treat schemas as **optional references**
rather than **mandatory contracts**.

**Root Cause:** Missing validation contract specification in agent prompts; no enforcement gates;
ambiguous schema discovery; lack of preflight validation requirements.

**Impact:** Outputs that appear valid but violate schema constraints; downstream tool failures;
inability to guarantee schema conformance; protocol violations cascading through the system.

---

## Impact

### Artifact Quality

- Outputs produced without schema validation
- Structural drift from canonical format
- Missing required fields or incorrect field types
- No machine-readable validation reports

### Operational

- **Trust erosion:** Cannot guarantee schema conformance
- **Debugging overhead:** Schema violations discovered late in pipeline
- **Tool failures:** Downstream validators reject non-conformant artifacts
- **Protocol violations:** Missing validation step breaks quality gates

### Systemic

- Schema investment wasted if not enforced
- Layer 3 (schemas) disconnected from Layer 5 (prompts)
- No validation traceability (no evidence of schema checks)

---

## Root Cause Analysis

### Primary Causes

1. **No Validation Contract in Prompts**
   - Layer 5 prompts don't explicitly require schema validation
   - No instructions on HOW to validate (ajv, jsonschema, etc.)
   - No requirement to produce validation reports

2. **Schema Discovery Ambiguity**
   - Multiple ways to provide schemas (zip, separate files, embedded, URL)
   - No canonical discovery mechanism specified
   - No SCHEMA_INDEX.json to declare authoritative schemas

3. **Missing Enforcement Gates**
   - No hard stops on validation failure
   - No requirement to show validation evidence
   - Agents can proceed without validation

4. **Lack of Preflight Requirements**
   - No requirement to verify schema before producing output
   - No "echo back the schema" step to confirm understanding
   - No minimal valid instance + negative test requirement

### Contributing Factors

- **Zip file discoverability:** Schemas buried in directory structures
- **No schema binding in outputs:** Artifacts don't declare which schema they conform to
- **Soft language:** "Should validate" vs "MUST validate, or STOP"
- **No validation report artifact:** Missing `validation_report.json` as required output

---

## Timeline

### Pre-Incident Pattern

1. Schemas created and validated (Layer 3) ✅
2. Schemas available in repository ✅
3. AI agents loaded with role prompts ✅
4. **Gap:** No validation contract in prompts ❌
5. Outputs produced without validation ❌
6. Schema violations discovered late ❌

### Example Incident

**Scenario:** Story Spark loop execution

1. **T+0:** Agent receives Story Spark request
2. **T+1:** Agent produces structure (appears valid to human)
3. **T+2:** Output lacks validation report
4. **T+3:** User asks: "Did you validate against the schema?"
5. **T+4:** Agent: "I used the structure but didn't run validation"
6. **Result:** No evidence of conformance; potential violations

---

## What Worked

1. **Schemas exist and are well-defined** — Layer 3 complete
2. **Schemas are accessible** — In repository, via canonical URLs
3. **Schemas are valid** — Meta-validation passes
4. **Agent capability** — Agents CAN validate when explicitly directed

---

## What Didn't Work

1. **Implicit validation expectations** — Not embedded in prompts
2. **Soft requirements** — "Should" vs "MUST"
3. **No gating** — Can proceed without validation
4. **No discovery protocol** — Ambiguous how to find canonical schema
5. **No validation artifact** — Missing validation_report.json
6. **No preflight** — No "verify schema first" step

---

## Solutions Implemented (Proposed)

### 1. Validation Contract Specification

**Create:** `04-protocol/VALIDATION_CONTRACT.md`

```markdown
# Validation Contract

ALL artifact outputs MUST:

1. Validate against canonical JSON schema before emission
2. Include "$schema" field pointing to schema $id
3. Produce validation_report.json (even if empty errors array)
4. STOP and return validation errors if validation fails

## Preflight Protocol

Before producing any artifact:

1. Read canonical schema
2. Echo: {$id, draft, path, sha256}
3. Show minimal valid instance
4. Show one invalid example + why it fails
5. Only then proceed with actual task
```

### 2. SCHEMA_INDEX.json

**Create:** `03-schemas/SCHEMA_INDEX.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "QuestFoundry Schema Index",
  "description": "Canonical registry of all schemas with discovery metadata",
  "schemas": {
    "hook_card": {
      "$id": "https://questfoundry.liesdonk.nl/schemas/hook_card.schema.json",
      "path": "03-schemas/hook_card.schema.json",
      "draft": "2020-12",
      "sha256": "<computed>",
      "intent": "hook.propose",
      "roles": ["plotwright", "scene_smith", "lore_weaver"]
    },
    "story_spark": {
      "$id": "https://questfoundry.liesdonk.nl/schemas/story_spark.schema.json",
      "path": "03-schemas/story_spark.schema.json",
      "draft": "2020-12",
      "sha256": "<computed>",
      "intent": "tu.open",
      "roles": ["showrunner", "plotwright"]
    }
    // ... all schemas
  }
}
```

### 3. Update Layer 5 Prompts

**Add to ALL role prompts:**

```markdown
## Validation Protocol

Before producing ANY JSON artifact:

1. Locate canonical schema via SCHEMA_INDEX.json
2. Verify: $id, draft, path, sha256
3. Produce artifact with "$schema" field
4. Validate using jsonschema (Python) or ajv (JavaScript)
5. If validation fails: STOP, return validation report, DO NOT PROCEED
6. If validation succeeds: produce artifact + validation_report.json

## Required Outputs

For every artifact X.json:

- X.json (artifact with "$schema" field)
- X_validation_report.json (errors array, empty if valid)

## Gating Rule

HARD STOP on validation failure. Do not continue the loop.
```

### 4. Showrunner Loop Orchestration Update

**Add validation checkpoint to every loop:**

```markdown
## Validation Checkpoint (After Each Artifact)

1. Agent produces artifact + validation report
2. Showrunner verifies:
   - validation_report.json exists
   - errors array is empty
   - artifact has "$schema" field
3. If validation failed: STOP loop, escalate to human
4. If validation passed: continue to next step
```

### 5. Gatekeeper Pre-Gate Validation

**Enhance Gatekeeper prompt:**

```markdown
## Schema Validation (Quality Bar 8)

For ALL artifacts in the TU:

1. Verify each artifact has "$schema" field
2. Verify validation_report.json exists for each artifact
3. Re-validate all artifacts against canonical schemas
4. Report:
   - Total artifacts: N
   - Schema-conformant: M
   - Validation failures: N-M (with details)
5. GATE RULE: REJECT TU if any artifact fails validation
```

---

## Enforcement Mechanisms

### Best-to-Worst Schema Delivery Methods

**Ranked by determinism and enforceability:**

1. **✅ BEST: Separate schema file + explicit binding**
   - Upload schema separately
   - Provide: path, $id, draft, SHA-256
   - Hard gate: "Do not proceed without validation"
   - Result: 100% addressable, verifiable, gatable

2. **✅ GOOD: Zip with SCHEMA_INDEX.json**
   - Include schemas in zip
   - Add SCHEMA_INDEX.json with canonical entries
   - Instruct: "Use THIS index, ignore others"
   - Result: Good discoverability, verifiable

3. **⚠️ ACCEPTABLE: Schema embedded in prompt**
   - Embed schema JSON in prompt
   - Provide: $id, draft, SHA-256 of embedded text
   - Say: "Treat this as canonical"
   - Cons: Token heavy, copy-paste risks

4. **❌ AVOID: Soft mention ("there's a schema somewhere")**
   - "Schemas are in the repo..."
   - No explicit path or binding
   - No enforcement
   - Result: Invites drift and non-compliance

### Copy-Paste Contract Template

```markdown
VALIDATION CONTRACT:

- Canonical schema: /03-schemas/hook_card.schema.json
- Schema $id: https://questfoundry.liesdonk.nl/schemas/hook_card.schema.json
- Draft: 2020-12
- SHA256: <paste hex>

REQUIREMENTS:

1. Preflight: read schema; reply with {$id, draft, path, sha256} + minimal valid instance + one
   invalid example
2. Only produce outputs that validate. If validation fails: return report, STOP.
3. Emit outputs:
   - /out/hook_card.json (with "$schema": "$id")
   - /out/validation_report.json (ajv/jsonschema errors array)
4. Do not use other schema copies. If file missing or hash mismatch: REFUSE TO PROCEED.
```

---

## Questions Answered

### Q: Would separate files vs zip have made a difference?

**A: Yes, but only with explicit binding.**

- **Separate files:** Easier to address, quote path + hash, enforce. **Recommended.**
- **Zip:** Fine if includes SCHEMA_INDEX.json and explicit instructions.
- **Key:** Not the delivery method, but the **binding + gating instructions**.

### Q: Would embedding schema in prompt have helped?

**A: Only with SHA-256 and "treat as canonical" instruction.**

- Pros: Guaranteed visibility, no file I/O
- Cons: Token heavy, copy-paste defects, version drift
- **Use only if:** Also provide $id, draft, SHA-256 of embedded text
- **Better:** Separate file is more deterministic

### Q: What's the single most important fix?

**A: Hard gates with STOP on validation failure.**

The schema can be delivered any way, but:

1. Must be explicitly named (path + $id + SHA)
2. Must be bound to outputs ("use THIS schema")
3. Must have hard gate ("STOP if validation fails")

---

## Action Items

### Immediate (Layer 4-5)

- [ ] **Create** `04-protocol/VALIDATION_CONTRACT.md`
- [ ] **Create** `03-schemas/SCHEMA_INDEX.json`
- [ ] **Update** all Layer 5 role prompts with validation protocol
- [ ] **Add** validation checkpoint to all 13 loop playbooks
- [ ] **Enhance** Gatekeeper prompt with schema validation quality bar

### Short-Term (spec-tools)

- [ ] **Add** `qfspec-validate-artifact` command (validates single artifact + produces report)
- [ ] **Update** `qfspec-check-instance` to output validation_report.json format
- [ ] **Create** `compute-schema-index` script (generates SCHEMA_INDEX.json with SHA-256s)

### Medium-Term (Layer 6-7)

- [ ] **Python SDK:** Add `questfoundry.validate(artifact, schema_name)` → ValidationReport
- [ ] **CLI:** `qf validate <artifact>` command with exit codes
- [ ] **Upload kits:** Include SCHEMA_INDEX.json in all kits

### Documentation

- [ ] **Update** USAGE_GUIDE.md with validation contract
- [ ] **Create** validation contract example in 05-prompts/
- [ ] **Document** SCHEMA_INDEX.json format in 03-schemas/README.md
- [ ] **Add** validation examples to 04-protocol/EXAMPLES/

---

## Lessons Learned

### What We Learned

1. **Presence ≠ Usage:** Having schemas doesn't guarantee they're used
2. **Soft requirements fail:** "Should validate" gets ignored under pressure
3. **Hard gates work:** "STOP if invalid" is clear and enforceable
4. **Preflights prevent drift:** "Echo schema first" catches misunderstandings early
5. **Artifacts need binding:** `"$schema"` field makes conformance explicit
6. **Validation evidence matters:** `validation_report.json` proves conformance

### What We're Changing

1. **Validation is now mandatory** — Not optional, not soft
2. **Gating is now explicit** — STOP on validation failure
3. **Evidence is now required** — validation_report.json for every artifact
4. **Discovery is now deterministic** — SCHEMA_INDEX.json is canonical
5. **Preflights are now standard** — Verify schema before producing output

### What We're Keeping

1. **Layer 3 schemas** — Already excellent, just need enforcement
2. **Canonical URLs** — questfoundry.liesdonk.nl/schemas/ works well
3. **Draft 2020-12** — Solid choice, good tooling support
4. **spec-tools validation** — Just needs output format alignment

---

## Metrics

### Current State (Pre-Fix)

- Schema validation rate: ~0% (not enforced)
- Validation reports produced: 0
- Hard stops on validation failure: 0
- Artifacts with "$schema" field: ~0%

### Target State (Post-Fix)

- Schema validation rate: 100% (enforced)
- Validation reports produced: 1 per artifact
- Hard stops on validation failure: 100%
- Artifacts with "$schema" field: 100%

### Success Criteria

- **Week 1:** Validation contract documented and in all role prompts
- **Week 2:** SCHEMA_INDEX.json created and tested
- **Week 4:** All loop playbooks include validation checkpoints
- **Week 8:** spec-tools outputs validation_report.json format
- **Week 12:** Python SDK has validate() function

---

## Conclusion

Schema validation failures weren't due to missing schemas or agent inability—they were due to
**missing enforcement contracts**. The fix isn't more schemas or better schemas; it's **explicit
binding, hard gates, and mandatory evidence**.

With validation contracts in place:

1. Agents know **which** schema to use (SCHEMA_INDEX.json)
2. Agents know **how** to validate (preflight + validate + report)
3. Agents know **when** to stop (validation failure = hard gate)
4. Humans can verify **evidence** (validation_report.json for every artifact)

**Next Step:** Create VALIDATION_CONTRACT.md and SCHEMA_INDEX.json, then update Layer 5 prompts with
mandatory validation protocol.

---

**Post-Mortem Author:** Claude (Anthropic) **Reviewed By:** Peter van Liesdonk **Date:** 2025-11-06
**Status:** Approved - Implementation Pending
