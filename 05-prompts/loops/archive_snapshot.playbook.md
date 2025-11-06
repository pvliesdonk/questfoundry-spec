# Archive Snapshot — Executable Loop Playbook

**Category:** Export **Abbreviation:** AS **Schema:**
<https://questfoundry.liesdonk.nl/schemas/tu_brief.schema.json>

> **Note:** Full specification pending in Layer 0. This playbook provides a skeletal structure based
> on taxonomy and canonical naming conventions.

## Purpose

Create a comprehensive, versioned snapshot of the entire project state (Hot and Cold) at a
significant milestone for long-term archival, reproducibility, and provenance. Capture all
artifacts, TU history, gatecheck reports, schema versions, and metadata to enable future recovery,
audit, or analysis. Outcome: A timestamped archive package with complete project state, manifest,
and restoration instructions.

## Activation Criteria (Showrunner)

- Major milestone completion (chapter/act/book release)
- Before significant refactoring or architectural changes
- Periodic archival schedule (e.g., monthly, quarterly)
- Before team transitions or long breaks
- Legal/compliance requirements for version preservation

Showrunner opens a Trace Unit (TU): `tu-archive-snapshot-<milestone>` and coordinates archival
process.

## RACI Matrix

| Role        | Assignment | Responsibilities                                              |
| ----------- | ---------- | ------------------------------------------------------------- |
| Showrunner  | R/A        | Coordinates snapshot; verifies completeness; archives package |
| Book Binder | C          | Assists with artifact collection and manifest generation      |
| Gatekeeper  | C          | Verifies integrity of archived artifacts                      |
| All Roles   | I          | Informed of snapshot creation and archive location            |

## Inputs

- Current Cold snapshot with all merged artifacts
- Current Hot snapshot with work-in-progress
- All TU records (opened, stabilizing, gatecheck, cold-merged, closed)
- All Gatecheck Reports
- All Hook Cards
- Schema versions and specifications
- Configuration files and tool versions
- Post-Mortem Reports (if any)
- View Logs from Binding Runs

## Procedure (Message Sequences)

> **Note:** Detailed message sequences pending in Layer 4 protocol specification.

### Step 1: Prepare Snapshot

Freeze current state of all repositories/surfaces:

- Cold snapshot with merge date
- Hot snapshot with active TU states
- Timestamp and version tag

### Step 2: Collect Artifacts

Gather all files and metadata:

- Manuscript sections (all versions in Cold/Hot)
- Canon Packs (spoiler-level lore)
- Codex entries (player-safe surfaces)
- Hook Cards (all statuses: proposed/accepted/deferred/rejected)
- TU Briefs (complete lifecycle history)
- Gatecheck Reports (all decisions and bar statuses)
- Style Addenda and motif kits
- Art Plans and renders (with determinism logs)
- Audio Plans and assets (with reproducibility notes)
- Language Packs (all translation slices)
- View Logs (all exports)
- Schema files and versions

### Step 3: Generate Manifest

Create comprehensive manifest listing:

- All files with checksums (SHA-256)
- Directory structure
- Schema versions used
- Tool versions and dependencies
- Snapshot IDs (Cold and Hot)
- Archive creation date and creator
- Restoration instructions

### Step 4: Verify Integrity

Gatekeeper spot-checks archive:

- All checksums valid
- Critical artifacts present
- Manifest completeness
- Restoration instructions testable

### Step 5: Package and Store

Create archive package:

- Compressed archive (tar.gz or zip)
- Signed with checksum/signature
- Stored in multiple locations (local, cloud, offline backup)
- Cataloged in archive index

### Step 6: Document Snapshot

Record in project history:

- Archive creation date
- Snapshot IDs captured
- Archive location(s)
- Restoration tested (yes/no/partial)
- Notes on significant changes since last archive

## Deliverables

- **Archive Package:**
  - Complete project state (Hot and Cold)
  - All artifacts and metadata
  - Manifest with checksums
  - Restoration instructions
  - Schema files and tool versions
- **Archive Index Entry:**
  - Snapshot metadata
  - Archive location(s)
  - Creation date and creator
  - Restoration status

## Success Criteria

- All critical artifacts included in archive
- Manifest checksums validate
- Archive stored in multiple locations
- Restoration instructions documented and testable
- Archive cataloged and findable
- Team informed of archive creation

## Failure Modes & Remedies

- **Incomplete artifact collection** → Use manifest checklist; verify against TU registry
- **Checksum failures** → Re-archive from source; verify file integrity
- **Untested restoration** → Test restoration on clean system; update instructions as needed
- **Single point of failure** → Store archives in at least 3 locations (local, cloud, offline)
- **Missing metadata** → Ensure snapshot IDs, schema versions, and tool versions recorded

## Quality Bars Pressed

**Primary:** Integrity (complete and verifiable archive)

**Secondary:** Determinism (reproducibility of project state), Presentation (clear documentation)

## Handoffs

- **To Showrunner:** Archive confirmation and location reference
- **To All Roles:** Archive creation notification with snapshot IDs and restoration contact
- **To Archive Index:** Cataloged entry for future retrieval
- **To Future Team:** Complete, recoverable project state for continuity
