# Proposal: Genre-Aware Defaults & Presets System

**Date:** 2025-11-05
**Status:** 🔵 PROPOSAL (awaiting approval)
**Related:** project_metadata.md, style_manifest.md, art_manifest.md

---

## Problem Statement

Current implementation has hardcoded values in various places:
- Font choices: Source Serif 4 + Cormorant Garamond (in prompts and examples)
- Genre options: Listed inline in Showrunner init flow
- Style presets: No recommendations for writing_style, tone, paragraph_density
- Length defaults: No guidance on "typical" section counts per genre
- No alignment with industry-standard gamebook/CYOA metrics

**Issues:**
1. Hardcoded values make it hard to adapt to different genres
2. No discoverability - users don't know what options exist
3. No genre-specific recommendations (noir vs. fantasy have different conventions)
4. Defaults scattered across prompts, schemas, examples
5. Length categories don't reflect published gamebook standards (50-1000+ sections)

---

## Proposed Solution

**Create a genre-aware presets system** with:
1. **Centralized preset definitions** in `/resources/presets/`
2. **Genre-specific recommendations** (not hardcodes)
3. **Fallback hierarchy**: user override → genre preset → global default
4. **Discoverability**: CLI/UI can list available presets

---

## Gamebook Design Metrics (Industry Standards)

This proposal incorporates established metrics from published gamebook (CYOA) design. These metrics provide realistic defaults for scope, pacing, and structure.

### Length Categories by Scope

Based on analysis of published print and digital gamebooks:

| Category | Section Count | Total Word Count | Branching Complexity |
|----------|--------------|------------------|---------------------|
| **Short** | 50 - 150 | 10,000 - 30,000 | **Low.** Simple paths with 2-4 distinct endings. Choices frequently merge back to central trunk. Ideal for tutorials or focused stories. |
| **Medium** | 250 - 500 | 30,000 - 70,000 | **Moderate.** Standard for full-length title. Supports 5-10+ endings and several distinct sub-plots. Good replayability. |
| **Long** | 500 - 1,000 | 70,000 - 150,000 | **High.** Complex digital titles. Can support 15-20+ endings. Major choices lead to significantly different mid-games. |
| **Epic** | 1,000+ | 150,000 - 500,000+ | **Very High / Sandboxy.** Dozens of endings or persistent states. Paths deeply divergent; often impossible to see all content in few playthroughs. |

### Content Pacing Defaults

Default pacing targets **Medium scope** (scalable up/down):

| Unit | Default Value | Rationale |
|------|--------------|-----------|
| **Standard Section** | ~125 words | Core "beat" of the game. Long enough to set scene and present problem, short enough to maintain momentum. (e.g., 50,000 words / 400 sections) |
| **Standard Paragraph** | ~50 words | Readability default. 125-word section = 2-3 visual chunks to avoid "wall of text." |
| **"Fail" Section** | < 50 words | Clear "Game Over" or "Bad Ending." Purpose is finality, not exposition. |
| **"Hub" Section** | < 100 words | Recurring location (e.g., town square). Short and functional for re-orientation. |
| **Choices per Section** | 3 | Ergonomic standard. 2 is binary; 4+ causes decision fatigue. |

### Default Structural Logic: "Branch and Merge"

Pure exponential branching is logistically unwritable. Default model:

1. **Branch:** Choice leads to divergent path (A, B, C)
2. **Diverge:** Path continues for several unique sections (3-5 sections per path)
3. **Set Consequence:** Variable records choice (e.g., `ally_status = "angered"`)
4. **Merge:** All paths link back to common major plot-point section
5. **Check:** Later, logic checks variable (`IF ally_status = "angered"`) for long-term consequence

This creates the *feel* of fully branched story while keeping scope manageable.

### Genre-Based Metric Variations

Genre expectations directly influence all metrics:

