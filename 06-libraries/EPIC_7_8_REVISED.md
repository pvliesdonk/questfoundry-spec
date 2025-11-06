# Epic 7 & 8 Implementation — Revised Architecture

**Document Version:** 2.0 (2025-11-06)
**Supersedes:** EPIC_7_UPDATES.md v1.0
**Key Insight:** Playbooks are **specifications to code**, not documents to parse at runtime

---

## Executive Summary

**CRITICAL ARCHITECTURAL DECISION:**

Playbooks don't need to be parsed at runtime. Instead:
- **Playbooks = specifications** → Implement loop logic as **hardcoded Python classes**
- **Role adapters/prompts = expertise** → Load into **LLM for domain knowledge**

This is simpler, more maintainable, and more testable than dynamic playbook parsing.

---

## Architecture: Hardcoded Loops + LLM Expertise

### What Gets Coded (Deterministic Logic)

Implement in Python:
- Loop procedures (message sequences)
- RACI flow (who does what when)
- Validation checkpoints
- Error handling
- State transitions

**Source:** Loop playbooks serve as **specifications** for this code

### What Uses LLM (Domain Expertise)

Load into LLM:
- Role adapters (orchestration mode)
- Full role prompts (standalone mode)
- Shared patterns
- Validation contract + schema index

**Source:** Layer 5 prompt files loaded at runtime

### Example: Story Spark Loop

**Playbook (`loops/story_spark.playbook.md`):**
- Documents the procedure
- Specifies message sequences
- Defines RACI: Plotwright (R), Scene Smith (R), Style Lead (C), etc.

**Implementation (`src/questfoundry/loops/story_spark.py`):**

