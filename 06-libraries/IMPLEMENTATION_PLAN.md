# Layer 6 Implementation Plan

**Target Agent:** GitHub Copilot or similar code-generation AI **Repository:**
`pvliesdonk/questfoundry-lib` **Language:** Python 3.11+ **Package Manager:** UV (modern Python
package manager)

## Overview

This plan breaks Layer 6 implementation into sequential epics and features. Each epic is designed to
be self-contained and builds upon previous work. AI agents should implement features in the order
specified.

---

## Epic 1: Project Foundation

**Goal:** Set up repository structure, tooling, and basic infrastructure.

**Dependencies:** None

**Estimated Effort:** 1-2 days

### Features

#### 1.1: Repository Setup

**Files to create:**

```
questfoundry-lib/
  .gitignore
  .github/
    workflows/
      test.yml           # CI/CD for tests
      lint.yml           # Linting and formatting
  README.md
  LICENSE              # MIT or Apache 2.0
  pyproject.toml       # Project metadata and dependencies
  uv.lock             # UV lock file
```

**Tasks:**

- Initialize Python project with UV
- Configure `pyproject.toml`:
  - Package name: `questfoundry`
  - Version: `0.1.0`
  - Python requirement: `>=3.11`
  - Dependencies: `pydantic>=2.0`, `jsonschema>=4.0`, `httpx>=0.25`, `python-dotenv>=1.0`
- Set up GitHub Actions for CI/CD
- Create comprehensive `.gitignore` for Python

**Acceptance Criteria:**

- `uv sync` works
- CI/CD pipeline runs successfully
- README has basic project description

---

#### 1.2: Package Structure

**Files to create:**

```
src/questfoundry/
  __init__.py
  py.typed              # PEP 561 marker for type hints
  version.py            # Version info
```

**Tasks:**

- Create src-layout package structure
- Add type hints marker for mypy
- Export version info

**Acceptance Criteria:**

- `import questfoundry` works
- Package version accessible: `questfoundry.__version__`

---

#### 1.3: Development Tools

**Files to create:**

```
.pre-commit-config.yaml
.ruff.toml              # or pyproject.toml section
.mypy.ini               # Type checking config
```

**Tasks:**

- Set up Ruff for linting and formatting
- Configure mypy for strict type checking
- Set up pre-commit hooks
- Add pytest configuration in `pyproject.toml`

**Acceptance Criteria:**

- `ruff check` passes
- `mypy src/` passes
- `pytest` runs (even with no tests)

---

## Epic 2: Layer 3/4 Integration

**Goal:** Load and validate against Layer 3 schemas and Layer 4 protocol.

**Dependencies:** Epic 1

**Estimated Effort:** 3-4 days

### Features

#### 2.1: Schema Bundling

**Files to create:**

```
src/questfoundry/
  resources/
    __init__.py
    schemas/
      __init__.py
      hook_card.schema.json
      tu_brief.schema.json
      [... all 17 schemas from Layer 3]
    loader.py
```

**Tasks:**

- Copy all 17 JSON schemas from `questfoundry/03-schemas/` into resources
- Create `loader.py` with `get_schema(artifact_type: str) -> dict` function
- Use `importlib.resources` for cross-platform resource loading

**Acceptance Criteria:**

- All 17 schemas accessible via `get_schema()`
- Schemas validate as proper JSON Schema Draft 2020-12

---

#### 2.2: Schema Validation

**Files to create:**

```
src/questfoundry/
  validation/
    __init__.py
    schema.py
    result.py
tests/
  validation/
    test_schema.py
```

**Tasks:**

- Implement `validate_artifact(artifact_type, data) -> ValidationResult`
- Use `jsonschema` library for validation
- Create `ValidationResult` dataclass with:
  - `valid: bool`
  - `errors: List[ValidationError]`
  - `warnings: List[str]`
- Add comprehensive error messages

**Acceptance Criteria:**

- Valid artifacts pass validation
- Invalid artifacts return detailed error messages
- All 17 artifact types supported

**Test Cases:**

- Valid hook_card validates successfully
- Invalid hook_card (missing required field) fails with clear error
- Invalid enum value fails with suggestion

---

#### 2.3: Protocol Envelope

**Files to create:**

```
src/questfoundry/
  protocol/
    __init__.py
    envelope.py
    types.py          # Protocol type definitions
tests/
  protocol/
    test_envelope.py
    fixtures/
      envelopes/      # Example envelopes from Layer 4
```

