# Architecture Decision Record (ADR) — Template

> **Purpose:** Record cross-book **policy/standards** decisions that outlive a single TU. Keep the ADR short, cite the Bars it stabilizes, and link the slice that triggered it. Player-safe by default; if spoiler risk exists, keep specifics abstract.

---

## ADR ID

```

ADR-<YYYYMMDD>-<seq>-<short-slug>

```

*Example:* `ADR-20251029-01-diegetic-gate-lines`

---

## Status

```

Proposed | Accepted | Superseded by ADR-<id> | Deprecated

```

---

## Context

> What forced this decision? Tie to **Quality Bars** and the triggering work.

- Trigger: TU `<id>` — `<loop>` — `<slice>`
- Bars pressed: **<Integrity | Reachability | Nonlinearity | Gateways | Style | Presentation | Accessibility>**
- Symptoms (player-safe): <1–3 bullets>
- Prior attempts: <brief notes or links to TUs/notes>

---

## Decision

> The policy, stated crisply. Prefer MUST/SHOULD/MAY language.

- **We DECIDE:** <one or two sentences>
- Scope: <this book | this repo | all QuestFoundry projects>
- Owner(s): <role(s) responsible for enforcing/maintaining>

---

## Rationale

> Why this option beats the alternatives—short and specific.

- <reason 1>
- <reason 2>
- <reason 3>

---

## Consequences

> What gets easier/harder. Include migration or adoption notes.

**Positive**

- <bullet>
- <bullet>

**Negative**

- <bullet> (mitigation: <how>)

**Migration**

- Effective date/snapshot:
- Who updates what: <roles & artifacts>
- Cutover plan: <steps or “on next TU touching …”>

---

## Policy & Examples (player-safe)

> Tiny, reusable examples that **don’t** reveal canon or internals.

- **Rule:** <short rule>
  - *Example:* “<safe line>”
  - *Counterexample:* “<what to avoid>”

*(Repeat if needed.)*

---

## Interactions & Ownership

- Affected roles: <list>  
- Handshakes to update: `01-roles/interfaces/*.md` (links)  
- Templates to update: `01-roles/templates/*.md` (links)  
- Binder/Translator anchor policy: <if applicable>

---

## Alternatives Considered

- **Option A:** <summary> — rejected because <reason>
- **Option B:** <summary> — rejected because <reason>
- **Do nothing:** <risk of inaction>

---

## Verification

> How we’ll know the ADR is working.

- Gatekeeper checks: <which Bars and quick test>
- PN dry-run signals: <expected reduction in tags, e.g., `gate-friction`>
- Binding: <anchor/label health expectations>

---

## References & Lineage

- TUs: <ids>  
- Gatecheck reports: <ids>  
- View Logs: <ids> (if export policy)  
- Canon Packs / Style Addenda / Language Packs touched: <ids>  
- Related ADRs: <ids> (supersedes/depends-on)

---

## Changelog

```

YYYY-MM-DD — Proposed by <name/agent>
YYYY-MM-DD — Accepted by <owner> (roles present: <list>)
YYYY-MM-DD — Superseded by ADR-<id> (reason)

```
