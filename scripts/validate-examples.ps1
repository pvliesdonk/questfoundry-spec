# validate-examples.ps1
#
# Validates all Layer 4 envelope examples against envelope.schema.json and their payloads
# against Layer 3 schemas.
#
# Usage:
#   .\scripts\validate-examples.ps1
#   .\scripts\validate-examples.ps1 04-protocol\EXAMPLES\hook.create.json
#
# Exit code 0 on success, 1 on failure

param(
    [string[]]$EnvelopeFiles
)

# Colors for output
$ErrorColor = "Red"
$SuccessColor = "Green"
$WarningColor = "Yellow"

# Find repository root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Write-Host "=== QuestFoundry: Validate Layer 4 Envelope Examples ===" -ForegroundColor Cyan
Write-Host "Repository: $RepoRoot"
Write-Host ""

# Check if uv is available
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Error: 'uv' command not found" -ForegroundColor $ErrorColor
    Write-Host "Please install uv: https://github.com/astral-sh/uv"
    exit 1
}

# Check if tools directory exists
$ToolsDir = Join-Path $RepoRoot "tools"
if (-not (Test-Path $ToolsDir)) {
    Write-Host "Error: tools\ directory not found" -ForegroundColor $ErrorColor
    Write-Host "Please ensure you're running from the repository root"
    exit 1
}

# Set up tools if needed
Write-Host "Setting up validation tools..."
Push-Location $ToolsDir
try {
    uv sync --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to set up validation tools" -ForegroundColor $ErrorColor
        exit 1
    }
} finally {
    Pop-Location
}
Write-Host ""

# Determine which files to validate
Set-Location $RepoRoot

if ($EnvelopeFiles.Count -eq 0) {
    # No arguments: validate all examples
    $ExamplesDir = Join-Path $RepoRoot "04-protocol\EXAMPLES"
    
    if (-not (Test-Path $ExamplesDir)) {
        Write-Host "Error: 04-protocol\EXAMPLES\ directory not found" -ForegroundColor $ErrorColor
        exit 1
    }
    
    # Find all .json files in EXAMPLES directory
    $EnvelopeFiles = Get-ChildItem -Path $ExamplesDir -Filter "*.json" | ForEach-Object { $_.FullName } | Sort-Object
    
    if ($EnvelopeFiles.Count -eq 0) {
        Write-Host "Warning: No envelope examples found in $ExamplesDir" -ForegroundColor $WarningColor
        exit 0
    }
    
    Write-Host "Validating $($EnvelopeFiles.Count) envelope examples..."
    Write-Host ""
} else {
    Write-Host "Validating $($EnvelopeFiles.Count) specified envelope(s)..."
    Write-Host ""
}

# Validate each envelope
$Failed = 0
$Passed = 0

foreach ($envelopeFile in $EnvelopeFiles) {
    # Make path absolute if relative
    if (-not [System.IO.Path]::IsPathRooted($envelopeFile)) {
        $envelopeFile = Join-Path $RepoRoot $envelopeFile
    }
    
    if (-not (Test-Path $envelopeFile)) {
        $filename = Split-Path -Leaf $envelopeFile
        Write-Host "✗ $filename - File not found" -ForegroundColor $ErrorColor
        $Failed++
        continue
    }
    
    # Validate using qfspec-check-envelope
    $output = uv run --directory $ToolsDir qfspec-check-envelope $envelopeFile 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        $filename = Split-Path -Leaf $envelopeFile
        Write-Host "✓ $filename" -ForegroundColor $SuccessColor
        $Passed++
    } else {
        $filename = Split-Path -Leaf $envelopeFile
        Write-Host "✗ $filename" -ForegroundColor $ErrorColor
        # Show validation errors
        $output | Where-Object { $_ -match "Validation error|validation errors" } | ForEach-Object {
            Write-Host "  $_" -ForegroundColor $ErrorColor
        }
        Write-Host ""
        $Failed++
    }
}

# Summary
Write-Host ""
Write-Host "=== Validation Summary ===" -ForegroundColor Cyan
Write-Host "Total: $($Passed + $Failed)"
Write-Host "Passed: $Passed" -ForegroundColor $SuccessColor

if ($Failed -eq 0) {
    Write-Host "All envelope examples are valid!" -ForegroundColor $SuccessColor
    exit 0
} else {
    Write-Host "Failed: $Failed" -ForegroundColor $ErrorColor
    exit 1
}
