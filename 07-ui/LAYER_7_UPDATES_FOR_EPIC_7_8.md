# Layer 7 Updates for Epic 7/8 Revised Architecture

**Document Version:** 1.0 (2025-11-06)
**Related:** `06-libraries/EPIC_7_8_REVISED.md` v2.2
**Purpose:** Document how Layer 6 Epic 7/8 architecture changes affect Layer 7 CLI implementation

---

## Executive Summary

The revised Layer 6 architecture (Epic 7 & 8) introduces significant changes that affect how Layer 7 (CLI) presents loop execution to users:

**Key Changes:**
1. **Loop stabilization** — Loops iterate until stable (not single linear pass)
2. **Showrunner orchestration** — LLM-backed Showrunner makes dynamic decisions
3. **Revision cycles** — Later steps can trigger earlier step revisions
4. **Loop goals** — Each loop has fixed scope boundaries
5. **Two-tier context** — Showrunner knows all loops (registry) but detailed context only for active loop

**Impact on Layer 7:**
- **Epic 5 (Loop Execution)** — Progress indicators must handle iteration, not just linear steps
- **Epic 7 (Quickstart)** — Loop sequencing is Showrunner-decided, not hardcoded
- **User expectations** — Need to communicate stabilization, revision cycles clearly

This document analyzes which CLI epics need updates and recommends UX approaches.

---

## Layer 6 Architecture Changes (Summary)

### Before (Original Plan)

**Loop execution:**
```
Story Spark: step_1 → step_2 → step_3 → ... → step_8 → DONE
```
- Linear, one-pass execution
- Steps execute in order
- No iteration

**Showrunner:**
- Follows hardcoded playbooks
- No strategic decision-making

### After (Epic 7/8 Revised v2.2)

**Loop execution:**
```
Story Spark:
  Iteration 1: step_1 → step_2 → step_3 → ... → step_7 (Gatekeeper BLOCKS)
  Iteration 2: step_1 (revise) → step_2 → step_3 → ... → step_7 (PASS)
  → step_8 → DONE (loop stabilized)
```
- Iterative, convergence-based
- Steps can execute multiple times
- Showrunner decides which step runs next
- Loop stabilizes when all quality criteria met

**Showrunner:**
- LLM-backed strategic orchestrator
- Decides which role to wake for each step (playbook recommends, SR decides)
- Approves/denies agent collaboration requests
- Decides which loop runs next (from registry of all loops)
- Decides when loop has stabilized

**Loop scopes:**
- Story Spark: Develops plot (cannot change style/art)
- Style Tune Up: Refines tone (cannot change plot)
- Art Touch Up: Polishes visuals (cannot change plot/prose)

---

## Impact Analysis by Epic

### Epic 5: Loop Execution (`qf run <loop-name>`)

**Original Plan (from IMPLEMENTATION_PLAN.md):**
```bash
$ qf run hook-harvest

Hook Harvest Loop
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Showrunner created TU-2025-10-31-SR01
✓ Lore Weaver analyzing...
✓ Hook generation complete

[Summary display]
```

**Assumption:** Single linear pass, progress shows steps completing in sequence.

**New Reality:**
- Loop can iterate multiple times
- Steps can repeat (revision cycles)
- Showrunner makes dynamic decisions
- Loop stabilizes when quality bars pass

**Required UX Changes:**

#### 5.1: Enhanced Progress Display

Show iteration and stabilization, not just linear progress:

