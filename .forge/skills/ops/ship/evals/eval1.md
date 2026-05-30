---
query: "Run /ship to deploy v1.2.0"
expected_behavior: "The agent checks that the branch is main and CI is green. It runs pre-flight checks, writes the changelog, makes logical commits, tags the release, and pushes."
---
