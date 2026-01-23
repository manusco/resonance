# Tools - Command Boundaries

## Allowed Commands
These commands are safe to auto-run:
- `ls`, `dir` - List files
- `cat`, `type` - Read files
- `git status`, `git log` - Check git status (read-only)
- `npm test` - Run tests
- `npm run dev` - Start dev server

## Requires Approval
These commands need user approval:
- `git commit` - Commits code changes
- `git push` - Pushes to remote
- `npm install` - Installs dependencies
- `rm`, `del` - Deletes files
- Any destructive operations

## Forbidden
These commands should never be run:
- `rm -rf /` or equivalent
- `format` - Disk formatting
- System-level changes
- Anything that could cause data loss

## Terminal Access Philosophy
Resonance leverages Google Antigravity's terminal access responsibly. The agent can run analysis and build commands autonomously, but destructive operations require user approval.

---

**Note**: This file defines what the agent can/cannot do with terminal access.

---

[→ Back to State (Active Context)](01_state.md)