```python
class StorySparkLoop(Loop):
    """Story Spark loop implementation.

    Specification: 05-prompts/loops/story_spark.playbook.md
    """

    def get_required_roles(self) -> dict[str, RAciRole]:
        """Return RACI matrix from playbook spec."""
        return {
            "plotwright": RaciRole.RESPONSIBLE,
            "scene_smith": RaciRole.RESPONSIBLE,
            "style_lead": RaciRole.CONSULTED,
            "lore_weaver": RaciRole.CONSULTED,
            "gatekeeper": RaciRole.CONSULTED,
            "showrunner": RaciRole.ACCOUNTABLE,
        }

    async def step_1_topology_draft(self, ctx: LoopContext) -> StepResult:
        """Plotwright: Map current topology and propose changes.

        Spec: loops/story_spark.playbook.md - Step 1: Topology Draft
        """
        # Wake Plotwright with adapter (orchestration) or full prompt (standalone)
        plotwright = await ctx.wake_role("plotwright")

        # Execute step with LLM (LLM provides expertise)
        response = await plotwright.execute(
            message=self._build_step_1_message(ctx),
            validation_required=["topology_notes"]  # Markdown output
        )

        # Validation checkpoint (hardcoded logic)
        if not response.valid:
            return StepResult.failed(
                "Plotwright validation failed",
                errors=response.validation_errors
            )

        # Store artifacts for next step
        ctx.store_artifact("topology_notes", response.artifacts["topology_notes"])

        return StepResult.success(artifacts=response.artifacts)

    async def step_2_section_briefs(self, ctx: LoopContext) -> StepResult:
        """Plotwright: Create section briefs for affected sections.

        Spec: loops/story_spark.playbook.md - Step 2: Section Briefs
        """
        plotwright = ctx.get_active_role("plotwright")

        response = await plotwright.execute(
            message=self._build_step_2_message(ctx),
            validation_required=["section_briefs"]
        )

        if not response.valid:
            return StepResult.failed("Section brief validation failed")

        ctx.store_artifact("section_briefs", response.artifacts["section_briefs"])
        return StepResult.success(artifacts=response.artifacts)

    async def step_3_prose_pass(self, ctx: LoopContext) -> StepResult:
        """Scene Smith: Draft prose for sections.

        Spec: loops/story_spark.playbook.md - Step 3: Prose Pass
        """
        # Wake Scene Smith
        scene_smith = await ctx.wake_role("scene_smith")

        # Provide context from previous steps
        response = await scene_smith.execute(
            message=self._build_step_3_message(ctx),
            context={
                "topology_notes": ctx.get_artifact("topology_notes"),
                "section_briefs": ctx.get_artifact("section_briefs"),
            },
            validation_required=["scene_drafts"]
        )

        if not response.valid:
            return StepResult.failed("Scene draft validation failed")

        ctx.store_artifact("scene_drafts", response.artifacts["scene_drafts"])
        return StepResult.success(artifacts=response.artifacts)

    async def step_4_hook_generation(self, ctx: LoopContext) -> StepResult:
        """Plotwright & Scene Smith: Generate hooks.

        Spec: loops/story_spark.playbook.md - Step 4: Hook Generation
        """
        # Both roles contribute
        plotwright = ctx.get_active_role("plotwright")
        scene_smith = ctx.get_active_role("scene_smith")

        # Parallel execution (both can work independently)
        pw_response, ss_response = await asyncio.gather(
            plotwright.execute(
                message=self._build_step_4_pw_message(ctx),
                validation_required=["hook_card"]  # JSON with schema
            ),
            scene_smith.execute(
                message=self._build_step_4_ss_message(ctx),
                validation_required=["hook_card"]  # JSON with schema
            )
        )

        # Validation checkpoint (v0.2.0: check validation_report.json)
        if not pw_response.valid or not ss_response.valid:
            return StepResult.failed("Hook validation failed")

        # Combine hooks
        all_hooks = (
            pw_response.artifacts.get("hooks", []) +
            ss_response.artifacts.get("hooks", [])
        )

        ctx.store_artifact("hooks", all_hooks)
        return StepResult.success(artifacts={"hooks": all_hooks})

    async def step_5_style_check(self, ctx: LoopContext) -> StepResult:
        """Style Lead (consulted): Review tone and motifs.

        Spec: loops/story_spark.playbook.md - Step 5: Style Check
        """
        style_lead = await ctx.wake_role("style_lead")

        response = await style_lead.execute(
            message=self._build_step_5_message(ctx),
            context={
                "scene_drafts": ctx.get_artifact("scene_drafts"),
            },
            validation_required=["style_feedback"]
        )

        if not response.valid:
            return StepResult.failed("Style check validation failed")

        ctx.store_artifact("style_feedback", response.artifacts["style_feedback"])
        return StepResult.success(artifacts=response.artifacts)

    async def step_6_feasibility_check(self, ctx: LoopContext) -> StepResult:
        """Lore Weaver (consulted): Check canon feasibility.

        Spec: loops/story_spark.playbook.md - Step 6: Feasibility Check
        """
        lore_weaver = await ctx.wake_role("lore_weaver")

        response = await lore_weaver.execute(
            message=self._build_step_6_message(ctx),
            context={
                "topology_notes": ctx.get_artifact("topology_notes"),
                "scene_drafts": ctx.get_artifact("scene_drafts"),
            },
            validation_required=["feasibility_notes"]
        )

        if not response.valid:
            return StepResult.failed("Feasibility check validation failed")

        ctx.store_artifact("feasibility_notes", response.artifacts["feasibility_notes"])
        return StepResult.success(artifacts=response.artifacts)

    async def step_7_preview_gate(self, ctx: LoopContext) -> StepResult:
        """Gatekeeper (consulted): Preview gate for early issues.

        Spec: loops/story_spark.playbook.md - Step 7: Preview Gate
        """
        gatekeeper = await ctx.wake_role("gatekeeper")

        response = await gatekeeper.execute(
            message=self._build_step_7_message(ctx),
            context={
                "topology_notes": ctx.get_artifact("topology_notes"),
                "section_briefs": ctx.get_artifact("section_briefs"),
                "scene_drafts": ctx.get_artifact("scene_drafts"),
            },
            validation_required=["gatecheck_report"]  # JSON with schema
        )

        # Validation checkpoint (gatecheck_report must validate)
        if not response.valid:
            return StepResult.failed("Gatecheck report validation failed")

        gatecheck = response.artifacts["gatecheck_report"]

        # Check gate decision
        if gatecheck.get("decision") == "block":
            return StepResult.blocked(
                "Preview gate blocked",
                remediation=gatecheck.get("remediation", [])
            )

        ctx.store_artifact("gatecheck_report", gatecheck)
        return StepResult.success(artifacts=response.artifacts)

    async def step_8_triage_handoff(self, ctx: LoopContext) -> StepResult:
        """Handoff hooks to Hook Harvest loop.

        Spec: loops/story_spark.playbook.md - Step 8: Triage Hand-off
        """
        hooks = ctx.get_artifact("hooks")

        # Schedule next loop (handled by Showrunner)
        ctx.schedule_next_loop("hook_harvest", inputs={"hooks": hooks})

        return StepResult.success(
            artifacts={},
            next_loop="hook_harvest"
        )

    async def execute(self, ctx: LoopContext) -> LoopResult:
        """Execute complete Story Spark loop.

        This is the main entry point called by Showrunner.
        """
        try:
            # Open TU
            ctx.open_tu(loop_name="story_spark")

            # Execute steps in sequence (hardcoded flow)
            step_1 = await self.step_1_topology_draft(ctx)
            if not step_1.success:
                return LoopResult.failed(step_1.error)

            step_2 = await self.step_2_section_briefs(ctx)
            if not step_2.success:
                return LoopResult.failed(step_2.error)

            step_3 = await self.step_3_prose_pass(ctx)
            if not step_3.success:
                return LoopResult.failed(step_3.error)

            step_4 = await self.step_4_hook_generation(ctx)
            if not step_4.success:
                return LoopResult.failed(step_4.error)

            step_5 = await self.step_5_style_check(ctx)
            if not step_5.success:
                return LoopResult.failed(step_5.error)

            step_6 = await self.step_6_feasibility_check(ctx)
            if not step_6.success:
                return LoopResult.failed(step_6.error)

            step_7 = await self.step_7_preview_gate(ctx)
            if not step_7.success:
                if step_7.blocked:
                    return LoopResult.blocked(step_7.remediation)
                return LoopResult.failed(step_7.error)

            step_8 = await self.step_8_triage_handoff(ctx)

            # Collect all artifacts
            all_artifacts = ctx.get_all_artifacts()

            # Create checkpoint
            checkpoint = ctx.create_checkpoint(
                loop_name="story_spark",
                artifacts=all_artifacts,
                validation_summary=ctx.get_validation_summary()
            )

            # Dormant roles
            await ctx.dormant_all_roles()

            # Close TU
            ctx.close_tu(success=True)

            return LoopResult.success(
                loop="story_spark",
                artifacts=all_artifacts,
                checkpoint=checkpoint,
                next_loop=step_8.next_loop
            )

        except Exception as e:
            ctx.close_tu(success=False, error=str(e))
            return LoopResult.failed(str(e))
```

