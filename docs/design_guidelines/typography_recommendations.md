# Typography Recommendations

**Purpose:** Font pairing guidance for gamebooks by genre, with rationale and accessibility
considerations.

**Note:** These are **recommendations**, not requirements. Users may choose any fonts or create
custom pairings.

---

## How to Use This Document

Each genre has 2-3 recommended font pairings:

- **Prose font** - For body text (readability priority)
- **Display font** - For titles, headers, section markers
- **Rationale** - Why this pairing works for the genre
- **License** - Ensure legal use (SIL OFL, Apache, etc.)
- **Fallback** - Web-safe font if recommended not available

**For prompts:** Present these as options to users during style manifest creation, always allowing
custom fonts.

**For Style Lead:** Use as reference when guiding typography specifications.

---

## General Typography Principles

### **IMPORTANT:** Readability Over Theme (HARD RULE)

**This is the primary typography principle for gamebooks:**

- **Body text and choices MUST use readable fonts**—always prioritize legibility over aesthetic
- **Thematic fonts** (horror fonts, script fonts, pixel fonts, blackletter, etc.) may ONLY be used
  for:
  - Titles and chapter headings
  - Decorative headers
  - Non-essential flourishes
- **NEVER use thematic fonts for:**
  - Body prose
  - Choice text
  - Any text the user must read to progress

**Why this matters:** Gamebooks require sustained reading and frequent decision-making. Decorative
fonts cause eye strain, slow reading speed, and frustrate users. A horror story with Comic Sans body
text is more readable (and therefore better) than one with a "spooky" illegible font.

**For Style Lead:** This is a **hard constraint**. Reject thematic fonts for body text even if user
requests them. Explain why readability matters.

---

### Readability First

- **Prose fonts must be readable** at small sizes (12-16px)
- **Line height:** 1.4-1.6 for prose (higher for tighter fonts)
- **Line length:** 50-75 characters for optimal readability
- **Avoid:** Decorative fonts for body text, low-contrast pairings

### Hierarchy and Contrast

- **Display fonts** should contrast with prose (serif + sans, or different serif styles)
- **Weight contrast:** Display can be bold/black, prose should be regular/medium
- **Size contrast:** Titles 2-3x body text size

### Accessibility

- **Dyslexia-friendly:** Open dyslexic fonts or sans-serifs with distinct letterforms
- **Vision impairment:** High contrast, no thin weights for body text
- **WCAG compliance:** Color contrast ratios apply if fonts have color

### EPUB Considerations

- **Embed fonts** if using custom fonts (adds file size)
- **Fallback fonts** essential for EPUB readers that don't support embedding
- **Test across readers:** Kindle, Apple Books, Kobo may render differently

---

## Font Pairing by Genre

---

### Detective Noir

#### Classic Noir

**Prose:** Source Serif 4 **Display:** Cormorant Garamond **Rationale:** Evokes 1940s-50s pulp
fiction aesthetic. Source Serif 4 is highly readable with sharp serifs (clear even in low-light
reading). Cormorant Garamond adds elegant, dramatic contrast for chapter titles—evoking old
detective novel covers. **License:** SIL Open Font License **Fallback:** Georgia (universally
available, appropriate serif tone)

**Where to get:**

