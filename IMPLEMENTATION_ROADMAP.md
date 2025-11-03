# QuestFoundry Implementation Roadmap

## Layers 5, 6, 7 — Comprehensive Build Order

**Created:** 2025-10-31 **Status:** Planning Phase

---

## Executive Summary

This document provides the **complete implementation order** for building QuestFoundry Layers 5, 6,
and 7, designed for AI agents to implement with human oversight.

**Target Agents:**

- **Layer 6 (questfoundry-lib):** GitHub Copilot - Python SDK implementation
- **Layer 5 (prompts):** Claude (Sonnet 3.5+) - Sophisticated prompt engineering
- **Layer 7 (questfoundry-cli):** GitHub Copilot - CLI UX implementation

---

## Critical Path Overview

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: Layer 6 Foundation (Weeks 1-4)                     │
│ Build core infrastructure that everything depends on        │
└─────────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: Layer 5 Foundations + Layer 7 Start (Weeks 5-8)    │
│ Prompt foundations + CLI basics (can work in parallel)      │
└─────────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: Provider System (Weeks 9-12)                       │
│ LLM integration enables role execution                      │
└─────────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 4: Role Prompts + Orchestration (Weeks 13-18)         │
│ Core intelligence layer + coordination                      │
└─────────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 5: Quickstart + Assets (Weeks 19-22)                  │
│ User-facing workflows complete                               │
└─────────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 6: Quality + Polish (Weeks 23-26)                     │
│ Testing, documentation, distribution                         │
└─────────────────────────────────────────────────────────────┘
```

**Total Estimated Timeline:** 26 weeks (6 months) for full MVP

---

## Phase 1: Layer 6 Foundation (Weeks 1-4)

**Goal:** Build core infrastructure that all other work depends on.

**Priority:** CRITICAL PATH - Nothing else can proceed without this.

### Week 1: Setup & Schema Integration

| Epic  | Feature           | Layer | Agent   | Deliverable                    |
| ----- | ----------------- | ----- | ------- | ------------------------------ |
| L6-E1 | Repository Setup  | 6     | Copilot | `questfoundry-lib` repo, CI/CD |
| L6-E1 | Package Structure | 6     | Copilot | Python package structure       |
| L6-E1 | Development Tools | 6     | Copilot | Linting, testing, pre-commit   |
| L6-E2 | Schema Bundling   | 6     | Copilot | 17 schemas from Layer 3        |
| L6-E2 | Schema Validation | 6     | Copilot | `validate_artifact()` function |

**Checkpoint:** Can validate artifacts against Layer 3 schemas ✅

---

### Week 2: Protocol & Envelopes

| Epic  | Feature              | Layer | Agent   | Deliverable                    |
| ----- | -------------------- | ----- | ------- | ------------------------------ |
| L6-E2 | Protocol Envelope    | 6     | Copilot | Pydantic envelope models       |
| L6-E2 | Protocol Conformance | 6     | Copilot | `validate_envelope()` function |

**Checkpoint:** Can create and validate Layer 4 envelopes ✅

---

### Week 3: State Management (SQLite)

| Epic  | Feature               | Layer | Agent   | Deliverable              |
| ----- | --------------------- | ----- | ------- | ------------------------ |
| L6-E3 | State Store Interface | 6     | Copilot | Abstract `StateStore`    |
| L6-E3 | SQLite Project File   | 6     | Copilot | `.qfproj` implementation |

**Checkpoint:** Can create `.qfproj` files and store artifacts ✅

---

### Week 4: State Management (Files) & Workspace

| Epic  | Feature                  | Layer | Agent   | Deliverable              |
| ----- | ------------------------ | ----- | ------- | ------------------------ |
| L6-E3 | File-Based Hot Workspace | 6     | Copilot | Hot workspace file store |
| L6-E3 | Workspace Manager        | 6     | Copilot | Unified workspace API    |

**Checkpoint:** Hot/Cold workspace working ✅

**Phase 1 Milestone:** Layer 6 foundation complete - can manage projects and artifacts

---

## Phase 2: Foundations + CLI Start (Weeks 5-8)

**Goal:** Start Layer 5 prompts (foundations) and Layer 7 CLI (basic commands) in parallel.

**Priority:** HIGH - Enables testing of Layer 6 via CLI

### Week 5: Artifact Types + CLI Setup

| Epic  | Feature             | Layer | Agent   | Deliverable             |
| ----- | ------------------- | ----- | ------- | ----------------------- |
| L6-E4 | Base Artifact Class | 6     | Copilot | `Artifact` base class   |
| L6-E4 | Core Artifact Types | 6     | Copilot | HookCard, TUBrief, etc. |
| L7-E1 | Repository Setup    | 7     | Copilot | `questfoundry-cli` repo |
| L7-E1 | Package Structure   | 7     | Copilot | CLI package with Typer  |

**Checkpoint:** Can create typed artifacts + CLI skeleton exists ✅

---

### Week 6: More Artifacts + Layer 5 Foundations

| Epic  | Feature                    | Layer | Agent   | Deliverable                     |
| ----- | -------------------------- | ----- | ------- | ------------------------------- |
| L6-E4 | Remaining Artifact Types   | 6     | Copilot | All 17 artifacts                |
| L5-E1 | Context Management Pattern | 5     | Claude  | `_shared/context_management.md` |
| L5-E1 | Safety Protocol Pattern    | 5     | Claude  | `_shared/safety_protocol.md`    |
| L5-E1 | Escalation Rules Pattern   | 5     | Claude  | `_shared/escalation_rules.md`   |
| L5-E1 | Human Interaction Pattern  | 5     | Claude  | `_shared/human_interaction.md`  |

**Checkpoint:** All artifacts implemented + Layer 5 shared foundations ready ✅

---

### Week 7: Lifecycles + CLI Commands

| Epic  | Feature                     | Layer | Agent   | Deliverable                       |
| ----- | --------------------------- | ----- | ------- | --------------------------------- |
| L6-E4 | Hook Lifecycle              | 6     | Copilot | Hook state machine                |
| L6-E4 | TU Lifecycle                | 6     | Copilot | TU state machine                  |
| L7-E2 | Project Management Commands | 7     | Copilot | `qf init`, `qf open`, `qf status` |

**Checkpoint:** State machines work + can create projects via CLI ✅

---

### Week 8: Protocol Client + CLI Inspection

| Epic  | Feature              | Layer | Agent   | Deliverable            |
| ----- | -------------------- | ----- | ------- | ---------------------- |
| L6-E5 | File-Based Transport | 6     | Copilot | Message file transport |
| L6-E5 | Protocol Client      | 6     | Copilot | `ProtocolClient` class |
| L7-E2 | Artifact Listing     | 7     | Copilot | `qf list` command      |
| L7-E2 | Artifact Inspection  | 7     | Copilot | `qf show` command      |
| L7-E2 | History Command      | 7     | Copilot | `qf history` command   |

**Checkpoint:** Protocol client works + can inspect projects via CLI ✅

**Phase 2 Milestone:** Can create/inspect projects via CLI, Layer 5 foundations ready

---

## Phase 3: Provider System (Weeks 9-12)

**Goal:** Implement LLM and image provider plugins.

**Priority:** HIGH - Required for role execution

### Week 9: Provider Foundation

| Epic  | Feature              | Layer | Agent   | Deliverable                  |
| ----- | -------------------- | ----- | ------- | ---------------------------- |
| L6-E6 | Provider Interface   | 6     | Copilot | Abstract provider interfaces |
| L6-E6 | Configuration System | 6     | Copilot | Config loading with env vars |
| L7-E3 | Config Command       | 7     | Copilot | `qf config` commands         |

**Checkpoint:** Provider system designed + configurable via CLI ✅

---

### Week 10: Text Providers

| Epic  | Feature               | Layer | Agent   | Deliverable           |
| ----- | --------------------- | ----- | ------- | --------------------- |
| L6-E6 | OpenAI Provider       | 6     | Copilot | GPT-4 text generation |
| L6-E6 | Ollama Provider       | 6     | Copilot | Local LLM support     |
| L7-E3 | Provider List Command | 7     | Copilot | `qf provider list`    |

**Checkpoint:** Text generation working with 2 providers ✅

---

### Week 11: Image Providers

| Epic  | Feature                | Layer | Agent   | Deliverable         |
| ----- | ---------------------- | ----- | ------- | ------------------- |
| L6-E6 | Automatic1111 Provider | 6     | Copilot | SD image generation |
| L6-E6 | DALL-E Provider        | 6     | Copilot | DALL-E integration  |

**Checkpoint:** Image generation working with 2 providers ✅

---

### Week 12: Quality & Validation Commands

| Epic  | Feature            | Layer | Agent   | Deliverable                      |
| ----- | ------------------ | ----- | ------- | -------------------------------- |
| L7-E4 | Validation Command | 7     | Copilot | `qf validate` command            |
| L7-E4 | Gatecheck Command  | 7     | Copilot | `qf check` command (placeholder) |

**Checkpoint:** Can validate artifacts via CLI ✅

**Phase 3 Milestone:** LLM integration working, can generate text and images

---

## Phase 4: Role Prompts + Orchestration (Weeks 13-18)

**Goal:** Implement role prompts and orchestration logic.

**Priority:** CRITICAL - This is the intelligence layer

### Week 13: Orchestration Roles (Prompts)

| Epic  | Feature                    | Layer | Agent  | Deliverable            |
| ----- | -------------------------- | ----- | ------ | ---------------------- |
| L5-E2 | Showrunner System Prompt   | 5     | Claude | Showrunner prompt      |
| L5-E2 | Showrunner Intent Handlers | 5     | Claude | Intent handler prompts |
| L5-E2 | Showrunner Examples        | 5     | Claude | Example conversations  |

**Checkpoint:** Showrunner prompt complete ✅

---

### Week 14: Gatekeeper + Role Execution Foundation

| Epic  | Feature                  | Layer | Agent   | Deliverable           |
| ----- | ------------------------ | ----- | ------- | --------------------- |
| L5-E2 | Gatekeeper System Prompt | 5     | Claude  | Gatekeeper prompt     |
| L5-E2 | Quality Bar Checks       | 5     | Claude  | 8 quality bar prompts |
| L5-E2 | Gatekeeper Examples      | 5     | Claude  | Example conversations |
| L6-E7 | Prompt Bundling          | 6     | Copilot | Load Layer 5 prompts  |

**Checkpoint:** Gatekeeper prompt complete + Layer 6 can load prompts ✅

---

### Week 15: Role Session Management

| Epic  | Feature         | Layer | Agent   | Deliverable              |
| ----- | --------------- | ----- | ------- | ------------------------ |
| L6-E7 | Role Session    | 6     | Copilot | `RoleSession` class      |
| L6-E7 | Prompt Executor | 6     | Copilot | Execute prompts with LLM |
| L6-E7 | Session Manager | 6     | Copilot | `SessionManager` class   |

**Checkpoint:** Can execute role prompts with real LLMs ✅

---

### Week 16: Core Content Roles (Prompts)

| Epic  | Feature                         | Layer | Agent  | Deliverable                |
| ----- | ------------------------------- | ----- | ------ | -------------------------- |
| L5-E3 | Lore Weaver System Prompt       | 5     | Claude | Lore Weaver prompt         |
| L5-E3 | Lore Weaver Handlers & Examples | 5     | Claude | Intent handlers + examples |
| L5-E3 | Scene Smith System Prompt       | 5     | Claude | Scene Smith prompt         |
| L5-E3 | Scene Smith Handlers & Examples | 5     | Claude | Intent handlers + examples |

**Checkpoint:** Core content role prompts complete ✅

---

### Week 17: Orchestration Implementation

| Epic  | Feature           | Layer | Agent   | Deliverable              |
| ----- | ----------------- | ----- | ------- | ------------------------ |
| L6-E8 | Loop Definitions  | 6     | Copilot | 11 loop structures       |
| L6-E8 | Checkpoint System | 6     | Copilot | Checkpoint management    |
| L6-E8 | Showrunner Core   | 6     | Copilot | Loop orchestration logic |

**Checkpoint:** Can run simple loops end-to-end ✅

---

### Week 18: Loop Execution via CLI

| Epic  | Feature                 | Layer | Agent   | Deliverable         |
| ----- | ----------------------- | ----- | ------- | ------------------- |
| L7-E5 | Run Command             | 7     | Copilot | `qf run` command    |
| L7-E5 | Loop Summary Formatting | 7     | Copilot | Rich loop summaries |

**Checkpoint:** Can run loops from CLI! ✅

**Phase 4 Milestone:** Core roles working, can run loops end-to-end via CLI

---

## Phase 5: Quickstart + Assets (Weeks 19-22)

**Goal:** Implement quickstart workflow and asset generation.

**Priority:** HIGH - This is the main user experience

### Week 19: Structure & Discovery Roles

| Epic  | Feature                     | Layer | Agent   | Deliverable                     |
| ----- | --------------------------- | ----- | ------- | ------------------------------- |
| L5-E4 | Plotwright System Prompt    | 5     | Claude  | Plotwright prompt + handlers    |
| L5-E4 | Codex Curator System Prompt | 5     | Claude  | Codex Curator prompt + handlers |
| L6-E8 | Quickstart Orchestration    | 6     | Copilot | Quickstart workflow logic       |

**Checkpoint:** Structure roles complete + quickstart logic ready ✅

---

### Week 20: Style & Quality Roles

| Epic  | Feature                  | Layer | Agent   | Deliverable                   |
| ----- | ------------------------ | ----- | ------- | ----------------------------- |
| L5-E5 | Style Lead System Prompt | 5     | Claude  | Style Lead prompt + handlers  |
| L5-E5 | Researcher System Prompt | 5     | Claude  | Researcher prompt (optional)  |
| L6-E9 | Quality Bar Validators   | 6     | Copilot | 8 quality bar implementations |
| L6-E9 | Gatekeeper Integration   | 6     | Copilot | Gatekeeper orchestration      |

**Checkpoint:** Style/quality roles complete + gatechecks working ✅

---

### Week 21: Asset Roles + Generation Commands

| Epic  | Feature                    | Layer | Agent   | Deliverable           |
| ----- | -------------------------- | ----- | ------- | --------------------- |
| L5-E6 | Art Director System Prompt | 5     | Claude  | Art Director prompt   |
| L5-E6 | Illustrator System Prompt  | 5     | Claude  | Illustrator prompt    |
| L5-E6 | Audio Director & Producer  | 5     | Claude  | Audio role prompts    |
| L7-E6 | Generate Command           | 7     | Copilot | `qf generate` command |
| L7-E6 | Asset Preview              | 7     | Copilot | Image/audio preview   |

**Checkpoint:** Asset generation working via CLI ✅

---

### Week 22: Quickstart CLI Implementation

| Epic  | Feature                     | Layer | Agent   | Deliverable             |
| ----- | --------------------------- | ----- | ------- | ----------------------- |
| L7-E7 | Quickstart Guided Mode      | 7     | Copilot | `qf quickstart` command |
| L7-E7 | Quickstart Interactive Mode | 7     | Copilot | `--interactive` flag    |
| L7-E7 | Progress Tracking           | 7     | Copilot | Progress indicators     |

**Checkpoint:** Quickstart working! Can generate manuscript end-to-end ✅

**Phase 5 Milestone:** Full quickstart workflow working, can generate complete project

---

## Phase 6: Quality + Polish (Weeks 23-26)

**Goal:** Testing, documentation, distribution.

**Priority:** MEDIUM - Quality and usability

### Week 23: Publication Roles + Export

| Epic   | Feature                       | Layer | Agent   | Deliverable                  |
| ------ | ----------------------------- | ----- | ------- | ---------------------------- |
| L5-E7  | Translator System Prompt      | 5     | Claude  | Translator prompt (optional) |
| L5-E7  | Book Binder System Prompt     | 5     | Claude  | Book Binder prompt           |
| L5-E7  | Player-Narrator System Prompt | 5     | Claude  | PN prompt (critical!)        |
| L6-E9  | PN Guard                      | 6     | Copilot | PN boundary enforcement      |
| L6-E10 | View Generation               | 6     | Copilot | View export logic            |
| L6-E10 | Git Export                    | 6     | Copilot | Git-friendly export          |
| L6-E10 | Book Binder                   | 6     | Copilot | Book Binder implementation   |
| L7-E8  | Export Command                | 7     | Copilot | `qf export` command          |
| L7-E8  | Bind Command                  | 7     | Copilot | `qf bind` command            |

**Checkpoint:** Can export views and player-safe content ✅

---

### Week 24: Testing & Shell Completion

| Epic  | Feature                    | Layer | Agent   | Deliverable                |
| ----- | -------------------------- | ----- | ------- | -------------------------- |
| L5-E8 | Prompt Validation Suite    | 5     | Claude  | Validation scripts         |
| L5-E8 | Conversation Test Fixtures | 5     | Claude  | Test conversation examples |
| L5-E8 | Role Interaction Matrix    | 5     | Claude  | Role interaction docs      |
| L7-E9 | Completion Scripts         | 7     | Copilot | Bash/Zsh/Fish completion   |

**Checkpoint:** Testing infrastructure complete + autocomplete works ✅

---

### Week 25: Documentation

| Epic   | Feature                  | Layer | Agent   | Deliverable          |
| ------ | ------------------------ | ----- | ------- | -------------------- |
| L5-E9  | Prompt Engineering Guide | 5     | Claude  | Customization docs   |
| L5-E9  | Role Comparison Matrix   | 5     | Claude  | Role reference table |
| L5-E9  | Migration Guide          | 5     | Claude  | Versioning strategy  |
| L6-E11 | API Documentation        | 6     | Copilot | Layer 6 API docs     |
| L6-E11 | Integration Examples     | 6     | Copilot | Code examples        |
| L7-E11 | User Documentation       | 7     | Copilot | CLI user guide       |
| L7-E11 | Help Text Polish         | 7     | Copilot | Review all help text |

**Checkpoint:** Documentation complete ✅

---

### Week 26: Distribution & Final Polish

| Epic   | Feature                   | Layer | Agent   | Deliverable            |
| ------ | ------------------------- | ----- | ------- | ---------------------- |
| L6-E11 | Package Distribution      | 6     | Copilot | PyPI setup for lib     |
| L7-E11 | Error Message Improvement | 7     | Copilot | Better error messages  |
| L7-E12 | Package Metadata          | 7     | Copilot | README, CHANGELOG      |
| L7-E12 | Release Automation        | 7     | Copilot | GitHub Actions release |
| L7-E12 | Installation Testing      | 7     | Copilot | Multi-platform testing |

**Checkpoint:** Ready for public release! ✅

**Phase 6 Milestone:** All layers complete, documented, and distributed

---

## Parallel Work Opportunities

### Can Be Done in Parallel

**Weeks 5-8:**

- Layer 5 Epic 1 (foundations) + Layer 7 Epic 1-2 (CLI basics)
- These don't depend on each other

**Weeks 13-14:**

- Layer 5 Epic 2 (prompts) + Layer 6 Epic 7 (role execution)
- Prompts can be written while execution framework is built

**Week 21:**

- Layer 5 Epic 6 (asset roles) + Layer 7 Epic 6 (generate command)
- CLI can be built with placeholder implementations

### Cannot Be Parallelized (Critical Dependencies)

- **Layer 6 Epics 1-5 must complete before others** - This is the foundation
- **Layer 5 Epic 1 must complete before other Layer 5 epics** - Shared patterns required
- **Layer 6 Epic 6 (providers) required for Epic 7 (role execution)** - Can't execute without LLMs
- **Layer 6 Epic 8 (orchestration) required for Layer 7 Epic 7 (quickstart)** - CLI wraps
  orchestration

---

## Milestones & Deliverables

### Milestone 1: Foundation Complete (Week 4)

**Deliverables:**

- ✅ Layer 6 repository set up with CI/CD
- ✅ Can create `.qfproj` files
- ✅ Can store and retrieve artifacts
- ✅ Schema validation working

**Success Criteria:**

- All Layer 6 Epic 1-3 tests passing
- Can manually test artifact storage

---

### Milestone 2: CLI Basics (Week 8)

**Deliverables:**

- ✅ Layer 7 CLI installed via `pip install -e .`
- ✅ Can create projects via `qf init`
- ✅ Can inspect projects via `qf list`, `qf show`
- ✅ Layer 5 shared foundations documented

**Success Criteria:**

- CLI commands work end-to-end
- Layer 5 foundation docs reviewed and approved

---

### Milestone 3: LLM Integration (Week 12)

**Deliverables:**

- ✅ OpenAI and Ollama text generation working
- ✅ A1111 and DALL-E image generation working
- ✅ Configurable via CLI

**Success Criteria:**

- Can generate text/images programmatically
- Can configure providers via `qf config`

---

### Milestone 4: First Loop Working (Week 18)

**Deliverables:**

- ✅ Showrunner, Gatekeeper, Lore Weaver, Scene Smith prompts complete
- ✅ Can run Hook Harvest loop via `qf run hook-harvest`
- ✅ Artifacts created and validated

**Success Criteria:**

- Full loop executes without errors
- Generated artifacts pass validation
- Human can review and understand what happened

---

### Milestone 5: Quickstart MVP (Week 22)

**Deliverables:**

- ✅ All 14 role prompts complete
- ✅ Quickstart workflow working (guided mode)
- ✅ Can generate complete manuscript from setup questions

**Success Criteria:**

- Quickstart runs end-to-end without errors
- Generated manuscript is coherent and playable
- User testing feedback positive

---

### Milestone 6: Public Release (Week 26)

**Deliverables:**

- ✅ All layers complete and tested
- ✅ Documentation comprehensive
- ✅ Installable via PyPI
- ✅ Works on Windows, macOS, Linux

**Success Criteria:**

- > 80% test coverage on Layer 6
- > 70% test coverage on Layer 7
- All documentation reviewed
- Installation tested on multiple platforms
- No critical bugs

---

## Risk Mitigation

### High-Risk Areas

**1. LLM Output Quality (Weeks 13-18)**

- **Risk:** AI role prompts don't produce good output
- **Mitigation:**
  - Extensive testing with real LLMs during Week 15-16
  - Iterate on prompts based on output quality
  - Have human review all generated content initially
  - Add refinement loops if needed

**2. Orchestration Complexity (Week 17)**

- **Risk:** Coordinating multiple roles is more complex than expected
- **Mitigation:**
  - Start with simplest loop (Hook Harvest)
  - Add loops incrementally
  - Extensive logging and debugging tools
  - Checkpoints allow recovery from failures

**3. Cross-Platform CLI Issues (Week 26)**

- **Risk:** CLI doesn't work on all platforms
- **Mitigation:**
  - Test on Windows, macOS, Linux throughout
  - Use CI/CD with multiple platforms
  - Avoid platform-specific dependencies
  - Test with different shells

### Medium-Risk Areas

**4. Provider API Changes**

- **Risk:** OpenAI/Ollama/A1111 APIs change
- **Mitigation:**
  - Pin dependency versions
  - Comprehensive error handling
  - Abstract provider interface allows swapping

**5. Performance Issues**

- **Risk:** Large projects are slow
- **Mitigation:**
  - SQLite for efficient queries
  - Lazy loading of artifacts
  - Caching where appropriate
  - Performance testing in Week 24

---

## Resource Requirements

### Human Oversight

**Required human involvement:**

**Weekly Reviews (2-3 hours/week):**

- Review epic completions
- Test deliverables
- Approve before next epic
- Course correct if needed

**Critical Review Points (4-6 hours each):**

- End of Phase 1 (Week 4): Review Layer 6 foundation
- End of Phase 2 (Week 8): Test CLI basics
- Week 15: Test first role execution with real LLM
- Week 18: Test first complete loop
- Week 22: Test quickstart end-to-end
- Week 26: Final QA before release

**Total Human Time: ~80-100 hours over 26 weeks**

---

### Compute Resources

**Development:**

- GitHub Actions CI/CD (free tier sufficient)
- Local development machines

**Testing:**

- OpenAI API credits: ~$50-100 for testing
- Ollama: Free (local)
- A1111: Free (local) or cloud GPU

**Production:**

- Users provide their own API keys
- No hosting costs for MVP

---

## Success Metrics

### Technical Metrics

- [ ] Layer 6: >80% test coverage
- [ ] Layer 7: >70% test coverage
- [ ] All 17 artifact types validated correctly
- [ ] All 8 quality bars implemented
- [ ] All 11 loops can execute
- [ ] All 14 roles have prompts

### User Experience Metrics

- [ ] Quickstart completes in <30 minutes (guided mode)
- [ ] Generated content passes human quality review
- [ ] CLI commands feel intuitive (user testing)
- [ ] Error messages are helpful
- [ ] Documentation is clear

### Distribution Metrics

- [ ] Installable via PyPI
- [ ] Works on Windows, macOS, Linux
- [ ] Works with Python 3.11, 3.12, 3.13
- [ ] Shell completion works in bash, zsh, fish

---

## Alternative Timelines

### Aggressive Timeline (16 weeks)

**Changes:**

- Skip some optional roles (Researcher, Translator)
- Implement only OpenAI provider initially (add Ollama later)
- Minimal documentation initially
- Skip advanced CLI features (Epic 10)

**Risk:** Higher technical debt, less robust

---

### Conservative Timeline (40 weeks)

**Changes:**

- More iteration on prompts (add buffer weeks)
- Extensive user testing between phases
- Implement all future providers (Gemini, Bedrock, Imagen)
- Add TUI/GUI alongside CLI
- Comprehensive testing on all platforms

**Risk:** Slower to market, scope creep

---

## Next Actions

### Immediate (This Week)

1. **Review this roadmap** with stakeholders
2. **Confirm timeline** (aggressive/moderate/conservative)
3. **Set up repositories:**
   - Create `pvliesdonk/questfoundry-lib`
   - Create `pvliesdonk/questfoundry-cli`
4. **Prepare AI agents:**
   - Set up GitHub Copilot
   - Set up Claude access
   - Create agent instruction templates

### Week 1 Start

1. **Begin Layer 6 Epic 1:** Repository setup
2. **Daily standups:** Quick check-ins on progress
3. **Track against plan:** Note any deviations early

---

## Appendices

### A. Epic Dependencies Graph

```
L6-E1 (Foundation)
  ↓