**Key Points:**

1. **Loop logic is hardcoded** — Message sequences, RACI flow, validation checkpoints
2. **LLM provides expertise** — Role adapters loaded at each `execute()` call
3. **Type safe** — Python typing, not string parsing
4. **Testable** — Mock LLM responses, test flow logic
5. **Maintainable** — Change loop logic by editing Python, not parsing markdown

---

## Revised Epic 7: Role Execution

### 7.1: Prompt Bundling ✅ (Keep as planned)

Still need to load prompts from resources:
- Validation contract + schema index
- Shared patterns
- Role adapters (orchestration mode)
- Full role prompts (standalone mode)
- Showrunner modules

**No change** — Prompts are still loaded into LLM, just not parsed for logic

```python
class PromptLoader:
    def load_validation_contract() -> str
    def load_schema_index() -> dict
    def load_role_adapter(role: str) -> str  # For orchestration
    def load_role_prompt(role: str) -> str   # For standalone
    def load_shared_pattern(name: str) -> str
```

---

### 7.2: Role Session ✅ (Keep as planned)

Still need session management:
- Track conversation history
- Track TU context
- Validation report tracking

**No change** — Sessions are orthogonal to loop execution

---

### 7.3: Prompt Executor ✅ (Keep as planned)

Still need to execute prompts with LLM:
- Load appropriate prompts (adapter vs full)
- Execute with LLM provider
- Parse response
- Validate artifacts

**No change** — Executor still invokes LLM with prompts

