# Architectural Decision Records (ADRs)

ADRs capture **policy-level** choices that shape QuestFoundry’s rules: roles, bars, SoT boundaries, loop taxonomy, repository layout, etc. They are **not** for everyday content edits (use a **Trace Unit**, TU, for that).

> TL;DR — If you’re **changing the rules of the studio**, write an ADR. If you’re **working within the rules**, open a TU and a normal PR.

---

## 1) When to write an ADR (vs. a TU)

Use an **ADR** when a change:

- Adds/removes/renames a **role** or alters its authority/dormancy policy.
- Changes **Hot/Cold** boundaries, **snapshot** policy, or the **merge train**.
- Alters **Quality Bars**, **PN Principles**, **Spoiler Hygiene**, or **Accessibility** baselines.
- Introduces/retire­s a **loop** or **playbook**, or redefines their hand-offs.
- Reorganizes the **layered repo** structure or cross-layer contract (e.g., where schemas live).
- Materially affects downstream implementations in Layers 3–7.

Use a **TU** when:

- You’re drafting prose, canon, codex pages, style addenda, plans, translations.
- You’re running the existing loops/playbooks as-is.
- You’re fixing typos, links, or making clarifications that don’t move policy.

---

## 2) File naming & location

All ADRs live in this directory as flat files:

```

DECISIONS/
ADR-YYYYMMDD-<slug>.md

```

Examples:

- `ADR-20251028-rename-plot-drafter-to-plotwright.md`
- `ADR-20251029-cold-snapshot-tagging-policy.md`

---

## 3) ADR lifecycle & states

Each ADR has a **Status**:

- `Proposed` — under discussion; open PR exists.
- `Accepted` — merged; now **normative** for the spec.
- `Superseded by ADR-YYYYMMDD-<slug>` — replaced by a newer decision.
- `Rejected` — discussed and deliberately not taken (kept for context).
- `Deprecated` — temporarily in force but scheduled for replacement/removal.

ADRs are immutable after merge except for:

- Fixing typos/links (non-semantic).
- Appending a **Superseded** footer when replaced.

---

## 4) Process (lightweight)

1. **Open a Discussion or Draft PR** with your ADR file.
2. Link any motivating **TUs** (e.g., repeated friction discovered in loops).
3. Collect focused feedback; resolve comments.
4. **Gatekeeper** checks for conflicts with Quality Bars / PN boundaries.
5. **Showrunner** decides **Accept / Reject** (or requests revisions).
6. Merge → tag **Accepted**. If it **Supersedes** another ADR, add the backlink.

> Pro tip: Keep ADRs small and crisp. One decision per file.

---

## 5) Template

Copy this to start a new ADR:

```markdown
# ADR: <concise title>

- **ID**: ADR-YYYYMMDD-<slug>
- **Status**: Proposed | Accepted | Rejected | Deprecated | Superseded by ADR-YYYYMMDD-<slug>
- **Date**: YYYY-MM-DD
- **Authors**: <names/handles>
- **Related TUs**: <tu-ids, optional>
- **Areas**: Roles | SoT | Quality Bars | Loops | PN | Repo | Localization | Art/Audio | Accessibility | Other

## Context

<What problem or tension exists? Include constraints, prior decisions, and why the current rules aren’t sufficient.>

## Decision

<The rule we are adopting. Write it as normative guidance. If renaming/restructuring, specify exact new names/paths.>

## Consequences

### Positive

<What gets better? Clarity, safety, velocity, UX…>

### Negative / Risks

<Migration pain, temporary churn, open questions.>

## Alternatives Considered

<Short bullets. Why not each alternative?>

## Migration

<Exactly what to change in the repo (paths/files), and which docs must be updated (links, indices). Timebox if phased.>

## Compatibility

<Impact on Layers 3–7 (future). Any guarantees or breakages to call out.>

## Appendix (optional)

<Diagrams, examples, or rationale that helps future readers.>
```

---

## 6) Cross-referencing & traceability

- Link ADRs from the docs they affect (e.g., add a small **“Decision History”** section to `WORKING_MODEL.md` with ADR IDs).
- If an ADR **mandates** doc changes, include them in the **same PR** or open follow-up PRs that reference the ADR ID.
- TUs can reference ADRs when they execute work **under** the new policy.

---

## 7) Review expectations

- Keep scope tight; avoid omnibus ADRs.
- Use concrete examples in the **Decision** section.
- Prefer minimal, incremental migrations; avoid breaking readers’ mental model unless necessary.
- If an ADR touches **Spoiler Hygiene** or **Accessibility**, ping those reviewers explicitly.

---

## 8) FAQ

**Q: Can I bundle an ADR with large content edits?**
A: No. Split the **policy** (ADR) from the **execution** (TUs/regular docs PRs). It sharpens review and rollbacks.

**Q: Do we need an ADR to rename a file?**
A: Only if it changes the **documented structure** or the meaning of a canon term. Otherwise, a TU + PR is fine.

**Q: Where do deprecated decisions go?**
A: They remain here with `Status: Superseded by ADR-…` so future readers can trace evolution.

---

**Purpose of this folder**
This directory is the **ledger of rule changes**. If someone asks _“Why is the studio like this?”_, the answer lives here with dates and rationale.

```

```
