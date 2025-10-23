#!/usr/bin/env python3
"""Cross-artifact consistency checks for Questfoundry projects."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple


def load_json(path: Path) -> Tuple[Optional[dict], Optional[str]]:
    if not path.exists():
        return None, f"missing file: {path}"
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle), None
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON in {path}: {exc}"


def collect_outline_beats(outline: dict) -> Dict[str, Set[str]]:
    beats: Dict[str, Set[str]] = {}
    for thread_id, thread in outline.get("threads", {}).items():
        thread_beats = thread.get("beats", {})
        beats[thread_id] = set(thread_beats.keys())
    return beats


def collect_plot_nodes(plot_map: dict) -> Set[str]:
    return {node.get("id") for node in plot_map.get("nodes", []) if node.get("id")}


def collect_sections(sections_dir: Path) -> Iterable[Tuple[Path, dict]]:
    for path in sections_dir.glob("*/current.json"):
        try:
            with path.open("r", encoding="utf-8") as handle:
                yield path, json.load(handle)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"invalid JSON in {path}: {exc}") from exc


def collect_canon_entities(canon: dict) -> Set[str]:
    return {
        entity.get("id")
        for entity in canon.get("entities", [])
        if entity.get("id")
    }


def normalise_ref(ref: Optional[str]) -> Optional[str]:
    if not ref:
        return None
    return ref.split("#", 1)[0]


def check_consistency(root: Path, strict_missing: bool = False) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    outline_path = root / "plot_outline.json"
    plot_map_path = root / "plot_map.json"
    canon_path = root / "world" / "canon.json"
    sections_dir = root / "sections"
    art_plan_path = root / "art" / "art_plan.json"

    outline, outline_issue = load_json(outline_path)
    if outline_issue:
        (errors if strict_missing else warnings).append(outline_issue)

    plot_map, map_issue = load_json(plot_map_path)
    if map_issue:
        (errors if strict_missing else warnings).append(map_issue)

    canon, canon_issue = load_json(canon_path)
    if canon_issue:
        (errors if strict_missing else warnings).append(canon_issue)

    section_records: List[Tuple[Path, dict]] = []
    if sections_dir.exists():
        try:
            section_records = list(collect_sections(sections_dir))
        except RuntimeError as exc:  # invalid JSON already formatted
            errors.append(str(exc))
    elif strict_missing:
        errors.append(f"missing directory: {sections_dir}")
    else:
        warnings.append(f"missing directory: {sections_dir}")

    outline_beats = collect_outline_beats(outline or {}) if outline else {}
    plot_nodes = collect_plot_nodes(plot_map or {}) if plot_map else set()
    section_ids = {record[1].get("id") for record in section_records if record[1].get("id")}
    canon_entities = collect_canon_entities(canon or {}) if canon else set()

    # Sections ↔ outline/linkage checks
    for path, section in section_records:
        section_id = section.get("id") or path.parent.name
        beat_ref = section.get("beat_ref") or {}
        thread_id = beat_ref.get("thread_id")
        beat_id = beat_ref.get("beat_id")

        if not thread_id or not beat_id:
            errors.append(f"{path}: missing beat_ref.thread_id/beat_id")
            continue

        beats_for_thread = outline_beats.get(thread_id)
        if beats_for_thread is None:
            errors.append(f"{path}: thread '{thread_id}' not found in plot_outline.json")
        elif beat_id not in beats_for_thread:
            errors.append(
                f"{path}: beat '{beat_id}' not present in plot_outline.json thread '{thread_id}'"
            )

        if plot_nodes and beat_id not in plot_nodes:
            errors.append(
                f"{path}: beat '{beat_id}' not present in plot_map.json nodes"
            )

    # Art plan refs
    art_plan, art_issue = load_json(art_plan_path)
    if art_issue:
        (errors if strict_missing else warnings).append(art_issue)
    elif art_plan:
        valid_refs = plot_nodes | section_ids | canon_entities
        for idx, item in enumerate(art_plan.get("items", [])):
            item_id = item.get("id", f"<item {idx}>")
            ref = normalise_ref(item.get("ref"))
            if not ref:
                warnings.append(f"art_plan.json item '{item_id}' missing ref")
                continue
            if ref not in valid_refs:
                errors.append(
                    f"art_plan.json item '{item_id}' references unknown ref '{ref}'"
                )

    return errors, warnings


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Questfoundry project root (defaults to current directory)",
    )
    parser.add_argument(
        "--strict-missing",
        action="store_true",
        help="Treat missing artifacts as errors rather than warnings.",
    )
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    errors, warnings = check_consistency(root, strict_missing=args.strict_missing)

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        return 1

    if not warnings:
        print("Questfoundry cross-doc consistency: OK")
    else:
        print("Questfoundry cross-doc consistency: OK (with warnings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
