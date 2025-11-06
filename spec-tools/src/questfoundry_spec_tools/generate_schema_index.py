#!/usr/bin/env python3
"""
Generate SCHEMA_INDEX.json for Layer 5 prompts.

This script scans all JSON schemas in 03-schemas/, computes SHA-256 hashes,
and creates an index file that maps schema names to their metadata.

The index is used by Layer 5 prompts to discover and validate artifacts.
"""

import hashlib
import json
from pathlib import Path
from typing import Any, Dict

# Role-to-schema mappings based on Layer 5 role definitions
ROLE_SCHEMAS: Dict[str, list[str]] = {
    "plotwright": [
        "hook_card",
        "outline",
        "scene_outline",
        "plot_card",
        "beat_sequence",
    ],
    "scene_smith": [
        "scene",
        "narrative_block",
        "dialogue_block",
    ],
    "style_lead": [
        "style_audit_report",
        "style_proposal",
    ],
    "gatekeeper": [
        "gatecheck_report",
        "merge_decision",
        "spoiler_audit",
    ],
    "book_binder": [
        "cold_book",
        "cold_manifest",
        "export_manifest",
    ],
    "lore_weaver": [
        "lore_entry",
        "canon_question",
        "lore_audit",
    ],
    "codex_curator": [
        "codex_entry",
        "knowledge_graph_node",
        "player_safe_summary",
    ],
    "player_narrator": [
        "narration_script",
        "player_choice",
        "session_log",
    ],
    "art_director": [
        "art_brief",
        "art_asset_spec",
    ],
    "illustrator": [
        "art_asset",
        "cold_art_manifest",
    ],
    "audio_director": [
        "audio_brief",
        "audio_asset_spec",
    ],
    "audio_producer": [
        "audio_asset",
    ],
    "translator": [
        "translation_glossary",
        "translated_artifact",
    ],
    "researcher": [
        "research_report",
        "source_citation",
    ],
    "showrunner": [
        "tu_card",
        "loop_manifest",
        "hot_manifest",
        "project_metadata",
    ],
}

# Intent-to-schema mappings based on Layer 4 protocol
INTENT_SCHEMAS: Dict[str, list[str]] = {
    "hook.propose": ["hook_card"],
    "hook.classify": ["hook_card"],
    "hook.integrate": ["hook_card"],
    "outline.propose": ["outline", "scene_outline"],
    "outline.revise": ["outline", "scene_outline"],
    "scene.draft": ["scene", "narrative_block"],
    "scene.revise": ["scene", "narrative_block"],
    "style.audit": ["style_audit_report"],
    "style.propose": ["style_proposal"],
    "lore.question": ["canon_question"],
    "lore.answer": ["lore_entry"],
    "lore.integrate": ["lore_entry"],
    "codex.summarize": ["codex_entry", "player_safe_summary"],
    "codex.expand": ["codex_entry"],
    "gate.request": ["gatecheck_report"],
    "gate.decide": ["merge_decision"],
    "gate.audit": ["spoiler_audit"],
    "bind.request": ["cold_book", "cold_manifest"],
    "bind.deliver": ["export_manifest"],
    "narrate.dry_run": ["narration_script", "session_log"],
    "art.brief": ["art_brief", "art_asset_spec"],
    "art.deliver": ["art_asset", "cold_art_manifest"],
    "audio.brief": ["audio_brief", "audio_asset_spec"],
    "audio.deliver": ["audio_asset"],
    "translate.request": ["translation_glossary"],
    "translate.deliver": ["translated_artifact"],
    "research.request": ["research_report"],
    "research.deliver": ["source_citation"],
    "tu.open": ["tu_card"],
    "tu.close": ["tu_card"],
    "tu.checkpoint": ["tu_card"],
}


def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def extract_schema_metadata(schema_path: Path) -> Dict[str, Any]:
    """Extract metadata from a JSON schema file."""
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    return {
        "$id": schema.get("$id", ""),
        "title": schema.get("title", ""),
        "description": schema.get("description", ""),
        "$schema": schema.get("$schema", ""),
    }