L6-E2 (Layer 3/4 Integration)
  ↓
L6-E3 (State Management) ← L7-E1 (CLI Setup) can start in parallel
  ↓                         ↓
L6-E4 (Artifacts)          L7-E2 (Basic Commands)
  ↓                         ↓
L6-E5 (Protocol Client) ← L5-E1 (Foundations) can start in parallel
  ↓                         ↓
L6-E6 (Providers)          L5-E2 (Orchestration Roles)
  ↓                         ↓
L6-E7 (Role Execution) ←  L5-E3 (Content Roles)
  ↓                         ↓
L6-E8 (Orchestration)      L5-E4 (Structure Roles)
  ↓                         ↓
L6-E9 (Safety/Quality)     L5-E5 (Style Roles)
  ↓                         ↓
L6-E10 (Export)            L5-E6 (Asset Roles)
  ↓                         ↓
L6-E11 (Docs/Polish)       L5-E7 (Publication Roles)
                            ↓
                           L5-E8 (Testing)
                            ↓
                           L5-E9 (Docs)

  L7-E3 (Config) depends on L6-E6
  L7-E4 (Validation) depends on L6-E9
  L7-E5 (Run) depends on L6-E8
  L7-E6 (Generate) depends on L6-E6, L5-E6
  L7-E7 (Quickstart) depends on L6-E8, L5-E7
  L7-E8 (Export) depends on L6-E10
  L7-E9-E12 (Polish) depends on all above
```

### B. Implementation Plan Files

- [Layer 6 Implementation Plan](06-libraries/IMPLEMENTATION_PLAN.md)
- [Layer 5 Implementation Plan](05-prompts/IMPLEMENTATION_PLAN.md)
- [Layer 7 Implementation Plan](07-ui/IMPLEMENTATION_PLAN.md)

### C. Key References

- [Layer 0 - North Star](00-north-star/WORKING_MODEL.md)
- [Layer 1 - Roles](01-roles/README.md)
- [Layer 2 - Dictionary](02-dictionary/README.md)
- [Layer 3 - Schemas](03-schemas/README.md)
- [Layer 4 - Protocol](04-protocol/README.md)
- [Layers 5-7 Vision](LAYERS_5-7_VISION.md)

---

**Document Version:** 1.0 **Last Updated:** 2025-10-31 **Status:** Ready for Implementation
