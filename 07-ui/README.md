# Layer 7 — UI (User Interfaces)

**Status:** 🚧 Planning Phase
**Last Updated:** 2025-10-31

## Overview

Layer 7 provides user interfaces for authors and players. The initial implementation focuses on a CLI tool that wraps Layer 6 library functionality.

## Purpose

- Provide author tools for running loops, managing TUs, generating artifacts
- Enable manual loop execution and individual role invocation
- Support quickstart workflow with checkpoints
- Generate and export views for players
- Offer interactive mode for conversational collaboration with AI agents

## Repository

**Primary Implementation:** `pvliesdonk/questfoundry-cli` (Python CLI)

This directory (`07-ui/`) in the spec repo contains:

- UX design documentation
- Command specifications
- Future UI concepts (TUI, GUI, WebUI, MCP server)

The actual implementation lives in the separate CLI repository.

## CLI Architecture

### Command Structure

**Verb-Noun Pattern (Git-style):**

```bash
# Project Management
qf init [path]                   # Create new .qfproj
qf open <project.qfproj>         # Load existing project
qf status                        # Show active roles, pending work
qf history                       # Show TU timeline

# Quickstart Workflow
qf quickstart                    # Orchestrated workflow (guided mode)
qf quickstart --interactive      # With chatbot collaboration
qf quickstart --express          # Fully autonomous (future)

# Manual Loop Execution
qf run <loop-name>               # Run specific loop
qf run hook-harvest
qf run lore-deepening --interactive
qf run art-touchup
qf run audio-pass

# Individual Asset Generation
qf generate image <shotlist-id>  # Generate image from shotlist
qf generate image SHOTLIST-001 --provider dalle
qf generate audio <cuelist-id>   # Generate audio from cuelist
qf generate scene <tu-id>        # Generate scene prose
qf generate canon <hook-id>      # Canonize hook

# Artifact Inspection
qf list hooks|tus|canon|views    # List artifacts
qf show <artifact-id>            # Show artifact details
qf show HOOK-001
qf show TU-2025-10-31-SR01

# Quality & Validation
qf check                         # Run gatechecks
qf check --bars integrity,style  # Specific quality bars
qf validate <artifact-id>        # Validate single artifact

# Export & Rendering
qf export view                   # Export player view
qf export view --snapshot latest
qf export git                    # Export git-friendly snapshot
qf bind view <snapshot-id>       # Run Book Binder

# Configuration
qf config set provider.text openai
qf config list
qf provider list                 # List available providers

# Aliases
qf qs        → qf quickstart
qf ls        → qf list
```

### Repository Structure

```
questfoundry-cli/
  src/qf/
    __main__.py                  # Entry point
    cli.py                       # CLI framework setup

    commands/
      init.py                    # Project creation
      quickstart.py              # Orchestrated workflow
      run.py                     # Loop execution
      generate.py                # Asset generation
      list.py                    # Artifact listing
      show.py                    # Artifact inspection
      check.py                   # Gatecheck execution
      export.py                  # View export
      config.py                  # Configuration

    interactive/
      session.py                 # Interactive mode handler
      prompts.py                 # CLI prompts/questions
      renderer.py                # Rich text rendering

    completions/
      bash.sh                    # Bash completion script
      zsh.sh                     # Zsh completion script
      fish.fish                  # Fish completion script

    formatting/
      tables.py                  # Table formatters
      artifacts.py               # Artifact renderers
      progress.py                # Progress indicators

  tests/
    test_commands/
    test_interactive/
    fixtures/

  pyproject.toml
  README.md
```

## Interaction Modes

### Guided Mode (Default, MVP)

**Loop-by-Loop Checkpoints:**

```bash
$ qf quickstart

Welcome to QuestFoundry!

Setting up your project...

? What's your story premise?
> A detective investigates mysterious disappearances in a coastal town

? What tone?
> Mystery with supernatural elements

? Target length?
> Short (2-3 hours gameplay)

Creating project: coastal-mystery.qfproj

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Starting Hook Harvest loop...

✓ Showrunner created TU-2025-10-31-SR01
✓ Lore Weaver analyzing premise...
✓ Hook generation complete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Loop Summary: Hook Harvest
  Duration: 2m 34s
  TU: TU-2025-10-31-SR01
  Artifacts:
    ✓ 5 hooks created
    ✓ All hooks marked 'proposed'

Hooks:
  HOOK-001: The lighthouse keeper's final log entry
  HOOK-002: Strange tidal patterns during disappearances
  HOOK-003: Local folklore about "the Calling"
  HOOK-004: Missing persons all visited the old pier
  HOOK-005: Witness reports of singing from the ocean

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Review hooks? [y/N]: y

[Shows detailed hook cards]

Continue to Lore Deepening? [Y/n]: Y

Starting Lore Deepening loop...
```

**Key Features:**

- Simple Y/N prompts at checkpoints
- Automatic summary of what just happened
- Optional detailed review before continuing
- Clear indication of which loop is next

