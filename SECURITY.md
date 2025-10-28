# Security & Responsible Disclosure

QuestFoundry is a **docs-first spec**. We don’t ship executables here yet, but security still matters—especially around **secrets**, **spoiler leaks**, and **supply-chain hygiene** when this spec is embedded into tools.

This document explains how to report issues safely and what we treat as a security concern.

---

## What counts as a security issue here?

- **Secrets exposure**  
  API keys, tokens, credentials, or private contact info committed by mistake.

- **Spoiler leakage into player surfaces**  
  A spec change or template that would cause **Cold** exports (manuscript, codex, captions, PN) to leak twists, gate conditions, internal labels, or determinism details. (Yes, this is “content security” for our use-case.)

- **Malicious/unsafe content patterns**  
  Templates or guidance that encourage unsafe HTML/JS embedding, executable macros, or remote-code execution in future Layers (3–7).

- **Supply-chain red flags** (in scaffolding)  
  Instructions that would fetch unpinned code, disable verification, or weaken sandboxing when implementers build tools around this spec.

> **Not security**: Typos, ordinary style disagreements, missing commas, or debates about narrative taste. Please use regular issues/PRs for those.

---

## How to report

- **Email (preferred):** <security@questfoundry.example>  
  Include:
  - A concise description of the issue and why it’s a risk
  - Minimal reproduction steps or the file/line references
  - Impact scope (who is affected; Hot vs Cold)
  - Suggested mitigation if you have one

- **Private issue:** Open a ticket titled `Security (private)` with just a pointer; a maintainer will move it to a confidential channel.

We aim to acknowledge within **72 hours** and provide a remediation plan or next steps shortly after.

---

## Responsible disclosure policy

- Please **do not** create public issues or PRs containing sensitive details.  
- Do not share proof-of-concept exploits or spoiler payloads publicly.  
- Give us a reasonable window to assess and remediate before disclosure.  
- We’ll credit reporters in release notes (if desired) once a fix lands.

---

## What we do on our side

- Triage as **Showrunner**; assess risk as **Gatekeeper** (Quality Bars + Presentation Safety).  
- Create a **Trace Unit (TU)** for remediation work (kept private until safe).  
- Patch the docs/templates; add tests/checklists where applicable.  
- If a **Cold** surface was impacted, we’ll note it in the **View Log** policy and recommend re-exports.

---

## Tips for reporters (what helps us fix fast)

- Point to exact files/sections (paths + headings).  
- Tell us whether it breaks **Hot/Cold boundaries** or **Quality Bars**.  
- If it involves exports, specify which surfaces (manuscript/codex/captions/PN).  
- If it’s supply-chain, list commands or scripts that are risky and why.

---

## PGP / encrypted reports

If you need encryption, ask via email and we’ll share a temporary PGP key for your disclosure.

---

## Thank you

Security for a narrative spec means keeping **players safe from spoilers** and **builders safe from bad patterns**. Thanks for helping us keep both sides clean.