---

### 7.4: Role Interface ✅ (Simplified)

**Old plan:** SessionManager with wake/dormant
**New plan:** Role interface for loop execution

```python
class Role:
    """Represents a role in a loop.

    Handles prompt loading and LLM execution for a single role.
    """

    def __init__(
        self,
        role_name: str,
        mode: PromptMode,
        prompt_loader: PromptLoader,
        llm_client: LLMClient
    ):
        self.role_name = role_name
        self.mode = mode
        self.prompt_loader = prompt_loader
        self.llm_client = llm_client
        self.conversation_history: list[Message] = []

    async def execute(
        self,
        message: str,
        context: Optional[dict] = None,
        validation_required: Optional[list[str]] = None
    ) -> RoleResponse:
        """Execute role action with LLM.

        Args:
            message: Instruction/query for this step
            context: Artifacts from previous steps
            validation_required: List of expected artifacts to validate

        Returns:
            RoleResponse with artifacts and validation status
        """
        # Load appropriate prompt
        if self.mode == PromptMode.ORCHESTRATION:
            prompt = self._load_orchestration_prompt()
        else:
            prompt = self._load_standalone_prompt()

        # Build full message with context
        full_message = self._build_message(message, context)

        # Execute with LLM
        llm_response = await self.llm_client.chat(
            system=prompt,
            messages=self.conversation_history + [full_message]
        )

        # Parse response and extract artifacts
        artifacts = self._extract_artifacts(llm_response)

        # Validate artifacts (v0.2.0)
        validation = self._validate_artifacts(artifacts, validation_required)

        # Update conversation history
        self.conversation_history.append(full_message)
        self.conversation_history.append(llm_response)

        return RoleResponse(
            artifacts=artifacts,
            validation=validation,
            valid=validation.all_valid
        )

    def _load_orchestration_prompt(self) -> str:
        """Load prompts for orchestration mode."""
        parts = [
            self.prompt_loader.load_validation_contract(),  # File #1
            self.prompt_loader.load_schema_index(),         # File #2
            self.prompt_loader.load_shared_pattern("context_management"),
            self.prompt_loader.load_shared_pattern("safety_protocol"),
            self.prompt_loader.load_role_adapter(self.role_name),
        ]

        # Add showrunner modules if needed
        if self.role_name == "showrunner":
            parts.extend([
                self.prompt_loader.load_showrunner_module("system_prompt"),
                self.prompt_loader.load_showrunner_module("loop_orchestration"),
            ])

        return "\n\n---\n\n".join(parts)

    def _load_standalone_prompt(self) -> str:
        """Load prompts for standalone mode."""
        parts = [
            self.prompt_loader.load_validation_contract(),  # File #1
            self.prompt_loader.load_schema_index(),         # File #2
            self.prompt_loader.load_shared_pattern("context_management"),
            self.prompt_loader.load_shared_pattern("safety_protocol"),
            self.prompt_loader.load_role_prompt(self.role_name),
        ]
        return "\n\n---\n\n".join(parts)
```

---

### 7.5: Loop Context ✅ (New)

Need context management for loop execution:

```python
class LoopContext:
    """Context for executing a loop.

    Manages TU, artifacts, roles, validation.
    """

    def __init__(
        self,
        workspace: Workspace,
        prompt_loader: PromptLoader,
        llm_client: LLMClient,
        mode: PromptMode
    ):
        self.workspace = workspace
        self.prompt_loader = prompt_loader
        self.llm_client = llm_client
        self.mode = mode

        self.tu: Optional[TU] = None
        self.artifacts: dict[str, Any] = {}
        self.active_roles: dict[str, Role] = {}
        self.validation_reports: dict[str, ValidationReport] = {}

    def open_tu(self, loop_name: str):
        """Open TU for this loop."""
        self.tu = self.workspace.create_tu(loop_name)

    def close_tu(self, success: bool, error: Optional[str] = None):
        """Close TU."""
        self.workspace.close_tu(self.tu, success, error)

    async def wake_role(self, role_name: str) -> Role:
        """Wake a role (load prompts, create session)."""
        if role_name not in self.active_roles:
            role = Role(
                role_name=role_name,
                mode=self.mode,
                prompt_loader=self.prompt_loader,
                llm_client=self.llm_client
            )
            self.active_roles[role_name] = role

        return self.active_roles[role_name]

    def get_active_role(self, role_name: str) -> Role:
        """Get already-woken role."""
        return self.active_roles[role_name]

    async def dormant_role(self, role_name: str):
        """Put role to dormant."""
        if role_name in self.active_roles:
            del self.active_roles[role_name]

    async def dormant_all_roles(self):
        """Put all roles to dormant."""
        self.active_roles.clear()

    def store_artifact(self, name: str, artifact: Any):
        """Store artifact from step."""
        self.artifacts[name] = artifact

    def get_artifact(self, name: str) -> Any:
        """Get artifact from previous step."""
        return self.artifacts.get(name)

    def get_all_artifacts(self) -> dict[str, Any]:
        """Get all artifacts from loop."""
        return self.artifacts.copy()

    def schedule_next_loop(self, loop_name: str, inputs: dict):
        """Schedule next loop (handled by Showrunner)."""
        # This is a hint to Showrunner
        self.artifacts["__next_loop__"] = {
            "loop": loop_name,
            "inputs": inputs
        }

    def create_checkpoint(
        self,
        loop_name: str,
        artifacts: dict,
        validation_summary: ValidationSummary
    ) -> Checkpoint:
        """Create checkpoint after loop."""
        return self.workspace.create_checkpoint(
            tu=self.tu,
            loop=loop_name,
            artifacts=artifacts,
            validation=validation_summary
        )

    def get_validation_summary(self) -> ValidationSummary:
        """Get validation summary for all roles."""
        all_reports = []
        for role in self.active_roles.values():
            all_reports.extend(role.validation_reports)

        return ValidationSummary.from_reports(all_reports)
```

---

## Revised Epic 8: Orchestration

Epic 8 becomes: **Implement all 13 loops as hardcoded Python classes**

### 8.1: Loop Base Class ✅

```python
from abc import ABC, abstractmethod
from enum import Enum

class RaciRole(Enum):
    RESPONSIBLE = "R"
    ACCOUNTABLE = "A"
    CONSULTED = "C"
    INFORMED = "I"

class Loop(ABC):
    """Base class for all loop implementations.

    Each loop playbook from 05-prompts/loops/ is implemented as a
    subclass with hardcoded step logic.
    """

    @abstractmethod
    def get_required_roles(self) -> dict[str, RaciRole]:
        """Return RACI matrix for this loop."""
        pass

    @abstractmethod
    async def execute(self, ctx: LoopContext) -> LoopResult:
        """Execute the complete loop."""
        pass

    def get_playbook_spec(self) -> str:
        """Return path to playbook specification."""
        return f"05-prompts/loops/{self.__class__.__name__.lower()}.playbook.md"
```

---

### 8.2: Implement All 13 Loops ✅

**Tasks:**

1. **Story Spark** (`loops/story_spark.py`) — See example above
2. **Hook Harvest** (`loops/hook_harvest.py`)
3. **Lore Deepening** (`loops/lore_deepening.py`)
4. **Codex Expansion** (`loops/codex_expansion.py`)
5. **Style Tune-up** (`loops/style_tune_up.py`)
6. **Gatecheck** (`loops/gatecheck.py`)
7. **Binding Run** (`loops/binding_run.py`)
8. **Narration Dry-Run** (`loops/narration_dry_run.py`)
9. **Art Touch-up** (`loops/art_touch_up.py`)
10. **Audio Pass** (`loops/audio_pass.py`)
11. **Translation Pass** (`loops/translation_pass.py`)
12. **Post-Mortem** (`loops/post_mortem.py`)
13. **Archive Snapshot** (`loops/archive_snapshot.py`)

**For each loop:**
- Extend `Loop` base class
- Implement `get_required_roles()` from RACI matrix
- Implement step methods (one per playbook step)
- Implement `execute()` to orchestrate steps
- Handle validation checkpoints (v0.2.0)
- Handle error cases

**Playbooks serve as specifications** — Read the playbook markdown, code the logic

---

### 8.3: Loop Registry ✅

