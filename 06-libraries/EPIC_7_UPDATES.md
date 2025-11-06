# Epic 7 Implementation Changes — Loop-Focused Architecture

**Document Version:** 1.0 (2025-11-06)
**Context:** Changes needed for Layer 6 Epic 7 based on commit 428140c and v0.2.0 validation enforcement

---

## Executive Summary

The original Epic 7 plan assumed a **role-focused architecture** where full role prompts were the primary executable units. Commit 428140c introduced a **loop-focused architecture** with dual usage modes (standalone and orchestration), and v0.2.0 added mandatory schema validation enforcement.

**Key Impact:** Epic 7 must now support **two distinct execution modes** with fundamentally different prompt loading and execution strategies.

---

## What Changed: commit 428140c + v0.2.0

### 1. Dual-Format Strategy (Two Usage Modes)

**Standalone Mode** (traditional):
- Full role prompts (200-300 lines each)
- Single role works independently
- Human-led workflows
- Context: ~200-300 lines per role

**Orchestration Mode** ⭐ (new, recommended):
- Loop playbooks (primary) + role adapters (thin interfaces)
- Showrunner coordinates multiple roles
- Multi-role workflows
- Context: ~500-1000 lines (1 playbook + 3-5 adapters + showrunner)
- **70% context reduction** vs standalone

### 2. New Artifacts

**Loop Playbooks** (`loops/*.playbook.md`) — 13 files:
- Complete procedures with message sequences
- RACI matrices
- Deliverables and success criteria
- Schema references
- **PRIMARY** executable units in orchestration mode

**Role Adapters** (`role_adapters/*.adapter.md`) — 15 files:
- Thin interface specs (50-100 lines)
- Core expertise (3-5 bullet points)
- Protocol intents handled
- Loop participation references
- Used in orchestration mode

**Modular Showrunner** (5 modules):
- `system_prompt.md` (110 lines) — Index
- `loop_orchestration.md` (100 lines) — Execute playbooks
- `manifest_management.md` (102 lines) — Hot/Cold operations
- `initialization.md` (223 lines) — Project setup
- `protocol_handlers.md` (230 lines) — Message handling