- Source Serif 4: [Google Fonts](https://fonts.google.com/specimen/Source+Serif+4)
- Cormorant Garamond: [Google Fonts](https://fonts.google.com/specimen/Cormorant+Garamond)

---

#### Modern Noir

**Prose:** IBM Plex Serif **Display:** Bebas Neue **Rationale:** Urban, industrial feel for
contemporary noir settings. IBM Plex Serif is clean and readable with technical precision. Bebas
Neue (bold, condensed sans) creates stark, impact-driven headers—like newspaper headlines or crime
scene markers. **License:** SIL Open Font License **Fallback:** Georgia + Impact

**Where to get:**

- IBM Plex Serif: [Google Fonts](https://fonts.google.com/specimen/IBM+Plex+Serif)
- Bebas Neue: [Google Fonts](https://fonts.google.com/specimen/Bebas+Neue)

---

### Fantasy / RPG

#### Epic Fantasy

**Prose:** Cinzel **Display:** Crimson Pro **Rationale:** Medieval, ornate aesthetic for classic
fantasy. Cinzel has Roman-inspired capitals (think ancient tomes). Crimson Pro is readable with
slight old-style flair—works for both body text and emphasis. **Note:** Cinzel can be hard to read
in large blocks; consider using for titles/headers only, not body text. **License:** SIL Open Font
License **Fallback:** Garamond + Times New Roman

**Where to get:**

- Cinzel: [Google Fonts](https://fonts.google.com/specimen/Cinzel)
- Crimson Pro: [Google Fonts](https://fonts.google.com/specimen/Crimson+Pro)

---

#### High Fantasy (Literary)

**Prose:** EB Garamond **Display:** Alegreya **Rationale:** Classic, literary feel. EB Garamond is
elegant and highly readable (based on historical Garamond). Alegreya has calligraphic details that
add fantasy flair without being illegible. **License:** SIL Open Font License **Fallback:**
Garamond + Georgia

**Where to get:**

- EB Garamond: [Google Fonts](https://fonts.google.com/specimen/EB+Garamond)
- Alegreya: [Google Fonts](https://fonts.google.com/specimen/Alegreya)

---

#### Dark Fantasy

**Prose:** Source Serif 4 **Display:** Spectral **Rationale:** Gothic, mysterious tone. Source Serif
4 keeps readability. Spectral has sharp serifs and slight gothic character (think dark grimoires)
for headers. **License:** SIL Open Font License **Fallback:** Georgia + Times New Roman

**Where to get:**

- Source Serif 4: [Google Fonts](https://fonts.google.com/specimen/Source+Serif+4)
- Spectral: [Google Fonts](https://fonts.google.com/specimen/Spectral)

---

### Horror / Thriller

#### Gothic Horror

**Prose:** Crimson Text **Display:** Spectral **Rationale:** Classic horror aesthetic. Crimson Text
is readable with slightly dark tone. Spectral has sharp, angular serifs that feel unsettling—perfect
for horror chapter titles. **License:** SIL Open Font License **Fallback:** Georgia + Times New
Roman

**Where to get:**

- Crimson Text: [Google Fonts](https://fonts.google.com/specimen/Crimson+Text)
- Spectral: [Google Fonts](https://fonts.google.com/specimen/Spectral)

---

#### Modern Horror

**Prose:** Lora **Display:** Work Sans **Rationale:** Clean, clinical, contemporary feel (think
modern psychological horror or medical horror). Lora is warm serif for readability. Work Sans is
neutral, geometric sans—cold and impersonal for headers. **License:** SIL Open Font License
**Fallback:** Georgia + Arial

**Where to get:**

- Lora: [Google Fonts](https://fonts.google.com/specimen/Lora)
- Work Sans: [Google Fonts](https://fonts.google.com/specimen/Work+Sans)

---

#### Cosmic Horror

**Prose:** Libre Baskerville **Display:** Raleway **Rationale:** Literary, otherworldly feel. Libre
Baskerville is elegant serif (Lovecraftian prose). Raleway is thin, geometric sans that feels alien
and distant—evoking the unknowable. **License:** SIL Open Font License **Fallback:** Georgia +
Helvetica

**Where to get:**

- Libre Baskerville: [Google Fonts](https://fonts.google.com/specimen/Libre+Baskerville)
- Raleway: [Google Fonts](https://fonts.google.com/specimen/Raleway)

---

### Mystery / Detective

#### Classic Mystery (Victorian/Golden Age)

**Prose:** Libre Baskerville **Display:** Playfair Display **Rationale:** Victorian elegance for
Christie/Doyle-style mysteries. Libre Baskerville is highly readable. Playfair Display has high
contrast and dramatic serifs—evokes old book titles and newspaper headlines. **License:** SIL Open
Font License **Fallback:** Georgia + Times New Roman

**Where to get:**

- Libre Baskerville: [Google Fonts](https://fonts.google.com/specimen/Libre+Baskerville)
- Playfair Display: [Google Fonts](https://fonts.google.com/specimen/Playfair+Display)

---

#### Modern Mystery

**Prose:** Source Serif 4 **Display:** Source Sans 3 **Rationale:** Clean, contemporary feel. Source
Serif 4 and Source Sans 3 are designed as complementary pair—perfect harmony. Professional,
readable, no-nonsense. **License:** SIL Open Font License **Fallback:** Georgia + Arial

**Where to get:**

- Source Serif 4: [Google Fonts](https://fonts.google.com/specimen/Source+Serif+4)
- Source Sans 3: [Google Fonts](https://fonts.google.com/specimen/Source+Sans+3)

---

#### Cozy Mystery

**Prose:** Crimson Text **Display:** Montserrat **Rationale:** Warm, approachable feel for
lighthearted mysteries. Crimson Text is friendly serif. Montserrat is geometric sans with
personality—modern but not cold. **License:** SIL Open Font License **Fallback:** Georgia + Verdana

**Where to get:**

- Crimson Text: [Google Fonts](https://fonts.google.com/specimen/Crimson+Text)
- Montserrat: [Google Fonts](https://fonts.google.com/specimen/Montserrat)

---

### Romance

#### Sweet Romance

**Prose:** Lora **Display:** Montserrat **Rationale:** Warm, friendly, approachable. Lora is
readable serif with slight calligraphic feel (romantic). Montserrat is clean sans with rounded
edges—inviting and modern. **License:** SIL Open Font License **Fallback:** Georgia + Arial

**Where to get:**

- Lora: [Google Fonts](https://fonts.google.com/specimen/Lora)
- Montserrat: [Google Fonts](https://fonts.google.com/specimen/Montserrat)

---

#### Steamy Romance

**Prose:** Lato **Display:** Playfair Display **Rationale:** Elegant, sensual. Lato is clean sans
(modern, straightforward). Playfair Display has dramatic high-contrast serifs—evokes passion and
intensity in headers. **License:** SIL Open Font License **Fallback:** Arial + Times New Roman

**Where to get:**

- Lato: [Google Fonts](https://fonts.google.com/specimen/Lato)
- Playfair Display: [Google Fonts](https://fonts.google.com/specimen/Playfair+Display)

---

#### Contemporary Romance

**Prose:** Merriweather **Display:** Inter **Rationale:** Modern, clean, readable. Merriweather is
slightly condensed serif optimized for screens. Inter is neutral, professional sans—contemporary
without being cold. **License:** SIL Open Font License **Fallback:** Georgia + Arial

**Where to get:**

- Merriweather: [Google Fonts](https://fonts.google.com/specimen/Merriweather)
- Inter: [Google Fonts](https://fonts.google.com/specimen/Inter)

---

### Sci-Fi / Cyberpunk

#### Cyberpunk

**Prose:** Inter **Display:** Share Tech Mono **Rationale:** Techy, futuristic, monospace aesthetic.
Inter is clean, modern sans (readable). Share Tech Mono is monospace font with digital/code
feel—perfect for cyberpunk headers and tech interfaces. **License:** SIL Open Font License
**Fallback:** Arial + Courier New

**Where to get:**

- Inter: [Google Fonts](https://fonts.google.com/specimen/Inter)
- Share Tech Mono: [Google Fonts](https://fonts.google.com/specimen/Share+Tech+Mono)

---

#### Space Opera

**Prose:** Source Sans 3 **Display:** Exo 2 **Rationale:** Clean, optimistic, forward-looking.
Source Sans 3 is highly readable sans. Exo 2 has geometric, futuristic feel—evokes starships and
space stations without being hard to read. **License:** SIL Open Font License **Fallback:** Arial +
Verdana

**Where to get:**

- Source Sans 3: [Google Fonts](https://fonts.google.com/specimen/Source+Sans+3)
- Exo 2: [Google Fonts](https://fonts.google.com/specimen/Exo+2)

---

#### Hard Sci-Fi

**Prose:** IBM Plex Serif **Display:** IBM Plex Sans **Rationale:** Technical, precise,
contemporary. IBM Plex Serif and Sans are designed as family—perfect harmony. Clean, corporate,
scientific feel. No-nonsense readability. **License:** SIL Open Font License **Fallback:** Georgia +
Arial

**Where to get:**

- IBM Plex Serif: [Google Fonts](https://fonts.google.com/specimen/IBM+Plex+Serif)
- IBM Plex Sans: [Google Fonts](https://fonts.google.com/specimen/IBM+Plex+Sans)

---

## Universal Fallbacks

If custom fonts are unavailable, these web-safe fonts work across devices:

| Use Case           | Font                 | Notes                                 |
| ------------------ | -------------------- | ------------------------------------- |
| **Readable Serif** | Georgia              | Designed for screens, highly readable |
| **Display Serif**  | Times New Roman      | Classic, universally available        |
| **Readable Sans**  | Arial / Helvetica    | Neutral, clean, highly available      |
| **Display Sans**   | Impact / Arial Black | Bold, high contrast                   |
| **Monospace**      | Courier New          | Code/tech aesthetic                   |

---

## Font Embedding in EPUB

**When to embed:**

- Using custom fonts not available on all devices
- Want consistent visual presentation

**When NOT to embed:**

- File size is a concern (fonts add 100kb-1MB+ per weight)
- Reader preference flexibility is priority
- Using only web-safe fonts

**Best Practice:**

1. Embed fonts with SIL OFL or Apache licenses
2. Include regular + bold + italic weights (minimum)
3. Always specify fallback fonts in CSS
4. Test on multiple EPUB readers (Kindle, Apple Books, Kobo)

**Example CSS:**

```css
@font-face {
  font-family: "Source Serif 4";
  src: url("../fonts/SourceSerif4-Regular.ttf") format("truetype");
  font-weight: normal;
  font-style: normal;
}

body {
  font-family: "Source Serif 4", Georgia, "Times New Roman", serif;
  font-size: 1em;
  line-height: 1.6;
}
```

---

## Accessibility Considerations

### Dyslexia-Friendly Fonts

Recommended fonts for dyslexic readers:

- **OpenDyslexic** (designed specifically for dyslexia)
- **Comic Sans MS** (controversial but effective—wide letterforms, distinct shapes)
- **Arial / Helvetica** (simple, sans-serif)
- **Verdana** (wide spacing, distinct letterforms)

**Best practices:**

- Avoid serif fonts if targeting dyslexic audience
- Larger font sizes (14-16px minimum)
- Increased line height (1.5-2.0)
- Increased letter spacing (0.05-0.1em)

### High Contrast

Ensure sufficient contrast between text and background:

- **WCAG AA:** 4.5:1 contrast ratio for normal text
- **WCAG AAA:** 7:1 contrast ratio for normal text
- Black text on white background = safe default
- Avoid light gray text on white backgrounds

### Font Size and Scaling

- **Minimum body text:** 12-14px
- **Optimal body text:** 14-16px
- **Allow user scaling** in digital formats (EPUB, web)
- Avoid fixed pixel sizes; use em or rem units

---

## Custom Font Pairing Guidelines

If creating custom pairings:

### 1. Contrast is Key

- **Serif + Sans** - Classic combination (e.g., Garamond + Helvetica)
- **Serif + Serif** - Must have different styles (e.g., oldstyle + modern)
- **Sans + Sans** - Must have different weights/widths (e.g., narrow + wide)

### 2. Limit Font Count

- **Maximum 2-3 fonts** per project
- Prose, display, and optional monospace (for code/tech)
- More fonts = harder to maintain hierarchy

### 3. Test Readability

- Print a page and read it at arm's length
- Test on mobile (small screens reveal readability issues)
- Read 500+ words continuously—if eye strain, font may be too decorative

### 4. Check Licensing

- **Commercial use allowed?** (Some free fonts restrict commercial projects)
- **Embedding allowed?** (Some fonts prohibit EPUB embedding)
- **SIL OFL, Apache, or custom license** - Read terms carefully

### 5. Match Genre Tone

- **Fantasy:** Serif, ornate, calligraphic
- **Sci-Fi:** Sans-serif, geometric, futuristic
- **Horror:** Gothic, angular, unsettling
- **Romance:** Elegant, warm, friendly
- **Mystery:** Classic, readable, sophisticated

---

## Font Recommendations by Age (Children's Gamebooks)

### Pre-reader (3-5 years)

**Font Requirements:**

- **Very large size:** 18-24pt minimum
- **Rounded, friendly sans-serif:** Poppins, Baloo, Comic Sans (yes, really—it's effective here)
- **Unambiguous letterforms:** Clear distinction between "a/g", avoid stylized characters
- **Line spacing:** 1.8-2.0 (generous white space)

**Prose:** Baloo 2 or Poppins (rounded, friendly) **Display:** Same font, larger size (simplicity
priority) **Rationale:** Pre-readers need maximum clarity. Illustration-dominant layout with minimal
text.

---

### Early Reader (6-8 years)

**Font Requirements:**

- **Large size:** 16-20pt
- **High readability:** Designed for beginning readers
- **Line spacing:** 1.5-2.0

**Prose:** Sassoon Primary, Atkinson Hyperlegible, or Open Sans **Display:** Same family, bold
weight **Rationale:** Fonts designed specifically for reading education. Atkinson Hyperlegible has
exceptional letter distinction for emerging readers.

**Accessibility Note:** Sassoon Primary was designed for teaching handwriting and is excellent for
dyslexic readers.

---

### Middle Grade (9-12 years)

**Font Requirements:**

- **Standard book size:** 11-13pt
- **Clear navigation:** Section numbers must be bold and easily scannable
- **Line spacing:** 1.4-1.6

**Prose:** Garamond, Times New Roman, Georgia (traditional book fonts) **Display:** Same font, bold
or a complementary sans-serif **Rationale:** Middle grade readers can handle adult book typography.
Focus on clear section numbering for CYOA-style navigation.

**Critical:** Section numbers and choice options must be **bolded and clearly separated** from prose
for easy navigation.

---

### Young Adult (13-17 years)

**Font Requirements:**

- Same as adult (see genre-specific recommendations above)
- May prefer slightly larger base size (12-14pt vs. 11-12pt)

**Prose & Display:** Use adult genre recommendations **Rationale:** YA readers have adult reading
capability. Typography should match genre (detective, fantasy, romance, etc.).

---

### Layout Guidance by Age

| Age       | Font Size (Prose) | Line Height | Paragraph Spacing               | White Space Priority |
| --------- | ----------------- | ----------- | ------------------------------- | -------------------- |
| **3-5**   | 18-24pt           | 1.8-2.0     | Generous (1.5-2x line height)   | Very High            |
| **6-8**   | 16-20pt           | 1.5-2.0     | Generous (1.2-1.5x line height) | High                 |
| **9-12**  | 11-13pt           | 1.4-1.6     | Standard (1x line height)       | Moderate             |
| **13-17** | 11-14pt           | 1.4-1.6     | Standard                        | Standard             |

---

## Resources

**Font Sources:**

- [Google Fonts](https://fonts.google.com/) - Free, open-source fonts with SIL OFL licensing
- [Font Squirrel](https://www.fontsquirrel.com/) - Curated free fonts, 100% free for commercial use
- [Adobe Fonts](https://fonts.adobe.com/) - Subscription-based, high-quality fonts
- [DaFont](https://www.dafont.com/) - Large collection (check licenses carefully)

**Font Pairing Tools:**

- [FontPair](https://fontpair.co/) - Google Fonts pairing suggestions
- [Typewolf](https://www.typewolf.com/) - Font inspiration and pairings
- [Font Combinations](https://www.fontcombinations.com/) - Visual pairing tool

**Typography Education:**

- _The Elements of Typographic Style_ by Robert Bringhurst (classic reference)
- Butterick's Practical Typography ([online book](https://practicaltypography.com/))
- [Typographica](https://typographica.org/) - Font reviews and articles

---

**Last Updated:** 2025-11-05

**Contributing:** Font recommendations can be updated based on user feedback and new font releases.
Submit PRs with rationale and license verification.