```python
class LoopRegistry:
    """Registry of all available loops."""

    def __init__(self):
        self._loops: dict[str, type[Loop]] = {
            "story_spark": StorySparkLoop,
            "hook_harvest": HookHarvestLoop,
            "lore_deepening": LoreDeepeningLoop,
            "codex_expansion": CodexExpansionLoop,
            "style_tune_up": StyleTuneUpLoop,
            "gatecheck": GatecheckLoop,
            "binding_run": BindingRunLoop,
            "narration_dry_run": NarrationDryRunLoop,
            "art_touch_up": ArtTouchUpLoop,
            "audio_pass": AudioPassLoop,
            "translation_pass": TranslationPassLoop,
            "post_mortem": PostMortemLoop,
            "archive_snapshot": ArchiveSnapshotLoop,
        }

    def get_loop(self, loop_name: str) -> type[Loop]:
        """Get loop class by name."""
        if loop_name not in self._loops:
            raise ValueError(f"Unknown loop: {loop_name}")
        return self._loops[loop_name]

    def get_available_loops(self) -> list[str]:
        """Get all available loop names."""
        return list(self._loops.keys())
```

---

### 8.4: Showrunner ✅ (Simplified)

```python
class Showrunner:
    """Executes loops via hardcoded Loop classes."""

    def __init__(
        self,
        workspace: Workspace,
        prompt_loader: PromptLoader,
        llm_client: LLMClient,
        mode: PromptMode = PromptMode.ORCHESTRATION
    ):
        self.workspace = workspace
        self.prompt_loader = prompt_loader
        self.llm_client = llm_client
        self.mode = mode
        self.loop_registry = LoopRegistry()

    async def run_loop(
        self,
        loop_name: str,
        interactive: bool = True
    ) -> LoopResult:
        """Execute a loop.

        Args:
            loop_name: Name of loop to execute
            interactive: Allow human intervention during loop

        Returns:
            LoopResult with artifacts and validation
        """
        # Get loop implementation
        loop_class = self.loop_registry.get_loop(loop_name)
        loop = loop_class()

        # Create context
        ctx = LoopContext(
            workspace=self.workspace,
            prompt_loader=self.prompt_loader,
            llm_client=self.llm_client,
            mode=self.mode
        )

        # Execute loop (hardcoded logic)
        result = await loop.execute(ctx)

        return result
```

**That's it!** Much simpler than dynamic playbook parsing.

---

## Comparison: Old vs New Approach

### Old Approach (EPIC_7_UPDATES.md v1.0)

```python
# Parse playbook at runtime
playbook_content = loader.load_playbook("story_spark")
raci_matrix = parse_raci_matrix(playbook_content)
steps = parse_procedure(playbook_content)

# Execute dynamically
for step in steps:
    responsible_role = raci_matrix.get_responsible(step.name)
    await executor.execute_step(playbook, step, responsible_role, ...)
```

**Problems:**
- Complex playbook parsing
- Error-prone string manipulation
- Hard to debug
- No type safety
- Hard to test

### New Approach (This Document)

```python
# Loop implementation (hardcoded from playbook spec)
class StorySparkLoop(Loop):
    async def execute(self, ctx: LoopContext) -> LoopResult:
        step_1 = await self.step_1_topology_draft(ctx)
        step_2 = await self.step_2_section_briefs(ctx)
        # ... hardcoded flow
        return LoopResult.success(...)

# Execute
loop = StorySparkLoop()
result = await loop.execute(ctx)
```

**Benefits:**
- Simple, explicit code
- Type safe (Python typing)
- Easy to debug
- Easy to test (mock role responses)
- Clear control flow
- Better error handling

---

## What Changed from v1.0

### Removed / Simplified

❌ **Remove:** PlaybookExecutor.parse_raci_matrix()
❌ **Remove:** PlaybookExecutor.execute_step()
❌ **Remove:** Dynamic playbook parsing
❌ **Remove:** Complex step execution logic

✅ **Simplify:** Loops are classes, not parsed documents
✅ **Simplify:** Showrunner just instantiates loop classes
✅ **Simplify:** No runtime playbook interpretation

### Added