**Tasks:**

- Create Pydantic models for Layer 4 protocol:
  - `Protocol` (name, version)
  - `Sender`, `Receiver` (role, agent)
  - `Context` (hot_cold, tu, snapshot, loop)
  - `Safety` (player_safe, spoilers)
  - `Payload` (type, schema, data)
  - `Envelope` (top-level)
- Implement envelope builder with fluent API
- Add serialization (to/from JSON)

**Acceptance Criteria:**

- Can construct valid envelopes programmatically
- Can parse envelope JSON from Layer 4 examples
- Pydantic validation catches malformed envelopes

**Test Cases:**

- Build and serialize envelope
- Parse all 13 example envelopes from `04-protocol/EXAMPLES/`
- Invalid envelope raises validation error

---

#### 2.4: Protocol Conformance

**Files to create:**

```
src/questfoundry/
  validation/
    conformance.py
tests/
  validation/
    test_conformance.py
```

**Tasks:**

- Implement `validate_envelope(envelope) -> ConformanceResult`
- Check Layer 4 conformance rules:
  - Protocol version compatibility
  - Intent valid for sender/receiver roles
  - Payload schema matches artifact type
  - Safety flags appropriate for receiver
  - Context fields present when required
- Reference Layer 4 `CONFORMANCE.md`

**Acceptance Criteria:**

- Valid envelopes pass conformance
- Violations clearly reported
- PN safety rules enforced

**Test Cases:**

- Valid envelope passes
- Envelope with invalid intent fails
- Envelope to PN with spoilers fails safety check

---

## Epic 3: State Management

**Goal:** Implement state persistence for projects, artifacts, and TUs.

**Dependencies:** Epic 2

**Estimated Effort:** 4-5 days

### Features

#### 3.1: State Store Interface

**Files to create:**

```
src/questfoundry/
  state/
    __init__.py
    store.py          # Abstract interface
    types.py          # State type definitions
```

**Tasks:**

- Define abstract `StateStore` interface:
  - `get_project_info() -> ProjectInfo`
  - `save_artifact(artifact: Artifact)`
  - `get_artifact(artifact_id: str) -> Optional[Artifact]`
  - `list_artifacts(type: str, filters: dict) -> List[Artifact]`
  - `save_tu(tu: TU)`
  - `get_tu(tu_id: str) -> Optional[TU]`
  - `list_tus(filters: dict) -> List[TU]`
- Create Pydantic models for state types

**Acceptance Criteria:**

- Clear abstract interface defined
- Type hints for all methods
- Docstrings with examples

---

#### 3.2: SQLite Project File

**Files to create:**

```
src/questfoundry/
  state/
    sqlite_store.py
    schema.sql        # Database schema
tests/
  state/
    test_sqlite_store.py
```

**Tasks:**

- Implement `SQLiteStore(StateStore)` for `.qfproj` files
- Create database schema:
  - `project` table (metadata)
  - `snapshots` table
  - `views` table
  - `artifacts` table (polymorphic, JSONB data column)
  - `tus` table
  - `history` table (audit log)
- Use SQLite JSON functions for querying
- Implement all StateStore methods
- Add migrations system (simple version numbering)

**Acceptance Criteria:**

- Can create new `.qfproj` file
- Can save and retrieve artifacts
- Can query artifacts by type, status, etc.
- ACID transactions work

**Test Cases:**

- Create project, save artifact, retrieve it
- List all hooks with status='proposed'
- Transaction rollback on error

---

#### 3.3: File-Based Hot Workspace

**Files to create:**

```
src/questfoundry/
  state/
    file_store.py
tests/
  state/
    test_file_store.py
```

**Tasks:**

- Implement `FileStore(StateStore)` for hot workspace
- Directory structure:
  ```
  .questfoundry/
    hot/
      hooks/
        HOOK-001.json
      canon/
      tu_briefs/
    metadata.json
  ```
- File naming: `{ARTIFACT-ID}.json`
- Atomic writes (write to temp, rename)

**Acceptance Criteria:**

- Can save artifacts as JSON files
- Can load artifacts from files
- Atomic writes prevent corruption
- Directory structure auto-created

**Test Cases:**

- Save and load artifact
- List all artifacts in hot workspace
- Concurrent writes don't corrupt

---

#### 3.4: Workspace Manager

**Files to create:**

