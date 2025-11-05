# Design Guidelines

**Purpose:** Reference documentation for humans writing QuestFoundry charters and prompts.

These guidelines are **informational, not programmatic constraints**. They provide best practices based on published gamebook/CYOA industry standards to help create sensible defaults without hardcoding values.

---

## What Are Design Guidelines?

Design guidelines are markdown documentation containing:

- **Industry standards** for gamebook design (length, pacing, structure)
- **Genre conventions** for popular gamebook genres
- **Typography recommendations** for font pairings by genre
- **Visual aesthetic guidance** for art direction by genre

**They are NOT:**
- ❌ JSON preset files loaded at runtime
- ❌ Schema validation rules
- ❌ Enforced constraints on user choices
- ❌ Required values that must be used

**They ARE:**
- ✅ Reference material for humans writing Layer 1 charters
- ✅ Best practices embedded in Layer 2 prompts as LLM context
- ✅ Genre-specific recommendations (not requirements)
- ✅ Informational guidance that users can freely override

---

## How to Use Design Guidelines

### For Charter Writers (Layer 1)

When writing custom prompts or modifying system prompts:

1. **Read relevant guidelines** to understand best practices
2. **Reference conventions** for the genres you're targeting
3. **Embed guidance** directly in your prompt text as context
4. **Allow user overrides** - recommendations are not requirements

**Example:**
```markdown
When guiding users on project length, reference docs/design_guidelines/gamebook_design_metrics.md:
- Medium scope: 250-500 sections (~1hr playtime, 5-10+ endings)
However, user may choose any valid scope (5-500 sections per schema).
```

### For Prompt Engineers (Layer 2)

Prompts should embed guidance from design guidelines:

- **Reference guidelines in comments:** `(see docs/design_guidelines/genre_conventions.md)`
- **Present recommendations to users** during interactive workflows
- **Explain rationale** for suggestions (e.g., "Medium scope is typical for detective-noir")
- **Always allow overrides** - schemas remain maximally flexible

### For Contributors

Improvements to design guidelines are welcome via PRs:

1. **Update prose documentation** (not JSON files)
2. **Add genre entries** with research/citations
3. **Improve recommendations** based on user feedback
4. **Fix inconsistencies** across guidelines

See "Contributing to Design Guidelines" section below.

---

## Guidelines Structure

```
/docs/design_guidelines/
  README.md                        # This file - overview and usage
  gamebook_design_metrics.md       # Industry standards for length, pacing, structure
  genre_conventions.md             # 15+ popular genres with detailed best practices
  typography_recommendations.md    # Font pairings by genre with rationale
  art_style_references.md          # Visual aesthetic guidance by genre
```

---

## Key Documents

### 1. Gamebook Design Metrics

**File:** `gamebook_design_metrics.md`

**Contains:**
- Length categories (Short, Medium, Long, Epic) with section counts
- Industry-standard word counts and playtimes
- Content pacing defaults (words per section, choices per section)
- Structural patterns (branch-and-merge vs. exponential branching)
- Genre-based metric variations

**Use this when:**
- Guiding users on project scope
- Setting expectations for playtime
- Designing branching structures

### 2. Genre Conventions

**File:** `genre_conventions.md`

**Contains:**
- 15+ popular gamebook genres (detective-noir, fantasy, horror, romance, sci-fi, etc.)
- Typical project characteristics per genre (scope, pacing, style)
- Common themes and locations
- Writing style recommendations (tone, POV, dialogue)
- Cross-references to typography and art style

**Use this when:**
- Helping users select appropriate genres
- Providing genre-specific recommendations
- Understanding typical conventions for a genre

### 3. Typography Recommendations

**File:** `typography_recommendations.md`

**Contains:**
- 2-3 font pairings per genre with rationale
- Prose + display font combinations
- Fallback recommendations
- License information (SIL OFL, Google Fonts, etc.)
- Examples of what aesthetic each pairing creates

**Use this when:**
- Guiding Style Lead on font selection
- Creating style_manifest artifacts
- Explaining font pairing choices to users

### 4. Art Style References

**File:** `art_style_references.md`

**Contains:**
- Color palettes by genre
- Composition notes (angles, lighting, atmosphere)
- Reference artists and visual styles
- Prompt template fragments for consistency
- Mood and tone guidance