| Genre | Impact on Length & Branching | Primary Focus |
|-------|----------------------------|---------------|
| **Fantasy / RPG** | Long to Epic. High section count (exploration) and high word count (lore). "Wide" branching (hub-and-spoke). | **World-building & Systems.** Supports stat-tracking, combat, inventory, explorable world. |
| **Romance** | Long to Epic (word count). "Deep" branching (many variables) but not structurally divergent. Same core plot, choices modify relationships. | **Character & State-Tracking.** High word count for nuanced dialogue. 300k-word romance may have fewer sections than 70k-word fantasy. |
| **Horror / Thriller** | Short to Medium. "Lethal" branching—few golden paths to survival, many short fail-state branches. Sections often < 125 words. | **Pacing & Tension.** Short sections = rapid page-turning. Game is puzzle: find survival path. |
| **Mystery** | Medium. "Hub-and-spoke" branching. Gather clues (detailed sections), return to central point to decide next lead. | **Information Gathering.** Structure is "web" not "tree." Replayability from exploring different leads. |

---

## Architecture

### Directory Structure

```
/resources/presets/
  README.md                       # Overview of preset system
  genres.json                     # Genre catalog with metadata
  global_defaults.json            # Universal fallbacks

  genres/
    detective-noir.json           # Detective noir preset
    fantasy-adventure.json        # Fantasy adventure preset
    sci-fi-thriller.json          # Sci-fi thriller preset
    horror-survival.json          # Horror survival preset
    historical-drama.json         # Historical drama preset
    romance.json                  # Romance preset
    generic.json                  # Generic/other preset (minimal assumptions)
```

---

## Schema: Genre Preset

Each genre preset file contains:

```json
{
  "genre_id": "detective-noir",
  "display_name": "Detective Noir",
  "description": "Hard-boiled detective stories with moral ambiguity, urban settings, and atmospheric tension.",
  "tags": ["mystery", "crime", "urban", "atmospheric"],

  "project_defaults": {
    "target_length": "medium",
    "target_sections_range": [250, 500],
    "target_word_count_range": [30000, 70000],
    "avg_words_per_section": 125,
    "branching_style": "moderate",
    "branching_pattern": "branch-and-merge",
    "choices_per_section": 3,
    "style": {
      "writing_style": "pulp",
      "paragraph_density": "rich",
      "tone": "gritty",
      "pov": "second-person"
    }
  },

  "typography": {
    "recommended_fonts": [
      {
        "preset_name": "Classic Noir",
        "prose": {
          "font_family": "Source Serif 4",
          "fallback": "Georgia, Times New Roman, serif"
        },
        "display": {
          "font_family": "Cormorant Garamond",
          "fallback": "Georgia, serif"
        }
      },
      {
        "preset_name": "Modern Noir",
        "prose": {
          "font_family": "IBM Plex Serif",
          "fallback": "Georgia, serif"
        },
        "display": {
          "font_family": "Bebas Neue",
          "fallback": "Impact, sans-serif"
        }
      }
    ],
    "default_preset": "Classic Noir"
  },

  "art_style": {
    "palette_guidance": "High contrast black and white with selective color (amber, red)",
    "composition_notes": "Low angles, deep shadows, rain/fog atmospheric effects",
    "reference_artists": ["Film noir cinematography", "Edward Hopper", "Sin City graphic novels"],
    "prompt_template_fragments": {
      "atmosphere": "rain-soaked, high contrast, dramatic shadows, film noir lighting",
      "color": "black and white with amber accents",
      "mood": "tense, atmospheric, morally ambiguous"
    }
  },

  "suggested_sections": {
    "short": {
      "sections": [50, 150],
      "words": [10000, 30000],
      "playtime": "~30min",
      "endings": "2-4 distinct endings"
    },
    "medium": {
      "sections": [250, 500],
      "words": [30000, 70000],
      "playtime": "~1hr",
      "endings": "5-10+ endings"
    },
    "long": {
      "sections": [500, 1000],
      "words": [70000, 150000],
      "playtime": "~2hr",
      "endings": "15-20+ endings"
    },
    "epic": {
      "sections": [1000, 2000],
      "words": [150000, 500000],
      "playtime": "3hr+",
      "endings": "Dozens of endings"
    }
  },

  "common_themes": [
    "Investigation and deduction",
    "Moral ambiguity",
    "Urban decay",
    "Corruption and betrayal",
    "Lone protagonist vs. system"
  ]
}
```

---

## Schema: Global Defaults

`global_defaults.json` provides universal fallbacks when no genre is selected:

```json
{
  "version": "1.0.0",
  "last_updated": "2025-11-05",

  "project": {
    "default_genre": null,
    "default_license": "CC BY-NC 4.0",
    "default_language": "en",
    "default_target_length": "medium",
    "default_branching_style": "moderate",
    "default_style": {
      "writing_style": "literary",
      "paragraph_density": "moderate",
      "tone": "neutral",
      "pov": "second-person"
    }
  },

  "typography": {
    "default_prose_font": "Georgia",
    "default_display_font": "Georgia",
    "default_fallback": "Times New Roman, serif",
    "embed_in_epub": false
  },

  "lengths": {
    "short": {
      "sections": [50, 150],
      "words": [10000, 30000],
      "playtime": "~30min",
      "branching_complexity": "low"
    },
    "medium": {
      "sections": [250, 500],
      "words": [30000, 70000],
      "playtime": "~1hr",
      "branching_complexity": "moderate"
    },
    "long": {
      "sections": [500, 1000],
      "words": [70000, 150000],
      "playtime": "~2hr",
      "branching_complexity": "high"
    },
    "epic": {
      "sections": [1000, 2000],
      "words": [150000, 500000],
      "playtime": "3hr+",
      "branching_complexity": "very-high"
    }
  },

  "pacing": {
    "standard_section_words": 125,
    "standard_paragraph_words": 50,
    "fail_section_max_words": 50,
    "hub_section_max_words": 100,
    "choices_per_section": 3
  }
}
```

---

## Schema: Genre Catalog

`genres.json` provides discoverability:

```json
{
  "version": "1.0.0",
  "genres": [
    {
      "genre_id": "detective-noir",
      "display_name": "Detective Noir",
      "short_description": "Hard-boiled detective stories with atmospheric tension",
      "preset_file": "genres/detective-noir.json",
      "popularity": "common",
      "complexity": "medium"
    },
    {
      "genre_id": "fantasy-adventure",
      "display_name": "Fantasy Adventure",
      "short_description": "Epic quests in magical worlds",
      "preset_file": "genres/fantasy-adventure.json",
      "popularity": "common",
      "complexity": "high"
    },
    {
      "genre_id": "sci-fi-thriller",
      "display_name": "Sci-Fi Thriller",
      "short_description": "Futuristic suspense with technology themes",
      "preset_file": "genres/sci-fi-thriller.json",
      "popularity": "common",
      "complexity": "medium"
    },
    {
      "genre_id": "generic",
      "display_name": "Other / Custom",
      "short_description": "Flexible preset for any genre",
      "preset_file": "genres/generic.json",
      "popularity": "fallback",
      "complexity": "low"
    }
  ]
}
```

---

## Fallback Hierarchy

**For any configurable value:**

```
1. User explicit override (highest priority)
   ↓
2. Genre preset recommendation
   ↓
3. Global default
   ↓
4. Schema default (lowest priority)
```

**Example: Paragraph Density**

```
User selects genre "detective-noir" but doesn't specify paragraph_density:

1. User override? No
2. Genre preset? Yes → "rich" (detective-noir.json)
3. Use "rich" ✓
```

**Example: Font Choice**

```
User selects genre "fantasy-adventure" but fonts not available:

1. User override? No
2. Genre preset? Yes → "Cinzel + Crimson Pro" (fantasy-adventure.json)
3. Check availability? No (not in /resources/fonts/)
4. Fallback to global default → "Georgia"
5. Use "Georgia" ✓
```

---

## Integration Points

### Layer 2: Prompts

**Showrunner** (`05-prompts/showrunner/system_prompt.md`):

```markdown
### Project Initialization Flow

**Step 1: Genre Selection**

1. Read `/resources/presets/genres.json` to get available genres
2. Present list to user with descriptions
3. User selects genre_id
4. Load genre preset from `genres/{genre_id}.json`
5. Apply preset defaults to project_metadata

**Step 3: Length Selection**

1. Use genre preset's `suggested_sections` ranges
2. Present options: short (X-Y sections), medium (X-Y), etc.
3. Allow custom override
```

**Style Lead** (`05-prompts/style_lead/system_prompt.md`):

```markdown
### Typography Specification

**Default Selection:**

1. Read genre preset from project_metadata.genre
2. Load `genres/{genre_id}.json`
3. Check `typography.recommended_fonts` array
4. Present options to user (if multiple presets)
5. Verify font availability in `/resources/fonts/`
6. Fall back to global defaults if unavailable
7. Create style_manifest.json
```

**Art Director** (`05-prompts/art_director/system_prompt.md`):

