# Layers 5-7 Vision & Architecture

**Date:** 2025-10-31
**Status:** Planning / Design Phase

## Executive Summary

This document captures the architectural vision and design decisions for QuestFoundry Layers 5, 6, and 7, discussed after Layer 4 (Protocol) was merged to main.

## Architecture Overview

### Three-Repository Model

1. **Spec Repo:** `pvliesdonk/questfoundry` (current)
   - Layers 0-5: Specifications, documentation, prompts
   - Human-readable, git-tracked canonical source

2. **Library Repo:** `pvliesdonk/questfoundry-lib`
   - Layer 6: Python SDK implementation
   - Protocol client, validators, providers, state management
   - Bundles Layer 5 prompts and Layer 3 schemas

3. **CLI Repo:** `pvliesdonk/questfoundry-cli`
   - Layer 7: Command-line interface
   - Thin wrapper around Layer 6 library
   - User-facing interaction layer

## Layer 5 — Role Prompts

### Purpose

Transform Layer 1 role charters into executable AI agent prompts.

### Key Decisions

**Stateful Sessions:**

- Agents maintain conversation history during active loops
- Session lifetime = loop duration
- Showrunner manages wake/dormancy
- Archived for audit trail

**Agent-to-Human Communication:**

- Hybrid approach: Simple callback API backed by protocol
- Agents call `ask_human(question, context, suggestions)`
- Implemented as `human.question` / `human.response` intents
- Enables conversational collaboration in interactive mode

**Repository Location:**

- Lives in spec repo (`05-prompts/`) as canonical source
- Bundled into Layer 6 library during build
- No runtime dependency on spec repo

**Structure per Role:**

```
05-prompts/
  _shared/
    context_management.md
    safety_protocol.md
    human_interaction.md
  showrunner/
    system_prompt.md
    intent_handlers/
    examples/
  gatekeeper/
    system_prompt.md
    quality_bars/
    examples/
  [... all 14 roles]
```

**Evolution Path:**

1. Phase 1: Core roles (Showrunner, Gatekeeper, Lore Weaver, Scene Smith)
2. Phase 2: Content roles (Plotwright, Codex Curator, Style Lead)
3. Phase 3: Asset roles (Art Director, Illustrator, Audio roles)
4. Phase 4: Support roles (Researcher, Translator, Book Binder)

## Layer 6 — Libraries

### Purpose

Provide SDK for protocol communication, validation, state management, and LLM integration.

### Key Decisions

**State Persistence:**

- **Cold SoT:** SQLite project file (`.qfproj`)
  - Contains: snapshots, views, canon, TU history
  - Portable, efficient, ACID compliant
- **Hot SoT:** File-based workspace (`.questfoundry/hot/`)
  - Human-readable, inspectable
  - Git-friendly (optional export)
- **Future:** Redis/Valkey for distributed workflows

**Provider Plugin Architecture:**

- Start simple: Unified text/image provider config
- Evolve to: Per-role provider configuration
- Plugin interface for extensibility

**Supported Providers (Planned):**

_Text Generation:_

- OpenAI GPT (Phase 2)
- Ollama - local models (Phase 2)
- Google Gemini (Phase 5)
- Amazon Bedrock (Phase 5)

_Image Generation:_

- Automatic1111 Stable Diffusion (Phase 4)
- OpenAI DALL-E (Phase 4)
- Google Imagen 4 (Phase 5)

_Audio Generation:_

- ElevenLabs (Phase 4)

**Core Components:**

```
questfoundry-lib/
  src/questfoundry/
    protocol/         # Layer 4 client
    validation/       # Layer 3 schemas
    lifecycles/       # State machines
    artifacts/        # Typed wrappers
    state/            # Storage backends
    providers/        # LLM/image/audio plugins
    roles/            # Session management
    orchestration/    # Showrunner
    safety/           # PN boundaries
    resources/        # Bundled prompts/schemas
```

**Evolution Path:**

1. Phase 1: Core infrastructure (protocol, validation, state)
2. Phase 2: Basic providers (OpenAI, Ollama)
3. Phase 3: Role execution (sessions, prompts)
4. Phase 4: Asset generation (image, audio)
5. Phase 5: Advanced providers (Gemini, Bedrock, Imagen)

## Layer 7 — UI

### Purpose

Provide author and player interfaces. Initial focus: CLI.

### Key Decisions

**Command Structure (Verb-Noun, Git-style):**

```bash
# Project
qf init, qf open, qf status

# Quickstart
qf quickstart [--interactive|--express]

# Loops
qf run <loop-name> [--interactive]

# Asset Generation
qf generate image|audio|scene|canon <artifact-id> [--provider X]

# Inspection
qf list hooks|tus|canon
qf show <artifact-id>

# Quality
qf check [--bars X,Y]

# Export
qf export view|git
```

**Interaction Modes:**

1. **Guided Mode (MVP, Default):**
   - Loop-by-loop checkpoints
   - Simple Y/N prompts
   - Author reviews between loops
   - Fast for experienced users

2. **Interactive Mode:**
   - Agents ask questions inline
   - Free-form human responses
   - Conversational collaboration
   - Flag: `--interactive`

3. **Express Mode (Future):**
   - Fully autonomous
   - Setup questions → complete manuscript
   - Only stops for failures
   - Flag: `--express`

**Quickstart Evolution:**

- Start with Option B (Loop-by-Loop Checkpoints)
- Add Option C (Approval Tiers: Guided/Interactive/Express)
- Eventually enable Option A (Fully Autonomous) as mature feature

**UI Toolkit:**