```bash
$ qf run story-spark

Story Spark Loop
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Goal: Develop new story beats and plot progression
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Iteration 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Step 1: Topology Draft (Plotwright)
✓ Step 2: Section Briefs (Plotwright)
✓ Step 3: Prose Pass (Scene Smith)
✓ Step 4: Hook Generation (Plotwright, Scene Smith)
✓ Step 5: Style Check (Style Lead)
✓ Step 6: Feasibility Check (Lore Weaver)
⟳ Step 7: Preview Gate (Gatekeeper)...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ Gatekeeper found issues
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issues:
  - Topology inconsistencies in section 3
  - Scene draft doesn't match lore constraints

Showrunner decision: Revise topology (back to Step 1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Iteration 2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⟳ Step 1: Topology Draft - Revision (Plotwright)...
✓ Step 1: Topology revised
✓ Step 2: Section Briefs updated
✓ Step 3: Prose Pass revised
✓ Step 4: Hook Generation (no changes needed)
✓ Step 5: Style Check (passed)
✓ Step 6: Feasibility Check (passed)
✓ Step 7: Preview Gate (Gatekeeper - PASSED)
✓ Step 8: Triage Hand-off

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Loop Stabilized
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Duration: 4m 12s (2 iterations)
TU: TU-2025-11-06-SS01

Artifacts Created:
  ✓ topology_notes (revised)
  ✓ section_briefs (revised)
  ✓ scene_drafts (revised)
  ✓ 5 hooks generated

Next suggested loop: Hook Harvest
```

**Key UX elements:**
1. **Show iteration count** — User sees loop is refining, not stuck
2. **Show Showrunner decisions** — Why did we go back? Clear communication
3. **Show revision status** — "Revision" tag on repeated steps
4. **Final "Loop Stabilized"** — Clear completion signal
5. **Duration shows iterations** — "4m 12s (2 iterations)"

#### 5.2: Progress API Changes

**Current assumption:**
```python
# Linear progress
progress.add_task("Running Hook Harvest...", total=None)
```

**New requirement:**
```python
# Support iteration and dynamic steps
progress_tracker = LoopProgressTracker(console)

# Loop can iterate
for iteration in loop_execution:
    progress_tracker.start_iteration(iteration_num)

    for step in iteration:
        progress_tracker.start_step(step.name, step.agent)
        result = await step.execute()

        if result.blocked:
            progress_tracker.mark_blocked(step.name, result.issues)
            progress_tracker.show_showrunner_decision(result.remediation)
        else:
            progress_tracker.complete_step(step.name)

    if loop.is_stable():
        progress_tracker.mark_stabilized()
        break
```

#### 5.3: Implementation Updates

**Files to modify:**
- `src/qf/commands/run.py` — Add iteration tracking
- `src/qf/formatting/progress.py` — Support iterative progress display
- `src/qf/formatting/loop_summary.py` — Show iteration count, revision summary

**New classes needed:**
```python
class LoopProgressTracker:
    """Track progress of iterative loop execution."""

    def start_iteration(self, iteration_num: int):
        """Mark start of new iteration."""

    def start_step(self, step_name: str, agent: str, is_revision: bool = False):
        """Mark start of step (show if revision)."""

    def mark_blocked(self, step_name: str, issues: list[str]):
        """Show step was blocked (e.g., Gatekeeper)."""

    def show_showrunner_decision(self, decision: str):
        """Show Showrunner's decision (which step next, why)."""

    def complete_step(self, step_name: str):
        """Mark step complete."""

    def mark_stabilized(self):
        """Show loop has stabilized."""
```

---

### Epic 7: Quickstart Workflow

**Original Plan:**
```python
# Hardcoded loop sequence
loops = [
    "hook_harvest",
    "lore_deepening",
    "story_spark",
    # ... fixed order
]

for loop in loops:
    run_loop(loop)
    show_checkpoint()
    if not user_continues():
        break
```

**Assumption:** Fixed loop sequence, linear execution.

**New Reality:**
- Showrunner decides which loop runs next (from registry)
- Loops can stabilize through multiple iterations
- Each loop has a goal/scope (Story Spark = plot, not style)

**Required UX Changes:**

#### 7.1: Dynamic Loop Sequencing

Quickstart can't have a hardcoded sequence; Showrunner decides:

