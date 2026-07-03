# Toolchain Detection: run the project's commands, not npm by reflex

> Not every project is a Node project. Before you run tests, a build, or a linter, detect what the project actually uses and run that. Hardcoding `npm test` fails silently on a Python, Go, Rust, or pnpm project. Read the repo, then run the right command.

## Detect, in this order

Look for the marker file and use its ecosystem's commands. Stop at the first match, but a repo can be polyglot (a frontend and a backend); handle each part.

- **`package.json`** (Node/JS/TS): the package manager is the lockfile. `pnpm-lock.yaml` means pnpm, `yarn.lock` means yarn, `bun.lockb` means bun, otherwise npm. Run the scripts that exist in `package.json` (`test`, `build`, `lint`, `typecheck`); do not assume a script is defined, read it first.
- **`pyproject.toml` / `setup.py` / `requirements.txt`** (Python): tests are usually `pytest` (or `python -m pytest`), lint `ruff` or `flake8`, types `mypy`. Check for a `tox.ini` or a `[tool.*]` config.
- **`go.mod`** (Go): `go test ./...`, `go build ./...`, `go vet ./...`.
- **`Cargo.toml`** (Rust): `cargo test`, `cargo build`, `cargo clippy`.
- **`Gemfile`** (Ruby): `bundle exec rspec` or `rake test`.
- **`composer.json`** (PHP): `composer test` or `phpunit`.
- **`pom.xml` / `build.gradle`** (Java/Kotlin): `mvn test` / `./gradlew test`.
- **A `Makefile`** with `test` / `build` targets: prefer `make test`, `make build`; the project author chose those on purpose.
- **CI config** (`.github/workflows/*`, `.gitlab-ci.yml`): the canonical commands are whatever CI runs. When in doubt, mirror CI.

## The rules

- **Read before you run.** Confirm the script or target exists. `npm run build` on a project with no `build` script is a failure you caused, not a real result.
- **Prefer the project's own entry points.** A `Makefile` target or a `package.json` script encodes the author's intent, including flags you would otherwise miss.
- **Polyglot repos:** run each part's commands (the web app's tests and the API's tests), not just the first one found.
- **No runnable check exists:** that is a gap to surface, not a pass. Say the project has no test or build command rather than pretending one ran.
