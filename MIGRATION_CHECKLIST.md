# QuestFoundry Layer 6/7 Migration - Execution Checklist

**Status:** Ready to Execute **Domain:** ✅ questfoundry.liesdonk.nl configured **Approval:** ✅
Three-repository architecture approved **Date:** 2025-11-05

---

## Phase 1: Enable GitHub Pages (Do First - ~5 minutes)

### Step 1.1: Configure GitHub Pages

**Action Required:** Configure in GitHub UI

1. Go to: https://github.com/pvliesdonk/questfoundry/settings/pages
2. **Source:**
   - Select: "Deploy from a branch"
   - Branch: `main`
   - Folder: `/docs`
3. **Custom domain:**
   - Enter: `questfoundry.liesdonk.nl`
   - Click "Save"
   - Wait for DNS check (may take a few minutes)
4. **Enforce HTTPS:**
   - Check the "Enforce HTTPS" box (once DNS check passes)
5. Click "Save"

**Expected Result:** DNS check should pass (domain is already configured)

### Step 1.2: Verify Deployment

**Wait 2-5 minutes** for initial deployment, then test:

```bash
# Test main page
curl -I https://questfoundry.liesdonk.nl/

# Test schema access
curl https://questfoundry.liesdonk.nl/schemas/hook_card.schema.json | jq '.title'
# Should return: "Hook Card"
```

**Checklist:**

- [ ] GitHub Pages enabled
- [ ] Custom domain configured
- [ ] HTTPS enforced
- [ ] Main page loads: https://questfoundry.liesdonk.nl/
- [ ] Schema accessible: https://questfoundry.liesdonk.nl/schemas/hook_card.schema.json
- [ ] All 18 schemas accessible

---

## Phase 2: Test Schema Publishing Workflow (~10 minutes)

### Step 2.1: Create Schema Release Tag

```bash
# From repository root
cd /home/user/questfoundry

# Create and push tag
git tag schemas-v0.1.0 -m "Initial schema release"
git push origin schemas-v0.1.0
```

### Step 2.2: Monitor GitHub Actions

1. Go to: https://github.com/pvliesdonk/questfoundry/actions
2. Watch "Publish Schemas" workflow run
3. Verify it completes successfully (green checkmark)

### Step 2.3: Verify Release Created

1. Go to: https://github.com/pvliesdonk/questfoundry/releases
2. Verify "Schemas v0.1.0" release exists
3. Download and check contents:
   - `questfoundry-schemas-v0.1.0.zip`
   - `questfoundry-schemas-v0.1.0.zip.sha256`

**Checklist:**

- [ ] Tag created and pushed
- [ ] GitHub Action completed successfully
- [ ] GitHub Release published
- [ ] Schema bundle downloadable
- [ ] Checksum file present

---

## Phase 3: Repository Rename (~15 minutes)

⚠️ **IMPORTANT:** Coordinate with any active PRs or external references

### Step 3.1: Pre-Rename Backups

```bash
# Document current state
git log --oneline -10 > .migration-backup-log.txt
git remote -v > .migration-backup-remotes.txt
git branch -a > .migration-backup-branches.txt
```

### Step 3.2: Rename Repository

**Action Required:** Rename in GitHub UI

1. Go to: https://github.com/pvliesdonk/questfoundry/settings
2. Scroll to "Repository name"
3. Change from: `questfoundry`
4. Change to: `questfoundry-spec`
5. Click "Rename"
6. **GitHub automatically creates redirect from old name**

### Step 3.3: Update Local Repository

```bash
# Update remote URL (optional - redirect works, but this is cleaner)
git remote set-url origin https://github.com/pvliesdonk/questfoundry-spec.git

# Verify
git remote -v
```

### Step 3.4: Update README

```bash
# Add redirect notice banner to README.md
```

**Banner text to add at top of README:**

```markdown
> **📦 Repository Renamed** This repository was renamed from `questfoundry` to `questfoundry-spec`
> on 2025-11-05. GitHub automatically redirects, but please update your bookmarks.
>
> **Looking for implementations?**
>
> - 🐍 Python Library: [questfoundry-py](https://github.com/pvliesdonk/questfoundry-py)
> - 🖥️ CLI Tool: [questfoundry-cli](https://github.com/pvliesdonk/questfoundry-cli)
```

**Checklist:**

- [ ] Backups created
- [ ] Repository renamed to `questfoundry-spec`
- [ ] Local remote URL updated
- [ ] README updated with redirect notice
- [ ] Changes committed and pushed

---

## Phase 4: Rename tools → spec-tools (~5 minutes)

```bash
# Rename directory
git mv tools spec-tools

# Update references in README
# Search and replace: "tools/" → "spec-tools/"

# Update workflow file
sed -i 's|cd tools|cd spec-tools|g' .github/workflows/publish-schemas.yml
sed -i 's|cd tools|cd spec-tools|g' .github/workflows/deploy-schemas-to-pages.yml

# Update any other references
grep -r "cd tools" . --exclude-dir=.git
# Manually fix any remaining references

# Commit
git add -A
git commit -m "refactor: rename tools/ to spec-tools/ for clarity

Clarifies that these are spec development tools, not runtime tools."

git push
```

