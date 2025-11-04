# Upload Kits — Quick File Lists And Zip Commands

This folder provides quick copy‑pasta file lists and example commands for creating zip archives of
the Layer 5 prompts you’ll typically upload to a chatbot (ChatGPT, Claude, Gemini).

## Minimal Upload Kit

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

## Full Upload Kit

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

## Platform Notes (General)

- Prefer individual files over zips when possible: better grounding and inline citation.
- Keep filenames stable and descriptive — most UIs show them prominently.
- Reattach your kit when starting a fresh thread; some UIs drop context.
- If attachments are capped, load shared patterns + Showrunner first, then add role prompts as needed.
