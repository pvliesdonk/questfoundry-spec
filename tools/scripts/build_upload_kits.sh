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
  local rel="$1"; rel="${rel#05-prompts/}"; echo "${rel//\//.}"
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

# ChatGPT kits
make_folder_from_manifest "$MANIFEST_DIR/chatgpt_minimal.list" "$OUT_DIR/chatgpt/minimal"
make_folder_from_manifest "$MANIFEST_DIR/chatgpt_addons.list" "$OUT_DIR/chatgpt/addons"
zip_from_folder "$OUT_DIR/chatgpt/minimal" "$OUT_DIR/chatgpt/minimal.zip"
zip_from_folder "$OUT_DIR/chatgpt/addons" "$OUT_DIR/chatgpt/addons.zip"

# Gemini kits
make_folder_from_manifest "$MANIFEST_DIR/gemini_core_zip.list" "$OUT_DIR/gemini/core_zip"
make_folder_from_manifest "$MANIFEST_DIR/gemini_optional_zip.list" "$OUT_DIR/gemini/optional_zip"
zip_from_folder "$OUT_DIR/gemini/core_zip" "$OUT_DIR/gemini/core.zip"
zip_from_folder "$OUT_DIR/gemini/optional_zip" "$OUT_DIR/gemini/optional.zip"

echo "Upload kits built under: $OUT_DIR"

