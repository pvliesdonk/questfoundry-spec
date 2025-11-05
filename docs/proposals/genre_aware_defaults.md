# Proposal: Design Guidelines for Genre-Aware Defaults

**Date:** 2025-11-05 **Status:** ✅ APPROVED (documentation-based approach) **Related:**
project_metadata.md, style_manifest.md, art_manifest.md

---

## Problem Statement

Current implementation has hardcoded values scattered across prompts:

- Font choices: Source Serif 4 + Cormorant Garamond (in prompts and examples)
- Genre options: Listed inline in Showrunner init flow
- Style presets: No recommendations for writing_style, tone, paragraph_density
- Length defaults: Arbitrary numbers not aligned with published gamebooks (e.g., "medium 20-30
  sections")
- No reference to industry-standard gamebook/CYOA metrics

**Issues:**

1. Hardcoded values make prompts brittle and hard to maintain
2. No centralized guidance - recommendations inconsistent across prompts
3. No genre-specific best practices (noir vs. fantasy have different conventions)
4. Length categories don't reflect actual published gamebook standards (50-1000+ sections)
5. Users (humans writing Layer 1 charters) have no reference for sensible defaults

---

## Proposed Solution

**Create design guidelines documentation** providing reference information for humans, not
programmatic constraints:

1. **Markdown reference docs** in `/docs/design_guidelines/`
2. **Best practices** for genre conventions, typography, art direction, pacing
3. **Industry-standard gamebook metrics** (published gamebook analysis)
4. **Informational, not enforced** - schemas remain maximally flexible
5. **LLMs embed knowledge** - Layer 2 prompts include guidance as context

---

## Gamebook Design Metrics (Industry Standards)

This proposal incorporates established metrics from published gamebook (CYOA) design. These metrics
provide realistic defaults for scope, pacing, and structure.

### Length Categories by Scope

Based on analysis of published print and digital gamebooks:

| Category   | Section Count | Total Word Count   | Branching Complexity                                                                                                                               |
| ---------- | ------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Short**  | 50 - 150      | 10,000 - 30,000    | **Low.** Simple paths with 2-4 distinct endings. Choices frequently merge back to central trunk. Ideal for tutorials or focused stories.           |
| **Medium** | 250 - 500     | 30,000 - 70,000    | **Moderate.** Standard for full-length title. Supports 5-10+ endings and several distinct sub-plots. Good replayability.                           |
| **Long**   | 500 - 1,000   | 70,000 - 150,000   | **High.** Complex digital titles. Can support 15-20+ endings. Major choices lead to significantly different mid-games.                             |
| **Epic**   | 1,000+        | 150,000 - 500,000+ | **Very High / Sandboxy.** Dozens of endings or persistent states. Paths deeply divergent; often impossible to see all content in few playthroughs. |

### Content Pacing Defaults

Default pacing targets **Medium scope** (scalable up/down):

| Unit                    | Default Value | Rationale                                                                                                                                     |
| ----------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Standard Section**    | ~125 words    | Core "beat" of the game. Long enough to set scene and present problem, short enough to maintain momentum. (e.g., 50,000 words / 400 sections) |
| **Standard Paragraph**  | ~50 words     | Readability default. 125-word section = 2-3 visual chunks to avoid "wall of text."                                                            |
| **"Fail" Section**      | < 50 words    | Clear "Game Over" or "Bad Ending." Purpose is finality, not exposition.                                                                       |
| **"Hub" Section**       | < 100 words   | Recurring location (e.g., town square). Short and functional for re-orientation.                                                              |
| **Choices per Section** | 3             | Ergonomic standard. 2 is binary; 4+ causes decision fatigue.                                                                                  |

### Default Structural Logic: "Branch and Merge"

Pure exponential branching is logistically unwritable. Default model:

1. **Branch:** Choice leads to divergent path (A, B, C)
2. **Diverge:** Path continues for several unique sections (3-5 sections per path)
3. **Set Consequence:** Variable records choice (e.g., `ally_status = "angered"`)
4. **Merge:** All paths link back to common major plot-point section
5. **Check:** Later, logic checks variable (`IF ally_status = "angered"`) for long-term consequence

This creates the _feel_ of fully branched story while keeping scope manageable.

### Genre-Based Metric Variations

Genre expectations directly influence all metrics:

| Genre                 | Impact on Length & Branching                                                                                                               | Primary Focus                                                                                                                          |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Fantasy / RPG**     | Long to Epic. High section count (exploration) and high word count (lore). "Wide" branching (hub-and-spoke).                               | **World-building & Systems.** Supports stat-tracking, combat, inventory, explorable world.                                             |
| **Romance**           | Long to Epic (word count). "Deep" branching (many variables) but not structurally divergent. Same core plot, choices modify relationships. | **Character & State-Tracking.** High word count for nuanced dialogue. 300k-word romance may have fewer sections than 70k-word fantasy. |
| **Horror / Thriller** | Short to Medium. "Lethal" branching—few golden paths to survival, many short fail-state branches. Sections often < 125 words.              | **Pacing & Tension.** Short sections = rapid page-turning. Game is puzzle: find survival path.                                         |
| **Mystery**           | Medium. "Hub-and-spoke" branching. Gather clues (detailed sections), return to central point to decide next lead.                          | **Information Gathering.** Structure is "web" not "tree." Replayability from exploring different leads.                                |

---

## Architecture

### Documentation Structure

**NOT Layer 0/1** (Technical Specifications):

- ❌ No `/resources/presets/*.json` files
- ❌ No schema constraints for "recommended values"
- ❌ No programmatic enforcement of defaults

**YES - Documentation Layer** (`/docs/design_guidelines/`):

- ✅ Reference material for humans writing Layer 1 charters
- ✅ Best practices for genre conventions
- ✅ Industry standards for gamebook design
- ✅ LLMs at Layer 2 can embed this knowledge in prompts

```
/docs/design_guidelines/
  README.md                        # Overview of design guidelines
  gamebook_design_metrics.md       # Industry standards (length, pacing, structure)
  genre_conventions.md             # Genre-specific best practices (15+ genres)
  typography_recommendations.md    # Font pairing guidance by genre
  art_style_references.md          # Visual aesthetic guidance by genre
```

### What This Means

**For Schemas (Layer 0):**

- Accept any valid values within type constraints
- No "recommended range" validation
- Maximum flexibility - examples: `target_sections: 5-500`, `genre: any string 3-80 chars`

**For Prompts (Layer 2):**

- Embed guidance directly in prompt text as context for LLMs
- Reference design guidelines in comments: `(see docs/design_guidelines/gamebook_design_metrics.md)`
- Present recommendations to users during interactive workflows
- Users can override any suggestion freely

**For Humans (Layer 1 Charter Writers):**

- Read design guidelines to understand best practices
- Use as reference when writing custom prompts
- Contribute improvements to guidelines via PRs

---

## Reference Content: Genre Best Practices

Instead of JSON preset files, design guidelines contain prose descriptions with examples.

### Example from `genre_conventions.md`:

```markdown
## Detective Noir

**Description:** Hard-boiled detective stories with moral ambiguity, atmospheric urban settings, and
tension-driven pacing. Think Chandler, Hammett, and film noir classics.

**Tags:** mystery, crime, urban, atmospheric, investigation

### Typical Project Characteristics

**Scope & Pacing:**

- Target length: Medium (250-500 sections, 30k-70k words, ~1hr playtime)
- Branching style: Moderate (branch-and-merge pattern)
- Choices per section: 3 (standard ergonomic default)
- Section length: ~125 words (2-3 paragraphs)

**Writing Style:**

- Style: Pulp (terse, vivid, action-oriented prose)
- Paragraph density: Rich (atmospheric description balanced with pacing)
- Tone: Gritty (cynical, world-weary, morally complex)
- POV: Second-person (immersive "you are the detective")

**Common Themes:**

- Investigation and deduction
- Moral ambiguity and ethical dilemmas
- Urban decay and social critique
- Corruption in institutions
- Lone protagonist vs. system
- Femme fatale archetypes
- Past haunting present

**Typical Locations:**

- Rain-soaked city streets
- Smoky bars and nightclubs
- Shabby detective offices
- Docks and warehouses
- Penthouses and mansions
- Police precincts
- Dark alleys
```

### Example from `typography_recommendations.md`:

```markdown
## Detective Noir Typography

**Classic Noir Pairing:**

- Prose: Source Serif 4 (traditional, readable serif)
- Display: Cormorant Garamond (elegant headers with dramatic contrast)
- Rationale: Evokes 1940s-50s pulp fiction aesthetic

**Modern Noir Pairing:**

- Prose: IBM Plex Serif (clean, contemporary serif)
- Display: Bebas Neue (bold, impact-driven sans-serif)
- Rationale: Urban, industrial feel for contemporary noir settings

**Fallback:** Georgia (universally available, appropriate tone)
```

### Example from `art_style_references.md`:

```markdown
## Detective Noir Visual Aesthetic

**Color Palette:**

- High contrast black and white
- Selective color: amber (streetlights), red (danger, blood, neon signs)

**Composition:**

- Low camera angles emphasizing looming threats
- Deep shadows with single dramatic light sources (venetian blinds, street lamps)
- Rain and fog for atmosphere
- Dutch angles for disorientation

**Reference Artists:**

- Film noir cinematography (1940s-50s classics)
- Edward Hopper (urban isolation, dramatic lighting)
- Frank Miller's Sin City (high-contrast graphic style)

**Prompt Template Fragments:**

- Atmosphere: "rain-soaked streets, high contrast lighting, dramatic shadows, film noir aesthetic"
- Color: "black and white with amber accents from streetlights"
- Mood: "tense, morally ambiguous, atmospheric, noir"
```

---

## Integration: How Prompts Use Guidelines

**Key Principle:** Prompts embed knowledge from design guidelines as context for LLMs, rather than
loading external data files.

### Layer 2: Showrunner Example

**Current (hardcoded):**

```markdown
Step 3: Scope & Length

Suggest target section count:

- Short: 10-15 sections (~30min)
- Medium: 20-30 sections (~1hr)
- Long: 40-60 sections (~2hr)
```

**With Embedded Guidance (from `gamebook_design_metrics.md`):**

```markdown
Step 3: Scope & Length

Guide user using industry-standard gamebook metrics (see
docs/design_guidelines/gamebook_design_metrics.md):

- Short (50-150 sections, ~30min): Quick stories with 2-4 endings
- Medium (250-500 sections, ~1hr): Full-length with 5-10+ endings
- Long (500-1000 sections, ~2hr): Complex with 15-20+ endings
- Epic (1000+ sections, 3hr+): Dozens of endings, highly divergent paths

For detective-noir, medium scope (250-500 sections) is typical in published gamebooks. However, user
may choose any scope—schemas accept 5-500 sections.
```

### Layer 2: Style Lead Example

**Current (hardcoded):**

```markdown
Typography Specification

Default fonts:

- Prose: Source Serif 4
- Display: Cormorant Garamond
```

**With Embedded Guidance (from `typography_recommendations.md`):**

```markdown
Typography Specification

Recommend typography based on genre conventions (see
docs/design_guidelines/typography_recommendations.md):

Detective Noir:

- Classic Noir: Source Serif 4 + Cormorant Garamond (traditional pulp aesthetic)
- Modern Noir: IBM Plex Serif + Bebas Neue (contemporary urban feel)

Fantasy:

- Epic Fantasy: Cinzel + Crimson Pro (medieval, ornate)
- High Fantasy: EB Garamond + Alegreya (classic, readable)

Fallback: Georgia (universally available)

Ask user which pairing they prefer, or accept custom fonts.
```

### Layer 2: Art Director Example

**With Embedded Guidance (from `art_style_references.md`):**

```markdown
Visual Style Guidance

For detective-noir (see docs/design_guidelines/art_style_references.md):

Color Palette:

- High contrast black and white with amber accents (streetlights) and red (danger)

Composition:

- Low angles, deep shadows, single dramatic light sources
- Rain/fog atmospheric effects
- Reference: Film noir cinematography, Edward Hopper, Sin City

When generating shotlist prompts, incorporate these fragments:

- Atmosphere: "rain-soaked streets, high contrast lighting, dramatic shadows, film noir aesthetic"
- Mood: "tense, morally ambiguous, atmospheric, noir"
```

### No SDK/CLI Changes Needed

**Layer 6 (SDK):** No new preset loading logic required. Existing project metadata handling
continues as-is.

**Layer 7 (CLI):** No new commands needed. Existing `qf init` workflow continues, prompts now have
better guidance embedded.

---

## Benefits

### 1. **Cleaner Architecture**

- No programmatic preset system to maintain
- No SDK loading logic required
- No validation of "recommended ranges"
- Schemas remain maximally flexible

### 2. **Better Human Guidance**

- Centralized reference documentation in `/docs/design_guidelines/`
- Easy to read, understand, and contribute to (markdown > JSON)
- Prose explanations with rationale, not just data structures
- Charts writers can reference when building custom prompts

### 3. **LLM Context Integration**

- Prompts embed guidance directly as context
- LLMs have genre-aware knowledge at decision-making time
- No external file reads during runtime
- Consistent recommendations across all prompts

### 4. **Genre-Aware Recommendations**

- Noir gets "gritty" tone, fantasy gets "epic"
- Typography matches genre conventions
- Art direction aligned with genre expectations
- Based on published gamebook industry standards

### 5. **Maximum Flexibility**

- User can override any suggestion
- No enforcement or validation against "recommended values"
- Can mix-and-match (noir story with fantasy fonts, etc.)
- Schemas accept full range of valid values

### 6. **Easy Maintenance**

- Update guidance by editing markdown files
- Clear prose > editing JSON structures
- Community can contribute via PRs
- Version control tracks evolution of best practices

---

## Popular Genres to Include

Based on gamebook/CYOA market analysis, include these popular genres in initial implementation:

### Tier 1: Core Genres (Must Have)

1. **Fantasy / RPG** - Most popular gamebook genre. High section count, stat systems, exploration.
2. **Horror / Thriller** - Classic gamebook format. Lethal branching, tension-focused pacing.
3. **Mystery / Detective** - Investigation-focused. Hub-and-spoke structure, clue gathering.
4. **Sci-Fi / Cyberpunk** - Futuristic settings. Technology themes, moral dilemmas.
5. **Romance** - Growing market. Character-focused, relationship variables, dialogue-heavy.

### Tier 2: Secondary Genres (Should Have)

6. **Historical Fiction** - Period settings. Research-grounded, educational potential.
7. **Adventure / Action** - Straightforward branching. Focus on exciting set pieces.
8. **Western** - Classic genre with established tropes. Moral choices, frontier justice.
9. **Superhero** - Powers & consequences. Moral dilemmas, secret identity mechanics.
10. **Post-Apocalyptic / Survival** - Resource management. Harsh choices, group dynamics.

### Tier 3: Specialized Genres (Nice to Have)

11. **Comedy / Satire** - Tone-driven. Absurdist branches, meta-commentary.
12. **Slice of Life / Contemporary** - Everyday choices. Relationship-focused, low stakes.
13. **War / Military** - Strategic choices. Squad dynamics, mission planning.
14. **Sports** - Competition-focused. Training montages, rivalry paths.

### Generic Fallback

15. **Generic / Other** - Minimal assumptions. Flexible baseline for non-standard genres.

Each genre preset includes: length recommendations, branching patterns, typography suggestions, art
style guidance, pacing defaults, and common themes.

---

## Implementation Plan

### Phase 1: Create Design Guidelines Documentation (P1 High)

1. Create `/docs/design_guidelines/` directory structure
2. Create `README.md` - Overview of design guidelines and how to use them
3. Create `gamebook_design_metrics.md` - Industry standards reference:
   - Length categories (Short: 50-150, Medium: 250-500, Long: 500-1000, Epic: 1000+)
   - Content pacing defaults (125 words/section, 3 choices, branch-and-merge)
   - Structural patterns explanation
4. Create `genre_conventions.md` - **Tier 1 genres** (5+ detailed entries):
   - Detective Noir (investigation, hub-and-spoke, medium scope)
   - Fantasy/RPG (exploration, long/epic, stat systems)
   - Horror/Thriller (tension, short/medium, lethal branching)
   - Mystery (clue gathering, medium, web structure)
   - Romance (relationships, long, deep variables)
   - Sci-Fi (technology themes, medium/long)
5. Create `typography_recommendations.md` - Font pairing guidance:
   - 2-3 pairings per Tier 1 genre
   - Rationale for each pairing
   - Fallback recommendations
6. Create `art_style_references.md` - Visual aesthetic guidance:
   - Color palettes by genre
   - Composition notes
   - Reference artists
   - Prompt template fragments

### Phase 2: Update Prompts with Embedded Guidance (P1 High)

1. Update `showrunner/system_prompt.md`:
   - Replace hardcoded length ranges with gamebook metrics
   - Add genre selection guidance with Tier 1 genres
   - Reference design guidelines in comments
2. Update `style_lead/system_prompt.md`:
   - Replace hardcoded font defaults with typography recommendations
   - Show genre-specific pairings
   - Add fallback logic
3. Update `art_director/system_prompt.md`:
   - Add genre-aware visual style guidance
   - Include palette and composition notes
   - Show prompt template fragments
4. Review other prompts for hardcoded values and update as needed

### Phase 3: Expansion (P2 Medium)

1. Add **Tier 2 genre entries** to `genre_conventions.md` (5+ genres):
   - Historical Fiction, Adventure, Western, Superhero, Post-Apocalyptic
2. Add typography recommendations for Tier 2 genres
3. Add art style references for Tier 2 genres

### Phase 4: Community Contribution (P3 Low)

1. Add contribution guidelines to design guidelines README
2. Document how to propose new genre entries
3. Create templates for genre convention entries

---

## Example: Detective Noir Entry in `genre_conventions.md`

**Full example** showing how this would be documented:

```markdown
## Detective Noir

**Display Name:** Detective Noir

**Description:** Hard-boiled detective stories with moral ambiguity, atmospheric urban settings, and
tension-driven pacing. Think Chandler, Hammett, and film noir classics.

**Tags:** mystery, crime, urban, atmospheric, investigation

---

### Typical Project Characteristics

**Scope & Pacing:**

- **Target Length:** Medium (250-500 sections)
- **Word Count:** 30,000-70,000 words
- **Playtime:** ~1 hour
- **Section Length:** ~125 words (2-3 paragraphs)
- **Branching Style:** Moderate
- **Branching Pattern:** Branch-and-merge (choices diverge for 3-5 sections, then merge at plot
  points)
- **Choices per Section:** 3 (ergonomic standard)

**Writing Style:**

- **Style:** Pulp (terse, vivid, action-oriented prose)
- **Paragraph Density:** Rich (atmospheric description balanced with pacing)
- **Tone:** Gritty (cynical, world-weary, morally complex)
- **POV:** Second-person ("You light a cigarette and watch the rain...")
- **Narrative Voice:** Cynical, world-weary, observant
- **Dialogue:** Snappy, sardonic, revealing subtext

---

### Scope Variations

| Scope      | Sections | Words    | Playtime | Description                                  |
| ---------- | -------- | -------- | -------- | -------------------------------------------- |
| **Short**  | 50-150   | 10k-30k  | ~30min   | Single case or incident                      |
| **Medium** | 250-500  | 30k-70k  | ~1hr     | Full investigation with twists (most common) |
| **Long**   | 500-1000 | 70k-150k | ~2hr     | Complex case with subplots                   |
| **Epic**   | 1000+    | 150k+    | 3hr+     | Multi-case saga or conspiracy                |

---

### Common Themes

- Investigation and deduction
- Moral ambiguity and ethical dilemmas
- Urban decay and social critique
- Corruption in institutions
- Lone protagonist vs. system
- Femme fatale archetypes
- Past haunting present

### Typical Locations

- Rain-soaked city streets
- Smoky bars and nightclubs
- Shabby detective offices
- Docks and warehouses
- Penthouses and mansions
- Police precincts
- Dark alleys

---

### Typography (see typography_recommendations.md)

**Classic Noir Pairing:**

- Prose: Source Serif 4
- Display: Cormorant Garamond
- Rationale: Evokes 1940s-50s pulp fiction aesthetic

**Modern Noir Pairing:**

- Prose: IBM Plex Serif
- Display: Bebas Neue
- Rationale: Contemporary urban, industrial feel

---

### Visual Aesthetic (see art_style_references.md)

**Color Palette:**

- High contrast black and white
- Selective color: amber (streetlights), red (danger, blood)

**Composition:**

- Low angles emphasizing looming threats
- Deep shadows with single dramatic light sources
- Rain and fog for atmosphere

**Reference Artists:**

- Film noir cinematography (1940s-50s)
- Edward Hopper (urban isolation)
- Frank Miller's Sin City (high-contrast style)

**Prompt Fragments:**

- Atmosphere: "rain-soaked streets, high contrast lighting, dramatic shadows, film noir aesthetic"
- Color: "black and white with amber accents from streetlights"
- Mood: "tense, morally ambiguous, atmospheric, noir"
```

---

## Design Decisions (Resolved)

1. **Documentation location:** ✅ `/docs/design_guidelines/` (markdown), NOT `/resources/presets/`
   (JSON)

2. **Enforcement:** ✅ No enforcement. Schemas remain maximally flexible. Guidelines are
   informational.

3. **Prompt integration:** ✅ Embed guidance directly in prompt text as context for LLMs, no file
   loading.

4. **Genre selection:** ✅ Take popular genres from gamebook/CYOA space (fantasy, horror, mystery,
   romance, sci-fi, etc.)

5. **Extensibility:** ✅ Community can contribute genre entries via PRs to markdown docs

6. **Versioning:** ✅ No genre versioning needed - just update markdown docs with improved guidance

---

## Backwards Compatibility

**Existing projects:**

- No breaking changes - schemas unchanged
- Existing examples remain valid
- No migration needed

**Existing prompts:**

- Continue to work as-is
- Can be updated incrementally with improved guidance
- Old hardcoded values can be replaced with embedded guidance over time

**No new dependencies:**

- No SDK changes required
- No CLI changes required
- No runtime file loading added

---

## Success Metrics

1. **No hardcoded values** in prompts - replaced with embedded guidance from design guidelines
2. **Centralized documentation** in `/docs/design_guidelines/` that humans can reference
3. **Genre-aware recommendations** based on published gamebook industry standards
4. **Flexibility** - users can override any suggestion, schemas accept full valid range
5. **Maintainability** - updating guidance = editing markdown files (easy to review, contribute,
   version control)
6. **Cleaner architecture** - no preset loading system, no enforcement, no validation of
   "recommended ranges"

---

**END OF PROPOSAL**
