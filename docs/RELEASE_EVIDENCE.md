# Release Evidence

Every public release must be reproducible from the tested `main` commit.

Minimum release evidence:

- CI passed on the release commit.
- `py .forge/tests/run.py` passed.
- `py .forge/validate_skill.py --all --strict .agents/skills` passed.
- `py .forge/validate_library.py --strict` passed.
- `py .forge/doc_drift.py` passed.
- `py .forge/run_evals.py --all --check` passed.
- `py .forge/orch_eval.py --check` passed.
- `.forge/release_manifest.py` produced `release-manifest.json` and
  `SHA256SUMS`.

The release workflow creates the tag and GitHub Release from `main`. Do not move
published tags. If a release is wrong, fix forward with a new version.
