# Post‑Mortem — "Midnight Deposition" TU Cycle (Cold @ 2025-11-04)

## 0) Why this write‑up exists (and why it's longer)

This post‑mortem is deliberately expansive so that anyone—future us, another LLM, or a human
team—can reconstruct _what happened_, _why it happened_, and _how we made it better_. It captures
process flow, missteps, device quirks, and policy decisions so the next loop starts from a firmer
ground. Consider it the living appendix to the runner.

---

## 1) Scope & Working Context

- **Initiative:** Detective‑noir interactive manuscript (choice‑driven) orchestrated by the
  **Showrunner**. Core roles: **Plotwright** (structure/plot), **Scene Smith** (beats → scenes),
  **Style Lead** (voice, paragraph density), **Art Director/Illustrator** (covers/plates/thumbs).
- **Targets:** ~30 sections; **3–4 paragraphs of prose per section**, gritty noir voice with longer
  paragraphs (explicit SL steer).
- **Pipelines exercised:** Lore Deepening → Story Spark → PW → SS → SL (iterate to stabilization) →
  Hook Harvest → Book Binder → AD/Illustrator → Exporters (Markdown/HTML/EPUB).
- **Licensing & authorship:** **CC BY‑NC 4.0**; Author **Peter van Liesdonk**; Showrunner assigned
  title **"Midnight Deposition."**

---

## 2) Deliverables & State

### Manuscript & Metadata

- Manuscript stabilized in Hot/Cold SoT; Style Lead locked tone to "grit + longer paras."
- Metadata centralized (title/author/license/description/subjects) and injected into exporters.

### Art

- **Approved**: title‑locked **PNG** cover (with title), SVG cover as backup; interior plate
  **A2_K**; scene plate **A3_H**; square vignette **A1_H**.
- **Rejected**: early "book mockup" interior (prompt bias).
- **Manifest**: `art_manifest.updated.json` includes roles, sizes, captions, filenames, and
  **SHA‑256 hashes**.

### EPUB Builds (key milestones)

1. **Link‑repair build** (anti‑spoiler start; cross‑file anchors fixed).
2. **With art** (images injected at their anchors).
3. **Title policy enforced** (title‑locked PNG as `cover-image`; SVG backup included).
4. **Captions from manifest** rendered into `<figcaption>`.
5. **Final so far**: `midnight_deposition_cover_png_titled_from_illustrator.epub`.

---

## 3) What Worked (the boring but important wins)

- **Role handoffs stabilized prose**: PW→SS→SL loop produced consistent voice and scene density;
  lore deepening + hook harvest added affordances without destabilizing.
- **Exporter hardening**:
  - Start at **Section 1** (no TOC/anchor‑map in spine).
  - Cross‑file links normalized to `NNN.xhtml#ID`.
  - Captions are **manifest‑driven** (prevents drift).
  - **Cover policy**: ship **only** title‑bearing covers; keep SVG backup.
- **Art pipeline discipline**: strict prompts ("scene‑only; no book/magazine/mockup/text"),
  deterministic filenames, SHA‑256 hashing, and explicit approvals/rejections recorded.

---

## 4) What Didn't (and how we tripped into it)

- **Early narrative oddities**: in pre‑stabilization runs we saw **S1 choices funnel to S2** and
  muddled S1 prose. Diagnosis: prompt drift + trying to "ship a demo" before stabilization.
- **Book Binder choice layout**: inconsistent UX—sometimes **entire choice is a link**, elsewhere
  **label + trailing link**. This inconsistency confuses readers and downstream converters.
- **Section header hygiene**: some headers contain operational words like **"Hub," "Unofficial,"
  "Quick."** Those are helpful while drafting, but **not reader‑facing** and leak process into the
  prose.
- **Art misrender (book mockup)**: classic image‑model bias when asked for "book/illustration"—fixed
  by hard prompt steer and separating title‑locked covers from interior/scene prompts.
- **Typeface gap**: no agreed font family at first; we later set policy for free, embeddable fonts.
- **Export wobble**: first EPUB opened on TOC; second had link targets that were fine in mobile
  readers but failed on **Kobo Clara 2e**.

---

## 5) Root Causes (blame the system, then fix the system)

- **Protocol vs. demo instinct**: we optimized for "show structure fast" instead of "complete per
  spec." The spec demands no placeholders; narrative JSON/MD is canonical.
- **Cognitive load shortcuts**: complex prose and art were deferred while the pipeline was
  proven—this created tech debt.
- **Model bias (imagery)**: without explicit negations, models generate mockups/layouts.
- **Template leakage**: Binder templates expose drafting labels (Hub/Quick/Unofficial) into headers
  if not sanitized at export time.
- **Device variance**: the Kobo stack differs in EPUB3/anchor handling from some mobile readers.

---

## 6) Device‑Specific Finding — Kobo Clara 2e Hyperlinks

**Observed:** Internal hyperlinks work in a mobile EPUB reader but **don't** trigger on **Kobo Clara
2e** for the same file.

**Likely factors (Kobo quirks + EPUB compat):**

- **Cross‑file anchors**: some Kobo firmware builds are picky about `file.xhtml#anchor`
  targets—especially when the anchor is on a parent element like `<section id="…">` rather than an
  explicit inline anchor.