**Use this when:**
- Guiding Art Director on visual style
- Creating shotlist prompts
- Building art_manifest artifacts
- Maintaining consistent visual aesthetic

---

## Contributing to Design Guidelines

### Proposing New Genre Entries

To add a new genre to `genre_conventions.md`:

1. **Research the genre** in published gamebooks/CYOA
2. **Identify typical characteristics** (length, branching, themes)
3. **Draft genre entry** using the Detective Noir example as template
4. **Include citations** if referencing specific published works
5. **Submit PR** with clear rationale

**Required sections for genre entries:**
- Description and tags
- Typical project characteristics (scope, pacing, style)
- Scope variations (short/medium/long/epic)
- Common themes and locations
- Cross-references to typography and art style

### Updating Existing Guidelines

To improve existing documentation:

1. **Identify issue** (outdated info, missing details, inconsistency)
2. **Research improvement** (user feedback, industry changes, published works)
3. **Update markdown** with clear explanation
4. **Submit PR** with rationale

**Examples of good updates:**
- Adding new font pairing option with rationale
- Updating word count ranges based on recent published gamebooks
- Clarifying structural pattern explanations
- Adding visual examples or diagrams

### Review Process

Design guideline PRs are reviewed for:

- **Accuracy:** Are recommendations based on research/industry standards?
- **Clarity:** Is the prose clear and easy to understand?
- **Completeness:** Are all required sections included?
- **Consistency:** Does it match the style/format of other entries?
- **Flexibility:** Does it present recommendations without enforcing constraints?

---

## Relationship to Architecture Layers

### Layer 0: Schemas (Technical Specifications)

- **NO connection** - schemas remain maximally flexible
- Schemas accept any valid value within type constraints
- No validation against "recommended ranges"
- Example: `target_sections` accepts 5-500, not just the "recommended" 250-500

### Layer 1: Charters (Human-Written Prompts)

- **Reference material** - charter writers read guidelines when creating prompts
- Guidelines inform what sensible defaults should be
- Charter writers embed guidance directly in prompt text

### Layer 2: Prompts (LLM System Prompts)

- **Embedded context** - prompts include guidance from guidelines
- LLMs use this knowledge to make recommendations
- Users presented with informed suggestions during workflows

### Layer 3: Tools & Validation

- **NO validation** against design guidelines
- Tools validate against schemas only (flexible type constraints)
- No enforcement of "recommended values"

### Layers 6/7: SDK & CLI

- **NO programmatic loading** of design guidelines
- No preset manager, no runtime file reads
- Existing project metadata handling continues as-is

---

## Frequently Asked Questions

**Q: Why markdown instead of JSON?**

A: Markdown is more human-readable, easier to review/contribute to, better for prose explanations with rationale, and doesn't require parsing logic.

**Q: How do prompts access this information?**

A: Prompts embed guidance directly as text (context for LLMs), rather than loading external files at runtime.

**Q: Can users override recommendations?**

A: Yes, absolutely. Guidelines are informational, not constraints. Schemas accept full range of valid values.

**Q: Should I validate user input against guidelines?**

A: No. Only validate against schema constraints (type, min/max). Don't enforce "recommended ranges."

**Q: How do I know which genre a user selected?**

A: Check `project_metadata.genre` field. It's a free-form string, so treat it as informational rather than an enum.

**Q: What if a user chooses a genre not in the guidelines?**

A: That's fine. Use generic fallback recommendations, or ask user for details to provide custom guidance.

**Q: Can Layer 6/7 (SDK/CLI) add user custom presets?**

A: Potentially in the future, but it's not part of this proposal. The focus here is on providing baseline guidance, not building a preset system.

---

## Maintenance

Design guidelines should be updated:

- **Quarterly:** Review for accuracy based on user feedback
- **As needed:** Add new genres, improve clarity, fix inconsistencies
- **Community-driven:** Accept PRs from contributors

Guidelines are living documents and should evolve with:
- New published gamebook releases
- User feedback and usage patterns
- Industry trends and conventions
- Community contributions

---

**Last Updated:** 2025-11-05

**Status:** ✅ Active - these guidelines are approved and ready to use
