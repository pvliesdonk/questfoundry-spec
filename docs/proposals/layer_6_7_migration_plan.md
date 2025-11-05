# Layer 6 & 7 Migration Plan

**Date:** 2025-11-05
**Status:** Proposal
**Decision Required:** Repository architecture, schema hosting strategy

---

## Executive Summary

This document outlines the migration plan for setting up Layer 6 (Python library) and Layer 7 (CLI tool) as separate repositories, with considerations for schema publishing and the existing schema URL structure.

**Key Decisions:**
1. Rename current repo `questfoundry` → `questfoundry-spec`
2. Create `questfoundry-py` (Layer 6) and `questfoundry-cli` (Layer 7)
3. Establish schema publishing strategy that respects existing `$id` URLs
4. Set up automated schema distribution via GitHub Actions

---

## Repository Architecture

### Three-Repository Model

```
pvliesdonk/questfoundry-spec (current repo renamed)
├─ Layers 0-5: Specification, schemas, protocol, prompts
├─ Documentation and design guidelines
├─ spec-tools/: Validation tools for spec development
└─ Authoritative source for all schemas and prompts

pvliesdonk/questfoundry-py (new)
├─ Layer 6: Python library implementation
├─ Bundles schemas and prompts at build time
├─ Published to PyPI as: questfoundry-py
└─ Import as: from questfoundry import ...

pvliesdonk/questfoundry-cli (new)
├─ Layer 7: Command-line interface
├─ Depends on questfoundry-py from PyPI
├─ Published to PyPI as: questfoundry-cli
└─ Command: qf
```

### Submodule Strategy

**During Development:**

Both implementation repos reference spec as submodule:

```bash
# In questfoundry-py
git submodule add https://github.com/pvliesdonk/questfoundry-spec spec/
# Use spec/ for development reference
# Copy schemas/prompts into package resources during build

# In questfoundry-cli
git submodule add https://github.com/pvliesdonk/questfoundry-spec spec/
# Use spec/ for documentation and examples
# No copying needed (uses questfoundry-py from PyPI)
```

**At Build Time:**

Build scripts copy from submodule into package resources:

```python
# In questfoundry-py/build.py
shutil.copytree('spec/03-schemas', 'src/questfoundry/resources/schemas')
shutil.copytree('spec/05-prompts', 'src/questfoundry/resources/prompts')
```

---

## Schema Publishing Strategy

### Current State: Schema URLs

All schemas use canonical URLs in their `$id` field:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://questfoundry.liesdonk.nl/schemas/hook_card.schema.json",
  ...
}
```

**Discovery:** All 18 schemas reference `https://questfoundry.liesdonk.nl/schemas/` as base URL.

### Schema Hosting Options

**RECOMMENDED: Option A - GitHub Pages at Custom Domain**

```
Domain: questfoundry.liesdonk.nl
Hosting: GitHub Pages from questfoundry-spec repo
Path: /schemas/ → maps to 03-schemas/ directory
Result: Schema $id URLs resolve correctly
Benefit: Stable, canonical URLs; no breaking changes needed
```

**Setup:**
1. Enable GitHub Pages for questfoundry-spec
2. Configure custom domain `questfoundry.liesdonk.nl` in repo settings
3. Add CNAME record in DNS: `questfoundry.liesdonk.nl → pvliesdonk.github.io`
4. Create `docs/schemas/` symlink or copy from `03-schemas/`
5. Schema URLs resolve automatically

**Alternative: Option B - Update Schema IDs to GitHub Raw URLs**

```json
{
  "$id": "https://raw.githubusercontent.com/pvliesdonk/questfoundry-spec/main/03-schemas/hook_card.schema.json"
}
```

**Pros:** No custom domain needed
**Cons:** Breaking change; requires updating all schemas and documentation

**Alternative: Option C - Dual Publishing**

Keep `$id` URLs as-is, but document multiple access methods:

1. Canonical: `https://questfoundry.liesdonk.nl/schemas/hook_card.schema.json`
2. GitHub Raw: `https://raw.githubusercontent.com/...`
3. GitHub Releases: Download schema bundle
4. PyPI Package: `pip install questfoundry-py`

### Distribution Channels

#### 1. GitHub Pages (Canonical URLs)

