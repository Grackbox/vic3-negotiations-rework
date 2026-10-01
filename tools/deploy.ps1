# Mirrors the mod into the game's local mod folder for testing (files deleted here disappear there too).
# Usage: pwsh tools/deploy.ps1 [-Target <mod folder>]
param(
    [string]$Target = "$env:USERPROFILE\Documents\Paradox Interactive\Victoria 3\mod\negotiations_rework"
)
$Source = Split-Path -Parent $PSScriptRoot
robocopy $Source $Target /MIR /XD .git .github tools docs __pycache__ /XF .gitignore .gitattributes README_NR.md /NJH /NJS /NP /NDL /NS /NC
if ($LASTEXITCODE -lt 8) {
    Write-Output "Deployed to $Target"
    exit 0
}
exit $LASTEXITCODE
