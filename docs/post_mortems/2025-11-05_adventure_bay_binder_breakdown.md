# Post-Mortem: Adventure Bay Binder Breakdown

**Date:** 2025-11-05 **Scope:** Showrunner pipeline (Gatekeeper → Plotwright → Scene Smith →
Art/Illustration → Binder → EPUB/PDF) for the "Beks op de Baai" Paw Patrol story **Status:**
Resolved with recovery bundle; systemic fixes required **Severity:** High - Protocol violation,
determinism failure **Incident Owner:** Showrunner/Binder roles

---

## Executive Summary

We produced a compelling story and high-quality illustrations, but the publishing phase **diverged
from protocol**. Images in EPUB/PDF were mis-ordered, missing, or stale, because the Binder deviated
from the "Cold Source of Truth (SoT) + manifest-first" rule and allowed heuristic remapping and
ad-hoc rebuilds.

**Recovery:** Packaged a Cold SoT bundle (texts + assets + SHA-256 inventory)

**Impact:** Reader artifacts unusable; multiple rebuild cycles; trust erosion

**Root Cause:** Protocol non-adherence + missing Cold SoT format specification

---

## Impact

### Reader Artifacts

- EPUB(s) initially lacked images
- Later variants had incorrect order, wrong substitutions
- Cover-only images displayed on Kobo reader

### Operational

- **Wasted cycles:** Multiple rebuilds, redundant illustration renders
- **Manual intervention:** User had to identify and flag non-compliance
- **Trust erosion:** Violating spec's determinism guarantees delayed hand-off

---

## Timeline

1. **Story + images iterated successfully**
   - Cover approved
   - Several plates approved
   - **Gap:** No SHA-256 recorded at approval time

2. **EPUB builds via Pandoc**
   - Resources not embedded → images missing on device
   - **Gap:** No preflight check for resource resolution

3. **Manual EPUB/PDF attempts**
   - Partial success but order drift introduced
   - Stale assets introduced by heuristics
   - Environment resets dropped in-memory mappings
   - **Gap:** Multiple build paths without canonical source

4. **User flags non-compliance**
   - Image order incorrect
   - Binder not honoring manifest
   - **Gap:** No automated validation gates

5. **Recovery**
   - Delivered Cold SoT bundle:
     - `manifest_sections.json`
     - `manifest_images.json`
     - `assets_inventory.csv`
     - SHA-256 for all assets

---

## Root Cause Analysis

### Primary Root Cause

**Protocol deviation:** Binder deviated from protocol when build failed. Instead of stopping to
re-establish Cold SoT + manifest as the only source, the system:

- Injected images heuristically (filename pattern guesses, "newest file wins")
- Used mixed routes (Pandoc then manual packer) without re-anchoring to manifest
- Let environment resets drop in-memory notion of image-to-section mapping

**This violated spec invariants:**

- ❌ Deterministic mapping from manifest → layout
- ❌ No heuristics allowed
- ❌ Hash-anchored assets required

### Contributing Factors

1. **Environment volatility**
   - Working directory changed between builds
   - Prior artifacts garbage-collected or overwritten
   - Path resolution differed between builds

2. **Missing hash discipline**
   - No SHA-256 recorded at illustration approval time
   - Impossible to prove using latest/correct files

3. **Tooling fallbacks**
   - Pandoc resource resolution failed → manual packer
   - Manual packer didn't re-bind to manifest

4. **Spec pressure vs. speed**
   - Bias toward "get a working EPUB now"
   - Defeated "manifest or bust" rule

5. **Policy constraints**
   - Child likeness policy change (back view required)
   - Re-renders needed
   - Some "old" images lingered, increasing confusion

6. **No red-flag gate**
   - Gatekeeper didn't hard-stop builds lacking complete, hash-verified manifest

---

## What Went Well

✅ **Creative pipeline**

- Plotwright/Scene Smith loop produced cohesive scenes
- Art Director loop produced on-brand visuals

✅ **Constraint handling**

- Adapted ethically (child from back) without blocking narrative

✅ **Recovery**

- Delivered forensic Cold bundle enabling deterministic reconstruction
- Manifests + SHA-256 + assets packaged

---

## What Went Wrong

❌ **Protocol non-adherence**

- Spec clearly states Cold SoT is canonical
- Allowed "hot" heuristics to creep in

❌ **Inconsistent binders**

- Multiple build methods (Pandoc vs. manual)
- No single, manifest-driven source of layout truth

❌ **Resource path fragility**

- Pandoc runs without `--resource-path`
- Missing assets produced silent failures (cover only)

❌ **State drift**

- "Latest image" ≠ "approved image"
- Filenames alone insufficient without hashes and versioning

❌ **Missing preflight**

- No pre-build check for 1:1 section-to-plate mapping
- No hash verification before build

❌ **Cold SoT format non-compliance**

- Build path didn't use canonical Cold format
- Ad-hoc files and layouts introduced
- No schema validation

---

## Detection