```
src/questfoundry/
  state/
    workspace.py
tests/
  state/
    test_workspace.py
```

**Tasks:**

- Create `Workspace` class that manages:
  - `.qfproj` file (cold SoT via SQLiteStore)
  - `.questfoundry/` directory (hot SoT via FileStore)
  - Config file (`.questfoundry/config.yml`)
- Provide unified API:
  - `get_cold_artifact(id)` → SQLite
  - `get_hot_artifact(id)` → File
  - `promote_to_cold(artifact_id)` → Hot → Cold
- Handle workspace initialization

**Acceptance Criteria:**

- Can init new workspace with both stores
- Can access hot and cold artifacts
- Can promote artifacts from hot to cold

**Test Cases:**

- Initialize workspace
- Save to hot, promote to cold
- Query both hot and cold

---

## Epic 4: Artifact Types & Lifecycles

**Goal:** Implement typed wrappers and state machines for all artifacts.

**Dependencies:** Epic 3

**Estimated Effort:** 5-6 days

### Features

#### 4.1: Base Artifact Class

**Files to create:**

```
src/questfoundry/
  artifacts/
    __init__.py
    base.py
tests/
  artifacts/
    test_base.py
```

**Tasks:**

- Create `Artifact` base class:
  - Common fields: id, type, created, modified, author
  - Methods: `validate()`, `to_dict()`, `from_dict()`
  - Integration with schema validation
- Use Pydantic for data modeling

**Acceptance Criteria:**

- Base class provides common functionality
- Validation delegates to schema validator
- Serialization works

---

#### 4.2: Core Artifact Types

**Files to create:**

```
src/questfoundry/
  artifacts/
    hook_card.py
    tu_brief.py
    canon_pack.py
    gatecheck_report.py
tests/
  artifacts/
    test_hook_card.py
    [... tests for each]
```

**Tasks:**

- Implement typed wrappers for core artifacts:
  - `HookCard` (with lifecycle methods)
  - `TUBrief`
  - `CanonPack`
  - `GatecheckReport`
- Each class:
  - Inherits from `Artifact`
  - Type-safe field access
  - Lifecycle-specific methods if applicable

**Acceptance Criteria:**

- Type-safe artifact creation
- IDE autocomplete works
- Validation enforced

**Test Cases:**

- Create valid HookCard
- Invalid HookCard raises ValidationError
- Serialize and deserialize

---

#### 4.3: Remaining Artifact Types

**Files to create:**

```
src/questfoundry/
  artifacts/
    codex_entry.py
    style_addendum.py
    research_memo.py
    shotlist.py
    cuelist.py
    view_log.py
    [... all remaining artifacts]
```

**Tasks:**

- Implement remaining 13 artifact types
- Follow same pattern as core artifacts

**Acceptance Criteria:**

- All 17 artifact types implemented
- Consistent API across types

---

#### 4.4: Hook Lifecycle State Machine

**Files to create:**

```
src/questfoundry/
  lifecycles/
    __init__.py
    base.py           # Base state machine
    hooks.py
tests/
  lifecycles/
    test_hooks.py
```

**Tasks:**

- Implement Hook state machine from Layer 4:
  - States: proposed → accepted → in-progress → resolved → canonized
  - Transitions with validation
  - State history tracking
- Reference `04-protocol/LIFECYCLES/hooks.md`

**Acceptance Criteria:**

- Valid transitions succeed
- Invalid transitions raise StateTransitionError
- History tracked

**Test Cases:**

- Full lifecycle: proposed → canonized
- Invalid transition raises error
- State history queryable

---

#### 4.5: TU Lifecycle State Machine

**Files to create:**

```
src/questfoundry/
  lifecycles/
    tu.py
tests/
  lifecycles/
    test_tu.py
```

**Tasks:**

- Implement TU state machine:
  - States: hot-proposed → stabilizing → gatecheck → cold-merged
  - Transitions with validation
- Reference `04-protocol/LIFECYCLES/tu.md`

**Acceptance Criteria:**

- Valid transitions work
- Gatecheck required before cold-merged
- History tracked

---

## Epic 5: Protocol Client

**Goal:** Implement protocol client for sending/receiving messages.

**Dependencies:** Epic 4

**Estimated Effort:** 3-4 days

### Features

#### 5.1: File-Based Transport

**Files to create:**