- **URL Pattern:** `https://questfoundry.liesdonk.nl/schemas/{schema-name}.schema.json`
- **Use Case:** Schema validation tools, external references
- **Update Frequency:** On every commit to main (automatic via GitHub Pages)

#### 2. GitHub Releases

- **Asset Name:** `questfoundry-schemas-v{version}.zip`
- **Contents:** All schemas + README + CHANGELOG
- **Use Case:** Download full schema set for offline use
- **Update Frequency:** On version tags (e.g., `v0.1.0`, `v0.2.0`)

**Release Structure:**
```
questfoundry-schemas-v0.1.0.zip
├── schemas/
│   ├── hook_card.schema.json
│   ├── tu_brief.schema.json
│   └── ... (all 18 schemas)
├── README.md (usage instructions)
├── CHANGELOG.md (schema changes)
└── VERSION.txt
```

#### 3. PyPI Package (Bundled)

- **Package:** `questfoundry-py`
- **Access:** `from questfoundry.resources import get_schema`
- **Use Case:** Python applications using QuestFoundry
- **Update Frequency:** On package releases

#### 4. NPM Package (Future)

- **Package:** `@questfoundry/schemas`
- **Use Case:** JavaScript/TypeScript applications
- **Priority:** Phase 3 (if web consumers emerge)

---

## Migration Steps

### Phase 1: Preparation (Week 1, Day 1-2)

**1.1 Backup and Documentation**

- [ ] Create full backup of repository
- [ ] Document all external links that reference this repo
- [ ] Update IMPLEMENTATION_ROADMAP.md with migration status
- [ ] Create migration announcement draft

**1.2 Decision Points**

- [ ] **DECISION REQUIRED:** Schema hosting strategy (Option A recommended)
- [ ] **DECISION REQUIRED:** If Option A, confirm custom domain availability
- [ ] **DECISION REQUIRED:** Version number for initial schema release

### Phase 2: Schema Publishing Setup (Week 1, Day 3-4)

**2.1 GitHub Pages Setup (if Option A chosen)**

- [ ] Enable GitHub Pages in repository settings
- [ ] Configure custom domain: `questfoundry.liesdonk.nl`
- [ ] Update DNS: Add CNAME record
- [ ] Test schema URL resolution
- [ ] Add `docs/schemas/` directory (symlink or copy)

**2.2 GitHub Actions for Schema Distribution**

- [ ] Create `.github/workflows/publish-schemas.yml` (see below)
- [ ] Test workflow on feature branch
- [ ] Verify schema zip generation
- [ ] Test GitHub Release creation

**2.3 Schema Versioning**

- [ ] Add `SCHEMA_VERSION.txt` in `03-schemas/`
- [ ] Document versioning convention in `03-schemas/README.md`
- [ ] Create initial tag: `schemas-v0.1.0`

### Phase 3: Repository Rename (Week 1, Day 5)

**3.1 Rename Current Repository**

- [ ] GitHub → Settings → Repository name → `questfoundry-spec`
- [ ] Update repository description
- [ ] Verify automatic redirect works (`questfoundry` → `questfoundry-spec`)

**3.2 Update Internal References**

- [ ] Update README.md title and badges
- [ ] Update all cross-references in documentation
- [ ] Search and replace internal links: `questfoundry/` → `questfoundry-spec/`
- [ ] Update `.github/` workflow names and references
- [ ] Update `package.json` (if exists)

**3.3 Add Redirect Notice**

Add banner to README.md:

```markdown
> **📦 Repository Renamed:** This repository was renamed from `questfoundry` to `questfoundry-spec`.
> GitHub automatically redirects, but please update your bookmarks and git remotes.
>
> **Looking for implementations?**
> - Python Library: [questfoundry-py](https://github.com/pvliesdonk/questfoundry-py)
> - CLI Tool: [questfoundry-cli](https://github.com/pvliesdonk/questfoundry-cli)
```

**3.4 Rename tools/ Directory**

```bash
git mv tools spec-tools
# Update references in README.md and documentation
```

**Rationale:** Clarifies these are for spec development, not runtime tools.

### Phase 4: New Repository Creation (Week 2)

**4.1 Create questfoundry-py Repository**

