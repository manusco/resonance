# Legacy `/ship` workflow

## Input

- An approved implementation plan and a named release branch.
- A clean working tree, or an explicit list of changes included in the release.
- The repository's documented test, lint, and security-check commands.

## Steps

1. Confirm the approved scope and inspect the branch diff.
2. Run the relevant tests, linter, and security checks. Record command results and resolve failures before continuing.
3. Prepare the changelog entry and proposed version bump. Ask the release owner to approve both before changing release metadata.
4. Commit the approved release changes, push the branch to GitHub, and open a pull request with the scope, checks, and known risks.
5. Wait for required CI and reviewer approval. Do not merge without explicit authorization from the release owner.
6. After merge, hand off the release notes and any follow-up steps to the operator. Deployment is performed by the operator through their established process.

## Output

- A reviewable GitHub pull request for the approved release scope.
- A record of the checks run, version proposal, and handoff notes.

## Definition of Done

- The diff stays within the approved plan.
- Relevant tests, lint, and security checks pass, with their actual results recorded.
- The release owner approves the changelog and version metadata.
- The pull request is open with required CI complete and reviewer approval recorded, or the workflow stops with the unresolved blocker named.
- No merge or deployment is claimed unless it actually occurred with explicit authorization.

## Approval gates

- Ask before pushing release changes or opening the pull request unless the user has explicitly authorized those GitHub actions in the current task.
- Ask before merging. A successful check run does not authorize a merge.

## Recovery

- If checks fail twice for the same issue, stop and route to `/debug` with the failing command and evidence.
- If the approved scope or version is disputed, stop and return the decision to the release owner.
- If GitHub is unavailable, preserve the local branch and report the exact blocked handoff.

## Boundaries

- This workflow ends at GitHub branch and pull-request handling.
- Deployment, production migrations, backups, server access, SSH, and infrastructure settings remain operator-owned and out of scope.