```
src/questfoundry/
  protocol/
    transport.py
    file_transport.py
tests/
  protocol/
    test_file_transport.py
```

**Tasks:**

- Define `Transport` abstract interface:
  - `send(envelope: Envelope)`
  - `receive() -> Iterator[Envelope]`
- Implement `FileTransport`:
  - Writes envelopes to `.questfoundry/messages/outbox/`
  - Reads from `.questfoundry/messages/inbox/`
  - Atomic file operations
  - Message acknowledgment (move to processed/)

**Acceptance Criteria:**

- Can send envelope to file
- Can receive envelopes from directory
- No lost messages

**Test Cases:**

- Send and receive message
- Multiple messages in order
- Concurrent access safe

---

#### 5.2: Protocol Client

**Files to create:**

```
src/questfoundry/
  protocol/
    client.py
tests/
  protocol/
    test_client.py
```

**Tasks:**

- Implement `ProtocolClient`:
  - Constructor: `ProtocolClient(workspace, transport)`
  - `send(envelope) -> None`
  - `send_and_wait(envelope, timeout) -> Envelope`
  - `receive() -> Iterator[Envelope]`
  - `subscribe(intent_pattern, callback)`
- Integrate with workspace
- Auto-validation on send/receive

**Acceptance Criteria:**

- Can send messages via client
- Validation happens automatically
- Can wait for response

**Test Cases:**

- Send message
- Send and wait for response
- Subscribe to intent pattern

---

## Epic 6: Provider System

**Goal:** Implement LLM and image provider plugin architecture.

**Dependencies:** Epic 5

**Estimated Effort:** 6-8 days

### Features

#### 6.1: Provider Interface

**Files to create:**

```
src/questfoundry/
  providers/
    __init__.py
    base.py
    types.py
    registry.py
```

**Tasks:**

- Define `TextProvider` abstract interface:
  - `generate_text(prompt, model, **kwargs) -> str`
  - `generate_streaming(prompt, model, **kwargs) -> Iterator[str]`
- Define `ImageProvider` abstract interface:
  - `generate_image(prompt, model, **kwargs) -> bytes`
- Create provider registry for plugin discovery

**Acceptance Criteria:**

- Clear interfaces defined
- Registry can register/lookup providers

---

#### 6.2: Configuration System

**Files to create:**

```
src/questfoundry/
  config/
    __init__.py
    config.py
    schema.py
tests/
  config/
    test_config.py
```

**Tasks:**

- Implement configuration loading:
  - Read from `.questfoundry/config.yml`
  - Environment variable substitution (`${OPENAI_API_KEY}`)
  - Schema validation with Pydantic
- Configuration structure:
  - `providers.text.default`
  - `providers.text.{provider}.{settings}`
  - `providers.image.default`
  - Role overrides (future)

**Acceptance Criteria:**

- Can load config from YAML
- Environment variables substituted
- Invalid config raises error

**Test Cases:**

- Load valid config
- Environment variable substitution
- Missing required field raises error

---

#### 6.3: OpenAI Provider

**Files to create:**

```
src/questfoundry/
  providers/
    text/
      __init__.py
      openai.py
tests/
  providers/
    text/
      test_openai.py
```

**Tasks:**

- Implement `OpenAIProvider(TextProvider)`:
  - Use `openai` library (optional dependency)
  - Support GPT-4, GPT-4o, etc.
  - Handle API errors gracefully
  - Retry logic with exponential backoff
  - Streaming support
- Register in provider registry

**Acceptance Criteria:**

- Can generate text with OpenAI
- Errors handled gracefully
- Streaming works

**Test Cases:**

- Generate text (mocked API)
- Handle API error
- Streaming response

---

#### 6.4: Ollama Provider

**Files to create:**

```
src/questfoundry/
  providers/
    text/
      ollama.py
tests/
  providers/
    text/
      test_ollama.py
```

**Tasks:**

- Implement `OllamaProvider(TextProvider)`:
  - Use Ollama REST API
  - Support llama3, mistral, etc.
  - Local model support
  - Streaming support

**Acceptance Criteria:**

- Can generate text with Ollama
- Works with local models
- Streaming works

---

#### 6.5: Automatic1111 Provider

**Files to create:**

```
src/questfoundry/
  providers/
    image/
      __init__.py
      a1111.py
tests/
  providers/
    image/
      test_a1111.py
```

**Tasks:**

