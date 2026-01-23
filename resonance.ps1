# resonance.ps1 - The "Wake Up" Call for Resonance v2.0 (Windows Edition)

Write-Host "🔮 Resonance v2.0 System Check:"
Write-Host "================================================"

# 1. Check Memory (The Brain)
if (-not (Test-Path ".resonance\01_state.md")) {
    Write-Host "🧠 Resonance Core Loaded."
    Write-Host "👉 Action Required: Run '@Resonance /init' in your chat to configure this project."
    exit 0
}
Write-Host "✅ Memory Active (.resonance\)" -ForegroundColor Green

# 2. Check Skills (The Talent)
$skillCount = (Get-ChildItem -Path ".agent\skills\resonance-*" -ErrorAction SilentlyContinue).Count
if ($skillCount -eq 0) {
    Write-Host "⚠️  CRITICAL: No Resonance Skills found in .agent\skills\." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Resonance Skills Loaded ($skillCount active)" -ForegroundColor Green

# 3. Check Workflows (The Protocol)
$workflowCount = (Get-ChildItem -Path ".agent\workflows\*.md" -ErrorAction SilentlyContinue).Count
Write-Host "✅ Workflows Ready ($workflowCount protocols)" -ForegroundColor Green

# 4. Ensure Docs Structure
if (-not (Test-Path "docs")) {
    New-Item -ItemType Directory -Force -Path "docs\specs", "docs\architecture", "docs\reports" | Out-Null
    Write-Host "   Created docs\ directory structure."
}

Write-Host "================================================"
Write-Host ""
Write-Host "📖 Loading Soul (Vision):"
Get-Content -Path ".resonance\00_soul.md" -TotalCount 5
Write-Host "..."
Write-Host ""
Write-Host "📊 Loading State (Status):"
Get-Content -Path ".resonance\01_state.md" -TotalCount 10
Write-Host "..."
Write-Host ""
Write-Host "================================================"
Write-Host "System Online. Ready for orders." -ForegroundColor Green
Write-Host ""
Write-Host "Try: @Resonance /status"
