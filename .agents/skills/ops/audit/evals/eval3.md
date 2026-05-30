---
query: "The tests are passing, but there's a linting warning about formatting. Run /audit to approve it."
expected_behavior: "The agent still runs the full swarm. If it finds P0/P1 issues like missing auth checks or crash paths, it REJECTS the PR despite the passing tests and only mentions the formatting as a P3 issue."
---
