$Repo = "C:\Users\Ossama-Hashim\skills-tree"

Set-Location $Repo

Write-Host ""
Write-Host "Repository Root:"
Write-Host (Get-Location).Path
Write-Host ""

if (Test-Path ".\skills-tree") {
    throw "ERROR: Nested skills-tree directory detected."
}

hermes @args