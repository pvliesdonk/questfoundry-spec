# Epic 7 & 8 Implementation — Revised Architecture

**Document Version:** 2.1 (2025-11-06)
**Supersedes:** EPIC_7_UPDATES.md v1.0, EPIC_7_8_REVISED.md v2.0
**Key Insight:** Hybrid architecture - **hardcoded loop structure** + **LLM-backed agents & Showrunner**

---

## Executive Summary

**CRITICAL ARCHITECTURAL DECISION:**

This is a **hybrid architecture** combining structure with intelligence:
- **Loop structure = hardcoded** → Implement loop procedures as **Python classes** (from playbook specs)
- **Role agents = LLM-backed** → Agents provide domain expertise and make decisions
- **Showrunner = LLM-backed orchestrator** → Makes strategic decisions on role waking and collaboration
- **Playbooks = recommendations** → Showrunner usually follows them but can adapt to context

**Key Insights:**
1. **Playbooks don't need to be parsed at runtime** — Instead: Playbooks specify structure (what gets coded) + Prompts provide expertise (what LLM decides)
2. **Showrunner controls execution** — Which agents to wake, when to allow collaboration, when loop stabilizes
3. **Two-tier context architecture** — Showrunner knows lightweight registry of all loops (strategic) but only detailed context for current loop (tactical)

**Major Benefits:**
- **Bounded flexibility:** Hardcoded loop structure ensures quality bars are met, while LLM-backed agents and Showrunner adapt execution to context
- **Context efficiency:** ~97% reduction vs Layer 5 LLM-only approach (600 lines vs 10,000 lines per execution)
- **Modularity:** Add new loops without changing Showrunner prompt; agents don't need to know all playbooks

---

## Architecture: Hardcoded Loops + LLM-Backed Agents + Intelligent Orchestration

### What Gets Coded (Deterministic Structure)

Implement in Python:
- **Loop procedures** — Step sequences (step_1, step_2, ..., step_8)
- **RACI recommendations** — Playbook-recommended role assignments per step
- **Validation checkpoints** — Schema validation after each artifact generation
- **Error handling** — Failed validation, blocked gates, exceptions
- **State transitions** — TU lifecycle, artifact storage, checkpointing

**Source:** Loop playbooks serve as **specifications** for this code

### What Uses LLM (Intelligent Decisions)

**1. Role Agents (Domain Expertise)**

Each agent is LLM-backed and loaded with:
- Role adapter (orchestration mode) OR full prompt (standalone mode)
- Shared patterns
- Validation contract + schema index

Agents:
- Execute assigned tasks (draft topology, write prose, etc.)
- Can **suggest collaborators** when they need help
- Produce artifacts validated against schemas

**2. Showrunner (Strategic Orchestration)**

The Showrunner is also LLM-backed and makes strategic decisions:
- **Which role to wake** for each step (playbook recommends, Showrunner decides)
- **Whether to approve collaboration** when agents suggest additional roles
- **Which loop to run next** based on checkpoint review
- **When to ask human for guidance** in interactive mode

**Source:** All prompts loaded from Layer 5 at runtime

---

## Two-Tier Context Architecture

A key advantage of hardcoded loops over Layer 5's LLM-only approach is **context efficiency**. The Showrunner doesn't need to know all 13 playbooks in detail—just enough to make strategic decisions.

### Tier 1: Loop Registry (Strategic - Lightweight)

**Purpose:** Enable Showrunner to select the next loop without loading full playbooks.

**What Showrunner knows about all loops:**