def get_schema_key(filename: str) -> str:
    """Convert schema filename to index key (remove .schema.json suffix)."""
    return filename.replace(".schema.json", "")


def get_roles_for_schema(schema_key: str) -> list[str]:
    """Find all roles that use this schema."""
    roles = []
    for role, schemas in ROLE_SCHEMAS.items():
        if schema_key in schemas:
            roles.append(role)
    return sorted(roles)


def get_intents_for_schema(schema_key: str) -> list[str]:
    """Find all intents that use this schema."""
    intents = []
    for intent, schemas in INTENT_SCHEMAS.items():
        if schema_key in schemas:
            intents.append(intent)
    return sorted(intents)


def extract_draft_version(schema_uri: str) -> str:
    """Extract draft version from $schema URI."""
    # Examples:
    # https://json-schema.org/draft/2020-12/schema -> 2020-12
    # http://json-schema.org/draft-07/schema# -> draft-07
    if "2020-12" in schema_uri:
        return "2020-12"
    elif "draft-07" in schema_uri:
        return "draft-07"
    elif "draft-06" in schema_uri:
        return "draft-06"
    elif "draft-04" in schema_uri:
        return "draft-04"
    else:
        return "unknown"


def generate_schema_index(repo_root: Path, output_path: Path) -> None:
    """
    Generate SCHEMA_INDEX.json from schemas in 03-schemas/.

    Args:
        repo_root: Path to repository root
        output_path: Where to write SCHEMA_INDEX.json
    """
    schemas_dir = repo_root / "03-schemas"
    if not schemas_dir.exists():
        raise FileNotFoundError(f"Schemas directory not found: {schemas_dir}")

    index = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "QuestFoundry Schema Index",
        "description": "Index of all Layer 3 schemas with integrity hashes and role mappings",
        "version": "0.2.0",
        "generated": "2025-11-06",
        "schemas": {}
    }

    # Scan all .schema.json files
    schema_files = sorted(schemas_dir.glob("*.schema.json"))

    for schema_path in schema_files:
        schema_key = get_schema_key(schema_path.name)

        # Extract metadata from schema file
        metadata = extract_schema_metadata(schema_path)

        # Compute SHA-256 hash
        sha256 = compute_sha256(schema_path)

        # Relative path from repo root
        rel_path = schema_path.relative_to(repo_root).as_posix()

        # Draft version
        draft = extract_draft_version(metadata.get("$schema", ""))

        # Role and intent mappings
        roles = get_roles_for_schema(schema_key)
        intents = get_intents_for_schema(schema_key)

        # Add to index
        index["schemas"][schema_key] = {
            "$id": metadata["$id"],
            "title": metadata.get("title", ""),
            "description": metadata.get("description", ""),
            "path": rel_path,
            "draft": draft,
            "sha256": sha256,
            "roles": roles,
            "intent": intents,
        }

    # Write index to output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
        f.write("\n")  # Add trailing newline

    print(f"✅ Generated SCHEMA_INDEX.json with {len(index['schemas'])} schemas")
    print(f"📄 Output: {output_path}")

    # Print summary
    print("\n📊 Schema Summary:")
    for schema_key, schema_info in sorted(index["schemas"].items()):
        roles_str = ", ".join(schema_info["roles"][:3])
        if len(schema_info["roles"]) > 3:
            roles_str += f" (+{len(schema_info['roles']) - 3} more)"
        print(f"  • {schema_key:30s} — {roles_str or 'No roles'}")


def main() -> None:
    """CLI entry point."""
    # Determine repo root (script is in spec-tools/src/questfoundry_spec_tools/)
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent.parent

    # Output to 05-prompts/SCHEMA_INDEX.json
    output_path = repo_root / "05-prompts" / "SCHEMA_INDEX.json"

    print(f"🔍 Scanning schemas in: {repo_root / '03-schemas'}")
    generate_schema_index(repo_root, output_path)


if __name__ == "__main__":
    main()
