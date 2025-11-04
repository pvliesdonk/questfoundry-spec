# EPUB Validator — CI/QA Gates

**Status:** ✅ Implemented (2025-11-04)

**Purpose:** Automated validation to enforce post-mortem policies and prevent regression.

---

## Installation

```bash
cd tools/
uv sync
```

## Usage

```bash
# Validate an EPUB file
qfspec-validate-epub path/to/book.epub

# Example
qfspec-validate-epub ../exports/midnight_deposition.epub
```

## Exit Codes

- `0`: All gates passed (or only warnings)
- `1`: One or more gates failed

---

## Validation Gates

### Gate 1: Cover Policy

**Rule:** Final EPUB must use a title-bearing PNG as designated cover-image.

**Checks:**
- ✓ `content.opf` has `<meta name="cover" content="cover-image"/>`
- ✓ Cover image is PNG format
- ✓ Cover item exists in manifest
- ⚠ Optional SVG backup present

**Failure:** Block export; warn user to provide titled cover.

---

### Gate 2: Start Page Invariant

**Rule:** Reading order begins at first scene; frontmatter not in spine start.

**Checks:**
- ✓ First `<itemref>` in spine is a scene section (matches pattern `^\d{3}\.xhtml$`)
- ⚠ TOC/nav.xhtml has `linear="no"` attribute (optional check)

**Failure:** Warn; log incorrect spine order.

---

### Gate 3: Anchor Integrity

**Rule:** Every link target must exist; every section must have inline anchor.

**Checks:**
- ✓ Parse all `href="#id"` and `href="file.xhtml#id"` links
- ✓ Verify each target ID exists in referenced file
- ✓ Count inline anchors (`<a id="...">` or `<span id="...">`)
- ✓ Compare inline anchor count to section count
- ✓ Report orphaned links (broken references)
- ✓ Report collisions (duplicate IDs)

**Failure:** Block export if orphans > 0 or collisions > 0; log details.

---

### Gate 4: Kobo Compatibility

**Rule:** EPUB must include Kobo-specific navigation and anchor patterns.

**Checks:**
- ✓ `toc.ncx` file present in manifest (`application/x-dtbncx+xml`)
- ✓ `toc.ncx` includes all spine items with sequential `playOrder` (1..N)
- ✓ ARIA landmarks present in `nav.xhtml` (cover, toc, bodymatter)
- ⚠ (Optional) EPUB2 `<guide>` present in `content.opf`

**Failure:** Warn (non-blocking) if NCX/landmarks missing.

---

### Gate 5: Manifest Compliance (Art)

**Rule:** All images must be listed in art manifest with captions and hashes.

**Status:** Not yet implemented (requires access to `art_manifest.json` outside EPUB).

**Planned Checks:**
- Parse all `<img src="...">` tags in EPUB
- Verify each image path exists in `art_manifest.updated.json`
- Verify each image has non-empty `caption` field
- Verify each image has SHA-256 hash
- (Optional) Recompute hash and verify against manifest

**Failure:** Warn if caption missing; block if image not in manifest.

---

### Gate 6: Header Hygiene

**Rule:** Reader-facing section titles must not contain operational markers.

**Checks:**
- ✓ Parse all `<h2>` (sections) and `<h1>` (title) in EPUB
- ✓ Regex match: `(Hub|Unofficial|Quick|Temp|Draft|FLAG_\w+|CODEWORD):\s`
- ✓ Count matches (should be 0)

**Failure:** Block export if count > 0; log offending headers.

---

## Example Output

```
======================================================================
EPUB Validation Report
======================================================================

✓ Gate 1: Cover Policy: Cover policy validated
  Cover image: cover.png (image/png)
  ✓ Cover is PNG format
  ✓ SVG backup cover found

✓ Gate 2: Start Page: Start page validated
  First spine item: 001.xhtml
  ✓ Reading order starts at scene section

✓ Gate 3: Anchor Integrity: All links resolve
  Total anchors: 45
  Total links: 89
  Inline anchors: 45
  Sections: 45
  ✓ All links resolve
  ✓ Inline anchors present (Kobo compat)

✓ Gate 4: Kobo Compatibility: Kobo compatibility features present
  ✓ toc.ncx present in manifest
    NCX nav points: 30
    ✓ playOrder is sequential (1..N)
  ✓ ARIA landmarks present in nav.xhtml
    Landmark types: cover, toc, bodymatter
  ✓ EPUB2 guide present (3 references)

✓ Gate 6: Header Hygiene: Header hygiene validated
  ✓ No operational markers in headers

======================================================================
Summary: 5 passed, 0 warnings, 0 failed
======================================================================
```

---

## Integration with Book Binder

Book Binder can call validator post-export:

```python
import subprocess

# After generating EPUB
epub_path = "exports/midnight_deposition.epub"
result = subprocess.run(
    ["qfspec-validate-epub", epub_path],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print("EPUB validation failed:")
    print(result.stdout)
    # Fail export or log warning
else:
    print("✓ EPUB validation passed")
    # Append validator report to view_log
```

---

## Future Enhancements

1. **Gate 5 Implementation:** Add art manifest validation (requires project structure access)
2. **JSON Output:** Add `--json` flag for machine-readable results
3. **Fix Suggestions:** Provide actionable remediation steps for each failure
4. **CI Integration:** Add GitHub Actions workflow to validate EPUBs in PRs
5. **HTML/Markdown Validators:** Similar validators for other export formats

---

## Development

Run tests (when implemented):

```bash
cd tools/
uv run pytest tests/test_epub_validator.py
```

Add to pre-commit hooks:

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: epub-validator
      name: Validate EPUB exports
      entry: qfspec-validate-epub
      language: system
      files: '\.epub$'
```

---

## References

- Post-mortem: `/docs/post_mortems/2025-11-04_midnight_deposition.md` (§10)
- Fix Proposal: `/docs/post_mortems/2025-11-04_fix_proposal.md` (Proposal 5)
- Book Binder: `/05-prompts/book_binder/system_prompt.md`