```python
# Auto-generated from Loop subclasses
LOOP_REGISTRY = {
    "story_spark": {
        "purpose": "Develop new story beats and plot progression",
        "typical_inputs": ["existing canon", "hook cards"],
        "typical_outputs": ["scene drafts", "topology notes", "new hooks"],
        "scope": "Plot and narrative structure (no style/art changes)",
        "often_follows": ["hook_harvest"],
        "often_precedes": ["canon_weaving", "hook_harvest"]
    },
    "hook_harvest": {
        "purpose": "Evaluate and triage proposed hooks",
        "typical_inputs": ["hook cards"],
        "typical_outputs": ["accepted hooks", "canon packs"],
        "scope": "Hook evaluation and prioritization",
        "often_follows": ["story_spark", "lore_deepening"],
        "often_precedes": ["canon_weaving"]
    },
    "style_tune_up": {
        "purpose": "Refine tone, voice, and stylistic consistency",
        "typical_inputs": ["existing prose", "style guide"],
        "typical_outputs": ["revised prose", "style addendums"],
        "scope": "Style and tone only (no plot changes)",
        "often_follows": ["canon_weaving"],
        "often_precedes": ["art_touch_up"]
    },
    "art_touch_up": {
        "purpose": "Polish visual assets for scenes",
        "typical_inputs": ["scene descriptions", "art prompts"],
        "typical_outputs": ["images", "visual descriptions"],
        "scope": "Visual assets only (no plot/prose changes)",
        "often_follows": ["style_tune_up"],
        "often_precedes": ["final_review"]
    },
    # ... all 13 loops (just ~6-7 lines each = ~90 lines total)
}
```

**Size:** ~90 lines for all 13 loops

**Used for:**
- "Story Spark just completed. What loop should run next?"
- "We have hook cards in the TU. Which loop can process them?"
- "Is Style Tune Up an appropriate follow-up to Canon Weaving?"

**Loaded:** Once at Showrunner initialization, kept in memory

### Tier 2: Active Loop Context (Tactical - Detailed)

**Purpose:** Enable Showrunner to orchestrate the currently executing loop.

**What Showrunner knows about the CURRENT loop:**

```python
class StorySparkLoop(Loop):
    """Story Spark loop implementation."""

    # Registry metadata (Tier 1)
    name = "story_spark"
    purpose = "Develop new story beats and plot progression"
    typical_inputs = ["existing canon", "hook cards"]
    typical_outputs = ["scene drafts", "topology notes", "new hooks"]
    scope = "Plot and narrative structure (no style/art changes)"
    often_follows = ["hook_harvest"]
    often_precedes = ["canon_weaving", "hook_harvest"]

    def get_execution_context(self) -> dict:
        """Detailed context for orchestrating THIS loop.

        Only loaded when this loop is actively executing.
        """
        return {
            "goal": "Develop new story beats and plot progression",

            "available_steps": {
                "step_1_topology_draft": {
                    "description": "Map current topology and propose changes",
                    "playbook_recommends": "plotwright",
                    "produces": ["topology_notes"],
                    "can_iterate": True
                },
                "step_2_section_briefs": {
                    "description": "Create briefs for affected sections",
                    "playbook_recommends": "plotwright",
                    "produces": ["section_briefs"],
                    "requires": ["topology_notes"],
                    "can_iterate": True
                },
                "step_3_prose_pass": {
                    "description": "Draft prose for sections",
                    "playbook_recommends": "scene_smith",
                    "produces": ["scene_drafts"],
                    "requires": ["topology_notes", "section_briefs"],
                    "can_iterate": True
                },
                # ... all 8 steps with full details
            },

            "scope_constraints": {
                "can": [
                    "Draft topology and story structure",
                    "Write new scenes and prose",
                    "Generate hook cards for new beats",
                    "Check canon feasibility with Lore Weaver"
                ],
                "cannot": [
                    "Update style guide or change tone",
                    "Generate visual art or images",
                    "Produce audio assets",
                    "Directly modify canon (must go through Canon Weaving)"
                ]
            },

            "stabilization_criteria": {
                "required_steps": ["step_1", "step_2", "step_3", "step_7", "step_8"],
                "all_artifacts_valid": True,
                "gatekeeper_approved": True,
                "no_pending_revisions": True
            },

            "typical_flow": [
                "step_1", "step_2", "step_3", "step_4",
                "step_5", "step_6", "step_7", "step_8"
            ]
        }
```

**Size:** ~500 lines (detailed step descriptions, constraints, criteria)

**Used for:**
- "Which step should run next?"
- "Can Plotwright revise topology based on Gatekeeper feedback?"
- "Is this loop stable and ready to complete?"
- "What artifacts must be present for completion?"

