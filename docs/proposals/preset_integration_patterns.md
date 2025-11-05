# Preset Integration Patterns — How Prompts Use Presets

**Date:** 2025-11-05
**Status:** 🔵 DESIGN REFERENCE
**Related:** genre_aware_defaults.md

---

## Overview

This document shows **exactly how** roles (Layer 2 prompts) access and use preset data (Layer 0 resources).

---

## Integration Pattern: File Reference with SDK Resolution

**Approach:** Prompts reference preset files by path. The SDK/runtime environment provides the data.

This matches QuestFoundry's existing pattern where prompts reference artifacts like `02-dictionary/artifacts/front_matter.md`.

---

## Pattern 1: Showrunner Reading Genre Catalog

### Before (Hardcoded)

```markdown
# Showrunner — System Prompt

Project Initialization Flow

Step 1: Genre & Theme
- Ask user for primary genre/theme (detective-noir, fantasy, sci-fi, etc.)
```

**Problem:** Genre list is hardcoded. Adding new genres requires editing prompt.

---

### After (Preset-Driven)

```markdown
# Showrunner — System Prompt

Project Initialization Flow

Step 1: Genre Selection

1. **Load genre catalog:**
   - Read `/resources/presets/genres.json` to get available genres
   - Extract: `genre_id`, `display_name`, `short_description` for each genre

2. **Present options to user:**
   - List genres with descriptions
   - Example format:
     ```
     1. Detective Noir - Hard-boiled detective stories with atmospheric tension
     2. Fantasy Adventure - Epic quests in magical worlds
     3. Horror / Thriller - Suspenseful stories with lethal branching
     4. Sci-Fi / Cyberpunk - Futuristic settings with technology themes
     5. Romance - Character-focused stories with relationship dynamics
     6. Other / Custom - Flexible preset for any genre
     ```

3. **User selects genre_id**

4. **Load genre preset:**
   - Read `/resources/presets/genres/{genre_id}.json`
   - Extract `project_defaults` section

5. **Apply defaults to initialization:**
   - Use `target_sections_range` for Step 3 (Length)
   - Use `style` defaults for Step 4 (Style & Tone)
   - Use `suggested_sections` to present length options with context
```

---

### How SDK Provides Data

**Layer 6 (SDK) Implementation:**

```python
# In questfoundry-lib SDK
class ShowrunnerRole:
    def __init__(self, preset_manager: PresetManager):
        self.presets = preset_manager

    def run_project_init(self):
        # Step 1: Load genre catalog
        genres = self.presets.list_genres()
        # Returns: [
        #   {"genre_id": "detective-noir", "display_name": "Detective Noir", ...},
        #   {"genre_id": "fantasy-rpg", "display_name": "Fantasy Adventure", ...}
        # ]

        # Present to LLM as context
        system_prompt = load_prompt("showrunner/system_prompt.md")

        # Inject genre data into LLM context
        context = {
            "available_genres": genres,
            "instruction": "Present these genres to user and await selection"
        }

        response = llm.chat(system_prompt, context)

        # User selects "detective-noir"
        selected_genre = "detective-noir"

        # Step 2: Load preset
        preset = self.presets.load_genre(selected_genre)
        # Returns full preset JSON

        # Step 3: Apply defaults
        metadata = self.presets.apply_defaults(
            genre=selected_genre,
            user_overrides={"target_sections": 400}  # User can override
        )

        # Save to project
        save_json("project_metadata.json", metadata)
```

---

## Pattern 2: Style Lead Reading Typography Presets

### Before (Hardcoded)

```markdown
# Style Lead — System Prompt

Typography Specification

- Book Binder will read manifest during export; if missing, defaults apply (Source Serif 4 /
  Cormorant Garamond).
```

**Problem:** Fallback fonts are hardcoded. No genre-specific recommendations.

---

### After (Preset-Driven)

