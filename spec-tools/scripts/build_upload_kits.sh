#!/usr/bin/env bash
set -euo pipefail

# Build symlink folders and zipped upload kits under dist/upload_kits
# - Flattens filenames to role-qualified names to avoid collisions (e.g., showrunner.system_prompt.md)
# - Falls back to copying files if symlinks are not permitted

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
OUT_DIR="$ROOT_DIR/dist/upload_kits"
MANIFEST_DIR="$ROOT_DIR/05-prompts/upload_kits/manifests"

mkdir -p "$OUT_DIR"

name_from_rel() {
  local rel="$1"
  rel="${rel#05-prompts/}"
  # Special cases
  if [[ "$rel" == */system_prompt.md ]]; then
    printf "%s.md" "${rel%%/*}"
    return 0
  fi
  if [[ "$rel" == _shared/* ]]; then
    printf "%s" "${rel#_shared/}"
    return 0
  fi
  # Fallback: flatten
  echo "${rel//\//.}"
}

ensure_link() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")"
  if ln -sfn "$src" "$dest" 2>/dev/null; then
    return 0
  else
    cp -f "$src" "$dest"
  fi
}

make_folder_from_manifest() {
  local manifest="$1" folder="$2"
  rm -rf "$folder" && mkdir -p "$folder"
  while IFS= read -r rel || [[ -n "$rel" ]]; do
    [[ -z "$rel" ]] && continue
    local src="$ROOT_DIR/$rel"
    local dest_name; dest_name="$(name_from_rel "$rel")"
    local dest="$folder/$dest_name"
    ensure_link "$src" "$dest"
  done <"$manifest"
}

zip_from_folder() {
  local folder="$1" zip_path="$2"
  (cd "$folder" && zip -q -r "${zip_path}" .)
}

# Flat kits (no platform subfolders)
make_folder_from_manifest "$MANIFEST_DIR/chatgpt_minimal.list" "$OUT_DIR/minimal"
if [ -f "$MANIFEST_DIR/optional.list" ]; then opt_list="$MANIFEST_DIR/optional.list"; else opt_list="$MANIFEST_DIR/gemini_optional_zip.list"; fi
make_folder_from_manifest "$opt_list" "$OUT_DIR/optional"
zip_from_folder "$OUT_DIR/minimal" "$OUT_DIR/minimal.zip"
zip_from_folder "$OUT_DIR/optional" "$OUT_DIR/optional.zip"

# full = union of minimal + optional
rm -rf "$OUT_DIR/full" && mkdir -p "$OUT_DIR/full"
cp -f "$OUT_DIR/minimal"/* "$OUT_DIR/full"/ 2>/dev/null || true
cp -f "$OUT_DIR/optional"/* "$OUT_DIR/full"/ 2>/dev/null || true
zip_from_folder "$OUT_DIR/full" "$OUT_DIR/full.zip"

echo "Upload kits built under: $OUT_DIR"