✅ **Add:** Loop base class
✅ **Add:** 13 loop implementations (one per playbook)
✅ **Add:** LoopContext for execution state
✅ **Add:** LoopRegistry for loop discovery

### Unchanged

✅ **Keep:** Prompt loading (adapters, full prompts)
✅ **Keep:** Role execution with LLM
✅ **Keep:** Validation enforcement (v0.2.0)
✅ **Keep:** Session management
✅ **Keep:** Dual mode support (standalone vs orchestration)

---

## Implementation Priority (Updated)

1. **Epic 7.1**: Prompt Bundling — Load prompts (unchanged)
2. **Epic 7.2**: Role Session — Session management (unchanged)
3. **Epic 7.3**: Prompt Executor — Execute with LLM (unchanged)
4. **Epic 7.4**: Role Interface — Simplified role interface
5. **Epic 7.5**: Loop Context — Context management
6. **Epic 8.1**: Loop Base Class — Abstract base
7. **Epic 8.2**: Implement Loops — Code all 13 loops from playbook specs
8. **Epic 8.3**: Loop Registry — Registry for discovery
9. **Epic 8.4**: Showrunner — Simplified loop runner

---

## Testing Strategy (Updated)

**Unit Tests: Loop Logic**

```python
@pytest.mark.asyncio
async def test_story_spark_step_1():
    """Test step 1: Topology Draft."""
    # Mock role
    mock_plotwright = Mock(spec=Role)
    mock_plotwright.execute.return_value = RoleResponse(
        artifacts={"topology_notes": "Hub topology draft..."},
        validation=ValidationSummary(all_valid=True),
        valid=True
    )

    # Context
    ctx = LoopContext(...)
    ctx.active_roles["plotwright"] = mock_plotwright

    # Execute step
    loop = StorySparkLoop()
    result = await loop.step_1_topology_draft(ctx)

    # Assertions
    assert result.success
    assert "topology_notes" in ctx.artifacts
    mock_plotwright.execute.assert_called_once()
```

**Integration Tests: Full Loop**

```python
@pytest.mark.asyncio
async def test_story_spark_full_loop():
    """Test complete Story Spark loop."""
    # Mock LLM client
    mock_llm = MockLLMClient()
    mock_llm.add_response("plotwright", "topology", {...})
    mock_llm.add_response("plotwright", "briefs", {...})
    # ...

    # Execute loop
    showrunner = Showrunner(workspace, prompt_loader, mock_llm)
    result = await showrunner.run_loop("story_spark")

    # Assertions
    assert result.success
    assert "topology_notes" in result.artifacts
    assert "scene_drafts" in result.artifacts
    assert result.validation_summary.all_valid
```

---

## Benefits of Hardcoded Approach

1. **Simplicity** — No parsing, just Python code
2. **Type Safety** — Full Python typing, catch errors at dev time
3. **Debuggability** — Set breakpoints, step through logic
4. **Testability** — Mock role responses, test control flow
5. **Maintainability** — Change loop logic by editing code
6. **Performance** — No runtime parsing overhead
7. **Clear** — Code is documentation

**Playbooks remain authoritative specifications** — Implementation must match playbook

---

## Migration from EPIC_7_UPDATES.md v1.0

If you've already started implementing based on v1.0:

1. **Keep:** Prompt loading (7.1)
2. **Keep:** Role session (7.2)
3. **Keep:** Prompt executor (7.3)
4. **Simplify:** Remove PlaybookExecutor parsing logic
5. **Add:** Loop base class and implementations (Epic 8.2)
6. **Simplify:** Showrunner just runs loop classes

---

## Summary

**Key Decision:** Playbooks are **specifications**, not runtime documents.

**Implementation:**
- Code loop logic as Python classes (one per playbook)
- Load role prompts into LLM for expertise
- Hardcoded flow = simple, testable, maintainable

**Result:**
- Epic 7: Simpler (no playbook parsing)
- Epic 8: Straightforward (code 13 loops from specs)
- Better DX: Type safety, debugging, testing

**Playbooks serve as:**
- Specifications for loop implementations
- Documentation for users
- Validation references (message sequences, RACI)

**This is the recommended approach for Layer 6 implementation.**