- Implement `A1111Provider(ImageProvider)`:
  - Use A1111 REST API
  - Support txt2img endpoint
  - Handle generation parameters (steps, cfg_scale, etc.)
  - Save images with metadata

**Acceptance Criteria:**

- Can generate images via A1111
- Parameters configurable
- Returns image bytes

---

#### 6.6: DALL-E Provider

**Files to create:**

```
src/questfoundry/
  providers/
    image/
      dalle.py
tests/
  providers/
    image/
      test_dalle.py
```

**Tasks:**

- Implement `DALLEProvider(ImageProvider)`:
  - Use OpenAI images API
  - Support DALL-E 3
  - Handle size, quality parameters

**Acceptance Criteria:**

- Can generate images with DALL-E
- Parameters configurable

---

## Epic 7: Role Execution

**Goal:** Load prompts, execute with LLMs, manage sessions.

**Dependencies:** Epic 6

**Estimated Effort:** 5-7 days

### Features

#### 7.1: Prompt Bundling

**Files to create:**

```
src/questfoundry/
  resources/
    prompts/
      # Copied from 05-prompts/ in spec repo
      _shared/
      showrunner/
      gatekeeper/
      [... all roles]
    prompt_loader.py
```

**Tasks:**

- Copy Layer 5 prompts into resources (when available)
- Create `load_prompt(role_name, component) -> str` function
- Support prompt templating (Jinja2 or similar)

**Acceptance Criteria:**

- Prompts loadable from package
- Template variables can be substituted

---

#### 7.2: Role Session

**Files to create:**

```
src/questfoundry/
  roles/
    __init__.py
    session.py
tests/
  roles/
    test_session.py
```

**Tasks:**

- Implement `RoleSession`:
  - Maintains conversation history
  - Tracks TU context
  - Handles message send/receive
  - Provides `ask_human()` callback
- Session lifecycle management
- Session archival

**Acceptance Criteria:**

- Can create session for role
- Conversation history maintained
- Sessions can be archived

**Test Cases:**

- Create session, send messages
- Ask human callback
- Archive session

---

#### 7.3: Prompt Executor

**Files to create:**

```
src/questfoundry/
  roles/
    executor.py
tests/
  roles/
    test_executor.py
```

**Tasks:**

- Implement `PromptExecutor`:
  - Load prompt for role
  - Substitute template variables
  - Execute with configured LLM provider
  - Handle conversation history
  - Parse LLM response
  - Validate output artifacts

**Acceptance Criteria:**

- Can execute prompt with LLM
- Response parsed correctly
- Artifacts validated

---

#### 7.4: Session Manager

**Files to create:**

```
src/questfoundry/
  roles/
    manager.py
tests/
  roles/
    test_manager.py
```

**Tasks:**

- Implement `SessionManager`:
  - `wake_role(role, tu) -> RoleSession`
  - `dormant_role(role)`
  - `get_active_roles() -> List[str]`
  - Track all active sessions
  - Handle human question routing

**Acceptance Criteria:**

- Can wake/dormant roles
- Track active sessions
- Human questions routed correctly

---

## Epic 8: Orchestration

**Goal:** Implement Showrunner loop orchestration.

**Dependencies:** Epic 7

**Estimated Effort:** 5-6 days

### Features

#### 8.1: Loop Definitions

**Files to create:**

```
src/questfoundry/
  orchestration/
    __init__.py
    loops.py
    types.py
```

**Tasks:**

- Define loop structures from Layer 0:
  - 11 targeted loops
  - Roles involved in each
  - Message sequences
- Reference Layer 4 FLOWS

**Acceptance Criteria:**

- All 11 loops defined
- Role participation clear

---

#### 8.2: Checkpoint System

**Files to create:**

```
src/questfoundry/
  orchestration/
    checkpoint.py
tests/
  orchestration/
    test_checkpoint.py
```

**Tasks:**

- Implement checkpoint management:
  - Create checkpoint after each loop
  - Checkpoint contains: loop name, TU, artifacts created, summary
  - Store in workspace
  - Support checkpoint review

**Acceptance Criteria:**

- Checkpoints created automatically
- Can review checkpoint data
- Can resume from checkpoint

---

#### 8.3: Showrunner Core

**Files to create:**

```
src/questfoundry/
  orchestration/
    showrunner.py
tests/
  orchestration/
    test_showrunner.py
```

**Tasks:**

