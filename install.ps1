# DobbyOps Install Script
# Creates symlinks from ~/.claude/commands to dobbyops/commands

$DobbyOpsDir = $PSScriptRoot
$ClaudeCommandsDir = "$env:USERPROFILE\.claude\commands"

# Create commands directory if not exists
if (-not (Test-Path $ClaudeCommandsDir)) {
    New-Item -ItemType Directory -Path $ClaudeCommandsDir -Force
    Write-Host "Created $ClaudeCommandsDir"
}

# Get all skill files
$Skills = Get-ChildItem -Path "$DobbyOpsDir\commands" -Filter "*.md"

foreach ($Skill in $Skills) {
    $LinkPath = Join-Path $ClaudeCommandsDir $Skill.Name
    $TargetPath = $Skill.FullName

    # Remove existing file/link
    if (Test-Path $LinkPath) {
        Remove-Item $LinkPath -Force
    }

    # Create symlink (requires admin or developer mode)
    try {
        New-Item -ItemType SymbolicLink -Path $LinkPath -Target $TargetPath -Force
        Write-Host "Linked: $($Skill.Name)"
    }
    catch {
        # Fallback: copy file
        Copy-Item $TargetPath $LinkPath -Force
        Write-Host "Copied: $($Skill.Name) (symlink failed)"
    }
}

Write-Host ""
Write-Host "DobbyOps installed! Available skills:"
foreach ($Skill in $Skills) {
    $Name = $Skill.BaseName
    Write-Host "  /$Name"
}