```markdown
### Style Guidance

**Genre-Aware Prompts:**

1. Load genre preset art_style section
2. Incorporate `palette_guidance` into shotlist prompts
3. Use `prompt_template_fragments` to build consistent aesthetic
4. Reference `composition_notes` for spatial guidance
```

---

## Layer 6: Library Integration

**Python SDK usage:**

```python
from questfoundry.presets import PresetManager

# Initialize
pm = PresetManager()

# List available genres
genres = pm.list_genres()
# → [{"genre_id": "detective-noir", "display_name": "Detective Noir", ...}]

# Load genre preset
preset = pm.load_genre("detective-noir")

# Get recommended typography
typography = preset.get_typography_preset("Classic Noir")
# → {"prose": {"font_family": "Source Serif 4", ...}, ...}

# Apply defaults to project metadata
metadata = pm.apply_defaults(
    genre="detective-noir",
    user_overrides={"target_sections": 40}
)
# → Merges genre defaults with user overrides
```

---

## Layer 7: CLI Integration

**CLI commands:**

```bash
# List available genres with descriptions
qf genres list

# Show preset details for a genre
qf genres show detective-noir

# Initialize project with genre preset
qf init --genre detective-noir

# Initialize interactively (suggests based on genre)
qf init --interactive

# Override specific defaults
qf init --genre fantasy-adventure --length long --style pulp
```

---

## Benefits

### 1. **No Hardcodes**
- All defaults live in JSON files
- Can be updated without code changes
- Community can contribute genre presets

### 2. **Genre-Aware**
- Noir gets "gritty" tone, fantasy gets "epic"
- Typography matches genre conventions
- Art direction aligned with genre expectations

### 3. **Discoverable**
- CLI can list options: `qf genres list`
- Presets show examples of what's possible
- Users learn genre conventions

### 4. **Flexible**
- User overrides always win
- Can mix-and-match (noir story with fantasy fonts)
- Easy to add new genres

### 5. **Maintainable**
- Centralized in `/resources/presets/`
- Clear separation: presets vs. schemas vs. prompts
- Versioned (can track preset evolution)

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

Each genre preset includes: length recommendations, branching patterns, typography suggestions, art style guidance, pacing defaults, and common themes.

---

## Implementation Plan

### Phase 1: Core Structure (P1 High)

1. Create `/resources/presets/` directory
2. Define preset JSON schemas (validate with CI)
3. Create `global_defaults.json` with gamebook metrics
4. Create `genres.json` catalog
5. Create **Tier 1 genre presets** (5 presets):
   - `fantasy-rpg.json` - Most popular gamebook genre
   - `horror-thriller.json` - Classic gamebook format
   - `mystery-detective.json` - Investigation-focused (most detailed example)
   - `sci-fi-cyberpunk.json` - Futuristic settings
   - `romance.json` - Character & relationship-focused
   - `generic.json` - Minimal fallback

### Phase 2: Prompt Integration (P1 High)

1. Update Showrunner to read genres.json
2. Update Style Lead to use typography presets
3. Update Art Director to incorporate art_style guidance
4. Remove hardcoded values from prompts

### Phase 3: Validation (P2 Medium)

1. Add preset schema validation to CI
2. Validate all presets in `/resources/presets/` on commit
3. Test fallback hierarchy with missing presets

### Phase 4: Expansion (P3 Low)

1. Add **Tier 2 genre presets** (5 presets): historical, adventure, western, superhero, post-apocalyptic
2. Add **Tier 3 genre presets** (4 presets): comedy, slice-of-life, war, sports
3. Add typography preset alternatives per genre (2-3 options each)
4. Community contribution guidelines for new presets

---

## Example: Detective Noir Preset

**Full example** (for reference):