**Loaded:** Only when this loop is actively executing, unloaded when loop completes

### Context Size Comparison

**Layer 5 Approach (LLM-only Showrunner):**
```
Showrunner LLM Context:
  - Showrunner system prompt: ~500 lines
  - All 13 loop playbooks: 13 × 500 lines = 6,500 lines
  - All role adapters (orchestration): 15 × 200 lines = 3,000 lines
  - Validation contract + schema index: 300 lines
  ---------------------------------------------------
  TOTAL: ~10,300 lines PER EXECUTION
```

**Layer 6 Approach (Hardcoded loops + two-tier context):**
```
Showrunner LLM Context:
  - Showrunner system prompt: ~500 lines
  - Loop registry (all 13 loops): ~90 lines [TIER 1]
  - Active loop execution context: ~500 lines [TIER 2]
  - Validation contract + schema index: 300 lines
  ---------------------------------------------------
  TOTAL: ~1,390 lines per execution (strategic decisions)
         ~600 lines per execution (tactical decisions)
```

**Context Reduction:** ~97% for strategic decisions, ~94% for tactical decisions

### Auto-Generation of Loop Registry

The Loop Registry is automatically generated from Loop subclasses, ensuring it's always in sync:

```python
class Loop(ABC):
    """Base class for all loops."""

    # Registry metadata (defined in each subclass)
    name: str
    purpose: str
    typical_inputs: list[str]
    typical_outputs: list[str]
    scope: str
    often_follows: list[str]
    often_precedes: list[str]

    @classmethod
    def get_registry_metadata(cls) -> dict:
        """Extract registry metadata for Tier 1 context."""
        return {
            "purpose": cls.purpose,
            "typical_inputs": cls.typical_inputs,
            "typical_outputs": cls.typical_outputs,
            "scope": cls.scope,
            "often_follows": cls.often_follows,
            "often_precedes": cls.often_precedes
        }

    @abstractmethod
    def get_execution_context(self) -> dict:
        """Get detailed execution context for Tier 2."""
        pass


class LoopRegistry:
    """Registry of all available loops."""

    def __init__(self):
        """Auto-discover all Loop subclasses."""
        self.loops = {
            cls.name: cls.get_registry_metadata()
            for cls in Loop.__subclasses__()
        }

    def get_context_for_showrunner(self) -> str:
        """Format registry for Showrunner LLM (Tier 1 context)."""
        return yaml.dump(self.loops, sort_keys=True)

    def get_loop(self, loop_name: str) -> Loop:
        """Get loop instance for execution."""
        for cls in Loop.__subclasses__():
            if cls.name == loop_name:
                return cls()
        raise ValueError(f"Loop not found: {loop_name}")


# Usage in Showrunner
class Showrunner:
    def __init__(self):
        self.registry = LoopRegistry()
        self.llm = LLMClient()

        # Load Tier 1 context once
        self.tier1_context = self.registry.get_context_for_showrunner()

    async def decide_next_loop(self, tu_context: dict) -> str:
        """Strategic decision: which loop to run next?"""
        response = await self.llm.chat(
            system=self.showrunner_prompt,
            context=self.tier1_context,  # Just registry (~90 lines)
            user=f"TU completed. Available artifacts: {tu_context['artifacts']}. What loop next?"
        )
        return response.suggested_loop

    async def orchestrate_loop(self, loop_name: str, ctx: LoopContext):
        """Tactical orchestration: run the loop."""
        loop = self.registry.get_loop(loop_name)

        # Load Tier 2 context for THIS loop only
        tier2_context = loop.get_execution_context()

        while not await self.is_loop_stable(loop, ctx, tier2_context):
            next_step = await self.decide_next_step(loop, ctx, tier2_context)
            await loop.execute_step(next_step, ctx)
```

**Key Benefits:**

1. **No manual maintenance:** Registry updates automatically when loops added
2. **Always in sync:** Registry metadata comes from Loop class definitions
3. **Type safe:** Python classes enforce structure
4. **Extensible:** Custom loops work seamlessly

