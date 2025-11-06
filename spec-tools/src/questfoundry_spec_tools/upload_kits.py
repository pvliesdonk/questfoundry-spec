"""
Builds Layer 5 upload kits (symlink folders + zip archives) for chat platforms.

Creates dist/upload_kits/* with ORIGINAL DIRECTORY STRUCTURE PRESERVED in zips.
This allows multiple files named system_prompt.md to coexist via their parent paths.
Falls back to copying if symlinks are not permitted on the system.

Usage via uv:
  uv run qfspec-build-kits
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


def _find_repo_root() -> Path:
    # Mirror logic in cli.py: look for a parent that contains 03-schemas
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / "03-schemas").exists():
            return parent
    # Fallback: assume spec-tools/ layout
    repo_root = Path(__file__).resolve().parents[3]
    return repo_root


def _ensure_link_or_copy(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        if dest.exists() or dest.is_symlink():
            dest.unlink()
        os.symlink(src, dest)
    except Exception:
        # Windows without privileges or filesystems without symlink support
        shutil.copy2(src, dest)


def _read_manifest(manifest: Path) -> list[str]:
    items: list[str] = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        rel = line.strip()
        if not rel:
            continue
        items.append(rel)
    return items


def _build_folder_from_manifest(repo_root: Path, manifest: Path, out_folder: Path) -> None:
    """Build a folder with files from manifest, preserving original directory structure."""
    if out_folder.exists():
        shutil.rmtree(out_folder)
    out_folder.mkdir(parents=True, exist_ok=True)

    for rel in _read_manifest(manifest):
        src = (repo_root / rel).resolve()
        if not src.exists():
            raise FileNotFoundError(f"Manifest entry not found: {rel}")
        # Preserve original directory structure (e.g., 05-prompts/showrunner/system_prompt.md)
        dest = out_folder / rel
        _ensure_link_or_copy(src, dest)


def _zip_folder(folder: Path, zip_path: Path, manifest_order: list[str] | None = None) -> None:
    """
    Create a zip archive from a folder.

    If manifest_order is provided, files are added to the zip in that order.
    This ensures validation files (validation_contract.md, SCHEMA_INDEX.json)
    appear first in the zip, which is critical for LLM file loading order.
    """
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as zf:
        if manifest_order:
            # Add files in manifest order (preserves validation file precedence)
            for rel_path in manifest_order:
                file_path = folder / rel_path
                if file_path.is_file():
                    zf.write(file_path, rel_path)
        else:
            # Fallback to rglob (alphabetical/filesystem order)
            for p in folder.rglob("*"):
                if p.is_file():
                    zf.write(p, p.relative_to(folder))


def _build_kit(repo_root: Path, manifests_dir: Path, out_dir: Path, manifest_name: str, output_name: str) -> None:
    """Build a single kit from a manifest file."""
    manifest_path = manifests_dir / manifest_name
    if not manifest_path.exists():
        print(f"  Skipping {output_name}: manifest {manifest_name} not found")
        return

    folder = out_dir / output_name
    zip_path = out_dir / f"{output_name}.zip"

    manifest_order = _read_manifest(manifest_path)
    _build_folder_from_manifest(repo_root, manifest_path, folder)
    _zip_folder(folder, zip_path, manifest_order=manifest_order)
    print(f"  ✓ {output_name}.zip ({len(manifest_order)} files)")


def build_kits_cli() -> None:
    repo_root = _find_repo_root()
    manifests_dir = repo_root / "05-prompts" / "upload_kits" / "manifests"
    out_dir = repo_root / "dist" / "upload_kits"

    if not manifests_dir.exists():
        print(f"Manifests not found: {manifests_dir}")
        sys.exit(1)

    print("Building upload kits with preserved directory structure...\n")

    # Standalone kits (for traditional role-based usage)
    print("Standalone Kits:")
    _build_kit(repo_root, manifests_dir, out_dir, "chatgpt_minimal.list", "minimal-standalone")
    _build_kit(repo_root, manifests_dir, out_dir, "optional.list", "optional-standalone")
    _build_kit(repo_root, manifests_dir, out_dir, "full-standalone.list", "full-standalone")

    # Gemini splits for full standalone (10-file limit per zip)
    print("\nGemini Standalone Splits:")
    _build_kit(repo_root, manifests_dir, out_dir, "gemini_core_zip.list", "gemini-minimal-standalone")
    _build_kit(repo_root, manifests_dir, out_dir, "gemini_optional_zip.list", "gemini-optional-standalone")
    _build_kit(repo_root, manifests_dir, out_dir, "gemini-full-standalone-1.list", "gemini-full-standalone-1")
    _build_kit(repo_root, manifests_dir, out_dir, "gemini-full-standalone-2.list", "gemini-full-standalone-2")
    _build_kit(repo_root, manifests_dir, out_dir, "gemini-full-standalone-3.list", "gemini-full-standalone-3")

    # Orchestration kits (for loop-focused architecture)
    print("\nOrchestration Kits:")
    _build_kit(repo_root, manifests_dir, out_dir, "orchestration-complete.list", "orchestration-complete")

    # Gemini splits for orchestration (10-file limit per zip)
    print("\nGemini Orchestration Splits:")
    _build_kit(repo_root, manifests_dir, out_dir, "gemini-orchestration-1-foundation.list", "gemini-orchestration-1-foundation")
    _build_kit(repo_root, manifests_dir, out_dir, "gemini-orchestration-2-playbooks.list", "gemini-orchestration-2-playbooks")
    _build_kit(repo_root, manifests_dir, out_dir, "gemini-orchestration-3-playbooks-extra.list", "gemini-orchestration-3-playbooks-extra")
    _build_kit(repo_root, manifests_dir, out_dir, "gemini-orchestration-4-adapters-core.list", "gemini-orchestration-4-adapters-core")
    _build_kit(repo_root, manifests_dir, out_dir, "gemini-orchestration-5-adapters-extra.list", "gemini-orchestration-5-adapters-extra")

    print(f"\n✓ Upload kits built under: {out_dir}")


if __name__ == "__main__":
    build_kits_cli()
