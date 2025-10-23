# Change Log — v3.3-qa (2025-10-22)

### Added
- Annotated examples for **every schema** under `examples/contracts/`: `artlist`, `claim_registry`, `feedback`, `project_config`, `research_query`, `research_packet`, `session_line` (new).
- Release README focused on onboarding and flow.

### Changed
- Harmonized naming across examples: consistent IDs (`S-089`, `B-023`, `IMG-001`).
- Clarified art pipeline terms (distinguish `artlist` vs `art_plan`).

### Verified
- Examples in `examples/workflow/` reference beats/sections that exist in the contract examples.
- Feedback loop docs (`README_FEEDBACK.md`, `README_RESEARCH.md`) match `schemas/feedback.schema.json` enums and fields.

### Notes
- Protocol version for feedback events remains **3.2** to preserve compatibility.
- No schema-breaking changes were made.
