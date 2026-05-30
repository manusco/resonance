# PowerShell Automation Protocol

> "Automate the Windows world."

## 1. The Safety Net

Always enable strict mode at the top.

```powershell
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
```

## 2. The Object Pipeline

Don't parse text. Pass Objects.

*   ❌ `Get-Service | Select-String "Running"`
*   ✅ `Get-Service | Where-Object { $_.Status -eq 'Running' }`

## 3. Functions (Verbs)

Use standard verbs (`Get`, `Set`, `New`, `Remove`).

```powershell
function New-ResonanceUser {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Username
    )
    # ...
}
```

> 🔴 **Rule**: Never run `Invoke-Expression` (IEX) on remote strings.