- **When:** Post-build, during device testing
- **How:** User noticed images missing/mis-ordered
- **Verification:** Manifest drift confirmed, stale files found, no hashes present

---

## Resolution

### Immediate Fix

Created **Cold SoT Recovery Bundle:**

```text
cold/
├── manifest_sections.json    # anchors, titles, expected filenames
├── manifest_images.json      # filename → SHA-256, bytes
├── assets_inventory.csv      # comprehensive asset list
├── manifest_missing.json     # gaps identified
└── assets/
    └── *.png                 # All current PNGs with hashes
```

Built strict manifest EPUB/PDF variants to demonstrate correct assembly route.

**Stopped all further heuristic mapping.**

---

## Preventive Improvements

### A. Hard Protocol Guards (Gatekeeper)

**Fail fast** if any of the following is missing before build:

- ✅ Cold text file (canonical markdown)
- ✅ Manifest mapping: `anchor → title → image.filename → sha256`
- ✅ Physical asset at `assets/<filename>` with matching SHA-256

**Block heuristics:** If a referenced file is missing, build must **STOP** with clear error and
remediation checklist.

### B. Deterministic Asset Lifecycle

On illustration approval, **immediately:**

1. Compute SHA-256
2. Write/update `cold/art_manifest.json`
3. Enforce deterministic filename: `<anchor>__<role>__v<semver>.png`
4. Add provenance field (role, prompt snippet, timestamp)

**Binder consumes manifest only; no file system scans allowed.**

### C. Single Binder Route

**One—and only one—binder path:**

```text
Input:  cold/book.json + cold/art_manifest.json
Engine: Pandoc (EPUB) + WeasyPrint (PDF)
Output: EPUB + PDF
```

Manual packer allowed only behind `BINDER_FALLBACK=TRUE` flag and **must** use same manifest.

### D. Resource Path Contract

Pandoc must always receive:

```bash
--resource-path "<project-root>:assets"
```

Fail if any referenced resource is unresolved.

**Pre-step:** Open every referenced image and verify it's decodable.

### E. State Persistence & Rollback

Persist build context with outputs:

```json
build.json:
{
  "timestamp": "2025-11-05T14:30:00Z",
  "inputs": {
    "book": "cold/book.json",
    "art_manifest": "cold/art_manifest.json"
  },
  "files": [
    {"path": "assets/anchor001__plate__v1.png", "sha256": "abc123..."}
  ],
  "versions": {
    "pandoc": "3.1.9",
    "weasyprint": "60.1"
  }
}
```

Allow rollback by reusing exact manifest and file set.

### F. Policy-Aware Roles

**Researcher + Art Director checklist:**

- If real child likeness is out-of-policy → auto-fallback to back/¾ framing
- Record decision in `cold/art_manifest.json` so rerenders inherit it

---

## Cold SoT File Format Specification

### Required Cold Files

1. **`cold/manifest.json`** — Top-level index

   ```json
   {
     "$schema": "https://questfoundry.liesdonk.nl/schemas/cold_manifest.schema.json",
     "version": "1.0.0",
     "files": [
       { "path": "cold/book.json", "sha256": "..." },
       { "path": "cold/art_manifest.json", "sha256": "..." }
     ]
   }
   ```

2. **`cold/book.json`** — Story structure

   ```json
   {
     "title": "Adventure Bay Mystery",
     "language": "nl",
     "sections": [{ "anchor": "anchor001", "title": "The Beach", "text_file": "sections/001.md" }]
   }
   ```

3. **`cold/art_manifest.json`** — Asset mappings

   ```json
   {
     "assets": [
       {
         "anchor": "anchor001",
         "filename": "anchor001__plate__v1.png",
         "sha256": "abc123...",
         "approved_at": "2025-11-05T12:00:00Z",
         "provenance": {
           "role": "illustrator",
           "prompt_snippet": "Paw Patrol on beach, back view",
           "version": 1
         }
       }
     ]
   }
   ```

4. **`cold/fonts.json`** (optional) — Font declarations
5. **`cold/build.lock.json`** — Tool versions

### Gatekeeper Validation Rules

**MUST reject build if:**

- ❌ Any required Cold file missing
- ❌ Any file fails schema validation
- ❌ Any `sha256` in manifest doesn't match physical file
- ❌ Any `anchor` in `book.json` missing from `art_manifest.json`
- ❌ Any asset file referenced but not present in `assets/`

---

## Concrete Action Items

### Immediate (Week 1)

- [ ] **#1** Finalize Cold SoT file format schemas
  - `cold_manifest.schema.json`
  - `cold_book.schema.json`
  - `cold_art_manifest.schema.json`
  - Location: `03-schemas/`

- [ ] **#2** Create approval hook
  - On image approval: auto-write hash + rename file deterministically
  - Update `cold/art_manifest.json` immediately

- [ ] **#3** Implement `binder:verify` preflight
  - Enforce 1:1 mapping
  - Verify hash matches
  - Fail on mismatch with remediation steps