```markdown
# Style Lead — System Prompt

Typography Specification

1. **Load project genre:**
   - Read `project_metadata.json` to get `genre` field
   - Example: `"genre": "detective-noir"`

2. **Load genre typography presets:**
   - Read `/resources/presets/genres/{genre}.json`
   - Extract `typography.recommended_fonts` array

3. **Present font options to user (if multiple presets exist):**
   - List available typography presets for this genre
   - Example for detective-noir:
     ```
     Available typography presets for Detective Noir:

     1. Classic Noir (recommended)
        - Prose: Source Serif 4
        - Display: Cormorant Garamond
        - Style: Traditional serif fonts with elegant headers

     2. Modern Noir
        - Prose: IBM Plex Serif
        - Display: Bebas Neue
        - Style: Contemporary sans-serif with bold impact
     ```

4. **User selects preset (or accepts default):**
   - If user doesn't specify: use `typography.default_preset`
   - If user specifies: use selected preset

5. **Verify font availability:**
   - Check if fonts exist in `/resources/fonts/`
   - If present: use specified fonts
   - If absent: fall back to `global_defaults.json` typography

6. **Create style_manifest.json:**
   - Populate with selected typography preset
   - Set `embed_in_epub` based on font availability
```

---

### How SDK Provides Data

```python
# In questfoundry-lib SDK
class StyleLeadRole:
    def specify_typography(self):
        # Load project metadata
        project_meta = load_json("project_metadata.json")
        genre = project_meta["genre"]  # "detective-noir"

        # Load genre preset
        preset = self.presets.load_genre(genre)

        # Get typography options
        typo_options = preset["typography"]["recommended_fonts"]
        # Returns: [
        #   {"preset_name": "Classic Noir", "prose": {...}, "display": {...}},
        #   {"preset_name": "Modern Noir", "prose": {...}, "display": {...}}
        # ]

        # Present to user (or use default)
        default_preset_name = preset["typography"]["default_preset"]
        selected_preset = typo_options[0]  # "Classic Noir"

        # Check font availability
        fonts_available = check_fonts_exist(
            selected_preset["prose"]["font_family"],
            selected_preset["display"]["font_family"]
        )

        if not fonts_available:
            # Fall back to global defaults
            global_defaults = load_json("/resources/presets/global_defaults.json")
            fallback_fonts = global_defaults["typography"]
            selected_preset = merge_with_fallback(selected_preset, fallback_fonts)

        # Create style manifest
        style_manifest = {
            "typography": {
                "prose": selected_preset["prose"],
                "display": selected_preset["display"],
                "cover": selected_preset["cover"],
                "ui": {...}
            },
            "fonts_required": [...],
            "embed_in_epub": fonts_available
        }

        save_json("style_manifest.json", style_manifest)
```

---

## Pattern 3: Art Director Using Art Style Guidance

### Before (No Guidance)

Art Director currently has no genre-specific guidance in prompt.

---

### After (Preset-Driven)

```markdown
# Art Director — System Prompt

Art Style Guidance

1. **Load project genre:**
   - Read `project_metadata.json` to get `genre` field

2. **Load genre art style preset:**
   - Read `/resources/presets/genres/{genre}.json`
   - Extract `art_style` section containing:
     - `palette_guidance`: Color recommendations
     - `composition_notes`: Spatial/framing guidance
     - `prompt_template_fragments`: Reusable prompt components
     - `reference_artists`: Style references

3. **Incorporate into shotlist creation:**
   - When converting Scene Smith output to shotlist
   - Build image prompts using template fragments
   - Example for detective-noir:
     ```
     Base scene: "Rain-slicked alley with distant figure"

     + palette_guidance: "black and white with amber accents"
     + composition_notes: "Low angle, deep shadows, single light source"
     + prompt_fragments.atmosphere: "rain-soaked, film noir lighting"
     + prompt_fragments.mood: "tense, morally ambiguous, noir"

     Final prompt:
     "Film noir scene: rain-slicked alley with distant figure under
     single streetlight, low angle emphasizing shadows, high contrast
     black and white with amber accents from streetlight, tense and
     morally ambiguous atmosphere, dramatic noir lighting"
     ```

4. **Reference artists for consistency:**
   - Use `reference_artists` list to guide aesthetic
   - Example: "Film noir cinematography (1940s-50s), Edward Hopper, Frank Miller"

5. **Store in shotlist:**
   - Include full prompt in shotlist entry
   - Enables Illustrator to render with consistent genre aesthetic
```