```bash
gh repo create pvliesdonk/questfoundry-py --public --description "Layer 6: Python library for QuestFoundry protocol and artifact management"
cd questfoundry-py
git submodule add https://github.com/pvliesdonk/questfoundry-spec spec
```

- [ ] Initialize with Epic 1 from `06-libraries/IMPLEMENTATION_PLAN.md`
- [ ] Set up pyproject.toml with UV
- [ ] Configure GitHub Actions (test, lint, publish)
- [ ] Add comprehensive README (link to spec repo)

**4.2 Create questfoundry-cli Repository**

```bash
gh repo create pvliesdonk/questfoundry-cli --public --description "Layer 7: Command-line interface for QuestFoundry"
cd questfoundry-cli
git submodule add https://github.com/pvliesdonk/questfoundry-spec spec
```

- [ ] Initialize with Epic 1 from `07-ui/IMPLEMENTATION_PLAN.md`
- [ ] Set up pyproject.toml with UV and Typer
- [ ] Configure GitHub Actions (test, lint, publish)
- [ ] Add comprehensive README

### Phase 5: Post-Migration (Week 2-3)

**5.1 Documentation Updates**

In `questfoundry-spec`:

- [ ] Add "Related Repositories" section to README
- [ ] Add schema access documentation
- [ ] Update contribution guidelines
- [ ] Add links to implementation repos in layer READMEs

**5.2 Communication**

- [ ] Create GitHub Discussion: "Repository Migration Complete"
- [ ] Update any external links (personal website, social media)
- [ ] Create blog post or announcement (optional)

**5.3 Archive Old References**

- [ ] Review and close/update issues that reference old structure
- [ ] Update PR templates to mention new repo structure
- [ ] Update CONTRIBUTING.md with new workflow

---

## GitHub Actions Specifications

### Workflow 1: Publish Schemas on Release

**File:** `.github/workflows/publish-schemas.yml`

See implementation in next section.

**Trigger:** On tag push matching `schemas-v*`

**Actions:**
1. Validate all schemas
2. Create schema bundle zip
3. Create GitHub Release with bundle
4. (Optional) Publish to NPM

### Workflow 2: Update GitHub Pages

**File:** `.github/workflows/update-github-pages.yml`

**Trigger:** On push to `main` branch affecting `03-schemas/`

**Actions:**
1. Copy schemas to `docs/schemas/`
2. Generate index page
3. Deploy to GitHub Pages

---

## Schema Versioning Convention

### Version Format

```
schemas-v{MAJOR}.{MINOR}.{PATCH}

Examples:
- schemas-v0.1.0 (initial release)
- schemas-v0.2.0 (new artifact type added)
- schemas-v0.2.1 (bug fix in validation)
- schemas-v1.0.0 (stable API, breaking changes)
```

### Semantic Versioning for Schemas

- **MAJOR:** Breaking changes (removed fields, changed types)
- **MINOR:** Additive changes (new artifact types, new optional fields)
- **PATCH:** Non-breaking fixes (description updates, pattern fixes)

### Version Tracking

**File:** `03-schemas/SCHEMA_VERSION.txt`

```
0.1.0
```

**Changelog:** `03-schemas/CHANGELOG.md`

```markdown
# Schema Changelog

## [0.1.0] - 2025-11-05

### Added
- Initial release of all 18 artifact schemas
- hook_card, tu_brief, canon_pack, ...
- Full JSON Schema Draft 2020-12 compliance

### Schema IDs
All schemas use canonical URL: https://questfoundry.liesdonk.nl/schemas/
```

---

## Implementation Repos: Key Configuration

### questfoundry-py/pyproject.toml

```toml
[project]
name = "questfoundry-py"
version = "0.1.0"
description = "Python library for QuestFoundry protocol and artifact management"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "MIT"}

[project.urls]
Homepage = "https://github.com/pvliesdonk/questfoundry-py"
Documentation = "https://github.com/pvliesdonk/questfoundry-spec"
Specification = "https://github.com/pvliesdonk/questfoundry-spec"
Schemas = "https://questfoundry.liesdonk.nl/schemas/"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build]
include = [
  "src/**/*.py",
  "src/questfoundry/resources/schemas/**/*.json",
  "src/questfoundry/resources/prompts/**/*.md"
]
```

