# init.ps1
# Resonance Initialization Script for Windows

Write-Host "Initializing Resonance Engine (v1.0)..." -ForegroundColor Cyan

# 1. Create the .resonance directory if it doesn't exist
if (-not (Test-Path -Path ".resonance")) {
    New-Item -ItemType Directory -Path ".resonance" | Out-Null
    Write-Host "Created .resonance directory." -ForegroundColor Gray
}

# 2. Copy templates to the .resonance directory
Copy-Item "templates\*.md" -Destination ".resonance\" -Force

# 3. Install Pointers (Adapters)
Copy-Item "adapters\.cursorrules" -Destination ".\" -Force
Copy-Item "adapters\.windsurfrules" -Destination ".\" -Force

Write-Host "✅ Resonance initialized." -ForegroundColor Green
Write-Host " - Memory Bank: .resonance/ created"
Write-Host " - Brain: AGENT.md (Root)"
Write-Host " - Pointers: .cursorrules & .windsurfrules installed"