**Checklist:**

- [ ] Directory renamed
- [ ] README references updated
- [ ] Workflow files updated
- [ ] All references checked
- [ ] Changes committed and pushed

---

## Phase 5: Create New Repositories (~30 minutes)

### Step 5.1: Create questfoundry-py Repository

````bash
# Create repository
gh repo create pvliesdonk/questfoundry-py --public \
  --description "Layer 6: Python library for QuestFoundry protocol and artifact management"

# Clone and set up
cd /home/user
git clone https://github.com/pvliesdonk/questfoundry-py.git
cd questfoundry-py

# Add spec as submodule
git submodule add https://github.com/pvliesdonk/questfoundry-spec.git spec

# Initialize Python project structure (Epic 1 from implementation plan)
mkdir -p src/questfoundry
mkdir -p tests
touch src/questfoundry/__init__.py
touch src/questfoundry/py.typed

# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[project]
name = "questfoundry-py"
version = "0.1.0"
description = "Python library for QuestFoundry protocol and artifact management"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [
  {name = "QuestFoundry Team"}
]
dependencies = [
    "pydantic>=2.0",
    "jsonschema>=4.0",
    "httpx>=0.25",
    "python-dotenv>=1.0",
]

[project.urls]
Homepage = "https://github.com/pvliesdonk/questfoundry-py"
Documentation = "https://github.com/pvliesdonk/questfoundry-spec"
Specification = "https://questfoundry.liesdonk.nl"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0",
    "mypy>=1.0",
    "ruff>=0.1.0",
]
EOF

# Create README
cat > README.md << 'EOF'
# QuestFoundry Python Library

Layer 6 implementation for QuestFoundry - protocol client, validators, and artifact management.

## Installation

```bash
pip install questfoundry-py
````

## Quick Start

```python
from questfoundry import ProtocolClient, Workspace

# Create workspace
workspace = Workspace.init("my-project.qfproj")

# Access schemas
from questfoundry.resources import get_schema
schema = get_schema('hook_card')
```

## Documentation

- [Specification](https://github.com/pvliesdonk/questfoundry-spec)
- [Schemas](https://questfoundry.liesdonk.nl)
- [Implementation Plan](https://github.com/pvliesdonk/questfoundry-spec/blob/main/06-libraries/IMPLEMENTATION_PLAN.md)

## Development

See implementation plan:
[06-libraries/IMPLEMENTATION_PLAN.md](https://github.com/pvliesdonk/questfoundry-spec/blob/main/06-libraries/IMPLEMENTATION_PLAN.md)

## License

MIT EOF

# Create .gitignore

cat > .gitignore << 'EOF'

# Python

**pycache**/ _.py[cod] _$py.class _.so .Python build/ develop-eggs/ dist/ downloads/ eggs/ .eggs/
lib/ lib64/ parts/ sdist/ var/ wheels/ _.egg-info/ .installed.cfg \*.egg

# Virtual environments

.venv/ venv/ ENV/

# IDEs

.vscode/ .idea/ _.swp _.swo

# Testing

.pytest_cache/ .coverage htmlcov/

# UV

.uv/ uv.lock EOF

# Commit

git add -A git commit -m "Initial project structure - Epic 1 foundation" git push -u origin main

````

### Step 5.2: Create questfoundry-cli Repository

```bash
# Create repository
gh repo create pvliesdonk/questfoundry-cli --public \
  --description "Layer 7: Command-line interface for QuestFoundry"

# Clone and set up
cd /home/user
git clone https://github.com/pvliesdonk/questfoundry-cli.git
cd questfoundry-cli

# Add spec as submodule
git submodule add https://github.com/pvliesdonk/questfoundry-spec.git spec

# Initialize CLI project structure
mkdir -p src/qf/commands
touch src/qf/__init__.py
touch src/qf/py.typed

# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[project]
name = "questfoundry-cli"
version = "0.1.0"
description = "Command-line interface for QuestFoundry"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "MIT"}
dependencies = [
    "questfoundry-py>=0.1.0",
    "typer[all]>=0.9.0",
    "rich>=13.0.0",
    "questionary>=2.0.0",
    "python-dotenv>=1.0.0",
]

[project.scripts]
qf = "qf.cli:app"

[project.urls]
Homepage = "https://github.com/pvliesdonk/questfoundry-cli"
Documentation = "https://github.com/pvliesdonk/questfoundry-spec"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0",
    "mypy>=1.0",
    "ruff>=0.1.0",
]
EOF

# Create README
cat > README.md << 'EOF'
# QuestFoundry CLI

Layer 7 command-line interface for QuestFoundry.

## Installation

```bash
pip install questfoundry-cli
````

## Quick Start

```bash
# Create new project
qf init my-adventure

# Run quickstart
qf quickstart