### questfoundry-cli/pyproject.toml

```toml
[project]
name = "questfoundry-cli"
version = "0.1.0"
description = "Command-line interface for QuestFoundry"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "questfoundry-py>=0.1.0",
    "typer[all]>=0.9.0",
    "rich>=13.0.0",
    "questionary>=2.0.0"
]

[project.scripts]
qf = "qf.cli:app"

[project.urls]
Homepage = "https://github.com/pvliesdonk/questfoundry-cli"
Documentation = "https://github.com/pvliesdonk/questfoundry-spec"
```

---

## Documentation: Schema Access

**Add to `03-schemas/README.md`:**

```markdown
# Layer 3 — Schemas

JSON Schema definitions for all QuestFoundry artifacts.

## Accessing Schemas

### 1. Canonical URLs (Recommended for Validation)

```bash
curl https://questfoundry.liesdonk.nl/schemas/hook_card.schema.json
```

All schemas use this base URL in their `$id` field.

### 2. GitHub Releases (Offline Bundle)

Download complete schema set:

```bash
wget https://github.com/pvliesdonk/questfoundry-spec/releases/download/schemas-v0.1.0/questfoundry-schemas-v0.1.0.zip
unzip questfoundry-schemas-v0.1.0.zip
```

### 3. Python Package (Bundled)

```bash
pip install questfoundry-py
```

```python
from questfoundry.resources import get_schema

schema = get_schema('hook_card')
```

### 4. Raw GitHub (Direct)

```bash
curl https://raw.githubusercontent.com/pvliesdonk/questfoundry-spec/main/03-schemas/hook_card.schema.json
```

## Version Information

Current version: See [SCHEMA_VERSION.txt](./SCHEMA_VERSION.txt)

Changelog: See [CHANGELOG.md](./CHANGELOG.md)

## Schema Validation

See [spec-tools/README.md](../spec-tools/README.md) for validation tools.
```

---

## Risk Assessment

### Low Risk
- Repository rename (GitHub auto-redirects)
- Adding GitHub Actions
- Creating new repos

### Medium Risk
- Schema URL changes (if Option B chosen)
  - **Mitigation:** Use Option A with custom domain
- Submodule management complexity
  - **Mitigation:** Document clearly in each repo README

### High Risk
- Breaking existing integrations
  - **Mitigation:** Maintain backward compatibility; communicate changes
- Schema $id URL resolution failures
  - **Mitigation:** Test thoroughly before migration; use Option A

---

## Success Criteria

Migration is complete when:

- [ ] questfoundry-spec repo renamed and updated
- [ ] Schema URLs resolve correctly at `https://questfoundry.liesdonk.nl/schemas/`
- [ ] GitHub Actions publish schemas on release
- [ ] questfoundry-py repository created with Epic 1 structure
- [ ] questfoundry-cli repository created with Epic 1 structure
- [ ] All documentation cross-links work
- [ ] spec-tools/ renamed and functional
- [ ] Migration announcement published
- [ ] No broken external links

---

## Timeline

**Week 1: Spec Repo Migration**
- Days 1-2: Preparation and decisions
- Days 3-4: Schema publishing setup
- Day 5: Repository rename and updates

**Week 2: New Repos**
- Days 1-2: Create questfoundry-py
- Days 3-4: Create questfoundry-cli
- Day 5: Testing and documentation

**Week 3: Polish**
- Post-migration cleanup
- Communication and announcements
- Begin Layer 6 Epic 1 implementation

---

## Questions for Decision

1. **Schema Hosting:** Confirm Option A (GitHub Pages with custom domain) is feasible
2. **Schema Version:** Confirm `0.1.0` as initial schema release version
3. **Migration Timing:** Best time to execute rename (consider active PRs, external references)
4. **Communication:** Who needs to be notified about migration? (contributors, users, etc.)

---

## Next Steps

After approval of this plan:

1. Execute Phase 1 (Preparation)
2. Set up GitHub Actions (see next document)
3. Begin repository rename process
4. Create new implementation repositories

---

**Document Status:** Ready for review
**Author:** Claude
**Reviewer:** [Your name]
**Approval Date:** [TBD]
