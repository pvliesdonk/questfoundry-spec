# Layer Analysis — Fix Proposal Implementation Review

**Date:** 2025-11-04 **Purpose:** Systematic review of each proposal to determine implementation
layer and identify information gaps before proceeding.

---

## QuestFoundry Architecture Layers

### Layer 0: Core Concepts (01-roles, 02-dictionary, 00-north-star)

- **Purpose:** Define roles, artifacts, bars, and foundational concepts
- **Examples:** role charters, artifact schemas, quality bars, spoiler hygiene
- **Change impact:** High (affects all downstream layers)

### Layer 1: Protocol (04-protocol)

- **Purpose:** Define message contracts, flows, lifecycles
- **Examples:** ENVELOPE.md, INTENTS.md, FLOWS/_.md, LIFECYCLES/_.md
- **Change impact:** Medium-High (affects role coordination)

### Layer 2: Prompts (05-prompts)

- **Purpose:** Role-specific operating instructions and intent handlers
- **Examples:** system_prompt.md, intent_handlers/\*.md
- **Change impact:** Medium (affects role behavior)

### Layer 3: Tools & Validation (tools/)

- **Purpose:** Scripts, validators, CI/QA automation
- **Examples:** build-kits, epub_validator (proposed)
- **Change impact:** Low-Medium (affects quality gates)

### Layer 4: Implementation (actual code/templates)

- **Purpose:** Concrete exporters, renderers, formatters
- **Examples:** EPUB generator, HTML templates, CSS
- **Change impact:** Low (isolated changes)

---

## Proposal Analysis

---

### PROPOSAL 1: Header Hygiene

**What:** Strip operational markers (Hub, Unofficial, Quick, etc.) from reader-facing section titles
during export.

**Layer Assignment:**

- **Primary:** Layer 2 (Prompts) — `book_binder/system_prompt.md`
- **Secondary:** Layer 3 (Tools) — CI/QA validation gate

**Current State:**

- Book Binder system_prompt.md exists (63 lines, concise)
- No explicit header sanitization rules currently documented
- Choice normalization rules exist (lines 27-36), can extend pattern

**Information Needed:**

1. ✅ **Marker list:** Hub, Unofficial, Quick, Temp, Draft, FLAG\_\*, CODEWORD (defined in proposal)
2. ❓ **Where do these markers come from?** Are they added by Plotwright, Scene Smith, or manually?
3. ❓ **Should sanitization happen at export time only, or also during Hot→Cold transition?**
4. ❓ **Are there legitimate reader-facing uses of these words (e.g., "The Hub" as a location
   name)?**

**Implementation Readiness:** 🟡 **Medium** — Need clarification on questions 2-4 before
implementing regex rules.

**Recommended Next Steps:**

1. Confirm source of markers (which role adds them, when)
2. Confirm sanitization timing (export only vs. Cold stabilization)
3. Add header sanitization section to `book_binder/system_prompt.md` (similar to existing choice
   normalization)
4. Add CI gate in `tools/validation/epub_validator.md` (regex match check)

---

### PROPOSAL 2: Choice UX Standardization

**What:** Standardize choice presentation — entire choice is link, no decorative arrows.

**Layer Assignment:**

- **Primary:** Layer 2 (Prompts) — `book_binder/system_prompt.md`
- **Secondary:** Layer 0 (Dictionary) — May need to update
  `02-dictionary/patterns/choice_presentation.md` if exists

**Current State:**

- Choice normalization rules **already exist** in `book_binder/system_prompt.md` lines 27-36
- Current rule: "Render all choices as bullets where the entire line is the link (no trailing arrows
  like `→`)"
- Normalization patterns documented: bullets ending with `→ [Text](#ID)` → rewrite to
  `- [Text](#ID)`

**Information Needed:**

1. ✅ **Target pattern:** Entire choice as link (already documented)
2. ❓ **Are these rules being followed?** Post-mortem suggests inconsistency — is this a
   _compliance_ issue or _specification_ gap?