- Implement `Showrunner`:
  - `run_loop(loop_name, interactive) -> LoopResult`
  - Wake required roles
  - Execute message sequences from Layer 4 FLOWS
  - Create TUs
  - Create checkpoints
  - Handle errors
  - Dormant roles when done

**Acceptance Criteria:**

- Can run simple loop end-to-end
- Roles woken and dormented correctly
- Checkpoints created

**Test Cases:**

- Run Hook Harvest loop (mocked LLM)
- Error handling
- Checkpoint creation

---

#### 8.4: Quickstart Orchestration

**Files to create:**

```
src/questfoundry/
  orchestration/
    quickstart.py
tests/
  orchestration/
    test_quickstart.py
```

**Tasks:**

- Implement quickstart workflow:
  - Setup questions
  - Loop sequence (Hook Harvest → Lore Deepening → Story Spark → ...)
  - Checkpoint approval (guided mode)
  - Inline questions (interactive mode)

**Acceptance Criteria:**

- Can run quickstart with checkpoints
- Setup questions collected
- Loops execute in sequence

---

## Epic 9: Safety & Quality

**Goal:** Implement PN boundaries and gatekeeper validation.

**Dependencies:** Epic 8

**Estimated Effort:** 3-4 days

### Features

#### 9.1: PN Guard

**Files to create:**

```
src/questfoundry/
  safety/
    __init__.py
    pn_guard.py
tests/
  safety/
    test_pn_guard.py
```

**Tasks:**

- Implement PN boundary enforcement:
  - Filter envelopes to PN (only cold + player_safe)
  - Strip spoilers from artifacts
  - Validate gateway conditions diegetic
  - Prevent codewords/mechanics in player surfaces

**Acceptance Criteria:**

- PN only receives safe content
- Spoilers stripped
- Violations caught

**Test Cases:**

- Hot artifact blocked from PN
- Spoiler field stripped
- Cold player-safe artifact allowed

---

#### 9.2: Quality Bar Validators

**Files to create:**

```
src/questfoundry/
  validation/
    quality_bars/
      __init__.py
      integrity.py
      reachability.py
      style.py
      gateways.py
      nonlinearity.py
      determinism.py
      presentation.py
      spoiler_hygiene.py
tests/
  validation/
    quality_bars/
      test_integrity.py
      [... one per bar]
```

**Tasks:**

- Implement 8 quality bar validators:
  - Each returns pass/fail + violations
  - Reference Layer 0 QUALITY_BARS.md
- Integrate with Gatekeeper role

**Acceptance Criteria:**

- All 8 bars implemented
- Clear violation messages
- Can run individually or all together

---

#### 9.3: Gatekeeper Integration

**Files to create:**

```
src/questfoundry/
  validation/
    gatekeeper.py
tests/
  validation/
    test_gatekeeper.py
```

**Tasks:**

- Implement `Gatekeeper` class:
  - Run all quality bars
  - Generate gatecheck report artifact
  - Block hot→cold promotion on failures
  - Integrate with Showrunner

**Acceptance Criteria:**

- Can run full gatecheck
- Report generated
- Failures block promotion

---

## Epic 10: Export & Views

**Goal:** Implement view generation and export formats.

**Dependencies:** Epic 9

**Estimated Effort:** 3-4 days

### Features

#### 10.1: View Generation

**Files to create:**

```
src/questfoundry/
  export/
    __init__.py
    view.py
tests/
  export/
    test_view.py
```

**Tasks:**

- Implement view generation:
  - Extract cold artifacts from snapshot
  - Filter by player-safe flag
  - Package as view artifact
  - Store in .qfproj

**Acceptance Criteria:**

- Can generate view from snapshot
- Only player-safe content included
- View stored in project

---

#### 10.2: Git Export

**Files to create:**

```
src/questfoundry/
  export/
    git_export.py
tests/
  export/
    test_git_export.py
```

**Tasks:**

- Implement git-friendly export:
  - Export cold snapshot as YAML files
  - Human-readable directory structure
  - Manifest file
  - Can be diffed in git

**Acceptance Criteria:**

- Exports as YAML files
- Directory structure logical
- Can be committed to git

---

#### 10.3: Book Binder

**Files to create:**

```
src/questfoundry/
  export/
    binder.py
tests/
  export/
    test_binder.py
```

**Tasks:**

- Implement Book Binder role logic:
  - Render view to various formats
  - HTML export
  - Markdown export
  - PDF export (future)