```json
{
  "genre_id": "detective-noir",
  "display_name": "Detective Noir",
  "description": "Hard-boiled detective stories with moral ambiguity, atmospheric urban settings, and tension-driven pacing. Think Chandler, Hammett, and film noir classics.",
  "tags": ["mystery", "crime", "urban", "atmospheric", "investigation"],

  "project_defaults": {
    "target_length": "medium",
    "target_sections_range": [250, 500],
    "target_word_count_range": [30000, 70000],
    "avg_words_per_section": 125,
    "branching_style": "moderate",
    "branching_pattern": "branch-and-merge",
    "choices_per_section": 3,
    "style": {
      "writing_style": "pulp",
      "paragraph_density": "rich",
      "tone": "gritty",
      "pov": "second-person"
    }
  },

  "typography": {
    "recommended_fonts": [
      {
        "preset_name": "Classic Noir",
        "description": "Traditional serif fonts with elegant display headers",
        "prose": {
          "font_family": "Source Serif 4",
          "fallback": "Georgia, Times New Roman, serif",
          "font_size": "1em",
          "line_height": "1.6"
        },
        "display": {
          "font_family": "Cormorant Garamond",
          "fallback": "Georgia, serif",
          "h1_size": "2.5em",
          "h2_size": "2em"
        },
        "cover": {
          "title_font": "Cormorant Garamond Bold",
          "author_font": "Source Serif 4 Italic"
        }
      }
    ],
    "default_preset": "Classic Noir"
  },

  "art_style": {
    "palette_guidance": "High contrast black and white with selective color (amber for streetlights, red for danger)",
    "composition_notes": "Low angles emphasizing looming threats, deep shadows with single light sources, rain/fog for atmosphere",
    "reference_artists": [
      "Film noir cinematography (1940s-50s)",
      "Edward Hopper (urban isolation)",
      "Frank Miller (Sin City high-contrast style)"
    ],
    "prompt_template_fragments": {
      "atmosphere": "rain-soaked streets, high contrast lighting, dramatic shadows, film noir aesthetic",
      "color": "black and white with amber accents from streetlights",
      "mood": "tense, morally ambiguous, atmospheric, noir"
    }
  },

  "suggested_sections": {
    "short": { "min": 10, "max": 15, "playtime": "~30min", "description": "Single case or incident" },
    "medium": { "min": 25, "max": 35, "playtime": "~1hr", "description": "Full investigation with twists" },
    "long": { "min": 45, "max": 65, "playtime": "~2hr", "description": "Complex case with subplots" },
    "epic": { "min": 80, "max": 120, "playtime": "3hr+", "description": "Multi-case saga or conspiracy" }
  },

  "common_themes": [
    "Investigation and deduction",
    "Moral ambiguity and ethical dilemmas",
    "Urban decay and social critique",
    "Corruption in institutions",
    "Lone protagonist vs. system",
    "Femme fatale archetypes",
    "Past haunting present"
  ],

  "typical_locations": [
    "Rain-soaked city streets",
    "Smoky bars and nightclubs",
    "Shabby detective offices",
    "Docks and warehouses",
    "Penthouses and mansions",
    "Police precincts",
    "Dark alleys"
  ],

  "tone_guidance": {
    "narrative_voice": "Cynical, world-weary, observant",
    "pacing": "Deliberate with bursts of action",
    "dialogue": "Snappy, sardonic, revealing subtext",
    "atmosphere": "Oppressive, tense, morally gray"
  }
}
```

---

## Design Decisions (Resolved)

1. **Preset versioning:** ✅ No versioning by default. Only create alternative versions (e.g., "detective-noir-v2") if we want to maintain multiple variants.

2. **User custom presets:** ✅ Yes in Layer 6/7 (SDK/CLI). Not default behavior - plenty of opportunity to customize during init flow.

3. **Preset inheritance:** ✅ Yes, sounds good for extending presets (e.g., "cyberpunk-noir" extends "detective-noir"). Implementation deferred - may not be convenient for Layers 0-5.

4. **Genre selection:** ✅ Take popular genres from gamebook/CYOA space (fantasy, horror, mystery, romance, sci-fi, etc.)

5. **Preset validation:** Should there be a `qf validate-preset` command? (To be determined)

6. **Preset marketplace:** Future: community-contributed presets repository? (To be determined)

---

## Backwards Compatibility

**Existing projects:**
- No breaking changes - schemas still accept all fields
- Existing examples remain valid (they were using implicit "detective-noir" preset)
- Prompts still work if presets missing (fall back to global defaults)

**Migration:**
- No migration needed
- New projects get preset system automatically
- Old projects continue working as-is

---

## Success Metrics

1. **No hardcoded values** in prompts or examples
2. **Discoverability:** Users can `qf genres list` to explore options
3. **Consistency:** All detective-noir projects start with similar defaults
4. **Flexibility:** Users can override any default easily
5. **Extensibility:** Adding new genres is just adding a JSON file

---

**END OF PROPOSAL**