# Generate assets
qf generate image SHOTLIST-001
```

## Documentation

- [Specification](https://github.com/pvliesdonk/questfoundry-spec)
- [Implementation Plan](https://github.com/pvliesdonk/questfoundry-spec/blob/main/07-ui/IMPLEMENTATION_PLAN.md)

## Development

See implementation plan:
[07-ui/IMPLEMENTATION_PLAN.md](https://github.com/pvliesdonk/questfoundry-spec/blob/main/07-ui/IMPLEMENTATION_PLAN.md)

## License

MIT EOF

# Same .gitignore as questfoundry-py

cp ../questfoundry-py/.gitignore .

# Commit

git add -A git commit -m "Initial project structure - Epic 1 foundation" git push -u origin main

````

**Checklist:**
- [ ] questfoundry-py repo created
- [ ] questfoundry-py initialized with Epic 1 structure
- [ ] questfoundry-py spec submodule added
- [ ] questfoundry-cli repo created
- [ ] questfoundry-cli initialized with Epic 1 structure
- [ ] questfoundry-cli spec submodule added

---

## Phase 6: Update Documentation (~15 minutes)

### Step 6.1: Update questfoundry-spec README

Add to top (after rename banner):

```markdown
## Related Repositories

This is the **specification repository** for QuestFoundry.

**Implementations:**
- 🐍 **[questfoundry-py](https://github.com/pvliesdonk/questfoundry-py)** - Layer 6: Python library
- 🖥️ **[questfoundry-cli](https://github.com/pvliesdonk/questfoundry-cli)** - Layer 7: CLI tool

**Schemas:**
- 🔗 Canonical URLs: https://questfoundry.liesdonk.nl/schemas/
- 📦 Downloads: [GitHub Releases](https://github.com/pvliesdonk/questfoundry-spec/releases)
````

### Step 6.2: Update 03-schemas/README.md

Update schema access section to reflect canonical URLs are now live.

### Step 6.3: Create Migration Announcement

Create GitHub Discussion announcing migration and new repositories.

**Checklist:**

- [ ] questfoundry-spec README updated
- [ ] 03-schemas/README.md updated
- [ ] Layer 6 and 7 README files reference spec repo
- [ ] GitHub Discussion created

---

## Phase 7: Verification (~10 minutes)

### Final Checks

```bash
# Test canonical schema URLs
curl -I https://questfoundry.liesdonk.nl/schemas/hook_card.schema.json
# Should return 200 OK

# Test old repo name redirect
curl -I https://github.com/pvliesdonk/questfoundry
# Should redirect to questfoundry-spec

# Test schema validation
curl https://questfoundry.liesdonk.nl/schemas/hook_card.schema.json | \
  python3 -c "import sys, json; json.load(sys.stdin); print('✓ Valid JSON')"

# Clone new repos
cd /tmp
git clone https://github.com/pvliesdonk/questfoundry-py
git clone https://github.com/pvliesdonk/questfoundry-cli
# Both should clone successfully

# Check submodules
cd questfoundry-py && git submodule status
cd ../questfoundry-cli && git submodule status
# Should show spec submodule
```

**Checklist:**

- [ ] Canonical URLs resolve correctly
- [ ] Old repo name redirects work
- [ ] GitHub Pages deployed successfully
- [ ] New repositories are public and accessible
- [ ] Submodules initialized correctly
- [ ] All documentation links work

---

## Post-Migration Tasks

### Immediate (Week 1)

- [ ] Begin Layer 6 Epic 1 implementation
- [ ] Set up CI/CD for questfoundry-py
- [ ] Set up CI/CD for questfoundry-cli
- [ ] Update contribution guidelines

### Short-term (Week 2-4)

- [ ] Implement Layer 6 Epic 2 (schema bundling and validation)
- [ ] Begin Layer 7 Epic 1 (CLI foundation)
- [ ] Create first alpha releases
- [ ] Write getting-started tutorials

---

## Rollback Plan (If Needed)

If critical issues arise:

1. **Repository rename:** Can rename back (redirect will update)
2. **GitHub Pages:** Can disable in settings
3. **New repos:** Can archive or delete if unused
4. **No schema changes made:** Original files unchanged

---

## Success Criteria

Migration is successful when:

- ✅ questfoundry.liesdonk.nl/schemas/ resolves correctly
- ✅ Repository renamed to questfoundry-spec
- ✅ GitHub redirect from questfoundry works
- ✅ spec-tools/ renamed and functional
- ✅ questfoundry-py repo created and initialized
- ✅ questfoundry-cli repo created and initialized
- ✅ Schema release workflow tested
- ✅ All documentation updated and links work
- ✅ No broken external references

---

## Current Status

**Completed:**

- ✅ Migration plan approved
- ✅ Domain configured (questfoundry.liesdonk.nl)
- ✅ GitHub Pages structure prepared (docs/ directory)
- ✅ GitHub Actions created
- ✅ Schema version files created

**Next Step:** Phase 1 - Enable GitHub Pages

**Estimated Time:** 90 minutes total
