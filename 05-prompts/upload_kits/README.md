# Upload Kits — Quick File Lists And Zip Commands

This folder provides quick copy‑pasta file lists and example commands for creating zip archives of
the Layer 5 prompts you’ll typically upload to a chatbot (ChatGPT, Claude, Gemini).

Platform limits to keep in mind:

- ChatGPT: max 10 files per upload action (you can repeat uploads). Zips can carry more than 10 files.
- Gemini: zips can contain at most 10 files; use two zips (core + optional) for the full set.

## Minimal Upload Kit (10 files — ChatGPT‑friendly)

Files (relative to repo root):

```
05-prompts/_shared/context_management.md
05-prompts/_shared/safety_protocol.md
05-prompts/_shared/escalation_rules.md
05-prompts/_shared/human_interaction.md
05-prompts/showrunner/system_prompt.md
05-prompts/plotwright/system_prompt.md
05-prompts/scene_smith/system_prompt.md
05-prompts/style_lead/system_prompt.md
05-prompts/gatekeeper/system_prompt.md
05-prompts/book_binder/system_prompt.md
05-prompts/player_narrator/system_prompt.md
```

PowerShell (Windows):

```
Compress-Archive -Path @(
  '05-prompts/_shared/context_management.md',
  '05-prompts/_shared/safety_protocol.md',
  '05-prompts/_shared/escalation_rules.md',
  '05-prompts/_shared/human_interaction.md',
  '05-prompts/showrunner/system_prompt.md',
  '05-prompts/plotwright/system_prompt.md',
  '05-prompts/scene_smith/system_prompt.md',
  '05-prompts/style_lead/system_prompt.md',
  '05-prompts/gatekeeper/system_prompt.md',
  '05-prompts/book_binder/system_prompt.md',
  '05-prompts/player_narrator/system_prompt.md'
) -DestinationPath minimal-upload-kit.zip -Force
```

Bash (macOS/Linux):

```
zip -r minimal-upload-kit.zip \
  05-prompts/_shared/context_management.md \
  05-prompts/_shared/safety_protocol.md \
  05-prompts/_shared/escalation_rules.md \
  05-prompts/_shared/human_interaction.md \
  05-prompts/showrunner/system_prompt.md \
  05-prompts/plotwright/system_prompt.md \
  05-prompts/scene_smith/system_prompt.md \
  05-prompts/style_lead/system_prompt.md \
  05-prompts/gatekeeper/system_prompt.md \
  05-prompts/book_binder/system_prompt.md \
  05-prompts/player_narrator/system_prompt.md
```

## Full Upload Kit (split for Gemini)

Add these role prompts as needed:

```
05-prompts/lore_weaver/system_prompt.md
05-prompts/codex_curator/system_prompt.md
05-prompts/researcher/system_prompt.md
05-prompts/art_director/system_prompt.md
05-prompts/illustrator/system_prompt.md
05-prompts/audio_director/system_prompt.md
05-prompts/audio_producer/system_prompt.md
05-prompts/translator/system_prompt.md
```

PowerShell (Windows):

```
Compress-Archive -Path @(
  '05-prompts/_shared/context_management.md',
  '05-prompts/_shared/safety_protocol.md',
  '05-prompts/_shared/escalation_rules.md',
  '05-prompts/_shared/human_interaction.md',
  '05-prompts/showrunner/system_prompt.md',
  '05-prompts/plotwright/system_prompt.md',
  '05-prompts/scene_smith/system_prompt.md',
  '05-prompts/style_lead/system_prompt.md',
  '05-prompts/gatekeeper/system_prompt.md',
  '05-prompts/book_binder/system_prompt.md',
  '05-prompts/player_narrator/system_prompt.md',
  '05-prompts/lore_weaver/system_prompt.md',
  '05-prompts/codex_curator/system_prompt.md',
  '05-prompts/researcher/system_prompt.md',
  '05-prompts/art_director/system_prompt.md',
  '05-prompts/illustrator/system_prompt.md',
  '05-prompts/audio_director/system_prompt.md',
  '05-prompts/audio_producer/system_prompt.md',
  '05-prompts/translator/system_prompt.md'
) -DestinationPath full-upload-kit.zip -Force
```

Bash (macOS/Linux):

```
zip -r full-upload-kit.zip \
  05-prompts/_shared/context_management.md \
  05-prompts/_shared/safety_protocol.md \
  05-prompts/_shared/escalation_rules.md \
  05-prompts/_shared/human_interaction.md \
  05-prompts/showrunner/system_prompt.md \
  05-prompts/plotwright/system_prompt.md \
  05-prompts/scene_smith/system_prompt.md \
  05-prompts/style_lead/system_prompt.md \
  05-prompts/gatekeeper/system_prompt.md \
  05-prompts/book_binder/system_prompt.md \
  05-prompts/player_narrator/system_prompt.md \
  05-prompts/lore_weaver/system_prompt.md \
  05-prompts/codex_curator/system_prompt.md \
  05-prompts/researcher/system_prompt.md \
  05-prompts/art_director/system_prompt.md \
  05-prompts/illustrator/system_prompt.md \
  05-prompts/audio_director/system_prompt.md \
  05-prompts/audio_producer/system_prompt.md \
  05-prompts/translator/system_prompt.md
```

## Build Link Folders And Zips (Recommended)

Generate `dist/upload_kits/*` with flattened, role‑qualified filenames and ready‑made zips:

- Bash (macOS/Linux/WSL): `tools/scripts/build_upload_kits.sh`
- PowerShell (Windows): `tools/scripts/build_upload_kits.ps1`

You’ll get:

- `chatgpt/minimal/` (10 files) and `chatgpt/minimal.zip`
- `chatgpt/addons/` (PN) and `chatgpt/addons.zip`
- `gemini/core_zip/` (10 files) and `gemini/core.zip`
- `gemini/optional_zip/` (≤10 files) and `gemini/optional.zip`

Filenames are flattened (e.g., `showrunner.system_prompt.md`) to avoid collisions when attaching.

## Platform Notes (General)

- Prefer individual files over zips when possible: better grounding and inline citation.
- Keep filenames stable and descriptive — most UIs show them prominently.
- Reattach your kit when starting a fresh thread; some UIs drop context.
- If attachments are capped, load shared patterns + Showrunner first, then add role prompts as needed.
