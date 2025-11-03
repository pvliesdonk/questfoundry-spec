# Layer 6 — Libraries (SDK & Implementation)

**Status:** 🚧 Planning Phase **Last Updated:** 2025-10-31

## Overview

Layer 6 provides software libraries, validators, and runtime implementations for the QuestFoundry
system. This layer bridges the specification (Layers 0-5) with user interfaces (Layer 7).

## Purpose

- Provide programmatic access to QuestFoundry protocol
- Implement protocol client for sending/receiving Layer 4 envelopes
- Validate artifacts against Layer 3 schemas
- Manage artifact lifecycles (hooks, TUs, etc.)
- Support multiple LLM/image providers via plugin architecture
- Manage role sessions and state persistence
- Execute Layer 5 prompts with real LLM backends

## Repository

**Primary Implementation:** `pvliesdonk/questfoundry-lib` (Python)

This directory (`06-libraries/`) in the spec repo contains:

- High-level architecture documentation
- Integration guides
- Cross-language specifications

The actual implementation lives in the separate library repository.

## Architecture

### Core Components

```
questfoundry-lib/
  src/questfoundry/
    protocol/
      client.py              # Protocol client
      envelope.py            # Envelope builder/parser
      transport.py           # File, HTTP, event transports

    validation/
      schema.py              # Layer 3 schema validation
      conformance.py         # Layer 4 conformance tests

    lifecycles/
      hooks.py               # Hook state machine
      tu.py                  # TU state machine
      gates.py               # Gate lifecycle
      views.py               # View lifecycle

    artifacts/
      base.py                # Base artifact class
      hook_card.py           # Typed wrappers
      tu_brief.py
      canon_pack.py
      # ... all 17 artifacts

    state/
      store.py               # Abstract state store
      file_store.py          # File-based implementation
      sqlite_store.py        # SQLite project file

    providers/
      base.py                # Provider plugin interface
      text/
        openai.py            # OpenAI GPT models
        ollama.py            # Local Ollama models
        google.py            # Google Gemini
        bedrock.py           # Amazon Bedrock
      image/
        a1111.py             # Automatic1111 Stable Diffusion
        dalle.py             # OpenAI DALL-E
        imagen.py            # Google Imagen 4
      audio/
        elevenlabs.py        # ElevenLabs TTS
        # Future providers

    roles/
      session.py             # Role session management
      loader.py              # Load Layer 5 prompts
      executor.py            # Execute prompts with LLMs

    orchestration/
      showrunner.py          # Loop orchestration
      checkpoint.py          # Checkpoint management

    safety/
      pn_guard.py            # PN boundary enforcement
      spoiler_filter.py      # Strip spoilers from artifacts

    resources/
      prompts/               # Bundled Layer 5 prompts
      schemas/               # Bundled Layer 3 schemas
```

## Key Design Decisions

### State Persistence Strategy

**MVP: File-Based with SQLite Project Files**

```
workspace/
  my-adventure.qfproj       # SQLite file (Cold SoT)
  .questfoundry/
    config.yml              # LLM providers, role config
    hot/                    # File-based hot workspace
      hooks/
      canon/
      artifacts/
    cache/                  # LLM response cache
    sessions/               # Active role sessions
```

**Cold SoT (Curated Canon):**

- Single `.qfproj` SQLite file
- Contains: snapshots, views, canon artifacts, TU history
- Portable, efficient, ACID compliant

**Hot SoT (Work in Progress):**

- File-based directory structure
- Easy inspection/editing
- Git-friendly (optional export)

**Future: Redis/Valkey for distributed workflows**

### Provider Plugin Architecture

**Interface:**

```python
class Provider(ABC):
    @abstractmethod
    def generate_text(
        self,
        prompt: str,
        model: str,
        **kwargs
    ) -> str:
        pass

class ImageProvider(ABC):
    @abstractmethod
    def generate_image(
        self,
        prompt: str,
        model: str,
        **kwargs
    ) -> bytes:
        pass
```

**Configuration:**

```yaml
# .questfoundry/config.yml

# MVP: Unified provider
providers:
  text:
    default: openai
    openai:
      api_key: ${OPENAI_API_KEY}
      model: gpt-4o
    ollama:
      base_url: http://localhost:11434
      model: llama3
    google:
      api_key: ${GOOGLE_API_KEY}
      model: gemini-2.0-flash-exp
    bedrock:
      region: us-east-1
      model: anthropic.claude-3-sonnet

  image:
    default: dalle
    a1111:
      base_url: http://localhost:7860
      model: sd-xl
    dalle:
      api_key: ${OPENAI_API_KEY}
      model: dall-e-3
    imagen:
      api_key: ${GOOGLE_API_KEY}
      model: imagen-4

# Future: Per-role overrides
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

### Role Session Management

**Stateful Sessions During Active Loops:**

```python
class RoleSession:
    """Maintains conversation context for an active role."""

    role: str
    tu_context: str
    conversation_history: List[Envelope]
    active_since: datetime
    dormancy_signals: List[str]

    def send_message(self, envelope: Envelope) -> Envelope:
        """Send message and update conversation history."""
        pass

    def ask_human(self, question: str, **kwargs) -> str:
        """Request human input (interactive mode)."""
        # Creates human.question intent
        # Waits for human.response
        pass

    def archive(self) -> dict:
        """Archive session state for audit trail."""
        pass

