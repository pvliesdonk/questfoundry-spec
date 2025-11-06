# GitHub Workflows - Deployment Flow Documentation

## Current Workflows

### 1. `publish-schemas.yml`

- **Triggers on:** `schemas-v*.*.*` tags
- **Purpose:** Create GitHub Release with schema bundle
- **Does NOT:** Deploy to Pages

### 2. `publish-protocol.yml`

- **Triggers on:** `protocol-v*.*.*` tags
- **Purpose:** Create GitHub Release with protocol bundle
- **Does NOT:** Deploy to Pages

### 3. `deploy-to-pages.yml` (NEW - Unified)

- **Triggers on:** Push to `main` branch with changes to `03-schemas/**` or `04-protocol/**`
- **Purpose:** Deploy schemas AND protocol to GitHub Pages
- **Replaces:** Old `deploy-schemas-to-pages.yml`

### 4. ~~`deploy-schemas-to-pages.yml`~~ (REMOVED)

- **Status:** Deleted to prevent conflicts
- **Issue:** Used same concurrency group as new workflow

---

## Why Pages Deployment Didn't Happen

### Root Cause

The `deploy-to-pages.yml` workflow only exists on the feature branch
(`claude/loop-focused-architecture-011CUpdeFWEHtQM1a3wv2GuD`), not on `main` yet.

### What Happened

1. ✅ User created `protocol-v0.2.1` tag
2. ✅ `publish-protocol.yml` ran and created GitHub Release
3. ❌ Pages deployment didn't run because:
   - The new `deploy-to-pages.yml` doesn't exist on `main` branch yet
   - The old `deploy-schemas-to-pages.yml` only handled schemas, not protocol
   - Tags don't trigger the Pages deployment workflow (only pushes to main do)

---

## How to Fix

### Step 1: Merge Feature Branch to Main

```bash
git checkout main
git pull origin main
git merge claude/loop-focused-architecture-011CUpdeFWEHtQM1a3wv2GuD
git push origin main
```

**This will:**

- Add the new unified `deploy-to-pages.yml` workflow to main
- Remove the old conflicting workflow
- Include protocol changes (04-protocol/\*\* changes)
- **Automatically trigger GitHub Pages deployment** (because of 04-protocol/\*\* changes)

### Step 2: Verify GitHub Pages Configuration

Ensure repository settings are correct:

1. Go to: **Settings → Pages**
2. **Source:** Should be "GitHub Actions" (not "Deploy from a branch")
3. **Custom domain:** Configure `questfoundry.liesdonk.nl` if desired

---

## Workflow Execution Sequence

### For Schema Releases

```text
1. Create schemas-vX.Y.Z tag → publish-schemas.yml runs
   ├─ Creates GitHub Release
   └─ Uploads schema bundle

2. Merge to main (if schemas changed) → deploy-to-pages.yml runs
   ├─ Deploys to GitHub Pages
   └─ Updates https://questfoundry.liesdonk.nl/schemas/
```

### For Protocol Releases

```text
1. Create protocol-vX.Y.Z tag → publish-protocol.yml runs
   ├─ Creates GitHub Release
   └─ Uploads protocol bundle

2. Merge to main (if protocol changed) → deploy-to-pages.yml runs
   ├─ Deploys to GitHub Pages
   └─ Updates https://questfoundry.liesdonk.nl/protocol/
```

### For Both (Coordinated Release)

```text
1. Create schemas-vX.Y.Z tag → publish-schemas.yml runs
2. Create protocol-vX.Y.Z tag → publish-protocol.yml runs
3. Merge to main → deploy-to-pages.yml runs ONCE
   ├─ Deploys BOTH schemas and protocol
   └─ Updates entire Pages site
```

---

## Concurrency Protection

All Pages deployments use:

```yaml
concurrency:
  group: "pages"
  cancel-in-progress: false
```

This ensures:

- Only one Pages deployment runs at a time
- No conflicts between multiple pushes to main
- Older deployments don't override newer ones

---

## Manual Trigger

You can manually trigger Pages deployment:

1. Go to: **Actions → Deploy Schemas and Protocol to GitHub Pages**
2. Click: **Run workflow**
3. Select branch: `main`
4. Click: **Run workflow**

---

## Verification After Merge

After merging to main, check:

1. **Actions tab:** `Deploy Schemas and Protocol to GitHub Pages` should run
2. **Pages URL:** `https://<user>.github.io/<repo>/` should show both:
   - `/schemas/` directory
   - `/protocol/` directory
3. **Schema $id fields:** Should resolve (e.g.,
   `https://questfoundry.liesdonk.nl/schemas/hook_card.schema.json`)
4. **Protocol $id fields:** Should resolve (e.g.,
   `https://questfoundry.liesdonk.nl/protocol/envelope.schema.json`)

---

## Troubleshooting

### Issue: Pages deployment fails with "404 Not Found"

**Solution:** Check that GitHub Pages is enabled and source is set to "GitHub Actions"

### Issue: Workflow doesn't trigger after merge

**Solution:** Ensure changes touched `03-schemas/**` or `04-protocol/**` paths

### Issue: Old workflow still running

**Solution:** Disable old workflow in Actions → Workflows → Select workflow → "..." → Disable
workflow

### Issue: Custom domain not resolving

**Solution:**

1. Add CNAME file: `echo "questfoundry.liesdonk.nl" > docs/CNAME`
2. Configure DNS: Point CNAME to `<user>.github.io`
3. Wait for DNS propagation (up to 24 hours)

---

## Summary

**Current Status:**

- ✅ GitHub Releases work correctly (publish-schemas.yml, publish-protocol.yml)
- ✅ Unified Pages workflow created (deploy-to-pages.yml)
- ✅ Old conflicting workflow removed
- ⏳ Pages deployment will happen after merge to main

**Next Steps:**

1. Merge feature branch to main
2. Verify Pages deployment runs
3. Test canonical URLs
4. Configure custom domain (optional)
