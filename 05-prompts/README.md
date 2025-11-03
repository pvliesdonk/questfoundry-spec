# Layer 5 — Role Prompts (AI Agent Kits)

**Status:** 🚧 Planning Phase
**Last Updated:** 2025-10-31

## Overview

Layer 5 transforms Layer 1 role charters into executable AI agents that communicate via Layer 4 protocol and validate artifacts against Layer 3 schemas.

## Purpose

- Provide AI agent prompts that implement each of the 14 roles
- Enable human/AI interchangeability for roles
- Support stateful conversation sessions during active loops
- Implement agent-to-human question/answer in interactive mode
- Use Layer 4 protocol for all inter-role communication

## Design Principles

1. **Role Fidelity:** Prompts must faithfully implement Layer 1 charters
2. **Protocol Native:** All communication via Layer 4 envelopes
3. **Schema Compliant:** All artifacts validated against Layer 3 schemas
4. **Context Aware:** Maintain TU, snapshot, hot/cold awareness
5. **Safety First:** Enforce PN boundaries at agent level
6. **Stateful Sessions:** Conversation history during active loops
7. **Human Collaborative:** Agents can ask clarifying questions

## Repository Structure

```
05-prompts/
  README.md                    # This file
  DESIGN.md                    # Detailed design decisions

  _shared/
    context_management.md      # How to track TU, snapshot, hot/cold
    safety_protocol.md         # PN boundary enforcement
    escalation_rules.md        # When to wake Showrunner
    human_interaction.md       # Asking questions to human

  showrunner/
    system_prompt.md           # Main role prompt
    intent_handlers/           # Per-intent behavior
      tu.start.md
      role.wake.md
      loop.checkpoint.md
    examples/
      hook_harvest.json        # Example conversation

  gatekeeper/
    system_prompt.md
    quality_bars/              # Per-bar validation logic
      integrity.md
      reachability.md
      style.md
    intent_handlers/
      gate.execute.md
    examples/

  lore_weaver/
    system_prompt.md
    intent_handlers/
      hook.canonize.md
      canon.create.md
    examples/

  scene_smith/
  plotwright/
  codex_curator/
  style_lead/
  researcher/
  art_director/
  illustrator/
  audio_director/
  audio_producer/
  translator/
  book_binder/

  tests/
    test_prompts/              # Prompt validation tests
    fixtures/                  # Test scenarios
```

## Key Concepts

### Stateful Sessions

Agents maintain conversation history during active loops:

```python
class RoleSession:
    role: str
    tu_context: str
    conversation_history: List[Message]
    active_since: datetime

# Session lifetime = loop duration
# Showrunner manages wake (create) / dormancy (archive)
```

### Agent-to-Human Communication

In interactive mode, agents can ask clarifying questions:

```python
# Agent perspective (simple API)
tone = ask_human(
    question="This hook feels ambiguous. Horror or mystery tone?",
    context={"hook_id": "HOOK-001"},
    suggestions=["horror", "mystery", "both"]
)

# Implemented via Layer 4 protocol:
# - Agent sends: intent="human.question"
# - Showrunner routes to CLI
# - Human responds via CLI
# - Response returns as: intent="human.response"
```

### Context Management

Every agent maintains awareness of:

- Current TU
- Active snapshot (if any)
- Hot vs Cold state
- Recent artifacts in conversation
- Role dormancy signals

## Prompt Structure

Each role prompt includes:

1. **Role Charter** (from Layer 1)
2. **Mission & Scope**
3. **Protocol Integration**
   - How to receive/send Layer 4 envelopes
   - Intent routing
4. **Schema Validation**
   - Required artifact structure
   - Validation requirements
5. **Context Tracking**
   - TU awareness
   - Hot/Cold boundaries
6. **Safety Guidelines**
   - PN boundary enforcement
   - Spoiler hygiene
7. **Quality Bars** (role-specific)
8. **Human Interaction**
   - When to ask questions
   - How to phrase questions
9. **Dormancy Signals**
   - When to go dormant
   - How to signal Showrunner
10. **Example Conversations**
    - Typical message flows
    - Edge cases

## Implementation Modes

### Guided Mode (Default for MVP)

- Loop-by-loop checkpoints
- Author approves next loop before execution
- Agents run within approved loop
- Human reviews artifacts between loops

### Express Mode (Future)

- Fully autonomous execution
- Setup questions → complete manuscript
- Only stops for gatecheck failures

### Interactive Mode

- Agents ask clarifying questions inline
- Free-form human responses
- Conversational collaboration
- Available as `--interactive` flag

## Provider Support

Agents are provider-agnostic. Layer 6 handles:

- Text generation (OpenAI, Ollama, Google AI Studio, Amazon Bedrock)
- Image generation (A1111, DALL-E, Imagen 4)
- Audio generation (ElevenLabs, etc.)

Per-role provider configuration supported (future).

## Evolution Path

### Phase 1: Core Roles (MVP)

- Showrunner
- Gatekeeper
- Lore Weaver
- Scene Smith

### Phase 2: Content Roles

- Plotwright
- Codex Curator
- Style Lead

### Phase 3: Asset Roles

- Art Director
- Illustrator
- Audio Director
- Audio Producer

### Phase 4: Support Roles

- Researcher
- Translator
- Book Binder

## Testing Strategy

1. **Prompt Validation:** Verify prompts reference correct schemas/protocol
2. **Intent Coverage:** Each role handles required intents
3. **Protocol Compliance:** All messages conform to Layer 4
4. **Schema Compliance:** All artifacts validate against Layer 3
5. **Safety Checks:** PN boundaries enforced
6. **Conversation Tests:** Example flows execute correctly

## Dependencies

- **Layer 0:** Quality bars, loops, PN principles
- **Layer 1:** Role charters and missions
- **Layer 2:** Artifact structures and terminology
- **Layer 3:** JSON schemas for validation
- **Layer 4:** Protocol envelopes and intents

## Integration with Layer 6

Layer 6 (questfoundry-lib) will:

- Bundle these prompts as package resources
- Provide `get_prompt(role_name)` API
- Manage role sessions
- Handle LLM provider routing
- Implement agent-to-human callbacks

## Next Steps

1. ✅ Complete Layer 4 (protocol) → **DONE**
2. 🚧 Design shared prompt patterns (`_shared/`)
3. ⏸️ Implement Showrunner prompt (orchestrator)
4. ⏸️ Implement Gatekeeper prompt (quality enforcement)
5. ⏸️ Implement Lore Weaver prompt (canonization)
6. ⏸️ Implement Scene Smith prompt (prose generation)
7. ⏸️ Create example conversations
8. ⏸️ Test with Layer 6 implementation

## References

- [Layer 1 - Roles](../01-roles/README.md)
- [Layer 4 - Protocol](../04-protocol/README.md)
- [Targeted Loops](../00-north-star/LOOPS/README.md)
- [Quality Bars](../00-north-star/QUALITY_BARS.md)
