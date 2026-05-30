# resonance.ps1 - System check for Resonance v2.2.0 (Windows)

Write-Host "🔮 Resonance v2.2.0 — System Check"
Write-Host "========================================"

# 1. Check Memory (project brain)
if (-not (Test-Path ".resonance\01_state.md")) {
    Write-Host ""
    Write-Host "🧠 Resonance skills loaded. Project memory not found."
    Write-Host "👉 Next step: type '/init' in your AI chat to configure this project."
    Write-Host "   The agent will ask what you're building and scaffold .resonance\ for you."
    exit 0
}
Write-Host "✅ Project memory active (.resonance\)" -ForegroundColor Green

# 2. Check Skills
$skillFiles = Get-ChildItem -Path ".agents\skills" -Filter "SKILL.md" -Recurse -ErrorAction SilentlyContinue
$skillCount = $skillFiles.Count
if ($skillCount -eq 0) {
    Write-Host "⚠️  No compiled skills found in .agents\skills\." -ForegroundColor Red
    Write-Host "   Run: py .forge\forge.py build --all"
    exit 1
}
Write-Host "✅ Skill library loaded ($skillCount skills active)" -ForegroundColor Green

# 3. Ensure docs structure exists
if (-not (Test-Path "docs")) {
    New-Item -ItemType Directory -Force -Path "docs\prd", "docs\architecture", "docs\features", "docs\rfcs" | Out-Null
    Write-Host "   Created docs\ directory structure."
}
Write-Host "✅ Docs structure ready" -ForegroundColor Green

Write-Host ""
Write-Host "📖 Soul (Vision):"
Get-Content -Path ".resonance\00_soul.md" -TotalCount 5
Write-Host "..."
Write-Host ""
Write-Host "📊 State (Current task):"
Get-Content -Path ".resonance\01_state.md" -TotalCount 10
Write-Host "..."
Write-Host ""
Write-Host "========================================"
Write-Host "System online. Ready." -ForegroundColor Green
Write-Host ""
Write-Host "Slash commands: /plan  /build  /debug  /audit  /ship"