### Interactive Mode

**Conversational Collaboration:**

```bash
$ qf quickstart --interactive

Welcome to QuestFoundry Interactive Mode!

In this mode, AI agents can ask you questions as they work.
You can respond naturally and guide the creative process.

Starting Hook Harvest loop...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Lore Weaver]: I'm analyzing your premise. I see potential for
both cosmic horror and psychological thriller elements.

Question: Should the supernatural elements be:
  a) Ambiguous (possibly explained naturally)
  b) Clearly supernatural
  c) Something else?

Your answer: Let's keep it ambiguous until midgame, then reveal
cosmic horror elements gradually

[Lore Weaver]: Perfect! That gives us great narrative tension.
I'll seed hooks that work both ways...

[Lore Weaver]: For HOOK-003 about local folklore, I'm torn
between two approaches:

Question: Should "the Calling" be:
  - An old sailor's superstition (builds misdirection)
  - A recent phenomenon (increases urgency)

Your answer: recent phenomenon

[Lore Weaver]: Got it. Creating hooks now...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Hook Harvest complete (5 hooks created)

Continue? [Y/n]:
```

**Agent Questions Implementation:**

- Agents use `ask_human()` API (Layer 6)
- Creates `human.question` intent (Layer 4)
- CLI displays question with context
- Human responds free-form
- Response sent as `human.response` intent
- Agent continues with answer

### Express Mode (Future)

**Fully Autonomous:**

```bash
$ qf quickstart --express

Express Mode: Fully autonomous execution

? Story premise: [...]
? Tone: [...]
? Length: [...]

Running full production...

This may take 15-30 minutes. You can safely close this window.
Progress will be saved and you can check status with: qf status

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ Progress bar with current loop ]

Completed:
  ✓ Hook Harvest (2m 34s)
  ✓ Lore Deepening (4m 12s)
  ✓ Story Spark (3m 45s)

Currently Running:
  ⟳ Scene Writing (TU-2025-10-31-SS01)

Pending:
  ⏸ Gatecheck
  ⏸ Codex Expansion
  ⏸ Binding Run
```

## Manual Operations

### Running Individual Loops

```bash
$ qf run hook-harvest

Hook Harvest Loop
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

? Work from existing premise? [Y/n]: Y

Loading premise from TU-2025-10-30-SR01...

✓ Lore Weaver analyzing...
✓ 3 new hooks generated

Hooks:
  HOOK-006: The harbormaster's encrypted journal
  HOOK-007: Unusual marine biology specimens
  HOOK-008: Connection to 1920s incidents

Complete.
```

### Generating Individual Assets

```bash
$ qf generate image SHOTLIST-003

Generating image from SHOTLIST-003...

Shotlist: "The abandoned lighthouse, sunset, broken windows"
Provider: dalle (dall-e-3)
Style: painterly, atmospheric

⟳ Generating... (this may take 30-60 seconds)

✓ Image generated
✓ Saved to: .questfoundry/assets/IMG-003.png
✓ Linked to SHOTLIST-003

Review? [Y/n]: Y

[Displays image in terminal if supported, or opens in default viewer]
```

**Provider Override:**

```bash
$ qf generate image SHOTLIST-003 --provider a1111 --model sd-xl
$ qf generate audio CUELIST-001 --provider elevenlabs --voice rachel
```

### Artifact Inspection

```bash
$ qf list hooks

Hooks (8 total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID         Status      Stakes  Title
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOOK-001   canonized   5       The lighthouse keeper's log
HOOK-002   canonized   4       Strange tidal patterns
HOOK-003   in-progress 4       Local folklore
HOOK-004   proposed    3       Missing persons pattern
...

$ qf show HOOK-001

Hook Card: HOOK-001
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Title:    The lighthouse keeper's final log entry
Status:   canonized
Stakes:   5 (out of 5)
Created:  2025-10-31 by Lore Weaver
TU:       TU-2025-10-31-LW01

Description:
  The last entry in keeper Samuel Morrison's log is dated
  the night before his disappearance. It describes "the song
  from the deep" and mentions coordinates.

Implications:
  - Provides concrete lead (coordinates)
  - Establishes pattern (disappearances + song)
  - Creates urgency (recent incident)

Gateway Conditions:
  - Player must visit lighthouse
  - Player must find log (hidden)

Linked Canon:
  → CANON-001: Samuel Morrison backstory
  → CANON-005: The Calling origins

Player-Safe: Yes (marked for Codex)
```

### Quality Checks

```bash
$ qf check

Running Gatekeeper validation...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Quality Bar Results:

✓ Integrity        All references resolve
✓ Reachability     All critical beats reachable
✗ Style            3 inconsistencies found
✓ Gateways         All conditions clear
✓ Nonlinearity     Hub structure valid
✓ Determinism      Asset reproducibility OK
✓ Presentation     Player surfaces clean
✓ Spoiler Hygiene  No leaks detected

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ GATECHECK FAILED

Issues:
  Style Bar:
    - TU-2025-10-31-SS03: Tone shift in scene 7
    - TU-2025-10-31-SS05: Register mismatch
    - CODEX-004: Inconsistent term usage

Review issues with: qf show <artifact-id>
Request style review: qf run style-tuneup
```

