# Git Mastery Protocol

> "Git is a time machine. Use it to save your future self."

## 1. The Bisect (Bug Hunting)
When a bug appears, and you don't know when it started.

```bash
git bisect start
git bisect bad HEAD
git bisect good <commit-hash-from-last-week>
# Git will checkout the middle commit.
# Test it.
git bisect good # or bad
# Repeat until it says "c6d12f is the first bad commit".
```

## 2. The Reflog (The Safety Net)
"I just deleted my branch!" -> No you didn't.

```bash
git reflog
# Find the hash where you were before the disaster.
git checkout -b recovery-branch <hash>
```

## 3. The Interactive Rebase (Cleanup)
Never merge "fix typo", "fix again", "wip" into main. Squash them.

```bash
git rebase -i HEAD~3
# Change 'pick' to 'squash' (s) for the typo fixes.
```

## 4. The Mandate

*   **Atomic Commits**: One feature per commit.
*   **Conventional Commits**: `feat: add user login` (Not `wip`).

> 🔴 **Rule**: Never force push to shared branches.