### Advantages Over Layer 5

| Aspect | Layer 5 (LLM-only) | Layer 6 (Two-tier) |
|--------|-------------------|-------------------|
| **Context per execution** | ~10,000 lines | ~600-1,400 lines |
| **Showrunner needs to know** | All 13 playbooks in detail | Registry + active loop only |
| **Adding new loop** | Update Showrunner prompt | Add Loop subclass (auto-discovered) |
| **Agent context** | Must understand all loops | Only receives task for current step |
| **Modularity** | Monolithic (all or nothing) | Modular (loops independent) |
| **Testing** | Hard (LLM interprets playbooks) | Easy (mock Showrunner decisions) |

### Example: Showrunner Deciding Next Loop

**After Story Spark completes:**

```python
# Showrunner LLM receives (Tier 1 context only):
"""
You are the Showrunner. A Story Spark loop just completed.

Current TU artifacts:
  - topology_notes (markdown)
  - section_briefs (markdown)
  - scene_drafts (markdown)
  - hooks (12 hook cards, JSON)
  - gatecheck_report (passed)

Available loops:
  story_spark: Develop new story beats (often_precedes: canon_weaving, hook_harvest)
  hook_harvest: Evaluate hooks (typical_inputs: hook cards)
  canon_weaving: Weave changes into canon (typical_inputs: accepted hooks, scene drafts)
  style_tune_up: Refine tone (scope: style only, no plot)
  lore_deepening: Expand worldbuilding
  ... [rest of registry]

What loop should run next?
"""

# Showrunner responds:
"""
Suggested loop: hook_harvest

Reasoning:
- Story Spark produced 12 hook cards
- hook_harvest.typical_inputs includes "hook cards"
- story_spark.often_precedes includes "hook_harvest"
- Need to triage hooks before weaving into canon
"""
```

**Total context:** ~600 lines (no playbook details needed!)

**Compare to Layer 5:** Would need all 13 playbooks (~6,500 lines) to make same decision

---

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
        """Step 1: Topology Draft (Playbook recommends Plotwright).

        Spec: loops/story_spark.playbook.md - Step 1: Topology Draft
        """
        # Playbook recommends Plotwright, but Showrunner decides
        agent = await ctx.request_role_for_step(
            step="step_1_topology_draft",
            playbook_recommends="plotwright",
            reason="Map current topology and propose story changes"
        )
        # Showrunner LLM evaluates: context, previous results, recommendations
        # Usually follows playbook, but might choose different role if context suggests it

        # Execute step with chosen agent (LLM provides expertise)
        response = await agent.execute(
            message=self._build_step_1_message(ctx),
            validation_required=["topology_notes"]  # Markdown output
        )

        # Agent might suggest collaboration (Showrunner must approve)
        if response.suggests_collaboration:
            for suggested_role in response.suggested_roles:
                # Showrunner LLM decides whether to wake additional agent
                collaborator = await ctx.request_collaboration(
                    current_agent=agent.role,
                    suggested_role=suggested_role,
                    reason=response.collaboration_reason
                )
                if collaborator:
                    # Approved - let collaborator contribute
                    collab_response = await collaborator.execute(
                        message=self._build_collaboration_message(ctx, suggested_role),
                        validation_required=["topology_notes"]
                    )
                    # Merge contributions
                    response.merge_artifacts(collab_response)

        # Validation checkpoint (hardcoded logic)
        if not response.valid:
            return StepResult.failed(
                "Topology draft validation failed",
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

    async def execute_step(self, step_name: str, ctx: LoopContext) -> StepResult:
        """Execute a specific step by name.

        Called by Showrunner when it decides which step to run next.
        """
        step_methods = {
            "step_1_topology_draft": self.step_1_topology_draft,
            "step_2_section_briefs": self.step_2_section_briefs,
            "step_3_prose_pass": self.step_3_prose_pass,
            "step_4_hook_generation": self.step_4_hook_generation,
            "step_5_style_check": self.step_5_style_check,
            "step_6_feasibility_check": self.step_6_feasibility_check,
            "step_7_preview_gate": self.step_7_preview_gate,
            "step_8_triage_handoff": self.step_8_triage_handoff,
        }

        if step_name not in step_methods:
            raise ValueError(f"Unknown step: {step_name}")

        return await step_methods[step_name](ctx)

    async def execute(self, ctx: LoopContext) -> LoopResult:
        """Execute Story Spark loop until stabilization.

        This is the main entry point called by Showrunner.
        Loop provides available steps, Showrunner orchestrates execution.
        """
        try:
            # Open TU
            ctx.open_tu(loop_name="story_spark")

            # Showrunner orchestrates until loop stabilizes
            # (This is Showrunner's responsibility, not hardcoded here)
            while not await ctx.is_loop_stable():
                # Showrunner decides next step based on:
                # - Execution context (available steps, typical flow)
                # - Current state (which steps completed, artifacts present)
                # - Agent feedback (revision requests, quality issues)
                next_step = await ctx.showrunner.decide_next_step(
                    loop=self,
                    execution_context=self.get_execution_context(),
                    current_state=ctx.get_state()
                )

                # Execute the step Showrunner chose
                result = await self.execute_step(next_step, ctx)

                # If step blocked (e.g., Gatekeeper preview gate),
                # Showrunner might decide to revise earlier steps
                if result.blocked:
                    await ctx.showrunner.handle_blocked_step(
                        step=next_step,
                        remediation=result.remediation
                    )
                    # Showrunner will decide: which step to revise?
                    # Loop continues until stabilization

            # Loop stabilized - all steps complete, validation passed, no revisions
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
                next_loop="hook_harvest"  # From step 8
            )

        except Exception as e:
            ctx.close_tu(success=False, error=str(e))
            return LoopResult.failed(str(e))
