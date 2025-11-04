Param(
  [string]$RootDir = $(Resolve-Path (git rev-parse --show-toplevel 2>$null)).Path
)

$ErrorActionPreference = 'Stop'
$OutDir = Join-Path $RootDir 'dist/upload_kits'
$ManifestDir = Join-Path $RootDir '05-prompts/upload_kits/manifests'

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

function Name-FromRel([string]$rel) {
  $trim = $rel -replace '^05-prompts/', ''
  return ($trim -replace '/', '.')
}

function Ensure-Link([string]$src, [string]$dest) {
  $destDir = Split-Path -Parent $dest
  New-Item -ItemType Directory -Force -Path $destDir | Out-Null
  try {
    New-Item -ItemType SymbolicLink -Path $dest -Target $src -Force | Out-Null
  } catch {
    Copy-Item -LiteralPath $src -Destination $dest -Force
  }
}

function Make-FolderFromManifest([string]$manifest, [string]$folder) {
  if (Test-Path $folder) { Remove-Item -Recurse -Force $folder }
  New-Item -ItemType Directory -Force -Path $folder | Out-Null
  Get-Content -Path $manifest | ForEach-Object {
    $rel = $_.Trim()
    if ($rel -eq '') { return }
    $src = Join-Path $RootDir $rel
    $destName = Name-FromRel $rel
    $dest = Join-Path $folder $destName
    Ensure-Link $src $dest
  }
}

function Zip-FromFolder([string]$folder, [string]$zipPath) {
  if (Test-Path $zipPath) { Remove-Item -Force $zipPath }
  Compress-Archive -Path (Join-Path $folder '*') -DestinationPath $zipPath -Force
}

# Flat kits (no platform subfolders)
Make-FolderFromManifest (Join-Path $ManifestDir 'chatgpt_minimal.list') (Join-Path $OutDir 'minimal')
Make-FolderFromManifest (Join-Path $ManifestDir 'chatgpt_addons.list') (Join-Path $OutDir 'addons')
Zip-FromFolder (Join-Path $OutDir 'minimal') (Join-Path $OutDir 'minimal.zip')
Zip-FromFolder (Join-Path $OutDir 'addons') (Join-Path $OutDir 'addons.zip')

Write-Host "Upload kits built under: $OutDir"
