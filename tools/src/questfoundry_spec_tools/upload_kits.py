"""
Builds Layer 5 upload kits (symlink folders + zip archives) for chat platforms.

Creates dist/upload_kits/* with role‑qualified filenames to avoid collisions.
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
    # Fallback: assume tools/ layout
    repo_root = Path(__file__).resolve().parents[3]
    return repo_root


def _flatten_rel(rel: str) -> str:
    # Convert 05-prompts/foo/bar.md -> foo.bar.md for easier attachments
    if rel.startswith("05-prompts/"):
        rel = rel[len("05-prompts/") :]
    return rel.replace("/", ".")


def _ensure_link_or_copy(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        if dest.exists() or dest.is_symlink():
            dest.unlink()
        os.symlink(src, dest)
    except Exception:
        # Windows without privileges or filesystems without symlink support
        shutil.copy2(src, dest)


def _read_manifest(manifest: Path) -> list[Path]:
    items: list[Path] = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        rel = line.strip()
        if not rel:
            continue
        items.append(Path(rel))
    return items


def _build_folder_from_manifest(repo_root: Path, manifest: Path, out_folder: Path) -> None:
    if out_folder.exists():
        shutil.rmtree(out_folder)
    out_folder.mkdir(parents=True, exist_ok=True)

    for rel in _read_manifest(manifest):
        src = (repo_root / rel).resolve()
        if not src.exists():
            raise FileNotFoundError(f"Manifest entry not found: {rel}")
        dest_name = _flatten_rel(str(rel))
        dest = out_folder / dest_name
        _ensure_link_or_copy(src, dest)


def _zip_folder(folder: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as zf:
        for p in folder.rglob("*"):
            if p.is_file():
                zf.write(p, p.relative_to(folder))


def build_kits_cli() -> None:
    repo_root = _find_repo_root()
    manifests_dir = repo_root / "05-prompts" / "upload_kits" / "manifests"
    out_dir = repo_root / "dist" / "upload_kits"

    if not manifests_dir.exists():
        print(f"Manifests not found: {manifests_dir}")
        sys.exit(1)

    # ChatGPT kits
    cg_min_folder = out_dir / "chatgpt" / "minimal"
    cg_min_zip = out_dir / "chatgpt" / "minimal.zip"
    cg_add_folder = out_dir / "chatgpt" / "addons"
    cg_add_zip = out_dir / "chatgpt" / "addons.zip"

    _build_folder_from_manifest(
        repo_root, manifests_dir / "chatgpt_minimal.list", cg_min_folder
    )
    _zip_folder(cg_min_folder, cg_min_zip)

    _build_folder_from_manifest(
        repo_root, manifests_dir / "chatgpt_addons.list", cg_add_folder
    )
    _zip_folder(cg_add_folder, cg_add_zip)

    # Gemini kits
    gm_core_folder = out_dir / "gemini" / "core_zip"
    gm_core_zip = out_dir / "gemini" / "core.zip"
    gm_opt_folder = out_dir / "gemini" / "optional_zip"
    gm_opt_zip = out_dir / "gemini" / "optional.zip"

    _build_folder_from_manifest(
        repo_root, manifests_dir / "gemini_core_zip.list", gm_core_folder
    )
    _zip_folder(gm_core_folder, gm_core_zip)

    _build_folder_from_manifest(
        repo_root, manifests_dir / "gemini_optional_zip.list", gm_opt_folder
    )
    _zip_folder(gm_opt_folder, gm_opt_zip)

    print(f"Upload kits built under: {out_dir}")