```

**Key Points:**

1. **Loop provides step library** — Available steps defined as methods (step_1, step_2, ..., step_8)
2. **Showrunner orchestrates execution** — Decides which step to run next, when to iterate, when loop stabilizes
3. **Loops stabilize through iteration** — Not linear execution; steps can repeat until quality achieved
4. **Agents provide expertise** — LLM-backed roles execute tasks, can suggest collaboration
5. **Playbooks provide recommendations** — Typical flow + role recommendations, but Showrunner decides
6. **Loop goals bound scope** — Story Spark develops plot (can't change style), Style Tune Up refines tone (can't change plot)
7. **Type safe** — Python typing, structured data, not string parsing
8. **Testable** — Mock LLM responses (agents + Showrunner), test step logic independently
9. **Maintainable** — Change step logic by editing methods, not parsing markdown

---

## LoopContext API: Showrunner-Controlled Role Waking

### Showrunner Decision-Making Protocol

The `LoopContext` provides methods that delegate strategic decisions to the Showrunner LLM:

```python
class LoopContext:
    """Execution context for a loop, with Showrunner control."""

    async def request_role_for_step(
        self,
        step: str,
        playbook_recommends: str,
        reason: str,
        context: Optional[dict] = None
    ) -> Role:
        """Request Showrunner to decide which role should execute this step.

        Args:
            step: Step identifier (e.g., "step_1_topology_draft")
            playbook_recommends: Role recommended by playbook spec
            reason: What this step accomplishes
            context: Additional context for Showrunner's decision

        Returns:
            Role instance to execute the step (usually playbook recommendation)

        Flow:
            1. Loop code provides: step name, playbook recommendation, reason
            2. Showrunner LLM evaluates:
               - Playbook recommendation (baseline)
               - Current TU context (previous artifacts, issues)
               - Project preferences (role overrides, efficiency)
               - Step requirements (what expertise is needed)
            3. Showrunner decides which role to wake (usually follows playbook)
            4. Context wakes role and returns to loop
        """
        # Send decision request to Showrunner LLM
        decision = await self.showrunner.decide_next_role(
            step=step,
            playbook_recommends=playbook_recommends,
            reason=reason,
            tu_context=self.get_tu_context(),
            project_context=self.get_project_context()
        )

        # Wake chosen role (might differ from playbook if Showrunner overrides)
        chosen_role = decision.role  # Usually == playbook_recommends
        agent = await self.wake_role(chosen_role)

        return agent

    async def request_collaboration(
        self,
        current_agent: str,
        suggested_role: str,
        reason: str
    ) -> Optional[Role]:
        """Request Showrunner to approve agent's collaboration suggestion.

        Args:
            current_agent: Agent requesting collaboration
            suggested_role: Role the agent wants to collaborate with
            reason: Why collaboration would help

        Returns:
            Role instance if approved, None if denied

        Flow:
            1. Agent suggests: "I need Lore Weaver to verify canon consistency"
            2. Showrunner LLM evaluates:
               - Is this collaboration necessary?
               - Will it improve quality?
               - Is it efficient? (cost/benefit)
            3. Showrunner approves or denies
            4. If approved, wake collaborator and return
        """
        approved = await self.showrunner.approve_collaboration(
            current_agent=current_agent,
            suggested_role=suggested_role,
            reason=reason,
            tu_context=self.get_tu_context()
        )

        if approved:
            return await self.wake_role(suggested_role)
        else:
            return None