---

### How SDK Provides Data

```python
# In questfoundry-lib SDK
class ArtDirectorRole:
    def create_shotlist(self, scene_description):
        # Load genre preset
        project_meta = load_json("project_metadata.json")
        genre = project_meta["genre"]
        preset = self.presets.load_genre(genre)

        art_style = preset["art_style"]
        # Returns: {
        #   "palette_guidance": "High contrast black and white...",
        #   "composition_notes": "Low angles, deep shadows...",
        #   "prompt_template_fragments": {
        #     "atmosphere": "rain-soaked, film noir lighting...",
        #     "color": "black and white with amber accents",
        #     "mood": "tense, morally ambiguous, noir"
        #   }
        # }

        # Build prompt using fragments
        base_prompt = scene_description  # From Scene Smith

        enhanced_prompt = f"""
        {base_prompt},
        {art_style['prompt_template_fragments']['atmosphere']},
        {art_style['prompt_template_fragments']['color']},
        {art_style['prompt_template_fragments']['mood']},
        {art_style['composition_notes']}
        """

        # Create shotlist entry
        shotlist_entry = {
            "id": "shot_001",
            "scene_anchor": "A2_K",
            "description": scene_description,
            "prompt": enhanced_prompt,
            "palette_notes": art_style["palette_guidance"],
            "references": art_style["reference_artists"]
        }

        return shotlist_entry
```

---

## Pattern 4: Plotwright Using Section Count Guidance

### Before (Arbitrary Numbers)

Plotwright might have hardcoded assumptions about scope.

---

### After (Preset-Driven)

```markdown
# Plotwright — System Prompt

Scope Planning

1. **Load project metadata:**
   - Read `project_metadata.json`
   - Extract: `genre`, `target_sections`, `target_length`, `branching_style`

2. **Load genre preset for context:**
   - Read `/resources/presets/genres/{genre}.json`
   - Extract `suggested_sections[target_length]` for guidance
   - Example for detective-noir + medium:
     ```json
     {
       "sections": [250, 500],
       "words": [30000, 70000],
       "playtime": "~1hr",
       "endings": "5-10+ endings"
     }
     ```

3. **Extract branching patterns:**
   - Check `project_defaults.branching_pattern` (e.g., "branch-and-merge")
   - Check `project_defaults.choices_per_section` (e.g., 3)

4. **Plan topology using preset guidance:**
   - Target section count from `target_sections` (e.g., 350 sections)
   - Branching pattern: branch-and-merge (not exponential)
   - Choices per junction: 3 (ergonomic default)
   - Expected endings: 5-10+ (from preset guidance)

5. **Apply genre-specific structural patterns:**
   - Detective-noir → Hub-and-spoke (investigation structure)
   - Fantasy → Wide branching (exploration)
   - Horror → Lethal branching (many fail states)
   - Romance → Deep variables (relationship states)
```

---

### How SDK Provides Data

