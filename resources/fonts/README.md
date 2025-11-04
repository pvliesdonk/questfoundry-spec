# Typography Policy

**Status:** ✅ Defined (2025-11-04)

**Purpose:** Establish embeddable fonts for EPUB/HTML exports with consistent cross-device rendering.

---

## Fonts for EPUB/HTML Exports

**Body Text:** Source Serif 4
**Display Titles:** Cormorant Garamond
**License:** SIL Open Font License (embeddable, redistributable)

---

## Directory Structure

```
/resources/fonts/
  source-serif-4/
    SourceSerif4-Regular.otf
    SourceSerif4-Italic.otf
    SourceSerif4-Bold.otf
    SourceSerif4-BoldItalic.otf
    LICENSE.txt
  cormorant-garamond/
    CormorantGaramond-Regular.ttf
    CormorantGaramond-Italic.ttf
    CormorantGaramond-Bold.ttf
    LICENSE.txt
```

---

## Font Installation

### Source Serif 4

**Download:** https://github.com/adobe-fonts/source-serif/releases

**Files needed:**
- SourceSerif4-Regular.otf
- SourceSerif4-Italic.otf
- SourceSerif4-Bold.otf
- SourceSerif4-BoldItalic.otf

**Installation:**
```bash
cd /resources/fonts/source-serif-4/
# Download release from GitHub
# Extract OTF files to this directory
# Include LICENSE.txt from source repository
```

**License:** SIL Open Font License 1.1
**Embeddable:** Yes (redistributable in EPUB/PDF)

---

### Cormorant Garamond

**Download:** https://github.com/CatharsisFonts/Cormorant/releases

**Files needed:**
- CormorantGaramond-Regular.ttf
- CormorantGaramond-Italic.ttf
- CormorantGaramond-Bold.ttf

**Installation:**
```bash
cd /resources/fonts/cormorant-garamond/
# Download release from GitHub
# Extract TTF files (Garamond variant) to this directory
# Include LICENSE.txt from source repository
```

**License:** SIL Open Font License 1.1
**Embeddable:** Yes (redistributable in EPUB/PDF)

---

## EPUB CSS Template

```css
/* Source Serif 4 - Body Text */
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
  font-family: 'Source Serif 4';
  src: url('../fonts/SourceSerif4-Bold.otf');
  font-weight: bold;
  font-style: normal;
}

@font-face {
  font-family: 'Source Serif 4';
  src: url('../fonts/SourceSerif4-BoldItalic.otf');
  font-weight: bold;
  font-style: italic;
}

/* Cormorant Garamond - Display Titles */
@font-face {
  font-family: 'Cormorant Garamond';
  src: url('../fonts/CormorantGaramond-Regular.ttf');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'Cormorant Garamond';
  src: url('../fonts/CormorantGaramond-Italic.ttf');
  font-weight: normal;
  font-style: italic;
}

@font-face {
  font-family: 'Cormorant Garamond';
  src: url('../fonts/CormorantGaramond-Bold.ttf');
  font-weight: bold;
  font-style: normal;
}

/* Typography Application */
body {
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 1em;
  line-height: 1.6;
}

h1, h2, h3 {
  font-family: 'Cormorant Garamond', Georgia, serif;
}

h1 {
  font-size: 2.5em;
  line-height: 1.2;
}

h2 {
  font-size: 2em;
  line-height: 1.3;
}

h3 {
  font-size: 1.5em;
  line-height: 1.4;
}
```

---

## Fallback Strategy

If fonts not available in `/resources/fonts/`:

**Body Text Fallback:**
- Georgia (serif, widely available)
- Times New Roman (serif, universal)
- serif (system default)

**Display Titles Fallback:**
- Georgia (serif, elegant)
- serif (system default)

**Book Binder Behavior:**
1. Check if fonts exist in `/resources/fonts/`
2. If present: embed in EPUB, include `@font-face` CSS
3. If absent: use system fallback fonts (Georgia, Times New Roman)
4. Log font embedding status in `view_log`

---

## Typography Principles

### Readability
- Source Serif 4 is designed for screen reading with large x-height and open counters
- Body text at 1em with 1.6 line-height provides comfortable reading
- Paragraph spacing (1em) creates visual separation

### Hierarchy
- Cormorant Garamond provides elegant contrast for titles and headers
- Display fonts are larger (2-2.5em) to establish clear hierarchy
- Bold weights available for emphasis

### Device Compatibility
- Both fonts render well on e-ink displays (Kobo, Kindle)
- OTF/TTF formats supported by all major EPUB readers
- Fallback fonts ensure graceful degradation

---

## Style Lead Integration

Typography decisions are made by **Style Lead** during style stabilization and stored in `style_manifest.json`.

**Example `style_manifest.json`:**
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
    "Source Serif 4 (Regular, Italic, Bold, BoldItalic)",
    "Cormorant Garamond (Regular, Italic, Bold)"
  ],
  "embed_in_epub": true
}
```

Book Binder reads this manifest and applies typography settings to all export formats.

---

## Validation Checklist

- [ ] Fonts are SIL OFL licensed (embeddable)
- [ ] All required font files present in `/resources/fonts/`
- [ ] LICENSE.txt included in each font directory
- [ ] `@font-face` declarations match file paths
- [ ] Fallback fonts specified in CSS
- [ ] Test rendering on:
  - [ ] Apple Books (iOS/macOS)
  - [ ] Kobo Clara 2e (e-ink)
  - [ ] Calibre (desktop)
  - [ ] Browser-based readers (Readium, etc.)

---

## References

- **SIL Open Font License:** https://scripts.sil.org/OFL
- **Source Serif 4:** https://github.com/adobe-fonts/source-serif
- **Cormorant:** https://github.com/CatharsisFonts/Cormorant
- **EPUB3 Spec (Fonts):** https://www.w3.org/TR/epub-33/#sec-resource-locations
- **Fix Proposal:** `/docs/post_mortems/2025-11-04_fix_proposal.md` (Proposal 6)
- **Style Manifest:** `/02-dictionary/artifacts/style_manifest.md`
- **Book Binder:** `/05-prompts/book_binder/system_prompt.md` (Typography section)

---

## Font Attribution

When using these fonts in exports, include attribution in front matter or copyright page:

```
Typography:
- Body text: Source Serif 4 by Adobe (SIL OFL 1.1)
- Display titles: Cormorant Garamond by Christian Thalmann (SIL OFL 1.1)
```