- CLI Framework: Typer or Click
- Rich Text: Rich library (tables, progress, colors)
- Prompts: Questionary or InquirerPy
- Shell Completion: Bash, Zsh, Fish

**Structure:**

```
questfoundry-cli/
  src/qf/
    commands/         # Command implementations
    interactive/      # Interactive mode handling
    completions/      # Shell autocomplete
    formatting/       # Output rendering
```

**Evolution Path:**

1. Phase 1: Basic CLI (init, list, show, run, check, export)
2. Phase 2: Quickstart guided mode
3. Phase 3: Interactive mode (agent questions)
4. Phase 4: Asset generation commands
5. Phase 5: Express mode, advanced features
6. Future: TUI, GUI, WebUI, MCP server

## Cross-Cutting Concerns

### Workflow Orchestration

**Quickstart Modes:**

| Mode        | Autonomy | Checkpoints      | Agent Questions           | Target User            |
| ----------- | -------- | ---------------- | ------------------------- | ---------------------- |
| Guided      | Low      | After each loop  | No (batch at checkpoints) | Learning, reviewing    |
| Interactive | Medium   | After each loop  | Yes (inline)              | Collaborative creation |
| Express     | High     | Only on failures | Auto-answered/skipped     | Fast iteration         |

**Evolution:** B (Guided) → C (Tiers) → A (Express mature)

### Provider Configuration

**MVP (Simple):**

```yaml
providers:
  text:
    default: openai
    openai: { api_key: ..., model: gpt-4o }
  image:
    default: dalle
```

**Future (Per-Role):**

```yaml
roles:
  scene_smith:
    provider: openai
    model: gpt-4o
  gatekeeper:
    provider: ollama
    model: llama3
  illustrator:
    provider: dalle
    model: dall-e-3
```

### Safety & Traceability

- All agent-to-human questions logged as protocol messages
- TU links every decision and artifact
- Session archives for audit trails
- PN boundaries enforced at multiple layers:
  - Protocol (Layer 4): Envelope routing
  - Library (Layer 6): Safety guards
  - Prompts (Layer 5): Agent instructions

### Testing Strategy

**Layer 5:**

- Prompt validation (references to schemas/protocol)
- Intent coverage (each role handles required intents)
- Conversation tests (example flows)

**Layer 6:**

- Unit tests (components)
- Integration tests (protocol + state)
- Provider tests (mock and real)
- End-to-end tests (full loops with mock LLM)

**Layer 7:**

- Command tests (all arguments)
- Interactive tests (mock user input)
- Rendering tests (output formatting)
- Completion tests (autocomplete)

## Implementation Timeline

### Immediate (Post-Layer 4)

- ✅ Capture vision in documentation (this doc + READMEs)
- ⏸️ Create Layer 6 repository structure
- ⏸️ Create Layer 7 repository structure

### Short Term (Phase 1-2)

- ⏸️ Layer 6: Protocol client, validation, state persistence
- ⏸️ Layer 6: OpenAI + Ollama providers
- ⏸️ Layer 7: Basic CLI commands
- ⏸️ Layer 5: Core role prompts (4 roles)

### Medium Term (Phase 3-4)

- ⏸️ Layer 6: Session management, role execution
- ⏸️ Layer 6: Image/audio providers
- ⏸️ Layer 7: Quickstart guided mode
- ⏸️ Layer 7: Interactive mode
- ⏸️ Layer 5: All 14 roles complete

### Long Term (Phase 5+)

- ⏸️ Layer 6: Advanced providers (Gemini, Bedrock, Imagen)
- ⏸️ Layer 6: Redis/Valkey state backend
- ⏸️ Layer 7: Express mode
- ⏸️ Layer 7: Advanced features (diff, queries)
- ⏸️ Future UIs: TUI, GUI, WebUI, MCP

## Key Design Principles

1. **Progressive Disclosure:** Simple by default, powerful when needed
2. **Evolutionary Design:** Start simple, architect for future complexity
3. **Protocol First:** Everything flows through Layer 4 protocol
4. **Canon First:** All artifacts validate against Layer 3 schemas
5. **Safety Always:** PN boundaries enforced at every layer
6. **Human in Loop:** Always option for human review/intervention
7. **Audit Trail:** Every decision tracked via TUs and protocol messages

## Open Questions (For Future Resolution)

1. **LLM Context Management:** How to handle very long conversation histories?
2. **Cost Control:** Rate limiting, budget caps for LLM calls?
3. **Offline Mode:** Can any operations work without LLM access?
4. **Multi-Author:** If needed later, how to handle concurrent sessions?
5. **Asset Versioning:** How to track iterations of generated images/audio?
6. **Prompt Versioning:** Strategy for updating prompts without breaking projects?

## Success Criteria

**Layer 5:**

- All 14 roles have complete, tested prompts
- Agents successfully execute their role charters
- Human-AI collaboration works smoothly in interactive mode
- Safety boundaries respected by all agents

**Layer 6:**

- Protocol client works reliably
- Multiple LLM providers supported
- State persistence robust (SQLite + files)
- Session management handles complex loops
- Full test coverage

**Layer 7:**

- CLI intuitive for new users
- Quickstart creates usable manuscripts
- Interactive mode feels natural
- Shell completion works
- Clear progress indicators and summaries

## References

- [Layer 5 README](./05-prompts/README.md)
- [Layer 6 README](./06-libraries/README.md)
- [Layer 7 README](./07-ui/README.md)
- [Layer 4 Protocol](./04-protocol/README.md)
- [Layer 1 Roles](./01-roles/README.md)
- [North Star Loops](./00-north-star/LOOPS/README.md)

---

**Next Action:** Begin Layer 6 repository setup once Layer 4 stabilizes on main.
