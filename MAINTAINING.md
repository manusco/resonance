# Maintaining Resonance

This guide keeps routine maintenance small, visible, and repeatable.

## Community routes

| Request | Route |
| :--- | :--- |
| Usage question | GitHub Discussions |
| Reproducible defect | Bug report issue form |
| Skill contract gap | Skill field report form |
| Improvement proposal | Proposal issue form |
| Suspected vulnerability | Private vulnerability report |
| Code change | Pull request |

Keep support questions out of Issues. Keep security reports private. Close duplicate or incomplete reports with a short reason and a link to the correct route.

## Versioning

Resonance uses [Semantic Versioning](https://semver.org/) in the form `MAJOR.MINOR.PATCH`.

- Increase `MAJOR` for an incompatible framework or migration change.
- Increase `MINOR` for a backward-compatible capability, skill, or substantial feature.
- Increase `PATCH` for backward-compatible fixes, protocol improvements, documentation, tests, and repository maintenance.

Treat each part as an integer, not a decimal. For example, `2.4.10` follows `2.4.9`. Published historical tags remain unchanged. From `v2.4.87` onward, every release must be greater than all existing release tags. The next patch release is `v2.4.88`.

## Prepare a release

Use one pull request for the release candidate.

1. Update the version in every surface checked by `.forge/doc_drift.py`.
2. Add a concise `CHANGELOG.md` entry for that exact version.
3. Rebuild generated files.
4. Run the local gate in [CONTRIBUTING.md](CONTRIBUTING.md).
5. Merge only after CI passes and the diff has been reviewed.

Do not publish a release from an unmerged branch. Do not move or replace a published tag.

## Publish a release

Run the **Publish release** workflow from the `main` branch in GitHub Actions. It reads the version from `package.json`, extracts the matching changelog section, verifies that the version is new and increasing, repeats the release gate, then creates the tag and GitHub Release at the tested commit.

After it finishes, confirm that:

- the release appears under GitHub Releases;
- the tag points to the intended `main` commit;
- the README release badge opens the new release;
- `main` is clean and CI is green.

## Routine maintenance

- Review new Discussions and Issues when practical. Route first, then investigate.
- Merge Dependabot pull requests only after CI passes and the action release notes are acceptable.
- Review private vulnerability reports before public disclosure.
- Keep the support, security, contribution, and release documents accurate when repository behavior changes.

No public roadmap, response-time promise, or release cadence is required. Publish when a reviewed change is ready.