- **Anchor targets**: better reliability when we include a **dedicated inline anchor** at the top of
  the section: `<a id="A1_H"></a>` or `<span id="A1_H"></span>`, not just an `id` on `<section>` or
  `<h2>`.
- **EPUB2 vs EPUB3 navigation**: older Kobo handling improves if we also ship a **legacy NCX
  (`toc.ncx`)** alongside `nav.xhtml`.
- **Guide landmarks**: adding a `guide`/`landmarks` block (EPUB2/ARIA) can influence start positions
  and link resolution on older stacks.
- **Filename/ID strictness**: mixed case/underscores generally work, but we'll enforce **ASCII‑safe,
  lowercase, dash‑separated IDs** for maximum compatibility.

**Mitigations to implement in our exporter:**

1. **Twin anchors** at the top of every section: keep `id` on `<section>` _and_ add
   `<a id="ID"></a>` immediately inside.
2. **Legacy NCX**: generate and include `toc.ncx` (manifest `application/x-dtbncx+xml`) in addition
   to EPUB3 `nav.xhtml`.
3. **Landmarks**: include ARIA/EPUB landmarks and (if needed) EPUB2 `guide` for start page.
4. **ID policy**: normalize all anchors to **lowercase‑dash** and rewrite links accordingly (ship an
   alias map so existing links still work).
5. **Optional Kobo‑compat build**: offer a **single‑file spine** variant (all sections in one XHTML)
   for devices that mishandle cross‑file fragments.

---

## 7) Fixes Already Applied

- **Exporter invariants**: start at Scene 1; frontmatter outside spine; anchors cross‑file; captions
  from manifest; CC BY‑NC 4.0 stamped throughout.
- **Cover policy**: final builds must use a **title‑locked PNG** as designated cover; a **titleful
  SVG** is included as backup; **no textless covers** in release artifacts.
- **Art pipeline**: prompt steer enforced; title typography only on covers; deterministic
  filenames + hashing; manifest records approvals/rejections.

---

## 8) Fixes To Apply Next (Binder & Exporters)

**Binder (manuscript presentation):**

- Sanitize reader‑facing headers (strip **Hub**, **Unofficial**, **Quick**, etc.); keep those only
  in developer notes or IDs.
- Standardize choice presentation: pick **either** "entire choice is link" **or** "label + linked
  target" and use it everywhere (recommend the latter for readability).

**Exporters (EPUB/HTML/Markdown):**

- Add **inline anchor spans** at section starts.
- Include **`toc.ncx`** and **EPUB landmarks/guide**.
- Normalize **anchor IDs** and provide an alias rewrite so older links still function.
- Add **Kobo validation gates** to CI (see §10).

---

## 9) Typeface & Typography Policy (cover _and_ prose)

- **Body**: _Source Serif 4_ (free, readable, EPUB‑friendly).
- **Display titles**: _Cormorant Garamond_ or _Playfair Display_.
- **Runner rule**: support loading from the user's fonts directory; embed in EPUB where licensing
  allows; fall back to system fonts otherwise.

---

## 10) CI/QA Recommendations (preventing déjà vu)

- **Cover guard**: fail build if `cover-image` is not a **title‑bearing PNG**; allow optional SVG
  backup.
- **Start‑page invariant**: assert reading order begins at first scene; frontmatter not in spine.
- **Anchor audit**: ensure every link target exists; ensure per‑section **inline anchors**; verify
  cross‑file links resolve.
- **Kobo check**: run an EPUB linter plus a **Kobo‑compat script** (simulated checks: NCX present,
  landmarks present, inline anchors present).
- **Manifest compliance**: all images listed in the art manifest, with captions and hashes; warn if
  caption missing.
- **Header hygiene**: fail if reader‑facing section titles contain "hub / unofficial / quick / temp
  / draft."

---

## 11) Actionable Checklist

- [ ] **Header cleanup**: strip operational markers from H2; preserve them only in IDs/notes.
- [ ] **Choice UX**: unify layout template.
- [ ] **EPUB compat**: add inline anchors + NCX + landmarks; test on Kobo Clara 2e.
- [ ] **ID normalization**: lowercase‑dash IDs + alias map.
- [ ] **Font embedding**: bundle Source Serif 4 + chosen display font; align cover + prose
      typography.
- [ ] **Art completion**: render remaining plates/thumbs; update hashes; re‑export.
- [ ] **HTML/MD parity**: export with the same anti‑spoiler, cover, captions, and anchors.
- [ ] **Validator report**: attach to release artifacts.

---

## 12) Art & File Inventory (for reproducibility)

- **Covers**: `art/cover_titlelocked.png` (primary), SVG backup in `/covers/`; alternate titled
  cover archived.
- **Interior & Scenes**: `art/plate_A2_K.png`, `art/plate_A3_H.png`, `art/thumb_A1_H.png`.
- **Manifests**: `art_manifest.updated.json` (statuses + SHA‑256).
- **EPUBs**: latest `midnight_deposition_cover_png_titled_from_illustrator.epub` (title‑locked PNG
  cover; captions; anti‑spoiler).

---

## 13) Closing Notes

We've moved from a wobbly demo mindset to a **spec‑true** pipeline: canonical manuscript first, then
art and exports that respect spoiler safety, device quirks, and typography consistency. The
remaining work is mostly _hygiene and compatibility_: naming, anchors, and Kobo‑friendly nav shims.
Once those are locked, this runner can scale to bigger books without re‑learning the same lessons.