## UI Toolkit

**CLI Framework:** [Typer](https://typer.tiangolo.com/) or [Click](https://click.palletsprojects.com/)

- Type-safe commands
- Automatic help generation
- Built-in completion support

**Rich Text:** [Rich](https://rich.readthedocs.io/)

- Tables, progress bars
- Syntax highlighting
- Markdown rendering
- Tree views

**Prompts:** [Questionary](https://github.com/tmbo/questionary) or [InquirerPy](https://inquirerpy.readthedocs.io/)

- Interactive prompts
- Multi-select, autocomplete
- Validation

**Shell Completion:**

- Bash, Zsh, Fish support
- Dynamic completion (artifact IDs, loop names)
- Install via: `qf --install-completion`

## Configuration

**Config File:** `.questfoundry/config.yml`

```yaml
# Default provider
providers:
  text:
    default: openai
    openai:
      api_key: ${OPENAI_API_KEY}
      model: gpt-4o

  image:
    default: dalle

# CLI preferences
ui:
  color: true
  progress_bars: true
  auto_open_images: true
  editor: ${EDITOR}

# Quickstart defaults
quickstart:
  mode: guided # guided | interactive | express
  auto_continue: false # Auto-proceed at checkpoints
  detailed_reviews: true # Show full artifacts at checkpoints
```

## Evolution Path

### Phase 1: Basic CLI (MVP)

- `init`, `open`, `status`
- `list`, `show`
- `run` (simple loops)
- `check`, `export`

### Phase 2: Quickstart

- Guided mode with checkpoints
- Setup questions
- Loop orchestration
- Summary displays

### Phase 3: Interactive Mode

- Agent questions
- Free-form responses
- Conversational flow

### Phase 4: Asset Generation

- `generate` commands
- Provider selection
- Image/audio support

### Phase 5: Advanced Features

- Express mode (autonomous)
- Per-role provider config
- Advanced artifact queries
- Diff/comparison tools

### Future: Alternative Interfaces

- **TUI:** Terminal UI with panels (like `k9s`, `lazygit`)
- **GUI:** Desktop app (Electron, Tauri)
- **WebUI:** Browser-based interface
- **MCP Server:** Integration with Claude Desktop, other AI tools

## Testing Strategy

1. **Command Tests:** Each command with various args
2. **Interactive Tests:** Mock user input flows
3. **Integration Tests:** Full workflows end-to-end
4. **Rendering Tests:** Output formatting
5. **Completion Tests:** Shell autocomplete accuracy

## Python Package Structure

```toml
# pyproject.toml
[project]
name = "questfoundry-cli"
version = "0.1.0"
dependencies = [
    "questfoundry>=0.1.0",    # Layer 6 library
    "typer[all]>=0.9.0",
    "rich>=13.0.0",
    "questionary>=2.0.0",
]

[project.scripts]
qf = "qf.cli:app"

[project.entry-points.questfoundry_ui]
# Plugin discovery for future UI extensions
```

## Distribution

**PyPI Package:**

```bash
pip install questfoundry-cli

# Includes questfoundry library dependency
```

**Shell Completion:**

```bash
# Install completion
qf --install-completion

# Or manually
eval "$(_QF_COMPLETE=bash_source qf)" >> ~/.bashrc
```

## Dependencies

- **Layer 6:** questfoundry library for all operations
- **Layer 5:** (via Layer 6) prompts for agent execution
- **Layer 4:** (via Layer 6) protocol for communication
- **Layer 3:** (via Layer 6) schemas for validation

## Integration with Layer 6

CLI is a thin wrapper around Layer 6:

```python
# Example: qf run hook-harvest

from questfoundry.orchestration import Showrunner
from questfoundry import ProtocolClient

def run_loop(loop_name: str, interactive: bool = False):
    client = ProtocolClient(workspace=current_project)
    showrunner = Showrunner(client, interactive=interactive)

    # Execute loop
    result = showrunner.run_loop(loop_name)

    # Display results
    display_loop_summary(result)
```

## Next Steps

1. ⏸️ Create `pvliesdonk/questfoundry-cli` repository
2. ⏸️ Set up Typer/Click framework
3. ⏸️ Implement basic commands (Phase 1)
4. ⏸️ Add Rich formatting
5. ⏸️ Implement quickstart guided mode (Phase 2)
6. ⏸️ Add interactive mode (Phase 3)
7. ⏸️ Implement generate commands (Phase 4)
8. ⏸️ Add shell completion
9. ⏸️ Package for PyPI distribution

## References

- [Layer 6 - Libraries](../06-libraries/README.md)
- [Layer 5 - Prompts](../05-prompts/README.md)
- [Targeted Loops](../00-north-star/LOOPS/README.md)
