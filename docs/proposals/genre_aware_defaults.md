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

**Issues:**
1. Hardcoded values make it hard to adapt to different genres
2. No discoverability - users don't know what options exist
3. No genre-specific recommendations (noir vs. fantasy have different conventions)
4. Defaults scattered across prompts, schemas, examples

---

## Proposed Solution

**Create a genre-aware presets system** with:
1. **Centralized preset definitions** in `/resources/presets/`
2. **Genre-specific recommendations** (not hardcodes)
3. **Fallback hierarchy**: user override → genre preset → global default
4. **Discoverability**: CLI/UI can list available presets

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
    "target_sections_range": [25, 35],
    "branching_style": "moderate",
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
    "short": { "min": 10, "max": 15, "playtime": "~30min" },
    "medium": { "min": 25, "max": 35, "playtime": "~1hr" },
    "long": { "min": 45, "max": 65, "playtime": "~2hr" },
    "epic": { "min": 80, "max": 120, "playtime": "3hr+" }
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
    "short": { "sections": 15, "playtime": "~30min" },
    "medium": { "sections": 30, "playtime": "~1hr" },
    "long": { "sections": 60, "playtime": "~2hr" },
    "epic": { "sections": 100, "playtime": "3hr+" }
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

## Implementation Plan

### Phase 1: Core Structure (P1 High)

1. Create `/resources/presets/` directory
2. Define preset JSON schemas
3. Create `global_defaults.json`
4. Create `genres.json` catalog
5. Create 3 initial genre presets:
   - `detective-noir.json` (most complete)
   - `generic.json` (minimal fallback)
   - `fantasy-adventure.json` (example alternative)

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

1. Add remaining genre presets (horror, sci-fi, romance, etc.)
2. Add typography preset alternatives per genre
3. Community contribution guidelines for new presets

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
    "target_sections_range": [25, 35],
    "branching_style": "moderate",
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

## Open Questions

1. **Preset versioning:** Should genre presets have versions? (e.g., "detective-noir-v2.json")

2. **User custom presets:** Should users be able to save their own presets in project directories?

3. **Preset inheritance:** Should presets support inheritance? (e.g., "cyberpunk-noir" extends "detective-noir")

4. **Preset validation:** Should there be a `qf validate-preset` command?

5. **Preset marketplace:** Future: community-contributed presets repository?

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