```python
# In questfoundry-lib SDK
class PlotwrightRole:
    def plan_topology(self):
        # Load project config
        project_meta = load_json("project_metadata.json")

        # Load genre preset
        genre = project_meta["genre"]
        preset = self.presets.load_genre(genre)

        # Get scope guidance
        target_length = project_meta["target_length"]  # "medium"
        scope = preset["suggested_sections"][target_length]
        # Returns: {
        #   "sections": [250, 500],
        #   "words": [30000, 70000],
        #   "endings": "5-10+ endings"
        # }

        # Get structural guidance
        branching_pattern = project_meta.get(
            "branching_pattern",
            preset["project_defaults"]["branching_pattern"]  # "branch-and-merge"
        )

        choices_per_section = project_meta.get(
            "choices_per_section",
            preset["project_defaults"]["choices_per_section"]  # 3
        )

        # Plan topology
        topology_plan = {
            "target_sections": project_meta["target_sections"],  # e.g., 350
            "section_range": scope["sections"],  # [250, 500]
            "word_budget": scope["words"],  # [30000, 70000]
            "avg_words_per_section": 125,  # from preset or global default
            "branching_pattern": branching_pattern,
            "choices_per_node": choices_per_section,
            "target_endings": scope["endings"],
            "structural_notes": preset.get("structural_pattern_notes", "")
        }

        return topology_plan
```

---

## Fallback Hierarchy in Action

**Example: User selects detective-noir but fonts not available**

```python
# User init flow
user_selections = {
    "genre": "detective-noir",
    "target_sections": 400  # User override
}

# SDK applies presets
preset = presets.load_genre("detective-noir")

# Step 1: Start with preset defaults
project_config = preset["project_defaults"].copy()
# {
#   "target_sections_range": [250, 500],
#   "avg_words_per_section": 125,
#   "style": {"tone": "gritty", ...}
# }

# Step 2: Apply user overrides
project_config["target_sections"] = user_selections["target_sections"]  # 400

# Step 3: Validate against preset range
if not (250 <= 400 <= 500):
    warn("Target sections outside recommended range for detective-noir")

# Typography with fallback
typo_preset = preset["typography"]["recommended_fonts"][0]  # "Classic Noir"
fonts_needed = ["Source Serif 4", "Cormorant Garamond"]

if not fonts_available(fonts_needed):
    # Fallback to global defaults
    global_defaults = load_json("/resources/presets/global_defaults.json")
    typo_preset = {
        "prose": {"font_family": global_defaults["typography"]["default_prose_font"]},  # "Georgia"
        "display": {"font_family": global_defaults["typography"]["default_display_font"]}  # "Georgia"
    }
    warn("Preset fonts not available, using fallback: Georgia")

# Final config merges user overrides + preset defaults + global fallbacks
final_config = {
    "genre": "detective-noir",
    "target_sections": 400,  # USER OVERRIDE
    "target_word_count": 50000,  # Calculated: 400 * 125
    "avg_words_per_section": 125,  # FROM PRESET
    "style": {"tone": "gritty", ...},  # FROM PRESET
    "typography": typo_preset  # FROM GLOBAL FALLBACK (fonts missing)
}
```

---

## Summary: Integration Points

| Layer | Component | How Presets Are Used |
|-------|-----------|---------------------|
| **Layer 0** | `/resources/presets/*.json` | Source of truth for genre defaults |
| **Layer 2** | Prompt system_prompt.md | References preset files by path (e.g., "Read /resources/presets/genres.json") |
| **Layer 6** | SDK (questfoundry-lib) | Reads JSON files, provides data to LLM as context, applies fallback hierarchy |
| **Layer 7** | CLI (qf commands) | Lists genres (`qf genres list`), passes user selections to SDK |

---

## Key Principles

1. **Prompts don't parse JSON directly**
   - Prompts say "Load /resources/presets/genres.json"
   - SDK intercepts and provides the data
   - LLM receives structured data as context

2. **Fallback hierarchy is enforced by SDK**
   - User override → Genre preset → Global default → Schema default
   - SDK handles validation and merging

3. **Presets are read-only for prompts**
   - Roles use preset data to make decisions
   - They don't modify presets (only create artifacts like project_metadata.json)

4. **Discoverability through Layer 7**
   - CLI: `qf genres list` shows available options
   - CLI: `qf genres show detective-noir` shows preset details
   - User learns what's possible

---

**END OF INTEGRATION PATTERNS**