**Validation Enforcement** (v0.2.0):
- `_shared/validation_contract.md` — Mandatory validation requirements (file #1)
- `SCHEMA_INDEX.json` — Schema registry with SHA-256 hashes (file #2)
- All role prompts updated with validation sections
- All loop playbooks updated with validation checkpoints
- Gatekeeper enhanced with schema validation quality bar

### 3. Execution Model Change

**OLD (role-focused):**
```
Role Prompt (contains loop procedure) → LLM → Output
```

**NEW (loop-focused):**
```
Orchestration: Playbook (procedure) + Adapter (expertise) → LLM → Output
Standalone:    Full Prompt (procedure + expertise) → LLM → Output
```

---

## Impact Analysis: Original Epic 7 Features

### 7.1: Prompt Bundling

**Original Plan:**
```python
resources/
  prompts/
    _shared/
    showrunner/
    gatekeeper/
    [... all roles with system_prompt.md]
  prompt_loader.py  # load_prompt(role_name, component) -> str
```

**Problems:**
1. ❌ Assumes single prompt per role (no adapters, playbooks)
2. ❌ No concept of usage modes
3. ❌ Doesn't handle modular showrunner
4. ❌ Missing validation files
5. ❌ No playbook support

**Required Changes:**

```python
resources/
  prompts/
    # Validation enforcement (v0.2.0)
    _shared/
      validation_contract.md        # CRITICAL: File #1
    SCHEMA_INDEX.json               # CRITICAL: File #2

    # Shared patterns
    _shared/
      context_management.md
      safety_protocol.md
      escalation_rules.md
      human_interaction.md

    # Loop playbooks (orchestration mode)
    loops/
      *.playbook.md                 # 13 playbooks
      examples/
        *.json                      # Validation flows

    # Role adapters (orchestration mode)
    role_adapters/
      *.adapter.md                  # 15 adapters (50-100 lines each)

    # Full role prompts (standalone mode)
    showrunner/
      system_prompt.md              # Index
      loop_orchestration.md
      manifest_management.md
      initialization.md             # Optional (for init flow)
      protocol_handlers.md
    gatekeeper/
      system_prompt.md              # Full prompt (200-300 lines)
    plotwright/
      system_prompt.md
    [... all 15 roles]

  prompt_loader.py                  # NEW API (see below)
```

**New API:**

```python
from enum import Enum
from typing import Optional

class PromptMode(Enum):
    STANDALONE = "standalone"
    ORCHESTRATION = "orchestration"

class PromptLoader:
    def load_validation_contract(self) -> str:
        """Load validation contract (ALWAYS file #1)."""

    def load_schema_index(self) -> dict:
        """Load SCHEMA_INDEX.json (ALWAYS file #2)."""

    def load_shared_pattern(self, pattern: str) -> str:
        """Load shared pattern (context_management, safety_protocol, etc)."""

    # Standalone mode
    def load_role_prompt(self, role: str, module: Optional[str] = None) -> str:
        """Load full role prompt (standalone mode).

        Args:
            role: Role name (e.g., "plotwright", "showrunner")
            module: Optional module for modular roles (e.g., "loop_orchestration")

        Returns:
            Full role prompt content
        """

    # Orchestration mode
    def load_playbook(self, playbook: str) -> str:
        """Load loop playbook (orchestration mode).

        Args:
            playbook: Playbook name (e.g., "story_spark", "lore_deepening")

        Returns:
            Complete playbook with procedure
        """

    def load_adapter(self, role: str) -> str:
        """Load role adapter (orchestration mode).

        Args:
            role: Role name (e.g., "plotwright", "lore_weaver")

        Returns:
            Thin role adapter (50-100 lines)
        """

    def get_playbook_roles(self, playbook: str) -> list[str]:
        """Get roles involved in a playbook (from RACI matrix)."""

    def get_available_playbooks(self) -> list[str]:
        """Get all available loop playbooks."""

    def get_available_roles(self) -> list[str]:
        """Get all available roles."""
```

**Usage Examples:**

```python
# Standalone mode: Load full role prompt
loader = PromptLoader()
validation_contract = loader.load_validation_contract()  # ALWAYS FIRST
schema_index = loader.load_schema_index()               # ALWAYS SECOND
context_mgmt = loader.load_shared_pattern("context_management")
plotwright_prompt = loader.load_role_prompt("plotwright")

# Orchestration mode: Load playbook + adapters
validation_contract = loader.load_validation_contract()  # ALWAYS FIRST
schema_index = loader.load_schema_index()               # ALWAYS SECOND
playbook = loader.load_playbook("story_spark")
showrunner_adapter = loader.load_adapter("showrunner")
plotwright_adapter = loader.load_adapter("plotwright")
scene_smith_adapter = loader.load_adapter("scene_smith")
```

---

### 7.2: Role Session

**Original Plan:**
```python
class RoleSession:
    def __init__(self, role_name: str, tu_context: TUContext):
        # Maintains conversation history
        # Tracks TU context
        # Handles message send/receive
```

**Problems:**
1. ❌ No concept of standalone vs orchestration mode
2. ❌ Doesn't handle playbook context
3. ❌ Missing validation enforcement tracking

**Required Changes:**

```python
class RoleSession:
    def __init__(
        self,
        role_name: str,
        tu_context: TUContext,
        mode: PromptMode,
        playbook: Optional[str] = None  # NEW: For orchestration mode
    ):
        self.role_name = role_name
        self.tu_context = tu_context
        self.mode = mode
        self.playbook = playbook  # Which playbook this session is part of
        self.conversation_history: list[Message] = []
        self.validation_reports: dict[str, ValidationReport] = {}  # NEW: Track validation

    def get_context_size(self) -> int:
        """Estimate context size in tokens.

        Orchestration mode should be ~70% smaller than standalone.
        """

    def add_validation_report(self, artifact: str, report: ValidationReport):
        """Track validation reports for artifacts produced in this session.

        v0.2.0: Mandatory for all JSON artifacts.
        """

    def get_validation_status(self) -> dict[str, bool]:
        """Get validation status for all artifacts in session.

        Returns:
            {artifact_name: is_valid}
        """
```

---

### 7.3: Prompt Executor

**Original Plan:**
```python
class PromptExecutor:
    def execute(self, role: str, ...) -> Response:
        # Load prompt for role
        # Execute with LLM
        # Parse response
        # Validate output artifacts
```

**Problems:**
1. ❌ Assumes single prompt per role
2. ❌ Doesn't handle orchestration mode (playbook + adapters)
3. ❌ Missing validation enforcement (preflight, validation_report.json)

**Required Changes:**

```python
class PromptExecutor:
    def __init__(self, loader: PromptLoader, llm_client: LLMClient):
        self.loader = loader
        self.llm_client = llm_client

    def execute_standalone(
        self,
        role: str,
        message: str,
        session: RoleSession
    ) -> Response:
        """Execute in standalone mode: full role prompt.

        Steps:
        1. Load validation_contract.md (file #1)
        2. Load SCHEMA_INDEX.json (file #2)
        3. Load shared patterns
        4. Load full role prompt
        5. Prepend conversation history
        6. Execute with LLM
        7. Validate artifacts (check validation_report.json)
        8. Parse response
        """

    def execute_orchestration(
        self,
        playbook: str,
        role: str,
        step: str,
        message: str,
        session: RoleSession
    ) -> Response:
        """Execute in orchestration mode: playbook + adapter.

        Steps:
        1. Load validation_contract.md (file #1)
        2. Load SCHEMA_INDEX.json (file #2)
        3. Load shared patterns
        4. Load playbook (provides procedure context)
        5. Load role adapter (provides expertise)
        6. Load showrunner modules (if role is showrunner)
        7. Inject current step from playbook
        8. Prepend conversation history
        9. Execute with LLM
        10. Validate artifacts (check validation_report.json)
        11. Parse response

        Context: playbook (procedure) + adapter (expertise)
                 = ~70% smaller than full prompt
        """

    def validate_artifacts(self, response: Response, session: RoleSession) -> bool:
        """Validate all artifacts in response (v0.2.0).

        Checks:
        1. All JSON artifacts have validation_report.json
        2. validation_report.json shows "valid": true
        3. validation_report.json has empty "errors": []
        4. Artifacts have "$schema" field

        Returns:
            True if all artifacts valid, False otherwise
        """
```

---

### 7.4: Session Manager

**Original Plan:**
```python
class SessionManager:
    def wake_role(self, role: str, tu: TU) -> RoleSession:
        ...
    def dormant_role(self, role: str):
        ...
    def get_active_roles(self) -> list[str]:
        ...
```

**Problems:**
1. ❌ Doesn't distinguish between standalone and orchestration modes
2. ❌ Missing playbook context tracking

**Required Changes:**

```python
class SessionManager:
    def __init__(self):
        self.active_sessions: dict[str, RoleSession] = {}
        self.current_mode: Optional[PromptMode] = None
        self.current_playbook: Optional[str] = None

    def wake_role_standalone(self, role: str, tu: TU) -> RoleSession:
        """Wake role in standalone mode (full prompt)."""
        session = RoleSession(role, tu, PromptMode.STANDALONE)
        self.active_sessions[role] = session
        self.current_mode = PromptMode.STANDALONE
        return session

    def wake_role_orchestration(
        self,
        role: str,
        tu: TU,
        playbook: str
    ) -> RoleSession:
        """Wake role in orchestration mode (adapter).

        Args:
            role: Role to wake
            tu: Current TU
            playbook: Which playbook this role is participating in
        """
        session = RoleSession(role, tu, PromptMode.ORCHESTRATION, playbook)
        self.active_sessions[role] = session
        self.current_mode = PromptMode.ORCHESTRATION
        self.current_playbook = playbook
        return session

    def dormant_role(self, role: str):
        """Put role to dormant (remove session)."""
        if role in self.active_sessions:
            del self.active_sessions[role]

    def get_active_roles(self) -> list[str]:
        """Get all active role names."""
        return list(self.active_sessions.keys())

    def get_mode(self) -> Optional[PromptMode]:
        """Get current execution mode."""
        return self.current_mode

    def get_current_playbook(self) -> Optional[str]:
        """Get current playbook (orchestration mode only)."""
        return self.current_playbook

    def validate_all_sessions(self) -> dict[str, dict[str, bool]]:
        """Get validation status for all active sessions (v0.2.0).

        Returns:
            {role_name: {artifact_name: is_valid}}
        """
```

---

## New Feature Required: 7.5 Playbook Executor

**Not in original plan — must be added.**

```python
class PlaybookExecutor:
    """Execute loop playbooks in orchestration mode.

    This is the NEW primary execution unit for orchestration mode.
    Replaces the role-as-primary-unit model.
    """

    def __init__(
        self,
        loader: PromptLoader,
        session_manager: SessionManager,
        prompt_executor: PromptExecutor
    ):
        self.loader = loader
        self.session_manager = session_manager
        self.prompt_executor = prompt_executor

    def execute_playbook(
        self,
        playbook_name: str,
        tu: TU,
        interactive: bool = True
    ) -> PlaybookResult:
        """Execute a complete loop playbook.

        Steps:
        1. Load playbook (complete procedure)
        2. Parse RACI matrix to identify required roles
        3. Wake required roles (adapters)
        4. Execute message sequence from playbook:
           - For each step:
             - Identify responsible role
             - Execute via PromptExecutor.execute_orchestration()
             - Validate artifacts (check validation_report.json)
             - If validation fails: STOP playbook
             - If interactive: allow human review/intervention
        5. Collect all artifacts
        6. Validate all artifacts (Gatekeeper quality bar)
        7. Dormant roles when complete
        8. Return result

        Returns:
            PlaybookResult with artifacts, validation reports, checkpoints
        """

    def parse_raci_matrix(self, playbook_content: str) -> dict[str, list[str]]:
        """Parse RACI matrix from playbook to identify roles.

        Returns:
            {"responsible": [...], "accountable": [...], "consulted": [...]}
        """

    def execute_step(
        self,
        playbook: str,
        step_name: str,
        responsible_role: str,
        message: str,
        session: RoleSession
    ) -> StepResult:
        """Execute one step of playbook.

        Delegates to PromptExecutor.execute_orchestration()
        """

    def validate_playbook_artifacts(
        self,
        artifacts: list[Artifact],
        sessions: dict[str, RoleSession]
    ) -> ValidationSummary:
        """Validate all artifacts from playbook execution (v0.2.0).

        Checks (Gatekeeper quality bar):
        1. All artifacts have validation_report.json
        2. All validation_report.json show "valid": true
        3. All artifacts have "$schema" field

        Returns:
            Summary with pass/fail per artifact
        """

@dataclass
class PlaybookResult:
    playbook_name: str
    tu: TU
    artifacts: list[Artifact]
    validation_reports: dict[str, ValidationReport]
    validation_summary: ValidationSummary
    checkpoints: list[Checkpoint]
    success: bool
    error: Optional[str]
```

---

## Epic 8 Changes: Orchestration

**Original Epic 8:**
- 8.1: Loop Definitions (define 11 loops in code)
- 8.2: Checkpoint System
- 8.3: Showrunner Core

**Problems:**
1. ❌ "Define loop structures from Layer 0" — WRONG, loops now defined in Layer 5 playbooks
2. ❌ "11 targeted loops" — NOW 13 loop playbooks
3. ❌ Assumed loops would be coded — NOW loops are markdown playbooks

**Required Changes:**

Epic 8 becomes much simpler:

- **8.1: Loop Registry** — Map playbook names to files (trivial)
- **8.2: Checkpoint System** — Same as planned
- **8.3: Showrunner Core** — Use PlaybookExecutor (Epic 7.5)

```python
class Showrunner:
    def __init__(self, playbook_executor: PlaybookExecutor):
        self.playbook_executor = playbook_executor
        self.checkpoint_manager = CheckpointManager()

    def run_loop(
        self,
        loop_name: str,
        tu: Optional[TU] = None,
        interactive: bool = True
    ) -> LoopResult:
        """Run a loop playbook.

        Steps:
        1. Open or reuse TU
        2. Execute playbook via PlaybookExecutor
        3. Create checkpoint
        4. Return result
        """
        if not tu:
            tu = self.create_tu(loop_name)

        result = self.playbook_executor.execute_playbook(
            loop_name,
            tu,
            interactive
        )

        checkpoint = self.checkpoint_manager.create_checkpoint(
            loop_name,
            tu,
            result.artifacts,
            result.validation_summary
        )

        return LoopResult(
            loop=loop_name,
            tu=tu,
            result=result,
            checkpoint=checkpoint
        )
```

---

## Implementation Priority

**Recommended sequence:**

1. **Update 7.1 (Prompt Bundling)** — FIRST
   - Copy all new files from 05-prompts/
   - Implement new PromptLoader API
   - Support both modes

2. **Update 7.2 (Role Session)** — SECOND
   - Add mode support
   - Add playbook tracking
   - Add validation tracking

3. **Update 7.3 (Prompt Executor)** — THIRD
   - Implement execute_standalone()
   - Implement execute_orchestration()
   - Add validation enforcement

4. **Add 7.5 (Playbook Executor)** — FOURTH (NEW)
   - Core orchestration logic
   - Execute playbooks
   - Coordinate role adapters

5. **Update 7.4 (Session Manager)** — FIFTH
   - Add mode tracking
   - Distinguish wake_role_standalone vs wake_role_orchestration

6. **Update Epic 8** — SIXTH
   - Simplify using PlaybookExecutor
   - Implement Showrunner.run_loop()

---

## Testing Strategy

**Standalone Mode:**
```python
def test_standalone_execution():
    loader = PromptLoader()
    executor = PromptExecutor(loader, mock_llm)
    session_mgr = SessionManager()

    # Wake plotwright in standalone mode
    session = session_mgr.wake_role_standalone("plotwright", tu)

    # Execute with full prompt
    response = executor.execute_standalone(
        "plotwright",
        "Design a hub for the docking bay",
        session
    )

    assert response.valid
    assert session.get_validation_status()["hook_card.json"] == True
```

**Orchestration Mode:**
```python
def test_orchestration_execution():
    loader = PromptLoader()
    executor = PromptExecutor(loader, mock_llm)
    session_mgr = SessionManager()
    playbook_executor = PlaybookExecutor(loader, session_mgr, executor)

    # Execute Story Spark playbook
    result = playbook_executor.execute_playbook(
        "story_spark",
        tu,
        interactive=False
    )

    assert result.success
    assert result.validation_summary.all_valid
    assert "plotwright" in session_mgr.get_active_roles()
    assert session_mgr.get_mode() == PromptMode.ORCHESTRATION
```

---

## Context Size Comparison

**Standalone Mode (old approach):**
```
validation_contract.md       ~8KB
SCHEMA_INDEX.json           ~15KB
context_management.md        ~2KB
plotwright/system_prompt.md ~15KB (full prompt)
--------------------------------
Total: ~40KB (~10K tokens)
```

**Orchestration Mode (new approach):**
```
validation_contract.md           ~8KB
SCHEMA_INDEX.json               ~15KB
context_management.md            ~2KB
loops/story_spark.playbook.md    ~6KB  (procedure)
role_adapters/plotwright.adapter ~2KB  (expertise)
role_adapters/scene_smith.adapter ~2KB
role_adapters/showrunner.adapter  ~2KB
showrunner/loop_orchestration.md ~4KB
--------------------------------
Total: ~41KB (~10K tokens)

BUT: Reusable across all Story Spark participants
Plotwright standalone would be ~40KB total
Orchestration serves 3+ roles with same context
Effective per-role cost: ~13KB (~3K tokens) = 70% reduction
```

---

## Summary

**Epic 7 requires fundamental changes:**

1. ✅ Support two distinct execution modes
2. ✅ Load loop playbooks + role adapters (orchestration)
3. ✅ Load full role prompts (standalone)
4. ✅ Handle modular showrunner components
5. ✅ Implement validation enforcement (v0.2.0)
6. ✅ NEW: PlaybookExecutor for orchestration
7. ✅ Session tracking per mode
8. ✅ Context-aware execution

**Epic 8 becomes simpler:**
- Loops already defined in playbooks
- Showrunner just executes playbooks
- Checkpoint system as planned

**Benefits of new approach:**
- 70% context reduction in orchestration mode
- Single source of truth for loop procedures
- Role interchangeability
- Easier maintenance
- Better validation enforcement

---

## Next Steps

1. Review this document with team
2. Update Epic 7 tasks in IMPLEMENTATION_PLAN.md
3. Begin implementation with 7.1 (Prompt Bundling)
4. Add Epic 7.5 (Playbook Executor)
5. Update Epic 8 to use playbooks