```python
# New approach
current_loop = None
completed_loops = []

while True:
    # Showrunner decides next loop (strategic decision using Tier 1 context)
    next_loop = await showrunner.decide_next_loop(
        tu_context=get_current_tu_context(),
        completed_loops=completed_loops
    )

    if next_loop is None:
        break  # Showrunner says we're done

    # Run loop (with iteration/stabilization)
    result = await run_loop_with_progress(next_loop)
    completed_loops.append(next_loop)

    # Checkpoint
    show_loop_summary(result)

    if not await get_user_checkpoint_approval(next_loop_suggestion=showrunner.suggest_next()):
        break
```

**UX Impact:**
```bash
$ qf quickstart

[Setup questions]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Showrunner Decision: Starting with Hook Harvest
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Hook Harvest executes with stabilization]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Loop Complete: Hook Harvest (2m 34s)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Artifacts: 5 hooks created

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Showrunner suggests next: Story Spark
Reason: Hooks are ready to be developed into story beats
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Continue to Story Spark? [Y/n]:
```

**Key UX elements:**
1. **Show Showrunner decisions** — User understands why this loop is next
2. **Show Showrunner reasoning** — "Hooks are ready to be developed..."
3. **Suggest next loop** — User can see what's coming
4. **Allow override** — Advanced users might want different sequence

#### 7.2: Progress Tracking Update

**Old assumption:**
```
Completed:
  ✓ Hook Harvest
  ✓ Lore Deepening

Currently Running:
  ⟳ Story Spark

Pending:
  ⏸ Canon Weaving
  ⏸ Gatecheck
```

**New reality:**
- Can't show "Pending" (Showrunner decides dynamically)
- Can show "Suggested Next" from Showrunner

```
Completed Loops:
  ✓ Hook Harvest (2m 34s)
  ✓ Story Spark (4m 12s, 2 iterations)

Currently Running:
  ⟳ Hook Harvest (iteration 1)

Showrunner's Plan:
  → Hook Harvest (processing new hooks from Story Spark)
  → Suggested next: Canon Weaving
```

#### 7.3: Loop Goal Communication

