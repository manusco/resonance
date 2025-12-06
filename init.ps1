# init.ps1
# Resonance Initialization Script for Windows

Write-Host "Initializing Resonance Engine..." -ForegroundColor Cyan

# Create the .resonance directory if it doesn't exist
if (-not (Test-Path -Path ".resonance")) {
    New-Item -ItemType Directory -Path ".resonance" | Out-Null
    Write-Host "Created .resonance directory." -ForegroundColor Gray
}

# Copy templates to the .resonance directory
Copy-Item "templates\*.md" -Destination ".resonance\" -Force

Write-Host "✅ Resonance initialized. Memory bank created at .resonance/" -ForegroundColor Green
Write-Host "Next step: Install the adapter for your IDE from the adapters/ folder." -ForegroundColor Yellow