### Short-term (Weeks 2-4)

- [ ] **#4** Centralize Pandoc template
  - Pin `--resource-path`
  - Add CI test: open resulting EPUB on headless validator

- [ ] **#5** Pin PDF compositor
  - WeasyPrint stylesheet
  - Section-per-page enforced
  - Cover full-bleed page 1

- [ ] **#6** Create regression tests
  - **Kobo test:** Assert multiple images appear beyond cover
  - **Order test:** Anchors appear in manifest order; first `<img>` per section = manifest image
    (path + hash)
  - **No-heuristics test:** Disable directory globbing

### Medium-term (Weeks 5-8)

- [ ] **#7** Incident playbook
  - If build fails: (a) freeze Cold + manifests, (b) compute hashes, (c) never render/rename until
    hashes recorded
  - Location: `00-north-star/INCIDENT_RESPONSE.md`

- [ ] **#8** Build artifact shipping
  - Ship `build.json` alongside EPUB/PDF
  - Include all inputs' SHA-256

- [ ] **#9** Update role prompts
  - Showrunner/Gatekeeper: Reject non-compliant builds
  - Art Director/Illustrator: Return `(filename, sha256, anchor)` on approval
  - Binder: Inputs = Cold only; fail on unresolved references
  - Researcher/Policy: Default to back/¾ view for children

---

## Updated Role Contracts

### Showrunner

```diff
+ "Cold SoT is the only accepted source. No build shall proceed from non-Cold inputs."
+ "Before initiating Binder: verify cold/manifest.json exists and validates."
```

### Gatekeeper

```diff
+ "Reject any Binder request unless manifest_art.json exists with SHA-256 for every referenced plate."
+ "Each plate file must exist under assets/ with matching hash."
+ "If any mismatch → STOP and emit remediation steps. Do not attempt replacement or guessing."
+ "Block heuristics: missing files = build failure, not fallback."
```

### Art Director / Illustrator

```diff
+ "On approval, return (filename, sha256, anchor, provenance, version)."
+ "Filename must be deterministic: <anchor>__<role>__v<N>.png"
+ "No duplicate filenames allowed."
+ "Update cold/art_manifest.json immediately upon approval."
```

### Binder (Book Binder)

```diff
+ "Inputs: cold/book.json + cold/art_manifest.json ONLY."
+ "Output: EPUB + PDF + build.json"
+ "No other inputs permitted. Fail on unresolved references."
+ "No directory scans. No heuristics. No 'newest file wins'."
+ "Preflight: verify every anchor has exactly one approved plate with matching hash."
```

### Researcher / Policy

```diff
+ "Children's likeness: default to back/¾ view when in doubt."
+ "Persist this decision in provenance field of cold/art_manifest.json."
```

---

## Open Questions

1. **Asset versioning:** Should we vendor fonts/art into versioned archive per build, or keep in
   `assets/` with hashes only?

2. **Manifest merging:** If multiple art passes exist per anchor, do we need a manifest merger, or
   enforce single active plate per anchor?

3. **Canonical naming:** Confirm naming scheme `<anchor>__<role>__v<N>.png` to avoid accidental
   overwrites?

4. **Cold migration:** For legacy projects, create `cold-normalizer` tool to convert hot → cold
   format?

---

## Lessons Learned

### What We Learned

1. **Determinism requires discipline:** Heuristics destroy reproducibility
2. **Manifests are non-negotiable:** No build without manifest + hashes
3. **Environment resets are dangerous:** State must persist in files, not memory
4. **Multiple build paths = drift:** Enforce single canonical route
5. **Schema validation is a gate:** Not a nice-to-have

### What We'll Do Differently

1. **Hard stops:** Gatekeeper blocks non-compliant builds
2. **Hash discipline:** SHA-256 at approval time, always
3. **Single binder:** One path, manifest-driven
4. **Preflight checks:** Verify before build, not after
5. **Cold SoT format:** Explicit, versioned, schema-validated

---

## Related Documents

- **Quality Bars:** `00-north-star/QUALITY_BARS.md` → Add "Build Determinism" bar
- **Traceability:** `00-north-star/TRACEABILITY.md` → Add hash requirements
- **Binder Charter:** `01-roles/charters/book_binder.md` → Update inputs/outputs
- **Schemas:** `03-schemas/cold_*.schema.json` → Create new schemas
- **Protocol:** `04-protocol/INTENTS.md` → Add `binder.verify` intent

---

## Sign-Off

**Incident Owner:** Showrunner **Reviewed By:** Gatekeeper **Date:** 2025-11-05 **Status:** Systemic
fixes in progress

**Next Review:** After all action items complete (Week 8)

---

**Addendum: This post-mortem identifies a critical gap in the QuestFoundry specification—the Cold
SoT file format was not sufficiently explicit, and build validation gates were missing. The fixes
above will be incorporated into Layer 0 (policies), Layer 2 (artifact definitions), Layer 3
(schemas), and Layer 5 (prompts).**
