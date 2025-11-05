# Fix Proposal — "Midnight Deposition" Post-Mortem Action Items

**Date:** 2025-11-04 **Status:** PROPOSAL (awaiting approval) **Related:**
`2025-11-04_midnight_deposition.md` (§8, §10, §11)

---

## Overview

This document proposes specific code/prompt changes to address the 11 action items from the
"Midnight Deposition" post-mortem. All fixes target **Book Binder** prompt logic and export
templates, with QA/CI validation rules to prevent regression.

---

## Fix Categories

1. **Header Hygiene** — Strip operational markers from reader-facing titles
2. **Choice UX Standardization** — Unified link presentation
3. **EPUB Kobo Compatibility** — Inline anchors, NCX, landmarks
4. **ID Normalization** — Lowercase-dash IDs with alias mapping
5. **CI/QA Gates** — Automated validation

---

## PROPOSAL 1: Header Hygiene (Binder)

### Problem

Section headers contain operational markers like "Hub," "Unofficial," "Quick," "Temp," "Draft" that
leak process into reader-facing prose.

**Example bad headers:**

```markdown
## Hub: Dock Seven

## Quick: Decision Point

## Unofficial: Alternate Path
```

**Expected good headers:**

```markdown
## Dock Seven

## Decision Point

## Alternate Path
```

### Proposed Fix

**File:** `/05-prompts/book_binder/system_prompt.md`

**Location:** Add to "Export Normalization Rules" section (after anchor normalization)

```markdown
### Header Sanitization

Strip operational markers from reader-facing section titles during export:

**Markers to Remove:**

- Prefixes: `Hub:`, `Unofficial:`, `Quick:`, `Temp:`, `Draft:`, `FLAG_*:`, `CODEWORD:`
- Pattern: `^(Hub|Unofficial|Quick|Temp|Draft|FLAG_\w+|CODEWORD):\s*`

**Implementation:**

1. Scan all H2 headers in manuscript sections
2. Apply regex replacement: `^(Hub|Unofficial|Quick|Temp|Draft|FLAG_\w+|CODEWORD):\s*` → ``
3. Preserve markers in:
   - Section IDs (e.g., `hub-dock-seven` remains)
   - Developer notes
   - Internal documentation

**Example:**
```

INPUT: ## Hub: Dock Seven OUTPUT: ## Dock Seven ID: hub-dock-seven (preserved)

```

**Validation:**
- Log count of sanitized headers in `view_log`
- Fail export if markers remain after sanitization (indicates regex error)
```

**File:** `/05-prompts/book_binder/intent_handlers/format.render.md`

**Location:** Add to "Pre-Render Validation" checklist

```markdown
- [ ] Apply header sanitization (strip Hub/Unofficial/Quick/Temp/Draft prefixes)
- [ ] Verify no operational markers remain in exported section titles
- [ ] Log sanitization count in view_log
```

---

## PROPOSAL 2: Choice UX Standardization (Binder)

### Problem

Inconsistent choice presentation:

- Sometimes: entire choice is a link (good)
- Sometimes: label with trailing arrow `→ [Link](#id)` (confusing)

### Proposed Fix

**File:** `/05-prompts/book_binder/system_prompt.md`

**Location:** Enhance existing "Choice Normalization" section

**Current rule:**

```markdown
- Bullets ending with → [Text](#ID) → rewrite to - [Text](#ID)
- Bullets with prose + inline link → collapse to link-only, keep link text
```

**Enhanced rule:**

