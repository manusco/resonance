# Resonance Scripts

This directory contains utility scripts for the Resonance framework.

## safe-commit

**Purpose:** Atomic, controlled git commits with safety guardrails.

**Available versions:**
- `safe-commit.sh` - Bash (Linux/macOS)
- `safe-commit.ps1` - PowerShell (Windows/cross-platform)

### Usage

**Syntax:**
```bash
# Bash
./.resonance/scripts/safe-commit.sh [--force] "commit message" "file1" "file2" ...

# PowerShell
.\.resonance\scripts\safe-commit.ps1 [-Force] "commit message" "file1" "file2" ...
```

**Examples:**
```bash
# Commit specific files
./.resonance/scripts/safe-commit.sh "feat: add authentication" "src/auth.js" "src/config.js"

# Force removal of stale lock file
./.resonance/scripts/safe-commit.sh --force "fix: resolve merge conflict" "README.md"
```

```powershell
# Commit specific files (PowerShell)
.\.resonance\scripts\safe-commit.ps1 "feat: add authentication" "src/auth.js" "src/config.js"

# Force removal of stale lock file (PowerShell)
.\.resonance\scripts\safe-commit.ps1 -Force "fix: resolve merge conflict" "README.md"
```

### Safety Features

1. **No accidental full staging**: Rejects `.` as a file argument to prevent `git add .`
2. **File validation**: Verifies all files exist or are tracked before staging
3. **Atomic commits**: Clears staging area and stages only specified files
4. **Empty commit prevention**: Fails if no changes are detected
5. **Lock file handling**: `--force` flag removes stale `.git/index.lock` files
6. **Message validation**: Ensures commit message is not empty and not a file path

### How It Works

1. Validates commit message and file arguments
2. Clears the current staging area (`git restore --staged :/`)
3. Stages only the specified files (`git add -A -- <files>`)
4. Verifies changes exist in staging area
5. Creates commit with specified message
6. If commit fails due to lock file and `--force` is set, removes lock and retries

### Exit Codes

- `0` - Success
- `1` - Commit failed (validation error, no changes, or git error)
- `2` - Invalid usage (missing arguments)

### When to Use

Use `safe-commit` when you want to ensure:
- Only specific files are committed (avoid accidental inclusions)
- Atomic changesets (multiple files as one logical unit)
- No orphaned staging area state after failed commits
- Protection against accidentally staging the entire repository
