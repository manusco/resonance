#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Safe atomic git commit helper
.DESCRIPTION
    Stages only specified files and creates a commit with validation.
    Prevents accidental staging of entire repository and handles git lock files.
.PARAMETER Message
    Commit message (required, non-empty)
.PARAMETER Files
    List of files to stage and commit
.PARAMETER Force
    Attempt to remove stale git lock files if commit fails
.EXAMPLE
    .\safe-commit.ps1 "feat: add new feature" "src/file1.ts" "src/file2.ts"
.EXAMPLE
    .\safe-commit.ps1 -Force "fix: resolve bug" "README.md"
#>

param(
    [Parameter(Mandatory=$false)]
    [switch]$Force,
    
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Message,
    
    [Parameter(Mandatory=$true, Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$Files
)

$ErrorActionPreference = 'Stop'

# Validate commit message is not empty
if ([string]::IsNullOrWhiteSpace($Message)) {
    Write-Error "Error: commit message must not be empty"
    exit 1
}

# Prevent accidentally passing a file path as commit message
if (Test-Path $Message -PathType Any) {
    Write-Error "Error: first argument looks like a file path ('$Message'); provide the commit message first"
    exit 1
}

# Validate files array is not empty
if ($Files.Count -eq 0) {
    Write-Error "Error: at least one file must be specified"
    exit 1
}

# Disallow "." to prevent accidental staging of entire repository
foreach ($file in $Files) {
    if ($file -eq ".") {
        Write-Error 'Error: "." is not allowed; list specific paths instead'
        exit 1
    }
}

# Verify files exist or are staged for deletion
foreach ($file in $Files) {
    if (-not (Test-Path $file)) {
        # Check if file is tracked in git
        $isTracked = git ls-files --error-unmatch -- $file 2>$null
        $isInHead = git cat-file -e "HEAD:$file" 2>$null
        
        if (-not $isTracked -and -not $isInHead) {
            Write-Error "Error: file not found: $file"
            exit 1
        }
    }
}

# Clear staging area and stage only specified files
git restore --staged :/ 2>$null
git add -A -- $Files

# Verify there are changes to commit
$stagedChanges = git diff --staged --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Warning "Warning: no staged changes detected for: $($Files -join ', ')"
    exit 1
}

# Attempt commit
$committed = $false
$lastError = $null

try {
    git commit -m $Message -- $Files 2>&1 | Tee-Object -Variable commitOutput | Out-Null
    $committed = $true
}
catch {
    $lastError = $_
}

# Handle stale lock file if --force is specified
if (-not $committed -and $Force) {
    # Extract lock path from error message
    $lockPattern = "Unable to create '(.+\.git[/\\]index\.lock)'"
    if ($commitOutput -match $lockPattern) {
        $lockPath = $matches[1]
        
        if (Test-Path $lockPath) {
            Remove-Item -Path $lockPath -Force
            Write-Warning "Removed stale git lock: $lockPath"
            
            # Retry commit
            try {
                git commit -m $Message -- $Files
                $committed = $true
            }
            catch {
                # Commit still failed after lock removal
            }
        }
    }
}

if (-not $committed) {
    Write-Error "Commit failed"
    exit 1
}

Write-Host "Committed '$Message' with $($Files.Count) file(s)" -ForegroundColor Green