```

### Playbook as Recommendation, Not Requirement

**The Playbook Provides:**
- **Recommended choreography** — Best-practice role assignments per step
- **RACI matrix** — Responsible, Accountable, Consulted, Informed
- **Message templates** — What information each role needs
- **Validation checkpoints** — What to validate at each step

**The Showrunner Decides:**
- Which role to actually wake (usually follows playbook)
- Whether to approve agent collaboration requests
- When to deviate if context suggests a better approach

**Bounds on Deviation:**
- **Loop goal is fixed** — Story Spark develops plot, Style Tune Up refines tone, etc.
- **Step library is fixed** — Available steps defined by loop class (can't invent new steps)
- **Required steps must execute** — Core steps (e.g., step_1, step_7, step_8) must run at least once
- **Validation checkpoints are mandatory** — All artifacts must validate against schemas
- **Quality bars enforced** — Gatekeeper must approve before loop can complete
- **Scope constraints enforced** — Story Spark can't update style guide, Style Tune Up can't change plot

**But loops STABILIZE through iteration (not linear execution):**
- Later agents can request earlier agents to revise work
- Steps can execute multiple times until quality is achieved
- Showrunner decides when loop has stabilized and is complete

**Example Deviations & Iterations (Showrunner might choose):**

1. **Efficiency:** Step 1 recommends Plotwright, but previous loop already had Plotwright draft topology → Showrunner: "Reuse existing draft, skip to step 2"

2. **Context-aware role selection:** Step 3 recommends Scene Smith, but topology changes are minimal → Showrunner: "Plotwright can handle prose for these small changes, no need to wake Scene Smith"

3. **Collaboration control:** Plotwright suggests Lore Weaver collaboration in step 1 → Showrunner evaluates: "Topology changes don't touch established canon, deny collaboration request"

4. **Quality-driven reordering:** Step 5 recommends Style Lead, but previous checkpoint flagged tone issues → Showrunner: "Wake Style Lead early, before prose pass, to provide guidance upfront"

5. **Revision cycle (STABILIZATION):** Gatekeeper (step 7) finds topology inconsistencies → Showrunner: "Go back to step_1_topology_draft, have Plotwright revise. Then re-run steps 2-7 with revised topology. Loop is NOT stable yet."

6. **Iterative refinement:** Scene Smith (step 3) prose doesn't match Lore Weaver's feasibility notes (step 6) → Showrunner: "Return to step_3_prose_pass, have Scene Smith revise with Lore Weaver's input. Re-validate at step 7. Loop stabilizes when all agents are satisfied."

**Stabilization Criteria (when loop completes):**
- All required steps have executed at least once
- All artifacts validate against schemas
- Gatekeeper preview gate passes (step 7)
- No pending revisions requested by any agent
- Showrunner determines loop goal has been achieved

**Result:** Playbook provides available steps and typical flow, Showrunner orchestrates execution adaptively (forward progress + revision cycles) until loop stabilizes.

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
