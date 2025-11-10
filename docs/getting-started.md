# Getting Started with QuestFoundry

Welcome to **QuestFoundry**, a layered specification for creating interactive nonlinear gamebooks.
This guide will help you understand the system and start using it effectively.

---

## Table of Contents

1. [What is QuestFoundry?](#what-is-questfoundry)
2. [Who is This For?](#who-is-this-for)
3. [Understanding the Layers](#understanding-the-layers)
4. [Quick Start by Role](#quick-start-by-role)
5. [Your First Loop](#your-first-loop)
6. [Next Steps](#next-steps)

---

## What is QuestFoundry?

QuestFoundry is a **multi-agent, compositional studio specification** for creating interactive
branching gamebooks. Unlike traditional single-author tools, QuestFoundry:

- **Separates concerns** into 7 clear layers (vision → roles → data → schemas → protocol → prompts →
  code)
- **Defines 15 specialized roles** that can be played by humans or AI agents
- **Uses structured artifacts** validated by JSON schemas
- **Tracks all changes** with Trace Units (TUs)
- **Separates discovery from canon** with Hot/Cold sources of truth
- **Enforces quality** with 7 quality bars before merging to production

Think of it as a **specification for a studio**, not just a tool. It's like a detailed blueprint
that tells everyone (human or AI) how to collaborate on creating complex, branching narratives.

---

## Who is This For?

### 🎨 Interactive Fiction Authors

If you write choice-based stories, QuestFoundry provides:

- Clear workflows for managing complex branching narratives
- Quality assurance processes to catch dead ends and broken references
- Separation between spoiler content and player-facing material
- Localization and accessibility built-in

**Start with:** [Layer 0: North Star](../00-north-star/README.md) to understand the vision

### 🤖 AI/LLM Developers

If you're building AI-powered writing tools, QuestFoundry provides:

- System prompts implementing 15 specialized writing roles
- JSON schemas for validating structured outputs
- Protocol specifications for agent-to-agent communication
- State machines for managing complex workflows

**Start with:** [Layer 4: Protocol](../04-protocol/ENVELOPE.md) and
[Layer 5: Prompts](../05-prompts/USAGE_GUIDE.md)

### 🛠️ Tool Builders

If you're implementing gamebook authoring tools, QuestFoundry provides:

- Complete JSON schema specifications (Draft 2020-12)
- Validation toolkit (`spec-tools`)
- Implementation roadmap with clear milestones
- Example artifacts and test cases

**Start with:** [Layer 3: Schemas](../03-schemas/README.md) and
[Validation Tools](../spec-tools/README.md)

### 📚 Specification Designers

If you're interested in multi-agent system design, QuestFoundry demonstrates:

- Layered architecture for complex specifications
- Role-based collaboration patterns
- State machine-driven workflows
- Hot/Cold separation for discovery vs. production

**Start with:** [Architecture Overview](architecture.md) and [ADRs](../DECISIONS/)

---

## Understanding the Layers

QuestFoundry is organized into **7 layers**, each building on the previous:

### Layer 0: North Star (Vision)

**What it is:** The "why" and "what" of QuestFoundry—vision, principles, operating model, quality
bars, and workflow loops.

**Read if you want to:** Understand the philosophy and approach.

**Key documents:**

- [`00-north-star/README.md`](../00-north-star/README.md) — Navigator
- [`WORKING_MODEL.md`](../00-north-star/WORKING_MODEL.md) — How the studio operates
- [`QUALITY_BARS.md`](../00-north-star/QUALITY_BARS.md) — What "good" means

### Layer 1: Roles (Who Does What)

**What it is:** 15 specialized roles with clear charters, responsibilities, and workflows.

**Read if you want to:** Understand who does what in the studio.

**Key documents:**

- [`01-roles/README.md`](../01-roles/README.md) — Role overview
- [`charters/`](../01-roles/charters/) — Detailed role charters
- [`interfaces/`](../01-roles/interfaces/) — How roles interact

### Layer 2: Common Language (Shared Vocabulary)

**What it is:** Data dictionary with 17 artifact templates (Hook Cards, Trace Units, Canon Packs,
etc.)

**Read if you want to:** Understand what artifacts the studio produces.

**Key documents:**

- [`02-dictionary/README.md`](../02-dictionary/README.md) — Dictionary overview
- [`artifacts/`](../02-dictionary/artifacts/) — 17 artifact templates

### Layer 3: Schemas (Machine-Readable Specs)

**What it is:** 21 JSON schemas conforming to JSON Schema Draft 2020-12.

**Read if you want to:** Validate artifacts or build tools.

**Key documents:**

- [`03-schemas/README.md`](../03-schemas/README.md) — Schema generation methodology
- [`*.schema.json`](../03-schemas/) — 21 schema files
- [Canonical URLs](https://questfoundry.liesdonk.nl/schemas/) — Hosted schemas

### Layer 4: Protocol (Communication Rules)

**What it is:** Message envelopes, intents, and state machines for role-to-role communication.

**Read if you want to:** Understand how agents communicate.

**Key documents:**

- [`ENVELOPE.md`](../04-protocol/ENVELOPE.md) — Message format specification
- [`INTENTS.md`](../04-protocol/INTENTS.md) — Intent catalog
- [`LIFECYCLES/`](../04-protocol/LIFECYCLES/) — State machines

### Layer 5: Prompts (AI Agent Implementations)

**What it is:** System prompts implementing Layer 1 roles for Claude/ChatGPT/Gemini.

**Read if you want to:** Use AI agents to play roles.

**Key documents:**

- [`USAGE_GUIDE.md`](../05-prompts/USAGE_GUIDE.md) — How to upload prompts to LLMs
- [`{role_name}/system_prompt.md`](../05-prompts/) — Individual role prompts

### Layer 6: Libraries (Software SDKs)

**What it is:** Python/TypeScript SDKs for building tools (planned).

**Status:** 📋 Planned for future implementation.

### Layer 7: UI (User Interfaces)

**What it is:** CLI, GUI, and Player-Narrator interfaces (planned).

**Status:** 📋 Planned for future implementation.

---

## Quick Start by Role

### I'm a **Story Creator** (Author/Writer)

**Goal:** Understand how to write branching stories with QuestFoundry.

**Path:**

1. Read [Working Model](../00-north-star/WORKING_MODEL.md) (10 min)
2. Review [Quality Bars](../00-north-star/QUALITY_BARS.md) (5 min)
3. Explore [Loops](../00-north-star/LOOPS/) to understand workflows
4. Pick a playbook from [Playbooks](../00-north-star/PLAYBOOKS/)
5. Try running a **Story Spark** loop

**What you'll learn:** How to organize your creative process, maintain quality, and collaborate with
others (or AI).

### I'm a **Tool Developer**

**Goal:** Build software that implements QuestFoundry.

**Path:**

1. Read [Protocol Specification](../04-protocol/ENVELOPE.md) (15 min)
2. Review [JSON Schemas](../03-schemas/) (20 min)
3. Install and run [`spec-tools`](../spec-tools/README.md)
4. Study [Example Messages](../04-protocol/EXAMPLES/)
5. Follow [Implementation Roadmap](../IMPLEMENTATION_ROADMAP.md)

**What you'll learn:** How to validate artifacts, implement protocol handlers, and integrate with
the ecosystem.

### I'm an **AI/LLM Engineer**

**Goal:** Use QuestFoundry prompts with language models.

**Path:**

1. Read [Prompt Usage Guide](../05-prompts/USAGE_GUIDE.md) (10 min)
2. Pick a role (start with **Plotwright** or **Scene Smith**)
3. Upload the system prompt to Claude/ChatGPT
4. Review [Example Conversations](../05-prompts/) for the role
5. Test with sample artifacts

**What you'll learn:** How to configure AI agents to play specific roles in the studio.

### I'm a **Researcher/Evaluator**

**Goal:** Understand the specification design.

**Path:**

1. Read [Architecture Overview](architecture.md) (10 min)
2. Review [ADRs](../DECISIONS/) for design decisions
3. Study [Layer 4 Protocol](../04-protocol/README.md)
4. Examine [Hot/Cold Semantics](../00-north-star/SOURCES_OF_TRUTH.md)
5. Check [Traceability System](../00-north-star/TRACEABILITY.md)

**What you'll learn:** Why QuestFoundry is designed the way it is, and how it compares to other
systems.

---

## Your First Loop

Let's walk through a simple **Story Spark** loop to create the beginning of a story.

### Prerequisites

- Basic understanding of interactive fiction
- Text editor
- (Optional) AI assistant with QuestFoundry prompts

### Step 1: Define Project Scope

Create a `project_metadata.json` describing your gamebook:

```json
{
  "title": "The Mystery of Oakwood Manor",
  "genre": "detective-noir",
  "target_sections": 50,
  "target_words_per_section": 150,
  "branch_factor": 2.5,
  "estimated_playtime_minutes": 30
}
```

### Step 2: Story Spark (Brainstorming)

Run a **Story Spark** loop (see [guide](../00-north-star/LOOPS/story_spark.md)):

**Roles involved:**

- **Showrunner** — Coordinates the loop
- **Plotwright** — Sketches story structure
- **Scene Smith** — Drafts opening scene

**Outputs:**

- Draft topology (hub-spoke structure)
- Opening scene prose
- Hook cards for follow-up ideas

### Step 3: Hook Harvest

Capture follow-up ideas as **Hook Cards** (`hook_card.json`):

```json
{
  "hook_id": "H-001",
  "title": "Explore the library clue",
  "description": "Player finds a torn letter in the library—needs deeper lore",
  "priority": "medium",
  "proposed_by": "scene_smith",
  "status": "proposed"
}
```

### Step 4: Gatekeeper Review

**Gatekeeper** validates against quality bars:

- ✅ Integrity: No broken references
- ✅ Reachability: All scenes reachable
- ✅ Style: Voice consistent
- ✅ Presentation: No spoilers in player text

### Step 5: Merge to Cold

Approved content moves from **Hot** (discovery) to **Cold** (canon):

```
Hot @ 2025-11-05 → Gatekeeper Pass → Cold @ 2025-11-05
```

### Step 6: Create Snapshot

Tag a Cold snapshot for export:

```bash
git tag cold-2025-11-05
```

### Step 7: Export View

**Book Binder** exports an EPUB:

```bash
qf-export --snapshot cold-2025-11-05 --format epub
```

---

## Next Steps

### Dive Deeper

- **Learn the 15 Roles:** Read [Role Charters](../01-roles/charters/)
- **Explore Artifacts:** Browse [Artifact Templates](../02-dictionary/artifacts/)
- **Master Quality Bars:** Study [Quality Bar Criteria](../00-north-star/QUALITY_BARS.md)
- **Run More Loops:** Try [Hook Harvest](../00-north-star/LOOPS/hook_harvest.md) or
  [Lore Deepening](../00-north-star/LOOPS/lore_deepening.md)

### Join the Community

- **Report issues:** [GitHub Issues](https://github.com/pvliesdonk/questfoundry-spec/issues)
- **Contribute:** Read [Contributing Guide](../CONTRIBUTING.md)
- **Discuss:** [GitHub Discussions](https://github.com/pvliesdonk/questfoundry-spec/discussions)

### Build Tools

- **Install spec-tools:** Follow [Installation Guide](../spec-tools/README.md)
- **Read roadmap:** [Implementation Roadmap](../IMPLEMENTATION_ROADMAP.md)
- **Check examples:** [Protocol Examples](../04-protocol/EXAMPLES/)

---

## Frequently Asked Questions

See the [FAQ](faq.md) for common questions.

---

## Need Help?

- 📖 **Documentation:** [questfoundry.liesdonk.nl](https://questfoundry.liesdonk.nl)
- 💬 **Discussions:**
  [GitHub Discussions](https://github.com/pvliesdonk/questfoundry-spec/discussions)
- 🐛 **Issues:** [GitHub Issues](https://github.com/pvliesdonk/questfoundry-spec/issues)
- 📧 **Email:** Check the [CONTRIBUTING.md](../CONTRIBUTING.md) for contact info

---

**Last Updated:** 2025-11-05