**Acceptance Criteria:**

- Can render view to HTML
- Can render view to Markdown

---

## Epic 11: Documentation & Polish

**Goal:** Complete documentation, examples, and package distribution.

**Dependencies:** Epic 10

**Estimated Effort:** 2-3 days

### Features

#### 11.1: API Documentation

**Files to create:**

```
docs/
  index.md
  api/
    protocol.md
    validation.md
    state.md
    providers.md
    roles.md
    orchestration.md
  examples/
    basic_usage.md
    custom_provider.md
```

**Tasks:**

- Write comprehensive API docs
- Add docstrings to all public APIs
- Create usage examples
- Set up Sphinx or MkDocs

**Acceptance Criteria:**

- All public APIs documented
- Examples work
- Docs build successfully

---

#### 11.2: Integration Examples

**Files to create:**

```
examples/
  01_create_project.py
  02_validate_artifact.py
  03_run_loop.py
  04_custom_provider.py
  05_quickstart.py
```

**Tasks:**

- Create runnable examples
- Cover common use cases
- Include inline comments

**Acceptance Criteria:**

- All examples run successfully
- Cover key functionality

---

#### 11.3: Package Distribution

**Files to create:**

```
MANIFEST.in
CHANGELOG.md
```

**Tasks:**

- Configure package for PyPI
- Include bundled resources (schemas, prompts)
- Test installation in clean environment
- Create GitHub release

**Acceptance Criteria:**

- Package installable via `pip install questfoundry`
- All resources bundled
- Wheels built for multiple platforms

---

## Testing Strategy

### Unit Tests

- Each module has corresponding test file
- Aim for >80% code coverage
- Use pytest fixtures for common setups

### Integration Tests

**Files to create:**

```
tests/
  integration/
    test_full_loop.py
    test_quickstart.py
    test_hot_to_cold.py
```

**Tasks:**

- Test complete workflows
- Use mock LLM providers
- Test error paths

### Performance Tests

**Files to create:**

```
tests/
  performance/
    test_large_project.py
```

**Tasks:**

- Test with large numbers of artifacts
- SQLite query performance
- File I/O performance

---

## Implementation Order Summary

**Phase 1: Foundation**

1. Epic 1: Project Foundation
2. Epic 2: Layer 3/4 Integration

**Phase 2: Core Infrastructure** 3. Epic 3: State Management 4. Epic 4: Artifact Types &
Lifecycles 5. Epic 5: Protocol Client

**Phase 3: Providers** 6. Epic 6: Provider System

**Phase 4: Intelligence** 7. Epic 7: Role Execution 8. Epic 8: Orchestration

**Phase 5: Quality & Export** 9. Epic 9: Safety & Quality 10. Epic 10: Export & Views

**Phase 6: Polish** 11. Epic 11: Documentation & Polish

---

## AI Agent Instructions

### For GitHub Copilot

**Context to provide:**

- "Implementing Layer 6 of QuestFoundry system"
- "Reference specification files in questfoundry repo"
- "Follow Pydantic models, type hints, and pytest patterns"
- "Maintain compatibility with Layer 3 schemas and Layer 4 protocol"

**Best practices:**

- Always add type hints
- Write docstrings for public APIs
- Create corresponding test files
- Use Pydantic for validation
- Handle errors gracefully

**When stuck:**

- Reference Layer 3 schemas in `03-schemas/`
- Reference Layer 4 protocol in `04-protocol/`
- Check existing test patterns

### Checkpoints

After each epic:

- [ ] All tests pass
- [ ] Type checking passes (mypy)
- [ ] Linting passes (ruff)
- [ ] Documentation updated
- [ ] Commit with conventional commit message

---

## Success Criteria

Layer 6 is complete when:

- [ ] All 11 epics implemented
- [ ] Test coverage >80%
- [ ] All Layer 3 schemas supported
- [ ] Layer 4 protocol fully implemented
- [ ] At least 2 text providers (OpenAI, Ollama)
- [ ] At least 2 image providers (A1111, DALL-E)
- [ ] Quickstart workflow works end-to-end
- [ ] Documentation complete
- [ ] Package published to PyPI

---

## Estimated Timeline

**Aggressive (Full-time AI agent):** 6-8 weeks **Moderate (Part-time):** 12-16 weeks
**Conservative:** 20-24 weeks

Assumes AI agent (Copilot) with human review at epic boundaries.