```markdown
### Choice Link Normalization

**Standard:** Entire choice text is the link (no decorative arrows).

**Patterns to normalize:**

| Input Pattern                            | Output               | Notes                                  |
| ---------------------------------------- | -------------------- | -------------------------------------- |
| `- Prose → [Link Text](#id)`             | `- [Link Text](#id)` | Remove prose + arrow                   |
| `- [Link Text](#id) →`                   | `- [Link Text](#id)` | Remove trailing arrow                  |
| `- Prose [Link](#id) more prose`         | `- [Link](#id)`      | Collapse to link only, use link's text |
| `- Multiple [Link1](#a) and [Link2](#b)` | Keep as-is           | Multi-link choices allowed             |

**Algorithm:**

1. For each bullet list item in a choice block
2. If pattern matches `prose → [link](#id)` or `[link](#id) →`:
   - Extract link text and target
   - Replace entire line with `- [link text](#id)`
3. If multiple links in one bullet: preserve as-is (valid multi-option)
4. If no links: preserve as narrative text (not a choice)

**Validation:**

- Count normalized choices in view_log
- Flag any remaining `→` in choice contexts for manual review
```

**File:** `/05-prompts/book_binder/intent_handlers/format.render.md`

**Location:** Add to "Choice Rendering" section

```markdown
### Choice Rendering (All Formats)

1. Apply choice link normalization (entire line as link, no arrows)
2. Validate all choice links resolve to valid anchors
3. Log normalization count in view_log

**HTML/EPUB:** Render as `<li><a href="#target">Choice text</a></li>` **Markdown:** Render as
`- [Choice text](#target)` **PDF:** Render as clickable text with underline/color (via HTML)
```

---

## PROPOSAL 3: EPUB Kobo Compatibility (Critical)

### Problem

EPUBs work on mobile readers but fail on **Kobo Clara 2e**:

- Cross-file anchor links don't trigger
- Missing legacy navigation (NCX)
- No EPUB2 landmarks/guide

### Proposed Fix (Multi-Part)

#### 3A: Inline Anchor Spans

**File:** `/05-prompts/book_binder/system_prompt.md`

**Location:** Add new section "EPUB Anchor Generation"

````markdown
### EPUB Anchor Generation (Kobo Compatibility)

**Problem:** Kobo devices require explicit inline anchor elements, not just `id` attributes on block
elements.

**Solution: Twin Anchors**

For every section with an anchor ID, generate both:

1. Block-level `id` on `<section>` or `<h2>` (standard EPUB3)
2. Inline `<a>` or `<span>` immediately inside the section (Kobo compat)

**Implementation:**

```html
<!-- EPUB3 Standard (works on most readers) -->
<section id="dock-seven">
  <h2>Dock Seven</h2>
  ...
</section>

<!-- Kobo Compatible (works everywhere) -->
<section id="dock-seven">
  <a id="dock-seven"></a>
  <h2>Dock Seven</h2>
  ...
</section>
```
````

**Template for All Sections:**

```html
<section id="{section-id}">
  <a id="{section-id}"></a>
  <h2>{section-title}</h2>
  {content}
</section>
```

**Validation:**

- Verify every section has both block ID and inline anchor
- Log dual-anchor count in view_log

````

#### 3B: Legacy NCX Navigation

**File:** `/05-prompts/book_binder/system_prompt.md`

**Location:** Add new section "EPUB2 Legacy Navigation"

```markdown
### EPUB2 Legacy Navigation (NCX)

**Problem:** Kobo devices prefer EPUB2 NCX (`toc.ncx`) alongside EPUB3 `nav.xhtml`.

**Solution: Generate Both**

**NCX Structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="{book-uuid}"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>{Book Title}</text>
  </docTitle>
  <navMap>
    <navPoint id="section-001" playOrder="1">
      <navLabel>
        <text>{Section Title}</text>
      </navLabel>
      <content src="001.xhtml"/>
    </navPoint>
    <!-- Repeat for all sections -->
  </navMap>
</ncx>
````

**Manifest Entry:**

```xml
<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
```

**Spine Reference:**

```xml
<spine toc="ncx">
  <itemref idref="section-001"/>
  <!-- etc -->
</spine>
```

**Validation:**

- Verify NCX includes all spine items in reading order
- Verify playOrder is sequential 1..N
- Log NCX generation in view_log

````

#### 3C: EPUB Landmarks & Guide

**File:** `/05-prompts/book_binder/system_prompt.md`

**Location:** Add new section "EPUB Landmarks"

```markdown
### EPUB Landmarks & Guide

**Problem:** Kobo devices use landmarks for navigation and start position.

**Solution: ARIA Landmarks + EPUB2 Guide**

**ARIA Landmarks (in `nav.xhtml`):**
```html
<nav epub:type="landmarks" hidden="">
  <h2>Guide</h2>
  <ol>
    <li><a epub:type="cover" href="cover.xhtml">Cover</a></li>
    <li><a epub:type="toc" href="nav.xhtml">Table of Contents</a></li>
    <li><a epub:type="bodymatter" href="001.xhtml">Start of Content</a></li>
  </ol>
</nav>
````

**EPUB2 Guide (in `content.opf`):**

```xml
<guide>
  <reference type="cover" title="Cover" href="cover.xhtml"/>
  <reference type="toc" title="Table of Contents" href="nav.xhtml"/>
  <reference type="text" title="Start" href="001.xhtml"/>
</guide>
```

**Reading Order Policy:**

- Cover: `cover.xhtml` (title-bearing PNG)
- TOC: `nav.xhtml` (NOT in spine)
- Start: First scene section (e.g., `001.xhtml`)
- Frontmatter: copyright.xhtml, etc. (in spine but not start point)

**Validation:**

- Verify landmarks match spine items
- Verify `epub:type="bodymatter"` points to first scene (not TOC)
- Log landmark count in view_log

````

---

## PROPOSAL 4: ID Normalization & Alias Mapping

### Problem
Mixed-case and underscore IDs may cause issues on Kobo; also, legacy aliases (`S1′`, `S1p`) need mapping.

### Proposed Fix

**File:** `/05-prompts/book_binder/system_prompt.md`

**Location:** Enhance "Anchor Alias Normalization" section

**Current rule:**
```markdown
- S1′, S1p, variants → canonical s1-return
````

**Enhanced rule:**

````markdown
### Anchor ID Normalization & Aliasing

**Standard Format:** `lowercase-dash-separated` (ASCII-safe, Kobo-compatible)

**Normalization Rules:**

| Input Format              | Normalized   | Alias Mapping              |
| ------------------------- | ------------ | -------------------------- |
| `Section_1`, `Section-1`  | `section-1`  | `Section_1` → `section-1`  |
| `S1′`, `S1p`, `S1'`       | `s1-return`  | All variants → `s1-return` |
| `DockSeven`, `Dock_Seven` | `dock-seven` | Case variants aliased      |
| `A1_H`, `a1_h`            | `a1-h`       | Underscores to dashes      |

**Algorithm:**

1. Convert all IDs to lowercase
2. Replace underscores with dashes
3. Remove apostrophes/primes (', ′)
4. Generate alias map for backward compatibility

**Alias Map (JSON):**

```json
{
  "S1′": "s1-return",
  "S1p": "s1-return",
  "Section_1": "section-1",
  "DockSeven": "dock-seven",
  "A1_H": "a1-h"
}
```
````

**Link Rewriting:**

- Before export, rewrite all `href="#OldID"` to `href="#new-id"`
- Preserve original IDs as secondary anchors (twin IDs for compat)

**Validation:**

- Log alias count in view_log
- Verify 0 collisions after normalization
- Test all cross-file links resolve to normalized IDs

````

**File:** `/05-prompts/book_binder/intent_handlers/format.render.md`

**Location:** Add to "Anchor Processing" section

```markdown
### Anchor ID Processing

1. Apply ID normalization (lowercase-dash)
2. Generate alias map for legacy IDs
3. Rewrite all internal links to use normalized IDs
4. (Optional) Add secondary inline anchors with legacy IDs for backward compat
5. Validate 0 collisions, 0 orphaned links
6. Log normalization count and alias map in view_log
````

---

## PROPOSAL 5: CI/QA Validation Gates

### Problem

Manual validation is error-prone; need automated checks to enforce policies.

### Proposed Fix

**File:** Create `/spec-tools/validation/epub_validator.md` (specification for future implementation)

```markdown
# EPUB Validator — CI/QA Gates

## Purpose

Automated validation to enforce post-mortem policies and prevent regression.

---

## Gate 1: Cover Policy

**Rule:** Final EPUB must use a title-bearing PNG as designated cover-image.

**Checks:**

- [ ] `content.opf` has `<meta name="cover" content="cover-image"/>`
- [ ] Cover image is PNG format
- [ ] Cover image metadata includes "title-bearing: true" or filename matches `*_titled.png`
- [ ] Optional SVG backup present in manifest (not required to pass)

**Failure:** Block export; warn user to provide titled cover.

---

## Gate 2: Start Page Invariant

**Rule:** Reading order begins at first scene; frontmatter not in spine start.

**Checks:**

- [ ] First `<itemref>` in spine is a scene section (matches pattern `^\d{3}\.xhtml$`)
- [ ] TOC/nav.xhtml has `linear="no"` attribute (not in reading flow)
- [ ] Frontmatter (copyright, etc.) appears in spine but AFTER first scene OR has `linear="no"`

**Failure:** Block export; log incorrect spine order.

---

## Gate 3: Anchor Integrity

**Rule:** Every link target must exist; every section must have inline anchor.

**Checks:**

- [ ] Parse all `href="#id"` and `href="file.xhtml#id"` links
- [ ] Verify each target ID exists in referenced file
- [ ] Verify each section has both `<section id="x">` AND `<a id="x"></a>` (twin anchors)
- [ ] Count orphaned links (broken references)
- [ ] Count collisions (duplicate IDs)

**Failure:** Block export if orphans > 0 or collisions > 0; log details.

---

## Gate 4: Kobo Compatibility

**Rule:** EPUB must include Kobo-specific navigation and anchor patterns.

**Checks:**

- [ ] `toc.ncx` file present in manifest (`application/x-dtbncx+xml`)
- [ ] `toc.ncx` includes all spine items with sequential `playOrder`
- [ ] ARIA landmarks present in `nav.xhtml` (cover, toc, bodymatter)
- [ ] (Optional) EPUB2 `<guide>` present in `content.opf`
- [ ] All sections have inline anchor spans (`<a id="..."></a>`)

**Failure:** Warn (non-blocking) if NCX/landmarks missing; block if inline anchors missing.

---

## Gate 5: Manifest Compliance (Art)

**Rule:** All images must be listed in art manifest with captions and hashes.

**Checks:**

- [ ] Parse all `<img src="...">` tags in EPUB
- [ ] Verify each image path exists in `art_manifest.updated.json`
- [ ] Verify each image has non-empty `caption` field
- [ ] Verify each image has SHA-256 hash
- [ ] (Optional) Recompute hash and verify against manifest

**Failure:** Warn if caption missing; block if image not in manifest.

---

## Gate 6: Header Hygiene

**Rule:** Reader-facing section titles must not contain operational markers.

**Checks:**

- [ ] Parse all `<h2>` (sections) and `<h1>` (title) in EPUB
- [ ] Regex match: `(Hub|Unofficial|Quick|Temp|Draft|FLAG_\w+|CODEWORD):\s`
- [ ] Count matches (should be 0)

**Failure:** Block export if count > 0; log offending headers.

---

## Implementation Notes

This specification should be implemented as a Python/Node.js script or integrated into the Book
Binder export flow as validation steps.

**Suggested Flow:**

1. Book Binder generates EPUB
2. Run validator script: `./spec-tools/validation/epub_validator.py book.epub`
3. Validator outputs: PASS / WARN / FAIL with detailed report
4. Append validator report to `view_log`
5. If FAIL: block delivery to Production Nexus
6. If PASS/WARN: proceed with handoff

**Future Work:**

- Integrate into CI pipeline (GitHub Actions, etc.)
- Add HTML/Markdown validators with similar gates
- Generate badge/status for README
```

---

## PROPOSAL 6: Font Embedding (Typography Policy)

### Problem

No agreed typeface; need embeddable fonts for EPUB.

### Proposed Fix

**File:** Create `/resources/fonts/README.md`

```markdown
# Typography Policy

## Fonts for EPUB/HTML Exports

**Body Text:** Source Serif 4 **Display Titles:** Cormorant Garamond OR Playfair Display
**License:** SIL Open Font License (embeddable)

---

## Directory Structure
```

/resources/fonts/ source-serif-4/ SourceSerif4-Regular.otf SourceSerif4-Italic.otf
SourceSerif4-Bold.otf SourceSerif4-BoldItalic.otf LICENSE.txt cormorant-garamond/
CormorantGaramond-Regular.ttf CormorantGaramond-Italic.ttf CormorantGaramond-Bold.ttf LICENSE.txt

````

---

## EPUB CSS Template

```css
@font-face {
  font-family: 'Source Serif 4';
  src: url('../fonts/SourceSerif4-Regular.otf');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'Source Serif 4';
  src: url('../fonts/SourceSerif4-Italic.otf');
  font-weight: normal;
  font-style: italic;
}

@font-face {
  font-family: 'Cormorant Garamond';
  src: url('../fonts/CormorantGaramond-Regular.ttf');
  font-weight: normal;
  font-style: normal;
}

body {
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 1em;
  line-height: 1.6;
}

h1, h2, h3 {
  font-family: 'Cormorant Garamond', Georgia, serif;
}
````

---

## Fallback Strategy

If fonts not available:

- Body: Georgia, Times New Roman, serif
- Display: Georgia, serif

Book Binder should check `/resources/fonts/` and embed if present; otherwise use fallback fonts.

````

**File:** `/05-prompts/book_binder/system_prompt.md`

**Location:** Add new section "Typography & Font Embedding"

```markdown
### Typography & Font Embedding

**Policy:** Use free, embeddable fonts for consistent rendering across devices.

**Fonts:**
- Body: Source Serif 4 (SIL OFL)
- Display: Cormorant Garamond (SIL OFL)

**Implementation:**
1. Check if fonts exist in `/resources/fonts/`
2. If present: embed in EPUB; include `@font-face` CSS
3. If absent: use system fallback (Georgia, Times New Roman, serif)
4. Log font embedding status in view_log

**CSS Template:** See `/resources/fonts/README.md`

**Validation:**
- Verify embedded fonts are licensed for distribution
- Test rendering on major EPUB readers (Apple Books, Kobo, Kindle)
````

---

## Implementation Priority

| Priority        | Fix                                               | Files to Modify                                                | Complexity | Impact                     |
| --------------- | ------------------------------------------------- | -------------------------------------------------------------- | ---------- | -------------------------- |
| **P0 Critical** | EPUB Kobo Compat (inline anchors, NCX, landmarks) | `book_binder/system_prompt.md`, `format.render.md`             | High       | Fixes broken links on Kobo |
| **P1 High**     | Header Hygiene                                    | `book_binder/system_prompt.md`, `format.render.md`             | Low        | Prevents process leakage   |
| **P1 High**     | Choice UX Standardization                         | `book_binder/system_prompt.md`, `format.render.md`             | Low        | Improves reader UX         |
| **P2 Medium**   | ID Normalization                                  | `book_binder/system_prompt.md`, `format.render.md`             | Medium     | Better Kobo compat         |
| **P2 Medium**   | CI/QA Gates                                       | Create `/spec-tools/validation/epub_validator.md`                   | Medium     | Prevents regression        |
| **P3 Low**      | Font Embedding                                    | Create `/resources/fonts/README.md`, update `system_prompt.md` | Low        | Typography consistency     |

---

## Summary of Files to Create/Modify

### Files to Modify

1. `/05-prompts/book_binder/system_prompt.md`
   - Add: Header Sanitization rules
   - Add: Choice Link Normalization (enhanced)
   - Add: EPUB Anchor Generation (twin anchors)
   - Add: EPUB2 Legacy Navigation (NCX)
   - Add: EPUB Landmarks & Guide
   - Add: ID Normalization & Aliasing (enhanced)
   - Add: Typography & Font Embedding

2. `/05-prompts/book_binder/intent_handlers/format.render.md`
   - Add: Header sanitization to pre-render checklist
   - Add: Choice rendering standardization
   - Add: Anchor processing (normalization + twin anchors)
   - Add: NCX generation
   - Add: Landmarks generation

### Files to Create

3. `/spec-tools/validation/epub_validator.md`
   - Specification for CI/QA gates

4. `/resources/fonts/README.md`
   - Typography policy and font embedding guide

---

## Testing Plan

After implementation:

1. **Unit Tests** (manual for LLM-based system):
   - Test header sanitization with sample headers
   - Test choice normalization with various patterns
   - Test ID normalization with edge cases (underscores, primes, mixed case)

2. **Integration Tests:**
   - Generate EPUB from "Midnight Deposition" cold snapshot
   - Validate with `epub_validator` (all gates pass)
   - Test on devices:
     - Kobo Clara 2e (primary target)
     - Apple Books (iOS/macOS)
     - Calibre (desktop)
     - Browser-based reader (Readium, etc.)

3. **Regression Tests:**
   - Re-export previous EPUBs with new rules
   - Verify no broken links
   - Verify no missing content

4. **Device-Specific Tests (Kobo Clara 2e):**
   - Open EPUB on device
   - Test cross-file anchor links (click choice links)
   - Test TOC navigation (NCX)
   - Verify start page is first scene (not TOC)

---

## Rollout Strategy

1. **Phase 1:** Implement P0 (Kobo compat) + P1 (header hygiene, choice UX)
2. **Phase 2:** Implement P2 (ID normalization, CI gates)
3. **Phase 3:** Implement P3 (font embedding)
4. **Phase 4:** Test on Kobo Clara 2e; iterate based on findings
5. **Phase 5:** Update documentation and "USAGE_GUIDE.md"

---

## Open Questions

1. **Single-file EPUB variant:** Should we generate a Kobo-optimized single-file spine variant as
   mentioned in post-mortem §6.5? (Defer to Phase 4 testing)

2. **Alias backward compat:** Should we add secondary inline anchors with legacy IDs
   (`<a id="S1p"></a>` alongside `<a id="s1-return"></a>`) for external links? (Recommend: yes,
   minimal cost)

3. **NCX depth:** Post-mortem specifies `depth="1"` (flat TOC). Should we support nested sections in
   future? (Recommend: defer until multi-chapter books)

4. **PDF rendering:** PDF currently inherits HTML structure. Should we add PDF-specific formatting
   (page breaks, headers/footers)? (Recommend: separate proposal)

---

## PROPOSAL 7: Additional Refinements (User Feedback)

### 7A: Minimize JSON Exposure in Prompts

**Problem:** Book Binder prompts/outputs show too much JSON to users; should keep internal
representation hidden unless debugging.

**Proposed Fix:**

**File:** `/05-prompts/book_binder/system_prompt.md`

**Location:** Add to "User Communication" section (or create if missing)

```markdown
### User Communication & Output Format

**Principle:** Keep internal JSON representation hidden from user-facing outputs.

**Rules:**

1. **Protocol messages** (intents, artifacts) are internal—never show JSON to users unless:
   - User explicitly requests debug output
   - Error diagnostics require showing message structure
   - Developer mode is active

2. **Export outputs** should be clean prose/reports:
   - View log: formatted markdown table/list (not raw JSON)
   - Anchor map: human-readable summary (e.g., "45 anchors resolved, 0 orphans")
   - Validation results: prose description with counts/lists

3. **Error messages** should explain _what went wrong_ and _how to fix it_, not dump JSON structures

**Example (Good):**
```

✓ Export complete: EPUB, HTML, Markdown ✓ Anchor integrity: 45 manuscript, 24 codex, 89 crosslinks
(0 broken) ✓ Kobo compatibility: NCX + landmarks + inline anchors ⚠ Font embedding: fonts not found
in /resources/fonts/, using fallbacks

````

**Example (Bad):**
```json
{
  "intent": "view.export.result",
  "payload": {
    "data": {
      "anchor_map": "45 manuscript, 24 codex..."
    }
  }
}
````

````

---

### 7B: Metadata Auto-Generation & Consistency

**Problem:** Metadata (title, author, license, description, subjects) must be consistent across EPUB/HTML/Markdown but is sometimes manual.

**Proposed Fix:**

**File:** `/05-prompts/book_binder/system_prompt.md`

**Location:** Add new section "Metadata Management"

```markdown
### Metadata Management (All Export Formats)

**Principle:** Metadata is centralized and auto-injected into all export formats.

**Metadata Source Hierarchy:**
1. **Cold snapshot metadata** (if present): title, author, license, description, subjects
2. **Project defaults** (from configuration): fallback if snapshot lacks metadata
3. **Auto-generated** (if both missing): derived from manuscript content

**Required Metadata Fields:**

| Field | Source | Auto-Generation Rule | Format-Specific Handling |
|-------|--------|----------------------|--------------------------|
| **Title** | Cold snapshot or frontmatter | Use first H1 or "Untitled" | EPUB: `<dc:title>`, HTML: `<title>`, MD: YAML frontmatter |
| **Author** | Cold snapshot or config | Default: "Unknown Author" | EPUB: `<dc:creator>`, HTML: `<meta name="author">`, MD: YAML `author:` |
| **License** | Cold snapshot or config | Default: "All Rights Reserved" | EPUB: `<dc:rights>`, HTML: `<meta name="license">`, MD: YAML `license:` |
| **Description** | Cold snapshot or first paragraph | Extract first 2-3 sentences of prose | EPUB: `<dc:description>`, HTML: `<meta name="description">`, MD: YAML `description:` |
| **Subjects** | Cold snapshot or auto-detect | Genre keywords from prose/lore | EPUB: `<dc:subject>`, HTML: `<meta name="keywords">`, MD: YAML `tags:` |
| **Language** | Cold snapshot or config | Default: "en" (English) | EPUB: `<dc:language>`, HTML: `<html lang="en">`, MD: YAML `lang:` |
| **Publisher** | Cold snapshot or config | Optional; omit if not provided | EPUB: `<dc:publisher>`, HTML/MD: in copyright notice |
| **Date** | Auto-generated | ISO 8601 (e.g., "2025-11-04") | EPUB: `<dc:date>`, HTML: `<meta name="date">`, MD: YAML `date:` |
| **UUID** | Auto-generated | UUIDv4 for each export | EPUB: `<dc:identifier id="uuid">` |

**Implementation:**
1. On export request, gather metadata from Cold snapshot → config → auto-detect
2. Validate required fields are present (title, author, license, language, date, UUID)
3. Inject into format-specific templates:
   - **EPUB:** `content.opf` `<metadata>` block
   - **HTML:** `<head>` with `<meta>` tags
   - **Markdown:** YAML frontmatter at top of file
4. Log metadata source in `view_log` (e.g., "Metadata: snapshot-provided / auto-generated")

**Validation:**
- Fail export if title or author is missing (unless user explicitly allows)
- Warn if description/subjects are auto-generated (may need refinement)
- Log metadata source for each field in view_log
````

**File:** `/05-prompts/book_binder/intent_handlers/format.render.md`

**Location:** Add to "Pre-Render Validation" checklist

```markdown
- [ ] Gather metadata from Cold snapshot / config / auto-generation
- [ ] Validate required fields: title, author, license, language, date, UUID
- [ ] Inject metadata into format-specific templates (EPUB OPF, HTML head, MD YAML)
- [ ] Log metadata sources in view_log
```

---

### 7C: Cover Art Text Requirement & SVG Backup

**Problem:** Covers must bear the book title; SVG covers serve as backup for EPUB (vector
scalability).

**Proposed Fix:**

**File:** `/05-prompts/book_binder/system_prompt.md`

**Location:** Enhance existing "Cover Policy" section

```markdown
### Cover Art Policy (Title-Bearing Requirement)

**Rules:**

1. **Primary cover** must be a **title-bearing PNG**:
   - Title text rendered on the image (not added in post)
   - High resolution (min 1600x2400px recommended)
   - RGB color mode
   - Filename convention: `cover_titled.png` or `*_titled.png`

2. **SVG backup** included for EPUB:
   - Vector format for infinite scalability
   - Also title-bearing (text as paths or embedded fonts)
   - Filename convention: `cover_titled.svg` or `*_titled.svg`

3. **No textless covers** in final exports:
   - Textless covers are work-in-progress only
   - Archive as `cover_untitled.png` but do NOT include in EPUB/HTML

4. **Manifest tracking:**
   - Cover images listed in `art_manifest.updated.json`
   - Status: "approved" + metadata field `title_bearing: true`
   - SHA-256 hash for verification

**Implementation:**

1. Book Binder checks for titled cover: `cover_titled.png` and optionally `cover_titled.svg`
2. If missing: fail export with error "Title-bearing cover required"
3. EPUB uses PNG as primary (`<meta name="cover" content="cover-image"/>`), includes SVG as backup
   item
4. HTML uses PNG in `<meta property="og:image">` and as page banner
5. Log cover art status in view_log

**Validation (CI Gate 1):**

- [ ] Primary cover is PNG with `*_titled.png` filename or `title_bearing: true` in manifest
- [ ] (Optional) SVG backup present
- [ ] Cover dimensions ≥ 1600x2400px (warn if smaller)
- [ ] Cover listed in art manifest with SHA-256 hash
```

---

### 7D: Typography Decisions via Style Lead

**Problem:** Font choices for cover and prose are currently hard-coded in exporter; should be Style
Lead's domain.

**Proposed Fix:**

**File:** `/05-prompts/style_lead/system_prompt.md` (or equivalent)

**Location:** Add new section "Typography Specification"

````markdown
### Typography Specification (Cover & Prose)

**Authority:** Style Lead defines typography as part of style stabilization.

**Scope:**

1. **Prose body text:** Font family, size, line height, paragraph spacing
2. **Display titles:** Headings (H1, H2, H3), chapter markers
3. **Cover typography:** Title font, author font, tagline/subtitle (if any)
4. **UI elements:** Choice links, navigation, captions

**Output Format (Style Manifest):**

```json
{
  "typography": {
    "prose": {
      "font_family": "Source Serif 4",
      "fallback": "Georgia, Times New Roman, serif",
      "font_size": "1em",
      "line_height": "1.6",
      "paragraph_spacing": "1em"
    },
    "display": {
      "font_family": "Cormorant Garamond",
      "fallback": "Georgia, serif",
      "h1_size": "2.5em",
      "h2_size": "2em",
      "h3_size": "1.5em"
    },
    "cover": {
      "title_font": "Cormorant Garamond Bold",
      "author_font": "Source Serif 4 Italic",
      "fallback": "Georgia, serif"
    },
    "ui": {
      "link_color": "#2c5aa0",
      "link_underline": true,
      "caption_font": "Source Serif 4 Italic",
      "caption_size": "0.9em"
    }
  },
  "fonts_required": [
    "Source Serif 4 (Regular, Italic, Bold)",
    "Cormorant Garamond (Regular, Bold)"
  ],
  "embed_in_epub": true
}
```
````

**Integration with Book Binder:**

1. Style Lead writes `style_manifest.json` during style stabilization
2. Book Binder reads manifest during export
3. If manifest missing: use default typography (Source Serif 4 / Cormorant Garamond)
4. If fonts specified but not available in `/resources/fonts/`: warn and use fallbacks
5. Log typography source in view_log (e.g., "Typography: style_manifest / defaults / fallback")

**Validation:**

- [ ] Typography manifest includes prose, display, cover, and UI font specs
- [ ] Required fonts are available in `/resources/fonts/` or fallback specified
- [ ] EPUB embeds fonts if `embed_in_epub: true` and fonts are licensed for embedding

````

**File:** `/05-prompts/book_binder/system_prompt.md`

**Location:** Update "Typography & Font Embedding" section

```markdown
### Typography & Font Embedding

**Source:** Typography decisions come from **Style Lead's `style_manifest.json`**.

**Fallback Hierarchy:**
1. **Style manifest** (if present): use specified fonts and settings
2. **Project defaults** (if manifest missing): Source Serif 4 + Cormorant Garamond
3. **System fallbacks** (if fonts unavailable): Georgia, Times New Roman, serif

**Implementation:**
1. Check for `style_manifest.json` in Cold snapshot or project root
2. Extract typography block (prose, display, cover, UI)
3. Verify fonts exist in `/resources/fonts/`
4. If fonts missing: use fallback fonts specified in manifest or defaults
5. For EPUB: embed fonts if `embed_in_epub: true` and licensing permits
6. Log typography source and font availability in view_log

**CSS Generation:**
- Generate `@font-face` declarations from manifest
- Apply font-family, size, line-height to body and headings
- Include fallback fonts in CSS stack

**Validation:**
- [ ] Typography manifest is well-formed JSON
- [ ] Required fonts are available or fallbacks specified
- [ ] Embedded fonts are licensed for distribution (SIL OFL or similar)
- [ ] Test rendering on major EPUB readers
````

---

### 7E: Art Director Filename Conventions (ChatGPT Renderer)

**Problem:** When ChatGPT (or other LLMs) use `image_gen.text2im` to render art, filenames must
match art manifest entries to enable automatic linking.

**Proposed Fix:**

**File:** `/05-prompts/art_director/system_prompt.md` (or equivalent)

**Location:** Add section "Filename Conventions for Rendered Art"

```markdown
### Filename Conventions for Rendered Art

**Requirement:** When using `image_gen.text2im` or other rendering tools, output filenames **must
match** entries in `art_manifest.json`.

**Filename Pattern:**
```

{role}_{section_id}_{variant}.{ext}

Examples:

- cover_titled.png
- plate_A2_K.png
- thumb_A1_H.png
- scene_S3_wide.png

````

**Mapping to Manifest:**
1. Art Director updates `art_manifest.json` with planned filenames **before** rendering
2. Render art using image_gen.text2im (or equivalent)
3. Save file with exact filename from manifest
4. Compute SHA-256 hash and update manifest entry
5. Mark status as "approved" if accepted, "rejected" if re-render needed

**Example Manifest Entry:**
```json
{
  "id": "plate_A2_K",
  "role": "interior_plate",
  "filename": "plate_A2_K.png",
  "format": "PNG",
  "dimensions": "1024x1024",
  "caption": "Rain-slicked alley with distant figure",
  "prompt": "Film noir scene, rain-slicked alley, distant figure under streetlight, high contrast black and white, cinematic composition",
  "sha256": "abc123...",
  "status": "approved"
}
````

**Workflow:**

1. **Plan:** AD defines manifest entry with filename, role, caption, prompt
2. **Render:** Use image_gen.text2im with prompt; save as `plate_A2_K.png`
3. **Hash:** Compute SHA-256 of saved file
4. **Update:** Add hash to manifest; set status to "approved"
5. **Handoff:** Book Binder reads manifest and includes image at correct anchor

**Validation:**

- [ ] All rendered images match manifest filenames exactly (case-sensitive)
- [ ] All manifest entries with status="approved" have SHA-256 hashes
- [ ] No orphaned images (files not in manifest)
- [ ] No missing images (manifest entries without files)

**ChatGPT-Specific Note:** When delegating to ChatGPT via `image_gen.text2im`:

1. Provide the planned filename in the rendering request
2. Verify saved filename matches manifest
3. If filename mismatch: rename file immediately to prevent downstream issues

````

**File:** `/05-prompts/illustrator/system_prompt.md` (or equivalent)

**Location:** Add same section or reference AD conventions

```markdown
### Filename Conventions (Renderer)

**See Art Director conventions.** When rendering images, filenames must match `art_manifest.json` entries exactly.

**Key Points:**
- Filenames are deterministic: `{role}_{id}_{variant}.{ext}`
- Compute SHA-256 hash after rendering
- Update manifest with hash and status
- Never create images without manifest entry

**Integration with image_gen.text2im:**
```python
# Example pseudo-code for ChatGPT renderer
filename = manifest_entry["filename"]  # e.g., "plate_A2_K.png"
prompt = manifest_entry["prompt"]
image_gen.text2im(prompt, output=filename)
hash_sha256 = compute_hash(filename)
manifest_entry["sha256"] = hash_sha256
manifest_entry["status"] = "approved"
````

````

---

## Implementation Priority (Updated)

| Priority | Fix | Files to Modify | Complexity | Impact |
|----------|-----|-----------------|------------|--------|
| **P0 Critical** | EPUB Kobo Compat (inline anchors, NCX, landmarks) | `book_binder/system_prompt.md`, `format.render.md` | High | Fixes broken links on Kobo |
| **P1 High** | Header Hygiene | `book_binder/system_prompt.md`, `format.render.md` | Low | Prevents process leakage |
| **P1 High** | Choice UX Standardization | `book_binder/system_prompt.md`, `format.render.md` | Low | Improves reader UX |
| **P1 High** | Metadata Auto-Generation (7B) | `book_binder/system_prompt.md`, `format.render.md` | Medium | Ensures consistent metadata |
| **P2 Medium** | ID Normalization | `book_binder/system_prompt.md`, `format.render.md` | Medium | Better Kobo compat |
| **P2 Medium** | CI/QA Gates | Create `/spec-tools/validation/epub_validator.md` | Medium | Prevents regression |
| **P2 Medium** | JSON Exposure (7A) | `book_binder/system_prompt.md` | Low | Cleaner user-facing outputs |
| **P2 Medium** | Cover Policy (7C) | `book_binder/system_prompt.md`, CI gates | Low | Enforce title-bearing covers |
| **P3 Low** | Typography via Style Lead (7D) | `style_lead/system_prompt.md`, `book_binder/system_prompt.md` | Medium | Style Lead authority |
| **P3 Low** | Art Filename Conventions (7E) | `art_director/system_prompt.md`, `illustrator/system_prompt.md` | Low | Renderer integration |

---

## Summary of Files to Create/Modify (Updated)

### Files to Modify

1. `/05-prompts/book_binder/system_prompt.md`
   - Add: Header Sanitization rules
   - Add: Choice Link Normalization (enhanced)
   - Add: EPUB Anchor Generation (twin anchors)
   - Add: EPUB2 Legacy Navigation (NCX)
   - Add: EPUB Landmarks & Guide
   - Add: ID Normalization & Aliasing (enhanced)
   - Add: User Communication & Output Format (7A)
   - Add: Metadata Management (7B)
   - Update: Cover Art Policy (7C)
   - Update: Typography & Font Embedding (7D)

2. `/05-prompts/book_binder/intent_handlers/format.render.md`
   - Add: Header sanitization to pre-render checklist
   - Add: Choice rendering standardization
   - Add: Anchor processing (normalization + twin anchors)
   - Add: NCX generation
   - Add: Landmarks generation
   - Add: Metadata gathering and injection (7B)

3. `/05-prompts/style_lead/system_prompt.md`
   - Add: Typography Specification (7D)

4. `/05-prompts/art_director/system_prompt.md`
   - Add: Filename Conventions for Rendered Art (7E)

5. `/05-prompts/illustrator/system_prompt.md`
   - Add: Filename Conventions reference (7E)

### Files to Create

6. `/spec-tools/validation/epub_validator.md`
   - Specification for CI/QA gates (includes 7C cover validation)

7. `/resources/fonts/README.md`
   - Typography policy and font embedding guide

---

## PROPOSAL 8: Showrunner Initial Setup Flow (User Feedback)

### Problem
Showrunner currently lacks a guided onboarding flow for new projects. Users need help defining:
- Genre/theme
- Project title
- Target length (number of sections/choices)
- Style/tone preferences
- Other initial parameters

Without this, users must know the system deeply before starting.

### Proposed Fix

**File:** `/05-prompts/showrunner/system_prompt.md` (or equivalent)

**Location:** Add new section "Project Initialization Flow"

```markdown
### Project Initialization Flow

**Purpose:** Guide users through initial project setup for new interactive manuscripts.

**Trigger:** When Showrunner detects a new/empty project or user requests initialization.

**Flow:**

#### Step 1: Genre & Theme
````

Showrunner: "Let's set up your interactive story. What genre or theme are you exploring?"

Examples:

- Detective noir / mystery
- Fantasy adventure
- Sci-fi thriller
- Horror survival
- Historical drama
- Romance
- Other (specify)

User provides: [genre/theme]

```

**Capture:** Store in `project_metadata.json` as `"genre": "detective-noir"`

---

#### Step 2: Title (Provisional)
```

Showrunner: "What's your working title? (You can change this later)"

Options:

1. User provides title → use as-is
2. User requests suggestions → generate 3-5 title options based on genre
3. User defers → use placeholder "Untitled [Genre] Project"

User provides: [title or "suggest" or "later"]

```

**If user requests suggestions:**
```

Showrunner suggests (example for detective noir):

1. "Midnight Deposition"
2. "The Shadow Verdict"
3. "Crossfire Protocol"
4. "Neon Confessional"
5. "The Last Witness"

User selects: [number or provides own]

```

**Capture:** Store as `"title": "Midnight Deposition"` (provisional, can change)

---

#### Step 3: Scope & Length
```

Showrunner: "How long should this story be?"

Options:

1. Short (10-15 sections) — ~30min play time
2. Medium (20-30 sections) — ~1hr play time
3. Long (40-60 sections) — ~2hr play time
4. Epic (80+ sections) — multi-session
5. Custom (specify section count)

User selects: [option or custom number]

```

**Capture:** Store as `"target_sections": 30, "target_length": "medium"`

**Follow-up (optional):**
```

Showrunner: "How branching should the narrative be?"

Options:

1. Linear (few branches, converging paths)
2. Moderate (some meaningful choices, 2-3 major branches)
3. Highly branching (many paths, significant divergence)

User selects: [option]

```

**Capture:** Store as `"branching_style": "moderate"`

---

#### Step 4: Style & Tone
```

Showrunner: "What style and tone are you aiming for?"

Prompts:

- Writing style: Literary / Pulp / Journalistic / Poetic / Other
- Paragraph density: Sparse (1-2 paras) / Moderate (2-3) / Rich (3-4+)
- Tone: Gritty / Lighthearted / Suspenseful / Melancholic / Other
- POV: First person / Second person / Third person

User provides: [selections or free-form description]

````

**Capture:** Store as:
```json
{
  "style": {
    "writing_style": "pulp",
    "paragraph_density": "rich",
    "tone": "gritty",
    "pov": "second-person"
  }
}
````

---

#### Step 5: Licensing & Authorship

```
Showrunner: "Who's the author, and what license should we use?"

Author: [User provides name or "Anonymous"]
License options:
1. CC BY-NC 4.0 (Attribution, Non-Commercial)
2. CC BY 4.0 (Attribution)
3. CC BY-SA 4.0 (Attribution, Share-Alike)
4. All Rights Reserved
5. Custom (specify)

User selects: [option]
```

**Capture:** Store as:

```json
{
  "author": "Peter van Liesdonk",
  "license": "CC BY-NC 4.0"
}
```

---

#### Step 6: Confirmation & Handoff

```
Showrunner: "Here's your project setup:

📖 Title: Midnight Deposition
🎭 Genre: Detective noir
📏 Length: Medium (~30 sections, 1hr play time)
🌿 Branching: Moderate (meaningful choices, 2-3 major paths)
✍️ Style: Pulp writing, rich paragraphs (3-4 each), gritty tone, second-person POV
👤 Author: Peter van Liesdonk
⚖️ License: CC BY-NC 4.0

Ready to begin? I'll hand off to:
1. Lore Deepening (establish world/characters)
2. Story Spark (generate initial structure)

Or you can adjust any settings above."

User confirms: [yes / adjust X / cancel]
```

**Actions on confirmation:**

1. Write `project_metadata.json` with all settings
2. Create initial directory structure (if needed)
3. Initiate **Lore Deepening** or **Story Spark** based on user preference
4. Log initialization in project log

---

### Implementation Notes

**File Structure After Initialization:**

```
project_root/
  project_metadata.json      # Settings from init flow
  lore/                       # For Lore Deepening output
  manuscript/                 # Hot/Cold snapshots
  codex/                      # Game rules, world building
  art/                        # Cover, plates, etc.
  exports/                    # EPUB/HTML/MD outputs
```

**Metadata Schema (`project_metadata.json`):**

```json
{
  "title": "Midnight Deposition",
  "genre": "detective-noir",
  "author": "Peter van Liesdonk",
  "license": "CC BY-NC 4.0",
  "target_sections": 30,
  "target_length": "medium",
  "branching_style": "moderate",
  "style": {
    "writing_style": "pulp",
    "paragraph_density": "rich",
    "tone": "gritty",
    "pov": "second-person"
  },
  "created": "2025-11-04T12:00:00Z",
  "last_modified": "2025-11-04T12:00:00Z",
  "version": "0.1.0"
}
```

**Edge Cases:**

- If user already has a project: detect and ask "Resume existing or start new?"
- If user skips optional fields: use sensible defaults (e.g., "moderate" branching, "CC BY-NC 4.0"
  license)
- If user wants to change settings later: provide `/project/settings` command or similar

---

### Integration with Other Roles

Once initialized, Showrunner hands off to:

1. **Lore Deepening** (if user wants world/character building first)
2. **Story Spark** (if user wants structure/outline first)
3. **Plotwright** (if user already has lore and wants plot structure)

All downstream roles read `project_metadata.json` for context (title, genre, style, length targets).

---

### User Experience Goals

1. **Guided but flexible:** Users can skip/defer questions
2. **Suggests defaults:** Based on genre conventions
3. **Non-blocking:** Can change settings anytime
4. **Educational:** Explains what each choice affects
5. **Fast:** ~2-3 minutes for full setup

---

### Validation

- [ ] All required fields captured (title, author, license, genre)
- [ ] Metadata schema is valid JSON
- [ ] Style preferences are propagated to Style Lead
- [ ] Length/branching targets are propagated to Plotwright
- [ ] User can review and confirm before committing

````

**File:** Create `/05-prompts/showrunner/intent_handlers/project.init.md`

**Purpose:** Detailed handler for project initialization intent

```markdown
# Intent Handler: project.init

**Trigger:** User requests new project setup OR Showrunner detects empty project

**Protocol Message:**
```json
{
  "intent": "project.init.request",
  "sender": { "role": "USER" },
  "receiver": { "role": "SR" },
  "payload": {
    "mode": "interactive"  // or "quick" for defaults
  }
}
````

**Flow:** See "Project Initialization Flow" in `system_prompt.md`

**Completion:**

```json
{
  "intent": "project.init.complete",
  "sender": { "role": "SR" },
  "receiver": { "role": "USER" },
  "payload": {
    "metadata": { ... },  // Full project_metadata.json
    "next_steps": ["lore_deepening", "story_spark"],
    "message": "Project initialized. Ready to begin?"
  }
}
```

**Handoff to Next Role:**

- If user chooses Lore Deepening: `lore.deepen.request`
- If user chooses Story Spark: `structure.spark.request`

```

---

## Implementation Priority (Updated)

| Priority | Fix | Files to Modify | Complexity | Impact |
|----------|-----|-----------------|------------|--------|
| **P0 Critical** | EPUB Kobo Compat (inline anchors, NCX, landmarks) | `book_binder/system_prompt.md`, `format.render.md` | High | Fixes broken links on Kobo |
| **P1 High** | Header Hygiene | `book_binder/system_prompt.md`, `format.render.md` | Low | Prevents process leakage |
| **P1 High** | Choice UX Standardization | `book_binder/system_prompt.md`, `format.render.md` | Low | Improves reader UX |
| **P1 High** | Metadata Auto-Generation (7B) | `book_binder/system_prompt.md`, `format.render.md` | Medium | Ensures consistent metadata |
| **P1 High** | Showrunner Init Flow (8) | `showrunner/system_prompt.md`, create `project.init.md` | Medium | Onboarding UX |
| **P2 Medium** | ID Normalization | `book_binder/system_prompt.md`, `format.render.md` | Medium | Better Kobo compat |
| **P2 Medium** | CI/QA Gates | Create `/spec-tools/validation/epub_validator.md` | Medium | Prevents regression |
| **P2 Medium** | JSON Exposure (7A) | `book_binder/system_prompt.md` | Low | Cleaner user-facing outputs |
| **P2 Medium** | Cover Policy (7C) | `book_binder/system_prompt.md`, CI gates | Low | Enforce title-bearing covers |
| **P3 Low** | Typography via Style Lead (7D) | `style_lead/system_prompt.md`, `book_binder/system_prompt.md` | Medium | Style Lead authority |
| **P3 Low** | Art Filename Conventions (7E) | `art_director/system_prompt.md`, `illustrator/system_prompt.md` | Low | Renderer integration |

---

## Summary of Files to Create/Modify (Updated)

### Files to Modify

1. `/05-prompts/book_binder/system_prompt.md`
   - Add: Header Sanitization rules
   - Add: Choice Link Normalization (enhanced)
   - Add: EPUB Anchor Generation (twin anchors)
   - Add: EPUB2 Legacy Navigation (NCX)
   - Add: EPUB Landmarks & Guide
   - Add: ID Normalization & Aliasing (enhanced)
   - Add: User Communication & Output Format (7A)
   - Add: Metadata Management (7B)
   - Update: Cover Art Policy (7C)
   - Update: Typography & Font Embedding (7D)

2. `/05-prompts/book_binder/intent_handlers/format.render.md`
   - Add: Header sanitization to pre-render checklist
   - Add: Choice rendering standardization
   - Add: Anchor processing (normalization + twin anchors)
   - Add: NCX generation
   - Add: Landmarks generation
   - Add: Metadata gathering and injection (7B)

3. `/05-prompts/style_lead/system_prompt.md`
   - Add: Typography Specification (7D)

4. `/05-prompts/art_director/system_prompt.md`
   - Add: Filename Conventions for Rendered Art (7E)

5. `/05-prompts/illustrator/system_prompt.md`
   - Add: Filename Conventions reference (7E)

6. `/05-prompts/showrunner/system_prompt.md`
   - Add: Project Initialization Flow (8)

### Files to Create

7. `/spec-tools/validation/epub_validator.md`
   - Specification for CI/QA gates (includes 7C cover validation)

8. `/resources/fonts/README.md`
   - Typography policy and font embedding guide

9. `/05-prompts/showrunner/intent_handlers/project.init.md`
   - Project initialization intent handler (8)

---

## Approval Checklist

- [ ] Review all proposed changes (including 7A-7E refinements)
- [ ] Confirm priority order (P0 → P1 → P2 → P3)
- [ ] Approve file creation/modification list
- [ ] Approve testing plan
- [ ] Approve rollout strategy
- [ ] Answer open questions OR defer to implementation phase

---

**Once approved, proceed with implementation in priority order.**
```
