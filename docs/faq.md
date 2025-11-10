# Frequently Asked Questions (FAQ)

Common questions about the QuestFoundry specification.

---

## Table of Contents

- [General Questions](#general-questions)
- [Architecture & Design](#architecture--design)
- [Using QuestFoundry](#using-questfoundry)
- [For Developers](#for-developers)
- [For Authors](#for-authors)
- [AI & Automation](#ai--automation)
- [Contributing](#contributing)

---

## General Questions

### What is QuestFoundry?

QuestFoundry is a **specification** (not software) for creating interactive branching gamebooks. It
defines roles, workflows, data structures, protocols, and quality criteria that both humans and AI
agents can follow to collaboratively author complex choice-based narratives.

Think of it as a "recipe book" for building a collaborative writing studio, rather than the studio
itself.

### Is QuestFoundry a tool or an app?

No, QuestFoundry is a **specification**. It's documentation that describes:

- How a studio should work (Layer 0)
- What roles exist (Layer 1)
- What data structures to use (Layers 2-3)
- How components communicate (Layer 4)
- How to implement it (Layers 5-7)

However, the repository includes **validation tools** (`spec-tools`) for checking schemas and
artifacts.

### Who created QuestFoundry?

QuestFoundry is an open-source specification released under the MIT License. Check the
[repository](https://github.com/pvliesdonk/questfoundry-spec) for contributors and history.

### What's the difference between QuestFoundry and tools like Twine or Inkle?

| Feature            | QuestFoundry             | Twine          | Inkle          |
| ------------------ | ------------------------ | -------------- | -------------- |
| **Type**           | Specification            | Software       | Software       |
| **Approach**       | Multi-agent roles        | Single author  | Single author  |
| **AI Support**     | Built-in (role prompts)  | None           | None           |
| **Data Format**    | JSON (validated)         | HTML/CSS       | Ink script     |
| **Quality Checks** | 7 quality bars           | Manual         | Manual         |
| **Hot/Cold**       | Separate discovery/canon | Single version | Single version |
| **Traceability**   | TU system                | Git (manual)   | Git (manual)   |

QuestFoundry is **complementary**—you could build a Twine-like or Inkle-like tool that implements
the QuestFoundry spec.

---

## Architecture & Design

### Why 7 layers?

The layers separate **concerns** so each can evolve independently:

- **Layers 0-2**: Human-readable (vision, roles, data dictionary)
- **Layer 3**: Machine-readable (JSON schemas)
- **Layer 4**: Communication rules (protocol)
- **Layers 5-7**: Implementation (prompts, code, UI)

This allows:

- Authors to understand the system without reading code
- Developers to validate data without understanding narrative theory
- AI models to be swapped without changing the spec

### What is Hot vs. Cold?

**Hot** and **Cold** are **two sources of truth**:

- **Hot**: Discovery space for drafts, hooks, spoilers, experimentation
- **Cold**: Curated canon and player-safe surfaces, validated by Gatekeeper

**Why separate them?**

- **Safety**: Player-Narrator (PN) never sees spoilers in Hot
- **Quality**: Cold is always validated against quality bars
- **Freedom**: Hot allows experimentation without breaking canon
- **Reproducibility**: Cold snapshots are immutable and exportable

### What are Trace Units (TUs)?

**Trace Units** are work orders that track all changes. Each TU has:

- Unique ID: `TU-YYYY-MM-DD-RoleCode##`
- Type: topology, prose, style, canon, codex, policy, docs
- Status: `hot-proposed → stabilizing → gatecheck → cold-merged`
- Quality bars affected

TUs ensure **traceability**—every change can be tracked back to its origin.

### Why JSON Schema Draft 2020-12?

JSON Schema Draft 2020-12 is the latest stable specification with:

- Better validation features ($anchor, $dynamicRef)
- Improved error messages
- Wide tool support (Python, TypeScript, etc.)
- Clear semantics for $id and $ref

### What are the 7 Quality Bars?

The **Quality Bars** are validation criteria enforced by the Gatekeeper:

1. **Integrity** — No dead references, valid IDs
2. **Reachability** — Keystones reachable from start
3. **Nonlinearity** — Hubs/loops/gateways meaningful
4. **Gateways** — Coherent diegetic checks
5. **Style** — Voice/register/motifs consistent
6. **Determinism** — Assets promised are present
7. **Presentation** — No spoilers, accessibility baseline

See [`QUALITY_BARS.md`](../00-north-star/QUALITY_BARS.md) for details.

---

## Using QuestFoundry

### How do I start using QuestFoundry?

It depends on your role:

**If you're an author:**

1. Read [Getting Started Guide](getting-started.md)
2. Study [Working Model](../00-north-star/WORKING_MODEL.md)
3. Pick a workflow loop (e.g., Story Spark)
4. Try creating artifacts using templates from `02-dictionary/artifacts/`

**If you're a developer:**

1. Clone the repository
2. Install `spec-tools`: `cd spec-tools && uv sync`
3. Explore JSON schemas in `03-schemas/`
4. Follow [Implementation Roadmap](../IMPLEMENTATION_ROADMAP.md)

**If you're using AI:**

1. Browse prompts in `05-prompts/`
2. Read [Usage Guide](../05-prompts/USAGE_GUIDE.md)
3. Upload a role's system prompt to Claude/ChatGPT
4. Test with example conversations

### Do I need to use all 15 roles?

No! Roles have **dormancy** levels:

**Always On:**

- Showrunner, Gatekeeper

**Default On:**

- Plotwright, Scene Smith, Style Lead, Lore Weaver, Codex Curator

**Optional:**

- Researcher, Art Director, Illustrator, Audio Director, Audio Producer, Translator

**Downstream:**

- Book Binder, Player-Narrator

For a minimal project, you might only use:

- Showrunner
- Plotwright
- Scene Smith
- Gatekeeper

### Can I use QuestFoundry without AI?

**Yes!** QuestFoundry is designed for **humans or AI**. The roles can be played by:

- Individual authors (one person playing multiple roles)
- Teams of human collaborators
- AI agents (using Layer 5 prompts)
- Hybrid teams (humans + AI)

The key is following the **protocol** and **artifact schemas** so everyone (human or AI) can
collaborate.

### What file formats does QuestFoundry use?

**Input:**

- Markdown (`.md`) for templates and documentation
- JSON (`.json`) for artifacts and schemas
- YAML (`.yaml`) for configuration

**Output (from Book Binder):**

- EPUB (`.epub`) for e-readers
- HTML/CSS for web
- Plain text for accessibility
- Audiobook scripts for narration

### How do I validate my artifacts?

Use `spec-tools`:

```bash
cd spec-tools
uv sync

# Validate a hook card
uv run qfspec-check-instance hook_card my-hook.json

# Validate a protocol envelope
uv run qfspec-check-envelope my-message.json

# Validate all schemas
uv run qfspec-validate
```

See [`spec-tools/README.md`](../spec-tools/README.md) for details.

---

## For Developers

### How do I implement QuestFoundry in my tool?

Follow the [Implementation Roadmap](../IMPLEMENTATION_ROADMAP.md):

**Phase 1: Schema Validation (Weeks 1-4)**

- Integrate JSON Schema validators
- Implement two-pass envelope validation
- Create artifact parsers

**Phase 2: Protocol Handlers (Weeks 5-8)**

- Implement intent routing
- Build state machines for hooks & TUs
- Create protocol clients

**Phase 3: Role Agents (Weeks 9-16)**

- Integrate LLM APIs (Claude, ChatGPT)
- Load system prompts from Layer 5
- Implement intent handlers

**Phase 4: Hot/Cold Storage (Weeks 17-20)**

- Separate Hot & Cold databases
- Implement Gatekeeper validation
- Create snapshot tagging

**Phase 5: Export Engine (Weeks 21-24)**

- Build EPUB generator
- Create web export
- Implement view logging

**Phase 6: Testing & Polish (Weeks 25-26)**

- End-to-end tests
- Performance optimization
- Documentation

### What languages can I use?

QuestFoundry is **language-agnostic**. The specification uses:

- JSON for data (portable)
- JSON Schema for validation (tool support in most languages)
- Markdown for documentation (human-readable)

You can implement in:

- **Python** (current validation tools use this)
- **TypeScript/JavaScript** (planned SDK)
- **Rust**, **Go**, **C#**, etc.

### How do I add a new artifact type?

1. Create markdown template in `02-dictionary/artifacts/{artifact_name}.md`
2. Generate JSON schema:
   ```bash
   qfspec-generate-schema {artifact_name}
   ```
3. Validate schema:
   ```bash
   qfspec-validate
   ```
4. Add to schema index
5. Create example instances
6. Update protocol intents if needed

### How do I extend the protocol?

1. Document new intent in `04-protocol/INTENTS.md`
2. Define payload schema
3. Add example in `04-protocol/EXAMPLES/{intent}.json`
4. Update state machines if needed (in `04-protocol/LIFECYCLES/`)
5. Validate with `qfspec-check-envelope`
6. Submit PR

### Where can I find example code?

**Validation tools:**

- `spec-tools/src/` — Python validators

**Example artifacts:**

- `04-protocol/EXAMPLES/` — 20+ example messages

**Planned:**

- Layer 6 will include reference implementations in Python & TypeScript

---

## For Authors

### Do I need programming knowledge?

**No!** Layers 0-2 are designed for non-programmers:

- **Layer 0**: Vision and principles (plain English)
- **Layer 1**: Role descriptions (what each role does)
- **Layer 2**: Data templates (fill-in-the-blank)

You only need programming knowledge if you're building tools (Layers 3-7).

### How do I organize a large branching story?

QuestFoundry uses **topology** (structure) + **prose** (content):

1. **Plotwright** designs topology:
   - Hubs (sections with 3+ choices)
   - Loops (paths that revisit sections)
   - Gateways (conditional checks)

2. **Scene Smith** writes prose to fit topology

3. **Gatekeeper** validates:
   - All sections reachable
   - Nonlinearity meaningful
   - No dead ends

See [`00-north-star/LOOPS/story_spark.md`](../00-north-star/LOOPS/story_spark.md) for a walkthrough.

### How do I avoid spoiling players?

QuestFoundry enforces **spoiler hygiene**:

- **Hot** contains spoilers (hooks, canon packs, internal notes)
- **Cold** contains only player-safe content (codex entries, front matter)
- **Player-Narrator (PN)** only accesses Cold

The protocol enforces this with `safety.player_safe` and `safety.sot` fields.

See [`00-north-star/SPOILER_HYGIENE.md`](../00-north-star/SPOILER_HYGIENE.md).

### Can I use QuestFoundry for non-game books?

**Yes!** QuestFoundry works for any **branching narrative**:

- Choose Your Own Adventure books
- Interactive fiction
- Educational scenarios
- Training simulations
- Branching documentaries
- RPG modules

The "gamebook" terminology is for convenience—it applies to any choice-based narrative.

### How do I handle translations?

Use the **Translator** role:

1. Create `language_pack` artifact for each language
2. Create `register_map` for terminology consistency
3. Translator maintains parallel Cold versions
4. Book Binder exports language-specific views

See:

- `02-dictionary/artifacts/language_pack.md`
- `02-dictionary/artifacts/register_map.md`
- `01-roles/charters/translator.md`

---

## AI & Automation

### Can I use QuestFoundry with Claude, ChatGPT, or Gemini?

**Yes!** Layer 5 provides system prompts for all 15 roles, designed for:

- **Claude** (Anthropic)
- **ChatGPT** (OpenAI)
- **Gemini** (Google)

See [`05-prompts/USAGE_GUIDE.md`](../05-prompts/USAGE_GUIDE.md) for upload instructions.

### How do I upload prompts to my LLM?

**For Claude:**

1. Open Claude Projects
2. Create new project
3. Add `system_prompt.md` to "Project Knowledge"
4. Start conversation

**For ChatGPT:**

1. Create custom GPT
2. Paste system prompt in "Instructions"
3. Upload example conversations
4. Save GPT

See detailed steps in [`05-prompts/USAGE_GUIDE.md`](../05-prompts/USAGE_GUIDE.md).

### Can AI agents communicate with each other?

**Yes!** That's the purpose of Layer 4 (Protocol). AI agents can:

- Send messages using the envelope format
- Use intents to trigger actions (`hook.create`, `tu.advance`, etc.)
- Exchange artifacts validated by Layer 3 schemas
- Follow state machines for workflows

**Future (Layer 6):**

- SDK will provide agent communication libraries
- Multi-agent orchestration tools

### How do I prevent AI from generating spoilers?

The protocol includes **safety constraints**:

```json
{
  "safety": {
    "player_safe": true,
    "sot": "cold"
  }
}
```

If `player_safe: true` and `sot: "cold"`, the message is safe for Player-Narrator.

**Enforcement:**

- Gatekeeper validates before merging Hot → Cold
- PN agents reject messages that don't meet safety criteria
- Presentation quality bar checks for spoilers

### Can AI play the Gatekeeper role?

**Yes, but carefully.** Gatekeeper is a **critical role** that enforces quality. When using AI:

1. **Automate objective checks** (Integrity, Reachability, Determinism)
2. **Human review for subjective checks** (Style, Gateways, Nonlinearity)
3. **Always review gate failures** before rejecting TUs

See [`01-roles/charters/gatekeeper.md`](../01-roles/charters/gatekeeper.md).

---

## Contributing

### How do I contribute to the specification?

1. Read [`CONTRIBUTING.md`](../CONTRIBUTING.md)
2. Understand the [Working Model](../00-north-star/WORKING_MODEL.md)
3. Create a **Trace Unit (TU)** describing your change
4. Submit a PR referencing the TU
5. Wait for Gatekeeper review

### What kind of contributions are welcome?

**Documentation improvements:**

- Clarifying confusing sections
- Adding examples
- Fixing typos

**Specification enhancements:**

- New artifact types
- New intents
- New roles
- New quality bars

**Tooling:**

- Validation improvements
- Test coverage
- CI/CD enhancements

**Examples:**

- Sample artifacts
- Example workflows
- Tutorial content

### Do I need to create a Trace Unit for every change?

**TUs are for content changes:**

- Topology, prose, style, canon, codex, policy

**ADRs are for architectural changes:**

- Adding/removing layers
- Changing protocol rules
- Modifying core principles

**Small fixes don't need TUs:**

- Typos in documentation
- Formatting fixes
- Link corrections

See [`00-north-star/TRACEABILITY.md`](../00-north-star/TRACEABILITY.md).

### How do I report a bug?

1. Check [existing issues](https://github.com/pvliesdonk/questfoundry-spec/issues)
2. If not found, [open a new issue](https://github.com/pvliesdonk/questfoundry-spec/issues/new)
3. Include:
   - Description of the problem
   - Steps to reproduce
   - Expected vs. actual behavior
   - Layer affected (0-7)

### Can I use QuestFoundry in my commercial project?

**Yes!** QuestFoundry is licensed under **MIT License**, which allows:

- Commercial use
- Modification
- Distribution
- Private use

You must include the license and copyright notice.

See [`LICENSE`](../LICENSE) for full terms.

---

## Still Have Questions?

- 📖 **Documentation:** [questfoundry.liesdonk.nl](https://questfoundry.liesdonk.nl)
- 💬 **Discussions:**
  [GitHub Discussions](https://github.com/pvliesdonk/questfoundry-spec/discussions)
- 🐛 **Issues:** [GitHub Issues](https://github.com/pvliesdonk/questfoundry-spec/issues)
- 📧 **Contact:** See [CONTRIBUTING.md](../CONTRIBUTING.md) for contact info

---

**Last Updated:** 2025-11-05