3. ❓ **Where do non-compliant choices originate?** Scene Smith output? Manual edits?

**Implementation Readiness:** 🟢 **High** — Rules already exist, may just need enforcement/auditing.

**Recommended Next Steps:**

1. **Audit existing exports** to confirm non-compliance examples
2. **Enhance existing rules** with the detailed normalization table from proposal (lines 112-124 in
   fix_proposal.md)
3. Add validation check in CI gate (scan for remaining `→` in choice contexts)
4. Consider adding to `scene_smith/system_prompt.md` if Scene Smith is source of non-compliant
   patterns

---

### PROPOSAL 3: EPUB Kobo Compatibility

**What:** Add inline anchors, NCX, landmarks to fix Kobo Clara 2e link issues.

**Layer Assignment:**

- **Primary:** Layer 2 (Prompts) — `book_binder/system_prompt.md`
- **Secondary:** Layer 4 (Implementation) — EPUB generator templates (if separate from prompts)

**Current State:**

- Book Binder handles EPUB export (system_prompt.md line 23: "Render requested formats
  (Markdown/HTML/PDF/EPUB)")
- No mention of NCX, landmarks, or Kobo-specific compat in current prompt
- No intent handler for `format.render.md` found (only `view.export.md` and `format.render.md`
  exist)

**Information Needed:**

1. ✅ **Kobo issues:** Cross-file anchors, NCX, landmarks (detailed in post-mortem)
2. ❓ **How is EPUB currently generated?** Is it LLM-based (via prompts) or separate tooling?
3. ❓ **Where are EPUB templates stored?** Do we have access to modify them, or are they generated
   dynamically by Book Binder?
4. ❓ **NCX structure:** Can Book Binder generate XML, or does it need external tooling?

**Implementation Readiness:** 🟡 **Medium** — Need to understand EPUB generation mechanism before
implementing.

**Critical Questions:**

- **Is EPUB generation LLM-generated or template-based?**
  - If LLM: Add detailed instructions to `book_binder/system_prompt.md` or `format.render.md`
  - If template: Need to locate and modify EPUB templates (Layer 4)
- **Can current setup generate XML (NCX)?**
  - NCX is `toc.ncx` XML file — need to confirm Book Binder can create this

**Recommended Next Steps:**

1. **Locate EPUB generator** — check for existing templates or scripts
2. Read `format.render.md` intent handler to understand current EPUB generation flow
3. Test current EPUB output structure (unzip and inspect for nav.xhtml, content.opf, etc.)
4. Once generation mechanism is clear, add:
   - Twin anchor generation rules
   - NCX generation instructions
   - Landmarks/guide generation instructions

---

### PROPOSAL 4: ID Normalization & Alias Mapping

**What:** Normalize all anchor IDs to lowercase-dash format with alias mapping.

**Layer Assignment:**

- **Primary:** Layer 2 (Prompts) — `book_binder/system_prompt.md`
- **Secondary:** Layer 1 (Protocol) — May affect anchor contract in view.export

**Current State:**

- Existing anchor normalization: `S1′`, `S1p` → canonical `s1-return` (line 33)
- Anchor map validation exists in `view_log` artifact (02-dictionary/artifacts/view_log.md lines
  58-72)
- Current policy: "ASCII kebab-case" mentioned in view_log but not detailed in binder prompt

**Information Needed:**

1. ✅ **Normalization rules:** lowercase + dash-separation (defined in proposal)
2. ❓ **Who creates original IDs?** Plotwright? Scene Smith? Manual?
3. ❓ **Are IDs in Cold snapshot already normalized, or do they need runtime normalization?**
4. ❓ **Backward compatibility:** Do we need to preserve original IDs as secondary anchors, or just
   maintain alias map?

**Implementation Readiness:** 🟡 **Medium** — Need to understand ID lifecycle before implementing.

**Recommended Next Steps:**

1. Audit current anchor IDs in existing Cold snapshots (check case, underscore usage)
2. Determine if normalization should happen:
   - At Cold creation (Plotwright/Scene Smith output)
   - At export time (Book Binder transforms on-the-fly)
   - Both (normalize early, validate at export)
3. Enhance existing normalization rules in `book_binder/system_prompt.md`
4. Update `view_log` anchor map section to reflect normalization details

---

### PROPOSAL 5: CI/QA Validation Gates

**What:** Automated validation checks (cover policy, start page, anchor integrity, Kobo compat,
manifest compliance, header hygiene).

**Layer Assignment:**

- **Primary:** Layer 3 (Tools) — Create `tools/validation/epub_validator.md` (spec)
- **Secondary:** Layer 4 (Implementation) — Actual validator script (Python/Node/etc.)

**Current State:**

- No automated validation tooling found in `/tools/` directory
- Manual quality checks implied in Gatekeeper role (04-protocol/FLOWS/gatecheck.md)
- `view_log` artifact includes manual validation fields (Presentation, Accessibility bars)

**Information Needed:**

1. ✅ **Validation gates:** 6 gates defined in proposal (cover, start page, anchor, Kobo, manifest,
   header)
2. ❓ **Implementation language:** Python? Node? Shell script?
3. ❓ **Integration point:** Where does validator run? (CI pipeline? Pre-export? Post-export?)
4. ❓ **EPUB parsing:** Does validator need to unzip EPUB and parse XML/HTML? (requires library)

**Implementation Readiness:** 🟡 **Medium** — Specification is clear, but implementation requires
tooling decisions.

**Recommended Next Steps:**

1. **Phase 1:** Create specification document (`tools/validation/epub_validator.md`) ✅ (already in
   proposal)
2. **Phase 2:** Choose implementation approach:
   - Option A: Python with `lxml` + `zipfile` for EPUB parsing
   - Option B: Shell script with `unzip` + `xmllint` + `grep`
   - Option C: Node.js with `jszip` + `xml2js`
3. **Phase 3:** Integrate with Book Binder workflow (run validator after export, before handoff to
   PN)
4. **Phase 4:** Add CI integration (GitHub Actions, etc.)

**Defer to Phase 2+** unless user has strong preference on tooling now.

---

### PROPOSAL 6: Font Embedding (Typography Policy)

**What:** Embed Source Serif 4 + Cormorant Garamond in EPUBs with fallback strategy.

**Layer Assignment:**

- **Primary:** Layer 3 (Resources) — Create `/resources/fonts/` directory with README
- **Secondary:** Layer 2 (Prompts) — `book_binder/system_prompt.md` (font embedding logic)
- **Tertiary:** Layer 4 (Implementation) — CSS generation, EPUB font embedding

**Current State:**

- No `/resources/fonts/` directory exists
- No typography policy documented
- Book Binder prompt doesn't mention font embedding

**Information Needed:**

1. ✅ **Font choices:** Source Serif 4 (body), Cormorant Garamond (display) — both SIL OFL licensed
2. ❓ **Font acquisition:** Should we download fonts as part of setup, or expect user to provide?
3. ❓ **Embedding mechanism:** How does Book Binder include fonts in EPUB? (requires base64 encoding
   or file inclusion)
4. ❓ **CSS generation:** Is CSS template-based or dynamically generated?

**Implementation Readiness:** 🟡 **Medium** — Fonts are available (free), but embedding mechanism
unclear.

**Recommended Next Steps:**

1. **Phase 1:** Create `/resources/fonts/README.md` with typography policy ✅ (already in proposal)
2. **Phase 2:** Download fonts and place in `/resources/fonts/` directory structure
3. **Phase 3:** Update `book_binder/system_prompt.md` with font embedding instructions
4. **Phase 4:** Test EPUB with embedded fonts on multiple readers

**Decision needed:** Should fonts be committed to repo, or documented for user download?

---

### PROPOSAL 7A: Minimize JSON Exposure

**What:** Hide internal JSON from user-facing outputs; show clean prose/reports.

**Layer Assignment:**

- **Primary:** Layer 2 (Prompts) — `book_binder/system_prompt.md` (and potentially all role prompts)

**Current State:**

- Prompts use protocol envelopes extensively (04-protocol/ENVELOPE.md)
- View log format is markdown (02-dictionary/artifacts/view_log.md)
- No explicit "user communication style" guidance in prompts

**Information Needed:**

1. ✅ **Goal:** Hide JSON unless debugging (clear from proposal)
2. ❓ **Current behavior:** Do roles currently expose JSON to users? (not observed in examples)
3. ❓ **Scope:** Just Book Binder, or all roles?

**Implementation Readiness:** 🟢 **High** — Straightforward prompt enhancement.

**Recommended Next Steps:**

1. Add "User Communication & Output Format" section to `book_binder/system_prompt.md`
2. Consider adding to `_shared/human_interaction.md` for all roles
3. Provide good/bad examples in prompt

---

### PROPOSAL 7B: Metadata Auto-Generation

**What:** Centralize metadata (title, author, license, etc.) with fallback hierarchy and
auto-generation.

**Layer Assignment:**

- **Primary:** Layer 2 (Prompts) — `book_binder/system_prompt.md`
- **Secondary:** Layer 0 (Artifacts) — May need to define `project_metadata.json` schema in
  02-dictionary
- **Tertiary:** Layer 1 (Protocol) — May affect `view.export` payload

**Current State:**

- `front_matter` artifact exists (02-dictionary/artifacts/front_matter.md)
- Front matter includes: Title, Version, Snapshot, Options, Accessibility, Notes
- No `project_metadata.json` schema defined
- Metadata source hierarchy not documented

**Information Needed:**

1. ✅ **Metadata fields:** Title, author, license, description, subjects, language, date, UUID
   (defined in proposal)
2. ❓ **Where is project metadata currently stored?** Cold snapshot? Separate config file?
3. ❓ **Relationship to `front_matter` artifact:** Are these the same, or separate concerns?
4. ❓ **Auto-generation rules:** Extract from first H1, first paragraph — does Book Binder have
   access to full manuscript?

**Implementation Readiness:** 🟡 **Medium** — Need to clarify metadata storage and relationship to
existing artifacts.

**Recommended Next Steps:**

1. Review existing `front_matter` artifact and compare to proposal
2. Decide if `project_metadata.json` is new artifact or enhancement to existing
3. Update `book_binder/system_prompt.md` with metadata gathering hierarchy
4. Test metadata extraction from sample Cold snapshot

---

### PROPOSAL 7C: Cover Art Text Requirement & SVG Backup

**What:** Enforce title-bearing PNG as primary cover, SVG as backup; no textless covers in final
exports.

**Layer Assignment:**

- **Primary:** Layer 2 (Prompts) — `book_binder/system_prompt.md` + `art_director/system_prompt.md`
- **Secondary:** Layer 3 (Tools) — CI gate validation

**Current State:**

- No explicit cover policy documented in Book Binder prompt
- Post-mortem mentions cover policy already applied to "Midnight Deposition" exports
- Art manifest tracking mentioned in post-mortem (art_manifest.updated.json)

**Information Needed:**

1. ✅ **Cover requirements:** Title-bearing PNG + SVG backup (defined in proposal)
2. ❓ **Art manifest schema:** Where is `art_manifest.json` defined? (02-dictionary?)
3. ❓ **Who enforces cover policy?** Art Director (at creation) or Book Binder (at export)?
4. ❓ **Current cover handling:** How does Book Binder locate and include covers now?

**Implementation Readiness:** 🟡 **Medium** — Need art manifest schema and current cover handling
flow.

**Recommended Next Steps:**

1. Locate or create art manifest schema definition
2. Update `art_director/system_prompt.md` with title-bearing requirement
3. Update `book_binder/system_prompt.md` with cover validation and export logic
4. Add CI gate for cover policy validation

---

### PROPOSAL 7D: Typography Decisions via Style Lead

**What:** Move font decisions from Book Binder to Style Lead via `style_manifest.json`.

**Layer Assignment:**

- **Primary:** Layer 2 (Prompts) — `style_lead/system_prompt.md` (create manifest) +
  `book_binder/system_prompt.md` (consume manifest)
- **Secondary:** Layer 0 (Artifacts) — Define `style_manifest.json` schema in 02-dictionary

**Current State:**

- Style Lead prompt exists (05-prompts/style_lead/system_prompt.md)
- No mention of typography specification in current prompt
- No `style_manifest.json` schema defined

**Information Needed:**

1. ✅ **Typography scope:** Prose, display, cover, UI (defined in proposal)
2. ✅ **Manifest schema:** Defined in proposal (lines 912-946 in fix_proposal.md)
3. ❓ **When does Style Lead create manifest?** During style stabilization loop?
4. ❓ **Default typography:** If manifest missing, what defaults should Book Binder use?

**Implementation Readiness:** 🟢 **High** — Schema is well-defined, just needs prompt integration.

**Recommended Next Steps:**

1. Define `style_manifest.json` artifact in `02-dictionary/artifacts/style_manifest.md`
2. Update `style_lead/system_prompt.md` to include typography specification section
3. Update `book_binder/system_prompt.md` to read and apply style manifest
4. Test with and without manifest (fallback behavior)

---

### PROPOSAL 7E: Art Director Filename Conventions

**What:** When using `image_gen.text2im`, filenames must match art manifest entries.

**Layer Assignment:**

- **Primary:** Layer 2 (Prompts) — `art_director/system_prompt.md` + `illustrator/system_prompt.md`
- **Secondary:** Layer 0 (Artifacts) — Art manifest schema (if not already defined)

**Current State:**

- Art Director and Illustrator prompts exist
- Post-mortem mentions art manifest with filenames and SHA-256 hashes
- `image_gen.text2im` is external tool (ChatGPT)

**Information Needed:**

1. ✅ **Filename pattern:** `{role}_{section_id}_{variant}.{ext}` (defined in proposal)
2. ❓ **Art manifest location/schema:** Where is it defined?
3. ❓ **Who updates manifest?** Art Director (planning) or Illustrator (after rendering)?
4. ❓ **Hash computation:** How are SHA-256 hashes computed? (manual tool? automated?)

**Implementation Readiness:** 🟢 **High** — Clear filename convention, just needs prompt
documentation.

**Recommended Next Steps:**

1. Locate or create art manifest schema definition
2. Update `art_director/system_prompt.md` with filename conventions and workflow
3. Update `illustrator/system_prompt.md` with renderer integration notes
4. Add manifest validation to CI (check filename consistency, hashes)

---

### PROPOSAL 8: Showrunner Initial Setup Flow

**What:** Guided 6-step onboarding for new projects (genre, title, length, style, licensing).

**Layer Assignment:**

- **Primary:** Layer 2 (Prompts) — `showrunner/system_prompt.md`
- **Secondary:** Layer 1 (Protocol) — Create `project.init` intent flow
- **Tertiary:** Layer 0 (Artifacts) — Define `project_metadata.json` schema

**Current State:**

- Showrunner prompt exists (05-prompts/showrunner/system_prompt.md, 83 lines)
- No project initialization flow documented
- No `project.init` intent in protocol (04-protocol/INTENTS.md)
- No `project_metadata.json` schema defined

**Information Needed:**

1. ✅ **Setup flow:** 6 steps defined in proposal (genre → title → length → style → licensing →
   confirm)
2. ❓ **Trigger:** How does Showrunner detect "new project" vs. "resume existing"?
3. ❓ **Storage:** Where is `project_metadata.json` stored? (repo root? /project/?)
4. ❓ **Handoff:** After init, does Showrunner automatically start Lore Deepening / Story Spark, or
   wait for user?

**Implementation Readiness:** 🟡 **Medium** — Flow is well-defined, but needs protocol integration.

**Recommended Next Steps:**

1. **Define `project_metadata.json` schema** in `02-dictionary/artifacts/` (or `/project/` if
   different namespace)
2. **Add `project.init` intent** to `04-protocol/INTENTS.md`
3. **Create flow document** `04-protocol/FLOWS/project_init.md` (similar to binding_run.md)
4. **Update `showrunner/system_prompt.md`** with initialization flow section
5. **Create intent handler** `05-prompts/showrunner/intent_handlers/project.init.md`
6. **Test** with new project (no existing metadata) and existing project (metadata present)

---

## Summary: Implementation Readiness by Proposal

| Proposal                          | Layer                                   | Readiness | Blockers                               | Priority    |
| --------------------------------- | --------------------------------------- | --------- | -------------------------------------- | ----------- |
| **1. Header Hygiene**             | L2 Prompts                              | 🟡 Medium | Source of markers, sanitization timing | P1 High     |
| **2. Choice UX**                  | L2 Prompts                              | 🟢 High   | None (rules exist, need enforcement)   | P1 High     |
| **3. EPUB Kobo Compat**           | L2 Prompts / L4 Impl                    | 🟡 Medium | **EPUB generation mechanism unclear**  | P0 Critical |
| **4. ID Normalization**           | L2 Prompts                              | 🟡 Medium | ID lifecycle, normalization timing     | P2 Medium   |
| **5. CI/QA Gates**                | L3 Tools                                | 🟡 Medium | Tooling choice (Python/Node/Shell)     | P2 Medium   |
| **6. Font Embedding**             | L3 Resources / L2 Prompts               | 🟡 Medium | Font acquisition, embedding mechanism  | P3 Low      |
| **7A. JSON Exposure**             | L2 Prompts                              | 🟢 High   | None                                   | P2 Medium   |
| **7B. Metadata Auto-Gen**         | L2 Prompts / L0 Artifacts               | 🟡 Medium | Relationship to front_matter artifact  | P1 High     |
| **7C. Cover Policy**              | L2 Prompts / L3 Tools                   | 🟡 Medium | Art manifest schema location           | P2 Medium   |
| **7D. Typography via Style Lead** | L2 Prompts / L0 Artifacts               | 🟢 High   | None (schema defined)                  | P3 Low      |
| **7E. Art Filename Conventions**  | L2 Prompts                              | 🟢 High   | None (clear convention)                | P3 Low      |
| **8. Showrunner Init Flow**       | L2 Prompts / L1 Protocol / L0 Artifacts | 🟡 Medium | Protocol integration, metadata schema  | P1 High     |

---

## Critical Information Gaps (Must Resolve Before Implementation)

### 🔴 **Blocker: EPUB Generation Mechanism (Proposal 3)**

**Question:** How are EPUBs currently generated?

- Is it LLM-generated (Book Binder writes EPUB content via prompts)?
- Is it template-based (separate EPUB generator tool)?
- Is it hybrid (Book Binder orchestrates external tool)?

**Impact:** Cannot implement Kobo compatibility (NCX, landmarks, inline anchors) without
understanding generation mechanism.

**Action:** Read `format.render.md` intent handler and/or search for EPUB-related code/templates.

---

### 🟡 **Important: Artifact Schemas**

**Missing schemas:**

1. `project_metadata.json` (Proposal 8, affects 7B)
2. `art_manifest.json` (Proposal 7C, 7E)
3. `style_manifest.json` (Proposal 7D)

**Action:** Create artifact definitions in `02-dictionary/artifacts/` before implementing prompts.

---

### 🟡 **Important: Anchor ID Lifecycle**

**Questions:**

- Who creates original anchor IDs? (Plotwright? Scene Smith?)
- When should normalization happen? (Hot? Cold transition? Export?)
- Are IDs in current Cold snapshots already normalized?

**Action:** Audit existing Cold snapshot to see current ID formats.

---

### 🟡 **Important: Metadata Storage & Front Matter**

**Questions:**

- Is `project_metadata.json` separate from `front_matter` artifact?
- Where is project metadata currently stored?
- Does `front_matter` already contain metadata fields from Proposal 7B?

**Action:** Compare `front_matter.md` artifact schema to proposed `project_metadata.json` schema.

---

## Recommended Implementation Order (Revised Based on Readiness)

### Phase 1: Quick Wins (High Readiness, High/Medium Priority)

1. **Proposal 7A: JSON Exposure** 🟢 P2 — Add to `book_binder/system_prompt.md` (clean user outputs)
2. **Proposal 2: Choice UX** 🟢 P1 — Enhance existing rules, add CI gate
3. **Proposal 7D: Typography via Style Lead** 🟢 P3 — Define artifact, update prompts
4. **Proposal 7E: Art Filename Conventions** 🟢 P3 — Update art_director/illustrator prompts

### Phase 2: Artifact Definitions (Enables Multiple Proposals)

5. **Define `project_metadata.json`** (enables Proposals 7B, 8)
6. **Define `art_manifest.json`** (enables Proposals 7C, 7E)
7. **Define `style_manifest.json`** (enables Proposal 7D)

### Phase 3: Protocol & Schema Integration

8. **Proposal 8: Showrunner Init Flow** 🟡 P1 — Add protocol intent, create flow, update prompt
9. **Proposal 7B: Metadata Auto-Gen** 🟡 P1 — Integrate with project_metadata and front_matter

### Phase 4: EPUB & Validation (After Resolving Blockers)

10. **Resolve EPUB generation mechanism** (blocker for Proposal 3)
11. **Proposal 3: EPUB Kobo Compat** 🟡 P0 — Add NCX, landmarks, inline anchors
12. **Proposal 5: CI/QA Gates** 🟡 P2 — Create validator spec, implement tooling

### Phase 5: Remaining Proposals

13. **Proposal 1: Header Hygiene** 🟡 P1 — Clarify marker sources, add sanitization
14. **Proposal 4: ID Normalization** 🟡 P2 — Clarify ID lifecycle, add normalization
15. **Proposal 7C: Cover Policy** 🟡 P2 — Integrate art manifest, enforce policy
16. **Proposal 6: Font Embedding** 🟡 P3 — Acquire fonts, add embedding logic

---

## Questions for User

Before proceeding with implementation, please clarify:

### Critical (Blockers)

1. **EPUB Generation:** How are EPUBs currently generated? LLM-based (via prompts) or separate
   tooling?

### Important (Affects Multiple Proposals)

2. **Artifact Schemas:** Should I create `project_metadata.json`, `art_manifest.json`,
   `style_manifest.json` schemas in `02-dictionary/artifacts/` first?
3. **Metadata vs. Front Matter:** Is `project_metadata.json` (Proposal 8) the same as or different
   from `front_matter` artifact?
4. **Anchor IDs:** When should ID normalization happen? (Hot creation? Cold transition? Export?)

### Clarifying (Affects Specific Proposals)

5. **Header Markers:** Which role adds Hub/Unofficial/Quick markers? (Plotwright? Scene Smith?
   Manual?)
6. **Font Acquisition:** Should fonts be downloaded and committed to repo, or documented for user
   download?
7. **CI Tooling:** Preference for validator implementation? (Python? Node.js? Shell script?)

### Process

8. **Implementation Approach:** Should I proceed with Phase 1 (quick wins) while we resolve
   blockers, or wait for full clarity?
9. **Testing:** Do you have access to a test project / Cold snapshot I can use to validate changes?

---

## Conclusion

**8 proposals analyzed across 5 architecture layers.**

**Readiness:**

- 🟢 **4 proposals ready** (high readiness, can implement immediately)
- 🟡 **8 proposals need clarification** (medium readiness, require answers to proceed)

**Critical blocker:** EPUB generation mechanism (Proposal 3, P0 Critical).

**Recommended:** Start with **Phase 1 Quick Wins** (4 proposals) while resolving critical questions
for later phases.
