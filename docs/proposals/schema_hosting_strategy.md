# Schema Hosting Strategy

**Date:** 2025-11-05 **Status:** Proposal **Context:** `questfoundry.liesdonk.nl` is a placeholder;
`liesdonk.nl` domain is owned

---

## Current State

All 18 schemas currently reference canonical URLs:

```json
{
  "$id": "https://questfoundry.liesdonk.nl/schemas/hook_card.schema.json"
}
```

**Problem:** These URLs don't currently resolve. Domain is owned but not yet configured.

---

## Recommended Strategy: Phased Approach

### Phase 1: Immediate (Use GitHub as Primary)

**Don't change schema $id URLs** - treat them as future canonical references.

**Active distribution channels:**

1. **GitHub Releases** (primary for now)
   - Asset: `questfoundry-schemas-v{version}.zip`
   - Includes all schemas + README
   - **Works immediately**, no domain setup needed

2. **GitHub Raw URLs** (direct access)
   - Pattern:
     `https://raw.githubusercontent.com/pvliesdonk/questfoundry-spec/main/03-schemas/{schema}.json`
   - **Works immediately**, no configuration needed
   - Good for CI/CD validation

3. **PyPI Package** (bundled)
   - Package: `questfoundry-py`
   - Python access: `get_schema('hook_card')`
   - **Works immediately** once package published

**Documentation approach:**

```markdown
## Accessing Schemas

**Note:** Canonical URLs (`questfoundry.liesdonk.nl`) are being configured. Currently use these
alternatives:

### 1. GitHub Releases (Recommended for offline use)

[Download schema bundle](releases/latest)

### 2. Raw GitHub (Direct access)

https://raw.githubusercontent.com/pvliesdonk/questfoundry-spec/main/03-schemas/hook_card.schema.json

### 3. Python Package

pip install questfoundry-py
```

### Phase 2: Domain Setup (When Ready)

**Steps to activate canonical URLs:**

1. **Configure DNS** (at `liesdonk.nl` registrar):

   ```
   Type: CNAME
   Name: questfoundry
   Value: pvliesdonk.github.io
   TTL: 3600
   ```

2. **Enable GitHub Pages** (in questfoundry-spec repo):
   - Settings → Pages → Source: Deploy from branch
   - Branch: `main` / folder: `/docs`
   - Custom domain: `questfoundry.liesdonk.nl`
   - Enforce HTTPS: Yes

3. **Create schema directory structure**:

   ```bash
   mkdir -p docs/schemas
   # Copy or symlink from 03-schemas/
   cp 03-schemas/*.json docs/schemas/
   ```

4. **Add index page** (`docs/index.html`):

   ```html
   <!DOCTYPE html>
   <html>
     <head>
       <title>QuestFoundry Schemas</title>
       <meta
         http-equiv="refresh"
         content="0; url=https://github.com/pvliesdonk/questfoundry-spec"
       />
     </head>
     <body>
       <p>
         Redirecting to
         <a href="https://github.com/pvliesdonk/questfoundry-spec">QuestFoundry Specification</a>
       </p>
     </body>
   </html>
   ```

5. **Test resolution**:
   ```bash
   curl https://questfoundry.liesdonk.nl/schemas/hook_card.schema.json
   ```

**Timeline:** Can be done anytime, no urgency. Schemas work fine via GitHub in the meantime.

---

## Alternative: Update Schema $id URLs Now

**Option B:** Change schema `$id` to GitHub Raw URLs immediately.

**Pros:**

- URLs work immediately
- No future domain setup needed
- Simpler long-term

**Cons:**

- Breaking change (need to update all 18 schemas)
- Less professional-looking URLs
- GitHub dependency explicit

**Example change:**

```json
{
  "$id": "https://raw.githubusercontent.com/pvliesdonk/questfoundry-spec/v0.1.0/03-schemas/hook_card.schema.json"
}
```

**Recommendation:** Don't do this. Keep placeholder URLs as aspirational canonical references.

---

## Comparison Matrix

| Method          | Works Now               | Professional | Stable  | Setup              |
| --------------- | ----------------------- | ------------ | ------- | ------------------ |
| GitHub Releases | ✅ Yes                  | ⭐⭐⭐       | ✅ Very | None               |
| GitHub Raw      | ✅ Yes                  | ⭐⭐         | ✅ Very | None               |
| PyPI Package    | ✅ Yes (once published) | ⭐⭐⭐⭐     | ✅ Very | Package setup      |
| Custom Domain   | ❌ Not yet              | ⭐⭐⭐⭐⭐   | ✅ Very | DNS + GitHub Pages |

---

## Recommended Documentation

### In 03-schemas/README.md

```markdown
## Accessing Schemas

### Canonical URLs (Future)

All schemas use canonical URLs in their `$id` field:
```

https://questfoundry.liesdonk.nl/schemas/{schema-name}.schema.json

````

**Note:** These URLs are being configured. Use alternatives below in the meantime.

### Active Access Methods

#### 1. GitHub Releases (Offline Bundle)

Download the complete schema set:

```bash
# Latest release
wget https://github.com/pvliesdonk/questfoundry-spec/releases/latest/download/questfoundry-schemas-v0.1.0.zip
````

#### 2. Raw GitHub (Direct Access)

```bash
# Individual schema
curl https://raw.githubusercontent.com/pvliesdonk/questfoundry-spec/main/03-schemas/hook_card.schema.json

# In validation tools
ajv validate \
  -s https://raw.githubusercontent.com/pvliesdonk/questfoundry-spec/main/03-schemas/hook_card.schema.json \
  -d your-hook.json
```

#### 3. Python Package (Recommended for Python projects)

```bash
pip install questfoundry-py
```

```python
from questfoundry.resources import get_schema
schema = get_schema('hook_card')
```

### Version Pinning

For production use, pin to specific version:

```bash
# Pin to release tag
curl https://raw.githubusercontent.com/pvliesdonk/questfoundry-spec/schemas-v0.1.0/03-schemas/hook_card.schema.json
```

```

---

## Migration Impact: MINIMAL

**Good news:** Schema hosting method doesn't affect migration timeline.

**What changes:**
- Remove "GitHub Pages setup" from Phase 2 of migration plan
- Update documentation to reflect GitHub-first approach
- Custom domain becomes "nice to have" enhancement, not blocker

**What stays the same:**
- Schema $id URLs remain unchanged
- GitHub Actions for releases work immediately
- All distribution channels work except canonical domain
- Can set up domain later without breaking changes

---

## Decision Required

**Recommended: Proceed with GitHub-first approach**

✅ Keep schema `$id` URLs as-is (aspirational)
✅ Use GitHub Releases + Raw URLs as primary distribution
✅ Set up custom domain later (non-blocking)

**Alternative: Update schema $id URLs to GitHub**

- More work now (update 18 schemas)
- Less elegant URLs
- Not recommended unless domain setup is uncertain

---

## Next Steps

1. **Immediate:** Proceed with migration using GitHub-first strategy
2. **Week 1-2:** Create GitHub Actions for schema releases (works immediately)
3. **Week 3-4:** Begin Layer 6/7 implementation (uses bundled schemas)
4. **Future:** Set up `questfoundry.liesdonk.nl` when convenient
   - Will require: DNS CNAME, GitHub Pages config, 15 min setup
   - Non-breaking enhancement
   - Makes schema $id URLs resolve

---

**Recommendation:** ✅ GitHub-first approach
**Priority:** High (schema distribution) → Low (custom domain)
**Blocker:** None - proceed with migration
```