Users need to understand what each loop does (and doesn't do):

```bash
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Starting: Story Spark
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Goal: Develop new story beats and plot progression

This loop will:
  ✓ Draft topology and story structure
  ✓ Write scenes and prose
  ✓ Generate hook cards

This loop will NOT:
  ✗ Update style guide or change tone
  ✗ Generate visual art
  ✗ Produce audio assets

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

This helps users understand:
- Why loops have focused goals
- Why another loop might be needed for style/art
- What to expect from this loop

#### 7.4: Implementation Updates

**Files to modify:**
- `src/qf/commands/quickstart.py` — Remove hardcoded loop sequence, use Showrunner decisions
- `src/qf/formatting/quickstart.py` — Show Showrunner reasoning, loop goals

**New additions:**
```python
def show_showrunner_decision(loop_name: str, reasoning: str):
    """Display Showrunner's loop selection decision."""
    panel = Panel(
        f"[bold cyan]Showrunner Decision:[/] Starting with {loop_name}\n"
        f"[dim]{reasoning}[/]",
        border_style="cyan"
    )
    console.print(panel)

def show_loop_goal(loop_name: str, loop_metadata: dict):
    """Display loop's goal and scope before execution."""
    # From Tier 1 loop registry
    console.print(f"\n[bold]Starting: {loop_name}[/]")
    console.print(f"[dim]Goal:[/] {loop_metadata['purpose']}")

    # Show can/cannot
    console.print("\n[green]This loop will:[/]")
    for item in loop_metadata['scope']['can']:
        console.print(f"  ✓ {item}")

    console.print("\n[red]This loop will NOT:[/]")
    for item in loop_metadata['scope']['cannot']:
        console.print(f"  ✗ {item}")
```

---

### Epic 6: Asset Generation (`qf generate`)

**Impact:** Minimal

Asset generation is largely unaffected since it's about individual artifact generation, not loop orchestration. However:

**Minor update needed:**
- Show which loop generated an artifact (in artifact metadata)
- Show iteration number if artifact was revised

Example:
```bash
$ qf show HOOK-001

Hook Card: HOOK-001
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Title:    The lighthouse keeper's final log
Status:   canonized
Created:  2025-11-06 by Lore Weaver
Loop:     Hook Harvest (iteration 1)  # NEW
Revised:  Story Spark (iteration 2)  # NEW if revised
TU:       TU-2025-11-06-HH01

[... rest of artifact ...]
```

---

### Epic 2: Artifact Inspection (`qf list`, `qf show`)

**Impact:** Minor

Artifacts now have:
- **Loop provenance** — Which loop created/revised them
- **Iteration tracking** — Which iteration of the loop

**Update needed:**
```bash
$ qf show TU-2025-11-06-SS01

TU Brief: TU-2025-11-06-SS01
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Loop:       Story Spark
Iterations: 2  # NEW
Duration:   4m 12s  # NEW
Status:     Stabilized  # NEW

Iteration History:  # NEW
  1: Completed step_1-7, blocked at gatekeeper
  2: Revised step_1-3, passed gatekeeper, completed

Artifacts Created:
  - topology_notes (revised in iteration 2)
  - section_briefs (revised in iteration 2)
  - scene_drafts (revised in iteration 2)
  - 5 hooks (created in iteration 1)

[... rest of TU ...]
```

---

### Epic 4: Validation & Quality (`qf check`)

**Impact:** Minimal

Gatecheck runs the same, but:
- Users should understand gatecheck can trigger loop revision
- Show context: "If gatecheck fails during loop, Showrunner will revise"

Example:
```bash
$ qf check

Running Gatekeeper validation...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Quality Bar Results:
  ✓ Integrity
  ✗ Style (3 issues)
  ✓ Gateways
  [... all 8 bars ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ GATECHECK FAILED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommended action: Run Style Tune Up loop

Note: If gatecheck runs during a loop, Showrunner will
automatically revise earlier steps until issues are resolved.

$ qf run style-tune-up
```

---

## New Features to Consider

Based on the revised architecture, some new CLI features become valuable:

### 1. Loop Registry Explorer

Since Showrunner uses a loop registry (Tier 1 context), users might want to see it:

```bash
$ qf loops list

Available Loops (13)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name               Purpose
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
hook-harvest       Evaluate and triage proposed hooks
story-spark        Develop new story beats and plot
lore-deepening     Expand worldbuilding and lore
canon-weaving      Weave changes into canon
style-tune-up      Refine tone and voice consistency
art-touch-up       Polish visual assets
[...]

$ qf loops show story-spark

Story Spark Loop
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Purpose:     Develop new story beats and plot progression

Typical Inputs:
  - existing canon
  - hook cards

Typical Outputs:
  - scene drafts
  - topology notes
  - new hooks

Scope:
  Can:    Draft topology, write scenes, generate hooks
  Cannot: Update style guide, generate art, change canon

Often Follows:   hook-harvest
Often Precedes:  canon-weaving, hook-harvest

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Value:** Users understand what each loop does and when to use it manually.

### 2. Showrunner Explain Mode

For transparency, show Showrunner's reasoning:

```bash
$ qf run story-spark --explain

Story Spark Loop
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Iteration 1, Step 1: Topology Draft
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Showrunner Decision:
  Playbook recommends: Plotwright
  Showrunner chooses:  Plotwright
  Reasoning:          Following playbook recommendation,
                      no context suggests deviation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⟳ Plotwright drafting topology...
✓ Complete

[... continues with Showrunner decisions visible ...]
```

**Value:** Helps users understand Showrunner behavior, useful for debugging.

### 3. Iteration Summary

After a multi-iteration loop, show what changed:

```bash
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Iteration Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Iteration 1:
  Steps:     1-7
  Blocked:   Gatekeeper preview gate
  Issues:    Topology inconsistencies

Iteration 2:
  Revised:   Steps 1-3
  Reused:    Steps 4-6 (no changes needed)
  New:       Step 7-8
  Result:    STABILIZED

Total Duration: 4m 12s
Quality: All bars passed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Value:** Users see efficiency gains (some steps reused) and understand iteration flow.

---

## Recommended Implementation Priority

### Phase 1: Core Updates (Required)

**Epic 5.1-5.3:** Loop execution with iteration support
- Most critical change
- Affects all loop execution UX
- **Estimated effort:** 2-3 days additional work

**Epic 7.1-7.2:** Dynamic quickstart sequencing
- Removes hardcoded loop order
- Uses Showrunner decisions
- **Estimated effort:** 2-3 days additional work

### Phase 2: Enhanced UX (High value)

**Loop goal communication:** Show what each loop does/doesn't do
- Helps users understand scope boundaries
- **Estimated effort:** 1 day

**Showrunner decision visibility:** Show why Showrunner chose this role/loop
- Transparency and debuggability
- **Estimated effort:** 1 day

### Phase 3: Advanced Features (Nice to have)

**Loop registry explorer:** `qf loops list/show`
- Discoverability
- **Estimated effort:** 1 day

**Explain mode:** `qf run --explain`
- Power users and debugging
- **Estimated effort:** 1-2 days

**Iteration summary:** Detailed iteration breakdown
- Understanding and transparency
- **Estimated effort:** 1 day

---

## Files to Create/Modify

### New Files

```
src/qf/
  formatting/
    loop_progress.py       # LoopProgressTracker class
    showrunner.py          # Showrunner decision formatting
    iterations.py          # Iteration summary formatting

  commands/
    loops.py               # NEW: qf loops list/show

tests/
  formatting/
    test_loop_progress.py
    test_showrunner.py

  commands/
    test_loops.py
```

### Modified Files

```
src/qf/
  commands/
    run.py                 # Add iteration tracking
    quickstart.py          # Remove hardcoded sequence, use SR
    show.py                # Show loop/iteration metadata

  formatting/
    progress.py            # Support iterative progress
    loop_summary.py        # Show iteration count
    artifacts.py           # Show loop provenance

tests/
  commands/
    test_run.py            # Test multi-iteration loops
    test_quickstart.py     # Test dynamic sequencing
```

---

## Testing Considerations

### New Test Scenarios

**Loop iteration:**
- Loop completes in 1 iteration (no revisions)
- Loop requires 2 iterations (Gatekeeper blocks once)
- Loop requires 3+ iterations (multiple revision cycles)

**Showrunner decisions:**
- Showrunner follows playbook recommendations
- Showrunner overrides playbook (context-driven)
- Showrunner approves collaboration
- Showrunner denies collaboration

**Quickstart sequencing:**
- Showrunner suggests expected sequence
- Showrunner adapts sequence based on results
- User exits at checkpoint
- User overrides suggested next loop

### Mock Requirements

Need mocked Showrunner that can:
- Decide next role for step
- Decide collaboration approval
- Decide next loop in sequence
- Decide when loop is stable

Example mock:
```python
class MockShowrunner:
    def __init__(self, scenario: str):
        self.scenario = scenario

    async def decide_next_step(self, ...) -> str:
        if self.scenario == "linear":
            return playbook_recommended_step
        elif self.scenario == "one_revision":
            if iteration == 1 and step == 7:
                return "block"  # Trigger revision
            return playbook_recommended_step

    def is_loop_stable(self, ...) -> bool:
        return all_quality_bars_pass and no_pending_revisions
```

---

## Documentation Updates

### User Guide Additions

**New section:** "Understanding Loop Iterations"
```markdown
# Understanding Loop Iterations

Loops in QuestFoundry don't execute in a single pass. Instead,
they **stabilize** through iteration:

1. Loop executes steps in sequence
2. If quality issues found (e.g., Gatekeeper blocks):
   - Showrunner decides which step to revise
   - Loop returns to that step
   - Steps re-execute with revisions
3. Loop stabilizes when:
   - All steps complete
   - All artifacts validate
   - Gatekeeper approves
   - No pending revisions

This ensures quality while remaining efficient (steps that
don't need revision are reused).
```

**New section:** "How Showrunner Makes Decisions"
```markdown
# How Showrunner Makes Decisions

The Showrunner is an LLM-backed orchestrator that makes
strategic decisions:

**Deciding which role to wake:**
- Playbook recommends a role for each step
- Showrunner evaluates: playbook + context + project prefs
- Usually follows playbook (best practices)
- Can adapt when context suggests a better fit

**Deciding which loop to run next:**
- Showrunner knows all available loops (loop registry)
- Evaluates: TU artifacts, completed loops, project goals
- Suggests next loop with reasoning
- You can accept or override

**Deciding when loop is stable:**
- Checks: all steps complete, validation passed, no issues
- Continues iterating until stabilization criteria met
```

### Command Help Updates

**`qf run` help text:**
```bash
$ qf run --help

Usage: qf run [OPTIONS] LOOP_NAME

  Run a specific loop.

  Loops execute steps until they stabilize. This may involve
  multiple iterations if quality issues are found. The
  Showrunner orchestrates execution and decides when the
  loop is complete.

  Examples:
    qf run hook-harvest
    qf run story-spark --interactive
    qf run style-tune-up --explain  # Show Showrunner decisions

Options:
  --interactive      Enable agent questions during loop
  --explain          Show Showrunner decision-making
  --help             Show this message and exit
```

---

## Summary of Changes

### High Priority (Required for v1.0)

1. **Epic 5: Loop execution iteration support**
   - Progress tracking for multi-iteration loops
   - Show revision cycles
   - Show stabilization

2. **Epic 7: Dynamic quickstart sequencing**
   - Remove hardcoded loop order
   - Use Showrunner decisions
   - Show Showrunner reasoning

### Medium Priority (Strongly recommended)

3. **Loop goal communication**
   - Show what loop does/doesn't do
   - Helps users understand scope

4. **Showrunner decision visibility**
   - Show why this role was chosen
   - Show why this loop is next

### Low Priority (Nice to have)

5. **Loop registry explorer** (`qf loops list/show`)
6. **Explain mode** (`qf run --explain`)
7. **Iteration summaries**

---

## Estimated Additional Effort

**Original Layer 7 estimate:** 6-8 weeks (aggressive)

**Additional effort from Epic 7/8 changes:**
- Phase 1 (Core updates): +4-6 days
- Phase 2 (Enhanced UX): +2 days
- Phase 3 (Advanced features): +3-4 days (optional)

**New estimate:** 7-9 weeks (with Phase 1-2)

**Recommendation:** Implement Phase 1 (required) for v1.0, Phase 2 for v1.1, Phase 3 for v1.2+

---

## Conclusion

The Epic 7/8 revised architecture introduces **loop stabilization** and **Showrunner orchestration**, which significantly affect how Layer 7 presents loops to users.

**Key CLI changes needed:**
1. Progress indicators must handle iteration, not just linear steps
2. Quickstart must use dynamic sequencing, not hardcoded order
3. Users need to understand loop goals, stabilization, and Showrunner decisions

**Good news:** These changes make the CLI more transparent and powerful:
- Users see quality assurance in action (revision cycles)
- Users understand Showrunner reasoning (not a black box)
- Users can make informed decisions about which loops to run

**Implementation is tractable:** Core updates add ~1 week to development, with optional enhancements adding another week for great UX.

The revised architecture makes QuestFoundry more robust and the CLI more informative — a win for users.