class SessionManager:
    """Manages all active role sessions."""

    def wake_role(self, role: str, tu: str) -> RoleSession:
        """Create new session for role."""
        pass

    def dormant_role(self, role: str):
        """Archive and clear role session."""
        pass

    def get_active_roles(self) -> List[str]:
        """List currently active roles."""
        pass
```

**Session Lifetime:**

- Created when Showrunner wakes role
- Maintained during loop execution
- Archived when role goes dormant
- Linked to TU for traceability

### Protocol Client

**Simple API for Layer 4 Communication:**

```python
from questfoundry.protocol import ProtocolClient, Envelope

# Initialize client
client = ProtocolClient(workspace="./my-adventure.qfproj")

# Send message
envelope = Envelope(
    intent="hook.create",
    sender={"role": "SR", "agent": "human:alice"},
    receiver={"role": "LW"},
    context={"tu": "TU-2025-10-31-SR01"},
    payload={
        "type": "hook_card",
        "data": {...}
    }
)

response = client.send(envelope)

# Send and wait for response
response = client.send_and_wait(envelope, timeout=30)

# Receive messages
for message in client.receive():
    print(message.intent)
```

### Validation

**Schema Validation (Layer 3):**

```python
from questfoundry.validation import validate_artifact

# Validate artifact
result = validate_artifact(
    artifact_type="hook_card",
    data={...}
)

if not result.valid:
    for error in result.errors:
        print(error.message)
```

**Protocol Conformance (Layer 4):**

```python
from questfoundry.validation import validate_envelope

# Validate envelope
result = validate_envelope(envelope)

if not result.conformant:
    print(result.violations)
```

## Evolution Path

### Phase 1: Core Infrastructure (MVP)

- Protocol client with file transport
- File-based state store
- SQLite project files
- Schema validation
- Hook/TU state machines

### Phase 2: Provider Support

- OpenAI text provider
- Ollama text provider
- Basic prompt execution

### Phase 3: Role Execution

- Session management
- Prompt loader (Layer 5 integration)
- Agent-to-human callbacks
- Showrunner orchestration

### Phase 4: Asset Generation

- Image providers (A1111, DALL-E)
- Audio providers (ElevenLabs)
- Multi-modal artifact support

### Phase 5: Advanced Features

- Google AI Studio / Bedrock providers
- Imagen 4 image provider
- Per-role provider configuration
- Redis/Valkey state backend
- API transport (beyond file-based)

## Provider Roadmap

### Text Generation Providers

| Provider       | Status  | Priority |
| -------------- | ------- | -------- |
| OpenAI GPT     | Phase 2 | High     |
| Ollama (local) | Phase 2 | High     |
| Google Gemini  | Phase 5 | Medium   |
| Amazon Bedrock | Phase 5 | Medium   |

### Image Generation Providers

| Provider        | Status  | Priority |
| --------------- | ------- | -------- |
| Automatic1111   | Phase 4 | High     |
| OpenAI DALL-E   | Phase 4 | High     |
| Google Imagen 4 | Phase 5 | Medium   |

### Audio Generation Providers

| Provider   | Status  | Priority |
| ---------- | ------- | -------- |
| ElevenLabs | Phase 4 | Medium   |

## Testing Strategy

1. **Unit Tests:** Each component independently
2. **Integration Tests:** Protocol client + state store
3. **Provider Tests:** Mock and real provider calls
4. **Lifecycle Tests:** State machine transitions
5. **Conformance Tests:** Layer 4 protocol compliance
6. **End-to-End Tests:** Full loop execution with mock LLM

## Python Package Structure

```toml
# pyproject.toml
[project]
name = "questfoundry"
version = "0.1.0"
dependencies = [
    "pydantic>=2.0",
    "jsonschema>=4.0",
    "httpx>=0.25",
    "python-dotenv>=1.0",
]

[project.optional-dependencies]
openai = ["openai>=1.0"]
ollama = ["ollama>=0.1"]
google = ["google-generativeai>=0.3"]
bedrock = ["boto3>=1.34"]
all = ["questfoundry[openai,ollama,google,bedrock]"]

[project.entry-points.questfoundry_providers]
# Plugin discovery
```

## Distribution

**PyPI Package:**

```bash
pip install questfoundry

# With specific providers
pip install questfoundry[openai]
pip install questfoundry[all]
```

**Bundled Resources:**

- Layer 3 schemas (from spec repo)
- Layer 5 prompts (from spec repo)
- Default configuration templates

## Dependencies

- **Layer 3:** JSON schemas for validation
- **Layer 4:** Protocol specification
- **Layer 5:** Role prompts for execution

## Integration with Layer 7

Layer 7 (questfoundry-cli) will:

- Import `questfoundry` library
- Use protocol client for operations
- Provide UX wrapper around library functions
- Handle CLI-specific concerns (autocomplete, formatting)

## Next Steps

1. ⏸️ Create `pvliesdonk/questfoundry-lib` repository
2. ⏸️ Implement protocol client (Phase 1)
3. ⏸️ Implement file-based state store
4. ⏸️ Implement SQLite project file format
5. ⏸️ Add schema validation
6. ⏸️ Implement OpenAI provider (Phase 2)
7. ⏸️ Implement Ollama provider
8. ⏸️ Add session management (Phase 3)
9. ⏸️ Integrate Layer 5 prompts
10. ⏸️ Build Showrunner orchestration

## References

- [Layer 4 - Protocol](../04-protocol/README.md)
- [Layer 5 - Prompts](../05-prompts/README.md)
- [Layer 3 - Schemas](../03-schemas/README.md)
